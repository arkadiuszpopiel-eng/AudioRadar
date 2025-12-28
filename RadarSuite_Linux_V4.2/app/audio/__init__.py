"""
RadarSuite v4.2.0 - Audio Module
Audio processing, recording, classification, voice detection

ENHANCED v4.2.0: Added AudioProcessor for 3D localization algorithms
"""

from audio.cache import AudioProcessingCache
from audio.engine import AudioEngine
from audio.classifier import SoundClassifier
from audio.recorder import AudioRecorder
from audio.voice_detector import HumanVoiceDetector
from audio.processor import AudioProcessor, get_audio_processor

__all__ = [
    'AudioProcessingCache',
    'AudioEngine',
    'SoundClassifier',
    'AudioRecorder',
    'HumanVoiceDetector',
    'AudioProcessor',
    'get_audio_processor',
]
