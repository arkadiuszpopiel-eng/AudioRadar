"""
Radar Games ML v4.2.1-k0009 - Async Session Worker
Non-blocking I/O operations for ML Training sessions

FIXED v4.2.1-k0009: Prevent GUI freezing by moving disk I/O to background thread
"""
from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Optional, Callable, TYPE_CHECKING
from queue import Queue, Empty
from dataclasses import dataclass
from enum import Enum

import numpy as np

from app.core.logger import log

if TYPE_CHECKING:
    from .session_manager import LabeledSession


class SessionOperationType(Enum):
    """Types of session operations."""
    CREATE_DIR = "create_dir"
    SAVE_METADATA = "save_metadata"
    SAVE_LABELS = "save_labels"
    SAVE_AUDIO = "save_audio"
    LOAD_SESSION = "load_session"


@dataclass
class SessionOperation:
    """Represents a queued session operation."""
    op_type: SessionOperationType
    session: Optional['LabeledSession'] = None
    session_id: Optional[str] = None
    session_dir: Optional[Path] = None
    audio_data: Optional[np.ndarray] = None
    callback: Optional[Callable[[bool, Optional[str]], None]] = None


class AsyncSessionWorker:
    """
    Background worker for non-blocking session I/O operations.

    Runs in a separate thread to prevent GUI freezing during:
    - Directory creation (can be slow on Windows with antivirus)
    - JSON serialization/deserialization
    - Large numpy array saves

    v4.2.1-k0009: Thread-safe queue-based design
    """

    def __init__(self):
        """Initialize async session worker."""
        self._queue: Queue[Optional[SessionOperation]] = Queue()
        self._worker_thread: Optional[threading.Thread] = None
        self._running = False
        self._lock = threading.Lock()

        log("AsyncSessionWorker initialized", "INFO")

    def start(self) -> None:
        """Start the background worker thread."""
        with self._lock:
            if self._running:
                log("AsyncSessionWorker already running", "WARNING")
                return

            self._running = True
            self._worker_thread = threading.Thread(
                target=self._worker_loop,
                name="AsyncSessionWorker",
                daemon=True
            )
            self._worker_thread.start()
            log("AsyncSessionWorker thread started", "INFO")

    def stop(self, wait_for_pending: bool = True, timeout: float = 10.0) -> bool:
        """
        Stop the background worker thread.

        FIXED v4.3.0-k0001: Graceful shutdown with pending operations flush

        Args:
            wait_for_pending: Wait for pending operations to complete
            timeout: Maximum time to wait for pending operations (seconds)

        Returns:
            True if stopped gracefully, False if timed out
        """
        with self._lock:
            if not self._running:
                return True

            pending_count = self._queue.qsize()
            if pending_count > 0:
                log(f"AsyncSessionWorker: {pending_count} pending operations", "INFO")

            self._running = False

        # Wait for queue to empty if requested
        if wait_for_pending and pending_count > 0:
            log(f"Waiting for {pending_count} pending operations (max {timeout}s)...", "INFO")
            import time
            start_time = time.time()

            while not self._queue.empty() and (time.time() - start_time) < timeout:
                time.sleep(0.1)

            remaining = self._queue.qsize()
            if remaining > 0:
                log(f"Warning: {remaining} operations not completed (timeout)", "WARNING")

        # Signal worker to stop
        self._queue.put(None)

        if self._worker_thread and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=5.0)
            if self._worker_thread.is_alive():
                log("AsyncSessionWorker thread did not stop gracefully", "WARNING")
                return False
            else:
                log("AsyncSessionWorker thread stopped gracefully", "INFO")
                return True

        return True

    def queue_create_dir(
        self,
        session_dir: Path,
        callback: Optional[Callable[[bool, Optional[str]], None]] = None
    ) -> None:
        """
        Queue directory creation operation.

        Args:
            session_dir: Directory to create
            callback: Optional callback(success: bool, error_msg: Optional[str])
        """
        op = SessionOperation(
            op_type=SessionOperationType.CREATE_DIR,
            session_dir=session_dir,
            callback=callback
        )
        self._queue.put(op)

    def queue_save_session(
        self,
        session: 'LabeledSession',
        session_dir: Path,
        audio_data: Optional[np.ndarray] = None,
        callback: Optional[Callable[[bool, Optional[str]], None]] = None
    ) -> None:
        """
        Queue complete session save operation.

        Args:
            session: Session to save
            session_dir: Directory to save to
            audio_data: Optional audio data
            callback: Optional callback(success: bool, error_msg: Optional[str])
        """
        op = SessionOperation(
            op_type=SessionOperationType.SAVE_METADATA,
            session=session,
            session_dir=session_dir,
            audio_data=audio_data,
            callback=callback
        )
        self._queue.put(op)

    def _worker_loop(self) -> None:
        """Main worker thread loop."""
        log("AsyncSessionWorker loop started", "INFO")

        while self._running:
            try:
                # Block with timeout to allow checking _running flag
                op = self._queue.get(timeout=1.0)

                if op is None:
                    # Stop signal
                    break

                # Process operation
                self._process_operation(op)

            except Empty:
                # Timeout - just continue
                continue
            except Exception as e:
                log(f"AsyncSessionWorker error in loop: {e}", "ERROR")
                import traceback
                log(traceback.format_exc(), "ERROR")

        log("AsyncSessionWorker loop exited", "INFO")

    def _process_operation(self, op: SessionOperation) -> None:
        """Process a single operation."""
        try:
            if op.op_type == SessionOperationType.CREATE_DIR:
                self._do_create_dir(op)
            elif op.op_type == SessionOperationType.SAVE_METADATA:
                self._do_save_session(op)
            else:
                log(f"Unknown operation type: {op.op_type}", "WARNING")

        except Exception as e:
            log(f"Error processing operation {op.op_type}: {e}", "ERROR")
            if op.callback:
                try:
                    op.callback(False, str(e))
                except Exception as cb_err:
                    log(f"Error in operation callback: {cb_err}", "ERROR")

    def _do_create_dir(self, op: SessionOperation) -> None:
        """Execute directory creation."""
        log(f"[DEBUG] AsyncWorker: _do_create_dir started for {op.session_dir}", "DEBUG")
        try:
            if op.session_dir is None:
                raise ValueError("session_dir is None")

            log(f"[DEBUG] AsyncWorker: About to create directory {op.session_dir}", "DEBUG")
            op.session_dir.mkdir(parents=True, exist_ok=True)
            log(f"Created directory: {op.session_dir}", "INFO")

            if op.callback:
                log(f"[DEBUG] AsyncWorker: Calling callback with success=True", "DEBUG")
                op.callback(True, None)
                log(f"[DEBUG] AsyncWorker: Callback returned", "DEBUG")
            else:
                log(f"[DEBUG] AsyncWorker: No callback provided", "DEBUG")

        except Exception as e:
            log(f"Error creating directory {op.session_dir}: {e}", "ERROR")
            if op.callback:
                op.callback(False, str(e))

    def _do_save_session(self, op: SessionOperation) -> None:
        """Execute complete session save."""
        try:
            if op.session is None or op.session_dir is None:
                raise ValueError("session or session_dir is None")

            # Ensure directory exists
            op.session_dir.mkdir(parents=True, exist_ok=True)

            # Save metadata
            metadata_path = op.session_dir / "metadata.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(op.session.to_metadata_dict(), f, indent=2)

            # Save labels
            labels_path = op.session_dir / "labels.json"
            with open(labels_path, 'w', encoding='utf-8') as f:
                json.dump(op.session.to_labels_dict(), f, indent=2)

            # Save audio data if provided
            if op.audio_data is not None:
                audio_path = op.session_dir / "audio.npy"
                np.save(audio_path, op.audio_data)
                log(f"Saved audio: {op.audio_data.shape} samples", "INFO")

            log(f"Session saved: {op.session.session_id}", "INFO")

            if op.callback:
                op.callback(True, None)

        except Exception as e:
            log(f"Error saving session {op.session.session_id if op.session else 'unknown'}: {e}", "ERROR")
            if op.callback:
                op.callback(False, str(e))


# Global worker instance (lazy-initialized)
_global_worker: Optional[AsyncSessionWorker] = None
_worker_lock = threading.Lock()


def get_session_worker() -> AsyncSessionWorker:
    """Get or create the global async session worker."""
    global _global_worker

    with _worker_lock:
        if _global_worker is None:
            _global_worker = AsyncSessionWorker()
            _global_worker.start()

        return _global_worker


def stop_session_worker() -> None:
    """Stop the global async session worker."""
    global _global_worker

    with _worker_lock:
        if _global_worker is not None:
            _global_worker.stop()
            _global_worker = None
