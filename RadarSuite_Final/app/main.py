"""
RadarSuite Final v3.0.0-Claude-001
Advanced audio radar and detection system for gaming with AI-powered human detection
Supports: sounddevice, soundcard loopback, pyqtgraph visualization
Optimized for: ARC Raiders + Sound Blaster Z SE + HyperX Cloud II

NEW IN v3.0.0-Claude-001 - "Human Hunter":
✨ HUMAN FOOTSTEP PATTERN RECOGNITION ✨
- Temporal cadence analysis (detects human walking rhythm 1.5-2.5 steps/s, running 3-4.5 steps/s)
- L-R pattern detection (left-right-left-right foot classification)
- Weight distribution analysis (stereo channel analysis)
- Surface type detection (hard/medium/soft based on frequency signatures)
- Distance estimation (based on audio loudness)
- Confidence scoring (0-100% based on pattern regularity)
- Real-time gait classification (walk vs run vs unknown)

Previous features:
- Complete translation system EN/PL
- Radar target clearing on detection events only
- Independent Radar and LED windows
- Independent opacity controls
- Frameless window mode
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
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QPalette

# ============================================================================
# VERSION
# ============================================================================

VERSION = "v3.0.0-Claude-001"

# ============================================================================
# TRANSLATIONS
# ============================================================================

TRANSLATIONS = {
    'en': {
        'app_title': 'RadarSuite Final',
        'radar': 'Radar',
        'spectrum': 'Spectrum',
        'waterfall': 'Waterfall',
        'device_settings': 'Device & Settings',
        'detection': 'Detection',
        'led_alert': 'LED Edge Alert',
        'start': 'Start',
        'stop': 'Stop',
        'radar_alpha': 'Radar Alpha:',
        'led_alpha': 'LED Alpha:',
        'detach_radar': 'Detach Radar',
        'detach_led': 'Detach LED',
        'frameless_mode': 'Frameless Mode',
        'audio_device': 'Audio Device',
        'select_device': 'Select Device:',
        'refresh_devices': 'Refresh Devices',
        'audio_settings': 'Audio Settings',
        'sample_rate': 'Sample Rate:',
        'block_size': 'Block Size:',
        'channels': 'Channels:',
        'mode': 'Mode',
        'test_mode': 'Synthetic Test Mode',
        'loopback_mode': 'Loopback (soundcard)',
        'presets': 'Presets',
        'sb_preset': 'SB Z SE + Cloud II',
        'status': 'Status',
        'rms': 'RMS:',
        'backend': 'Backend:',
        'detection_profile': 'Detection Profile',
        'enable_detection': 'Enable Detection',
        'detect_walk': 'Detect WALK',
        'detect_run': 'Detect RUN',
        'detect_shot': 'Detect SHOT',
        'sensitivity': 'Sensitivity',
        'walk': 'Walk:',
        'run': 'Run:',
        'shot': 'Shot:',
        'detection_status': 'Detection Status',
        'walk_detected': 'WALK: DETECTED',
        'run_detected': 'RUN: DETECTED',
        'shot_detected': 'SHOT: DETECTED',
        'walk_none': 'WALK: —',
        'run_none': 'RUN: —',
        'shot_none': 'SHOT: —',
        'ready': 'Ready',
        'running': 'Running',
        'stopped': 'Stopped',
        'language': 'Language:',
    },
    'pl': {
        'app_title': 'RadarSuite Final',
        'radar': 'Radar',
        'spectrum': 'Widmo',
        'waterfall': 'Wodospad',
        'device_settings': 'Urządzenie i Ustawienia',
        'detection': 'Detekcja',
        'led_alert': 'Alarm LED',
        'start': 'Start',
        'stop': 'Stop',
        'radar_alpha': 'Przezroczystość Radaru:',
        'led_alpha': 'Przezroczystość LED:',
        'detach_radar': 'Odłącz Radar',
        'detach_led': 'Odłącz LED',
        'frameless_mode': 'Tryb Bez Ramek',
        'audio_device': 'Urządzenie Audio',
        'select_device': 'Wybierz Urządzenie:',
        'refresh_devices': 'Odśwież Urządzenia',
        'audio_settings': 'Ustawienia Audio',
        'sample_rate': 'Częstotliwość Próbkowania:',
        'block_size': 'Rozmiar Bloku:',
        'channels': 'Kanały:',
        'mode': 'Tryb',
        'test_mode': 'Tryb Testowy (Syntetyczny)',
        'loopback_mode': 'Loopback (karta dźwiękowa)',
        'presets': 'Presety',
        'sb_preset': 'SB Z SE + Cloud II',
        'status': 'Status',
        'rms': 'RMS:',
        'backend': 'Backend:',
        'detection_profile': 'Profil Detekcji',
        'enable_detection': 'Włącz Detekcję',
        'detect_walk': 'Wykrywaj CHÓD',
        'detect_run': 'Wykrywaj BIEG',
        'detect_shot': 'Wykrywaj STRZAŁY',
        'sensitivity': 'Czułość',
        'walk': 'Chód:',
        'run': 'Bieg:',
        'shot': 'Strzały:',
        'detection_status': 'Status Detekcji',
        'walk_detected': 'CHÓD: WYKRYTO',
        'run_detected': 'BIEG: WYKRYTO',
        'shot_detected': 'STRZAŁ: WYKRYTO',
        'walk_none': 'CHÓD: —',
        'run_none': 'BIEG: —',
        'shot_none': 'STRZAŁ: —',
        'ready': 'Gotowy',
        'running': 'Działa',
        'stopped': 'Zatrzymany',
        'language': 'Język:',
    }
}

current_language = 'en'

def tr(key):
    """Translate key to current language"""
    return TRANSLATIONS.get(current_language, TRANSLATIONS['en']).get(key, key)

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
        QWidget { background-color: #191923; color: #DCDCE6; }
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
        QPushButton:checked { background-color: #2A82DA; }
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
        QLabel { color: #DCDCE6; background: transparent; }
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
        QCheckBox { color: #DCDCE6; }
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
        self.backend = "sounddevice"
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
                    pass

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
                spk = sc.default_speaker()
                log(f"Using speaker: {spk.name}, channels: {spk.channels}", "INFO")

                with spk.recorder(samplerate=self.sample_rate, channels=self.channels, blocksize=self.blocksize) as rec:
                    while self.running:
                        data = rec.record(numframes=self.blocksize)
                        self.last_block = data.copy()

                        try:
                            self.queue.put_nowait(data.copy())
                        except queue.Full:
                            pass

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
# DETACHABLE RADAR WIDGET
# ============================================================================

class DetachableRadarWidget(QWidget):
    """
    Independent radar widget that can be detached from main window
    Works even when main window is minimized
    """

    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window | Qt.WindowStaysOnTopHint)
        log("DetachableRadarWidget.__init__", "INFO")

        self.setWindowTitle(f"{tr('radar')} - RadarSuite {VERSION}")
        self.setGeometry(100, 100, 500, 500)

        # Frameless mode
        self.is_frameless = False

        # Opacity
        self.window_opacity = 1.0
        self.setWindowOpacity(self.window_opacity)

        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Radar plot
        self.radar = RadarWidget()
        layout.addWidget(self.radar)

        self.setLayout(layout)

        # Dragging support for frameless mode
        self.dragging = False
        self.drag_position = QPoint()

    def set_opacity(self, opacity):
        """Set window opacity (0.0 - 1.0)"""
        self.window_opacity = max(0.0, min(1.0, opacity))
        self.setWindowOpacity(self.window_opacity)

    def set_frameless(self, frameless):
        """Toggle frameless window mode"""
        self.is_frameless = frameless

        if frameless:
            self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        else:
            self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

        self.show()

    def mousePressEvent(self, event):
        """Handle mouse press for dragging in frameless mode"""
        if self.is_frameless and event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging"""
        if self.is_frameless and self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if self.is_frameless:
            self.dragging = False
            event.accept()


