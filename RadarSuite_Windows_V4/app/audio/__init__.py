"""
RadarSuite v3.5.0 - Audio Module
Audio processing, recording, classification, voice detection
"""

from audio.cache import AudioProcessingCache
from audio.engine import AudioEngine
from audio.classifier import SoundClassifier
from audio.recorder import AudioRecorder
from audio.voice_detector import HumanVoiceDetector

__all__ = [
    'AudioProcessingCache',
    'AudioEngine',
    'SoundClassifier',
    'AudioRecorder',
    'HumanVoiceDetector',
]
