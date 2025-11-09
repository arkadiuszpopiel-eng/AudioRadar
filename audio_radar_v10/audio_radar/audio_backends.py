"""Optimized audio backend for AudioRadar v10.0.

This module provides low-latency audio capture using PyAudioWPatch for WASAPI
loopback support on Windows. It features thread priority boosting, optimized
buffer management, and graceful error handling.

The module is designed to minimize audio processing latency while maintaining
reliability. Default buffer size is optimized for ~10ms latency at 48kHz.
"""

from __future__ import annotations
from collections import deque
from typing import Optional, Callable, List, Tuple
import threading
import logging

# v10.0: Audio backend with WASAPI loopback support
try:
    import pyaudiowpatch as pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    try:
        import pyaudio
        PYAUDIO_AVAILABLE = True
    except ImportError:
        pyaudio = None  # type: ignore
        PYAUDIO_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    np = None  # type: ignore
    NUMPY_AVAILABLE = False


# v10.0: Optimized default buffer size for ~10ms latency at 48kHz
DEFAULT_BUFFER_FRAMES = 128  # was 256 in v9.9.32
DEFAULT_SAMPLE_RATE = 48000
DEFAULT_CHANNELS = 2


class LevelBuffer:
    """Thread-safe buffer for audio level data.
    
    This buffer uses a deque for efficient FIFO operations and provides
    methods for both standard pop (oldest value) and pop_latest (newest
    value, discarding intermediate values).
    """
    
    def __init__(self, maxsize: int = 100):
        """Initialize the level buffer.
        
        Parameters
        ----------
        maxsize : int
            Maximum number of items to store before old items are dropped.
        """
        self.q = deque(maxlen=maxsize)
        self._lock = threading.Lock()
    
    def push(self, value: float) -> None:
        """Add a value to the buffer.
        
        Parameters
        ----------
        value : float
            Level value to add.
        """
        with self._lock:
            self.q.append(value)
    
    def pop(self) -> Optional[float]:
        """Remove and return the oldest value.
        
        Returns
        -------
        float or None
            Oldest value, or None if buffer is empty.
        """
        with self._lock:
            try:
                return self.q.popleft()
            except IndexError:
                return None
    
    # v10.0: Optimized pop that gets latest value only
    def pop_latest(self) -> Optional[float]:
        """Pop only latest value, discard old ones.
        
        This method is more efficient when you only care about the most
        recent value and want to skip over any accumulated backlog.
        It pops from the right (newest) and discards all older values.
        
        Returns
        -------
        float or None
            Most recent value, or None if buffer is empty.
        """
        with self._lock:
            try:
                # Pop the latest (rightmost) value first
                latest = self.q.pop()
                # Discard all older values
                self.q.clear()
                return latest
            except IndexError:
                return None
    
    def clear(self) -> None:
        """Remove all values from the buffer."""
        with self._lock:
            self.q.clear()
    
    def __len__(self) -> int:
        """Return the number of items in the buffer."""
        return len(self.q)


