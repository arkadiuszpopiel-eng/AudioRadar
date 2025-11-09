"""
AudioRadar v10.0 - PyQt5 GUI
Modern dark-themed interface for audio radar
"""
import sys
import threading
import logging
from pathlib import Path
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QStatusBar, QListWidget, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont

try:
    import sounddevice as sd
except ImportError:
    sd = None

try:
    import numpy as np
except ImportError:
    np = None

from audio_capture import list_audio_input_devices, AudioStream
from sound_analysis import detect_event
from performance_monitor import PerformanceMonitor


class MainWindow(QMainWindow):
    """Main GUI window for AudioRadar v10.0"""
    
    # Signals for thread-safe GUI updates
    update_status_signal = pyqtSignal(str, str)  # (status, color)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AudioRadar v10.0 - Optimized Core")
        self.setMinimumSize(800, 600)
        
        # State
        self.audio_stream = None
        self.is_running = False
        self.selected_device = None
        self.perf_monitor = PerformanceMonitor()
        
        # Setup logging
        self.log_file = Path(__file__).parent / "log_v10.txt"
        logging.basicConfig(
            filename=str(self.log_file),
            filemode="a",
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
        )
        logging.info("AudioRadar v10.0 GUI started")
        
        # Build UI
        self.init_ui()
        
        # Connect signals
        self.update_status_signal.connect(self._update_status_bar)
        
        # Start performance monitoring timer
        self.perf_timer = QTimer()
        self.perf_timer.timeout.connect(self.update_performance)
        self.perf_timer.start(1000)  # Update every second
        
        # Initial device list refresh
        self.refresh_devices()
        
    def init_ui(self):
        """Initialize the user interface"""
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        # Main layout
        layout = QVBoxLayout(central)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("AudioRadar v10.0")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #00ffff;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Optimized Core + Modern GUI")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        # Device list
        device_label = QLabel("Urządzenia audio wejściowe:")
        device_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        layout.addWidget(device_label)
        
        self.device_list = QListWidget()
        self.device_list.setMinimumHeight(200)
        self.device_list.itemClicked.connect(self.on_device_selected)
        self.device_list.setToolTip("Wybierz urządzenie audio do monitorowania")
        layout.addWidget(self.device_list)
        
        # Control buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.start_btn = QPushButton("▶ START")
        self.start_btn.setMinimumHeight(50)
        self.start_btn.setToolTip("Uruchom monitorowanie (SPACE)")
        self.start_btn.clicked.connect(self.start_monitoring)
        button_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("■ STOP")
        self.stop_btn.setMinimumHeight(50)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setToolTip("Zatrzymaj monitorowanie (SPACE)")
        self.stop_btn.clicked.connect(self.stop_monitoring)
        button_layout.addWidget(self.stop_btn)
        
        self.refresh_btn = QPushButton("🔄 Lista urządzeń")
        self.refresh_btn.setMinimumHeight(50)
        self.refresh_btn.setToolTip("Odśwież listę urządzeń (F5)")
        self.refresh_btn.clicked.connect(self.refresh_devices)
        button_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(button_layout)
        
        # Status info
        info_label = QLabel("💡 SKRÓTY: SPACE = START/STOP | F5 = Odśwież urządzenia")
        info_label.setStyleSheet("color: #00ffff; font-style: italic;")
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)
        
        layout.addStretch()
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        self.status_label = QLabel("🔴 Disconnected")
        self.status_label.setStyleSheet("color: #ff4444; font-weight: bold;")
        self.status_bar.addWidget(self.status_label)
        
        self.latency_label = QLabel("Latencja: -- ms")
        self.status_bar.addPermanentWidget(self.latency_label)
        
        self.cpu_label = QLabel("CPU: --%")
        self.status_bar.addPermanentWidget(self.cpu_label)
        
    def keyPressEvent(self, event):
        """Handle keyboard shortcuts"""
        if event.key() == Qt.Key_Space:
            if self.is_running:
                self.stop_monitoring()
            else:
                self.start_monitoring()
        elif event.key() == Qt.Key_F5:
            self.refresh_devices()
        else:
            super().keyPressEvent(event)
    
    def refresh_devices(self):
        """Refresh the list of audio input devices"""
        self.device_list.clear()
        
        if sd is None:
            self.device_list.addItem("❌ sounddevice nie jest zainstalowane!")
            logging.error("sounddevice not installed")
            return
        
        try:
            devices = list_audio_input_devices()
            if not devices:
                self.device_list.addItem("⚠ Nie znaleziono urządzeń wejściowych")
                logging.warning("No input devices found")
            else:
                for idx, name in devices:
                    self.device_list.addItem(f"[{idx}] {name}")
                logging.info(f"Found {len(devices)} input devices")
        except Exception as e:
            self.device_list.addItem(f"❌ Błąd: {str(e)}")
            logging.error(f"Error listing devices: {e}")
    
    def on_device_selected(self, item):
        """Handle device selection"""
        text = item.text()
        if text.startswith("[") and "]" in text:
            try:
                idx_str = text.split("]")[0][1:]
                self.selected_device = int(idx_str)
                logging.info(f"Selected device: {self.selected_device}")
            except (ValueError, IndexError):
                pass
    
    def start_monitoring(self):
        """Start audio monitoring"""
        if self.is_running:
            return
        
        if sd is None or np is None:
            QMessageBox.critical(
                self,
                "Błąd",
                "Brak wymaganych bibliotek!\n\nZainstaluj: pip install sounddevice numpy"
            )
            return
        
        try:
            # Create audio stream
            self.audio_stream = AudioStream(
                input_device=self.selected_device,
                samplerate=44100,
                blocksize=1024
            )
            
            # Setup callback
            def on_audio_data(samples):
                event = detect_event(samples)
                if event:
                    logging.info(f"Detected event: {event}")
            
            self.audio_stream.on_data = on_audio_data
            
            # Start in background thread
            def audio_thread():
                try:
                    self.audio_stream.start()
                except Exception as exc:
                    logging.error(f"Audio stream error: {exc}")
                    self.update_status_signal.emit("Error", "red")
            
            t = threading.Thread(target=audio_thread, daemon=True)
            t.start()
            
            self.is_running = True
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.update_status_signal.emit("🟢 Connected", "green")
            
            logging.info("Monitoring started")
            
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie można uruchomić monitorowania:\n{str(e)}")
            logging.error(f"Failed to start monitoring: {e}")
    
    def stop_monitoring(self):
        """Stop audio monitoring"""
        if not self.is_running:
            return
        
        try:
            if self.audio_stream:
                self.audio_stream.stop()
                self.audio_stream = None
            
            self.is_running = False
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.update_status_signal.emit("🔴 Disconnected", "red")
            
            logging.info("Monitoring stopped")
            
        except Exception as e:
            logging.error(f"Error stopping monitoring: {e}")
    
    def update_performance(self):
        """Update performance metrics in status bar"""
        try:
            cpu = self.perf_monitor.get_cpu_usage()
            self.cpu_label.setText(f"CPU: {cpu:.1f}%")
            
            latency = self.perf_monitor.get_latency()
            self.latency_label.setText(f"Latencja: {latency:.1f} ms")
        except Exception as e:
            logging.error(f"Error updating performance: {e}")
    
    def _update_status_bar(self, status: str, color: str):
        """Update status bar (called from signal)"""
        color_map = {
            "green": "#44ff44",
            "red": "#ff4444",
            "yellow": "#ffff44"
        }
        self.status_label.setText(status)
        self.status_label.setStyleSheet(f"color: {color_map.get(color, '#ff4444')}; font-weight: bold;")
    
    def closeEvent(self, event):
        """Handle window close"""
        if self.is_running:
            self.stop_monitoring()
        logging.info("AudioRadar GUI closed")
        event.accept()
