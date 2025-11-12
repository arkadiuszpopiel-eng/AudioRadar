"""
Event detection module for Audio Radar.
Detects footsteps, running, and gunshots from audio data.
"""

import numpy as np
from scipy import signal
from typing import Optional, Dict, Any
from audioradar.logger import get_logger


class AudioEvent:
    """Represents a detected audio event."""
    
    FOOTSTEP = "footstep"
    RUNNING = "running"
    GUNSHOT = "gunshot"
    
    def __init__(self, event_type: str, confidence: float, features: Dict[str, Any]):
        self.type = event_type
        self.confidence = confidence
        self.features = features
        self.timestamp = None
    
    def __str__(self):
        return f"{self.type} (confidence: {self.confidence:.2f})"


class EventDetector:
    """Detects audio events (footsteps, running, gunshots)."""
    
    def __init__(self, sample_rate: int = 44100,
                 footstep_threshold: float = 0.3,
                 running_threshold: float = 0.5,
                 gunshot_threshold: float = 0.7):
        """
        Initialize event detector.
        
        Args:
            sample_rate: Audio sample rate
            footstep_threshold: Detection threshold for footsteps
            running_threshold: Detection threshold for running
            gunshot_threshold: Detection threshold for gunshots
        """
        self.logger = get_logger()
        self.sample_rate = sample_rate
        self.footstep_threshold = footstep_threshold
        self.running_threshold = running_threshold
        self.gunshot_threshold = gunshot_threshold
        
        # Design filters
        self._setup_filters()
        
        # State tracking
        self.last_event_time = 0
        self.event_history = []
        
        self.logger.info(f"EventDetector initialized: fs={sample_rate}Hz, "
                        f"thresholds=[{footstep_threshold}, {running_threshold}, {gunshot_threshold}]")
    
    def _setup_filters(self):
        """Setup bandpass filters for different event types."""
        # Footstep filter: 2-8 kHz
        self.footstep_sos = signal.butter(
            4, [2000, 8000], btype='band', 
            fs=self.sample_rate, output='sos'
        )
        
        # Gunshot filter: 200 Hz - 12 kHz (wide spectrum)
        self.gunshot_sos = signal.butter(
            4, [200, 12000], btype='band',
            fs=self.sample_rate, output='sos'
        )
    
    def detect(self, audio_data: np.ndarray) -> Optional[AudioEvent]:
        """
        Detect events in audio data.
        
        Args:
            audio_data: Audio samples (shape: [samples, channels])
        
        Returns:
            AudioEvent if detected, None otherwise
        """
        if audio_data.size == 0:
            return None
        
        # Convert to mono if multi-channel
        if len(audio_data.shape) > 1:
            audio_mono = np.mean(audio_data, axis=1)
        else:
            audio_mono = audio_data
        
        # Calculate RMS energy
        rms = np.sqrt(np.mean(audio_mono ** 2))
        
        # Skip if too quiet
        if rms < 0.01:
            return None
        
        # Extract features
        features = self._extract_features(audio_mono)
        
        # Classify event
        event = self._classify_event(features, rms)
        
        return event
    
    def _extract_features(self, audio_data: np.ndarray) -> Dict[str, Any]:
        """Extract features from audio data."""
        features = {}
        
        # Time domain features
        features['rms'] = np.sqrt(np.mean(audio_data ** 2))
        features['peak'] = np.max(np.abs(audio_data))
        features['zero_crossings'] = np.sum(np.diff(np.sign(audio_data)) != 0)
        
        # Frequency domain features
        fft = np.fft.rfft(audio_data)
        freqs = np.fft.rfftfreq(len(audio_data), 1/self.sample_rate)
        magnitude = np.abs(fft)
        
        features['spectral_centroid'] = np.sum(freqs * magnitude) / (np.sum(magnitude) + 1e-10)
        features['spectral_bandwidth'] = np.sqrt(
            np.sum(((freqs - features['spectral_centroid']) ** 2) * magnitude) / 
            (np.sum(magnitude) + 1e-10)
        )
        
        # Energy in different frequency bands
        low_band = (freqs >= 100) & (freqs < 2000)
        mid_band = (freqs >= 2000) & (freqs < 8000)
        high_band = (freqs >= 8000) & (freqs < 16000)
        
        features['low_energy'] = np.sum(magnitude[low_band])
        features['mid_energy'] = np.sum(magnitude[mid_band])
        features['high_energy'] = np.sum(magnitude[high_band])
        
        # Apply filters
        try:
            footstep_filtered = signal.sosfilt(self.footstep_sos, audio_data)
            gunshot_filtered = signal.sosfilt(self.gunshot_sos, audio_data)
            
            features['footstep_energy'] = np.sqrt(np.mean(footstep_filtered ** 2))
            features['gunshot_energy'] = np.sqrt(np.mean(gunshot_filtered ** 2))
        except Exception as e:
            self.logger.debug(f"Filter error: {e}")
            features['footstep_energy'] = 0
            features['gunshot_energy'] = 0
        
        return features
    
    def _classify_event(self, features: Dict[str, Any], rms: float) -> Optional[AudioEvent]:
        """Classify event based on features."""
        
        # Gunshot detection - high energy, wide spectrum, sharp transient
        if features['peak'] > self.gunshot_threshold and \
           features['gunshot_energy'] > 0.4 and \
           features['spectral_bandwidth'] > 2000:
            confidence = min(features['peak'] / self.gunshot_threshold, 1.0)
            return AudioEvent(AudioEvent.GUNSHOT, float(confidence), features)
        
        # Running detection - medium-high energy footsteps, higher rate
        if features['footstep_energy'] > self.running_threshold and \
           features['mid_energy'] > features['low_energy']:
            confidence = min(features['footstep_energy'] / self.running_threshold, 1.0)
            return AudioEvent(AudioEvent.RUNNING, float(confidence), features)
        
        # Footstep detection - moderate energy in mid frequencies
        if features['footstep_energy'] > self.footstep_threshold and \
           features['mid_energy'] > 0:
            confidence = min(features['footstep_energy'] / self.footstep_threshold, 1.0)
            return AudioEvent(AudioEvent.FOOTSTEP, float(confidence), features)
        
        return None
    
    def set_thresholds(self, footstep: float = None, 
                      running: float = None, 
                      gunshot: float = None):
        """
        Update detection thresholds.
        
        Args:
            footstep: Footstep threshold (0.0-1.0)
            running: Running threshold (0.0-1.0)
            gunshot: Gunshot threshold (0.0-1.0)
        """
        if footstep is not None:
            self.footstep_threshold = max(0.0, min(1.0, footstep))
        if running is not None:
            self.running_threshold = max(0.0, min(1.0, running))
        if gunshot is not None:
            self.gunshot_threshold = max(0.0, min(1.0, gunshot))
        
        self.logger.info(f"Thresholds updated: footstep={self.footstep_threshold}, "
                        f"running={self.running_threshold}, gunshot={self.gunshot_threshold}")
