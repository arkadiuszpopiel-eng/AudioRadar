"""
RadarSuite v3.5.0 - Core Module
Essential application components
"""

# Constants
from .constants import (
    VERSION,
    SAMPLE_RATE,
    BLOCK_SIZE,
    CHANNELS,
    TICK_INTERVAL_MS,
    GAME_SCAN_INTERVAL_MS,
    AUDIO_SCAN_INTERVAL_MS,
    STARTUP_DELAY_MS,
    STARTUP_AUDIO_DELAY_MS,
    ENERGY_THRESHOLD,
    RADAR_ROTATION_DEG,
    MAX_WORKERS,
    DETECTION_TIMEOUT_SEC,
    CLEANUP_INTERVAL_SEC,
    AUDIO_LEVEL_LOUD,
    AUDIO_LEVEL_MEDIUM,
    AUDIO_LEVEL_LOW,
    RECORDING_BUFFER_SIZE,
    RECORDING_FLUSH_INTERVAL,
    TOAST_DURATION_MS,
    TOAST_MAX_COUNT,
)

# Logger
from .logger import (
    ThreadSafeLogger,
    log,
    ROOT,
    SUPER_LOG,
)

# Config
from .config import ConfigManager

# Translations
from .translations import (
    TRANSLATIONS,
    current_language,
    tr,
    set_language,
)

# Dependency Injection (Point 11 - v3.5.0)
from .di import (
    ServiceContainer,
    get_container,
    configure_services,
)

__all__ = [
    # Constants
    'VERSION',
    'SAMPLE_RATE',
    'BLOCK_SIZE',
    'CHANNELS',
    'TICK_INTERVAL_MS',
    'GAME_SCAN_INTERVAL_MS',
    'AUDIO_SCAN_INTERVAL_MS',
    'STARTUP_DELAY_MS',
    'STARTUP_AUDIO_DELAY_MS',
    'ENERGY_THRESHOLD',
    'RADAR_ROTATION_DEG',
    'MAX_WORKERS',
    'DETECTION_TIMEOUT_SEC',
    'CLEANUP_INTERVAL_SEC',
    'AUDIO_LEVEL_LOUD',
    'AUDIO_LEVEL_MEDIUM',
    'AUDIO_LEVEL_LOW',
    'RECORDING_BUFFER_SIZE',
    'RECORDING_FLUSH_INTERVAL',
    'TOAST_DURATION_MS',
    'TOAST_MAX_COUNT',

    # Logger
    'ThreadSafeLogger',
    'log',
    'ROOT',
    'SUPER_LOG',

    # Config
    'ConfigManager',

    # Translations
    'TRANSLATIONS',
    'current_language',
    'tr',
    'set_language',

    # Dependency Injection
    'ServiceContainer',
    'get_container',
    'configure_services',
]
