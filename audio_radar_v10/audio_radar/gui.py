"""PyQt5 GUI for AudioRadar v10.0.

This module provides the main window interface with optimized 60 FPS updates,
live performance monitoring, and keyboard shortcuts. The interface features
a dark theme with cyan accents and comprehensive device management.
"""

from __future__ import annotations
from typing import Optional
import logging

# v10.0: PyQt5 imports for modern GUI
try:
    from PyQt5.QtWidgets import (
        QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
        QPushButton, QComboBox, QSpinBox, QLabel, QGroupBox,
        QStatusBar, QShortcut
    )
    from PyQt5.QtCore import QTimer, Qt, QSize
    from PyQt5.QtGui import QKeySequence, QFont
    PYQT5_AVAILABLE = True
except ImportError:
    QMainWindow = object  # type: ignore
    PYQT5_AVAILABLE = False

# v10.0: Import performance monitor
try:
    from performance_monitor import PerformanceMonitor
    PERF_MONITOR_AVAILABLE = True
except ImportError:
    PerformanceMonitor = None  # type: ignore
    PERF_MONITOR_AVAILABLE = False

# Import audio backend
try:
    from audio_backends import PyAudioInput, list_audio_devices
    AUDIO_BACKEND_AVAILABLE = True
except ImportError:
    PyAudioInput = None  # type: ignore
    list_audio_devices = None  # type: ignore
    AUDIO_BACKEND_AVAILABLE = False


