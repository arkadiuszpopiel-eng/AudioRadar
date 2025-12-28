"""
RadarSuite v4.2.0 - Detection Module
Detection worker and pattern recognition

FIXED v4.2.0: ARC Raiders-specific detection modules:
- SpectralFeatureExtractor: MFCC and spectral features
- ShotDetector: Close/distant shots and explosions
- HumanFootstepDetector: Enhanced with surface type classification
- ARCMachineDetector: Machine state detection (idle/patrol/search/combat)
"""

from detection.worker import DetectionWorker
from detection.footstep import HumanFootstepDetector
from detection.spectral import SpectralFeatureExtractor
from detection.shot import ShotDetector
from detection.machine import ARCMachineDetector

__all__ = [
    'DetectionWorker',
    'HumanFootstepDetector',
    'SpectralFeatureExtractor',
    'ShotDetector',
    'ARCMachineDetector',
]
