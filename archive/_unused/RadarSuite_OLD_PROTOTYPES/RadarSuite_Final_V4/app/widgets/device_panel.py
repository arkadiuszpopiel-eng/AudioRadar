"""
RadarSuite v3.5.0 - Device_Panel Widgets
"""

import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QSlider, QCheckBox, QSpinBox, QGroupBox, QFormLayout
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QPalette

from core import log, tr, TOAST_DURATION_MS, TOAST_MAX_COUNT


class DevicePanel(QWidget):
    """Device selection and configuration panel"""

    def __init__(self, audio_engine):
        super().__init__()
        self.audio = audio_engine
        log("DevicePanel.__init__", "INFO")

        layout = QVBoxLayout()

        # Device selection
        device_group = QGroupBox(tr('audio_device'))
        device_layout = QVBoxLayout()

        self.device_combo = QComboBox()
        self.select_device_label = QLabel(tr('select_device'))
        device_layout.addWidget(self.select_device_label)
        device_layout.addWidget(self.device_combo)

        self.refresh_btn = QPushButton(tr('refresh_devices'))
        self.refresh_btn.clicked.connect(self.refresh_devices)
        device_layout.addWidget(self.refresh_btn)

        device_group.setLayout(device_layout)
        layout.addWidget(device_group)

        # Audio settings
        settings_group = QGroupBox(tr('audio_settings'))
        settings_layout = QFormLayout()

        self.samplerate_combo = QComboBox()
        self.samplerate_combo.addItems(['44100', '48000', '96000'])
        self.samplerate_combo.setCurrentText('48000')
        settings_layout.addRow(tr('sample_rate'), self.samplerate_combo)

        self.blocksize_combo = QComboBox()
        self.blocksize_combo.addItems(['512', '1024', '2048', '4096'])
        self.blocksize_combo.setCurrentText('2048')
        settings_layout.addRow(tr('block_size'), self.blocksize_combo)

        self.channels_combo = QComboBox()
        self.channels_combo.addItems(['1', '2', '6', '8'])
        self.channels_combo.setCurrentText('2')
        settings_layout.addRow(tr('channels'), self.channels_combo)

        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)

        # Mode selection
        mode_group = QGroupBox(tr('mode'))
        mode_layout = QVBoxLayout()

        self.test_mode = QCheckBox(tr('test_mode'))
        mode_layout.addWidget(self.test_mode)

        self.loopback_mode = QCheckBox(tr('loopback_mode'))
        self.loopback_mode.toggled.connect(self.on_loopback_toggled)
        mode_layout.addWidget(self.loopback_mode)

        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)

        # Audio Enhancements (v3.1.2 - Auto-gain for quiet audio)
        enhance_group = QGroupBox("🎚️ Audio Enhancements")
        enhance_layout = QVBoxLayout()

        # Auto-gain checkbox
        self.auto_gain_enable = QCheckBox("Enable Auto-Gain (boost quiet audio)")
        self.auto_gain_enable.setToolTip("Automatically amplify quiet audio signals for better detection")
        self.auto_gain_enable.setChecked(False)
        enhance_layout.addWidget(self.auto_gain_enable)

        # Manual gain slider
        gain_slider_layout = QHBoxLayout()
        gain_slider_layout.addWidget(QLabel("Manual Gain:"))
        self.gain_slider = QSlider(Qt.Horizontal)
        self.gain_slider.setRange(1, 100)  # 1x to 100x gain
        self.gain_slider.setValue(1)  # Default 1x (no gain)
        self.gain_slider.setEnabled(True)  # Enabled by default (auto-gain is off)
        gain_slider_layout.addWidget(self.gain_slider)
        self.gain_label = QLabel("1x")
        self.gain_slider.valueChanged.connect(lambda v: self.gain_label.setText(f"{v}x"))
        gain_slider_layout.addWidget(self.gain_label)
        enhance_layout.addLayout(gain_slider_layout)

        # Connect auto-gain checkbox to disable manual slider
        self.auto_gain_enable.toggled.connect(lambda checked: self.gain_slider.setEnabled(not checked))

        # Noise gate threshold
        noise_gate_layout = QHBoxLayout()
        noise_gate_layout.addWidget(QLabel("Noise Gate:"))
        self.noise_gate_slider = QSlider(Qt.Horizontal)
        self.noise_gate_slider.setRange(0, 100)
        self.noise_gate_slider.setValue(5)  # Default -60 dB
        self.noise_gate_slider.setToolTip("Block audio below this level (reduces noise)")
        noise_gate_layout.addWidget(self.noise_gate_slider)
        self.noise_gate_label = QLabel("-60dB")
        self.noise_gate_slider.valueChanged.connect(
            lambda v: self.noise_gate_label.setText(f"-{80-v}dB")
        )
        noise_gate_layout.addWidget(self.noise_gate_label)
        enhance_layout.addLayout(noise_gate_layout)

        enhance_group.setLayout(enhance_layout)
        layout.addWidget(enhance_group)

        # Presets
        preset_group = QGroupBox(tr('presets'))
        preset_layout = QVBoxLayout()

        self.sb_btn = QPushButton(tr('sb_preset'))
        self.sb_btn.clicked.connect(self.apply_sb_preset)
        preset_layout.addWidget(self.sb_btn)

        preset_group.setLayout(preset_layout)
        layout.addWidget(preset_group)

        # Game Detection (v3.0)
        self.game_group = QGroupBox("🎮 Game Detection")
        game_layout = QVBoxLayout()

        self.detected_games_label = QLabel("No games detected")
        self.detected_games_label.setStyleSheet("font-size: 9pt; color: #888888;")
        self.detected_games_label.setWordWrap(True)
        game_layout.addWidget(self.detected_games_label)

        self.detected_engines_label = QLabel("No engines detected")
        self.detected_engines_label.setStyleSheet("font-size: 9pt; color: #888888;")
        self.detected_engines_label.setWordWrap(True)
        game_layout.addWidget(self.detected_engines_label)

        self.game_group.setLayout(game_layout)
        layout.addWidget(self.game_group)

        # Audio Sources (v3.0)
        self.sources_group = QGroupBox("🔊 Audio Sources")
        sources_layout = QVBoxLayout()

        # Active sources label
        self.active_sources_label = QLabel("Active: 0")
        self.active_sources_label.setStyleSheet("font-size: 9pt; font-weight: bold; color: #00FF00;")
        sources_layout.addWidget(self.active_sources_label)

        # Active sources list (compact)
        self.active_sources_list = QLabel("—")
        self.active_sources_list.setStyleSheet("font-size: 8pt; color: #00DD00;")
        self.active_sources_list.setWordWrap(True)
        self.active_sources_list.setMaximumHeight(60)
        sources_layout.addWidget(self.active_sources_list)

        # Inactive sources label
        self.inactive_sources_label = QLabel("Inactive: 0")
        self.inactive_sources_label.setStyleSheet("font-size: 9pt; font-weight: bold; color: #FF6666;")
        sources_layout.addWidget(self.inactive_sources_label)

        # Inactive sources list (compact)
        self.inactive_sources_list = QLabel("—")
        self.inactive_sources_list.setStyleSheet("font-size: 8pt; color: #DD6666;")
        self.inactive_sources_list.setWordWrap(True)
        self.inactive_sources_list.setMaximumHeight(40)
        sources_layout.addWidget(self.inactive_sources_list)

        self.sources_group.setLayout(sources_layout)
        layout.addWidget(self.sources_group)

        # Status
        status_group = QGroupBox(tr('status'))
        status_layout = QVBoxLayout()

        self.rms_label = QLabel(f"{tr('rms')} --- dBFS")
        status_layout.addWidget(self.rms_label)

        self.backend_label = QLabel(f"{tr('backend')} sounddevice")
        status_layout.addWidget(self.backend_label)

        status_group.setLayout(status_layout)
        layout.addWidget(status_group)

        layout.addStretch()
        self.setLayout(layout)

        self.refresh_devices()

    def refresh_devices(self):
        """Refresh device list"""
        self.device_combo.clear()
        devices = self.audio.list_devices()

        for dev in devices:
            if dev['type'] in ['input', 'loopback']:
                label = f"{dev['name']} ({dev['channels']}ch, {dev['samplerate']}Hz) [{dev['backend']}]"
                self.device_combo.addItem(label, dev)

        log(f"Refreshed devices: found {len(devices)}", "INFO")

    def apply_settings(self):
        """Apply current settings to audio engine"""
        self.audio.sample_rate = int(self.samplerate_combo.currentText())
        self.audio.blocksize = int(self.blocksize_combo.currentText())
        self.audio.channels = int(self.channels_combo.currentText())

        dev_data = self.device_combo.currentData()
        if dev_data:
            if dev_data['backend'] == 'sounddevice':
                self.audio.device = dev_data['index']
                self.audio.use_loopback = False
                self.backend_label.setText(f"{tr('backend')} sounddevice")
            else:
                self.audio.use_loopback = True
                self.backend_label.setText(f"{tr('backend')} soundcard (loopback)")

        log(f"Applied settings: SR={self.audio.sample_rate}, BS={self.audio.blocksize}, CH={self.audio.channels}", "INFO")

    def apply_sb_preset(self):
        """Apply Sound Blaster Z SE preset"""
        self.samplerate_combo.setCurrentText('48000')
        self.blocksize_combo.setCurrentText('2048')
        self.channels_combo.setCurrentText('2')
        log("Applied SB Z SE preset", "INFO")

    def on_loopback_toggled(self, checked):
        """Handle loopback mode toggle"""
        if checked:
            self.audio.use_loopback = True
            self.backend_label.setText(f"{tr('backend')} soundcard (loopback)")
        else:
            self.audio.use_loopback = False
            self.backend_label.setText(f"{tr('backend')} sounddevice")

    def update_translations(self):
        """Update UI translations"""
        # Update group box titles
        for i in range(self.layout().count()):
            item = self.layout().itemAt(i)
            if item and isinstance(item.widget(), QGroupBox):
                gb = item.widget()
                # Get the translation key based on current title
                if 'Audio Device' in gb.title() or 'Urządzenie Audio' in gb.title():
                    gb.setTitle(tr('audio_device'))
                elif 'Audio Settings' in gb.title() or 'Ustawienia Audio' in gb.title():
                    gb.setTitle(tr('audio_settings'))
                elif 'Mode' in gb.title() or 'Tryb' in gb.title():
                    gb.setTitle(tr('mode'))
                elif 'Presets' in gb.title() or 'Presety' in gb.title():
                    gb.setTitle(tr('presets'))
                elif 'Status' in gb.title():
                    gb.setTitle(tr('status'))

        # Update labels and buttons
        self.select_device_label.setText(tr('select_device'))
        self.refresh_btn.setText(tr('refresh_devices'))
        self.test_mode.setText(tr('test_mode'))
        self.loopback_mode.setText(tr('loopback_mode'))
        self.sb_btn.setText(tr('sb_preset'))

        # Update backend label
        if self.audio.use_loopback:
            self.backend_label.setText(f"{tr('backend')} soundcard (loopback)")
        else:
            self.backend_label.setText(f"{tr('backend')} sounddevice")


# ============================================================================
# SOUND CLASSIFIER (Module 7 - v3.2.0)
# ============================================================================





