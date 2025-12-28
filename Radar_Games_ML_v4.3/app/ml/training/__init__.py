"""
Radar Games ML v4.2.0 - ML Training Module
Recording and training pipeline for custom audio detection models

Components:
- SessionManager: Manages labeled recording sessions
- LabeledRecorder: Records audio with real-time labeling
- Trainer: Trains models from labeled data
"""

"""Convenience exports for the ML training pipeline.

This module exposes the high-level building blocks used by the UI:

* :class:`SessionManager` keeps track of labeled sessions.
* :class:`LabeledRecorder` records audio and attaches labels in real time.
* :class:`ModelTrainer` runs the feature extraction and training loop.
* :class:`TrainingStatus` enumerates the phases of the training lifecycle.
"""

from .session_manager import SessionManager, LabeledSession, AudioLabel
from .recorder import LabeledRecorder, RecordingState, RecordingStateEnum
from .trainer import ModelTrainer, TrainingConfig, TrainingStatus
from .recording_controller import RecordingController, InMemorySessionManager
from .async_session_worker import AsyncSessionWorker, get_session_worker, stop_session_worker
from .session_validator import SessionValidator, ValidationResult

__all__ = [
    'SessionManager',
    'LabeledSession',
    'AudioLabel',
    'LabeledRecorder',
    'RecordingState',
    'RecordingStateEnum',
    'RecordingController',
    'InMemorySessionManager',
    'ModelTrainer',
    'TrainingConfig',
    'TrainingStatus',
    'AsyncSessionWorker',
    'get_session_worker',
    'stop_session_worker',
    'SessionValidator',
    'ValidationResult',
]