class RadarWidget(pg.PlotWidget):
    """Radar visualization using pyqtgraph"""

    def __init__(self):
        super().__init__()

        self.setBackground("#050505")
        self.setAspectLocked(True)
        self.setXRange(-110, 110)
        self.setYRange(-110, 110)
        self.showGrid(x=True, y=True, alpha=0.25)
        self.setMouseEnabled(False, False)

        # Circles
        self.circles = []
        for radius in [25, 50, 75, 100]:
            circle = pg.QtWidgets.QGraphicsEllipseItem(-radius, -radius, radius * 2, radius * 2)
            circle.setPen(pg.mkPen(color=(0, 100, 200), width=1))
            self.addItem(circle)
            self.circles.append(circle)

        # Radial lines
        self.radials = []
        for angle_deg in range(0, 360, 45):
            angle_rad = math.radians(angle_deg)
            x = 100 * math.cos(angle_rad)
            y = 100 * math.sin(angle_rad)
            line = pg.PlotDataItem([0, x], [0, y], pen=pg.mkPen(color=(0, 100, 200), width=1))
            self.addItem(line)
            self.radials.append(line)

        # Distance labels
        self.distance_texts = []
        for radius in [25, 50, 75]:
            text = pg.TextItem(f"{radius}m", color=(100, 150, 255), anchor=(0.5, 0.5))
            text.setPos(0, radius)
            self.addItem(text)
            self.distance_texts.append(text)

        # Sweep line
        self.sweep_line = pg.PlotDataItem([0, 0], [0, 100], pen=pg.mkPen(color=(0, 255, 0), width=2))
        self.addItem(self.sweep_line)
        self.sweep_angle = 0

        # Target echo
        self.echo = pg.ScatterPlotItem(size=15, brush=pg.mkBrush(255, 0, 0, 200))
        self.addItem(self.echo)
        self.target_pos = None

    def update_sweep(self, angle_deg):
        """Update sweep line angle"""
        self.sweep_angle = angle_deg
        angle_rad = math.radians(angle_deg - 90)
        x = 100 * math.cos(angle_rad)
        y = 100 * math.sin(angle_rad)
        self.sweep_line.setData([0, x], [0, y])

    def update_target(self, angle_deg, distance):
        """Update target position"""
        if angle_deg is None or distance is None:
            self.echo.setData([], [])
            self.target_pos = None
            return

        distance = max(5, min(100, distance))

        angle_rad = math.radians(angle_deg - 90)
        x = distance * math.cos(angle_rad)
        y = distance * math.sin(angle_rad)

        self.echo.setData([x], [y])
        self.target_pos = (x, y)


# ============================================================================
# DETACHABLE LED WIDGET
# ============================================================================

