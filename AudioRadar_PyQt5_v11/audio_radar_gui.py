"""
Main GUI Application for AudioRadar PyQt5
Comprehensive interface with all controls, settings, and visualizations.
"""

import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QLabel, QComboBox, QSlider, QSpinBox, QDoubleSpinBox,
    QGroupBox, QFormLayout, QCheckBox, QProgressBar, QTextEdit,
    QSplitter, QMessageBox, QFileDialog, QStatusBar, QAction, QMenuBar
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon

from audio_manager import AudioManager
from sound_detector import SoundDetector, SoundType
from radar_widget import RadarWidget
from spectrum_analyzer import SpectrumAnalyzerWidget
from theme_manager import ThemeManager
from config_manager import ConfigManager
from logger import get_logger


class AudioRadarGUI(QMainWindow):
    """Main GUI application window."""

    def __init__(self):
        super().__init__()

        self.logger = get_logger()
        self.logger.info("Initializing Audio Radar GUI")

        # Initialize managers
        self.config_manager = ConfigManager()
        self.theme_manager = ThemeManager()
        self.audio_manager = AudioManager()
        self.sound_detector = SoundDetector()

        # UI components
        self.radar_widget = None
        self.detached_radar = None
        self.spectrum_widget = None

        # Status
        self.is_running = False

        # Setup UI
        self.init_ui()

        # Apply theme
        ui_config = self.config_manager.get_ui_config()
        self.theme_manager.apply_theme(ui_config.theme)

        # Connect signals
        self.connect_signals()

        # Load initial settings
        self.load_settings()

        self.logger.info("Audio Radar GUI initialized successfully")

    def init_ui(self):
        """Initialize user interface."""
        self.setWindowTitle("Audio Radar v11 - PyQt5 Professional Edition")

        # Get UI config
        ui_config = self.config_manager.get_ui_config()

        # Set window size
        self.resize(ui_config.window_width, ui_config.window_height)

        if ui_config.window_x >= 0 and ui_config.window_y >= 0:
            self.move(ui_config.window_x, ui_config.window_y)

        # Create menu bar
        self.create_menu_bar()

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Create splitter for resizable sections
        splitter = QSplitter(Qt.Horizontal)

        # Left panel - Controls and settings
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)

        # Right panel - Visualizations
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)

        # Set splitter proportions
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)

        main_layout.addWidget(splitter)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def create_menu_bar(self):
        """Create menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        export_action = QAction("Export Configuration", self)
        export_action.triggered.connect(self.export_config)
        file_menu.addAction(export_action)

        import_action = QAction("Import Configuration", self)
        import_action.triggered.connect(self.import_config)
        file_menu.addAction(import_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu
        view_menu = menubar.addMenu("View")

        detach_radar_action = QAction("Detach Radar", self)
        detach_radar_action.triggered.connect(self.toggle_detached_radar)
        view_menu.addAction(detach_radar_action)

        # Help menu
        help_menu = menubar.addMenu("Help")

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_left_panel(self) -> QWidget:
        """Create left control panel."""
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)

        # Control buttons
        control_group = self.create_control_group()
        layout.addWidget(control_group)

        # Audio device selection
        device_group = self.create_device_group()
        layout.addWidget(device_group)

        # Detection settings
        detection_group = self.create_detection_group()
        layout.addWidget(detection_group)

        # Radar settings
        radar_group = self.create_radar_group()
        layout.addWidget(radar_group)

        # Theme selection
        theme_group = self.create_theme_group()
        layout.addWidget(theme_group)

        # Add stretch to push everything to top
        layout.addStretch()

        return panel

    def create_control_group(self) -> QGroupBox:
        """Create control buttons group."""
        group = QGroupBox("Control")
        layout = QVBoxLayout()

        # Start/Stop button
        self.start_stop_button = QPushButton("Start")
        self.start_stop_button.clicked.connect(self.toggle_start_stop)
        self.start_stop_button.setMinimumHeight(40)
        layout.addWidget(self.start_stop_button)

        # Audio quality test button
        self.test_button = QPushButton("Test Audio Quality")
        self.test_button.clicked.connect(self.test_audio_quality)
        layout.addWidget(self.test_button)

        # Status label
        self.status_label = QLabel("Status: Stopped")
        layout.addWidget(self.status_label)

        group.setLayout(layout)
        return group

    def create_device_group(self) -> QGroupBox:
        """Create audio device selection group."""
        group = QGroupBox("Audio Device")
        layout = QVBoxLayout()

        # Refresh button
        refresh_button = QPushButton("Refresh Devices")
        refresh_button.clicked.connect(self.refresh_devices)
        layout.addWidget(refresh_button)

        # Device combobox
        self.device_combo = QComboBox()
        layout.addWidget(self.device_combo)

        # Device info
        self.device_info_label = QLabel("No device selected")
        self.device_info_label.setWordWrap(True)
        layout.addWidget(self.device_info_label)

        # Sound Blaster optimization button
        sb_button = QPushButton("Optimize for Sound Blaster Z")
        sb_button.clicked.connect(self.optimize_sound_blaster)
        layout.addWidget(sb_button)

        group.setLayout(layout)
        return group

    def create_detection_group(self) -> QGroupBox:
        """Create detection settings group."""
        group = QGroupBox("Detection Settings")
        layout = QFormLayout()

        # Enable/disable detection types
        self.walking_checkbox = QCheckBox()
        self.walking_checkbox.setChecked(True)
        layout.addRow("Enable Walking:", self.walking_checkbox)

        self.running_checkbox = QCheckBox()
        self.running_checkbox.setChecked(True)
        layout.addRow("Enable Running:", self.running_checkbox)

        self.shooting_checkbox = QCheckBox()
        self.shooting_checkbox.setChecked(True)
        layout.addRow("Enable Shooting:", self.shooting_checkbox)

        # Confidence threshold
        self.confidence_slider = QSlider(Qt.Horizontal)
        self.confidence_slider.setRange(0, 100)
        self.confidence_slider.setValue(50)
        self.confidence_slider.setTickPosition(QSlider.TicksBelow)
        self.confidence_slider.setTickInterval(10)
        self.confidence_label = QLabel("50%")
        self.confidence_slider.valueChanged.connect(
            lambda v: self.confidence_label.setText(f"{v}%")
        )
        layout.addRow("Confidence Threshold:", self.confidence_slider)
        layout.addRow("", self.confidence_label)

        group.setLayout(layout)
        return group

    def create_radar_group(self) -> QGroupBox:
        """Create radar settings group."""
        group = QGroupBox("Radar Settings")
        layout = QFormLayout()

        # Opacity slider
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(90)
        self.opacity_slider.setTickPosition(QSlider.TicksBelow)
        self.opacity_slider.setTickInterval(10)
        self.opacity_label = QLabel("90%")
        self.opacity_slider.valueChanged.connect(self.update_radar_opacity)
        layout.addRow("Opacity:", self.opacity_slider)
        layout.addRow("", self.opacity_label)

        # Fade duration
        self.fade_spin = QDoubleSpinBox()
        self.fade_spin.setRange(0.5, 10.0)
        self.fade_spin.setValue(2.0)
        self.fade_spin.setSingleStep(0.5)
        self.fade_spin.setSuffix(" s")
        layout.addRow("Fade Duration:", self.fade_spin)

        group.setLayout(layout)
        return group

    def create_theme_group(self) -> QGroupBox:
        """Create theme selection group."""
        group = QGroupBox("Theme")
        layout = QVBoxLayout()

        self.theme_combo = QComboBox()
        themes = self.theme_manager.get_available_themes()
        for theme in themes:
            self.theme_combo.addItem(theme.replace('_', ' ').title(), theme)

        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        layout.addWidget(self.theme_combo)

        group.setLayout(layout)
        return group

    def create_right_panel(self) -> QWidget:
        """Create right visualization panel."""
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)

        # Tab widget for different views
        tab_widget = QTabWidget()

        # Radar tab
        radar_tab = QWidget()
        radar_layout = QVBoxLayout()
        self.radar_widget = RadarWidget()
        radar_layout.addWidget(self.radar_widget)
        radar_tab.setLayout(radar_layout)
        tab_widget.addTab(radar_tab, "Radar")

        # Spectrum tab
        spectrum_tab = QWidget()
        spectrum_layout = QVBoxLayout()
        self.spectrum_widget = SpectrumAnalyzerWidget()
        spectrum_layout.addWidget(self.spectrum_widget)
        spectrum_tab.setLayout(spectrum_layout)
        tab_widget.addTab(spectrum_tab, "Spectrum Analyzer")

        # Statistics tab
        stats_tab = self.create_statistics_tab()
        tab_widget.addTab(stats_tab, "Statistics")

        # Log tab
        log_tab = self.create_log_tab()
        tab_widget.addTab(log_tab, "Log")

        layout.addWidget(tab_widget)

        return panel

    def create_statistics_tab(self) -> QWidget:
        """Create statistics tab."""
        tab = QWidget()
        layout = QVBoxLayout()

        # Detection statistics
        stats_group = QGroupBox("Detection Statistics")
        stats_layout = QFormLayout()

        self.total_detections_label = QLabel("0")
        stats_layout.addRow("Total Detections:", self.total_detections_label)

        self.walking_detections_label = QLabel("0")
        stats_layout.addRow("Walking:", self.walking_detections_label)

        self.running_detections_label = QLabel("0")
        stats_layout.addRow("Running:", self.running_detections_label)

        self.shooting_detections_label = QLabel("0")
        stats_layout.addRow("Shooting:", self.shooting_detections_label)

        self.avg_distance_label = QLabel("0.0 m")
        stats_layout.addRow("Average Distance:", self.avg_distance_label)

        self.avg_confidence_label = QLabel("0.0%")
        stats_layout.addRow("Average Confidence:", self.avg_confidence_label)

        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)

        # Audio quality metrics
        quality_group = QGroupBox("Audio Quality")
        quality_layout = QFormLayout()

        self.rms_level_label = QLabel("0.000")
        quality_layout.addRow("RMS Level:", self.rms_level_label)

        self.peak_level_label = QLabel("0.000")
        quality_layout.addRow("Peak Level:", self.peak_level_label)

        self.snr_label = QLabel("0.0 dB")
        quality_layout.addRow("SNR:", self.snr_label)

        self.noise_floor_label = QLabel("0.000")
        quality_layout.addRow("Noise Floor:", self.noise_floor_label)

        quality_group.setLayout(quality_layout)
        layout.addWidget(quality_group)

        # Update timer for statistics
        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.update_statistics)
        self.stats_timer.start(500)  # Update every 500ms

        layout.addStretch()
        tab.setLayout(layout)
        return tab

    def create_log_tab(self) -> QWidget:
        """Create log viewer tab."""
        tab = QWidget()
        layout = QVBoxLayout()

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumBlockCount(1000)  # Limit to 1000 lines
        layout.addWidget(self.log_text)

        # Buttons
        button_layout = QHBoxLayout()

        clear_button = QPushButton("Clear Log")
        clear_button.clicked.connect(self.log_text.clear)
        button_layout.addWidget(clear_button)

        save_button = QPushButton("Save Log")
        save_button.clicked.connect(self.save_log)
        button_layout.addWidget(save_button)

        button_layout.addStretch()

        layout.addLayout(button_layout)

        tab.setLayout(layout)
        return tab

    def connect_signals(self):
        """Connect signals between components."""
        # Audio manager signals
        self.audio_manager.audio_data_ready.connect(self.on_audio_data)
        self.audio_manager.audio_quality_changed.connect(self.on_quality_changed)
        self.audio_manager.error_occurred.connect(self.on_error)
        self.audio_manager.device_list_updated.connect(self.on_devices_updated)

        # Radar widget signal
        if self.radar_widget:
            self.radar_widget.detection_displayed.connect(self.on_detection_displayed)

        # Device combo signal
        self.device_combo.currentIndexChanged.connect(self.on_device_selected)

    def load_settings(self):
        """Load settings from configuration."""
        # Load audio config
        audio_config = self.config_manager.get_audio_config()

        # Load detection config
        detection_config = self.config_manager.get_detection_config()
        self.walking_checkbox.setChecked(detection_config.walking_enabled)
        self.running_checkbox.setChecked(detection_config.running_enabled)
        self.shooting_checkbox.setChecked(detection_config.shooting_enabled)
        self.confidence_slider.setValue(int(detection_config.confidence_threshold * 100))

        # Load radar config
        radar_config = self.config_manager.get_radar_config()
        self.opacity_slider.setValue(int(radar_config.opacity * 100))
        self.fade_spin.setValue(radar_config.fade_duration)

        if self.radar_widget:
            self.radar_widget.set_opacity(radar_config.opacity)
            self.radar_widget.fade_duration = radar_config.fade_duration

        # Refresh devices
        self.refresh_devices()

    def refresh_devices(self):
        """Refresh audio device list."""
        self.device_combo.clear()
        devices = self.audio_manager.get_input_devices()

        for device in devices:
            label = f"{device.name} ({device.channels}ch, {int(device.sample_rate)}Hz)"
            if device.is_default:
                label += " [Default]"
            self.device_combo.addItem(label, device)

        self.status_bar.showMessage(f"Found {len(devices)} input devices")

    def on_devices_updated(self, devices):
        """Handle device list update."""
        self.device_combo.clear()
        for device in devices:
            if device.is_input:
                label = f"{device.name} ({device.channels}ch, {int(device.sample_rate)}Hz)"
                if device.is_default:
                    label += " [Default]"
                self.device_combo.addItem(label, device)

    def on_device_selected(self, index):
        """Handle device selection."""
        if index >= 0:
            device = self.device_combo.itemData(index)
            if device:
                self.audio_manager.select_device(device)
                self.device_info_label.setText(
                    f"Selected: {device.name}\n"
                    f"Channels: {device.channels}\n"
                    f"Sample Rate: {int(device.sample_rate)} Hz\n"
                    f"Host API: {device.hostapi}"
                )

    def toggle_start_stop(self):
        """Toggle start/stop of audio capture and detection."""
        if not self.is_running:
            self.start()
        else:
            self.stop()

    def start(self):
        """Start audio capture and detection."""
        self.logger.info("Starting Audio Radar")

        # Update detection settings
        detection_config = self.config_manager.get_detection_config()
        detection_config.walking_enabled = self.walking_checkbox.isChecked()
        detection_config.running_enabled = self.running_checkbox.isChecked()
        detection_config.shooting_enabled = self.shooting_checkbox.isChecked()
        detection_config.confidence_threshold = self.confidence_slider.value() / 100.0

        # Start audio capture
        self.audio_manager.start_capture()

        self.is_running = True
        self.start_stop_button.setText("Stop")
        self.status_label.setText("Status: Running")
        self.status_bar.showMessage("Audio Radar started")

        self.log_message("Audio Radar started")

    def stop(self):
        """Stop audio capture and detection."""
        self.logger.info("Stopping Audio Radar")

        # Stop audio capture
        self.audio_manager.stop_capture()

        self.is_running = False
        self.start_stop_button.setText("Start")
        self.status_label.setText("Status: Stopped")
        self.status_bar.showMessage("Audio Radar stopped")

        self.log_message("Audio Radar stopped")

    def on_audio_data(self, audio_data, sample_rate):
        """Handle incoming audio data."""
        try:
            # Update spectrum analyzer
            if self.spectrum_widget:
                self.spectrum_widget.update_audio_data(audio_data, sample_rate)

            # Run sound detection
            detection = self.sound_detector.detect(audio_data, sample_rate)

            if detection:
                # Check if this type is enabled
                detection_config = self.config_manager.get_detection_config()

                enabled = True
                if detection.sound_type == SoundType.WALKING and not detection_config.walking_enabled:
                    enabled = False
                elif detection.sound_type == SoundType.RUNNING and not detection_config.running_enabled:
                    enabled = False
                elif detection.sound_type == SoundType.SHOOTING and not detection_config.shooting_enabled:
                    enabled = False

                if enabled:
                    # Update radar
                    if self.radar_widget:
                        self.radar_widget.add_detection(detection)

                    if self.detached_radar:
                        self.detached_radar.add_detection(detection)

                    # Log detection
                    self.log_message(
                        f"Detection: {detection.sound_type.value.upper()} at "
                        f"{detection.direction:.1f}° ({detection.distance:.1f}m)"
                    )

        except Exception as e:
            self.logger.error(f"Error processing audio data", e)

    def on_quality_changed(self, quality_metrics):
        """Handle audio quality metrics update."""
        self.current_quality_metrics = quality_metrics

    def on_error(self, error_message):
        """Handle error from audio manager."""
        self.logger.error(error_message)
        QMessageBox.critical(self, "Error", error_message)

    def on_detection_displayed(self, detection):
        """Handle detection displayed on radar."""
        pass  # Could add additional handling here

    def update_radar_opacity(self, value):
        """Update radar opacity."""
        opacity = value / 100.0
        self.opacity_label.setText(f"{value}%")

        if self.radar_widget:
            self.radar_widget.set_opacity(opacity)

        if self.detached_radar:
            self.detached_radar.set_opacity(opacity)

    def update_statistics(self):
        """Update statistics display."""
        # Update detection statistics
        summary = self.sound_detector.get_detection_summary()
        self.total_detections_label.setText(str(summary['total_detections']))
        self.walking_detections_label.setText(str(summary['walking']))
        self.running_detections_label.setText(str(summary['running']))
        self.shooting_detections_label.setText(str(summary['shooting']))
        self.avg_distance_label.setText(f"{summary['average_distance']:.1f} m")
        self.avg_confidence_label.setText(f"{summary['average_confidence'] * 100:.1f}%")

        # Update quality metrics
        if hasattr(self, 'current_quality_metrics'):
            metrics = self.current_quality_metrics
            self.rms_level_label.setText(f"{metrics.get('rms_level', 0):.4f}")
            self.peak_level_label.setText(f"{metrics.get('peak_level', 0):.4f}")
            self.snr_label.setText(f"{metrics.get('snr', 0):.1f} dB")
            self.noise_floor_label.setText(f"{metrics.get('noise_floor', 0):.4f}")

    def test_audio_quality(self):
        """Run audio quality test."""
        self.logger.info("Starting audio quality test")
        self.test_button.setEnabled(False)
        self.status_bar.showMessage("Testing audio quality...")

        # Run test
        results = self.audio_manager.test_audio_quality(duration=2.0)

        # Show results
        if results['success']:
            message = (
                f"Audio Quality Test Results:\n\n"
                f"Average RMS: {results['average_rms']:.4f}\n"
                f"Average Peak: {results['average_peak']:.4f}\n"
                f"Noise Floor: {results['noise_floor']:.4f}\n"
                f"SNR: {results['snr']:.1f} dB\n"
                f"Clipping: {'Yes' if results['clipping_detected'] else 'No'}\n\n"
                f"{results['message']}"
            )
            QMessageBox.information(self, "Audio Quality Test", message)
        else:
            QMessageBox.warning(self, "Audio Quality Test", results['message'])

        self.test_button.setEnabled(True)
        self.status_bar.showMessage("Ready")

    def optimize_sound_blaster(self):
        """Apply Sound Blaster Z SE optimizations."""
        self.audio_manager.optimize_for_sound_blaster_z()
        QMessageBox.information(
            self,
            "Sound Blaster Optimization",
            "Applied optimal settings for Sound Blaster Z SE:\n\n"
            "- Sample Rate: 48000 Hz\n"
            "- Block Size: 2048 samples\n"
            "- Channels: 2 (Stereo)"
        )
        self.log_message("Applied Sound Blaster Z SE optimizations")

    def toggle_detached_radar(self):
        """Toggle detached radar window."""
        if self.detached_radar is None:
            self.detached_radar = RadarWidget(detached=True)
            radar_config = self.config_manager.get_radar_config()
            self.detached_radar.set_opacity(radar_config.opacity)
            self.detached_radar.fade_duration = radar_config.fade_duration
            self.detached_radar.resize(radar_config.window_width, radar_config.window_height)
            self.detached_radar.move(radar_config.window_x, radar_config.window_y)
            self.detached_radar.show()
            self.log_message("Detached radar window opened")
        else:
            self.detached_radar.close()
            self.detached_radar = None
            self.log_message("Detached radar window closed")

    def change_theme(self, index):
        """Change application theme."""
        theme_name = self.theme_combo.itemData(index)
        self.theme_manager.apply_theme(theme_name)
        self.config_manager.set('ui', 'theme', theme_name)
        self.log_message(f"Theme changed to: {theme_name}")

    def log_message(self, message: str):
        """Add message to log viewer."""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")

    def export_config(self):
        """Export configuration to file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Configuration",
            "config_export.json",
            "JSON Files (*.json)"
        )

        if file_path:
            if self.config_manager.export_config(file_path):
                QMessageBox.information(self, "Export", "Configuration exported successfully")
            else:
                QMessageBox.warning(self, "Export", "Failed to export configuration")

    def import_config(self):
        """Import configuration from file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Configuration",
            "",
            "JSON Files (*.json)"
        )

        if file_path:
            if self.config_manager.import_config(file_path):
                self.load_settings()
                QMessageBox.information(self, "Import", "Configuration imported successfully")
            else:
                QMessageBox.warning(self, "Import", "Failed to import configuration")

    def save_log(self):
        """Save log to file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Log",
            "audio_radar_log.txt",
            "Text Files (*.txt)"
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.toPlainText())
                QMessageBox.information(self, "Save Log", "Log saved successfully")
            except Exception as e:
                QMessageBox.warning(self, "Save Log", f"Failed to save log: {str(e)}")

    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About Audio Radar",
            "Audio Radar v11 - PyQt5 Professional Edition\n\n"
            "Advanced audio detection and visualization system\n"
            "with directional tracking and distance estimation.\n\n"
            "Features:\n"
            "- Walking/Running/Shooting detection\n"
            "- Directional tracking (360°)\n"
            "- Distance estimation\n"
            "- Live spectrum analyzer\n"
            "- Detachable transparent radar\n"
            "- Sound Blaster Z SE optimization\n"
            "- Multiple themes\n"
            "- Comprehensive logging\n\n"
            "© 2024 Audio Radar Project"
        )

    def closeEvent(self, event):
        """Handle window close event."""
        # Stop audio capture
        if self.is_running:
            self.stop()

        # Save configuration
        ui_config = self.config_manager.get_ui_config()
        ui_config.window_width = self.width()
        ui_config.window_height = self.height()
        ui_config.window_x = self.x()
        ui_config.window_y = self.y()

        self.config_manager.save()

        # Close detached radar
        if self.detached_radar:
            self.detached_radar.close()

        self.logger.info("Audio Radar GUI closing")
        event.accept()
