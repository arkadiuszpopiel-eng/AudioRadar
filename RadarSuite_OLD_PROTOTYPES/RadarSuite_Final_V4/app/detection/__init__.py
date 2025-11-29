"""
RadarSuite v3.5.0 - Detection Module
Detection worker and footstep pattern recognition
"""

from .worker import DetectionWorker
from .footstep import HumanFootstepDetector

__all__ = [
    'DetectionWorker',
    'HumanFootstepDetector',
]
