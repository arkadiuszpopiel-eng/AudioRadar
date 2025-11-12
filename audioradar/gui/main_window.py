"""
Main application window for Audio Radar.
Integrates all GUI components and audio processing.
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QSplitter, QPushButton, QLabel, QStatusBar,
                             QMessageBox, QAction, QMenu)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon

from audioradar.config import Config
from audioradar.logger import get_logger
from audioradar.audio_engine import AudioEngine
from audioradar.detector import EventDetector
from audioradar.localizer import AudioLocalizer

from audioradar.gui.radar_widget import RadarWidget
from audioradar.gui.spectrum_widget import SpectrumWidget
from audioradar.gui.config_panel import ConfigPanel
from audioradar.gui.device_manager import DeviceManager
from audioradar.gui.audio_test_dialog import AudioTestDialog
from audioradar.gui.theme_manager import ThemeManager


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self, config: Config):
        super().__init__()
        
        self.config = config
        self.logger = get_logger()
        
        # Audio components
        self.audio_engine = None
        self.detector = None
        self.localizer = None
        
        # State
        self.is_running = False
        self.previous_distance = {}  # Track distances per event type
        
        # Setup UI
        self.setWindowTitle("Audio Radar")
        self._setup_ui()
        self._setup_menu()
        
        # Apply theme
        theme = self.config.get("gui", "theme", "dark")
        ThemeManager.apply_theme(self.app(), theme)
        self._update_widget_colors(theme)
        
        # Restore window state
        width = self.config.get("gui", "window_width", 1200)
        height = self.config.get("gui", "window_height", 800)
        self.resize(width, height)
        
        self.logger.info("Main window initialized")
    
    def app(self):
        """Get QApplication instance."""
        from PyQt5.QtWidgets import QApplication
        return QApplication.instance()
    
    def _setup_ui(self):
        """Setup user interface."""
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout()
        
        # Left side - Radar and Spectrum
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        
        # Radar widget
        radar_size = self.config.get("gui", "radar_size", 400)
        radar_transp = self.config.get("gui", "radar_transparency", 80)
        self.radar = RadarWidget(size=radar_size, transparency=radar_transp)
        left_layout.addWidget(self.radar, stretch=1)
        
        # Spectrum widget (optional)
        show_spectrum = self.config.get("visualization", "show_spectrum", True)
        self.spectrum = SpectrumWidget()
        if show_spectrum:
            left_layout.addWidget(self.spectrum)
        else:
            self.spectrum.hide()
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self._start_capture)
        button_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self._stop_capture)
        self.stop_btn.setEnabled(False)
        button_layout.addWidget(self.stop_btn)
        
        self.clear_btn = QPushButton("Clear Radar")
        self.clear_btn.clicked.connect(self.radar.clear_events)
        button_layout.addWidget(self.clear_btn)
        
        button_layout.addStretch()
        
        left_layout.addLayout(button_layout)
        
        left_widget.setLayout(left_layout)
        
        # Right side - Configuration panel
        self.config_panel = ConfigPanel(self.config)
        self.config_panel.configChanged.connect(self._on_config_changed)
        self.config_panel.themeChanged.connect(self._on_theme_changed)
        self.config_panel.deviceSelectRequested.connect(self._select_device)
        
        # Splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(self.config_panel)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(splitter)
        central.setLayout(main_layout)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_label = QLabel("Ready")
        self.status_bar.addPermanentWidget(self.status_label)
        
        self._update_status("Ready - Click Start to begin")
    
    def _setup_menu(self):
        """Setup menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Audio menu
        audio_menu = menubar.addMenu("&Audio")
        
        select_device = QAction("Select &Device...", self)
        select_device.triggered.connect(self._select_device)
        audio_menu.addAction(select_device)
        
        test_device = QAction("&Test Device...", self)
        test_device.triggered.connect(self._test_device)
        audio_menu.addAction(test_device)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        toggle_spectrum = QAction("Toggle &Spectrum", self)
        toggle_spectrum.triggered.connect(self._toggle_spectrum)
        view_menu.addAction(toggle_spectrum)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _start_capture(self):
        """Start audio capture and processing."""
        if self.is_running:
            return
        
        try:
            self.logger.info("Starting audio capture...")
            
            # Get audio configuration
            device = self.config.get("audio", "input_device")
            sample_rate = self.config.get("audio", "sample_rate", 44100)
            channels = self.config.get("audio", "channels", 2)
            
            # Create audio engine
            self.audio_engine = AudioEngine(
                device_index=device,
                sample_rate=sample_rate,
                channels=channels
            )
            
            # Create detector
            self.detector = EventDetector(
                sample_rate=sample_rate,
                footstep_threshold=self.config.get("detection", "footstep_threshold", 0.3),
                running_threshold=self.config.get("detection", "running_threshold", 0.5),
                gunshot_threshold=self.config.get("detection", "gunshot_threshold", 0.7)
            )
            
            # Create localizer
            self.localizer = AudioLocalizer(channels=channels)
            
            # Set audio callback
            self.audio_engine.set_callback(self._process_audio)
            
            # Start engine
            self.audio_engine.start()
            
            self.is_running = True
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self._update_status("Running - Listening for events...")
            
            self.logger.info("Audio capture started successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to start capture: {e}")
            QMessageBox.critical(self, "Error", f"Failed to start audio capture:\n{str(e)}")
            self._update_status("Error - Failed to start")
    
    def _stop_capture(self):
        """Stop audio capture."""
        if not self.is_running:
            return
        
        self.logger.info("Stopping audio capture...")
        
        if self.audio_engine:
            self.audio_engine.stop()
            self.audio_engine = None
        
        self.is_running = False
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self._update_status("Stopped")
        
        self.logger.info("Audio capture stopped")
    
    def _process_audio(self, audio_data):
        """Process audio data callback."""
        try:
            # Update spectrum
            self.spectrum.update_spectrum(audio_data)
            
            # Detect events
            event = self.detector.detect(audio_data)
            
            if event:
                # Localize event
                angle, distance = self.localizer.localize(audio_data)
                
                # Add to radar
                self.radar.add_event(event.type, angle, distance, event.confidence)
                
                # Log event
                self.logger.info(f"Event detected: {event.type} at {angle:.1f}° "
                               f"distance={distance:.2f} confidence={event.confidence:.2f}")
                
                # Update status
                direction = self._angle_to_direction(angle)
                self._update_status(f"Detected: {event.type} from {direction}")
                
                # Track distance changes
                prev_dist = self.previous_distance.get(event.type, distance)
                approaching = self.localizer.is_approaching(distance, prev_dist)
                self.previous_distance[event.type] = distance
                
                if approaching is not None:
                    direction_text = "approaching" if approaching else "receding"
                    self.logger.info(f"Event is {direction_text}")
        
        except Exception as e:
            self.logger.error(f"Error processing audio: {e}")
    
    def _angle_to_direction(self, angle: float) -> str:
        """Convert angle to compass direction."""
        directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        index = int((angle + 22.5) / 45) % 8
        return directions[index]
    
    def _update_status(self, message: str):
        """Update status bar message."""
        self.status_label.setText(message)
    
    def _select_device(self):
        """Show device selection dialog."""
        dialog = DeviceManager(self)
        if dialog.exec_():
            device = dialog.get_selected_device()
            if device is not None:
                self.config.set("audio", "input_device", device)
                self.logger.info(f"Selected audio device: {device}")
                QMessageBox.information(self, "Device Selected", 
                                      f"Audio device {device} selected.\n"
                                      "Restart capture for changes to take effect.")
    
    def _test_device(self):
        """Show device test dialog."""
        device = self.config.get("audio", "input_device")
        dialog = AudioTestDialog(device, self)
        dialog.exec_()
    
    def _toggle_spectrum(self):
        """Toggle spectrum analyzer visibility."""
        if self.spectrum.isVisible():
            self.spectrum.hide()
            self.config.set("visualization", "show_spectrum", False)
        else:
            self.spectrum.show()
            self.config.set("visualization", "show_spectrum", True)
    
    def _show_about(self):
        """Show about dialog."""
        QMessageBox.about(self, "About Audio Radar",
                         "Audio Radar v1.0.0\n\n"
                         "Advanced audio visualization and detection system.\n\n"
                         "Detects and localizes:\n"
                         "• Footsteps\n"
                         "• Running\n"
                         "• Gunshots\n\n"
                         "Features real-time 360° radar display with\n"
                         "frequency spectrum analysis.")
    
    def _on_config_changed(self, section: str, key: str, value):
        """Handle configuration changes."""
        self.logger.info(f"Config changed: {section}.{key} = {value}")
        
        # Apply changes
        if section == "gui" and key == "radar_transparency":
            self.radar.set_transparency(value)
        elif section == "visualization" and key == "decay_time":
            self.radar.set_decay_time(value)
        elif section == "detection":
            if self.detector:
                thresholds = {
                    "footstep_threshold": self.config.get("detection", "footstep_threshold"),
                    "running_threshold": self.config.get("detection", "running_threshold"),
                    "gunshot_threshold": self.config.get("detection", "gunshot_threshold"),
                }
                self.detector.set_thresholds(**thresholds)
    
    def _on_theme_changed(self, theme: str):
        """Handle theme changes."""
        self.logger.info(f"Theme changed to: {theme}")
        ThemeManager.apply_theme(self.app(), theme)
        self._update_widget_colors(theme)
        self.config.set("gui", "theme", theme)
    
    def _update_widget_colors(self, theme: str):
        """Update widget colors based on theme."""
        colors = ThemeManager.get_radar_colors(theme)
        self.radar.set_colors(colors)
        self.spectrum.set_colors(colors)
    
    def closeEvent(self, event):
        """Handle window close event."""
        # Stop capture if running
        if self.is_running:
            self._stop_capture()
        
        # Save window size
        self.config.set("gui", "window_width", self.width())
        self.config.set("gui", "window_height", self.height())
        self.config.save()
        
        self.logger.info("Application closing")
        event.accept()
