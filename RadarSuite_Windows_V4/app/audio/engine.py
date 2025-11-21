"""
RadarSuite v3.5.0 - Audio Engine
Audio capture via sounddevice/soundcard
"""

import time
import queue
import threading
import numpy as np

try:
    import sounddevice as sd
except ImportError:
    sd = None

try:
    import soundcard as sc
except ImportError:
    sc = None

from core.logger import log


class AudioEngine:
    """
    Audio capture engine supporting:
    - sounddevice (standard input devices)
    - soundcard loopback (capture from speaker output)
    """

    def __init__(self):
        log("AudioEngine.__init__", "INFO")
        self.sample_rate = 48000
        self.blocksize = 2048
        self.channels = 2
        self.device = None
        self.stream = None
        self.queue = queue.Queue(maxsize=8)
        self.last_block = None
        self.running = False
        self.backend = "sounddevice"
        self.use_loopback = False

    def list_devices(self):
        """List available audio devices"""
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
                        'name': f"{spk.name} (Loopback)",
                        'channels': spk.channels,
                        'samplerate': 48000,
                        'hostapi': 'soundcard',
                        'type': 'loopback',
                        'backend': 'soundcard',
                        'speaker_obj': spk
                    })
            except Exception as e:
                log(f"Error listing soundcard devices: {e}", "ERROR")

        return devices

    def start(self):
        """Start audio capture"""
        if self.running:
            log("AudioEngine already running", "WARN")
            return

        self.running = True

        if self.use_loopback and sc is not None:
            log(f"Starting soundcard loopback: {self.sample_rate}Hz, {self.blocksize} samples", "INFO")
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
        """Start soundcard loopback capture"""
        import threading

        def loopback_thread():
            try:
                spk = sc.default_speaker()
                log(f"Using speaker: {spk.name}, channels: {spk.channels}", "INFO")

                with spk.recorder(samplerate=self.sample_rate, channels=self.channels, blocksize=self.blocksize) as rec:
                    while self.running:
                        data = rec.record(numframes=self.blocksize)
                        self.last_block = data.copy()

                        try:
                            self.queue.put_nowait(data.copy())
                        except queue.Full:
                            pass

            except Exception as e:
                log(f"Error in loopback thread: {e}", "ERROR")
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

