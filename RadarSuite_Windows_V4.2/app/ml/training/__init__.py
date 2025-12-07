"""
RadarSuite v4.2.0 - ML Training Module
Recording and training pipeline for custom audio detection models

Components:
- SessionManager: Manages labeled recording sessions
- LabeledRecorder: Records audio with real-time labeling
- Trainer: Trains models from labeled data
"""

from .session_manager import SessionManager, LabeledSession, AudioLabel
from .recorder import LabeledRecorder
from .trainer import ModelTrainer, TrainingConfig

__all__ = [
    'SessionManager',
    'LabeledSession',
    'AudioLabel',
    'LabeledRecorder',
    'ModelTrainer',
    'TrainingConfig',
]
