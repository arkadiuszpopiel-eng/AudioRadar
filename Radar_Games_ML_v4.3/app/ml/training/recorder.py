"""
Radar Games ML v4.2.0 - Labeled Audio Recorder
Records audio with real-time labeling support for ML training

Features:
- Continuous audio recording
- Real-time label addition during recording
- Hotkey support for quick labeling
- Buffer management for long recordings
"""

import numpy as np
import threading
import time
from typing import Optional, Callable, List
from dataclasses import dataclass
from enum import Enum, auto

from app.core.logger import log
from app.core.constants import SAMPLE_RATE, CHANNELS, BLOCK_SIZE

from .session_manager import SessionManager, LabeledSession, AudioLabel


class RecordingStateEnum(Enum):
    """
    Finite State Machine states for recording lifecycle (v4.2.1-k0009).

    State transitions:
    - IDLE -> STARTING -> RECORDING
    - RECORDING -> STOPPING -> IDLE
    - Any -> ERROR (on exception)
    """
    IDLE = auto()        # Not recording, ready to start
    STARTING = auto()    # Initializing session, creating directories
    RECORDING = auto()   # Actively recording audio
    STOPPING = auto()    # Saving session, finalizing
    ERROR = auto()       # Error state, requires reset


@dataclass
class RecordingState:
    """Current recording state (v4.2.1-k0009: Added FSM)."""
    is_recording: bool = False
    start_time: float = 0.0
    elapsed_sec: float = 0.0
    samples_recorded: int = 0
    labels_added: int = 0
    fsm_state: RecordingStateEnum = RecordingStateEnum.IDLE  # v4.2.1-k0009: FSM state


