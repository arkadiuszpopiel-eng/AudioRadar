"""
AudioRadar v10.1 - Audio Test Dialog
Dialog for testing audio input levels and verifying device configuration
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QProgressBar, QComboBox, QGroupBox
)
from PyQt5.QtCore import Qt, QTimer
import sys

try:
    import sounddevice as sd
    import numpy as np
    HAS_AUDIO = True
except ImportError:
    HAS_AUDIO = False
    sd = None
    np = None


class AudioTestDialog(QDialog):
    """Dialog for testing audio input"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔊 Audio Input Test")
        self.setModal(True)
        self.resize(500, 400)
        
        # State
        self.is_testing = False
        self.audio_stream = None
        self.current_level = 0.0
        self.peak_level = 0.0
        
        # Setup UI
        self.init_ui()
        
        # Setup timer for level updates
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_levels)
        self.update_timer.start(50)  # Update every 50ms
    
    def init_ui(self):
        """Initialize the dialog UI"""
        layout = QVBoxLayout(self)
        
        # Info label
        info_label = QLabel("Test your audio input device to verify it's working correctly.")
        info_label.setWordWrap(True)
        info_label.setStyleSheet("font-size: 12px; color: #aaa; margin-bottom: 10px;")
        layout.addWidget(info_label)
        
        # Device selection
        device_group = QGroupBox("Audio Input Device:")
        device_layout = QVBoxLayout(device_group)
        
        self.device_combo = QComboBox()
        self.device_combo.setMinimumHeight(30)
        self.load_devices()
        device_layout.addWidget(self.device_combo)
        
        layout.addWidget(device_group)
        
        # Level indicators
        level_group = QGroupBox("Audio Levels:")
        level_layout = QVBoxLayout(level_group)
        
        # RMS level
        rms_label = QLabel("RMS Level (Average):")
        level_layout.addWidget(rms_label)
        
        self.rms_bar = QProgressBar()
        self.rms_bar.setMinimumHeight(25)
        self.rms_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #555;
                border-radius: 5px;
                text-align: center;
                background-color: #2b2b2b;
            }
            QProgressBar::chunk {
                background-color: #44ff44;
            }
        """)
        level_layout.addWidget(self.rms_bar)
        
        # Peak level
        peak_label = QLabel("Peak Level:")
        level_layout.addWidget(peak_label)
        
        self.peak_bar = QProgressBar()
        self.peak_bar.setMinimumHeight(25)
        self.peak_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #555;
                border-radius: 5px;
                text-align: center;
                background-color: #2b2b2b;
            }
            QProgressBar::chunk {
                background-color: #ff4444;
            }
        """)
        level_layout.addWidget(self.peak_bar)
        
        # Numeric values
        self.value_label = QLabel("RMS: 0.000 | Peak: 0.000")
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setStyleSheet("font-family: monospace; font-size: 14px; color: #00ffff;")
        level_layout.addWidget(self.value_label)
        
        layout.addWidget(level_group)
        
        # Status label
        self.status_label = QLabel("Status: Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-weight: bold; color: #ffff00;")
        layout.addWidget(self.status_label)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.btn_start = QPushButton("▶ Start Test")
        self.btn_start.setMinimumHeight(35)
        self.btn_start.clicked.connect(self.start_test)
        button_layout.addWidget(self.btn_start)
        
        self.btn_stop = QPushButton("■ Stop Test")
        self.btn_stop.setMinimumHeight(35)
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.stop_test)
        button_layout.addWidget(self.btn_stop)
        
        self.btn_close = QPushButton("Close")
        self.btn_close.setMinimumHeight(35)
        self.btn_close.clicked.connect(self.accept)
        button_layout.addWidget(self.btn_close)
        
        layout.addLayout(button_layout)
        
        # Instructions
        instr_label = QLabel(
            "📢 Make some noise (speak, clap, play music) to see the levels change.\n"
            "A working microphone should show values above 0.01 when you make sound."
        )
        instr_label.setWordWrap(True)
        instr_label.setStyleSheet("font-size: 11px; color: #888; margin-top: 10px;")
        layout.addWidget(instr_label)
    
    def load_devices(self):
        """Load available audio input devices"""
        self.device_combo.clear()
        
        if not HAS_AUDIO:
            self.device_combo.addItem("⚠ Audio libraries not available")
            return
        
        try:
            devices = sd.query_devices()
            for i, device in enumerate(devices):
                if device['max_input_channels'] > 0:
                    self.device_combo.addItem(f"{device['name']}", i)
            
            if self.device_combo.count() == 0:
                self.device_combo.addItem("⚠ No input devices found")
        except Exception as e:
            self.device_combo.addItem(f"⚠ Error: {e}")
    
    def start_test(self):
        """Start audio testing"""
        if not HAS_AUDIO:
            self.status_label.setText("Status: ⚠ Audio libraries not available!")
            self.status_label.setStyleSheet("font-weight: bold; color: #ff4444;")
            return
        
        device_idx = self.device_combo.currentData()
        if device_idx is None:
            self.status_label.setText("Status: ⚠ No device selected")
            return
        
        try:
            # Start audio stream
            self.audio_stream = sd.InputStream(
                device=device_idx,
                channels=1,
                samplerate=44100,
                blocksize=2048,
                callback=self.audio_callback
            )
            self.audio_stream.start()
            
            self.is_testing = True
            self.btn_start.setEnabled(False)
            self.btn_stop.setEnabled(True)
            self.status_label.setText("Status: 🟢 Testing... Make some noise!")
            self.status_label.setStyleSheet("font-weight: bold; color: #44ff44;")
            
        except Exception as e:
            self.status_label.setText(f"Status: ⚠ Error: {str(e)[:50]}")
            self.status_label.setStyleSheet("font-weight: bold; color: #ff4444;")
    
    def stop_test(self):
        """Stop audio testing"""
        self.is_testing = False
        
        if self.audio_stream:
            self.audio_stream.stop()
            self.audio_stream.close()
            self.audio_stream = None
        
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.status_label.setText("Status: Stopped")
        self.status_label.setStyleSheet("font-weight: bold; color: #ffff00;")
    
    def audio_callback(self, indata, frames, time_info, status):
        """Callback for audio stream"""
        if not self.is_testing:
            return
        
        # Calculate RMS (root mean square) level
        rms = np.sqrt(np.mean(indata**2))
        
        # Calculate peak level
        peak = np.max(np.abs(indata))
        
        # Store values
        self.current_level = float(rms)
        self.peak_level = float(peak)
    
    def update_levels(self):
        """Update level indicators"""
        if not self.is_testing:
            # Gradually decay levels when not testing
            self.current_level *= 0.95
            self.peak_level *= 0.95
        
        # Convert to percentage (0-100)
        # Typical speech is around 0.01-0.1, loud sounds up to 1.0
        rms_percent = min(100, int(self.current_level * 200))
        peak_percent = min(100, int(self.peak_level * 100))
        
        # Update bars
        self.rms_bar.setValue(rms_percent)
        self.peak_bar.setValue(peak_percent)
        
        # Update numeric display
        self.value_label.setText(f"RMS: {self.current_level:.4f} | Peak: {self.peak_level:.4f}")
        
        # Color warnings
        if self.is_testing:
            if self.peak_level > 0.95:
                self.value_label.setStyleSheet("font-family: monospace; font-size: 14px; color: #ff0000; font-weight: bold;")
            elif self.current_level < 0.001:
                self.value_label.setStyleSheet("font-family: monospace; font-size: 14px; color: #ffff00;")
            else:
                self.value_label.setStyleSheet("font-family: monospace; font-size: 14px; color: #00ffff;")
    
    def closeEvent(self, event):
        """Handle dialog close"""
        self.stop_test()
        super().closeEvent(event)


def main():
    """Standalone test"""
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    dialog = AudioTestDialog()
    dialog.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
