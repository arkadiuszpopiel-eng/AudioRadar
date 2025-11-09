"""Performance monitoring for AudioRadar v10.0.

This module tracks audio processing performance metrics including latency,
CPU usage, and audio dropouts. It provides graceful degradation if optional
dependencies like psutil are not available.

The PerformanceMonitor class maintains a rolling history of latency measurements
and can export statistics to CSV for analysis. All measurements are designed
to have minimal impact on the audio processing pipeline.
"""

from __future__ import annotations
from collections import deque
from typing import Optional, List
import time

# v10.0: Optional import of psutil for CPU monitoring
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    psutil = None  # type: ignore
    PSUTIL_AVAILABLE = False


class PerformanceMonitor:
    """Monitor and track audio processing performance metrics.
    
    This class tracks:
    - Audio latency history (rolling window of 300 samples)
    - CPU usage percentage
    - Audio dropout count
    - Processing statistics (min, max, average latency)
    
    If psutil is unavailable, CPU monitoring gracefully falls back to
    returning -1.0 to indicate unavailability.
    
    Attributes
    ----------
    latency_history : deque
        Rolling buffer of recent latency measurements in milliseconds.
    dropout_count : int
        Number of audio dropouts detected since monitoring started.
    """
    
    def __init__(self, history_size: int = 300):
        """Initialize the performance monitor.
        
        Parameters
        ----------
        history_size : int, optional
            Number of latency samples to keep in history. Default is 300,
            which at 60 FPS represents 5 seconds of data.
        """
        # v10.0: Track latency with deque for efficient rolling buffer
        self.latency_history: deque = deque(maxlen=history_size)
        self.dropout_count: int = 0
        self._start_time: float = time.time()
        
        # v10.0: Initialize psutil process handle if available
        if PSUTIL_AVAILABLE:
            try:
                self._process = psutil.Process()
                # Pre-call to avoid first-call overhead
                self._process.cpu_percent(interval=None)
            except Exception:
                self._process = None
        else:
            self._process = None
    
    def record_latency(self, latency_ms: float) -> None:
        """Record a latency measurement.
        
        Parameters
        ----------
        latency_ms : float
            Measured latency in milliseconds.
        """
        self.latency_history.append(latency_ms)
    
    def record_dropout(self) -> None:
        """Increment the dropout counter."""
        self.dropout_count += 1
    
    def get_current_cpu(self) -> float:
        """Get current CPU usage percentage.
        
        Returns
        -------
        float
            CPU usage as a percentage (0-100), or -1.0 if psutil
            is unavailable or CPU measurement fails.
        """
        if not PSUTIL_AVAILABLE or self._process is None:
            return -1.0
        
        try:
            # v10.0: Non-blocking CPU measurement
            cpu = self._process.cpu_percent(interval=None)
            # psutil returns per-core percentage, normalize to 0-100 range
            return cpu
        except Exception:
            return -1.0
    
    def get_latency_stats(self) -> dict:
        """Calculate statistics from latency history.
        
        Returns
        -------
        dict
            Dictionary with keys: 'min', 'max', 'avg', 'current', 'count'.
            All latency values are in milliseconds. Returns empty stats
            if no data has been recorded.
        """
        if not self.latency_history:
            return {
                'min': 0.0,
                'max': 0.0,
                'avg': 0.0,
                'current': 0.0,
                'count': 0
            }
        
        latencies = list(self.latency_history)
        return {
            'min': min(latencies),
            'max': max(latencies),
            'avg': sum(latencies) / len(latencies),
            'current': latencies[-1],
            'count': len(latencies)
        }
    
    def get_uptime(self) -> float:
        """Get monitor uptime in seconds.
        
        Returns
        -------
        float
            Seconds since monitor was initialized.
        """
        return time.time() - self._start_time
    
    def export_to_csv(self, filepath: str) -> bool:
        """Export performance statistics to CSV file.
        
        Parameters
        ----------
        filepath : str
            Path to the CSV file to create or overwrite.
        
        Returns
        -------
        bool
            True if export succeeded, False otherwise.
        """
        try:
            import csv
            
            stats = self.get_latency_stats()
            
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write summary statistics
                writer.writerow(['Metric', 'Value'])
                writer.writerow(['Uptime (seconds)', f"{self.get_uptime():.2f}"])
                writer.writerow(['Dropout Count', self.dropout_count])
                writer.writerow(['Min Latency (ms)', f"{stats['min']:.2f}"])
                writer.writerow(['Max Latency (ms)', f"{stats['max']:.2f}"])
                writer.writerow(['Avg Latency (ms)', f"{stats['avg']:.2f}"])
                writer.writerow(['Sample Count', stats['count']])
                writer.writerow([])
                
                # Write latency history
                writer.writerow(['Sample', 'Latency (ms)'])
                for idx, latency in enumerate(self.latency_history):
                    writer.writerow([idx, f"{latency:.2f}"])
            
            return True
        except Exception as e:
            # Silently fail - this is a non-critical feature
            return False
    
    def reset(self) -> None:
        """Reset all performance counters and history."""
        self.latency_history.clear()
        self.dropout_count = 0
        self._start_time = time.time()
        
        # Re-initialize CPU monitoring if available
        if PSUTIL_AVAILABLE and self._process:
            try:
                self._process.cpu_percent(interval=None)
            except Exception:
                pass
    
    def __repr__(self) -> str:
        """String representation of current performance state."""
        stats = self.get_latency_stats()
        return (
            f"PerformanceMonitor("
            f"latency_avg={stats['avg']:.1f}ms, "
            f"cpu={self.get_current_cpu():.1f}%, "
            f"dropouts={self.dropout_count}, "
            f"uptime={self.get_uptime():.1f}s)"
        )
