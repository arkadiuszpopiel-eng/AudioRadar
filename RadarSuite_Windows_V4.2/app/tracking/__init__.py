"""
RadarSuite V4.2.1 - Tracking Module
Multi-target tracking and threat priority system
"""

from tracking.target import Target, TargetTracker
from tracking.threat import ThreatPrioritySystem

__all__ = [
    'Target',
    'TargetTracker',
    'ThreatPrioritySystem',
]
