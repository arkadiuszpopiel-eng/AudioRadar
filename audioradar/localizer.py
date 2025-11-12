"""
Directional audio localization module.
Determines direction and distance of audio events.
"""

import numpy as np
from typing import Tuple, Optional
from audioradar.logger import get_logger


class AudioLocalizer:
    """Localizes audio events in 360 degrees."""
    
    # Standard channel mappings for surround sound
    STEREO_MAP = {
        0: 30,   # Left
        1: 330,  # Right
    }
    
    SURROUND_51_MAP = {
        0: 30,   # Front Left
        1: 330,  # Front Right
        2: 0,    # Center
        3: 180,  # LFE (rear)
        4: 120,  # Rear Left
        5: 240,  # Rear Right
    }
    
    SURROUND_71_MAP = {
        0: 30,   # Front Left
        1: 330,  # Front Right
        2: 0,    # Center
        3: 180,  # LFE
        4: 90,   # Side Left
        5: 270,  # Side Right
        6: 135,  # Rear Left
        7: 225,  # Rear Right
    }
    
    def __init__(self, channels: int = 2):
        """
        Initialize audio localizer.
        
        Args:
            channels: Number of audio channels (2, 6, or 8)
        """
        self.logger = get_logger()
        self.channels = channels
        self.channel_map = self._get_channel_map(channels)
        
        self.logger.info(f"AudioLocalizer initialized: {channels} channels")
        self.logger.debug(f"Channel map: {self.channel_map}")
    
    def _get_channel_map(self, channels: int) -> dict:
        """Get channel to angle mapping based on channel count."""
        if channels == 2:
            return self.STEREO_MAP
        elif channels == 6:
            return self.SURROUND_51_MAP
        elif channels == 8:
            return self.SURROUND_71_MAP
        else:
            # Default to stereo for unknown configurations
            self.logger.warning(f"Unknown channel count {channels}, using stereo map")
            return self.STEREO_MAP
    
    def localize(self, audio_data: np.ndarray) -> Tuple[float, float]:
        """
        Determine direction and distance of audio event.
        
        Args:
            audio_data: Multi-channel audio data (shape: [samples, channels])
        
        Returns:
            Tuple of (angle in degrees 0-360, distance 0-1)
        """
        if audio_data.size == 0:
            return 0.0, 0.0
        
        # Ensure proper shape
        if len(audio_data.shape) == 1:
            # Mono audio - assume front center
            rms = np.sqrt(np.mean(audio_data ** 2))
            distance = self._estimate_distance(rms)
            return 0.0, float(distance)
        
        # Calculate RMS for each channel
        channel_levels = []
        for ch in range(min(audio_data.shape[1], self.channels)):
            rms = np.sqrt(np.mean(audio_data[:, ch] ** 2))
            channel_levels.append(rms)
        
        # Pad with zeros if needed
        while len(channel_levels) < self.channels:
            channel_levels.append(0.0)
        
        # Find dominant direction
        angle = self._calculate_angle(channel_levels)
        
        # Estimate distance based on overall intensity
        max_level = max(channel_levels)
        distance = self._estimate_distance(max_level)
        
        return float(angle), float(distance)
    
    def _calculate_angle(self, channel_levels: list) -> float:
        """Calculate angle based on channel levels."""
        # Use weighted average of channel angles
        total_weight = 0.0
        weighted_x = 0.0
        weighted_y = 0.0
        
        for ch, level in enumerate(channel_levels):
            if ch not in self.channel_map or level < 0.01:
                continue
            
            angle_deg = self.channel_map[ch]
            angle_rad = np.deg2rad(angle_deg)
            
            # Convert to Cartesian coordinates
            x = level * np.cos(angle_rad)
            y = level * np.sin(angle_rad)
            
            weighted_x += x
            weighted_y += y
            total_weight += level
        
        if total_weight < 0.01:
            return 0.0
        
        # Convert back to angle
        angle_rad = np.arctan2(weighted_y, weighted_x)
        angle_deg = np.rad2deg(angle_rad)
        
        # Normalize to 0-360
        if angle_deg < 0:
            angle_deg += 360
        
        return angle_deg
    
    def _estimate_distance(self, level: float) -> float:
        """
        Estimate distance based on audio level.
        
        Args:
            level: RMS level (0.0-1.0)
        
        Returns:
            Distance (0.0 = far, 1.0 = very close)
        """
        # Simple inverse relationship
        # Higher level = closer distance
        if level < 0.01:
            return 0.0
        
        # Logarithmic scaling
        distance = np.clip(level * 2.0, 0.0, 1.0)
        
        return float(distance)
    
    def get_channel_info(self) -> dict:
        """
        Get information about channel configuration.
        
        Returns:
            Dictionary with channel information
        """
        return {
            'channels': self.channels,
            'channel_map': self.channel_map,
            'configuration': self._get_config_name()
        }
    
    def _get_config_name(self) -> str:
        """Get human-readable configuration name."""
        config_names = {
            2: "Stereo",
            6: "5.1 Surround",
            8: "7.1 Surround"
        }
        return config_names.get(self.channels, f"{self.channels}-channel")
    
    def localize_with_interpolation(self, audio_data: np.ndarray) -> Tuple[float, float]:
        """
        Localize with interpolation between channels for smoother angles.
        
        Args:
            audio_data: Multi-channel audio data
        
        Returns:
            Tuple of (angle, distance)
        """
        # Use standard localization for now
        # Can be enhanced with more sophisticated interpolation
        return self.localize(audio_data)
    
    def is_approaching(self, current_distance: float, 
                      previous_distance: float,
                      threshold: float = 0.05) -> Optional[bool]:
        """
        Determine if sound source is approaching or receding.
        
        Args:
            current_distance: Current distance estimate
            previous_distance: Previous distance estimate
            threshold: Minimum change to consider movement
        
        Returns:
            True if approaching, False if receding, None if no significant change
        """
        diff = current_distance - previous_distance
        
        if abs(diff) < threshold:
            return None
        
        return diff > 0  # Increasing distance value means getting closer
