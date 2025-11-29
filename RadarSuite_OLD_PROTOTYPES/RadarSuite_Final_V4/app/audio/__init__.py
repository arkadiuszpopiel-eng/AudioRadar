"""
RadarSuite v3.5.0 - Audio Module
Audio processing, recording, classification, voice detection
"""

from .cache import AudioProcessingCache
from .engine import AudioEngine
from .classifier import SoundClassifier
from .recorder import AudioRecorder
from .voice_detector import HumanVoiceDetector

__all__ = [
    'AudioProcessingCache',
    'AudioEngine',
    'SoundClassifier',
    'AudioRecorder',
    'HumanVoiceDetector',
]
