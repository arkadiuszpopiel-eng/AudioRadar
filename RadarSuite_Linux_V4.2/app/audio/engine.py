"""
RadarSuite v4.2.0 - Audio Engine (Linux)
Audio capture via sounddevice/soundcard/PulseAudio

LINUX VERSION: Uses PulseAudio/PipeWire monitor sources for loopback
"""

import time
import queue
import threading
import numpy as np
import sys
import subprocess

# FIXED v3.5.4: Proper numpy compatibility wrapper for soundcard library
# numpy.fromstring was removed in numpy 2.0, soundcard may use it internally
_original_frombuffer = np.frombuffer
def _fromstring_compat(string, dtype=float, count=-1, sep='', **kwargs):
    """Compatibility wrapper: numpy.fromstring -> numpy.frombuffer"""
    if sep == '' or sep is None:
        return _original_frombuffer(string, dtype=dtype, count=count)
    else:
        raise NotImplementedError("Text mode fromstring not supported in compat shim")

if not hasattr(np, 'fromstring'):
    np.fromstring = _fromstring_compat

try:
    import sounddevice as sd
except ImportError:
    sd = None

try:
    import soundcard as sc
except ImportError:
    sc = None

# Linux: Try pulsectl for PulseAudio control (optional, for better device listing)
PULSECTL_AVAILABLE = False
pulsectl = None

try:
    import pulsectl
    PULSECTL_AVAILABLE = True
except ImportError:
    pass

from core.logger import log

# Log PulseAudio availability at module load
if PULSECTL_AVAILABLE:
    log("pulsectl loaded successfully (PulseAudio control)", "INFO")
else:
    log("pulsectl NOT available - using soundcard for PulseAudio loopback", "INFO")