class PyAudioInput:
    """Low-latency audio input using PyAudio/PyAudioWPatch.
    
    This class provides optimized audio capture with thread priority boosting
    for minimal latency. It supports both standard audio inputs and WASAPI
    loopback devices on Windows.
    
    Attributes
    ----------
    device_index : int or None
        Index of the audio device to use.
    sample_rate : int
        Sample rate in Hz.
    buffer_frames : int
        Number of frames per buffer.
    channels : int
        Number of audio channels.
    """
    
    def __init__(
        self,
        device_index: Optional[int] = None,
        sample_rate: int = DEFAULT_SAMPLE_RATE,
        buffer_frames: int = DEFAULT_BUFFER_FRAMES,
        channels: int = DEFAULT_CHANNELS,
        logger: Optional[logging.Logger] = None
    ):
        """Initialize the PyAudio input.
        
        Parameters
        ----------
        device_index : int, optional
            Audio device index. If None, uses default input.
        sample_rate : int
            Sample rate in Hz (default: 48000).
        buffer_frames : int
            Buffer size in frames (default: 128).
        channels : int
            Number of channels (default: 2 for stereo).
        logger : logging.Logger, optional
            Logger instance for diagnostics.
        """
        if not PYAUDIO_AVAILABLE:
            raise RuntimeError("PyAudio or PyAudioWPatch is required but not available")
        
        self.device_index = device_index
        self.sample_rate = sample_rate
        self.buffer_frames = buffer_frames
        self.channels = channels
        self.logger = logger
        
        self.pa: Optional[pyaudio.PyAudio] = None
        self.stream = None
        self.callback: Optional[Callable[[np.ndarray], None]] = None
        self.is_running = False
        
        # v10.0: Thread priority boost for audio processing
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            current_thread = kernel32.GetCurrentThread()
            result = kernel32.SetThreadPriority(current_thread, 15)  # TIME_CRITICAL
            if self.logger and result:
                self.logger.info("Audio thread priority: TIME_CRITICAL")
        except Exception as e:
            if self.logger:
                self.logger.warning(f"Thread priority boost failed: {e}")
    
    def start(self, callback: Callable[[np.ndarray], None]) -> bool:
        """Start capturing audio.
        
        Parameters
        ----------
        callback : callable
            Function to call with each audio buffer. Receives numpy array
            of shape (frames, channels).
        
        Returns
        -------
        bool
            True if stream started successfully.
        """
        if not NUMPY_AVAILABLE:
            if self.logger:
                self.logger.error("NumPy is required but not available")
            return False
        
        self.callback = callback
        
        try:
            self.pa = pyaudio.PyAudio()
            
            # v10.0: Audio stream callback with optimized processing
            def audio_callback(in_data, frame_count, time_info, status):
                if status and self.logger:
                    self.logger.warning(f"Audio stream status: {status}")
                
                # Convert bytes to numpy array
                try:
                    audio_data = np.frombuffer(in_data, dtype=np.int16)
                    # Reshape to (frames, channels)
                    audio_data = audio_data.reshape(-1, self.channels)
                    # Normalize to float32 range [-1.0, 1.0]
                    audio_data = audio_data.astype(np.float32) / 32768.0
                    
                    if self.callback:
                        self.callback(audio_data)
                except Exception as e:
                    if self.logger:
                        self.logger.error(f"Audio callback error: {e}")
                
                return (in_data, pyaudio.paContinue)
            
            # Open stream
            self.stream = self.pa.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                input_device_index=self.device_index,
                frames_per_buffer=self.buffer_frames,
                stream_callback=audio_callback,
                start=False
            )
            
            self.stream.start_stream()
            self.is_running = True
            
            if self.logger:
                self.logger.info(
                    f"Audio stream started: {self.sample_rate}Hz, "
                    f"{self.buffer_frames} frames, {self.channels} channels"
                )
            
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to start audio stream: {e}")
            self.cleanup()
            return False
    
    def stop(self) -> None:
        """Stop capturing audio and clean up resources."""
        self.cleanup()
    
    def cleanup(self) -> None:
        """Clean up audio resources."""
        self.is_running = False
        
        if self.stream is not None:
            try:
                if self.stream.is_active():
                    self.stream.stop_stream()
                self.stream.close()
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error closing stream: {e}")
            finally:
                self.stream = None
        
        if self.pa is not None:
            try:
                self.pa.terminate()
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error terminating PyAudio: {e}")
            finally:
                self.pa = None
    
    def __del__(self):
        """Ensure cleanup on deletion."""
        self.cleanup()


def list_audio_devices() -> List[Tuple[int, str, bool]]:
    """List all available audio input devices.
    
    Returns
    -------
    list of tuple
        Each tuple contains (device_index, device_name, is_loopback).
        is_loopback indicates if the device supports WASAPI loopback.
    """
    if not PYAUDIO_AVAILABLE:
        return []
    
    devices = []
    pa = None
    
    try:
        pa = pyaudio.PyAudio()
        
        for i in range(pa.get_device_count()):
            try:
                info = pa.get_device_info_by_index(i)
                
                # Check if device has input channels
                if info.get('maxInputChannels', 0) > 0:
                    name = info.get('name', f'Device {i}')
                    
                    # v10.0: Check for WASAPI loopback support
                    is_loopback = 'loopback' in name.lower() or 'stereo mix' in name.lower()
                    
                    devices.append((i, name, is_loopback))
            except Exception:
                # Skip devices that can't be queried
                continue
        
    except Exception:
        pass
    finally:
        if pa is not None:
            try:
                pa.terminate()
            except Exception:
                pass
    
    return devices


def get_default_loopback_device() -> Optional[int]:
    """Get the default WASAPI loopback device index.
    
    Returns
    -------
    int or None
        Device index of the default loopback device, or None if not found.
    """
    devices = list_audio_devices()
    
    # Look for loopback devices
    loopback_devices = [idx for idx, name, is_loopback in devices if is_loopback]
    
    if loopback_devices:
        return loopback_devices[0]
    
    return None