class LabeledRecorder:
    """
    Audio recorder with real-time labeling support.

    Records audio data while allowing users to add labels
    at specific timestamps during the recording.
    """

    # Maximum recording duration (30 minutes)
    MAX_DURATION_SEC = 30 * 60

    # Buffer chunk size (1 second of audio)
    CHUNK_DURATION_SEC = 1.0

    def __init__(
        self,
        session_manager: Optional[SessionManager] = None,
        sample_rate: int = SAMPLE_RATE,
        channels: int = CHANNELS
    ):
        """
        Initialize labeled recorder.

        Args:
            session_manager: SessionManager instance (creates one if None)
            sample_rate: Audio sample rate
            channels: Number of audio channels
        """
        self.session_manager = session_manager or SessionManager()
        self.sample_rate = sample_rate
        self.channels = channels

        # Current session
        self._session: Optional[LabeledSession] = None
        self._audio_buffer: List[np.ndarray] = []

        # Recording state (v4.2.1-k0009: FSM initialized to IDLE)
        self._state = RecordingState(fsm_state=RecordingStateEnum.IDLE)
        self._lock = threading.RLock()  # FIXED v4.3.1-k0018: Use RLock to allow reentrant locking (same thread can acquire multiple times)
        self._error_message: Optional[str] = None  # v4.2.1-k0009: Error tracking

        # Callbacks
        self._on_state_change: Optional[Callable[[RecordingState], None]] = None
        self._on_label_added: Optional[Callable[[AudioLabel], None]] = None

        log("LabeledRecorder initialized (FSM: IDLE)", "INFO")

    @property
    def is_recording(self) -> bool:
        """Check if currently recording."""
        return self._state.is_recording

    @property
    def elapsed_seconds(self) -> float:
        """Get elapsed recording time in seconds."""
        if self._state.is_recording:
            return time.time() - self._state.start_time
        return self._state.elapsed_sec

    @property
    def current_session(self) -> Optional[LabeledSession]:
        """Get current session."""
        return self._session

    @property
    def state(self) -> RecordingState:
        """Get current recording state."""
        with self._lock:
            if self._state.is_recording:
                self._state.elapsed_sec = time.time() - self._state.start_time
            return RecordingState(
                is_recording=self._state.is_recording,
                start_time=self._state.start_time,
                elapsed_sec=self._state.elapsed_sec,
                samples_recorded=self._state.samples_recorded,
                labels_added=self._state.labels_added,
            )

    def set_callbacks(
        self,
        on_state_change: Optional[Callable[[RecordingState], None]] = None,
        on_label_added: Optional[Callable[[AudioLabel], None]] = None
    ) -> None:
        """Set callback functions for state changes and label additions."""
        self._on_state_change = on_state_change
        self._on_label_added = on_label_added

    def _transition_state(self, new_state: RecordingStateEnum, error_msg: Optional[str] = None) -> None:
        """
        Transition to a new FSM state (v4.2.1-k0009).

        Args:
            new_state: Target FSM state
            error_msg: Optional error message for ERROR state
        """
        old_state = self._state.fsm_state
        self._state.fsm_state = new_state

        if new_state == RecordingStateEnum.ERROR:
            self._error_message = error_msg
        else:
            self._error_message = None

        log(f"FSM transition: {old_state.name} -> {new_state.name}" +
            (f" (error: {error_msg})" if error_msg else ""), "INFO")

        if self._on_state_change:
            log(f"[DEBUG] _transition_state: About to call on_state_change callback", "DEBUG")
            self._on_state_change(self.state)
            log(f"[DEBUG] _transition_state: on_state_change callback returned", "DEBUG")

    def start_recording(self, notes: str = "") -> bool:
        """
        Start a new recording session.

        FIXED v4.2.1-k0009: FSM state management, async directory creation callback

        Args:
            notes: Optional session notes

        Returns:
            True if recording started successfully
        """
        with self._lock:
            # FSM: Only allow start from IDLE state
            if self._state.fsm_state != RecordingStateEnum.IDLE:
                log(f"Cannot start recording from state {self._state.fsm_state.name}", "WARNING")
                return False

            try:
                # Transition to STARTING
                self._transition_state(RecordingStateEnum.STARTING)
                log(f"[DEBUG] CHECKPOINT 1: After transition to STARTING", "DEBUG")

                # FIXED v4.3.1-k0017: Callback must handle BOTH success and error
                # Only transition to RECORDING after directory is successfully created
                log(f"[DEBUG] CHECKPOINT 2: About to define callback", "DEBUG")
                def on_dir_created(success: bool, error: Optional[str]) -> None:
                    log(f"[DEBUG] on_dir_created callback called: success={success}, error={error}", "DEBUG")
                    with self._lock:
                        if not success:
                            log(f"Session directory creation failed: {error}", "ERROR")
                            self._transition_state(RecordingStateEnum.ERROR, error)
                        else:
                            # Success: transition STARTING -> RECORDING
                            self._state.is_recording = True
                            self._state.start_time = time.time()
                            self._state.elapsed_sec = 0.0
                            self._state.samples_recorded = 0
                            self._state.labels_added = 0

                            self._transition_state(RecordingStateEnum.RECORDING)
                            log(f"Recording started: {self._session.session_id}", "INFO")

                log(f"[DEBUG] CHECKPOINT 3: Callback defined successfully", "DEBUG")
                log(f"[DEBUG] About to call create_session, session_manager={self.session_manager}", "DEBUG")
                self._session = self.session_manager.create_session(
                    sample_rate=self.sample_rate,
                    channels=self.channels,
                    notes=notes,
                    callback=on_dir_created
                )
                log(f"[DEBUG] create_session returned, session_id={self._session.session_id}", "DEBUG")

                # Reset buffers (safe to do immediately)
                self._audio_buffer = []

                # FIXED v4.3.1-k0017: Return True to indicate start was queued
                # Actual RECORDING transition happens in callback
                log(f"Recording start queued: {self._session.session_id}", "INFO")
                return True

            except Exception as e:
                log(f"Error starting recording: {e}", "ERROR")
                self._transition_state(RecordingStateEnum.ERROR, str(e))
                return False

    def stop_recording(self) -> Optional[LabeledSession]:
        """
        Stop recording and save the session.

        FIXED v4.2.1-k0009: FSM state management, async save callback

        Returns:
            Completed LabeledSession or None on error
        """
        with self._lock:
            # FSM: Only allow stop from RECORDING state
            if self._state.fsm_state != RecordingStateEnum.RECORDING:
                log(f"Cannot stop recording from state {self._state.fsm_state.name}", "WARNING")
                return None

            try:
                # Transition to STOPPING
                self._transition_state(RecordingStateEnum.STOPPING)

                # Calculate final duration
                duration = time.time() - self._state.start_time
                self._session.duration_sec = duration

                # Combine audio buffers
                if self._audio_buffer:
                    audio_data = np.concatenate(self._audio_buffer, axis=0)
                else:
                    audio_data = np.array([], dtype=np.float32)

                # Async save callback
                def on_save_complete(success: bool, error: Optional[str]) -> None:
                    with self._lock:
                        if not success:
                            log(f"Session save failed: {error}", "ERROR")
                            self._transition_state(RecordingStateEnum.ERROR, error)
                        else:
                            # Transition back to IDLE
                            self._transition_state(RecordingStateEnum.IDLE)

                # Save session (async)
                success = self.session_manager.save_session(
                    self._session,
                    audio_data=audio_data if len(audio_data) > 0 else None,
                    callback=on_save_complete
                )

                if not success:
                    log("Failed to queue session save", "ERROR")
                    self._transition_state(RecordingStateEnum.ERROR, "Failed to queue save")
                    return None

                # Update state
                self._state.is_recording = False
                self._state.elapsed_sec = duration

                log(f"Recording stopped: {duration:.1f}s, {len(self._session.labels)} labels", "INFO")

                completed_session = self._session
                self._session = None
                self._audio_buffer = []

                return completed_session

            except Exception as e:
                log(f"Error stopping recording: {e}", "ERROR")
                self._state.is_recording = False
                self._transition_state(RecordingStateEnum.ERROR, str(e))
                return None

    def add_audio_block(self, block: np.ndarray) -> None:
        """
        Add an audio block to the recording buffer.

        Called by the main audio processing loop.

        Args:
            block: Audio data block (samples, channels)
        """
        if not self._state.is_recording:
            return

        with self._lock:
            # Check max duration
            elapsed = time.time() - self._state.start_time
            if elapsed >= self.MAX_DURATION_SEC:
                log("Max recording duration reached", "WARNING")
                # Don't auto-stop here, just skip adding more data
                return

            # Add to buffer
            self._audio_buffer.append(block.copy())
            self._state.samples_recorded += len(block)

    def add_label(
        self,
        label_class: str,
        description: str = "",
        is_interval_start: bool = False
    ) -> Optional[AudioLabel]:
        """
        Add a label at the current recording timestamp.

        Args:
            label_class: Label category
            description: Optional description
            is_interval_start: If True, marks start of interval (end with add_label_end)

        Returns:
            Created AudioLabel or None on error
        """
        if not self._state.is_recording or not self._session:
            log("Cannot add label: not recording", "WARNING")
            return None

        with self._lock:
            try:
                timestamp = time.time() - self._state.start_time

                label = self._session.add_label(
                    label_class=label_class,
                    timestamp_sec=timestamp,
                    description=description,
                )

                self._state.labels_added += 1

                log(f"Label added: {label_class} at {timestamp:.2f}s", "INFO")

                if self._on_label_added:
                    self._on_label_added(label)

                return label

            except Exception as e:
                log(f"Error adding label: {e}", "ERROR")
                return None

    def add_label_with_hotkey(self, hotkey_index: int) -> Optional[AudioLabel]:
        """
        Add a label using a hotkey index (1-8 → label class).

        Args:
            hotkey_index: 1-based hotkey index

        Returns:
            Created AudioLabel or None
        """
        if hotkey_index < 1 or hotkey_index > len(SessionManager.DEFAULT_LABEL_CLASSES):
            return None

        label_class = SessionManager.DEFAULT_LABEL_CLASSES[hotkey_index - 1]
        return self.add_label(label_class)

    def remove_last_label(self) -> bool:
        """Remove the last added label."""
        if not self._session or not self._session.labels:
            return False

        with self._lock:
            last_label = self._session.labels[-1]
            self._session.labels.pop()
            self._state.labels_added = max(0, self._state.labels_added - 1)
            log(f"Removed label: {last_label.label_class}", "INFO")
            return True

    def get_labels(self) -> List[AudioLabel]:
        """Get all labels in current session."""
        if not self._session:
            return []
        return self._session.labels.copy()

    def discard_recording(self) -> None:
        """Discard current recording without saving."""
        with self._lock:
            if self._state.is_recording:
                log("Recording discarded", "INFO")

            self._state.is_recording = False
            self._state.elapsed_sec = 0.0
            self._state.samples_recorded = 0
            self._state.labels_added = 0
            self._session = None
            self._audio_buffer = []

            if self._on_state_change:
                self._on_state_change(self.state)
