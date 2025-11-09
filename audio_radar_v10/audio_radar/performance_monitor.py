"""
AudioRadar v10.1 - Performance Monitor
Monitors CPU usage, memory, and audio latency
"""
import time
import threading

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
    psutil = None


class PerformanceMonitor:
    """Monitors system and application performance"""
    
    def __init__(self):
        """Initialize performance monitor"""
        self.cpu_usage = 0.0
        self.memory_usage = 0.0
        self.latency_ms = 0.0
        self.audio_buffer_size = 1024
        self.sample_rate = 44100
        
        # Last update time
        self.last_update = time.time()
        self.update_interval = 1.0  # Update every second
        
        # Audio timing
        self.last_audio_time = time.time()
        self.audio_callback_count = 0
        
        # Lock for thread safety
        self.lock = threading.Lock()
    
    def update(self):
        """Update performance metrics"""
        current_time = time.time()
        
        # Only update at specified interval
        if current_time - self.last_update < self.update_interval:
            return
        
        with self.lock:
            # Update CPU usage
            if HAS_PSUTIL:
                try:
                    self.cpu_usage = psutil.cpu_percent(interval=0.1)
                    
                    # Memory usage (MB)
                    process = psutil.Process()
                    self.memory_usage = process.memory_info().rss / 1024 / 1024
                except Exception:
                    pass
            else:
                # Simulate some values if psutil not available
                self.cpu_usage = 5.0
                self.memory_usage = 50.0
            
            # Calculate theoretical latency based on buffer size and sample rate
            # Latency = (buffer_size / sample_rate) * 1000 ms
            if self.sample_rate > 0:
                self.latency_ms = (self.audio_buffer_size / self.sample_rate) * 1000.0
            else:
                self.latency_ms = 0.0
            
            self.last_update = current_time
    
    def get_cpu_usage(self):
        """Get current CPU usage percentage
        
        Returns:
            float: CPU usage (0-100%)
        """
        with self.lock:
            return self.cpu_usage
    
    def get_memory_usage(self):
        """Get current memory usage in MB
        
        Returns:
            float: Memory usage in MB
        """
        with self.lock:
            return self.memory_usage
    
    def get_latency(self):
        """Get current audio latency in milliseconds
        
        Returns:
            float: Latency in ms
        """
        with self.lock:
            return self.latency_ms
    
    def set_audio_params(self, buffer_size, sample_rate):
        """Set audio parameters for latency calculation
        
        Args:
            buffer_size: Audio buffer size in samples
            sample_rate: Sample rate in Hz
        """
        with self.lock:
            self.audio_buffer_size = buffer_size
            self.sample_rate = sample_rate
            
            # Recalculate latency
            if self.sample_rate > 0:
                self.latency_ms = (self.audio_buffer_size / self.sample_rate) * 1000.0
    
    def on_audio_callback(self):
        """Called when audio callback is triggered"""
        with self.lock:
            self.audio_callback_count += 1
            current_time = time.time()
            
            # Calculate actual callback rate
            time_diff = current_time - self.last_audio_time
            if time_diff > 0.1:  # Update every 100ms
                # Actual latency can be measured by callback timing
                expected_callbacks = time_diff * (self.sample_rate / self.audio_buffer_size)
                if expected_callbacks > 0:
                    actual_latency = (self.audio_callback_count / expected_callbacks) * self.latency_ms
                    self.latency_ms = actual_latency
                
                self.audio_callback_count = 0
                self.last_audio_time = current_time
    
    def get_stats(self):
        """Get all performance statistics
        
        Returns:
            dict: Dictionary with all stats
        """
        with self.lock:
            return {
                'cpu_usage': self.cpu_usage,
                'memory_usage': self.memory_usage,
                'latency_ms': self.latency_ms,
                'buffer_size': self.audio_buffer_size,
                'sample_rate': self.sample_rate
            }
    
    def format_stats(self):
        """Format statistics as a readable string
        
        Returns:
            str: Formatted statistics
        """
        stats = self.get_stats()
        return (
            f"CPU: {stats['cpu_usage']:.1f}% | "
            f"Memory: {stats['memory_usage']:.1f} MB | "
            f"Latency: {stats['latency_ms']:.1f} ms | "
            f"Buffer: {stats['buffer_size']} @ {stats['sample_rate']} Hz"
        )


def main():
    """Test performance monitor"""
    print("=" * 70)
    print("  AudioRadar - Performance Monitor Test")
    print("=" * 70)
    print()
    
    monitor = PerformanceMonitor()
    
    # Set some audio parameters
    monitor.set_audio_params(buffer_size=1024, sample_rate=44100)
    
    print("Testing performance monitoring...")
    print()
    
    for i in range(5):
        monitor.update()
        print(f"[{i+1}] {monitor.format_stats()}")
        time.sleep(1)
    
    print()
    print("[OK] Performance monitor test complete")


if __name__ == "__main__":
    main()
