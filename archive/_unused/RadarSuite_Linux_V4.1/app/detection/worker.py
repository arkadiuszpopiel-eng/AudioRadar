"""
RadarSuite v3.5.0 - Detection Worker
Thread pool for parallel detection processing
FIXED v3.5.0: Memory leak cleanup
"""

import threading
import time
from concurrent.futures import ThreadPoolExecutor

from core.logger import log
from core.constants import MAX_WORKERS, CLEANUP_INTERVAL_SEC, DETECTION_TIMEOUT_SEC


class DetectionWorker:
    """
    Worker thread for parallel audio detection processing
    Offloads heavy computation from main UI thread

    ENHANCED v3.5.0: Thread-safe shutdown with timeout
    FIXED v3.5.0: Memory leak - automatic cleanup of completed futures
    """

    def __init__(self, max_workers=3):
        log(f"DetectionWorker.__init__ (max_workers={max_workers})", "INFO")
        self.executor = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="DetectionWorker")
        self.active_futures = []
        self.shutdown_event = threading.Event()
        self._lock = threading.Lock()

        # FIXED v3.5.0: Periodic cleanup to prevent memory leak
        self._cleanup_timer = None
        self._start_periodic_cleanup()

    def _start_periodic_cleanup(self):
        """Start periodic cleanup timer (every 10 seconds)"""
        if not self.shutdown_event.is_set():
            self._cleanup_done_futures()
            self._cleanup_timer = threading.Timer(CLEANUP_INTERVAL_SEC, self._start_periodic_cleanup)  # FIXED v3.5.0: Use constant
            self._cleanup_timer.daemon = True
            self._cleanup_timer.start()

    def _cleanup_done_futures(self):
        """Remove completed futures from list (MEMORY LEAK FIX)"""
        with self._lock:
            before_count = len(self.active_futures)
            self.active_futures = [f for f in self.active_futures if not f.done()]
            cleaned_count = before_count - len(self.active_futures)

            if cleaned_count > 0:
                log(f"Cleaned {cleaned_count} completed futures (remaining: {len(self.active_futures)})", "DEBUG")

    def submit_detection(self, det_panel, block, sample_rate, fft_cache):
        """Submit detection task to worker pool (with automatic cleanup)"""
        if self.shutdown_event.is_set():
            log("Worker pool shutting down, rejecting new detection task", "WARNING")
            return None

        # FIXED v3.5.0: Cleanup before submit to prevent unbounded growth
        with self._lock:
            self.active_futures = [f for f in self.active_futures if not f.done()]

        future = self.executor.submit(self._run_detection, det_panel, block, sample_rate, fft_cache)

        with self._lock:
            self.active_futures.append(future)

        return future

    def submit_localization(self, compute_func, block, sample_rate):
        """Submit 3D localization task to worker pool (with automatic cleanup)"""
        if self.shutdown_event.is_set():
            log("Worker pool shutting down, rejecting new localization task", "WARNING")
            return None

        # FIXED v3.5.0: Cleanup before submit
        with self._lock:
            self.active_futures = [f for f in self.active_futures if not f.done()]

        future = self.executor.submit(compute_func, block, sample_rate)

        with self._lock:
            self.active_futures.append(future)

        return future

    def submit_classification(self, classifier, block, sample_rate, fft_cache):
        """Submit sound classification task to worker pool (with automatic cleanup)"""
        if self.shutdown_event.is_set():
            log("Worker pool shutting down, rejecting new classification task", "WARNING")
            return None

        # FIXED v3.5.0: Cleanup before submit
        with self._lock:
            self.active_futures = [f for f in self.active_futures if not f.done()]

        future = self.executor.submit(self._run_classification, classifier, block, sample_rate, fft_cache)

        with self._lock:
            self.active_futures.append(future)

        return future

    @staticmethod
    def _run_detection(det_panel, block, sample_rate, fft_cache):
        """Run detection in worker thread (uses cached FFT)"""
        try:
            # Use cached FFT data
            events, bands = det_panel.analyze(block, sample_rate, fft_cache=fft_cache)
            return events, bands
        except Exception as e:
            log(f"Error in detection worker: {e}", "ERROR")
            return {'walk': False, 'run': False, 'shot': False}, {}

    @staticmethod
    def _run_classification(classifier, block, sample_rate, fft_cache):
        """Run classification in worker thread (uses cached FFT)"""
        try:
            return classifier.classify_sound(block, sample_rate, fft_cache=fft_cache)
        except Exception as e:
            log(f"Error in classification worker: {e}", "ERROR")
            return {'type': 'unknown', 'confidence': 0, 'details': {}}

    def shutdown(self, timeout=DETECTION_TIMEOUT_SEC):  # FIXED v3.5.0: Use constant
        """
        Thread-safe shutdown with timeout

        Args:
            timeout: Maximum time to wait for tasks to complete (seconds)

        ENHANCED v3.5.0: Proper cleanup with cancel_futures + timer cleanup
        """
        log(f"DetectionWorker.shutdown (timeout={timeout}s)", "INFO")
        self.shutdown_event.set()

        # FIXED v3.5.0: Stop periodic cleanup timer
        if self._cleanup_timer is not None:
            self._cleanup_timer.cancel()
            log("Cleanup timer stopped", "DEBUG")

        # Cancel pending futures
        cancelled_count = 0
        with self._lock:
            for future in self.active_futures:
                if not future.done():
                    cancelled = future.cancel()
                    if cancelled:
                        cancelled_count += 1

        if cancelled_count > 0:
            log(f"Cancelled {cancelled_count} pending tasks", "INFO")

        # Wait for running tasks with timeout
        try:
            self.executor.shutdown(wait=True, timeout=timeout)
            log("DetectionWorker shutdown complete", "INFO")
        except Exception as e:
            log(f"DetectionWorker shutdown error: {e}", "WARNING")
            # Force shutdown if timeout exceeded
            self.executor.shutdown(wait=False, cancel_futures=True)
            log("Forced shutdown after timeout", "WARNING")

