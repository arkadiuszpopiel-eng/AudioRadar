"""
AudioRadar v10.0 - Performance Monitor
Tracks CPU usage and audio latency
"""
import psutil
import time


class PerformanceMonitor:
    """Monitor system performance metrics"""
    
    def __init__(self):
        self.last_check = time.time()
        self.latency_ms = 0
        
    def get_cpu_usage(self) -> float:
        """Get current CPU usage percentage"""
        try:
            return psutil.cpu_percent(interval=0.1)
        except Exception:
            return 0.0
    
    def get_latency(self) -> float:
        """Get current audio latency in milliseconds"""
        return self.latency_ms
    
    def update_latency(self, latency_ms: float):
        """Update latency measurement"""
        self.latency_ms = latency_ms