class AudioEngine:
    """
    Audio capture engine supporting:
    - sounddevice (standard input devices)
    - soundcard loopback (capture from speaker output via PulseAudio monitor)
    - PulseAudio/PipeWire native loopback

    LINUX VERSION v4.2.0: Optimized for PulseAudio/PipeWire
    FIXED v4.1.2: Auto-detection of channel count for 5.1/7.1 support
    """

    def __init__(self):
        log("AudioEngine.__init__ (Linux)", "INFO")
        self.sample_rate = 48000
        self.blocksize = 2048
        self.channels = 2  # Default, will be auto-detected
        self.requested_channels = 0  # 0 = auto-detect from device
        self.actual_channels = 2  # What we actually got from device
        self.device = None
        self.stream = None
        self.queue = queue.Queue(maxsize=8)
        self.last_block = None
        self.running = False
        self.backend = "sounddevice"
        self.use_loopback = False

        # FIXED v4.1.2: Channel layout info for spatial audio
        self.channel_layout = "stereo"  # "stereo", "5.1", "7.1"
        self.has_surround = False  # True if 5.1 or higher

    def list_devices(self):
        """List available audio devices including PulseAudio monitors"""
        devices = []

        if sd is not None:
            try:
                sd_devices = sd.query_devices()
                for idx, dev in enumerate(sd_devices):
                    devices.append({
                        'index': idx,
                        'name': dev['name'],
                        'channels': dev['max_input_channels'],
                        'samplerate': int(dev['default_samplerate']),
                        'hostapi': sd.query_hostapis(dev['hostapi'])['name'],
                        'type': 'input' if dev['max_input_channels'] > 0 else 'output',
                        'backend': 'sounddevice'
                    })
            except Exception as e:
                log(f"Error listing sounddevice devices: {e}", "ERROR")

        if sc is not None:
            try:
                speakers = sc.all_speakers()
                for idx, spk in enumerate(speakers):
                    devices.append({
                        'index': f"loopback_{idx}",
                        'name': f"{spk.name} (Loopback/Monitor)",
                        'channels': spk.channels,
                        'samplerate': 48000,
                        'hostapi': 'PulseAudio',
                        'type': 'loopback',
                        'backend': 'soundcard',
                        'speaker_obj': spk
                    })
            except Exception as e:
                log(f"Error listing soundcard devices: {e}", "ERROR")

        # Additional: List PulseAudio monitor sources via pulsectl
        if PULSECTL_AVAILABLE:
            try:
                with pulsectl.Pulse('radarsuite-list') as pulse:
                    for source in pulse.source_list():
                        if '.monitor' in source.name:
                            devices.append({
                                'index': f"pulse_monitor_{source.index}",
                                'name': f"{source.description} (PulseAudio Monitor)",
                                'channels': source.channel_count,
                                'samplerate': source.sample_spec.rate,
                                'hostapi': 'PulseAudio',
                                'type': 'loopback',
                                'backend': 'pulsectl',
                                'pulse_name': source.name
                            })
            except Exception as e:
                log(f"Error listing PulseAudio monitors: {e}", "ERROR")

        return devices

    def start(self):
        """Start audio capture"""
        if self.running:
            log("AudioEngine already running", "WARN")
            return

        self.running = True

        if self.use_loopback and sc is not None:
            log(f"Starting PulseAudio loopback: {self.sample_rate}Hz, {self.blocksize} samples", "INFO")
            self._start_loopback()
        else:
            log(f"Starting sounddevice: device={self.device}, {self.sample_rate}Hz, {self.blocksize} samples", "INFO")
            self._start_sounddevice()

    def _start_sounddevice(self):
        """Start sounddevice input stream"""
        try:
            def callback(indata, frames, time_info, status):
                if status:
                    log(f"sounddevice status: {status}", "WARN")

                data = indata.copy()
                self.last_block = data

                try:
                    self.queue.put_nowait(data)
                except queue.Full:
                    pass

            self.stream = sd.InputStream(
                device=self.device,
                channels=self.channels,
                samplerate=self.sample_rate,
                blocksize=self.blocksize,
                callback=callback
            )
            self.stream.start()
            log(f"sounddevice stream started successfully", "INFO")

        except Exception as e:
            log(f"Error starting sounddevice: {e}", "ERROR")
            self.running = False

    def _start_loopback(self):
        """Start loopback capture via soundcard (PulseAudio monitor on Linux)"""

        if sc is not None:
            log("Starting loopback via soundcard (PulseAudio monitor)", "INFO")
            self._start_loopback_soundcard()
        else:
            log("No loopback backend available! Install soundcard: pip install soundcard", "ERROR")
            self.running = False

    def _start_loopback_soundcard(self):
        """Start soundcard loopback capture via PulseAudio monitor"""

        def loopback_thread():
            try:
                # FIXED v3.5.4: Apply numpy patch again inside thread with proper wrapper
                import numpy as _np
                if not hasattr(_np, 'fromstring'):
                    _np.fromstring = _fromstring_compat
                    log("Numpy fromstring patched in loopback thread", "INFO")

                spk = sc.default_speaker()
                log(f"Using speaker: {spk.name}, channels: {spk.channels}", "INFO")

                # LINUX v4.2.0: Auto-detect channel count from speaker
                device_channels = spk.channels

                # Use device's native channel count if auto-detect (0) or requested > available
                if self.requested_channels == 0 or self.requested_channels > device_channels:
                    channels = device_channels
                else:
                    channels = self.requested_channels

                # Update engine's actual channel count
                self.actual_channels = channels

                # Determine channel layout for spatial audio
                if channels >= 8:
                    self.channel_layout = "7.1"
                    self.has_surround = True
                elif channels >= 6:
                    self.channel_layout = "5.1"
                    self.has_surround = True
                else:
                    self.channel_layout = "stereo"
                    self.has_surround = False

                log(f"PulseAudio loopback: {spk.name}", "INFO")
                log(f"  Device channels: {device_channels}, Using: {channels} ({self.channel_layout})", "INFO")
                log(f"  Sample rate: {self.sample_rate}Hz, Surround: {self.has_surround}", "INFO")

                # Use get_microphone with include_loopback for PulseAudio monitor
                loopback_mic = sc.get_microphone(id=str(spk.id), include_loopback=True)
                log(f"Loopback microphone (monitor): {loopback_mic.name}", "INFO")

                with loopback_mic.recorder(samplerate=self.sample_rate, channels=channels, blocksize=self.blocksize) as rec:
                    while self.running:
                        data = rec.record(numframes=self.blocksize)
                        self.last_block = data.copy()

                        try:
                            self.queue.put_nowait(data.copy())
                        except queue.Full:
                            pass

            except Exception as e:
                log(f"Error in PulseAudio loopback thread: {e}", "ERROR")
                import traceback
                log(f"Traceback: {traceback.format_exc()}", "DEBUG")
                self.running = False

        thread = threading.Thread(target=loopback_thread, daemon=True)
        thread.start()

    def stop(self):
        """
        Stop audio capture with automatic retry

        ENHANCED v3.5.0: Retry logic prevents hangs on device errors
        """
        if not self.running:
            return

        log("Stopping AudioEngine", "INFO")
        self.running = False

        if self.stream is not None:
            retry_count = 0
            max_retries = 3

            while retry_count < max_retries:
                try:
                    self.stream.stop()
                    self.stream.close()
                    self.stream = None
                    log("Audio stream stopped successfully", "INFO")
                    break  # Success
                except Exception as e:
                    retry_count += 1
                    log(f"Error stopping stream (attempt {retry_count}/{max_retries}): {e}", "WARNING")

                    if retry_count < max_retries:
                        time.sleep(0.5)  # Wait before retry
                    else:
                        log("Failed to stop stream after retries, forcing cleanup", "ERROR")
                        self.stream = None  # Force cleanup to prevent memory leak

    def read_block(self, timeout=0.0):
        """Read audio block from queue"""
        try:
            return self.queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def get_pulseaudio_info(self):
        """Get PulseAudio/PipeWire system info (Linux only)"""
        info = {
            'available': False,
            'server': None,
            'version': None,
            'default_sink': None
        }

        try:
            # Try pactl for PulseAudio info
            result = subprocess.run(
                ['pactl', 'info'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                info['available'] = True
                for line in result.stdout.split('\n'):
                    if 'Server Name:' in line:
                        info['server'] = line.split(':', 1)[1].strip()
                    elif 'Server Version:' in line:
                        info['version'] = line.split(':', 1)[1].strip()
                    elif 'Default Sink:' in line:
                        info['default_sink'] = line.split(':', 1)[1].strip()
        except Exception as e:
            log(f"Could not get PulseAudio info: {e}", "DEBUG")

        return info
