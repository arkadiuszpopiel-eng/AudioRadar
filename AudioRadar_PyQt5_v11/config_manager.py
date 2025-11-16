"""
Configuration Manager for AudioRadar PyQt5
Handles loading, saving, and managing all application configuration.
"""

import json
from pathlib import Path
from typing import Any, Dict
from dataclasses import dataclass, asdict

from logger import get_logger


@dataclass
class AudioConfig:
    """Audio configuration settings."""
    input_device_index: int = -1  # -1 = default
    sample_rate: int = 48000
    block_size: int = 2048
    channels: int = 2


@dataclass
class DetectionConfig:
    """Detection configuration settings."""
    walking_enabled: bool = True
    running_enabled: bool = True
    shooting_enabled: bool = True
    walking_rms_min: float = 0.02
    walking_rms_max: float = 0.15
    walking_freq_min: float = 1.0
    walking_freq_max: float = 3.0
    running_rms_min: float = 0.10
    running_rms_max: float = 0.40
    running_freq_min: float = 3.0
    running_freq_max: float = 6.0
    shooting_peak_threshold: float = 0.60
    shooting_attack_time: float = 0.01
    confidence_threshold: float = 0.5


@dataclass
class RadarConfig:
    """Radar visualization configuration."""
    opacity: float = 0.9
    fade_duration: float = 2.0
    detached: bool = False
    window_x: int = 100
    window_y: int = 100
    window_width: int = 400
    window_height: int = 400


@dataclass
class SpectrumConfig:
    """Spectrum analyzer configuration."""
    enabled: bool = True
    num_bars: int = 64
    min_freq: float = 20.0
    max_freq: float = 20000.0
    smoothing: float = 0.7


@dataclass
class UIConfig:
    """UI configuration settings."""
    theme: str = "dark"
    window_width: int = 1200
    window_height: int = 800
    window_x: int = -1  # -1 = center
    window_y: int = -1  # -1 = center
    show_spectrum: bool = True
    show_radar: bool = True
    show_controls: bool = True


@dataclass
class AppConfig:
    """Complete application configuration."""
    audio: AudioConfig
    detection: DetectionConfig
    radar: RadarConfig
    spectrum: SpectrumConfig
    ui: UIConfig


class ConfigManager:
    """Manages application configuration."""

    def __init__(self, config_file: str = "config.json"):
        self.logger = get_logger()
        self.logger.info("Initializing Configuration Manager")

        self.config_file = Path(config_file)
        self.config = self._create_default_config()

        # Load configuration if exists
        if self.config_file.exists():
            self.load()
        else:
            self.logger.info("No config file found, using defaults")
            self.save()  # Save default config

        self.logger.info("Configuration Manager initialized successfully")

    def _create_default_config(self) -> AppConfig:
        """Create default configuration."""
        return AppConfig(
            audio=AudioConfig(),
            detection=DetectionConfig(),
            radar=RadarConfig(),
            spectrum=SpectrumConfig(),
            ui=UIConfig()
        )

    def load(self) -> bool:
        """
        Load configuration from file.

        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info(f"Loading configuration from {self.config_file}")

            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Load each section
            if 'audio' in data:
                self.config.audio = AudioConfig(**data['audio'])

            if 'detection' in data:
                self.config.detection = DetectionConfig(**data['detection'])

            if 'radar' in data:
                self.config.radar = RadarConfig(**data['radar'])

            if 'spectrum' in data:
                self.config.spectrum = SpectrumConfig(**data['spectrum'])

            if 'ui' in data:
                self.config.ui = UIConfig(**data['ui'])

            self.logger.info("Configuration loaded successfully")
            return True

        except Exception as e:
            self.logger.error(f"Error loading configuration", e)
            return False

    def save(self) -> bool:
        """
        Save configuration to file.

        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info(f"Saving configuration to {self.config_file}")

            data = {
                'audio': asdict(self.config.audio),
                'detection': asdict(self.config.detection),
                'radar': asdict(self.config.radar),
                'spectrum': asdict(self.config.spectrum),
                'ui': asdict(self.config.ui)
            }

            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            self.logger.info("Configuration saved successfully")
            return True

        except Exception as e:
            self.logger.error(f"Error saving configuration", e)
            return False

    def get_audio_config(self) -> AudioConfig:
        """Get audio configuration."""
        return self.config.audio

    def get_detection_config(self) -> DetectionConfig:
        """Get detection configuration."""
        return self.config.detection

    def get_radar_config(self) -> RadarConfig:
        """Get radar configuration."""
        return self.config.radar

    def get_spectrum_config(self) -> SpectrumConfig:
        """Get spectrum configuration."""
        return self.config.spectrum

    def get_ui_config(self) -> UIConfig:
        """Get UI configuration."""
        return self.config.ui

    def set(self, section: str, key: str, value: Any):
        """
        Set a configuration value.

        Args:
            section: Configuration section (audio, detection, radar, spectrum, ui)
            key: Configuration key
            value: Value to set
        """
        try:
            if section == 'audio':
                setattr(self.config.audio, key, value)
            elif section == 'detection':
                setattr(self.config.detection, key, value)
            elif section == 'radar':
                setattr(self.config.radar, key, value)
            elif section == 'spectrum':
                setattr(self.config.spectrum, key, value)
            elif section == 'ui':
                setattr(self.config.ui, key, value)
            else:
                self.logger.warning(f"Unknown configuration section: {section}")

        except Exception as e:
            self.logger.error(f"Error setting configuration value", e)

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        Args:
            section: Configuration section
            key: Configuration key
            default: Default value if not found

        Returns:
            Configuration value or default
        """
        try:
            if section == 'audio':
                return getattr(self.config.audio, key, default)
            elif section == 'detection':
                return getattr(self.config.detection, key, default)
            elif section == 'radar':
                return getattr(self.config.radar, key, default)
            elif section == 'spectrum':
                return getattr(self.config.spectrum, key, default)
            elif section == 'ui':
                return getattr(self.config.ui, key, default)
            else:
                self.logger.warning(f"Unknown configuration section: {section}")
                return default

        except Exception as e:
            self.logger.error(f"Error getting configuration value", e)
            return default

    def reset_to_defaults(self):
        """Reset configuration to defaults."""
        self.logger.info("Resetting configuration to defaults")
        self.config = self._create_default_config()
        self.save()

    def export_config(self, file_path: str) -> bool:
        """
        Export configuration to a different file.

        Args:
            file_path: Path to export file

        Returns:
            True if successful
        """
        try:
            original_file = self.config_file
            self.config_file = Path(file_path)
            result = self.save()
            self.config_file = original_file
            return result

        except Exception as e:
            self.logger.error(f"Error exporting configuration", e)
            return False

    def import_config(self, file_path: str) -> bool:
        """
        Import configuration from a different file.

        Args:
            file_path: Path to import file

        Returns:
            True if successful
        """
        try:
            original_file = self.config_file
            self.config_file = Path(file_path)
            result = self.load()
            self.config_file = original_file
            return result

        except Exception as e:
            self.logger.error(f"Error importing configuration", e)
            return False
