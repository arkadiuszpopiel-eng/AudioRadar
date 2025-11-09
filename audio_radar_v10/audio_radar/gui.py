"""PyQt5-based GUI for Audio Radar with gain and threshold controls.

This module provides a graphical control panel for Audio Radar with:
- Audio device selection
- Input gain slider (0.1x - 10.0x amplification)
- Detection threshold slider (0.001 - 0.200)
- Signal strength indicator with color coding
- Auto-calibration feature
- Pre-amplifier quick boost

The GUI integrates with the existing audio processing and visualization
components, allowing users to adjust sensitivity for weak audio signals.
"""

from __future__ import annotations

import sys
import time
import logging
import threading
from pathlib import Path
from typing import Optional

try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget, QLabel, QSlider, QPushButton,
        QCheckBox, QProgressBar, QVBoxLayout, QHBoxLayout, QFormLayout,
        QComboBox, QMessageBox, QProgressDialog, QTabWidget
    )
    from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
    from PyQt5.QtGui import QFont
except ImportError:
    # PyQt5 not available - will need to be installed
    QApplication = None  # type: ignore
    QMainWindow = None  # type: ignore
    QWidget = None  # type: ignore

try:
    import sounddevice as sd
except ImportError:
    sd = None  # type: ignore

try:
    import numpy as np  # type: ignore
except ImportError:
    np = None  # type: ignore

try:
    import pygame
except ImportError:
    pygame = None  # type: ignore

# Import audio processing components
try:
    from audio_radar.audio_capture import list_audio_input_devices, AudioStream
    from audio_radar.sound_analysis import detect_event
    from audio_radar.visualization import Visualizer
except ImportError:
    from audio_capture import list_audio_input_devices, AudioStream  # type: ignore
    from sound_analysis import detect_event  # type: ignore
    from visualization import Visualizer  # type: ignore


