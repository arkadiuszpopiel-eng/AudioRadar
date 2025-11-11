"""Audio backend for AudioRadar v10.2 using sounddevice and WASAPI loopback.

This module handles audio capture from WASAPI loopback devices on Windows,
applies gain control, and emits peak/RMS levels and audio chunks for analysis.
"""

from __future__ import annotations
from typing import Callable, List, Tuple, Optional
import threading
import numpy as np

try:
    import sounddevice as sd
except ImportError:
    sd = None


def list_wasapi_loopback_devices() -> List[Tuple[int, str]]:
    """Return list of WASAPI loopback output devices.
    
    Returns
    -------
    List[Tuple[int, str]]
        List of (device_index, device_name) tuples for output devices
        that can be used for loopback capture on Windows.
    """
    if sd is None:
        return []
    
    devices = sd.query_devices()
    results: List[Tuple[int, str]] = []
    for idx, dev in enumerate(devices):
        # Look for output devices (max_output_channels > 0)
        if dev.get("max_output_channels", 0) > 0:
            name = dev.get("name", f"Device {idx}")
            results.append((idx, name))
    return results


class AudioWorker:
    """Worker for capturing audio with sounddevice and computing levels.
    
    This class captures audio from a WASAPI loopback device, applies
    gain control, and emits peak/RMS levels along with audio chunks.
    
    Parameters
    ----------
    device_index : Optional[int]
        Index of the audio device to capture from. If None, uses default.
    samplerate : int
        Sample rate in Hz (default: 44100).
    blocksize : int
        Number of frames per block (default: 1024).
    gain : float
        Gain multiplier (default: 1.0).
    
    Attributes
    ----------
    on_audio_data : Callable[[np.ndarray, float, float], None]
        Callback invoked with (audio_chunk, peak_level, rms_level).
    """
    
    def __init__(
        self,
        device_index: Optional[int] = None,
        samplerate: int = 44100,
        blocksize: int = 1024,
        gain: float = 1.0
    ):
        if sd is None:
            raise RuntimeError("sounddevice library is required")
        
        self.device_index = device_index
        self.samplerate = samplerate
        self.blocksize = blocksize
        self.gain = gain
        self.stream: Optional[sd.InputStream] = None
        self.running = False
        self.thread: Optional[threading.Thread] = None
        
        # Callback for audio data: (audio_chunk, peak, rms)
        self.on_audio_data: Callable[[np.ndarray, float, float], None] = lambda chunk, peak, rms: None
    
    def set_gain(self, gain: float) -> None:
        """Update the gain multiplier.
        
        Parameters
        ----------
        gain : float
            New gain value (typically 0.1 to 5.0).
        """
        self.gain = max(0.0, min(gain, 10.0))  # Clamp between 0 and 10
    
    def start(self) -> None:
        """Start audio capture in a background thread."""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()
    
    def stop(self) -> None:
        """Stop audio capture."""
        self.running = False
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        if self.thread is not None:
            self.thread.join(timeout=2.0)
            self.thread = None
    
    def _capture_loop(self) -> None:
        """Internal method to capture audio and emit data."""
        try:
            # Determine number of channels for the device
            if self.device_index is not None:
                device_info = sd.query_devices(self.device_index, 'input')
                channels = device_info.get('max_input_channels', 2)
            else:
                channels = 2
            
            # Open input stream
            self.stream = sd.InputStream(
                device=self.device_index,
                channels=channels,
                samplerate=self.samplerate,
                blocksize=self.blocksize,
                dtype='float32'
            )
            self.stream.start()
            
            # Read blocks while running
            while self.running:
                try:
                    data, overflowed = self.stream.read(self.blocksize)
                    if overflowed:
                        print("Warning: Audio buffer overflow detected")
                    
                    # Apply gain
                    data_gained = data * self.gain
                    
                    # Compute levels
                    if data_gained.size > 0:
                        # Convert to mono if stereo
                        if data_gained.ndim == 2:
                            mono = data_gained.mean(axis=1)
                        else:
                            mono = data_gained.ravel()
                        
                        peak = float(np.max(np.abs(mono)))
                        rms = float(np.sqrt(np.mean(mono ** 2)))
                    else:
                        peak = 0.0
                        rms = 0.0
                    
                    # Emit data via callback
                    self.on_audio_data(data_gained.copy(), peak, rms)
                    
                except Exception as e:
                    print(f"Error reading audio: {e}")
                    break
        
        except Exception as e:
            print(f"Error in audio capture loop: {e}")
        finally:
            if self.stream is not None:
                self.stream.stop()
                self.stream.close()
                self.stream = None