class DetachableLedWidget(QWidget):
    """
    Independent LED Edge Alert widget
    Works even when main window is minimized
    """

    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window | Qt.WindowStaysOnTopHint)
        log("DetachableLedWidget.__init__", "INFO")

        self.setWindowTitle(f"{tr('led_alert')} - RadarSuite {VERSION}")
        self.setGeometry(100, 600, 800, 150)

        # Frameless mode
        self.is_frameless = False

        # Opacity
        self.window_opacity = 1.0
        self.setWindowOpacity(self.window_opacity)

        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # LED overlay
        self.led_overlay = LedOverlayWidget()
        layout.addWidget(self.led_overlay)

        self.setLayout(layout)

        # Dragging support
        self.dragging = False
        self.drag_position = QPoint()

    def set_opacity(self, opacity):
        """Set window opacity (0.0 - 1.0)"""
        self.window_opacity = max(0.0, min(1.0, opacity))
        self.setWindowOpacity(self.window_opacity)

    def set_frameless(self, frameless):
        """Toggle frameless window mode"""
        self.is_frameless = frameless

        if frameless:
            self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        else:
            self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

        self.show()

    def mousePressEvent(self, event):
        """Handle mouse press for dragging"""
        if self.is_frameless and event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging"""
        if self.is_frameless and self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if self.is_frameless:
            self.dragging = False
            event.accept()


# ============================================================================
# SPECTRUM WIDGET
# ============================================================================

class SpectrumWidget(pg.PlotWidget):
    """Real-time FFT spectrum analyzer"""

    def __init__(self):
        super().__init__()
        log("SpectrumWidget.__init__", "INFO")

        self.setBackground("#050505")
        self.setLabel('left', 'Power', units='dB')
        self.setLabel('bottom', 'Frequency', units='Hz')
        self.setXRange(20, 10000, padding=0)
        self.setYRange(-80, 0, padding=0)
        self.showGrid(x=True, y=True, alpha=0.25)

        self.spectrum_curve = self.plot(pen=pg.mkPen(color=(0, 255, 0), width=2))
        self.avg_curve = self.plot(pen=pg.mkPen(color=(255, 255, 0), width=1))

        self.freqs = None
        self.avg_buffer = []
        self.avg_size = 30

    def update_fft(self, data):
        """Update spectrum from audio data"""
        try:
            if data.ndim == 2:
                mono = np.mean(data, axis=1)
            else:
                mono = data.ravel()

            window = np.hanning(len(mono))
            windowed = mono * window

            fft_data = np.fft.rfft(windowed)
            freqs = np.fft.rfftfreq(len(mono), d=1.0/48000)

            power = 20 * np.log10(np.abs(fft_data) + 1e-10)

            self.spectrum_curve.setData(freqs, power)

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
    """Waterfall display (spectrogram over time)"""

    def __init__(self):
        super().__init__()
        log("WaterfallWidget.__init__", "INFO")

        self.setBackground("#050505")
        self.setLabel('left', 'Time')
        self.setLabel('bottom', 'Frequency', units='Hz')

        self.img = pg.ImageItem()
        self.addItem(self.img)

        colormap = pg.colormap.get('viridis')
        self.img.setLookupTable(colormap.getLookupTable())

        self.data = np.zeros((100, 512))
        self.row_idx = 0

    def push_row(self, row):
        """Add new row to waterfall"""
        try:
            self.data = np.roll(self.data, 1, axis=0)

            if len(row) != self.data.shape[1]:
                row = np.interp(
                    np.linspace(0, len(row), self.data.shape[1]),
                    np.arange(len(row)),
                    row
                )

            self.data[0, :] = row

            self.img.setImage(self.data.T, autoLevels=False, levels=(-80, 0))

        except Exception as e:
            log(f"Error in push_row: {e}", "ERROR")


# ============================================================================
# DEVICE PANEL
# ============================================================================

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

        # Presets
        preset_group = QGroupBox(tr('presets'))
        preset_layout = QVBoxLayout()

        self.sb_btn = QPushButton(tr('sb_preset'))
        self.sb_btn.clicked.connect(self.apply_sb_preset)
        preset_layout.addWidget(self.sb_btn)

        preset_group.setLayout(preset_layout)
        layout.addWidget(preset_group)

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
# HUMAN FOOTSTEP DETECTOR (v3.0)
# ============================================================================

class HumanFootstepDetector:
    """
    Advanced human footstep pattern recognition
    Detects cadence, rhythm, weight distribution, and distinguishes human steps from other sounds
    """

    def __init__(self):
        log("HumanFootstepDetector.__init__", "INFO")

        # Temporal analysis buffers
        self.step_history = []  # timestamps of detected steps
        self.max_history = 20   # keep last 20 steps

        # L-R pattern tracking
        self.lr_pattern = []    # left/right classification history
        self.max_lr_history = 10

        # Surface type detection
        self.surface_type = "unknown"
        self.surface_confidence = 0.0

        # Distance estimation
        self.estimated_distance = 0.0

        # Cadence parameters (steps per second)
        self.cadence_walk = (1.5, 2.5)   # 1.5-2.5 steps/sec for walking
        self.cadence_run = (3.0, 4.5)    # 3.0-4.5 steps/sec for running

        # Frequency ranges for human footsteps
        self.freq_impact = (60, 180)     # main impact (heel strike)
        self.freq_detail = (180, 400)    # shoe/surface detail
        self.freq_body = (20, 60)        # body weight shift

        # Pattern detection
        self.last_step_time = 0.0
        self.step_intervals = []
        self.max_intervals = 10

    def analyze_footstep(self, block, sample_rate, stereo=True):
        """
        Analyze audio block for human footstep patterns

        Returns:
            dict: {
                'is_human_step': bool,
                'confidence': float (0-100),
                'cadence': float (steps/sec),
                'foot': str ('left'/'right'/'unknown'),
                'surface': str,
                'distance_m': float,
                'gait_type': str ('walk'/'run'/'unknown')
            }
        """
        try:
            current_time = time.time()

            # Convert to mono for frequency analysis
            if block.ndim == 2:
                mono = np.mean(block, axis=1)
                left = block[:, 0]
                right = block[:, 1]
            else:
                mono = block.ravel()
                left = mono
                right = mono
                stereo = False

            # FFT analysis
            window = np.hanning(len(mono))
            windowed = mono * window
            fft_data = np.fft.rfft(windowed)
            freqs = np.fft.rfftfreq(len(mono), d=1.0/sample_rate)
            power = np.abs(fft_data)

            # Analyze frequency bands characteristic for human footsteps
            impact_mask = (freqs >= self.freq_impact[0]) & (freqs < self.freq_impact[1])
            detail_mask = (freqs >= self.freq_detail[0]) & (freqs < self.freq_detail[1])
            body_mask = (freqs >= self.freq_body[0]) & (freqs < self.freq_body[1])

            impact_power = np.mean(power[impact_mask]) if np.any(impact_mask) else 0.0
            detail_power = np.mean(power[detail_mask]) if np.any(detail_mask) else 0.0
            body_power = np.mean(power[body_mask]) if np.any(body_mask) else 0.0

            total_power = np.mean(power) + 1e-9

            # Ratios characteristic for footsteps
            impact_ratio = impact_power / total_power
            detail_ratio = detail_power / total_power
            body_ratio = body_power / total_power

            # Human footstep signature: strong impact + moderate detail + low body
            # Threshold for detection
            is_step_candidate = (
                impact_ratio > 0.15 and  # strong impact
                detail_ratio > 0.05 and  # some detail
                body_ratio > 0.02        # some body weight
            )

            # Initialize result
            result = {
                'is_human_step': False,
                'confidence': 0.0,
                'cadence': 0.0,
                'foot': 'unknown',
                'surface': 'unknown',
                'distance_m': 0.0,
                'gait_type': 'unknown'
            }

            if not is_step_candidate:
                return result

            # Temporal pattern analysis (cadence detection)
            time_since_last = current_time - self.last_step_time

            # Valid step interval: 150ms to 800ms (covers walk and run)
            if 0.15 < time_since_last < 0.8:
                self.step_intervals.append(time_since_last)
                if len(self.step_intervals) > self.max_intervals:
                    self.step_intervals.pop(0)

                self.step_history.append(current_time)
                if len(self.step_history) > self.max_history:
                    self.step_history.pop(0)

                # Calculate cadence (steps per second)
                if len(self.step_intervals) >= 3:
                    avg_interval = np.mean(self.step_intervals[-5:])
                    cadence = 1.0 / avg_interval if avg_interval > 0 else 0.0

                    # Check if cadence matches human walking or running
                    is_walk_cadence = self.cadence_walk[0] <= cadence <= self.cadence_walk[1]
                    is_run_cadence = self.cadence_run[0] <= cadence <= self.cadence_run[1]

                    if is_walk_cadence or is_run_cadence:
                        result['is_human_step'] = True
                        result['cadence'] = cadence
                        result['gait_type'] = 'walk' if is_walk_cadence else 'run'

                        # Confidence based on pattern regularity
                        if len(self.step_intervals) >= 5:
                            interval_std = np.std(self.step_intervals[-5:])
                            regularity = 1.0 - min(interval_std / avg_interval, 1.0)
                            result['confidence'] = regularity * 100.0
                        else:
                            result['confidence'] = 60.0  # moderate confidence

                self.last_step_time = current_time

            # L-R pattern detection (foot classification)
            if stereo and result['is_human_step']:
                left_rms = np.sqrt(np.mean(left ** 2))
                right_rms = np.sqrt(np.mean(right ** 2))

                if left_rms > right_rms * 1.2:
                    result['foot'] = 'left'
                    self.lr_pattern.append('L')
                elif right_rms > left_rms * 1.2:
                    result['foot'] = 'right'
                    self.lr_pattern.append('R')
                else:
                    result['foot'] = 'center'
                    self.lr_pattern.append('C')

                if len(self.lr_pattern) > self.max_lr_history:
                    self.lr_pattern.pop(0)

                # Check for L-R-L-R pattern (increases confidence)
                if len(self.lr_pattern) >= 4:
                    pattern_str = ''.join(self.lr_pattern[-4:])
                    if pattern_str in ['LRLR', 'RLRL', 'LRCR', 'RLCR', 'CRLR', 'CLRL']:
                        result['confidence'] = min(result['confidence'] + 15.0, 100.0)

            # Surface type detection (based on detail frequency ratio)
            if result['is_human_step']:
                if detail_ratio > 0.15:
                    result['surface'] = 'hard'  # concrete, metal
                elif detail_ratio > 0.08:
                    result['surface'] = 'medium'  # wood, tile
                else:
                    result['surface'] = 'soft'  # carpet, grass, dirt

                self.surface_type = result['surface']

            # Distance estimation (based on loudness)
            if result['is_human_step']:
                rms = np.sqrt(np.mean(mono ** 2))
                if rms > 0:
                    # Rough estimation: louder = closer
                    # This is simplified, real distance needs proper calibration
                    db = 20 * np.log10(rms + 1e-10)
                    # Map dB to distance (empirical formula)
                    # -60 dB = far (50m), -20 dB = close (5m)
                    distance = np.clip(50.0 * ((-20 - db) / 40.0), 1.0, 100.0)
                    result['distance_m'] = distance
                    self.estimated_distance = distance

            return result

        except Exception as e:
            log(f"Error in HumanFootstepDetector.analyze_footstep: {e}", "ERROR")
            return {
                'is_human_step': False,
                'confidence': 0.0,
                'cadence': 0.0,
                'foot': 'unknown',
                'surface': 'unknown',
                'distance_m': 0.0,
                'gait_type': 'unknown'
            }

    def get_pattern_quality(self):
        """
        Get overall pattern quality score (0-100)
        Based on regularity and L-R pattern consistency
        """
        if len(self.step_intervals) < 3:
            return 0.0

        # Temporal regularity
        avg_interval = np.mean(self.step_intervals)
        std_interval = np.std(self.step_intervals)
        temporal_quality = (1.0 - min(std_interval / avg_interval, 1.0)) * 50.0

        # L-R pattern quality
        lr_quality = 0.0
        if len(self.lr_pattern) >= 4:
            # Count alternations
            alternations = sum(1 for i in range(len(self.lr_pattern)-1)
                             if self.lr_pattern[i] != self.lr_pattern[i+1])
            expected_alternations = len(self.lr_pattern) - 1
            if expected_alternations > 0:
                lr_quality = (alternations / expected_alternations) * 50.0

        return temporal_quality + lr_quality


# ============================================================================
# DETECTION PANEL
# ============================================================================

class DetectionPanel(QWidget):
    """Sound detection configuration and status"""

    def __init__(self):
        super().__init__()
        log("DetectionPanel.__init__", "INFO")

        # Initialize advanced footstep detector
        self.footstep_detector = HumanFootstepDetector()

        layout = QVBoxLayout()

        # Profile selection
        self.profile_group = QGroupBox(tr('detection_profile'))
        profile_layout = QVBoxLayout()

        self.profile_combo = QComboBox()
        self.profile_combo.addItems([
            'Universal',
            'ARC Raiders (PC)',
            'ARC Raiders + SB Z SE + Cloud II'
        ])
        self.profile_combo.setCurrentText('ARC Raiders + SB Z SE + Cloud II')
        profile_layout.addWidget(self.profile_combo)

        self.profile_group.setLayout(profile_layout)
        layout.addWidget(self.profile_group)

        # Detection enables
        self.enable_group = QGroupBox(tr('enable_detection'))
        enable_layout = QVBoxLayout()

        self.walk_enable = QCheckBox(tr('detect_walk'))
        self.walk_enable.setChecked(True)
        enable_layout.addWidget(self.walk_enable)

        self.run_enable = QCheckBox(tr('detect_run'))
        self.run_enable.setChecked(True)
        enable_layout.addWidget(self.run_enable)

        self.shot_enable = QCheckBox(tr('detect_shot'))
        self.shot_enable.setChecked(True)
        enable_layout.addWidget(self.shot_enable)

        self.enable_group.setLayout(enable_layout)
        layout.addWidget(self.enable_group)

        # Sensitivity sliders
        self.sens_group = QGroupBox(tr('sensitivity'))
        sens_layout = QVBoxLayout()

        # Walk
        walk_layout = QHBoxLayout()
        self.walk_label_sens = QLabel(tr('walk'))
        walk_layout.addWidget(self.walk_label_sens)
        self.walk_sens = QSlider(Qt.Horizontal)
        self.walk_sens.setRange(1, 100)
        self.walk_sens.setValue(55)
        walk_layout.addWidget(self.walk_sens)
        self.walk_sens_label = QLabel("55")
        self.walk_sens.valueChanged.connect(lambda v: self.walk_sens_label.setText(str(v)))
        walk_layout.addWidget(self.walk_sens_label)
        sens_layout.addLayout(walk_layout)

        # Run
        run_layout = QHBoxLayout()
        self.run_label_sens = QLabel(tr('run'))
        run_layout.addWidget(self.run_label_sens)
        self.run_sens = QSlider(Qt.Horizontal)
        self.run_sens.setRange(1, 100)
        self.run_sens.setValue(55)
        run_layout.addWidget(self.run_sens)
        self.run_sens_label = QLabel("55")
        self.run_sens.valueChanged.connect(lambda v: self.run_sens_label.setText(str(v)))
        run_layout.addWidget(self.run_sens_label)
        sens_layout.addLayout(run_layout)

        # Shot
        shot_layout = QHBoxLayout()
        self.shot_label_sens = QLabel(tr('shot'))
        shot_layout.addWidget(self.shot_label_sens)
        self.shot_sens = QSlider(Qt.Horizontal)
        self.shot_sens.setRange(1, 100)
        self.shot_sens.setValue(65)
        shot_layout.addWidget(self.shot_sens)
        self.shot_sens_label = QLabel("65")
        self.shot_sens.valueChanged.connect(lambda v: self.shot_sens_label.setText(str(v)))
        shot_layout.addWidget(self.shot_sens_label)
        sens_layout.addLayout(shot_layout)

        self.sens_group.setLayout(sens_layout)
        layout.addWidget(self.sens_group)

        # Human Footstep Analysis (v3.0)
        self.footstep_group = QGroupBox("Human Footstep Analysis (v3.0)")
        footstep_layout = QVBoxLayout()

        self.human_confidence_label = QLabel("Confidence: —")
        self.human_confidence_label.setStyleSheet("font-size: 10pt; color: #888888;")
        footstep_layout.addWidget(self.human_confidence_label)

        self.cadence_label = QLabel("Cadence: —")
        self.cadence_label.setStyleSheet("font-size: 10pt; color: #888888;")
        footstep_layout.addWidget(self.cadence_label)

        self.foot_label = QLabel("Foot: —")
        self.foot_label.setStyleSheet("font-size: 10pt; color: #888888;")
        footstep_layout.addWidget(self.foot_label)

        self.surface_label = QLabel("Surface: —")
        self.surface_label.setStyleSheet("font-size: 10pt; color: #888888;")
        footstep_layout.addWidget(self.surface_label)

        self.distance_label = QLabel("Distance: —")
        self.distance_label.setStyleSheet("font-size: 10pt; color: #888888;")
        footstep_layout.addWidget(self.distance_label)

        self.gait_label = QLabel("Gait: —")
        self.gait_label.setStyleSheet("font-size: 10pt; color: #888888;")
        footstep_layout.addWidget(self.gait_label)

        self.footstep_group.setLayout(footstep_layout)
        layout.addWidget(self.footstep_group)

        # Detection status
        self.status_group = QGroupBox(tr('detection_status'))
        status_layout = QVBoxLayout()

        self.walk_label = QLabel(tr('walk_none'))
        self.walk_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        status_layout.addWidget(self.walk_label)

        self.run_label = QLabel(tr('run_none'))
        self.run_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        status_layout.addWidget(self.run_label)

        self.shot_label = QLabel(tr('shot_none'))
        self.shot_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        status_layout.addWidget(self.shot_label)

        self.status_group.setLayout(status_layout)
        layout.addWidget(self.status_group)

        layout.addStretch()
        self.setLayout(layout)

        self.walk_hold = 0
        self.run_hold = 0
        self.shot_hold = 0

    def analyze(self, block, sample_rate):
        """Analyze audio block for walk/run/shot detection"""
        try:
            if block.ndim == 2:
                mono = np.mean(block, axis=1)
            else:
                mono = block.ravel()

            window = np.hanning(len(mono))
            windowed = mono * window

            fft_data = np.fft.rfft(windowed)
            freqs = np.fft.rfftfreq(len(mono), d=1.0/sample_rate)
            power = np.abs(fft_data)

            low_mask = (freqs >= 20) & (freqs < 200)
            mid_mask = (freqs >= 200) & (freqs < 1500)
            high_mask = (freqs >= 1500) & (freqs < 6000)

            low_power = power[low_mask]
            mid_power = power[mid_mask]
            high_power = power[high_mask]

            total_power = np.mean(power) + 1e-9

            low_r = np.mean(low_power) / total_power if len(low_power) > 0 else 0.0
            mid_r = np.mean(mid_power) / total_power if len(mid_power) > 0 else 0.0
            high_r = np.max(high_power) / total_power if len(high_power) > 0 else 0.0

            walk_i = self.band_intensity(low_r, 0.08, self.walk_sens.value() / 100.0)
            run_i = self.band_intensity(mid_r, 0.06, self.run_sens.value() / 100.0)
            shot_i = self.band_intensity(high_r, 0.12, self.shot_sens.value() / 100.0)

            walk_det = walk_i > 0.0 and self.walk_enable.isChecked()
            run_det = run_i > 0.0 and self.run_enable.isChecked()
            shot_det = shot_i > 0.0 and self.shot_enable.isChecked()

            if walk_det:
                self.walk_hold = 6
            if run_det:
                self.run_hold = 6
            if shot_det:
                self.shot_hold = 6

            if self.walk_hold > 0:
                self.walk_hold -= 1
                self.walk_label.setText(tr('walk_detected'))
                self.walk_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #00FF00;")
            else:
                self.walk_label.setText(tr('walk_none'))
                self.walk_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #666666;")

            if self.run_hold > 0:
                self.run_hold -= 1
                self.run_label.setText(tr('run_detected'))
                self.run_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #FFA500;")
            else:
                self.run_label.setText(tr('run_none'))
                self.run_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #666666;")

            if self.shot_hold > 0:
                self.shot_hold -= 1
                self.shot_label.setText(tr('shot_detected'))
                self.shot_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #FF0000;")
            else:
                self.shot_label.setText(tr('shot_none'))
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

            # Advanced human footstep analysis (v3.0)
            footstep_result = self.footstep_detector.analyze_footstep(block, sample_rate, stereo=(block.ndim == 2))

            # Update UI with footstep analysis
            if footstep_result['is_human_step']:
                conf = footstep_result['confidence']
                color = "#00FF00" if conf > 75 else "#FFA500" if conf > 50 else "#FFFF00"

                self.human_confidence_label.setText(f"Confidence: {conf:.1f}%")
                self.human_confidence_label.setStyleSheet(f"font-size: 10pt; font-weight: bold; color: {color};")

                self.cadence_label.setText(f"Cadence: {footstep_result['cadence']:.2f} steps/s")
                self.cadence_label.setStyleSheet(f"font-size: 10pt; color: {color};")

                foot_icon = "👣L" if footstep_result['foot'] == 'left' else "👣R" if footstep_result['foot'] == 'right' else "👣"
                self.foot_label.setText(f"Foot: {foot_icon} {footstep_result['foot'].upper()}")
                self.foot_label.setStyleSheet(f"font-size: 10pt; color: {color};")

                self.surface_label.setText(f"Surface: {footstep_result['surface'].upper()}")
                self.surface_label.setStyleSheet(f"font-size: 10pt; color: {color};")

                self.distance_label.setText(f"Distance: ~{footstep_result['distance_m']:.1f}m")
                self.distance_label.setStyleSheet(f"font-size: 10pt; color: {color};")

                gait_icon = "🚶" if footstep_result['gait_type'] == 'walk' else "🏃" if footstep_result['gait_type'] == 'run' else "❓"
                self.gait_label.setText(f"Gait: {gait_icon} {footstep_result['gait_type'].upper()}")
                self.gait_label.setStyleSheet(f"font-size: 10pt; font-weight: bold; color: {color};")

                # Add footstep info to events
                events['footstep_detected'] = True
                events['footstep_confidence'] = conf
                events['footstep_distance'] = footstep_result['distance_m']
            else:
                # Reset to inactive state
                gray = "#666666"
                self.human_confidence_label.setText("Confidence: —")
                self.human_confidence_label.setStyleSheet(f"font-size: 10pt; color: {gray};")

                self.cadence_label.setText("Cadence: —")
                self.cadence_label.setStyleSheet(f"font-size: 10pt; color: {gray};")

                self.foot_label.setText("Foot: —")
                self.foot_label.setStyleSheet(f"font-size: 10pt; color: {gray};")

                self.surface_label.setText("Surface: —")
                self.surface_label.setStyleSheet(f"font-size: 10pt; color: {gray};")

                self.distance_label.setText("Distance: —")
                self.distance_label.setStyleSheet(f"font-size: 10pt; color: {gray};")

                self.gait_label.setText("Gait: —")
                self.gait_label.setStyleSheet(f"font-size: 10pt; color: {gray};")

                events['footstep_detected'] = False
                events['footstep_confidence'] = 0.0
                events['footstep_distance'] = 0.0

            return events, bands

        except Exception as e:
            log(f"Error in analyze: {e}", "ERROR")
            return {'walk': False, 'run': False, 'shot': False}, {}

    def band_intensity(self, ratio, base, sens):
        """Calculate band intensity with sensitivity threshold"""
        thr = base * (1.4 - sens)
        thr = max(0.02, min(0.6, thr))

        if ratio <= thr:
            return 0.0

        return min(1.0, (ratio - thr) / (1.0 - thr))

    def update_translations(self):
        """Update UI translations"""
        # Update group boxes
        self.profile_group.setTitle(tr('detection_profile'))
        self.enable_group.setTitle(tr('enable_detection'))
        self.sens_group.setTitle(tr('sensitivity'))
        self.status_group.setTitle(tr('detection_status'))

        # Update checkboxes
        self.walk_enable.setText(tr('detect_walk'))
        self.run_enable.setText(tr('detect_run'))
        self.shot_enable.setText(tr('detect_shot'))

        # Update sensitivity labels
        self.walk_label_sens.setText(tr('walk'))
        self.run_label_sens.setText(tr('run'))
        self.shot_label_sens.setText(tr('shot'))

        # Update detection status labels (preserve current state)
        # We need to check current text to determine state
        if 'DETECTED' in self.walk_label.text() or 'WYKRYTO' in self.walk_label.text():
            self.walk_label.setText(tr('walk_detected'))
        else:
            self.walk_label.setText(tr('walk_none'))

        if 'DETECTED' in self.run_label.text() or 'WYKRYTO' in self.run_label.text():
            self.run_label.setText(tr('run_detected'))
        else:
            self.run_label.setText(tr('run_none'))

        if 'DETECTED' in self.shot_label.text() or 'WYKRYTO' in self.shot_label.text():
            self.shot_label.setText(tr('shot_detected'))
        else:
            self.shot_label.setText(tr('shot_none'))


# ============================================================================
# LED OVERLAY WIDGET
# ============================================================================

class LedOverlayWidget(QWidget):
    """LED Edge Alert - colored bars on screen edges"""

    def __init__(self):
        super().__init__()
        log("LedOverlayWidget.__init__", "INFO")

        self.setMinimumHeight(100)

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

        self.timer = QTimer()
        self.timer.timeout.connect(self._tick)
        self.timer.start(50)

    def _tick(self):
        """Decay bar intensities"""
        for bar in self.bars.values():
            bar['intensity'] -= 0.08
            bar['intensity'] = max(0.0, bar['intensity'])

        self.update()

    def update_from_events(self, events, bands, energy, balance):
        """Update LED bars based on detection events"""
        walk = events.get('walk', False)
        run = events.get('run', False)
        shot = events.get('shot', False)

        walk_i = events.get('walk_int', 0.0)
        run_i = events.get('run_int', 0.0)
        shot_i = events.get('shot_int', 0.0)

        if balance < -0.2:
            side = 'left'
        elif balance > 0.2:
            side = 'right'
        else:
            side = 'center'

        if side == 'left':
            side_bars = ['L1', 'L2']
            flank_bars = ['G1', 'D1']
        elif side == 'right':
            side_bars = ['P1', 'P2']
            flank_bars = ['G3', 'D3']
        else:
            side_bars = ['G2', 'D2']
            flank_bars = ['G1', 'G3', 'D1', 'D3']

        if walk or run:
            strength = max(walk_i, run_i)
            color = self._walk_run_color(strength)

            for bar_name in side_bars + flank_bars:
                self.bars[bar_name]['color'] = color
                self.bars[bar_name]['intensity'] = min(1.0, self.bars[bar_name]['intensity'] + 0.3)

        if shot:
            shot_color = QColor(80, 160, 255)

            for bar_name in side_bars + flank_bars:
                self.bars[bar_name]['color'] = shot_color
                self.bars[bar_name]['intensity'] = min(1.0, self.bars[bar_name]['intensity'] + 0.5)

    def _walk_run_color(self, strength):
        """Generate color gradient for walk/run"""
        if strength < 0.5:
            r = int(255 * (strength * 2))
            g = 255
            b = 0
        else:
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

        # Top bars
        self._draw_bar(painter, 0, 0, width // 3, bar_thickness, self.bars['G1'])
        self._draw_bar(painter, width // 3, 0, width // 3, bar_thickness, self.bars['G2'])
        self._draw_bar(painter, 2 * width // 3, 0, width // 3, bar_thickness, self.bars['G3'])

        # Bottom bars
        self._draw_bar(painter, 0, height - bar_thickness, width // 3, bar_thickness, self.bars['D1'])
        self._draw_bar(painter, width // 3, height - bar_thickness, width // 3, bar_thickness, self.bars['D2'])
        self._draw_bar(painter, 2 * width // 3, height - bar_thickness, width // 3, bar_thickness, self.bars['D3'])

        # Left bars
        mid_height = (height - 2 * bar_thickness) // 2
        self._draw_bar(painter, 0, bar_thickness, bar_thickness, mid_height, self.bars['L1'])
        self._draw_bar(painter, 0, bar_thickness + mid_height, bar_thickness, mid_height, self.bars['L2'])

        # Right bars
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
    """Main application window"""

    def __init__(self):
        super().__init__()
        log("MainWindow.__init__", "INFO")

        self.setWindowTitle(f"{tr('app_title')} {VERSION}")
        self.setGeometry(100, 100, 1400, 900)

        self.audio = AudioEngine()
        self.is_running = False
        self.radar_angle = 0.0
        self.test_phase = 0.0

        # Detachable windows
        self.detached_radar = None
        self.detached_led = None

        self.create_ui()

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(50)

    def create_ui(self):
        """Create main UI"""
        # Central widget
        self.central = QTabWidget()

        self.spectrum = SpectrumWidget()
        self.central.addTab(self.spectrum, tr('spectrum'))

        self.waterfall = WaterfallWidget()
        self.central.addTab(self.waterfall, tr('waterfall'))

        self.setCentralWidget(self.central)

        # Radar dock
        self.radar_dock = QDockWidget(tr('radar'), self)
        self.radar_widget = RadarWidget()
        self.radar_dock.setWidget(self.radar_widget)
        self.addDockWidget(Qt.TopDockWidgetArea, self.radar_dock)

        # Device panel dock
        self.device_dock = QDockWidget(tr('device_settings'), self)
        self.dev_panel = DevicePanel(self.audio)
        self.device_dock.setWidget(self.dev_panel)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.device_dock)

        # Detection panel dock
        self.detection_dock = QDockWidget(tr('detection'), self)
        self.det_panel = DetectionPanel()
        self.detection_dock.setWidget(self.det_panel)
        self.addDockWidget(Qt.RightDockWidgetArea, self.detection_dock)

        # LED dock
        self.led_dock = QDockWidget(tr('led_alert'), self)
        self.led_widget = LedOverlayWidget()
        self.led_dock.setWidget(self.led_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.led_dock)

        # Toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        self.start_btn = QPushButton(tr('start'))
        self.start_btn.clicked.connect(self.toggle_start_stop)
        toolbar.addWidget(self.start_btn)

        toolbar.addSeparator()

        # Language switcher
        self.language_label = QLabel(tr('language'))
        toolbar.addWidget(self.language_label)
        self.lang_btn = QPushButton("EN/PL")
        self.lang_btn.setCheckable(True)
        self.lang_btn.clicked.connect(self.toggle_language)
        toolbar.addWidget(self.lang_btn)

        toolbar.addSeparator()

        # Radar controls
        self.radar_alpha_label = QLabel(tr('radar_alpha'))
        toolbar.addWidget(self.radar_alpha_label)
        self.radar_alpha = QSlider(Qt.Horizontal)
        self.radar_alpha.setRange(0, 100)
        self.radar_alpha.setValue(100)
        self.radar_alpha.setMaximumWidth(150)
        self.radar_alpha.valueChanged.connect(self.update_radar_alpha)
        toolbar.addWidget(self.radar_alpha)

        self.detach_radar_btn = QPushButton(tr('detach_radar'))
        self.detach_radar_btn.setCheckable(True)
        self.detach_radar_btn.clicked.connect(self.toggle_detach_radar)
        toolbar.addWidget(self.detach_radar_btn)

        self.radar_frameless_btn = QCheckBox(tr('frameless_mode'))
        self.radar_frameless_btn.toggled.connect(self.toggle_radar_frameless)
        toolbar.addWidget(self.radar_frameless_btn)

        toolbar.addSeparator()

        # LED controls
        self.led_alpha_label = QLabel(tr('led_alpha'))
        toolbar.addWidget(self.led_alpha_label)
        self.led_alpha = QSlider(Qt.Horizontal)
        self.led_alpha.setRange(0, 100)
        self.led_alpha.setValue(80)
        self.led_alpha.setMaximumWidth(150)
        self.led_alpha.valueChanged.connect(self.update_led_alpha)
        toolbar.addWidget(self.led_alpha)

        self.detach_led_btn = QPushButton(tr('detach_led'))
        self.detach_led_btn.setCheckable(True)
        self.detach_led_btn.clicked.connect(self.toggle_detach_led)
        toolbar.addWidget(self.detach_led_btn)

        self.led_frameless_btn = QCheckBox(tr('frameless_mode'))
        self.led_frameless_btn.toggled.connect(self.toggle_led_frameless)
        toolbar.addWidget(self.led_frameless_btn)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(tr('ready'))

    def toggle_language(self):
        """Toggle between EN and PL"""
        global current_language

        if current_language == 'en':
            current_language = 'pl'
        else:
            current_language = 'en'

        log(f"Language changed to: {current_language}", "INFO")
        self.update_ui_translations()

    def update_ui_translations(self):
        """Update all UI text with current language"""
        # Main window
        self.setWindowTitle(f"{tr('app_title')} {VERSION}")

        # Toolbar buttons and labels
        self.start_btn.setText(tr('start') if not self.is_running else tr('stop'))
        self.language_label.setText(tr('language'))
        self.radar_alpha_label.setText(tr('radar_alpha'))
        self.led_alpha_label.setText(tr('led_alpha'))
        self.detach_radar_btn.setText(tr('detach_radar'))
        self.detach_led_btn.setText(tr('detach_led'))
        self.radar_frameless_btn.setText(tr('frameless_mode'))
        self.led_frameless_btn.setText(tr('frameless_mode'))

        # Dock widget titles
        self.radar_dock.setWindowTitle(tr('radar'))
        self.device_dock.setWindowTitle(tr('device_settings'))
        self.detection_dock.setWindowTitle(tr('detection'))
        self.led_dock.setWindowTitle(tr('led_alert'))

        # Central widget tabs
        self.central.setTabText(0, tr('spectrum'))
        self.central.setTabText(1, tr('waterfall'))

        # Status bar
        self.status_bar.showMessage(tr('ready') if not self.is_running else tr('running'))

        # Update panels
        self.dev_panel.update_translations()
        self.det_panel.update_translations()

        # Update detached windows titles
        if self.detached_radar:
            self.detached_radar.setWindowTitle(f"{tr('radar')} - RadarSuite {VERSION}")

        if self.detached_led:
            self.detached_led.setWindowTitle(f"{tr('led_alert')} - RadarSuite {VERSION}")

    def update_radar_alpha(self, value):
        """Update radar opacity"""
        opacity = value / 100.0

        if self.detached_radar:
            self.detached_radar.set_opacity(opacity)

    def update_led_alpha(self, value):
        """Update LED opacity"""
        opacity = value / 100.0

        if self.detached_led:
            self.detached_led.set_opacity(opacity)
        else:
            self.led_widget.global_alpha = opacity

    def toggle_detach_radar(self, checked):
        """Toggle radar detachment"""
        if checked:
            # Create detached radar
            self.detached_radar = DetachableRadarWidget()
            self.detached_radar.set_opacity(self.radar_alpha.value() / 100.0)
            self.detached_radar.show()
            log("Radar detached", "INFO")
        else:
            # Close detached radar
            if self.detached_radar:
                self.detached_radar.close()
                self.detached_radar = None
            log("Radar attached", "INFO")

    def toggle_detach_led(self, checked):
        """Toggle LED detachment"""
        if checked:
            # Create detached LED
            self.detached_led = DetachableLedWidget()
            self.detached_led.set_opacity(self.led_alpha.value() / 100.0)
            self.detached_led.show()
            log("LED detached", "INFO")
        else:
            # Close detached LED
            if self.detached_led:
                self.detached_led.close()
                self.detached_led = None
            log("LED attached", "INFO")

    def toggle_radar_frameless(self, checked):
        """Toggle radar frameless mode"""
        if self.detached_radar:
            self.detached_radar.set_frameless(checked)

    def toggle_led_frameless(self, checked):
        """Toggle LED frameless mode"""
        if self.detached_led:
            self.detached_led.set_frameless(checked)

    def toggle_start_stop(self):
        """Toggle audio capture"""
        if not self.is_running:
            self.start()
        else:
            self.stop()

    def start(self):
        """Start audio capture"""
        log("Starting audio capture", "INFO")

        self.dev_panel.apply_settings()
        self.audio.start()

        self.is_running = True
        self.start_btn.setText(tr('stop'))
        self.status_bar.showMessage(tr('running'))

    def stop(self):
        """Stop audio capture"""
        log("Stopping audio capture", "INFO")

        self.audio.stop()

        self.is_running = False
        self.start_btn.setText(tr('start'))
        self.status_bar.showMessage(tr('stopped'))

    def tick(self):
        """Main update loop"""
        # Update radar sweep
        self.radar_angle = (self.radar_angle + 4.0) % 360.0

        # Update both radars
        self.radar_widget.update_sweep(self.radar_angle)
        if self.detached_radar:
            self.detached_radar.radar.update_sweep(self.radar_angle)

        # Get audio block
        if self.dev_panel.test_mode.isChecked():
            block = self.generate_test_block()
        else:
            block = self.audio.read_block(0.0) or self.audio.last_block

        if block is None:
            return

        # Update spectrum and waterfall
        self.spectrum.update_fft(block)

        if block.ndim == 2:
            mono = np.mean(block, axis=1)
        else:
            mono = block.ravel()

        fft_data = np.fft.rfft(mono * np.hanning(len(mono)))
        power = 20 * np.log10(np.abs(fft_data) + 1e-10)
        self.waterfall.push_row(power)

        # Compute energy and balance
        energy, balance = self.compute_orientation(block)

        if energy > 0:
            rms_db = 20 * np.log10(energy)
            self.dev_panel.rms_label.setText(f"{tr('rms')} {rms_db:.1f} dBFS")

        # Detection
        events, bands = self.det_panel.analyze(block, self.audio.sample_rate)

        # Update radar target - only show when detection occurs
        has_detection = events.get('walk', False) or events.get('run', False) or events.get('shot', False)

        if has_detection and energy > 0.0001:
            angle = 90.0 + balance * 75.0
            distance = min(100.0, max(10.0, energy * 4000.0))

            self.radar_widget.update_target(angle, distance)
            if self.detached_radar:
                self.detached_radar.radar.update_target(angle, distance)
        else:
            # Clear radar when no detection
            self.radar_widget.update_target(None, None)
            if self.detached_radar:
                self.detached_radar.radar.update_target(None, None)

        # Update LED overlays
        self.led_widget.update_from_events(events, bands, energy, balance)
        if self.detached_led:
            self.detached_led.led_overlay.update_from_events(events, bands, energy, balance)

    def compute_orientation(self, block):
        """Compute energy and L/R balance"""
        try:
            if block.ndim == 2 and block.shape[1] >= 2:
                left = block[:, 0]
                right = block[:, 1]

                rms_L = np.sqrt(np.mean(left ** 2))
                rms_R = np.sqrt(np.mean(right ** 2))

                energy = (rms_L + rms_R) / 2.0
                balance = (rms_R - rms_L) / (rms_R + rms_L + 1e-9)

                return energy, balance
            else:
                energy = np.sqrt(np.mean(block ** 2))
                return energy, 0.0

        except Exception as e:
            log(f"Error in compute_orientation: {e}", "ERROR")
            return 0.0, 0.0

    def generate_test_block(self):
        """Generate synthetic test audio"""
        duration = self.audio.blocksize / self.audio.sample_rate
        t = np.linspace(self.test_phase, self.test_phase + duration, self.audio.blocksize)
        self.test_phase += duration

        walk = 0.1 * np.sin(2 * np.pi * 80 * t)
        run = 0.15 * np.sin(2 * np.pi * 420 * t)

        shot = np.zeros_like(t)
        if int(self.test_phase) % 2 == 0 and (self.test_phase % 2) < 0.1:
            shot = 0.3 * np.sin(2 * np.pi * 2200 * t)

        mono = walk + run + shot

        left = mono * 0.9
        right = mono * 1.1

        stereo = np.column_stack([left, right]).astype(np.float32)

        return stereo

    def closeEvent(self, event):
        """Handle window close"""
        log("Application closing", "INFO")
        self.stop()

        if self.detached_radar:
            self.detached_radar.close()

        if self.detached_led:
            self.detached_led.close()

        event.accept()


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """Main entry point"""
    log("=" * 80, "INFO")
    log(f"RadarSuite Final {VERSION} - Starting", "INFO")
    log("=" * 80, "INFO")

    log(f"Python: {sys.version}", "INFO")
    log(f"NumPy: {np.__version__}", "INFO")
    log(f"pyqtgraph: {pg.__version__}", "INFO")
    log(f"sounddevice available: {sd is not None}", "INFO")
    log(f"soundcard available: {sc is not None}", "INFO")

    app = QApplication(sys.argv)
    app.setApplicationName("RadarSuite Final")
    app.setOrganizationName("RadarSuite")

    apply_dark_theme(app)

    window = MainWindow()
    window.show()

    log("Main window shown, entering event loop", "INFO")

    exit_code = app.exec_()

    log(f"Application exited with code: {exit_code}", "INFO")
    log("=" * 80, "INFO")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
