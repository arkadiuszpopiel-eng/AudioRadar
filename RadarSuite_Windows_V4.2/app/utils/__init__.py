"""
RadarSuite v4.2.1 - Utilities Module
Performance monitoring, memory optimization, game detection, launcher detection, audio scanning

ENHANCED v4.2.1: Added MemoryOptimizer for ZADANIE 6
"""

from utils.performance import PerformanceMonitor, MemoryOptimizer, MemorySnapshot, MemoryStats
from utils.game_detector import GameProcessDetector
from utils.launcher import PlatformLauncherDetector
from utils.audio_scanner import AudioSourceScanner

__all__ = [
    'PerformanceMonitor',
    'MemoryOptimizer',
    'MemorySnapshot',
    'MemoryStats',
    'GameProcessDetector',
    'PlatformLauncherDetector',
    'AudioSourceScanner',
]
