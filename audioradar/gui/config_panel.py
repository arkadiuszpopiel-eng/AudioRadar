"""
Configuration panel for Audio Radar settings.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                             QLabel, QSlider, QComboBox, QPushButton, QSpinBox,
                             QCheckBox)
from PyQt5.QtCore import Qt, pyqtSignal
from audioradar.config import Config


class ConfigPanel(QWidget):
    """Configuration panel widget."""
    
    # Signals
    configChanged = pyqtSignal(str, str, object)  # section, key, value
    themeChanged = pyqtSignal(str)  # theme name
    deviceSelectRequested = pyqtSignal()
    
    def __init__(self, config: Config, parent=None):
        super().__init__(parent)
        
        self.config = config
        self._setup_ui()
        self._load_values()
    
    def _setup_ui(self):
        """Setup user interface."""
        layout = QVBoxLayout()
        
        # Audio settings
        audio_group = QGroupBox("Audio Settings")
        audio_layout = QVBoxLayout()
        
        # Device selection
        device_layout = QHBoxLayout()
        device_layout.addWidget(QLabel("Input Device:"))
        self.device_btn = QPushButton("Select Device...")
        self.device_btn.clicked.connect(self.deviceSelectRequested.emit)
        device_layout.addWidget(self.device_btn)
        device_layout.addStretch()
        audio_layout.addLayout(device_layout)
        
        # Sample rate
        sr_layout = QHBoxLayout()
        sr_layout.addWidget(QLabel("Sample Rate:"))
        self.sample_rate = QComboBox()
        self.sample_rate.addItems(["44100", "48000", "96000"])
        self.sample_rate.currentTextChanged.connect(
            lambda v: self._on_value_changed("audio", "sample_rate", int(v))
        )
        sr_layout.addWidget(self.sample_rate)
        sr_layout.addStretch()
        audio_layout.addLayout(sr_layout)
        
        # Channels
        ch_layout = QHBoxLayout()
        ch_layout.addWidget(QLabel("Channels:"))
        self.channels = QComboBox()
        self.channels.addItems(["2 (Stereo)", "6 (5.1)", "8 (7.1)"])
        self.channels.currentIndexChanged.connect(
            lambda i: self._on_value_changed("audio", "channels", [2, 6, 8][i])
        )
        ch_layout.addWidget(self.channels)
        ch_layout.addStretch()
        audio_layout.addLayout(ch_layout)
        
        audio_group.setLayout(audio_layout)
        layout.addWidget(audio_group)
        
        # Detection settings
        detection_group = QGroupBox("Detection Settings")
        detection_layout = QVBoxLayout()
        
        # Footstep threshold
        self.footstep_threshold = self._create_slider_control(
            "Footstep Threshold:", 0, 100, 
            lambda v: self._on_value_changed("detection", "footstep_threshold", v/100)
        )
        detection_layout.addLayout(self.footstep_threshold)
        
        # Running threshold
        self.running_threshold = self._create_slider_control(
            "Running Threshold:", 0, 100,
            lambda v: self._on_value_changed("detection", "running_threshold", v/100)
        )
        detection_layout.addLayout(self.running_threshold)
        
        # Gunshot threshold
        self.gunshot_threshold = self._create_slider_control(
            "Gunshot Threshold:", 0, 100,
            lambda v: self._on_value_changed("detection", "gunshot_threshold", v/100)
        )
        detection_layout.addLayout(self.gunshot_threshold)
        
        detection_group.setLayout(detection_layout)
        layout.addWidget(detection_group)
        
        # GUI settings
        gui_group = QGroupBox("Display Settings")
        gui_layout = QVBoxLayout()
        
        # Theme
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Theme:"))
        self.theme = QComboBox()
        self.theme.addItems(["Dark", "Light"])
        self.theme.currentTextChanged.connect(
            lambda v: self.themeChanged.emit(v.lower())
        )
        theme_layout.addWidget(self.theme)
        theme_layout.addStretch()
        gui_layout.addLayout(theme_layout)
        
        # Radar transparency
        self.radar_transparency = self._create_slider_control(
            "Radar Transparency:", 10, 100,
            lambda v: self._on_value_changed("gui", "radar_transparency", v)
        )
        gui_layout.addLayout(self.radar_transparency)
        
        # Show spectrum
        self.show_spectrum = QCheckBox("Show Spectrum Analyzer")
        self.show_spectrum.stateChanged.connect(
            lambda s: self._on_value_changed("visualization", "show_spectrum", s == Qt.Checked)
        )
        gui_layout.addWidget(self.show_spectrum)
        
        # Show distance
        self.show_distance = QCheckBox("Show Distance Estimates")
        self.show_distance.stateChanged.connect(
            lambda s: self._on_value_changed("visualization", "show_distance", s == Qt.Checked)
        )
        gui_layout.addWidget(self.show_distance)
        
        gui_group.setLayout(gui_layout)
        layout.addWidget(gui_group)
        
        # Visualization settings
        viz_group = QGroupBox("Visualization Settings")
        viz_layout = QVBoxLayout()
        
        # Decay time
        decay_layout = QHBoxLayout()
        decay_layout.addWidget(QLabel("Event Decay Time (s):"))
        self.decay_time = QSpinBox()
        self.decay_time.setRange(1, 10)
        self.decay_time.valueChanged.connect(
            lambda v: self._on_value_changed("visualization", "decay_time", float(v))
        )
        decay_layout.addWidget(self.decay_time)
        decay_layout.addStretch()
        viz_layout.addLayout(decay_layout)
        
        viz_group.setLayout(viz_layout)
        layout.addWidget(viz_group)
        
        layout.addStretch()
        
        # Save button
        save_btn = QPushButton("Save Configuration")
        save_btn.clicked.connect(self._save_config)
        layout.addWidget(save_btn)
        
        self.setLayout(layout)
    
    def _create_slider_control(self, label: str, min_val: int, max_val: int, 
                               callback) -> QHBoxLayout:
        """Create a slider control with label."""
        layout = QHBoxLayout()
        layout.addWidget(QLabel(label))
        
        slider = QSlider(Qt.Horizontal)
        slider.setRange(min_val, max_val)
        slider.valueChanged.connect(callback)
        layout.addWidget(slider)
        
        value_label = QLabel(str(min_val))
        slider.valueChanged.connect(lambda v: value_label.setText(str(v)))
        layout.addWidget(value_label)
        
        # Store references
        layout.slider = slider
        layout.label = value_label
        
        return layout
    
    def _load_values(self):
        """Load values from config."""
        # Audio
        sr = self.config.get("audio", "sample_rate", 44100)
        self.sample_rate.setCurrentText(str(sr))
        
        ch = self.config.get("audio", "channels", 2)
        ch_map = {2: 0, 6: 1, 8: 2}
        self.channels.setCurrentIndex(ch_map.get(ch, 0))
        
        # Detection
        ft = int(self.config.get("detection", "footstep_threshold", 0.3) * 100)
        self.footstep_threshold.slider.setValue(ft)
        
        rt = int(self.config.get("detection", "running_threshold", 0.5) * 100)
        self.running_threshold.slider.setValue(rt)
        
        gt = int(self.config.get("detection", "gunshot_threshold", 0.7) * 100)
        self.gunshot_threshold.slider.setValue(gt)
        
        # GUI
        theme = self.config.get("gui", "theme", "dark")
        self.theme.setCurrentText(theme.capitalize())
        
        transp = self.config.get("gui", "radar_transparency", 80)
        self.radar_transparency.slider.setValue(transp)
        
        # Visualization
        show_spec = self.config.get("visualization", "show_spectrum", True)
        self.show_spectrum.setChecked(show_spec)
        
        show_dist = self.config.get("visualization", "show_distance", True)
        self.show_distance.setChecked(show_dist)
        
        decay = int(self.config.get("visualization", "decay_time", 2.0))
        self.decay_time.setValue(decay)
    
    def _on_value_changed(self, section: str, key: str, value):
        """Handle value change."""
        self.config.set(section, key, value)
        self.configChanged.emit(section, key, value)
    
    def _save_config(self):
        """Save configuration to file."""
        self.config.save()
