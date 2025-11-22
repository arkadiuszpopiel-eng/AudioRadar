"""
RadarSuite v3.5.0 - Audio Engine
Audio capture via sounddevice/soundcard/pyaudiowpatch
"""

import time
import queue
import threading
import numpy as np
import sys

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

# FIXED v3.5.4: Try pyaudiowpatch for WASAPI loopback (more reliable than soundcard)
try:
    import pyaudiowpatch as pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    pyaudio = None
    PYAUDIO_AVAILABLE = False

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
        """Start loopback capture - tries pyaudiowpatch first, falls back to soundcard"""

        # FIXED v3.5.4: Use pyaudiowpatch for WASAPI loopback (most reliable)
        if PYAUDIO_AVAILABLE and sys.platform == 'win32':
            log("Attempting loopback via pyaudiowpatch (WASAPI)", "INFO")
            if self._start_loopback_pyaudio():
                return
            log("pyaudiowpatch failed, trying soundcard fallback", "WARN")

        # Fallback to soundcard
        if sc is not None:
            log("Attempting loopback via soundcard", "INFO")
            self._start_loopback_soundcard()
        else:
            log("No loopback backend available!", "ERROR")
            self.running = False

    def _start_loopback_pyaudio(self):
        """Start WASAPI loopback using pyaudiowpatch (preferred method)"""
        try:
            def loopback_thread():
                p = None
                stream = None
                try:
                    p = pyaudio.PyAudio()

                    # Find WASAPI loopback device
                    wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
                    default_speakers = p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])

                    log(f"WASAPI loopback device: {default_speakers['name']}", "INFO")
                    log(f"  Channels: {default_speakers['maxOutputChannels']}, Rate: {default_speakers['defaultSampleRate']}", "INFO")

                    # Use speaker's native settings
                    channels = min(self.channels, int(default_speakers["maxOutputChannels"]))
                    sample_rate = int(default_speakers["defaultSampleRate"])

                    # Open loopback stream
                    stream = p.open(
                        format=pyaudio.paFloat32,
                        channels=channels,
                        rate=sample_rate,
                        frames_per_buffer=self.blocksize,
                        input=True,
                        input_device_index=default_speakers["index"],
                        as_loopback=True
                    )

                    log(f"pyaudiowpatch loopback started: {sample_rate}Hz, {channels}ch", "INFO")

                    while self.running:
                        try:
                            raw_data = stream.read(self.blocksize, exception_on_overflow=False)
                            data = np.frombuffer(raw_data, dtype=np.float32)

                            # Reshape to (frames, channels)
                            if channels > 1:
                                data = data.reshape(-1, channels)
                            else:
                                data = data.reshape(-1, 1)

                            self.last_block = data.copy()

                            try:
                                self.queue.put_nowait(data.copy())
                            except queue.Full:
                                pass

                        except Exception as e:
                            if self.running:
                                log(f"Loopback read error: {e}", "WARN")
                            break

                except Exception as e:
                    log(f"Error in pyaudiowpatch loopback thread: {e}", "ERROR")
                    self.running = False
                finally:
                    if stream is not None:
                        try:
                            stream.stop_stream()
                            stream.close()
                        except:
                            pass
                    if p is not None:
                        try:
                            p.terminate()
                        except:
                            pass

            thread = threading.Thread(target=loopback_thread, daemon=True)
            thread.start()
            return True

        except Exception as e:
            log(f"Failed to start pyaudiowpatch loopback: {e}", "ERROR")
            return False

    def _start_loopback_soundcard(self):
        """Start soundcard loopback capture (fallback method)"""

        def loopback_thread():
            # FIXED v3.5.3: Initialize COM on Windows for WASAPI loopback
            com_initialized = False
            if sys.platform == 'win32':
                # Try pythoncom first, then fallback to ctypes
                try:
                    import pythoncom
                    pythoncom.CoInitialize()
                    com_initialized = True
                    log("COM initialized via pythoncom", "INFO")
                except ImportError:
                    # Fallback: use ctypes to initialize COM
                    try:
                        import ctypes
                        ctypes.windll.ole32.CoInitialize(None)
                        com_initialized = True
                        log("COM initialized via ctypes", "INFO")
                    except Exception as e:
                        log(f"COM init failed (ctypes): {e}", "WARN")
                except Exception as e:
                    log(f"COM init error: {e}", "WARN")

            try:
                # FIXED v3.5.4: Apply numpy patch again inside thread with proper wrapper
                import numpy as _np
                if not hasattr(_np, 'fromstring'):
                    _np.fromstring = _fromstring_compat
                    log("Numpy fromstring patched in loopback thread", "INFO")

                spk = sc.default_speaker()
                log(f"Using speaker: {spk.name}, channels: {spk.channels}", "INFO")

                # FIXED v3.5.3: Use get_microphone with include_loopback for WASAPI loopback
                loopback_mic = sc.get_microphone(id=str(spk.id), include_loopback=True)
                log(f"Loopback microphone: {loopback_mic.name}", "INFO")

                with loopback_mic.recorder(samplerate=self.sample_rate, channels=self.channels, blocksize=self.blocksize) as rec:
                    while self.running:
                        data = rec.record(numframes=self.blocksize)
                        self.last_block = data.copy()

                        try:
                            self.queue.put_nowait(data.copy())
                        except queue.Full:
                            pass

            except Exception as e:
                log(f"Error in soundcard loopback thread: {e}", "ERROR")
                self.running = False
            finally:
                # Cleanup COM
                if com_initialized and sys.platform == 'win32':
                    try:
                        import ctypes
                        ctypes.windll.ole32.CoUninitialize()
                    except:
                        pass

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

