"""
Audio capture engine with device management.
Handles audio input from system devices with multi-channel support.
"""

import numpy as np
import sounddevice as sd
from typing import Callable, List, Tuple, Optional
from threading import Thread, Event
from queue import Queue
from audioradar.logger import get_logger


class AudioDevice:
    """Represents an audio device."""
    
    def __init__(self, index: int, name: str, channels: int, sample_rate: float):
        self.index = index
        self.name = name
        self.channels = channels
        self.sample_rate = sample_rate
    
    def __str__(self):
        return f"{self.index}: {self.name} ({self.channels}ch @ {self.sample_rate}Hz)"


class AudioEngine:
    """Audio capture engine with device management."""
    
    def __init__(self, device_index: Optional[int] = None, 
                 sample_rate: int = 44100, 
                 block_size: int = 1024,
                 channels: int = 2):
        """
        Initialize audio engine.
        
        Args:
            device_index: Audio device index (None = default)
            sample_rate: Sample rate in Hz
            block_size: Number of samples per block
            channels: Number of audio channels
        """
        self.logger = get_logger()
        self.device_index = device_index
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.channels = channels
        
        self.stream = None
        self.running = False
        self.callback = None
        self.audio_queue = Queue(maxsize=10)
        self.stop_event = Event()
        
        self.logger.info(f"AudioEngine initialized: device={device_index}, "
                        f"rate={sample_rate}Hz, block={block_size}, channels={channels}")
    
    @staticmethod
    def list_input_devices() -> List[AudioDevice]:
        """
        List all available audio input devices.
        
        Returns:
            List of AudioDevice objects
        """
        devices = []
        try:
            device_list = sd.query_devices()
            for i, dev in enumerate(device_list):
                if dev['max_input_channels'] > 0:
                    devices.append(AudioDevice(
                        index=i,
                        name=dev['name'],
                        channels=dev['max_input_channels'],
                        sample_rate=dev['default_samplerate']
                    ))
        except Exception as e:
            get_logger().error(f"Failed to list audio devices: {e}")
        
        return devices
    
    @staticmethod
    def get_default_device() -> Optional[AudioDevice]:
        """
        Get default audio input device.
        
        Returns:
            AudioDevice or None
        """
        try:
            default_dev = sd.query_devices(kind='input')
            return AudioDevice(
                index=sd.default.device[0],
                name=default_dev['name'],
                channels=default_dev['max_input_channels'],
                sample_rate=default_dev['default_samplerate']
            )
        except Exception as e:
            get_logger().error(f"Failed to get default device: {e}")
            return None
    
    def set_callback(self, callback: Callable[[np.ndarray], None]):
        """
        Set audio data callback.
        
        Args:
            callback: Function that receives audio data (numpy array)
        """
        self.callback = callback
    
    def start(self):
        """Start audio capture."""
        if self.running:
            self.logger.warning("Audio engine already running")
            return
        
        try:
            self.logger.info("Starting audio capture...")
            self.running = True
            self.stop_event.clear()
            
            # Create audio stream
            self.stream = sd.InputStream(
                device=self.device_index,
                channels=self.channels,
                samplerate=self.sample_rate,
                blocksize=self.block_size,
                callback=self._audio_callback
            )
            
            self.stream.start()
            self.logger.info("Audio capture started successfully")
            
            # Start processing thread
            self.process_thread = Thread(target=self._process_audio, daemon=True)
            self.process_thread.start()
            
        except Exception as e:
            self.logger.error(f"Failed to start audio capture: {e}")
            self.running = False
            raise
    
    def stop(self):
        """Stop audio capture."""
        if not self.running:
            return
        
        self.logger.info("Stopping audio capture...")
        self.running = False
        self.stop_event.set()
        
        if self.stream:
            try:
                self.stream.stop()
                self.stream.close()
            except Exception as e:
                self.logger.error(f"Error stopping stream: {e}")
        
        self.logger.info("Audio capture stopped")
    
    def _audio_callback(self, indata, frames, time_info, status):
        """Internal callback for audio stream."""
        if status:
            self.logger.warning(f"Audio stream status: {status}")
        
        # Copy data to avoid issues with the buffer
        audio_data = indata.copy()
        
        # Put in queue for processing
        if not self.audio_queue.full():
            self.audio_queue.put(audio_data)
    
    def _process_audio(self):
        """Process audio data from queue."""
        while self.running and not self.stop_event.is_set():
            try:
                # Get audio data from queue (with timeout)
                audio_data = self.audio_queue.get(timeout=0.1)
                
                # Call user callback if set
                if self.callback:
                    self.callback(audio_data)
                    
            except:
                # Queue empty or other error - continue
                continue
    
    def get_audio_level(self, audio_data: np.ndarray) -> float:
        """
        Get current audio level (RMS).
        
        Args:
            audio_data: Audio samples
        
        Returns:
            RMS level (0.0 to 1.0)
        """
        if audio_data.size == 0:
            return 0.0
        
        rms = np.sqrt(np.mean(audio_data ** 2))
        return float(min(rms, 1.0))
    
    def test_device(self, duration: float = 2.0) -> Tuple[bool, float, str]:
        """
        Test audio device quality.
        
        Args:
            duration: Test duration in seconds
        
        Returns:
            Tuple of (success, average_level, message)
        """
        self.logger.info(f"Testing audio device for {duration} seconds...")
        
        try:
            # Record audio for test duration
            recording = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=self.channels,
                device=self.device_index
            )
            sd.wait()
            
            # Calculate average level
            avg_level = np.sqrt(np.mean(recording ** 2))
            
            if avg_level < 0.001:
                return False, float(avg_level), "No audio signal detected"
            elif avg_level > 0.9:
                return False, float(avg_level), "Audio signal too loud (clipping)"
            else:
                return True, float(avg_level), f"Audio quality good (level: {avg_level:.3f})"
                
        except Exception as e:
            self.logger.error(f"Device test failed: {e}")
            return False, 0.0, f"Test failed: {str(e)}"
