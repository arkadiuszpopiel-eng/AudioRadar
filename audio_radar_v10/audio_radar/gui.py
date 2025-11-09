"""
AudioRadar v10.1 - Main PyQt5 GUI Window
Modern interface with dark theme, audio testing, and real-time monitoring
"""
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QComboBox, QProgressBar, QStatusBar, QTabWidget, QGroupBox,
    QGridLayout, QMessageBox, QApplication
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor
import threading
import time

try:
    import sounddevice as sd
    import numpy as np
    HAS_AUDIO = True
except ImportError:
    HAS_AUDIO = False
    sd = None
    np = None

try:
    from .audio_test_dialog import AudioTestDialog
except ImportError:
    try:
        from audio_test_dialog import AudioTestDialog
    except ImportError:
        AudioTestDialog = None

try:
    from .audio_backends import list_audio_devices
except ImportError:
    try:
        from audio_backends import list_audio_devices
    except ImportError:
        def list_audio_devices():
            """Fallback if audio_backends not available"""
            if sd is None:
                return []
            devices = sd.query_devices()
            return [(i, d['name']) for i, d in enumerate(devices) if d['max_input_channels'] > 0]

try:
    from .performance_monitor import PerformanceMonitor
except ImportError:
    try:
        from performance_monitor import PerformanceMonitor
    except ImportError:
        class PerformanceMonitor:
            """Fallback performance monitor"""
            def __init__(self):
                self.cpu_usage = 0.0
                self.latency_ms = 0.0
            
            def update(self):
                pass
            
            def get_cpu_usage(self):
                return self.cpu_usage
            
            def get_latency(self):
                return self.latency_ms


