"""
Audio device quality testing dialog.
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QPushButton, QLabel, 
                             QProgressBar, QTextEdit)
from PyQt5.QtCore import Qt, QTimer
from audioradar.audio_engine import AudioEngine
from audioradar.logger import get_logger


class AudioTestDialog(QDialog):
    """Audio device quality testing dialog."""
    
    def __init__(self, device_index, parent=None):
        super().__init__(parent)
        
        self.logger = get_logger()
        self.device_index = device_index
        
        self.setWindowTitle("Audio Device Test")
        self.setModal(True)
        self.setMinimumSize(400, 300)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup user interface."""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Audio Device Quality Test")
        title.setStyleSheet("font-size: 12pt; font-weight: bold;")
        layout.addWidget(title)
        
        # Info
        info = QLabel("This test will record audio for a few seconds\n"
                     "to check device quality and signal strength.")
        info.setWordWrap(True)
        layout.addWidget(info)
        
        # Progress
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        layout.addWidget(self.progress)
        
        # Results
        self.results = QTextEdit()
        self.results.setReadOnly(True)
        layout.addWidget(self.results)
        
        # Buttons
        self.test_btn = QPushButton("Start Test")
        self.test_btn.clicked.connect(self._run_test)
        layout.addWidget(self.test_btn)
        
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.accept)
        layout.addWidget(self.close_btn)
        
        self.setLayout(layout)
    
    def _run_test(self):
        """Run device test."""
        self.test_btn.setEnabled(False)
        self.results.clear()
        self.progress.setValue(0)
        
        try:
            # Create engine
            engine = AudioEngine(device_index=self.device_index)
            
            self.results.append("Starting test...")
            self.results.append(f"Device index: {self.device_index}")
            
            # Simulate progress
            for i in range(0, 101, 10):
                self.progress.setValue(i)
                QTimer.singleShot(i * 20, lambda: None)
            
            # Run test
            success, level, message = engine.test_device(duration=2.0)
            
            self.results.append("\nTest Results:")
            self.results.append("-" * 40)
            self.results.append(f"Status: {'SUCCESS' if success else 'FAILED'}")
            self.results.append(f"Average Level: {level:.4f}")
            self.results.append(f"Message: {message}")
            
            if success:
                quality = "Excellent" if level > 0.3 else "Good" if level > 0.1 else "Fair"
                self.results.append(f"\nQuality: {quality}")
                self.results.append("\n✓ Device is working properly")
            else:
                self.results.append("\n✗ Device test failed")
                self.results.append("Check device connections and settings")
            
            self.progress.setValue(100)
            
        except Exception as e:
            self.logger.error(f"Test error: {e}")
            self.results.append(f"\nERROR: {str(e)}")
            self.progress.setValue(0)
        
        finally:
            self.test_btn.setEnabled(True)
