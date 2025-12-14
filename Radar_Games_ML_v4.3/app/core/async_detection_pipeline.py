"""
Asynchronous Detection Pipeline (v4.3.1 ULEPSZENIE #1)

Completely non-blocking detection pipeline with result queueing.
Decouples detection processing from main UI thread for maximum responsiveness.
"""

from queue import Queue, Empty, Full
from typing import Optional, Dict, Any
import time
from core.logger import log


class AsyncDetectionPipeline:
    """
    Asynchronous detection pipeline with result queue.

    Features:
    - Non-blocking frame submission
    - Result queue with automatic expiration
    - Configurable queue size and timeout
    - Graceful degradation on overload
    """

    def __init__(self, detection_worker, max_queue_size: int = 10, result_timeout: float = 5.0):
        """
        Initialize async detection pipeline.

        Args:
            detection_worker: DetectionWorker instance for processing
            max_queue_size: Maximum number of pending results
            result_timeout: Maximum age of cached results (seconds)
        """
        self.detection_worker = detection_worker
        self.result_queue = Queue(maxsize=max_queue_size)
        self.result_timeout = result_timeout

        # Pending futures tracking
        self._pending_detection_future = None
        self._pending_classification_future = None

        # Default results (fallback when no data available)
        self._default_detection = {
            'events': {'walk': False, 'run': False, 'shot': False},
            'bands': {}
        }
        self._default_classification = {
            'type': 'unknown',
            'confidence': 0,
            'details': {}
        }

        # Last valid results with timestamp
        self._last_detection_result = {
            'data': self._default_detection.copy(),
            'timestamp': time.time()
        }
        self._last_classification_result = {
            'data': self._default_classification.copy(),
            'timestamp': time.time()
        }

        # Statistics
        self.stats = {
            'frames_submitted': 0,
            'frames_processed': 0,
            'frames_dropped': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'avg_processing_time': 0.0
        }

        log("AsyncDetectionPipeline initialized", "INFO")

    def submit_detection(self, det_panel, block, sample_rate, fft_result) -> Optional[Dict[str, Any]]:
        """
        Submit detection task and retrieve latest result (non-blocking).

        Args:
            det_panel: Detection panel for processing
            block: Audio block
            sample_rate: Sample rate
            fft_result: FFT computation result

        Returns:
            Latest detection result or None if unavailable
        """
        self.stats['frames_submitted'] += 1

        # Check if previous detection is ready (NON-BLOCKING)
        if self._pending_detection_future is not None:
            if self._pending_detection_future.done():
                try:
                    # Get result immediately (no timeout - it's done!)
                    detection_result = self._pending_detection_future.result(timeout=0)

                    if detection_result.success:
                        # Cache successful result
                        self._last_detection_result = {
                            'data': {
                                'events': detection_result.data['events'],
                                'bands': detection_result.data['bands']
                            },
                            'timestamp': time.time()
                        }
                        self.stats['frames_processed'] += 1
                    else:
                        log(f"Detection worker returned error: {detection_result.error}", "WARNING")
                        self.stats['frames_dropped'] += 1

                except (RuntimeError, ValueError, TimeoutError) as e:
                    log(f"Error getting detection result: {e}", "ERROR")
                    self.stats['frames_dropped'] += 1

                finally:
                    # Clear pending future
                    self._pending_detection_future = None

        # Submit new detection task (non-blocking)
        future = self.detection_worker.submit_detection(
            det_panel, block, sample_rate, fft_result
        )

        if future:
            self._pending_detection_future = future
        else:
            log("DetectionWorker rejected task (backpressure)", "DEBUG")
            self.stats['frames_dropped'] += 1

        # Return latest cached result (non-blocking!)
        return self._get_detection_result()

    def submit_classification(self, sound_classifier, block, sample_rate, fft_result) -> Optional[Dict[str, Any]]:
        """
        Submit classification task and retrieve latest result (non-blocking).

        Args:
            sound_classifier: Sound classifier instance
            block: Audio block
            sample_rate: Sample rate
            fft_result: FFT computation result

        Returns:
            Latest classification result or None if unavailable
        """
        # Check if previous classification is ready (NON-BLOCKING)
        if self._pending_classification_future is not None:
            if self._pending_classification_future.done():
                try:
                    # Get result immediately (no timeout - it's done!)
                    classification_result = self._pending_classification_future.result(timeout=0)

                    if classification_result.success:
                        # Cache successful result
                        self._last_classification_result = {
                            'data': classification_result.data,
                            'timestamp': time.time()
                        }
                    else:
                        log(f"Classification worker returned error: {classification_result.error}", "WARNING")

                except (RuntimeError, ValueError, TimeoutError) as e:
                    log(f"Error getting classification result: {e}", "ERROR")

                finally:
                    # Clear pending future
                    self._pending_classification_future = None

        # Submit new classification task (non-blocking)
        future = self.detection_worker.submit_classification(
            sound_classifier, block, sample_rate, fft_result
        )

        if future:
            self._pending_classification_future = future
        else:
            log("DetectionWorker rejected classification task", "DEBUG")

        # Return latest cached result (non-blocking!)
        return self._get_classification_result()

    def _get_detection_result(self) -> Dict[str, Any]:
        """
        Get latest detection result with timeout check.

        Returns:
            Cached detection result or default if stale
        """
        cache_age = time.time() - self._last_detection_result['timestamp']

        if cache_age > self.result_timeout:
            # Cache too old - reset to defaults
            log(f"Detection cache stale ({cache_age:.1f}s) - using defaults", "DEBUG")
            self._last_detection_result = {
                'data': self._default_detection.copy(),
                'timestamp': time.time()
            }
            self.stats['cache_misses'] += 1
            return self._default_detection.copy()

        # Return cached result
        self.stats['cache_hits'] += 1
        return self._last_detection_result['data']

    def _get_classification_result(self) -> Dict[str, Any]:
        """
        Get latest classification result with timeout check.

        Returns:
            Cached classification result or default if stale
        """
        cache_age = time.time() - self._last_classification_result['timestamp']

        if cache_age > self.result_timeout:
            # Cache too old - reset to defaults
            log(f"Classification cache stale ({cache_age:.1f}s) - using defaults", "DEBUG")
            self._last_classification_result = {
                'data': self._default_classification.copy(),
                'timestamp': time.time()
            }
            return self._default_classification.copy()

        # Return cached result
        return self._last_classification_result['data']

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get pipeline statistics.

        Returns:
            Dictionary with pipeline stats
        """
        total_frames = self.stats['frames_submitted']
        if total_frames > 0:
            process_rate = (self.stats['frames_processed'] / total_frames) * 100
            drop_rate = (self.stats['frames_dropped'] / total_frames) * 100
        else:
            process_rate = 0.0
            drop_rate = 0.0

        return {
            **self.stats,
            'process_rate': process_rate,
            'drop_rate': drop_rate,
            'cache_hit_rate': (self.stats['cache_hits'] / max(1, self.stats['cache_hits'] + self.stats['cache_misses'])) * 100
        }

    def cleanup(self):
        """Cleanup pending futures and resources"""
        self._pending_detection_future = None
        self._pending_classification_future = None
        log("AsyncDetectionPipeline cleanup complete", "INFO")
