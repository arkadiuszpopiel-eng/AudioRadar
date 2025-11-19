"""
RadarSuite v3.5.0 - Hardware Optimization Module
GPU acceleration and Sound Blaster optimization
"""

from .gpu import GPUAccelerator
from .soundblaster import SoundBlasterOptimizer

__all__ = [
    'GPUAccelerator',
    'SoundBlasterOptimizer',
]
