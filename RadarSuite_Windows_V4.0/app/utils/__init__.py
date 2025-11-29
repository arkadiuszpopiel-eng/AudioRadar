"""
RadarSuite v3.5.0 - Utilities Module
Performance monitoring, game detection, launcher detection, audio scanning
"""

from utils.performance import PerformanceMonitor
from utils.game_detector import GameProcessDetector
from utils.launcher import PlatformLauncherDetector
from utils.audio_scanner import AudioSourceScanner

__all__ = [
    'PerformanceMonitor',
    'GameProcessDetector',
    'PlatformLauncherDetector',
    'AudioSourceScanner',
]