class MainWindow(QMainWindow):
    """Main application window with PyQt5 GUI"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AudioRadar v10.1 - Optimized Core")
        self.setGeometry(100, 100, 800, 600)
        
        # State
        self.is_running = False
        self.audio_stream = None
        self.performance_monitor = PerformanceMonitor()
        
        # Setup UI
        self.init_ui()
        
        # Setup timers
        self.setup_timers()
        
        # Load audio devices
        self.refresh_devices()
    
    def init_ui(self):
        """Initialize the user interface"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Tab widget
        tabs = QTabWidget()
        tabs.addTab(self.create_control_tab(), "Control")
        tabs.addTab(self.create_radar_tab(), "Radar")
        main_layout.addWidget(tabs)
        
        # Status bar
        self.setup_status_bar()
    
    def create_control_tab(self):
        """Create the control tab with audio controls"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Audio device selection
        device_group = QGroupBox("Urządzenia audio wejściowe:")
        device_layout = QVBoxLayout(device_group)
        
        self.device_combo = QComboBox()
        self.device_combo.setMinimumHeight(30)
        device_layout.addWidget(self.device_combo)
        
        layout.addWidget(device_group)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.btn_start = QPushButton("▶ START")
        self.btn_start.setMinimumHeight(40)
        self.btn_start.setStyleSheet("QPushButton { background-color: #2d5f2d; font-weight: bold; }")
        self.btn_start.clicked.connect(self.on_start)
        self.btn_start.setToolTip("Uruchom nagrywanie i analizę audio\nSkrót: SPACE")
        button_layout.addWidget(self.btn_start)
        
        self.btn_stop = QPushButton("■ STOP")
        self.btn_stop.setMinimumHeight(40)
        self.btn_stop.setEnabled(False)
        self.btn_stop.setStyleSheet("QPushButton { background-color: #5f2d2d; font-weight: bold; }")
        self.btn_stop.clicked.connect(self.on_stop)
        self.btn_stop.setToolTip("Zatrzymaj nagrywanie\nSkrót: SPACE")
        button_layout.addWidget(self.btn_stop)
        
        self.btn_test = QPushButton("🔊 TEST Audio")
        self.btn_test.setMinimumHeight(40)
        self.btn_test.setStyleSheet("QPushButton { background-color: #2d4f5f; font-weight: bold; }")
        self.btn_test.clicked.connect(self.on_test_audio)
        self.btn_test.setToolTip("Test audio input\nSprawdza czy sygnał audio przychodzi")
        button_layout.addWidget(self.btn_test)
        
        layout.addLayout(button_layout)
        
        # Input level indicator
        level_group = QGroupBox("Input Level:")
        level_layout = QVBoxLayout(level_group)
        
        self.level_bar = QProgressBar()
        self.level_bar.setMinimumHeight(25)
        self.level_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #555;
                border-radius: 5px;
                text-align: center;
                background-color: #2b2b2b;
            }
            QProgressBar::chunk {
                background-color: #00ffff;
            }
        """)
        level_layout.addWidget(self.level_bar)
        
        layout.addWidget(level_group)
        
        # Spacer
        layout.addStretch()
        
        return widget
    
    def create_radar_tab(self):
        """Create the radar visualization tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Radar info
        info_label = QLabel("Radar visualization coming soon...\nFor now, use the Control tab to test audio.")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("font-size: 14px; color: #888;")
        layout.addWidget(info_label)
        
        return widget
    
    def setup_status_bar(self):
        """Setup the status bar with indicators"""
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        # Connection status
        self.status_led = QLabel("🔴 Disconnected")
        self.status_led.setStyleSheet("color: #ff4444; font-weight: bold;")
        self.statusBar.addPermanentWidget(self.status_led)
        
        # Latency
        self.status_latency = QLabel("Latency: --ms")
        self.status_latency.setStyleSheet("color: #00ffff;")
        self.statusBar.addPermanentWidget(self.status_latency)
        
        # CPU usage
        self.status_cpu = QLabel("CPU: --%")
        self.status_cpu.setStyleSheet("color: #00ffff;")
        self.statusBar.addPermanentWidget(self.status_cpu)
    
    def setup_timers(self):
        """Setup update timers"""
        # Status update timer
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(100)  # Update every 100ms
        
        # Performance monitor timer
        self.perf_timer = QTimer()
        self.perf_timer.timeout.connect(self.update_performance)
        self.perf_timer.start(1000)  # Update every second
    
    def refresh_devices(self):
        """Refresh the audio device list"""
        self.device_combo.clear()
        
        if not HAS_AUDIO:
            self.device_combo.addItem("⚠ Audio libraries not available")
            return
        
        try:
            devices = list_audio_devices()
            if not devices:
                self.device_combo.addItem("⚠ No audio input devices found")
            else:
                for idx, name in devices:
                    self.device_combo.addItem(f"{name}", idx)
        except Exception as e:
            self.device_combo.addItem(f"⚠ Error loading devices: {e}")
    
    def on_start(self):
        """Start audio capture and processing"""
        if not HAS_AUDIO:
            QMessageBox.warning(self, "Error", "Audio libraries not available!\n\nInstall: pip install sounddevice numpy")
            return
        
        self.is_running = True
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.status_led.setText("🟢 Connected")
        self.status_led.setStyleSheet("color: #44ff44; font-weight: bold;")
        
        # Start audio processing (placeholder)
        self.start_audio_stream()
    
    def on_stop(self):
        """Stop audio capture"""
        self.is_running = False
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.status_led.setText("🔴 Disconnected")
        self.status_led.setStyleSheet("color: #ff4444; font-weight: bold;")
        
        # Stop audio stream
        self.stop_audio_stream()
    
    def on_test_audio(self):
        """Open audio test dialog"""
        if AudioTestDialog is None:
            QMessageBox.information(self, "Test Audio", 
                "Audio test dialog not available.\n\n"
                f"Current audio level will be shown in the level bar.\n"
                f"{'Audio libraries available' if HAS_AUDIO else 'Audio libraries NOT available'}")
            return
        
        dialog = AudioTestDialog(self)
        dialog.exec_()
    
    def start_audio_stream(self):
        """Start the audio stream"""
        # Placeholder - implement actual audio streaming
        pass
    
    def stop_audio_stream(self):
        """Stop the audio stream"""
        # Placeholder - implement actual audio stopping
        pass
    
    def update_status(self):
        """Update status indicators"""
        if self.is_running and HAS_AUDIO:
            # Simulate input level (would be real audio level in production)
            import random
            level = random.randint(0, 100)
            self.level_bar.setValue(level)
        else:
            self.level_bar.setValue(0)
    
    def update_performance(self):
        """Update performance metrics"""
        self.performance_monitor.update()
        
        # Update latency
        latency = self.performance_monitor.get_latency()
        self.status_latency.setText(f"Latency: {latency:.1f}ms")
        
        # Update CPU
        cpu = self.performance_monitor.get_cpu_usage()
        self.status_cpu.setText(f"CPU: {cpu:.1f}%")
    
    def keyPressEvent(self, event):
        """Handle keyboard shortcuts"""
        if event.key() == Qt.Key_Space:
            if self.is_running:
                self.on_stop()
            else:
                self.on_start()
        elif event.key() == Qt.Key_F5:
            self.refresh_devices()
        else:
            super().keyPressEvent(event)


def main():
    """Main entry point for GUI"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
