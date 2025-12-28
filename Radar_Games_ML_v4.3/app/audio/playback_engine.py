"""
Radar Games ML v4.3 - Audio Playback Engine
Thread-safe audio playback using sounddevice with position tracking.

Features:
- Play/Pause/Stop/Seek controls
- Real-time position tracking
- Segment/loop playback
- Qt signal integration for UI updates
"""

from __future__ import annotations

import threading
import time
from enum import Enum, auto
from typing import Optional

import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

from app.core.logger import log

try:
    import sounddevice as sd
    SD_AVAILABLE = True
except ImportError:
    SD_AVAILABLE = False
    log("sounddevice not available - audio playback disabled", "WARNING")


class PlaybackState(Enum):
    """Playback engine states."""
    STOPPED = auto()
    PLAYING = auto()
    PAUSED = auto()


class AudioPlaybackEngine(QObject):
    """
    Thread-safe audio playback engine using sounddevice.

    Signals:
        position_changed: Emitted during playback with current position (seconds)
        playback_finished: Emitted when playback reaches end
        state_changed: Emitted when playback state changes
        error_occurred: Emitted when playback error occurs
    """

    # Qt Signals
    position_changed = pyqtSignal(float)  # position_sec
    playback_finished = pyqtSignal()
    state_changed = pyqtSignal(object)  # PlaybackState
    error_occurred = pyqtSignal(str)  # error_message

    def __init__(self, sample_rate: int = 48000):
        super().__init__()

        if not SD_AVAILABLE:
            log("AudioPlaybackEngine initialized without sounddevice support", "WARNING")

        # Audio configuration
        self.sample_rate = sample_rate
        self.audio_data: Optional[np.ndarray] = None
        self.channels = 1
        self.duration_sec = 0.0

        # Playback state
        self._state = PlaybackState.STOPPED
        self._state_lock = threading.RLock()
        self.position_sec = 0.0
        self._position_lock = threading.RLock()

        # Playback control
        self._stream: Optional[sd.OutputStream] = None
        self._playback_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()

        # Loop/segment playback
        self._loop_enabled = False
        self._loop_start_sec: Optional[float] = None
        self._loop_end_sec: Optional[float] = None

        # Position update timer (runs in Qt main thread)
        self._position_timer = QTimer()
        self._position_timer.timeout.connect(self._emit_position_update)

        log("AudioPlaybackEngine initialized", "INFO")

    @property
    def state(self) -> PlaybackState:
        """Get current playback state (thread-safe)."""
        with self._state_lock:
            return self._state

    def _set_state(self, new_state: PlaybackState):
        """Set playback state and emit signal (thread-safe)."""
        with self._state_lock:
            if self._state != new_state:
                self._state = new_state
                self.state_changed.emit(new_state)
                log(f"Playback state: {new_state.name}", "INFO")

    @property
    def position(self) -> float:
        """Get current playback position in seconds (thread-safe)."""
        with self._position_lock:
            return self.position_sec

    def _set_position(self, position: float):
        """Set playback position (thread-safe)."""
        with self._position_lock:
            self.position_sec = max(0.0, min(position, self.duration_sec))

    def load_audio(self, audio_data: np.ndarray, sample_rate: int):
        """
        Load audio data for playback.

        Args:
            audio_data: Audio samples (mono or stereo)
            sample_rate: Sample rate in Hz
        """
        # Stop any ongoing playback
        if self.state != PlaybackState.STOPPED:
            self.stop()

        # Handle mono/stereo
        if audio_data.ndim == 1:
            self.channels = 1
            self.audio_data = audio_data.reshape(-1, 1)  # Convert to 2D for sounddevice
        else:
            self.channels = audio_data.shape[1]
            self.audio_data = audio_data

        self.sample_rate = sample_rate
        self.duration_sec = len(audio_data) / sample_rate
        self._set_position(0.0)

        log(f"Audio loaded: {self.duration_sec:.2f}s, {self.channels}ch, {sample_rate}Hz", "INFO")

    def play(self, start_sec: Optional[float] = None):
        """
        Start playback from position.

        Args:
            start_sec: Start position in seconds (None = resume from current)
        """
        if not SD_AVAILABLE:
            self.error_occurred.emit("sounddevice not available")
            return

        if self.audio_data is None:
            self.error_occurred.emit("No audio loaded")
            return

        # If paused, resume
        if self.state == PlaybackState.PAUSED:
            self._pause_event.clear()

            # Restart position timer (v4.3.1-k0024: Fix resume from pause)
            self._position_timer.start(100)

            self._set_state(PlaybackState.PLAYING)
            return

        # If already playing, do nothing
        if self.state == PlaybackState.PLAYING:
            return

        # Set start position
        if start_sec is not None:
            self._set_position(start_sec)

        # Start playback thread
        self._stop_event.clear()
        self._pause_event.clear()
        self._playback_thread = threading.Thread(
            target=self._playback_worker,
            daemon=True,
            name="AudioPlaybackThread"
        )
        self._playback_thread.start()

        # Start position update timer
        self._position_timer.start(100)  # Update every 100ms

        self._set_state(PlaybackState.PLAYING)
        log(f"Playback started at {self.position:.2f}s", "INFO")

    def pause(self):
        """Pause playback (can be resumed)."""
        if self.state != PlaybackState.PLAYING:
            return

        self._pause_event.set()

        # Stop position timer while paused (v4.3.1-k0024: Fix pause button)
        self._position_timer.stop()

        self._set_state(PlaybackState.PAUSED)
        log("Playback paused", "INFO")

    def stop(self):
        """Stop playback and reset position."""
        if self.state == PlaybackState.STOPPED:
            return

        # Signal thread to stop
        self._stop_event.set()
        self._pause_event.clear()

        # Stop position timer
        self._position_timer.stop()

        # Wait for thread to finish
        if self._playback_thread and self._playback_thread.is_alive():
            self._playback_thread.join(timeout=1.0)

        # Stop and close stream
        if self._stream:
            try:
                self._stream.stop()
                self._stream.close()
            except Exception:
                pass
            self._stream = None

        self._set_position(0.0)
        self._set_state(PlaybackState.STOPPED)
        log("Playback stopped", "INFO")

    def seek(self, position_sec: float):
        """
        Seek to position.

        Args:
            position_sec: Target position in seconds
        """
        if self.audio_data is None:
            return

        was_playing = (self.state == PlaybackState.PLAYING)

        # Stop current playback
        if self.state != PlaybackState.STOPPED:
            self.stop()

        # Set new position
        self._set_position(position_sec)

        # Resume if was playing
        if was_playing:
            self.play()
        else:
            # Just emit position update for UI
            self.position_changed.emit(self.position)

        log(f"Seeked to {position_sec:.2f}s", "INFO")

    def set_loop_region(self, start_sec: float, end_sec: float, enabled: bool = True):
        """
        Set loop/segment playback region.

        Args:
            start_sec: Loop start in seconds
            end_sec: Loop end in seconds
            enabled: Whether to enable looping
        """
        self._loop_start_sec = start_sec
        self._loop_end_sec = end_sec
        self._loop_enabled = enabled

        if enabled:
            log(f"Loop region set: {start_sec:.2f}s - {end_sec:.2f}s", "INFO")
        else:
            log("Loop disabled", "INFO")

    def clear_loop(self):
        """Disable loop playback."""
        self._loop_enabled = False
        self._loop_start_sec = None
        self._loop_end_sec = None

    def _playback_worker(self):
        """
        Playback worker thread.
        Uses sounddevice callback for audio output.
        """
        try:
            # Calculate sample positions
            current_sample = int(self.position * self.sample_rate)

            # Create output stream with callback
            def callback(outdata, frames, time_info, status):
                """sounddevice callback for audio output."""
                nonlocal current_sample

                if status:
                    log(f"sounddevice status: {status}", "WARNING")

                # Check for stop signal
                if self._stop_event.is_set():
                    raise sd.CallbackStop

                # Handle pause (v4.3.1-k0024: Fix pause - don't advance position)
                if self._pause_event.is_set():
                    outdata[:] = 0  # Output silence
                    # Don't update current_sample - stay at same position
                    return

                # Calculate end sample
                end_sample = current_sample + frames

                # Handle loop region
                if self._loop_enabled and self._loop_end_sec is not None:
                    loop_end_sample = int(self._loop_end_sec * self.sample_rate)

                    if end_sample >= loop_end_sample:
                        # Wrap to loop start
                        loop_start_sample = int(self._loop_start_sec * self.sample_rate)
                        current_sample = loop_start_sample
                        end_sample = current_sample + frames
                        self._set_position(self._loop_start_sec)

                # Handle end of audio
                if end_sample > len(self.audio_data):
                    # Fill remaining samples
                    remaining = len(self.audio_data) - current_sample
                    if remaining > 0:
                        outdata[:remaining] = self.audio_data[current_sample:current_sample + remaining]
                        outdata[remaining:] = 0
                    else:
                        outdata[:] = 0

                    # Signal end of playback
                    raise sd.CallbackStop

                # Copy audio data to output
                outdata[:] = self.audio_data[current_sample:end_sample]

                # Update position
                current_sample = end_sample
                self._set_position(current_sample / self.sample_rate)

            # Create and start stream
            self._stream = sd.OutputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                callback=callback,
                blocksize=2048,
                dtype=np.float32
            )

            with self._stream:
                # Keep thread alive while stream is active
                while not self._stop_event.is_set():
                    time.sleep(0.1)

        except sd.CallbackStop:
            # Normal end of playback
            log("Playback finished", "INFO")
            self.playback_finished.emit()

        except Exception as e:
            log(f"Playback error: {e}", "ERROR")
            self.error_occurred.emit(str(e))

        finally:
            # Cleanup
            if self._stream:
                try:
                    self._stream.close()
                except Exception:
                    pass
                self._stream = None

            # Update state
            if not self._pause_event.is_set():
                self._set_state(PlaybackState.STOPPED)

    def _emit_position_update(self):
        """Timer callback to emit position updates (runs in Qt main thread)."""
        if self.state == PlaybackState.PLAYING:
            self.position_changed.emit(self.position)

    def cleanup(self):
        """Cleanup resources."""
        self.stop()
        self._position_timer.stop()
        log("AudioPlaybackEngine cleaned up", "INFO")
