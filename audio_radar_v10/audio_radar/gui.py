"""PyQt5 GUI for AudioRadar v10.2.

Main window with device selection, Start/Stop/Test controls,
Gain and Threshold sliders, VU meter, and status display.
"""

from __future__ import annotations
from typing import Optional
import sys

try:
    from PyQt5.QtWidgets import (
        QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
        QPushButton, QComboBox, QSlider, QProgressBar, QTextEdit,
        QGroupBox, QApplication
    )
    from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
    from PyQt5.QtGui import QPalette, QColor
except ImportError:
    # Fallback for when PyQt5 is not installed
    QMainWindow = object
    QWidget = object
    QObject = object

import numpy as np
from audio_backend import AudioWorker, list_wasapi_loopback_devices
from sound_analysis import detect_event


class MainWindow(QMainWindow):
    """Main application window for AudioRadar v10.2.
    
    Provides GUI controls for:
    - Device selection (WASAPI loopback outputs)
    - Start/Stop/Test buttons
    - Gain and Threshold sliders
    - VU meter (peak level display)
    - Status log
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AudioRadar v10.2 COMPLETE")
        self.setMinimumSize(600, 500)
        
        # Audio worker
        self.audio_worker: Optional[AudioWorker] = None
        self.current_device_index: Optional[int] = None
        self.gain = 1.0
        self.threshold = 0.3
        self.peak_level = 0.0
        
        # Setup UI
        self._setup_ui()
        
        # Timer for UI updates
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_vu_meter)
        self.update_timer.start(50)  # Update every 50ms
        
        self._log_status("AudioRadar v10.2 COMPLETE initialized")
        self._log_status("Select a WASAPI loopback device and click Start")
    
    def _setup_ui(self):
        """Setup the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Device selection group
        device_group = QGroupBox("Audio Device (WASAPI Loopback)")
        device_layout = QVBoxLayout()
        
        self.device_combo = QComboBox()
        self._populate_devices()
        device_layout.addWidget(self.device_combo)
        
        device_group.setLayout(device_layout)
        main_layout.addWidget(device_group)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self._on_start)
        button_layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self._on_stop)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)
        
        self.test_button = QPushButton("Test")
        self.test_button.clicked.connect(self._on_test)
        button_layout.addWidget(self.test_button)
        
        main_layout.addLayout(button_layout)
        
        # Gain slider
        gain_group = QGroupBox("Gain Control")
        gain_layout = QVBoxLayout()
        
        gain_label_layout = QHBoxLayout()
        gain_label_layout.addWidget(QLabel("Gain:"))
        self.gain_value_label = QLabel("1.0x")
        gain_label_layout.addWidget(self.gain_value_label)
        gain_label_layout.addStretch()
        gain_layout.addLayout(gain_label_layout)
        
        self.gain_slider = QSlider(Qt.Horizontal)
        self.gain_slider.setMinimum(1)
        self.gain_slider.setMaximum(50)
        self.gain_slider.setValue(10)  # 1.0x
        self.gain_slider.setTickPosition(QSlider.TicksBelow)
        self.gain_slider.setTickInterval(5)
        self.gain_slider.valueChanged.connect(self._on_gain_changed)
        gain_layout.addWidget(self.gain_slider)
        
        gain_group.setLayout(gain_layout)
        main_layout.addWidget(gain_group)
        
        # Threshold slider
        threshold_group = QGroupBox("Detection Threshold")
        threshold_layout = QVBoxLayout()
        
        threshold_label_layout = QHBoxLayout()
        threshold_label_layout.addWidget(QLabel("Threshold:"))
        self.threshold_value_label = QLabel("0.30")
        threshold_label_layout.addWidget(self.threshold_value_label)
        threshold_label_layout.addStretch()
        threshold_layout.addLayout(threshold_label_layout)
        
        self.threshold_slider = QSlider(Qt.Horizontal)
        self.threshold_slider.setMinimum(1)
        self.threshold_slider.setMaximum(100)
        self.threshold_slider.setValue(30)
        self.threshold_slider.setTickPosition(QSlider.TicksBelow)
        self.threshold_slider.setTickInterval(10)
        self.threshold_slider.valueChanged.connect(self._on_threshold_changed)
        threshold_layout.addWidget(self.threshold_slider)
        
        threshold_group.setLayout(threshold_layout)
        main_layout.addWidget(threshold_group)
        
        # VU Meter
        vu_group = QGroupBox("VU Meter (Peak Level)")
        vu_layout = QVBoxLayout()
        
        self.vu_meter = QProgressBar()
        self.vu_meter.setMinimum(0)
        self.vu_meter.setMaximum(100)
        self.vu_meter.setValue(0)
        self.vu_meter.setTextVisible(True)
        self.vu_meter.setFormat("%v%")
        vu_layout.addWidget(self.vu_meter)
        
        vu_group.setLayout(vu_layout)
        main_layout.addWidget(vu_group)
        
        # Status log
        status_group = QGroupBox("Status Log")
        status_layout = QVBoxLayout()
        
        self.status_log = QTextEdit()
        self.status_log.setReadOnly(True)
        self.status_log.setMaximumHeight(150)
        status_layout.addWidget(self.status_log)
        
        status_group.setLayout(status_layout)
        main_layout.addWidget(status_group)
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def _populate_devices(self):
        """Populate device combo box with WASAPI loopback devices."""
        devices = list_wasapi_loopback_devices()
        self.device_combo.clear()
        
        if not devices:
            self.device_combo.addItem("No devices found", None)
            self._log_status("Warning: No WASAPI output devices found")
        else:
            for idx, name in devices:
                self.device_combo.addItem(name, idx)
            self._log_status(f"Found {len(devices)} WASAPI output device(s)")
    
    def _on_start(self):
        """Handle Start button click."""
        device_index = self.device_combo.currentData()
        if device_index is None:
            self._log_status("Error: No device selected")
            return
        
        self.current_device_index = device_index
        device_name = self.device_combo.currentText()
        
        try:
            # Create and start audio worker
            self.audio_worker = AudioWorker(
                device_index=device_index,
                samplerate=44100,
                blocksize=1024,
                gain=self.gain
            )
            self.audio_worker.on_audio_data = self._on_audio_data
            self.audio_worker.start()
            
            self._log_status(f"Started capture on: {device_name}")
            self.statusBar().showMessage("Capturing audio...")
            
            # Update button states
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.device_combo.setEnabled(False)
            
        except Exception as e:
            self._log_status(f"Error starting capture: {e}")
            self.statusBar().showMessage("Error starting capture")
    
    def _on_stop(self):
        """Handle Stop button click."""
        if self.audio_worker is not None:
            self.audio_worker.stop()
            self.audio_worker = None
            self._log_status("Stopped audio capture")
            self.statusBar().showMessage("Stopped")
        
        # Reset UI state
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.device_combo.setEnabled(True)
        self.peak_level = 0.0
    
    def _on_test(self):
        """Handle Test button click."""
        self._log_status("Test: Simulating shot detection")
        # Simulate a shot event for testing
        test_samples = np.random.randn(1024) * 0.5
        event = detect_event(test_samples, self.threshold)
        if event:
            self._log_status(f"Test detected: {event}")
        else:
            self._log_status("Test: No event detected (increase gain or lower threshold)")
    
    def _on_gain_changed(self, value: int):
        """Handle gain slider change."""
        # Map slider value (1-50) to gain (0.1x - 5.0x)
        self.gain = value / 10.0
        self.gain_value_label.setText(f"{self.gain:.1f}x")
        
        if self.audio_worker is not None:
            self.audio_worker.set_gain(self.gain)
    
    def _on_threshold_changed(self, value: int):
        """Handle threshold slider change."""
        # Map slider value (1-100) to threshold (0.01 - 1.0)
        self.threshold = value / 100.0
        self.threshold_value_label.setText(f"{self.threshold:.2f}")
    
    def _on_audio_data(self, audio_chunk: np.ndarray, peak: float, rms: float):
        """Callback for audio data from worker.
        
        Parameters
        ----------
        audio_chunk : np.ndarray
            Audio samples
        peak : float
            Peak level (0.0 - 1.0+)
        rms : float
            RMS level
        """
        # Update peak level for VU meter
        self.peak_level = peak
        
        # Detect events
        event = detect_event(audio_chunk, self.threshold)
        if event:
            self._log_status(f"Detected: {event.upper()} (peak={peak:.3f})")
    
    def _update_vu_meter(self):
        """Update VU meter display."""
        # Convert peak level to percentage (0-100)
        # Clamp to reasonable range for display
        display_value = min(int(self.peak_level * 100), 100)
        self.vu_meter.setValue(display_value)
        
        # Color coding based on level
        if display_value > 80:
            color = "red"
        elif display_value > 50:
            color = "orange"
        else:
            color = "#0e639c"
        
        self.vu_meter.setStyleSheet(f"""
            QProgressBar::chunk {{
                background-color: {color};
            }}
        """)
        
        # Decay peak level over time
        self.peak_level *= 0.9
    
    def _log_status(self, message: str):
        """Add message to status log."""
        self.status_log.append(message)
        # Auto-scroll to bottom
        cursor = self.status_log.textCursor()
        cursor.movePosition(cursor.End)
        self.status_log.setTextCursor(cursor)
    
    def closeEvent(self, event):
        """Handle window close event."""
        if self.audio_worker is not None:
            self.audio_worker.stop()
        event.accept()
