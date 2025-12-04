"""
RadarSuite v3.5.0 - Detection Module
Detection worker and footstep pattern recognition
"""

from detection.worker import DetectionWorker
from detection.footstep import HumanFootstepDetector

__all__ = [
    'DetectionWorker',
    'HumanFootstepDetector',
]
