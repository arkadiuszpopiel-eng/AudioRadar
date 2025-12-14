"""
Adaptive Frame Skip Strategy (v4.3.1 ULEPSZENIE #3)

Intelligent frame skipping to maintain UI responsiveness under heavy load.
Dynamically adjusts processing rate based on system performance.
"""

import time
from collections import deque
from typing import Optional
from core.logger import log


class AdaptiveFrameSkip:
    """
    Adaptive frame skipping to maintain target FPS.

    Features:
    - Dynamic skip rate based on actual FPS
    - Configurable FPS targets and thresholds
    - Frame timing statistics
    - Graceful degradation under load
    """

    def __init__(self, target_fps: int = 20, min_fps: int = 10, history_size: int = 30):
        """
        Initialize adaptive frame skip.

        Args:
            target_fps: Target frames per second (default: 20)
            min_fps: Minimum acceptable FPS before aggressive skipping (default: 10)
            history_size: Number of frames to track for averaging (default: 30)
        """
        self.target_fps = target_fps
        self.min_fps = min_fps
        self.target_frame_time = 1.0 / target_fps  # 50ms for 20 FPS
        self.min_frame_time = 1.0 / min_fps        # 100ms for 10 FPS

        # Frame timing history
        self.frame_times = deque(maxlen=history_size)
        self.last_frame_time = time.time()

        # Skip statistics
        self.frames_processed = 0
        self.frames_skipped = 0
        self.total_frames = 0

        # Adaptive parameters
        self.skip_probability = 0.0  # 0.0 = no skip, 1.0 = skip all

        log(f"AdaptiveFrameSkip initialized: target={target_fps} FPS, min={min_fps} FPS", "INFO")

    def should_process_frame(self) -> bool:
        """
        Determine if current frame should be processed or skipped.

        Returns:
            True if frame should be processed, False to skip
        """
        self.total_frames += 1

        # Record frame timing
        current_time = time.time()
        frame_time = current_time - self.last_frame_time
        self.last_frame_time = current_time
        self.frame_times.append(frame_time)

        # Update skip probability based on performance
        self._update_skip_probability()

        # Decide: skip or process?
        if self.skip_probability > 0:
            import random
            if random.random() < self.skip_probability:
                self.frames_skipped += 1
                return False

        self.frames_processed += 1
        return True

    def _update_skip_probability(self):
        """
        Update skip probability based on recent frame times.

        Strategy:
        - If average frame time < target: skip_probability = 0 (no skip)
        - If average frame time > target: increase skip_probability
        - If average frame time > min_threshold: aggressive skipping
        """
        if len(self.frame_times) < 5:
            # Not enough data yet
            self.skip_probability = 0.0
            return

        # Calculate average frame time
        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        actual_fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0

        if actual_fps >= self.target_fps:
            # Performance good - no skipping
            self.skip_probability = max(0.0, self.skip_probability - 0.05)

        elif actual_fps >= self.min_fps:
            # Performance degraded - moderate skipping
            # Linear interpolation: min_fps → 0% skip, target_fps → 50% skip
            fps_ratio = (actual_fps - self.min_fps) / (self.target_fps - self.min_fps)
            target_skip = 0.5 * (1.0 - fps_ratio)
            self.skip_probability = min(0.5, target_skip)

        else:
            # Performance critical - aggressive skipping
            # Below min_fps: skip 50-80% of frames
            fps_ratio = actual_fps / self.min_fps  # 0.0 to 1.0
            target_skip = 0.8 - (0.3 * fps_ratio)  # 0.8 at 0 FPS, 0.5 at min_fps
            self.skip_probability = min(0.8, max(0.5, target_skip))

        # Clamp to valid range
        self.skip_probability = max(0.0, min(1.0, self.skip_probability))

    def get_current_fps(self) -> float:
        """
        Get current FPS based on frame timing history.

        Returns:
            Current FPS estimate
        """
        if len(self.frame_times) < 2:
            return 0.0

        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        return 1.0 / avg_frame_time if avg_frame_time > 0 else 0.0

    def get_statistics(self) -> dict:
        """
        Get frame skip statistics.

        Returns:
            Dictionary with statistics
        """
        skip_rate = (self.frames_skipped / self.total_frames * 100) if self.total_frames > 0 else 0
        process_rate = (self.frames_processed / self.total_frames * 100) if self.total_frames > 0 else 0

        return {
            'total_frames': self.total_frames,
            'frames_processed': self.frames_processed,
            'frames_skipped': self.frames_skipped,
            'skip_rate': skip_rate,
            'process_rate': process_rate,
            'current_fps': self.get_current_fps(),
            'target_fps': self.target_fps,
            'skip_probability': self.skip_probability * 100,  # Convert to percentage
        }

    def get_performance_status(self) -> str:
        """
        Get human-readable performance status.

        Returns:
            Status string: "EXCELLENT", "GOOD", "DEGRADED", or "CRITICAL"
        """
        fps = self.get_current_fps()

        if fps >= self.target_fps:
            return "EXCELLENT"
        elif fps >= self.target_fps * 0.9:
            return "GOOD"
        elif fps >= self.min_fps:
            return "DEGRADED"
        else:
            return "CRITICAL"

    def reset(self):
        """Reset all statistics and timing data"""
        self.frame_times.clear()
        self.frames_processed = 0
        self.frames_skipped = 0
        self.total_frames = 0
        self.skip_probability = 0.0
        self.last_frame_time = time.time()
        log("AdaptiveFrameSkip reset", "DEBUG")


# Example usage
if __name__ == '__main__':
    # Simulate frame processing with varying load
    frame_skip = AdaptiveFrameSkip(target_fps=20, min_fps=10)

    print("Simulating adaptive frame skip...")
    print("=" * 60)

    for i in range(100):
        if frame_skip.should_process_frame():
            # Simulate processing time (varies with load)
            if i < 30:
                time.sleep(0.03)  # Light load - 30ms
            elif i < 60:
                time.sleep(0.07)  # Heavy load - 70ms
            else:
                time.sleep(0.04)  # Medium load - 40ms

        # Print stats every 20 frames
        if (i + 1) % 20 == 0:
            stats = frame_skip.get_statistics()
            status = frame_skip.get_performance_status()
            print(f"\nFrame {i+1}:")
            print(f"  Status: {status}")
            print(f"  Current FPS: {stats['current_fps']:.1f}")
            print(f"  Skip Rate: {stats['skip_rate']:.1f}%")
            print(f"  Skip Probability: {stats['skip_probability']:.1f}%")

    print("\n" + "=" * 60)
    print("Final Statistics:")
    final_stats = frame_skip.get_statistics()
    for key, value in final_stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")
