"""
Radar Games ML v4.3.0 - Machine Learning Detection Module
Real-time ML Detection Enhancement (Roadmap Item 1)

Replaces rule-based detection with lightweight ML models (TFLite/ONNX)
Target: 30-50% better accuracy for footstep/gunshot recognition

Components:
- FeatureExtractor: Audio → Mel-spectrogram conversion
- YAMNetDetector: Pre-trained audio classifier (TFLite)
- MLDetector: Main interface combining features + inference
- ModelRegistry: Trained model management and auto-loading (v4.3.0)
- MLFootstepDetector: Real-time inference with trained models (v4.3.0)
"""

from .feature_extractor import FeatureExtractor, extract_mel_spectrogram
from .yamnet import YAMNetDetector, YAMNET_CLASS_MAP
from .detector import MLDetector, get_ml_detector
from .model_registry import ModelRegistry, ModelInfo, get_model_registry
from .ml_detector import MLFootstepDetector

__all__ = [
    'FeatureExtractor',
    'extract_mel_spectrogram',
    'YAMNetDetector',
    'YAMNET_CLASS_MAP',
    'MLDetector',
    'get_ml_detector',
    'ModelRegistry',
    'ModelInfo',
    'get_model_registry',
    'MLFootstepDetector',
]
