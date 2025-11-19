"""
RadarSuite v3.5.0 - Performance Monitor
Real-time FPS, CPU, memory, latency tracking
"""

import time
import psutil

from core.logger import log


class PerformanceMonitor:
    """
    Monitor application performance metrics
    Tracks FPS, CPU usage, memory usage, latency
    """

    def __init__(self):
        log("PerformanceMonitor.__init__", "INFO")
        self.frame_times = deque(maxlen=60)  # Last 60 frames
        self.last_frame_time = time.time()
        self.process = psutil.Process()

        # Metrics
        self.fps = 0.0
        self.cpu_percent = 0.0
        self.memory_mb = 0.0
        self.latency_ms = 0.0

        # Latency tracking
        self.audio_in_time = 0.0
        self.radar_update_time = 0.0

    def start_frame(self):
        """Mark start of processing frame"""
        self.audio_in_time = time.time()

    def end_frame(self):
        """Mark end of processing frame"""
        current_time = time.time()
        frame_time = current_time - self.last_frame_time
        self.frame_times.append(frame_time)
        self.last_frame_time = current_time

        # Calculate latency (audio in → radar update)
        if self.audio_in_time > 0:
            self.latency_ms = (current_time - self.audio_in_time) * 1000.0

    def update(self):
        """Update performance metrics"""
        # Calculate FPS
        if len(self.frame_times) > 0:
            avg_frame_time = np.mean(self.frame_times)
            self.fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0.0

        # CPU and memory (sample every 10 frames to reduce overhead)
        if len(self.frame_times) % 10 == 0:
            try:
                self.cpu_percent = self.process.cpu_percent()
                self.memory_mb = self.process.memory_info().rss / (1024 * 1024)
            except (psutil.Error, AttributeError) as e:
                log(f"Performance monitoring error: {e}", level="WARNING")
                self.cpu_percent = 0.0
                self.memory_mb = 0.0

    def get_stats(self):
        """Get current performance statistics"""
        return {
            'fps': self.fps,
            'cpu_percent': self.cpu_percent,
            'memory_mb': self.memory_mb,
            'latency_ms': self.latency_ms
        }