class AudioRadarGUI(QMainWindow):
    """Main GUI window for Audio Radar with gain and threshold controls."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Radar v10.2 - Control Panel")
        self.setGeometry(100, 100, 600, 700)
        
        # State variables
        self.current_gain = 1.0
        self.current_threshold = 0.050
        self.preamp_enabled = False
        self.is_running = False
        self.audio_stream: Optional[AudioStream] = None
        self.visualizer: Optional[Visualizer] = None
        self.visualizer_thread: Optional[threading.Thread] = None
        
        # Setup UI
        self.setup_ui()
        
        # Timer for updating signal strength
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_display)
        self.update_timer.start(100)  # Update every 100ms
        
        # Latest audio stats
        self.latest_peak = 0.0
        self.latest_rms = 0.0
        
    def setup_ui(self):
        """Setup the user interface."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        tabs = QTabWidget()
        main_layout.addWidget(tabs)
        
        # Control tab
        control_tab = QWidget()
        control_layout = QFormLayout(control_tab)
        tabs.addTab(control_tab, "Controls")
        
        # Title
        title = QLabel("Audio Radar v10.2")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #0d7377;")
        control_layout.addRow("", title)
        
        # Device selection
        self.lbl_device = QLabel("Audio Input Device:")
        self.combo_device = QComboBox()
        self.refresh_devices()
        control_layout.addRow(self.lbl_device, self.combo_device)
        
        btn_refresh = QPushButton("🔄 Refresh Devices")
        btn_refresh.clicked.connect(self.refresh_devices)
        control_layout.addRow("", btn_refresh)
        
        # Gain control
        self.lbl_gain = QLabel("Input Gain (Amplification):")
        self.slider_gain = QSlider(Qt.Horizontal)
        self.slider_gain.setMinimum(1)    # 0.1x
        self.slider_gain.setMaximum(100)  # 10.0x
        self.slider_gain.setValue(10)     # Default 1.0x
        self.slider_gain.setTickPosition(QSlider.TicksBelow)
        self.slider_gain.setTickInterval(10)
        self.slider_gain.valueChanged.connect(self.on_gain_changed)
        
        self.lbl_gain_value = QLabel("1.0x")
        self.lbl_gain_value.setStyleSheet("color: #0d7377; font-weight: bold;")
        
        gain_layout = QHBoxLayout()
        gain_layout.addWidget(self.slider_gain)
        gain_layout.addWidget(self.lbl_gain_value)
        
        control_layout.addRow(self.lbl_gain, gain_layout)
        
        self.slider_gain.setToolTip(
            "Wzmocnienie sygnału audio\n"
            "Zwiększ jeśli sygnał jest za słaby\n"
            "Domyślnie: 1.0x (bez wzmocnienia)"
        )
        
        # Threshold control
        self.lbl_threshold = QLabel("Detection Threshold:")
        self.slider_threshold = QSlider(Qt.Horizontal)
        self.slider_threshold.setMinimum(1)     # 0.001
        self.slider_threshold.setMaximum(200)   # 0.200
        self.slider_threshold.setValue(50)      # Default 0.050
        self.slider_threshold.setTickPosition(QSlider.TicksBelow)
        self.slider_threshold.setTickInterval(20)
        self.slider_threshold.valueChanged.connect(self.on_threshold_changed)
        
        self.lbl_threshold_value = QLabel("0.050")
        self.lbl_threshold_value.setStyleSheet("color: #0d7377; font-weight: bold;")
        
        threshold_layout = QHBoxLayout()
        threshold_layout.addWidget(self.slider_threshold)
        threshold_layout.addWidget(self.lbl_threshold_value)
        
        control_layout.addRow(self.lbl_threshold, threshold_layout)
        
        self.slider_threshold.setToolTip(
            "Próg wykrywania zdarzeń\n"
            "Niższy = bardziej czuły (więcej wykryć)\n"
            "Wyższy = mniej czuły (mniej false positives)\n"
            "Domyślnie: 0.050"
        )
        
        # Pre-amplifier checkbox
        self.chk_preamp = QCheckBox("Enable Pre-Amplifier (x5 boost for weak signals)")
        self.chk_preamp.setToolTip(
            "Automatyczne wzmocnienie x5\n"
            "Użyj gdy sygnał jest bardzo słaby"
        )
        self.chk_preamp.stateChanged.connect(self.on_preamp_changed)
        control_layout.addRow("", self.chk_preamp)
        
        # Signal strength indicator
        self.lbl_signal_strength = QLabel("Signal Strength:")
        self.pb_signal_strength = QProgressBar()
        self.pb_signal_strength.setRange(0, 100)
        self.pb_signal_strength.setValue(0)
        self.pb_signal_strength.setTextVisible(True)
        self.pb_signal_strength.setFormat("%v%")
        control_layout.addRow(self.lbl_signal_strength, self.pb_signal_strength)
        
        # Auto-calibrate button
        self.btn_calibrate = QPushButton("🎯 Auto-Calibrate Threshold")
        self.btn_calibrate.setToolTip(
            "Automatyczna kalibracja progu detekcji\n"
            "Program słucha 10s tła i ustawia optymalny threshold"
        )
        self.btn_calibrate.clicked.connect(self.on_auto_calibrate)
        control_layout.addRow("", self.btn_calibrate)
        
        # Start/Stop button
        self.btn_start = QPushButton("▶ START Detection")
        self.btn_start.setStyleSheet(
            "QPushButton { background-color: #00ff00; color: black; font-weight: bold; padding: 10px; }"
            "QPushButton:hover { background-color: #00dd00; }"
        )
        self.btn_start.clicked.connect(self.on_start_stop)
        control_layout.addRow("", self.btn_start)
        
        # Status label
        self.lbl_status = QLabel("Status: Ready")
        self.lbl_status.setStyleSheet("color: #888888;")
        control_layout.addRow("", self.lbl_status)
        
        # Info tab
        info_tab = QWidget()
        info_layout = QVBoxLayout(info_tab)
        tabs.addTab(info_tab, "Info")
        
        info_text = QLabel(
            "<h3>Audio Radar v10.2 - Gain Control & Adjustable Threshold</h3>"
            "<p><b>Problem:</b> Weak audio signals (Peak < 0.01) not detected</p>"
            "<p><b>Solution:</b></p>"
            "<ol>"
            "<li><b>Increase Input Gain:</b> Move slider right to amplify signal</li>"
            "<li><b>Lower Threshold:</b> Move slider left to increase sensitivity</li>"
            "<li><b>Auto-Calibrate:</b> Automatic threshold setup based on background</li>"
            "<li><b>Pre-Amplifier:</b> Quick x5 boost for very weak signals</li>"
            "</ol>"
            "<p><b>Signal Strength Indicator:</b></p>"
            "<ul>"
            "<li>🔴 Red (< 1%): Too weak - increase gain</li>"
            "<li>🟡 Orange (1-5%): Weak - may need adjustment</li>"
            "<li>🟢 Green (> 5%): Good signal</li>"
            "</ul>"
        )
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        info_layout.addStretch()
        
    def refresh_devices(self):
        """Refresh the list of available audio input devices."""
        self.combo_device.clear()
        if sd is None:
            self.combo_device.addItem("sounddevice not available")
            return
        
        devices = list_audio_input_devices()
        if not devices:
            self.combo_device.addItem("No input devices found")
            return
            
        for idx, name in devices:
            self.combo_device.addItem(f"{idx}: {name}", idx)
    
    def get_selected_device(self) -> Optional[int]:
        """Get the currently selected device ID."""
        if self.combo_device.count() == 0:
            return None
        data = self.combo_device.currentData()
        return data if data is not None else None
    
    def on_gain_changed(self, value: int):
        """Update gain value."""
        gain = value / 10.0  # Convert to float (1-100 -> 0.1-10.0)
        self.lbl_gain_value.setText(f"{gain:.1f}x")
        self.current_gain = gain
        
        # Update color based on value
        if gain < 1.0:
            color = "#888888"  # Gray (attenuated)
        elif gain == 1.0:
            color = "#0d7377"  # Cyan (normal)
        elif gain <= 3.0:
            color = "#00ff00"  # Green (boosted)
        else:
            color = "#ffaa00"  # Orange (high boost)
        
        self.lbl_gain_value.setStyleSheet(f"color: {color}; font-weight: bold;")
    
    def on_threshold_changed(self, value: int):
        """Update threshold value."""
        threshold = value / 1000.0  # Convert to float (1-200 -> 0.001-0.200)
        self.lbl_threshold_value.setText(f"{threshold:.3f}")
        self.current_threshold = threshold
        
        # Update color based on value
        if threshold < 0.010:
            color = "#ff0000"  # Red (very sensitive)
        elif threshold < 0.050:
            color = "#ffaa00"  # Orange (sensitive)
        else:
            color = "#00ff00"  # Green (normal)
        
        self.lbl_threshold_value.setStyleSheet(f"color: {color}; font-weight: bold;")
    
    def on_preamp_changed(self, state: int):
        """Toggle pre-amplifier."""
        if state == Qt.Checked:
            self.preamp_enabled = True
            # Automatically set gain to 5.0x
            self.slider_gain.setValue(50)  # 5.0x
        else:
            self.preamp_enabled = False
            # Reset to 1.0x
            self.slider_gain.setValue(10)
    
    def on_auto_calibrate(self):
        """Auto-calibrate threshold based on background noise."""
        if sd is None or np is None:
            QMessageBox.critical(self, "Error", "sounddevice and numpy are required for calibration")
            return
        
        # Ask user
        reply = QMessageBox.question(
            self,
            "Auto-Calibration",
            "Program będzie słuchał przez 10 sekund.\n\n"
            "Upewnij się że:\n"
            "✓ Żadna gra/muzyka nie gra\n"
            "✓ Jest tylko normalny szum tła\n\n"
            "Gotowy?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        # Progress dialog
        progress = QProgressDialog("Kalibracja...", "Anuluj", 0, 100, self)
        progress.setWindowTitle("Auto-Calibration")
        progress.setWindowModality(Qt.WindowModal)
        progress.show()
        
        # Record background
        device_id = self.get_selected_device()
        duration = 10  # seconds
        samplerate = 48000
        
        try:
            # Record
            recording = sd.rec(
                int(duration * samplerate),
                samplerate=samplerate,
                channels=2,
                device=device_id
            )
            
            # Update progress
            for i in range(100):
                QApplication.processEvents()
                progress.setValue(i)
                if progress.wasCanceled():
                    sd.stop()
                    return
                time.sleep(0.1)
            
            sd.wait()
            progress.setValue(100)
            
            # Analyze
            rms_bg = np.sqrt(np.mean(recording**2))
            peak_bg = np.max(np.abs(recording))
            
            # Set threshold = 2x background peak
            recommended_threshold = peak_bg * 2.0
            
            # Clamp to reasonable range
            recommended_threshold = max(0.001, min(recommended_threshold, 0.200))
            
            # Show results
            result = QMessageBox.question(
                self,
                "Kalibracja zakończona",
                f"Wyniki analizy tła:\n\n"
                f"RMS tła: {rms_bg:.6f}\n"
                f"Peak tła: {peak_bg:.6f}\n\n"
                f"Rekomendowany threshold: {recommended_threshold:.3f}\n"
                f"(2x powyżej poziomu tła)\n\n"
                f"Ustawić ten threshold?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if result == QMessageBox.Yes:
                # Set threshold slider
                slider_value = int(recommended_threshold * 1000)
                self.slider_threshold.setValue(slider_value)
                
                QMessageBox.information(
                    self,
                    "Gotowe",
                    f"Threshold ustawiony na: {recommended_threshold:.3f}\n\n"
                    "Teraz uruchom audio i sprawdź detekcję!"
                )
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Kalibracja nie powiodła się:\n{e}")
        
        finally:
            progress.close()
    
    def update_signal_strength(self, peak: float):
        """Update signal strength indicator with color coding."""
        # Convert peak to percentage
        strength = int(min(peak * 100, 100))
        self.pb_signal_strength.setValue(strength)
        
        # Color coding
        if peak < 0.01:
            # Red - too weak
            style = """
            QProgressBar { border: 2px solid #555; border-radius: 5px; background: #2b2b2b; }
            QProgressBar::chunk { background: #ff0000; }
            """
        elif peak < 0.05:
            # Orange - weak
            style = """
            QProgressBar { border: 2px solid #555; border-radius: 5px; background: #2b2b2b; }
            QProgressBar::chunk { background: #ffaa00; }
            """
        else:
            # Green - good
            style = """
            QProgressBar { border: 2px solid #555; border-radius: 5px; background: #2b2b2b; }
            QProgressBar::chunk { background: #00ff00; }
            """
        
        self.pb_signal_strength.setStyleSheet(style)
    
    def on_start_stop(self):
        """Start or stop audio detection."""
        if not self.is_running:
            self.start_detection()
        else:
            self.stop_detection()
    
    def start_detection(self):
        """Start audio detection and visualization."""
        if sd is None or np is None:
            QMessageBox.critical(self, "Error", "sounddevice and numpy are required")
            return
        
        try:
            # Get device
            device_id = self.get_selected_device()
            
            # Create audio stream
            self.audio_stream = AudioStream(input_device=device_id, samplerate=44100, blocksize=1024)
            
            # Define callback
            def on_audio_data(samples):
                # Apply gain
                amplified = samples * self.current_gain
                
                # Store stats
                if amplified.ndim == 2:
                    mono = amplified.mean(axis=1)
                else:
                    mono = amplified.ravel()
                self.latest_peak = float(np.max(np.abs(mono)))
                self.latest_rms = float(np.sqrt(np.mean(mono**2)))
                
                # Detect event with custom threshold
                event = self.detect_event_with_threshold(amplified, self.current_threshold)
                
                if event and self.visualizer:
                    logging.info("Detected event: %s (peak=%.4f, threshold=%.3f)", 
                                event, self.latest_peak, self.current_threshold)
                    self.visualizer.trigger_event(event)
            
            self.audio_stream.on_data = on_audio_data
            
            # Start audio in background thread
            def audio_thread():
                try:
                    self.audio_stream.start()
                except Exception as exc:
                    logging.error("Audio stream error: %s", exc)
            
            audio_t = threading.Thread(target=audio_thread, daemon=True)
            audio_t.start()
            
            # Create and start visualizer in separate thread
            if pygame is not None:
                self.visualizer = Visualizer(bar_width=40, bar_height=200, transparency=180)
                
                def vis_thread():
                    try:
                        self.visualizer.run()
                    except Exception as exc:
                        logging.error("Visualizer error: %s", exc)
                
                self.visualizer_thread = threading.Thread(target=vis_thread, daemon=True)
                self.visualizer_thread.start()
            
            self.is_running = True
            self.btn_start.setText("⏸ STOP Detection")
            self.btn_start.setStyleSheet(
                "QPushButton { background-color: #ff0000; color: white; font-weight: bold; padding: 10px; }"
                "QPushButton:hover { background-color: #dd0000; }"
            )
            self.lbl_status.setText("Status: Running")
            self.lbl_status.setStyleSheet("color: #00ff00;")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start detection:\n{e}")
    
    def stop_detection(self):
        """Stop audio detection and visualization."""
        if self.audio_stream:
            self.audio_stream.stop()
            self.audio_stream = None
        
        # Visualizer will stop when window is closed by user
        self.is_running = False
        self.btn_start.setText("▶ START Detection")
        self.btn_start.setStyleSheet(
            "QPushButton { background-color: #00ff00; color: black; font-weight: bold; padding: 10px; }"
            "QPushButton:hover { background-color: #00dd00; }"
        )
        self.lbl_status.setText("Status: Stopped")
        self.lbl_status.setStyleSheet("color: #888888;")
    
    def detect_event_with_threshold(self, samples: np.ndarray, threshold: float) -> Optional[str]:
        """Detect event using custom threshold."""
        if np is None or samples.size == 0:
            return None
        
        # Convert to mono
        if samples.ndim == 2 and samples.shape[1] > 1:
            mono = samples.mean(axis=1)
        else:
            mono = samples.ravel()
        
        # Normalize if needed
        if np.issubdtype(mono.dtype, np.integer):
            info = np.iinfo(mono.dtype)
            mono = mono.astype(np.float32) / max(abs(info.min), info.max)
        
        # Compute statistics
        peak = np.max(np.abs(mono))
        std = np.std(mono)
        
        # Use hardcoded shot threshold but custom footstep threshold
        SHOT_PEAK_THRESHOLD = 0.6
        if peak > SHOT_PEAK_THRESHOLD:
            return 'shot'
        
        # Use custom threshold for footsteps
        if std > threshold:
            return 'footstep'
        
        return None
    
    def update_display(self):
        """Update display with current signal strength."""
        if self.is_running:
            self.update_signal_strength(self.latest_peak)
    
    def closeEvent(self, event):
        """Handle window close event."""
        self.stop_detection()
        event.accept()


def main():
    """Main entry point for GUI application."""
    if QApplication is None:
        print("ERROR: PyQt5 is required for the GUI. Please install it:")
        print("  pip install PyQt5")
        return 1
    
    # Setup logging
    log_file = Path(__file__).parent / "log_v10.txt"
    logging.basicConfig(
        filename=str(log_file),
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    logging.info("Audio Radar GUI v10.2 starting")
    
    app = QApplication(sys.argv)
    window = AudioRadarGUI()
    window.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
