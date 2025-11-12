"""
Configuration management for Audio Radar.
Handles loading, saving, and validation of application settings.
"""

import json
from pathlib import Path
from typing import Any, Dict
from audioradar.logger import get_logger

CONFIG_FILE = Path(__file__).parent.parent / "config.json"

class Config:
    """Application configuration manager."""
    
    DEFAULT_CONFIG = {
        # Audio settings
        "audio": {
            "input_device": None,  # None = system default
            "sample_rate": 44100,
            "block_size": 1024,
            "channels": 2,
        },
        
        # Detection settings
        "detection": {
            "footstep_threshold": 0.3,
            "running_threshold": 0.5,
            "gunshot_threshold": 0.7,
            "min_frequency": 100,
            "max_frequency": 8000,
        },
        
        # GUI settings
        "gui": {
            "theme": "dark",  # dark or light
            "radar_transparency": 80,  # 10-100%
            "radar_size": 400,  # pixels
            "window_width": 1200,
            "window_height": 800,
            "radar_detached": False,
        },
        
        # Visualization settings
        "visualization": {
            "decay_time": 2.0,  # seconds
            "footstep_color": "#00FF00",  # green
            "running_color": "#FFFF00",  # yellow
            "gunshot_color": "#FF0000",  # red
            "show_spectrum": True,
            "show_distance": True,
        }
    }
    
    def __init__(self):
        """Initialize configuration."""
        self.logger = get_logger()
        self.config = self.DEFAULT_CONFIG.copy()
        self.load()
    
    def load(self):
        """Load configuration from file."""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                self._merge_config(user_config)
                self.logger.info(f"Configuration loaded from {CONFIG_FILE}")
            except Exception as e:
                self.logger.error(f"Failed to load configuration: {e}")
                self.logger.warning("Using default configuration")
        else:
            self.logger.info("No configuration file found, using defaults")
            self.save()  # Create default config file
    
    def save(self):
        """Save configuration to file."""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
            self.logger.info(f"Configuration saved to {CONFIG_FILE}")
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}")
    
    def _merge_config(self, user_config: Dict[str, Any]):
        """Merge user configuration with defaults."""
        for section, values in user_config.items():
            if section in self.config:
                if isinstance(values, dict):
                    self.config[section].update(values)
                else:
                    self.config[section] = values
    
    def get(self, section: str, key: str, default=None):
        """
        Get configuration value.
        
        Args:
            section: Configuration section name
            key: Configuration key
            default: Default value if not found
        
        Returns:
            Configuration value or default
        """
        return self.config.get(section, {}).get(key, default)
    
    def set(self, section: str, key: str, value: Any):
        """
        Set configuration value.
        
        Args:
            section: Configuration section name
            key: Configuration key
            value: Value to set
        """
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get entire configuration section.
        
        Args:
            section: Section name
        
        Returns:
            Dictionary of section values
        """
        return self.config.get(section, {})
