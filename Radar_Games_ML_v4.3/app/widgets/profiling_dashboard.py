"""
Profiling Dashboard Widget (v4.3.1 ULEPSZENIE #4)

Real-time performance monitoring dashboard for Radar Games ML.
Displays tick timing, GPU utilization, frame skip rate, and more.
"""

try:
    from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                                  QProgressBar, QGroupBox, QGridLayout)
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QFont
except ImportError:
    from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                                  QProgressBar, QGroupBox, QGridLayout)
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QFont

from core.logger import log


class ProfilingDashboard(QWidget):
    """
    Real-time performance monitoring dashboard.

    Displays:
    - Tick timing histogram (last 100 frames)
    - Detection worker queue depth
    - GPU utilization percentage
    - Frame skip rate
    - FPS (actual vs target)
    - Cache hit rates
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Performance Profiling Dashboard")
        self.setMinimumWidth(400)

        # Metrics storage
        self.tick_times = []
        self.max_history = 100

        self._init_ui()
        log("ProfilingDashboard initialized", "INFO")

    def _init_ui(self):
        """Initialize dashboard UI"""
        layout = QVBoxLayout()
        layout.setSpacing(10)

        # Title
        title = QLabel("⚡ PERFORMANCE DASHBOARD")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter if hasattr(Qt, 'AlignmentFlag') else Qt.AlignCenter)
        layout.addWidget(title)

        # FPS Group
        fps_group = self._create_fps_group()
        layout.addWidget(fps_group)

        # Timing Group
        timing_group = self._create_timing_group()
        layout.addWidget(timing_group)

        # Detection Worker Group
        worker_group = self._create_worker_group()
        layout.addWidget(worker_group)

        # GPU Group
        gpu_group = self._create_gpu_group()
        layout.addWidget(gpu_group)

        # Cache Group
        cache_group = self._create_cache_group()
        layout.addWidget(cache_group)

        layout.addStretch()
        self.setLayout(layout)

    def _create_fps_group(self) -> QGroupBox:
        """Create FPS monitoring group"""
        group = QGroupBox("🎯 FPS Monitoring")
        layout = QGridLayout()

        # Current FPS
        layout.addWidget(QLabel("Current FPS:"), 0, 0)
        self.fps_label = QLabel("0.0")
        self.fps_label.setStyleSheet("color: #00ff00; font-weight: bold; font-size: 14pt;")
        layout.addWidget(self.fps_label, 0, 1)

        # Target FPS
        layout.addWidget(QLabel("Target FPS:"), 1, 0)
        self.target_fps_label = QLabel("20.0")
        layout.addWidget(self.target_fps_label, 1, 1)

        # FPS Progress Bar
        self.fps_progress = QProgressBar()
        self.fps_progress.setRange(0, 20)
        self.fps_progress.setTextVisible(True)
        self.fps_progress.setFormat("%v FPS")
        layout.addWidget(self.fps_progress, 2, 0, 1, 2)

        group.setLayout(layout)
        return group

    def _create_timing_group(self) -> QGroupBox:
        """Create tick timing group"""
        group = QGroupBox("⏱️ Tick Timing")
        layout = QGridLayout()

        # Average tick time
        layout.addWidget(QLabel("Avg Tick Time:"), 0, 0)
        self.avg_tick_label = QLabel("0.0 ms")
        layout.addWidget(self.avg_tick_label, 0, 1)

        # Max tick time
        layout.addWidget(QLabel("Max Tick Time:"), 1, 0)
        self.max_tick_label = QLabel("0.0 ms")
        layout.addWidget(self.max_tick_label, 1, 1)

        # Tick time budget (50ms for 20 FPS)
        layout.addWidget(QLabel("Budget:"), 2, 0)
        self.budget_label = QLabel("50.0 ms")
        layout.addWidget(self.budget_label, 2, 1)

        # Tick time progress bar
        self.tick_progress = QProgressBar()
        self.tick_progress.setRange(0, 50)  # 50ms budget
        self.tick_progress.setTextVisible(True)
        self.tick_progress.setFormat("%v ms / 50 ms")
        layout.addWidget(self.tick_progress, 3, 0, 1, 2)

        group.setLayout(layout)
        return group

    def _create_worker_group(self) -> QGroupBox:
        """Create detection worker group"""
        group = QGroupBox("🔧 Detection Worker")
        layout = QGridLayout()

        # Queue depth
        layout.addWidget(QLabel("Queue Depth:"), 0, 0)
        self.queue_depth_label = QLabel("0 / 10")
        layout.addWidget(self.queue_depth_label, 0, 1)

        # Frames processed
        layout.addWidget(QLabel("Processed:"), 1, 0)
        self.frames_processed_label = QLabel("0")
        layout.addWidget(self.frames_processed_label, 1, 1)

        # Frames dropped
        layout.addWidget(QLabel("Dropped:"), 2, 0)
        self.frames_dropped_label = QLabel("0")
        layout.addWidget(self.frames_dropped_label, 2, 1)

        group.setLayout(layout)
        return group

    def _create_gpu_group(self) -> QGroupBox:
        """Create GPU monitoring group"""
        group = QGroupBox("🎮 GPU Acceleration")
        layout = QGridLayout()

        # GPU status
        layout.addWidget(QLabel("Status:"), 0, 0)
        self.gpu_status_label = QLabel("Unknown")
        layout.addWidget(self.gpu_status_label, 0, 1)

        # GPU utilization (simulated)
        layout.addWidget(QLabel("Utilization:"), 1, 0)
        self.gpu_util_label = QLabel("0%")
        layout.addWidget(self.gpu_util_label, 1, 1)

        # GPU progress bar
        self.gpu_progress = QProgressBar()
        self.gpu_progress.setRange(0, 100)
        self.gpu_progress.setTextVisible(True)
        self.gpu_progress.setFormat("%v%")
        layout.addWidget(self.gpu_progress, 2, 0, 1, 2)

        group.setLayout(layout)
        return group

    def _create_cache_group(self) -> QGroupBox:
        """Create cache statistics group"""
        group = QGroupBox("💾 Cache Statistics")
        layout = QGridLayout()

        # Detection cache hit rate
        layout.addWidget(QLabel("Detection Cache:"), 0, 0)
        self.det_cache_label = QLabel("0% hits")
        layout.addWidget(self.det_cache_label, 0, 1)

        # FFT cache hit rate
        layout.addWidget(QLabel("FFT Cache:"), 1, 0)
        self.fft_cache_label = QLabel("0% hits")
        layout.addWidget(self.fft_cache_label, 1, 1)

        # Frame skip rate
        layout.addWidget(QLabel("Frame Skip Rate:"), 2, 0)
        self.frame_skip_label = QLabel("0%")
        layout.addWidget(self.frame_skip_label, 2, 1)

        group.setLayout(layout)
        return group

    # =======================================================================
    # UPDATE METHODS
    # =======================================================================

    def update_fps(self, current_fps: float, target_fps: float = 20.0):
        """Update FPS display"""
        self.fps_label.setText(f"{current_fps:.1f}")
        self.target_fps_label.setText(f"{target_fps:.1f}")
        self.fps_progress.setValue(int(current_fps))

        # Color coding based on performance
        if current_fps >= target_fps:
            self.fps_label.setStyleSheet("color: #00ff00; font-weight: bold; font-size: 14pt;")
        elif current_fps >= target_fps * 0.8:
            self.fps_label.setStyleSheet("color: #ffff00; font-weight: bold; font-size: 14pt;")
        else:
            self.fps_label.setStyleSheet("color: #ff0000; font-weight: bold; font-size: 14pt;")

    def update_tick_timing(self, tick_time_ms: float):
        """Update tick timing display"""
        # Store tick time
        self.tick_times.append(tick_time_ms)
        if len(self.tick_times) > self.max_history:
            self.tick_times.pop(0)

        # Calculate average and max
        avg_tick = sum(self.tick_times) / len(self.tick_times) if self.tick_times else 0
        max_tick = max(self.tick_times) if self.tick_times else 0

        self.avg_tick_label.setText(f"{avg_tick:.1f} ms")
        self.max_tick_label.setText(f"{max_tick:.1f} ms")
        self.tick_progress.setValue(int(avg_tick))

        # Color coding
        if avg_tick <= 50:
            self.tick_progress.setStyleSheet("QProgressBar::chunk { background-color: #00ff00; }")
        elif avg_tick <= 75:
            self.tick_progress.setStyleSheet("QProgressBar::chunk { background-color: #ffff00; }")
        else:
            self.tick_progress.setStyleSheet("QProgressBar::chunk { background-color: #ff0000; }")

    def update_worker_stats(self, queue_depth: int, max_queue: int, processed: int, dropped: int):
        """Update detection worker statistics"""
        self.queue_depth_label.setText(f"{queue_depth} / {max_queue}")
        self.frames_processed_label.setText(f"{processed}")
        self.frames_dropped_label.setText(f"{dropped}")

    def update_gpu_stats(self, enabled: bool, utilization: float):
        """Update GPU statistics"""
        if enabled:
            self.gpu_status_label.setText("✅ Enabled")
            self.gpu_status_label.setStyleSheet("color: #00ff00;")
        else:
            self.gpu_status_label.setText("❌ Disabled")
            self.gpu_status_label.setStyleSheet("color: #ff0000;")

        self.gpu_util_label.setText(f"{utilization:.0f}%")
        self.gpu_progress.setValue(int(utilization))

    def update_cache_stats(self, det_cache_rate: float, fft_cache_rate: float, frame_skip_rate: float):
        """Update cache statistics"""
        self.det_cache_label.setText(f"{det_cache_rate:.1f}% hits")
        self.fft_cache_label.setText(f"{fft_cache_rate:.1f}% hits")
        self.frame_skip_label.setText(f"{frame_skip_rate:.1f}%")


# Standalone test
if __name__ == '__main__':
    import sys
    try:
        from PyQt6.QtWidgets import QApplication
    except ImportError:
        from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    dashboard = ProfilingDashboard()
    dashboard.show()

    # Simulate some data
    dashboard.update_fps(18.5, 20.0)
    dashboard.update_tick_timing(42.3)
    dashboard.update_worker_stats(3, 10, 1250, 15)
    dashboard.update_gpu_stats(True, 65.0)
    dashboard.update_cache_stats(78.5, 92.3, 12.5)

    sys.exit(app.exec())