class MainWindow(QMainWindow):
    """Main application window for AudioRadar v10.0.
    
    This window provides the primary user interface with:
    - Device selection and configuration
    - Start/Stop controls with keyboard shortcuts
    - Live performance monitoring (latency, CPU)
    - Status indicators (connection LED)
    - 60 FPS update loop for smooth visualization
    
    Attributes
    ----------
    backend : PyAudioInput or None
        Active audio backend instance.
    perf_monitor : PerformanceMonitor or None
        Performance monitoring instance.
    current_buffer_size : int
        Currently configured buffer size.
    current_rate : int
        Currently configured sample rate.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize the main window.
        
        Parameters
        ----------
        logger : logging.Logger, optional
            Logger instance for diagnostics.
        """
        if not PYQT5_AVAILABLE:
            raise RuntimeError("PyQt5 is required but not available")
        
        super().__init__()
        
        self.logger = logger
        self.backend: Optional[PyAudioInput] = None
        
        # v10.0: Initialize performance monitor
        if PERF_MONITOR_AVAILABLE:
            self.perf_monitor = PerformanceMonitor()
        else:
            self.perf_monitor = None
        
        # v10.0: Track current audio settings
        self.current_buffer_size = 256
        self.current_rate = 48000
        
        self._setup_ui()
        self._setup_shortcuts()
        
        # v10.0: Timer for 60 FPS updates (16ms interval)
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_tick)
        self.timer.start(16)  # ~60 FPS
    
    def _setup_ui(self) -> None:
        """Setup the user interface components."""
        # v10.0: Set window title and size
        self.setWindowTitle('AudioRadar v10.0 - Optimized Core')
        self.resize(1200, 700)  # Increased from 1000x640
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # === Device Selection Group ===
        device_group = QGroupBox('Urządzenia Audio')
        device_layout = QGridLayout()
        device_group.setLayout(device_layout)
        
        # Input device selector
        device_layout.addWidget(QLabel('Urządzenie wejściowe:'), 0, 0)
        self.combo_device = QComboBox()
        self.combo_device.setMinimumWidth(300)
        self.combo_device.setToolTip(
            'Wybierz urządzenie wejściowe audio.\n'
            'Dla przechwytywania dźwięku z gry użyj loopback (Stereo Mix).'
        )
        device_layout.addWidget(self.combo_device, 0, 1, 1, 2)
        
        # Refresh button
        self.btn_refresh = QPushButton('🔄 Odśwież')
        self.btn_refresh.setToolTip('Odśwież listę dostępnych urządzeń (F5)')
        self.btn_refresh.clicked.connect(self.on_list)
        device_layout.addWidget(self.btn_refresh, 0, 3)
        
        # Sample rate
        device_layout.addWidget(QLabel('Częstotliwość próbkowania:'), 1, 0)
        self.spin_rate = QSpinBox()
        self.spin_rate.setRange(8000, 192000)
        self.spin_rate.setValue(48000)
        self.spin_rate.setSuffix(' Hz')
        self.spin_rate.setToolTip(
            'Częstotliwość próbkowania audio.\n'
            '48000 Hz jest zalecaną wartością dla większości gier.'
        )
        device_layout.addWidget(self.spin_rate, 1, 1)
        
        # Buffer size
        device_layout.addWidget(QLabel('Rozmiar bufora:'), 1, 2)
        self.spin_buffer = QSpinBox()
        self.spin_buffer.setRange(64, 2048)
        self.spin_buffer.setValue(128)  # v10.0: Default 128 frames
        self.spin_buffer.setSuffix(' ramek')
        self.spin_buffer.setToolTip(
            'Rozmiar bufora audio.\n'
            'Mniejsze wartości = mniejsze opóźnienie, ale większe użycie CPU.\n'
            'Zalecane: 128-256 ramek.'
        )
        device_layout.addWidget(self.spin_buffer, 1, 3)
        
        main_layout.addWidget(device_group)
        
        # === Control Buttons ===
        control_layout = QHBoxLayout()
        control_layout.setSpacing(10)
        
        # v10.0: Enhanced buttons with symbols
        self.btn_start = QPushButton('▶ START')
        self.btn_start.setMinimumHeight(50)
        font_btn = QFont()
        font_btn.setPointSize(11)
        font_btn.setBold(True)
        self.btn_start.setFont(font_btn)
        self.btn_start.setToolTip(
            'Rozpocznij przechwytywanie audio (Spacja).\n'
            'Upewnij się, że wybrano odpowiednie urządzenie.'
        )
        self.btn_start.clicked.connect(self.on_start)
        control_layout.addWidget(self.btn_start)
        
        self.btn_stop = QPushButton('■ STOP')
        self.btn_stop.setMinimumHeight(50)
        self.btn_stop.setFont(font_btn)
        self.btn_stop.setEnabled(False)
        self.btn_stop.setToolTip('Zatrzymaj przechwytywanie audio (Spacja)')
        self.btn_stop.clicked.connect(self.on_stop)
        control_layout.addWidget(self.btn_stop)
        
        main_layout.addLayout(control_layout)
        
        # === Visualization Area (placeholder) ===
        vis_group = QGroupBox('Wizualizacja')
        vis_layout = QVBoxLayout()
        vis_group.setLayout(vis_layout)
        
        self.lbl_visualization = QLabel('Wizualizacja będzie wyświetlana tutaj po uruchomieniu.')
        self.lbl_visualization.setAlignment(Qt.AlignCenter)
        self.lbl_visualization.setMinimumHeight(300)
        self.lbl_visualization.setStyleSheet('background-color: #151515; border: 1px solid #2d2d2d;')
        vis_layout.addWidget(self.lbl_visualization)
        
        main_layout.addWidget(vis_group)
        
        # === Status Bar with 3 indicators ===
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        # v10.0: Status LED indicator
        self.status_led = QLabel('🔴 Rozłączono')
        self.status_led.setStyleSheet('color: #888; font-weight: bold;')
        self.statusBar.addWidget(self.status_led)
        
        self.statusBar.addWidget(QLabel('|'))
        
        # v10.0: Latency indicator
        self.status_latency = QLabel('Opóźnienie: -- ms')
        self.statusBar.addWidget(self.status_latency)
        
        self.statusBar.addWidget(QLabel('|'))
        
        # v10.0: CPU usage indicator
        self.status_cpu = QLabel('CPU: --%')
        self.statusBar.addPermanentWidget(self.status_cpu)
        
        # Initial device list
        self.on_list()
    
    def _setup_shortcuts(self) -> None:
        """Setup keyboard shortcuts."""
        # v10.0: Space key to toggle start/stop
        self.shortcut_space = QShortcut(QKeySequence(Qt.Key_Space), self)
        self.shortcut_space.activated.connect(self._toggle_start_stop)
        
        # v10.0: F5 to refresh device list
        self.shortcut_f5 = QShortcut(QKeySequence(Qt.Key_F5), self)
        self.shortcut_f5.activated.connect(self.on_list)
    
    def _toggle_start_stop(self) -> None:
        """Toggle between start and stop states."""
        if self.backend is None:
            self.on_start()
        else:
            self.on_stop()
    
    def on_list(self) -> None:
        """Refresh the list of available audio devices."""
        if not AUDIO_BACKEND_AVAILABLE or list_audio_devices is None:
            if self.logger:
                self.logger.error("Audio backend not available")
            return
        
        self.combo_device.clear()
        
        try:
            devices = list_audio_devices()
            
            for idx, name, is_loopback in devices:
                # v10.0: Mark loopback devices clearly
                display_name = f"{name}"
                if is_loopback:
                    display_name = f"🔄 {name} [LOOPBACK]"
                
                self.combo_device.addItem(display_name, idx)
            
            if self.logger:
                self.logger.info(f"Found {len(devices)} audio devices")
        
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error listing devices: {e}")
    
    def on_start(self) -> None:
        """Start audio capture."""
        if self.backend is not None:
            return  # Already running
        
        if not AUDIO_BACKEND_AVAILABLE or PyAudioInput is None:
            if self.logger:
                self.logger.error("Audio backend not available")
            return
        
        # Get configuration
        device_idx = self.combo_device.currentData()
        rate = self.spin_rate.value()
        buf = self.spin_buffer.value()
        
        # v10.0: Store current settings
        self.current_buffer_size = buf
        self.current_rate = rate
        
        try:
            # Create backend
            self.backend = PyAudioInput(
                device_index=device_idx,
                sample_rate=rate,
                buffer_frames=buf,
                channels=2,
                logger=self.logger
            )
            
            # Define audio callback
            def audio_callback(data):
                # Process audio data here
                # For now, just a placeholder
                pass
            
            # Start capture
            if self.backend.start(audio_callback):
                # v10.0: Update LED indicator
                self.status_led.setText('🟢 Połączono')
                self.status_led.setStyleSheet('color: #0d7377; font-weight: bold;')
                
                # Update UI state
                self.btn_start.setEnabled(False)
                self.btn_stop.setEnabled(True)
                self.combo_device.setEnabled(False)
                self.spin_rate.setEnabled(False)
                self.spin_buffer.setEnabled(False)
                
                if self.logger:
                    self.logger.info(f"Audio capture started: {rate}Hz, {buf} frames")
            else:
                self.backend = None
                if self.logger:
                    self.logger.error("Failed to start audio backend")
        
        except Exception as e:
            self.backend = None
            if self.logger:
                self.logger.error(f"Error starting audio: {e}")
    
    def on_stop(self) -> None:
        """Stop audio capture."""
        if self.backend is None:
            return
        
        try:
            self.backend.stop()
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error stopping audio: {e}")
        finally:
            self.backend = None
        
        # v10.0: Update LED indicator
        self.status_led.setText('🔴 Rozłączono')
        self.status_led.setStyleSheet('color: #888; font-weight: bold;')
        
        # Update UI state
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.combo_device.setEnabled(True)
        self.spin_rate.setEnabled(True)
        self.spin_buffer.setEnabled(True)
        
        if self.logger:
            self.logger.info("Audio capture stopped")
    
    def on_tick(self) -> None:
        """Update loop called at 60 FPS."""
        # v10.0: Update performance indicators
        if self.backend is not None and self.perf_monitor:
            # Get CPU usage
            cpu = self.perf_monitor.get_current_cpu()
            if cpu >= 0:
                self.status_cpu.setText(f'CPU: {cpu:.1f}%')
            else:
                self.status_cpu.setText('CPU: --%')
            
            # Calculate and display latency
            latency_ms = (self.current_buffer_size / self.current_rate) * 1000
            self.status_latency.setText(f'Opóźnienie: {latency_ms:.1f} ms')
            self.perf_monitor.record_latency(latency_ms)
        else:
            self.status_latency.setText('Opóźnienie: -- ms')
            self.status_cpu.setText('CPU: --%')
    
    def closeEvent(self, event) -> None:
        """Handle window close event."""
        # Stop audio if running
        if self.backend is not None:
            self.on_stop()
        
        # Stop timer
        self.timer.stop()
        
        event.accept()
