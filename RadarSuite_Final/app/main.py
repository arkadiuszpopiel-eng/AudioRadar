"""
RadarSuite Final v2.3.0
Advanced audio radar and detection system for gaming
Supports: sounddevice, soundcard loopback, pyqtgraph visualization
Optimized for: ARC Raiders + Sound Blaster Z SE + HyperX Cloud II
"""

import sys
import os
import queue
import time
import math
from pathlib import Path
from datetime import datetime

import numpy as np
from scipy import signal as sp_signal

try:
    import sounddevice as sd
except ImportError:
    sd = None

try:
    import soundcard as sc
except ImportError:
    sc = None

import pyqtgraph as pg
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QDockWidget, QTabWidget, QPushButton, QLabel, QComboBox,
    QSlider, QCheckBox, QToolBar, QStatusBar, QSpinBox, QGroupBox,
    QFormLayout, QMessageBox, QAction
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QPalette

# ============================================================================
# PATHS AND LOGGING
# ============================================================================

ROOT = Path(__file__).parent.parent
SUPER_LOG = ROOT / "super_log.txt"


def log(msg: str, level: str = "INFO"):
    """Write to super_log.txt with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    line = f"[{timestamp}] [{level}] {msg}\n"

    try:
        with open(SUPER_LOG, 'a', encoding='utf-8') as f:
            f.write(line)
    except Exception as e:
        print(f"LOG ERROR: {e}")

    if level in ["ERROR", "CRITICAL"]:
        print(line.strip())


def apply_dark_theme(app: QApplication):
    """Apply dark theme to application"""
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(25, 25, 35))
    palette.setColor(QPalette.WindowText, QColor(220, 220, 230))
    palette.setColor(QPalette.Base, QColor(18, 18, 28))
    palette.setColor(QPalette.AlternateBase, QColor(30, 30, 40))
    palette.setColor(QPalette.ToolTipBase, QColor(50, 50, 60))
    palette.setColor(QPalette.ToolTipText, QColor(220, 220, 230))
    palette.setColor(QPalette.Text, QColor(220, 220, 230))
    palette.setColor(QPalette.Button, QColor(45, 45, 55))
    palette.setColor(QPalette.ButtonText, QColor(220, 220, 230))
    palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))

    app.setPalette(palette)

    stylesheet = """
        QMainWindow { background-color: #191923; }
        QDockWidget { background-color: #191923; color: #DCDCE6; }
        QDockWidget::title { background-color: #2D2D37; padding: 5px; }
        QPushButton {
            background-color: #2D2D37;
            color: #DCDCE6;
            border: 1px solid #2A82DA;
            border-radius: 3px;
            padding: 5px 15px;
            min-width: 80px;
        }
        QPushButton:hover { background-color: #2A82DA; }
        QPushButton:pressed { background-color: #1A5AA0; }
        QComboBox, QSpinBox {
            background-color: #121218;
            color: #DCDCE6;
            border: 1px solid #2A82DA;
            border-radius: 3px;
            padding: 3px;
        }
        QSlider::groove:horizontal {
            background: #121218;
            height: 6px;
            border-radius: 3px;
        }
        QSlider::handle:horizontal {
            background: #2A82DA;
            width: 14px;
            margin: -4px 0;
            border-radius: 7px;
        }
        QLabel { color: #DCDCE6; }
        QGroupBox {
            border: 1px solid #2A82DA;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
            font-weight: bold;
            color: #2A82DA;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 5px;
        }
    """
    app.setStyleSheet(stylesheet)


# ============================================================================
# AUDIO ENGINE
# ============================================================================

class AudioEngine:
    """
    Audio capture engine supporting:
    - sounddevice (standard input devices)
    - soundcard loopback (capture from speaker output)
    """

    def __init__(self):
        log("AudioEngine.__init__", "INFO")
        self.sample_rate = 48000
        self.blocksize = 2048
        self.channels = 2
        self.device = None
        self.stream = None
        self.queue = queue.Queue(maxsize=8)
        self.last_block = None
        self.running = False
        self.backend = "sounddevice"  # or "soundcard"
        self.use_loopback = False

    def list_devices(self):
        """List available audio devices"""
        devices = []

        if sd is not None:
            try:
                sd_devices = sd.query_devices()
                for idx, dev in enumerate(sd_devices):
                    devices.append({
                        'index': idx,
                        'name': dev['name'],
                        'channels': dev['max_input_channels'],
                        'samplerate': int(dev['default_samplerate']),
                        'hostapi': sd.query_hostapis(dev['hostapi'])['name'],
                        'type': 'input' if dev['max_input_channels'] > 0 else 'output',
                        'backend': 'sounddevice'
                    })
            except Exception as e:
                log(f"Error listing sounddevice devices: {e}", "ERROR")

        if sc is not None:
            try:
                # Loopback devices
                speakers = sc.all_speakers()
                for idx, spk in enumerate(speakers):
                    devices.append({
                        'index': f"loopback_{idx}",
                        'name': f"{spk.name} (Loopback)",
                        'channels': spk.channels,
                        'samplerate': 48000,
                        'hostapi': 'soundcard',
                        'type': 'loopback',
                        'backend': 'soundcard',
                        'speaker_obj': spk
                    })
            except Exception as e:
                log(f"Error listing soundcard devices: {e}", "ERROR")

        return devices

    def start(self):
        """Start audio capture"""
        if self.running:
            log("AudioEngine already running", "WARN")
            return

        self.running = True

        if self.use_loopback and sc is not None:
            log(f"Starting soundcard loopback: {self.sample_rate}Hz, {self.blocksize} samples", "INFO")
            self._start_loopback()
        else:
            log(f"Starting sounddevice: device={self.device}, {self.sample_rate}Hz, {self.blocksize} samples", "INFO")
            self._start_sounddevice()

    def _start_sounddevice(self):
        """Start sounddevice input stream"""
        try:
            def callback(indata, frames, time_info, status):
                if status:
                    log(f"sounddevice status: {status}", "WARN")

                data = indata.copy()
                self.last_block = data

                try:
                    self.queue.put_nowait(data)
                except queue.Full:
                    pass  # Drop frame if queue full

            self.stream = sd.InputStream(
                device=self.device,
                channels=self.channels,
                samplerate=self.sample_rate,
                blocksize=self.blocksize,
                callback=callback
            )
            self.stream.start()
            log(f"sounddevice stream started successfully", "INFO")

        except Exception as e:
            log(f"Error starting sounddevice: {e}", "ERROR")
            self.running = False

    def _start_loopback(self):
        """Start soundcard loopback capture"""
        import threading

        def loopback_thread():
            try:
                # Get default speaker
                spk = sc.default_speaker()
                log(f"Using speaker: {spk.name}, channels: {spk.channels}", "INFO")

                with spk.recorder(samplerate=self.sample_rate, channels=self.channels, blocksize=self.blocksize) as rec:
                    while self.running:
                        data = rec.record(numframes=self.blocksize)
                        self.last_block = data.copy()

                        try:
                            self.queue.put_nowait(data.copy())
                        except queue.Full:
                            pass  # Drop frame if queue full

            except Exception as e:
                log(f"Error in loopback thread: {e}", "ERROR")
                self.running = False

        thread = threading.Thread(target=loopback_thread, daemon=True)
        thread.start()

    def stop(self):
        """Stop audio capture"""
        if not self.running:
            return

        log("Stopping AudioEngine", "INFO")
        self.running = False

        if self.stream is not None:
            try:
                self.stream.stop()
                self.stream.close()
                self.stream = None
            except Exception as e:
                log(f"Error stopping stream: {e}", "ERROR")

    def read_block(self, timeout=0.0):
        """Read audio block from queue"""
        try:
            return self.queue.get(timeout=timeout)
        except queue.Empty:
            return None


# ============================================================================
# RADAR WIDGET
# ============================================================================

class RadarWidget(pg.PlotWidget):
    """
    Radar visualization using pyqtgraph
    Shows 360° sweep and target position
    """

    def __init__(self):
        super().__init__()
        log("RadarWidget.__init__", "INFO")

        self.setBackground("#050505")
        self.setAspectLocked(True)
        self.setXRange(-110, 110)
        self.setYRange(-110, 110)
        self.showGrid(x=True, y=True, alpha=0.25)
        self.setMouseEnabled(False, False)

        # Draw circles for distance rings
        self.circles = []
        for radius in [25, 50, 75, 100]:
            circle = pg.QtWidgets.QGraphicsEllipseItem(-radius, -radius, radius * 2, radius * 2)
            circle.setPen(pg.mkPen(color=(0, 100, 200), width=1))
            self.addItem(circle)
            self.circles.append(circle)

        # Draw radial lines every 45 degrees
        self.radials = []
        for angle_deg in range(0, 360, 45):
            angle_rad = math.radians(angle_deg)
            x = 100 * math.cos(angle_rad)
            y = 100 * math.sin(angle_rad)
            line = pg.PlotDataItem([0, x], [0, y], pen=pg.mkPen(color=(0, 100, 200), width=1))
            self.addItem(line)
            self.radials.append(line)

        # Add distance labels
        self.distance_texts = []
        for radius in [25, 50, 75]:
            text = pg.TextItem(f"{radius}m", color=(100, 150, 255), anchor=(0.5, 0.5))
            text.setPos(0, radius)
            self.addItem(text)
            self.distance_texts.append(text)

        # Sweep line (rotating green line)
        self.sweep_line = pg.PlotDataItem([0, 0], [0, 100], pen=pg.mkPen(color=(0, 255, 0), width=2))
        self.addItem(self.sweep_line)
        self.sweep_angle = 0

        # Target echo (red dot)
        self.echo = pg.ScatterPlotItem(size=15, brush=pg.mkBrush(255, 0, 0, 200))
        self.addItem(self.echo)
        self.target_pos = None

    def update_sweep(self, angle_deg):
        """Update sweep line angle"""
        self.sweep_angle = angle_deg
        angle_rad = math.radians(angle_deg - 90)  # -90 to make 0° point up
        x = 100 * math.cos(angle_rad)
        y = 100 * math.sin(angle_rad)
        self.sweep_line.setData([0, x], [0, y])

    def update_target(self, angle_deg, distance):
        """Update target position"""
        if angle_deg is None or distance is None:
            self.echo.setData([], [])
            self.target_pos = None
            return

        # Clamp distance
        distance = max(5, min(100, distance))

        # Calculate position
        angle_rad = math.radians(angle_deg - 90)  # -90 to make 0° point up
        x = distance * math.cos(angle_rad)
        y = distance * math.sin(angle_rad)

        self.echo.setData([x], [y])
        self.target_pos = (x, y)


# ============================================================================
# SPECTRUM WIDGET
# ============================================================================

class SpectrumWidget(pg.PlotWidget):
    """
    Real-time FFT spectrum analyzer
    """

    def __init__(self):
        super().__init__()
        log("SpectrumWidget.__init__", "INFO")

        self.setBackground("#050505")
        self.setLabel('left', 'Power', units='dB')
        self.setLabel('bottom', 'Frequency', units='Hz')
        self.setXRange(20, 10000, padding=0)
        self.setYRange(-80, 0, padding=0)
        self.showGrid(x=True, y=True, alpha=0.25)

        # Current spectrum (green)
        self.spectrum_curve = self.plot(pen=pg.mkPen(color=(0, 255, 0), width=2))

        # Averaged spectrum (yellow)
        self.avg_curve = self.plot(pen=pg.mkPen(color=(255, 255, 0), width=1))

        self.freqs = None
        self.avg_buffer = []
        self.avg_size = 30

    def update_fft(self, data):
        """Update spectrum from audio data"""
        try:
            # Convert to mono
            if data.ndim == 2:
                mono = np.mean(data, axis=1)
            else:
                mono = data.ravel()

            # Apply Hanning window
            window = np.hanning(len(mono))
            windowed = mono * window

            # Compute FFT
            fft_data = np.fft.rfft(windowed)
            freqs = np.fft.rfftfreq(len(mono), d=1.0/48000)

            # Power spectrum in dB
            power = 20 * np.log10(np.abs(fft_data) + 1e-10)

            # Update curves
            self.spectrum_curve.setData(freqs, power)

            # Update average
            self.avg_buffer.append(power)
            if len(self.avg_buffer) > self.avg_size:
                self.avg_buffer.pop(0)

            avg_power = np.mean(self.avg_buffer, axis=0)
            self.avg_curve.setData(freqs, avg_power)

        except Exception as e:
            log(f"Error in update_fft: {e}", "ERROR")


# ============================================================================
# WATERFALL WIDGET
# ============================================================================

class WaterfallWidget(pg.PlotWidget):
    """
    Waterfall display (spectrogram over time)
    """

    def __init__(self):
        super().__init__()
        log("WaterfallWidget.__init__", "INFO")

        self.setBackground("#050505")
        self.setLabel('left', 'Time')
        self.setLabel('bottom', 'Frequency', units='Hz')

        # Image item for waterfall
        self.img = pg.ImageItem()
        self.addItem(self.img)

        # Colormap
        colormap = pg.colormap.get('viridis')
        self.img.setLookupTable(colormap.getLookupTable())

        self.data = np.zeros((100, 512))  # 100 time steps, 512 freq bins
        self.row_idx = 0

    def push_row(self, row):
        """Add new row to waterfall (scrolling down)"""
        try:
            # Roll data down
            self.data = np.roll(self.data, 1, axis=0)

            # Add new row at top
            if len(row) != self.data.shape[1]:
                # Resample row to match
                row = np.interp(
                    np.linspace(0, len(row), self.data.shape[1]),
                    np.arange(len(row)),
                    row
                )

            self.data[0, :] = row

            # Update image
            self.img.setImage(self.data.T, autoLevels=False, levels=(-80, 0))

        except Exception as e:
            log(f"Error in push_row: {e}", "ERROR")


# ============================================================================
# DEVICE PANEL
# ============================================================================

class DevicePanel(QWidget):
    """
    Device selection and configuration panel
    """

    def __init__(self, audio_engine):
        super().__init__()
        self.audio = audio_engine
        log("DevicePanel.__init__", "INFO")

        layout = QVBoxLayout()

        # Device selection
        device_group = QGroupBox("Audio Device")
        device_layout = QVBoxLayout()

        self.device_combo = QComboBox()
        device_layout.addWidget(QLabel("Select Device:"))
        device_layout.addWidget(self.device_combo)

        refresh_btn = QPushButton("Refresh Devices")
        refresh_btn.clicked.connect(self.refresh_devices)
        device_layout.addWidget(refresh_btn)

        device_group.setLayout(device_layout)
        layout.addWidget(device_group)

        # Audio settings
        settings_group = QGroupBox("Audio Settings")
        settings_layout = QFormLayout()

        self.samplerate_combo = QComboBox()
        self.samplerate_combo.addItems(['44100', '48000', '96000'])
        self.samplerate_combo.setCurrentText('48000')
        settings_layout.addRow("Sample Rate:", self.samplerate_combo)

        self.blocksize_combo = QComboBox()
        self.blocksize_combo.addItems(['512', '1024', '2048', '4096'])
        self.blocksize_combo.setCurrentText('2048')
        settings_layout.addRow("Block Size:", self.blocksize_combo)

        self.channels_combo = QComboBox()
        self.channels_combo.addItems(['1', '2', '6', '8'])
        self.channels_combo.setCurrentText('2')
        settings_layout.addRow("Channels:", self.channels_combo)

        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)

        # Mode selection
        mode_group = QGroupBox("Mode")
        mode_layout = QVBoxLayout()

        self.test_mode = QCheckBox("Synthetic Test Mode")
        mode_layout.addWidget(self.test_mode)

        self.loopback_mode = QCheckBox("Loopback (soundcard)")
        self.loopback_mode.toggled.connect(self.on_loopback_toggled)
        mode_layout.addWidget(self.loopback_mode)

        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)

        # Profile presets
        preset_group = QGroupBox("Presets")
        preset_layout = QVBoxLayout()

        sb_btn = QPushButton("SB Z SE + Cloud II")
        sb_btn.clicked.connect(self.apply_sb_preset)
        preset_layout.addWidget(sb_btn)

        preset_group.setLayout(preset_layout)
        layout.addWidget(preset_group)

        # Status
        status_group = QGroupBox("Status")
        status_layout = QVBoxLayout()

        self.rms_label = QLabel("RMS: --- dBFS")
        status_layout.addWidget(self.rms_label)

        self.backend_label = QLabel("Backend: sounddevice")
        status_layout.addWidget(self.backend_label)

        status_group.setLayout(status_layout)
        layout.addWidget(status_group)

        layout.addStretch()
        self.setLayout(layout)

        # Initial refresh
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

        # Get selected device
        dev_data = self.device_combo.currentData()
        if dev_data:
            if dev_data['backend'] == 'sounddevice':
                self.audio.device = dev_data['index']
                self.audio.use_loopback = False
                self.backend_label.setText("Backend: sounddevice")
            else:
                self.audio.use_loopback = True
                self.backend_label.setText("Backend: soundcard (loopback)")

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
            self.backend_label.setText("Backend: soundcard (loopback)")
        else:
            self.audio.use_loopback = False
            self.backend_label.setText("Backend: sounddevice")


# ============================================================================
# DETECTION PANEL
# ============================================================================

class DetectionPanel(QWidget):
    """
    Sound detection configuration and status
    """

    def __init__(self):
        super().__init__()
        log("DetectionPanel.__init__", "INFO")

        layout = QVBoxLayout()

        # Profile selection
        profile_group = QGroupBox("Detection Profile")
        profile_layout = QVBoxLayout()

        self.profile_combo = QComboBox()
        self.profile_combo.addItems([
            'Universal',
            'ARC Raiders (PC)',
            'ARC Raiders + SB Z SE + Cloud II'
        ])
        self.profile_combo.setCurrentText('ARC Raiders + SB Z SE + Cloud II')
        profile_layout.addWidget(self.profile_combo)

        profile_group.setLayout(profile_layout)
        layout.addWidget(profile_group)

        # Detection enables
        enable_group = QGroupBox("Enable Detection")
        enable_layout = QVBoxLayout()

        self.walk_enable = QCheckBox("Detect WALK")
        self.walk_enable.setChecked(True)
        enable_layout.addWidget(self.walk_enable)

        self.run_enable = QCheckBox("Detect RUN")
        self.run_enable.setChecked(True)
        enable_layout.addWidget(self.run_enable)

        self.shot_enable = QCheckBox("Detect SHOT")
        self.shot_enable.setChecked(True)
        enable_layout.addWidget(self.shot_enable)

        enable_group.setLayout(enable_layout)
        layout.addWidget(enable_group)

        # Sensitivity sliders
        sens_group = QGroupBox("Sensitivity")
        sens_layout = QVBoxLayout()

        # Walk sensitivity
        walk_layout = QHBoxLayout()
        walk_layout.addWidget(QLabel("Walk:"))
        self.walk_sens = QSlider(Qt.Horizontal)
        self.walk_sens.setRange(1, 100)
        self.walk_sens.setValue(55)
        walk_layout.addWidget(self.walk_sens)
        self.walk_sens_label = QLabel("55")
        self.walk_sens.valueChanged.connect(lambda v: self.walk_sens_label.setText(str(v)))
        walk_layout.addWidget(self.walk_sens_label)
        sens_layout.addLayout(walk_layout)

        # Run sensitivity
        run_layout = QHBoxLayout()
        run_layout.addWidget(QLabel("Run:"))
        self.run_sens = QSlider(Qt.Horizontal)
        self.run_sens.setRange(1, 100)
        self.run_sens.setValue(55)
        run_layout.addWidget(self.run_sens)
        self.run_sens_label = QLabel("55")
        self.run_sens.valueChanged.connect(lambda v: self.run_sens_label.setText(str(v)))
        run_layout.addWidget(self.run_sens_label)
        sens_layout.addLayout(run_layout)

        # Shot sensitivity
        shot_layout = QHBoxLayout()
        shot_layout.addWidget(QLabel("Shot:"))
        self.shot_sens = QSlider(Qt.Horizontal)
        self.shot_sens.setRange(1, 100)
        self.shot_sens.setValue(65)
        shot_layout.addWidget(self.shot_sens)
        self.shot_sens_label = QLabel("65")
        self.shot_sens.valueChanged.connect(lambda v: self.shot_sens_label.setText(str(v)))
        shot_layout.addWidget(self.shot_sens_label)
        sens_layout.addLayout(shot_layout)

        sens_group.setLayout(sens_layout)
        layout.addWidget(sens_group)

        # Detection status labels
        status_group = QGroupBox("Detection Status")
        status_layout = QVBoxLayout()

        self.walk_label = QLabel("WALK: —")
        self.walk_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        status_layout.addWidget(self.walk_label)

        self.run_label = QLabel("RUN: —")
        self.run_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        status_layout.addWidget(self.run_label)

        self.shot_label = QLabel("SHOT: —")
        self.shot_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        status_layout.addWidget(self.shot_label)

        status_group.setLayout(status_layout)
        layout.addWidget(status_group)

        layout.addStretch()
        self.setLayout(layout)

        # Hold counters for labels
        self.walk_hold = 0
        self.run_hold = 0
        self.shot_hold = 0

    def analyze(self, block, sample_rate):
        """
        Analyze audio block for walk/run/shot detection
        Returns: (events_dict, bands_dict)
        """
        try:
            # Convert to mono
            if block.ndim == 2:
                mono = np.mean(block, axis=1)
            else:
                mono = block.ravel()

            # Apply Hanning window
            window = np.hanning(len(mono))
            windowed = mono * window

            # FFT
            fft_data = np.fft.rfft(windowed)
            freqs = np.fft.rfftfreq(len(mono), d=1.0/sample_rate)
            power = np.abs(fft_data)

            # Band separation
            # Walk: 20-200 Hz (low frequency footsteps)
            # Run: 200-1500 Hz (mid frequency, faster steps)
            # Shot: 1500-6000 Hz (high frequency, sharp transients)

            low_mask = (freqs >= 20) & (freqs < 200)
            mid_mask = (freqs >= 200) & (freqs < 1500)
            high_mask = (freqs >= 1500) & (freqs < 6000)

            low_power = power[low_mask]
            mid_power = power[mid_mask]
            high_power = power[high_mask]

            total_power = np.mean(power) + 1e-9

            # Ratios
            low_r = np.mean(low_power) / total_power if len(low_power) > 0 else 0.0
            mid_r = np.mean(mid_power) / total_power if len(mid_power) > 0 else 0.0
            high_r = np.max(high_power) / total_power if len(high_power) > 0 else 0.0

            # Band intensity with sensitivity
            walk_i = self.band_intensity(low_r, 0.08, self.walk_sens.value() / 100.0)
            run_i = self.band_intensity(mid_r, 0.06, self.run_sens.value() / 100.0)
            shot_i = self.band_intensity(high_r, 0.12, self.shot_sens.value() / 100.0)

            # Detection flags
            walk_det = walk_i > 0.0 and self.walk_enable.isChecked()
            run_det = run_i > 0.0 and self.run_enable.isChecked()
            shot_det = shot_i > 0.0 and self.shot_enable.isChecked()

            # Update labels with hold
            if walk_det:
                self.walk_hold = 6
            if run_det:
                self.run_hold = 6
            if shot_det:
                self.shot_hold = 6

            # Decrement hold counters
            if self.walk_hold > 0:
                self.walk_hold -= 1
                self.walk_label.setText("WALK: DETECTED")
                self.walk_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #00FF00;")
            else:
                self.walk_label.setText("WALK: —")
                self.walk_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #666666;")

            if self.run_hold > 0:
                self.run_hold -= 1
                self.run_label.setText("RUN: DETECTED")
                self.run_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #FFA500;")
            else:
                self.run_label.setText("RUN: —")
                self.run_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #666666;")

            if self.shot_hold > 0:
                self.shot_hold -= 1
                self.shot_label.setText("SHOT: DETECTED")
                self.shot_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #FF0000;")
            else:
                self.shot_label.setText("SHOT: —")
                self.shot_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #666666;")

            events = {
                'walk': walk_det,
                'run': run_det,
                'shot': shot_det,
                'walk_int': walk_i,
                'run_int': run_i,
                'shot_int': shot_i
            }

            bands = {
                'low_r': low_r,
                'mid_r': mid_r,
                'high_r': high_r
            }

            return events, bands

        except Exception as e:
            log(f"Error in analyze: {e}", "ERROR")
            return {'walk': False, 'run': False, 'shot': False}, {}

    def band_intensity(self, ratio, base, sens):
        """
        Calculate band intensity with sensitivity threshold
        sens: 0.0-1.0 (from slider /100)
        """
        thr = base * (1.4 - sens)
        thr = max(0.02, min(0.6, thr))

        if ratio <= thr:
            return 0.0

        return min(1.0, (ratio - thr) / (1.0 - thr))


# ============================================================================
# LED EDGE ALERT WIDGET
# ============================================================================

class LedOverlayWidget(QWidget):
    """
    LED Edge Alert - colored bars on screen edges
    """

    def __init__(self):
        super().__init__()
        log("LedOverlayWidget.__init__", "INFO")

        self.setMinimumHeight(100)

        # Bar states: G1-G3 (top), D1-D3 (bottom), L1-L2 (left), P1-P2 (right)
        self.bars = {
            'G1': {'color': QColor(0, 0, 0), 'intensity': 0.0},
            'G2': {'color': QColor(0, 0, 0), 'intensity': 0.0},
            'G3': {'color': QColor(0, 0, 0), 'intensity': 0.0},
            'D1': {'color': QColor(0, 0, 0), 'intensity': 0.0},
            'D2': {'color': QColor(0, 0, 0), 'intensity': 0.0},
            'D3': {'color': QColor(0, 0, 0), 'intensity': 0.0},
            'L1': {'color': QColor(0, 0, 0), 'intensity': 0.0},
            'L2': {'color': QColor(0, 0, 0), 'intensity': 0.0},
            'P1': {'color': QColor(0, 0, 0), 'intensity': 0.0},
            'P2': {'color': QColor(0, 0, 0), 'intensity': 0.0},
        }

        self.global_alpha = 0.8

        # Decay timer
        self.timer = QTimer()
        self.timer.timeout.connect(self._tick)
        self.timer.start(50)  # 50ms = 20Hz

    def _tick(self):
        """Decay bar intensities"""
        for bar in self.bars.values():
            bar['intensity'] -= 0.08
            bar['intensity'] = max(0.0, bar['intensity'])

        self.update()

    def update_from_events(self, events, bands, energy, balance):
        """
        Update LED bars based on detection events

        events: dict with walk/run/shot flags and intensities
        bands: dict with low_r/mid_r/high_r
        energy: total energy (for radar)
        balance: L/R balance (-1 to 1)
        """
        walk = events.get('walk', False)
        run = events.get('run', False)
        shot = events.get('shot', False)

        walk_i = events.get('walk_int', 0.0)
        run_i = events.get('run_int', 0.0)
        shot_i = events.get('shot_int', 0.0)

        # Determine side based on balance
        if balance < -0.2:
            side = 'left'
        elif balance > 0.2:
            side = 'right'
        else:
            side = 'center'

        # Map to bars
        if side == 'left':
            side_bars = ['L1', 'L2']
            flank_bars = ['G1', 'D1']
        elif side == 'right':
            side_bars = ['P1', 'P2']
            flank_bars = ['G3', 'D3']
        else:
            side_bars = ['G2', 'D2']
            flank_bars = ['G1', 'G3', 'D1', 'D3']

        # Walk/Run - green to yellow to red gradient
        if walk or run:
            strength = max(walk_i, run_i)
            color = self._walk_run_color(strength)

            for bar_name in side_bars + flank_bars:
                self.bars[bar_name]['color'] = color
                self.bars[bar_name]['intensity'] = min(1.0, self.bars[bar_name]['intensity'] + 0.3)

        # Shot - blue, overrides walk/run
        if shot:
            shot_color = QColor(80, 160, 255)

            for bar_name in side_bars + flank_bars:
                self.bars[bar_name]['color'] = shot_color
                self.bars[bar_name]['intensity'] = min(1.0, self.bars[bar_name]['intensity'] + 0.5)

    def _walk_run_color(self, strength):
        """Generate color gradient for walk/run (green -> yellow -> red)"""
        # strength 0.0-1.0
        if strength < 0.5:
            # Green to Yellow
            r = int(255 * (strength * 2))
            g = 255
            b = 0
        else:
            # Yellow to Red
            r = 255
            g = int(255 * (1.0 - (strength - 0.5) * 2))
            b = 0

        return QColor(r, g, b)

    def paintEvent(self, event):
        """Draw LED bars"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()

        bar_thickness = 20

        # Top bars (G1, G2, G3)
        self._draw_bar(painter, 0, 0, width // 3, bar_thickness, self.bars['G1'])
        self._draw_bar(painter, width // 3, 0, width // 3, bar_thickness, self.bars['G2'])
        self._draw_bar(painter, 2 * width // 3, 0, width // 3, bar_thickness, self.bars['G3'])

        # Bottom bars (D1, D2, D3)
        self._draw_bar(painter, 0, height - bar_thickness, width // 3, bar_thickness, self.bars['D1'])
        self._draw_bar(painter, width // 3, height - bar_thickness, width // 3, bar_thickness, self.bars['D2'])
        self._draw_bar(painter, 2 * width // 3, height - bar_thickness, width // 3, bar_thickness, self.bars['D3'])

        # Left bars (L1, L2)
        mid_height = (height - 2 * bar_thickness) // 2
        self._draw_bar(painter, 0, bar_thickness, bar_thickness, mid_height, self.bars['L1'])
        self._draw_bar(painter, 0, bar_thickness + mid_height, bar_thickness, mid_height, self.bars['L2'])

        # Right bars (P1, P2)
        self._draw_bar(painter, width - bar_thickness, bar_thickness, bar_thickness, mid_height, self.bars['P1'])
        self._draw_bar(painter, width - bar_thickness, bar_thickness + mid_height, bar_thickness, mid_height, self.bars['P2'])

    def _draw_bar(self, painter, x, y, w, h, bar_data):
        """Draw single LED bar"""
        if bar_data['intensity'] <= 0:
            return

        color = bar_data['color']
        alpha = int(255 * bar_data['intensity'] * self.global_alpha)
        color.setAlpha(alpha)

        painter.fillRect(x, y, w, h, color)


# ============================================================================
# MAIN WINDOW
# ============================================================================

class MainWindow(QMainWindow):
    """
    Main application window with docked panels
    """

    def __init__(self):
        super().__init__()
        log("MainWindow.__init__", "INFO")

        self.setWindowTitle("RadarSuite Final v2.3.0")
        self.setGeometry(100, 100, 1400, 900)

        # Audio engine
        self.audio = AudioEngine()

        # Running state
        self.is_running = False

        # Radar sweep angle
        self.radar_angle = 0.0

        # Test signal phase
        self.test_phase = 0.0

        # Create UI
        self.create_ui()

        # Main timer (50ms = 20Hz)
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(50)

    def create_ui(self):
        """Create main UI with docks"""
        # Central widget - tabs for spectrum/waterfall
        central = QTabWidget()

        self.spectrum = SpectrumWidget()
        central.addTab(self.spectrum, "Spectrum")

        self.waterfall = WaterfallWidget()
        central.addTab(self.waterfall, "Waterfall")

        self.setCentralWidget(central)

        # Radar dock (top)
        radar_dock = QDockWidget("Radar", self)
        self.radar = RadarWidget()
        radar_dock.setWidget(self.radar)
        self.addDockWidget(Qt.TopDockWidgetArea, radar_dock)

        # Device panel dock (left)
        device_dock = QDockWidget("Device & Settings", self)
        self.dev_panel = DevicePanel(self.audio)
        device_dock.setWidget(self.dev_panel)
        self.addDockWidget(Qt.LeftDockWidgetArea, device_dock)

        # Detection panel dock (right)
        detection_dock = QDockWidget("Detection", self)
        self.det_panel = DetectionPanel()
        detection_dock.setWidget(self.det_panel)
        self.addDockWidget(Qt.RightDockWidgetArea, detection_dock)

        # LED overlay dock (bottom)
        led_dock = QDockWidget("LED Edge Alert", self)
        self.led_overlay = LedOverlayWidget()
        led_dock.setWidget(self.led_overlay)
        self.addDockWidget(Qt.BottomDockWidgetArea, led_dock)

        # Toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.toggle_start_stop)
        toolbar.addWidget(self.start_btn)

        toolbar.addSeparator()

        toolbar.addWidget(QLabel("Radar Alpha:"))
        self.radar_alpha = QSlider(Qt.Horizontal)
        self.radar_alpha.setRange(0, 100)
        self.radar_alpha.setValue(80)
        self.radar_alpha.setMaximumWidth(150)
        toolbar.addWidget(self.radar_alpha)

        toolbar.addWidget(QLabel("LED Alpha:"))
        self.led_alpha = QSlider(Qt.Horizontal)
        self.led_alpha.setRange(0, 100)
        self.led_alpha.setValue(80)
        self.led_alpha.setMaximumWidth(150)
        self.led_alpha.valueChanged.connect(lambda v: setattr(self.led_overlay, 'global_alpha', v / 100.0))
        toolbar.addWidget(self.led_alpha)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def toggle_start_stop(self):
        """Toggle audio capture"""
        if not self.is_running:
            self.start()
        else:
            self.stop()

    def start(self):
        """Start audio capture"""
        log("Starting audio capture", "INFO")

        # Apply settings
        self.dev_panel.apply_settings()

        # Start audio
        self.audio.start()

        self.is_running = True
        self.start_btn.setText("Stop")
        self.status_bar.showMessage("Running")

    def stop(self):
        """Stop audio capture"""
        log("Stopping audio capture", "INFO")

        self.audio.stop()

        self.is_running = False
        self.start_btn.setText("Start")
        self.status_bar.showMessage("Stopped")

    def tick(self):
        """Main update loop (called every 50ms)"""
        # 1. Update radar sweep
        self.radar_angle = (self.radar_angle + 4.0) % 360.0
        self.radar.update_sweep(self.radar_angle)

        # 2. Get audio block
        if self.dev_panel.test_mode.isChecked():
            block = self.generate_test_block()
        else:
            block = self.audio.read_block(0.0) or self.audio.last_block

        if block is None:
            return

        # 3. Update spectrum and waterfall
        self.spectrum.update_fft(block)

        # For waterfall, extract power spectrum
        if block.ndim == 2:
            mono = np.mean(block, axis=1)
        else:
            mono = block.ravel()

        fft_data = np.fft.rfft(mono * np.hanning(len(mono)))
        power = 20 * np.log10(np.abs(fft_data) + 1e-10)
        self.waterfall.push_row(power)

        # 4. Compute energy and balance
        energy, balance = self.compute_orientation(block)

        # Update RMS label
        if energy > 0:
            rms_db = 20 * np.log10(energy)
            self.dev_panel.rms_label.setText(f"RMS: {rms_db:.1f} dBFS")

        # 5. Update radar target
        if energy > 0.0003:
            # Pseudo angle from balance
            angle = 90.0 + balance * 75.0  # -75 to +75 from north

            # Pseudo distance from energy
            distance = min(100.0, max(10.0, energy * 4000.0))

            self.radar.update_target(angle, distance)
        else:
            self.radar.update_target(None, None)

        # 6. Detection
        events, bands = self.det_panel.analyze(block, self.audio.sample_rate)

        # 7. Update LED overlay
        self.led_overlay.update_from_events(events, bands, energy, balance)

        # 8. Status bar alert for shots
        if events.get('shot', False):
            self.status_bar.showMessage("ALERT: SHOT detected", 800)

    def compute_orientation(self, block):
        """
        Compute energy and L/R balance from audio block
        Returns: (energy, balance)
        """
        try:
            if block.ndim == 2 and block.shape[1] >= 2:
                left = block[:, 0]
                right = block[:, 1]

                rms_L = np.sqrt(np.mean(left ** 2))
                rms_R = np.sqrt(np.mean(right ** 2))

                energy = (rms_L + rms_R) / 2.0

                # Balance: -1 (left) to +1 (right)
                balance = (rms_R - rms_L) / (rms_R + rms_L + 1e-9)

                return energy, balance
            else:
                # Mono
                energy = np.sqrt(np.mean(block ** 2))
                return energy, 0.0

        except Exception as e:
            log(f"Error in compute_orientation: {e}", "ERROR")
            return 0.0, 0.0

    def generate_test_block(self):
        """Generate synthetic test audio (walk/run/shot)"""
        duration = self.audio.blocksize / self.audio.sample_rate
        t = np.linspace(self.test_phase, self.test_phase + duration, self.audio.blocksize)
        self.test_phase += duration

        # Mix of frequencies
        # Walk: 80 Hz
        # Run: 420 Hz
        # Shot: 2200 Hz (short bursts)

        walk = 0.1 * np.sin(2 * np.pi * 80 * t)
        run = 0.15 * np.sin(2 * np.pi * 420 * t)

        # Shot burst every ~2 seconds
        shot = np.zeros_like(t)
        if int(self.test_phase) % 2 == 0 and (self.test_phase % 2) < 0.1:
            shot = 0.3 * np.sin(2 * np.pi * 2200 * t)

        # Mix
        mono = walk + run + shot

        # Create stereo with slight difference (for direction test)
        left = mono * 0.9
        right = mono * 1.1

        stereo = np.column_stack([left, right]).astype(np.float32)

        return stereo

    def closeEvent(self, event):
        """Handle window close"""
        log("Application closing", "INFO")
        self.stop()
        event.accept()


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """Main entry point"""
    log("=" * 80, "INFO")
    log("RadarSuite Final v2.3.0 - Starting", "INFO")
    log("=" * 80, "INFO")

    log(f"Python: {sys.version}", "INFO")
    log(f"NumPy: {np.__version__}", "INFO")
    log(f"pyqtgraph: {pg.__version__}", "INFO")
    log(f"sounddevice available: {sd is not None}", "INFO")
    log(f"soundcard available: {sc is not None}", "INFO")

    app = QApplication(sys.argv)
    app.setApplicationName("RadarSuite Final")
    app.setOrganizationName("RadarSuite")

    # Apply dark theme
    apply_dark_theme(app)

    # Create and show main window
    window = MainWindow()
    window.show()

    log("Main window shown, entering event loop", "INFO")

    # Run event loop
    exit_code = app.exec_()

    log(f"Application exited with code: {exit_code}", "INFO")
    log("=" * 80, "INFO")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
