"""
Recording controller shared between ML Training panel and quick overlay.

Provides a single source of truth for recording state, level monitoring and
label operations so multiple widgets stay in sync.

ENHANCED v4.3.1-k0023: Added noise reduction and audio enhancement for cleaner recordings
"""
from __future__ import annotations

import threading
from pathlib import Path
from typing import Callable, List, Optional

import numpy as np
from scipy import signal

from app.core.logger import log

from .recorder import LabeledRecorder, RecordingState
from .session_manager import SessionManager, AudioLabel, LabeledSession


class InMemorySessionManager(SessionManager):
    """Lightweight session manager used for tests/self-test to avoid disk I/O."""

    def __init__(self):  # pragma: no cover - trivial wrapper
        super().__init__(base_path=Path("./Data/TestSessions"))
        self.last_saved_session: Optional[LabeledSession] = None

    def save_session(self, session: LabeledSession, audio_data: Optional[np.ndarray] = None) -> bool:
        # Store session in memory to avoid blocking disk writes during diagnostics
        self.last_saved_session = session
        if audio_data is not None:
            session.cached_audio = audio_data  # type: ignore[attr-defined]
        log(f"In-memory session saved: {session.session_id}", "INFO")
        return True


class RecordingController:
    """Shared controller coordinating labeled recordings (v4.3.1-k0023: With noise reduction)."""

    def __init__(self, session_manager: Optional[SessionManager] = None, test_mode: bool = False, sample_rate: int = 48000):
        self._test_mode = test_mode
        if session_manager is None:
            session_manager = InMemorySessionManager() if test_mode else SessionManager()
        self.session_manager = session_manager
        self.recorder = LabeledRecorder(self.session_manager)

        self._state_listeners: List[Callable[[RecordingState], None]] = []
        self._label_listeners: List[Callable[[AudioLabel], None]] = []
        self._level_listeners: List[Callable[[float], None]] = []
        self._last_session: Optional[LabeledSession] = None
        self._level_lock = threading.Lock()
        self._smoothed_level = 0.0

        # v4.3.1-k0023: Noise reduction settings
        self.noise_reduction_enabled = True  # Enable by default for better quality
        self.noise_gate_threshold = 0.01     # RMS threshold for noise gate
        self.sample_rate = sample_rate

        # v4.3.1-k0023: High-pass filter for low-frequency noise removal
        # Remove frequencies below 80 Hz (rumble, electrical hum)
        self._highpass_filter = self._create_highpass_filter(cutoff=80, order=4)

        self.recorder.set_callbacks(
            on_state_change=self._emit_state_change,
            on_label_added=self._emit_label_added,
        )

    # ------------------------------------------------------------------
    # Listener registration
    # ------------------------------------------------------------------
    def add_state_listener(self, callback: Callable[[RecordingState], None]) -> None:
        self._state_listeners.append(callback)

    def add_label_listener(self, callback: Callable[[AudioLabel], None]) -> None:
        self._label_listeners.append(callback)

    def add_level_listener(self, callback: Callable[[float], None]) -> None:
        self._level_listeners.append(callback)

    # ------------------------------------------------------------------
    # Recording lifecycle
    # ------------------------------------------------------------------
    def start_recording(self, notes: str = "") -> bool:
        started = self.recorder.start_recording(notes=notes)
        if started:
            self._last_session = None
        return started

    def stop_recording(self) -> Optional[LabeledSession]:
        session = self.recorder.stop_recording()
        if session:
            self._last_session = session
        return session

    def pause_recording(self) -> bool:
        """Pause the current recording (v4.3.1-k0023)."""
        return self.recorder.pause_recording()

    def resume_recording(self) -> bool:
        """Resume a paused recording (v4.3.1-k0023)."""
        return self.recorder.resume_recording()

    def discard_recording(self) -> None:
        self.recorder.discard_recording()
        self._last_session = None

    # ------------------------------------------------------------------
    # Label management
    # ------------------------------------------------------------------
    def add_label(self, label_class: str, description: str = "") -> Optional[AudioLabel]:
        return self.recorder.add_label(label_class=label_class, description=description)

    def add_label_hotkey(self, index: int) -> Optional[AudioLabel]:
        return self.recorder.add_label_with_hotkey(index)

    def remove_last_label(self) -> bool:
        return self.recorder.remove_last_label()

    # ------------------------------------------------------------------
    # Audio feeding & metering
    # ------------------------------------------------------------------
    def feed_audio(self, block: np.ndarray) -> None:
        """Feed an audio block to the recorder and update level meters (v4.3.1-k0023: With noise reduction)."""
        if block is None or block.size == 0:
            return

        # v4.3.1-k0023: Apply noise reduction if enabled and recording
        if self.recorder.is_recording:
            if self.noise_reduction_enabled:
                block = self._apply_noise_reduction(block)
            self.recorder.add_audio_block(block)

        # Lightweight RMS level with smoothing for overlays/visualizations
        with self._level_lock:
            try:
                rms = float(np.sqrt(np.mean(np.square(block))))
            except Exception:
                rms = 0.0
            # Simple exponential smoothing for stable bars
            alpha = 0.2
            self._smoothed_level = (1 - alpha) * self._smoothed_level + alpha * rms
            level = min(max(self._smoothed_level * 10.0, 0.0), 1.0)

        for callback in list(self._level_listeners):
            try:
                callback(level)
            except Exception as exc:  # pragma: no cover - UI callbacks
                log(f"RecordingController level listener error: {exc}", "WARNING")

    def simulate_quick_capture(self, blocks: int = 3, block_size: int = 256) -> Optional[LabeledSession]:
        """Utility for self-test to run a short, non-blocking capture cycle."""

        if not self.start_recording():
            return None

        dummy = np.zeros((block_size,), dtype=np.float32)
        for _ in range(blocks):
            self.feed_audio(dummy)

        return self.stop_recording()

    # ------------------------------------------------------------------
    # Accessors
    # ------------------------------------------------------------------
    @property
    def last_session(self) -> Optional[LabeledSession]:
        return self._last_session

    @property
    def state(self) -> RecordingState:
        return self.recorder.state

    @property
    def test_mode(self) -> bool:
        return self._test_mode

    # ------------------------------------------------------------------
    # Internal dispatch
    # ------------------------------------------------------------------
    def _emit_state_change(self, state: RecordingState) -> None:
        for callback in list(self._state_listeners):
            try:
                callback(state)
            except Exception as exc:  # pragma: no cover - UI callbacks
                log(f"RecordingController state listener error: {exc}", "WARNING")

    def _emit_label_added(self, label: AudioLabel) -> None:
        for callback in list(self._label_listeners):
            try:
                callback(label)
            except Exception as exc:  # pragma: no cover - UI callbacks
                log(f"RecordingController label listener error: {exc}", "WARNING")

    # ------------------------------------------------------------------
    # v4.3.1-k0023: Noise Reduction & Audio Enhancement
    # ------------------------------------------------------------------
    def _create_highpass_filter(self, cutoff: float = 80, order: int = 4):
        """
        Create a high-pass Butterworth filter to remove low-frequency noise.

        Args:
            cutoff: Cutoff frequency in Hz
            order: Filter order

        Returns:
            Filter coefficients (b, a)
        """
        try:
            nyquist = self.sample_rate / 2
            normal_cutoff = cutoff / nyquist
            b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
            return (b, a)
        except Exception as e:
            log(f"Error creating high-pass filter: {e}", "ERROR")
            return None

    def _apply_noise_reduction(self, block: np.ndarray) -> np.ndarray:
        """
        Apply noise reduction to audio block.

        Techniques:
        1. High-pass filter to remove low-frequency rumble/hum
        2. Noise gate to reduce background noise
        3. Soft clipping to prevent distortion

        Args:
            block: Input audio block

        Returns:
            Filtered audio block
        """
        try:
            # Handle mono/stereo
            if block.ndim == 1:
                filtered = block.copy()
            else:
                filtered = block.copy()

            # 1. Apply high-pass filter (remove low-frequency noise < 80 Hz)
            if self._highpass_filter is not None:
                b, a = self._highpass_filter
                if filtered.ndim == 1:
                    filtered = signal.filtfilt(b, a, filtered)
                else:
                    # Apply to each channel
                    for ch in range(filtered.shape[1]):
                        filtered[:, ch] = signal.filtfilt(b, a, filtered[:, ch])

            # 2. Noise gate - reduce low-level background noise
            rms = np.sqrt(np.mean(np.square(filtered)))
            if rms < self.noise_gate_threshold:
                # Attenuate by 50% instead of complete silence for natural sound
                filtered *= 0.5

            # 3. Soft clipping to prevent distortion
            filtered = np.clip(filtered, -0.95, 0.95)

            return filtered

        except Exception as e:
            log(f"Error applying noise reduction: {e}", "WARNING")
            return block  # Return original if filtering fails
