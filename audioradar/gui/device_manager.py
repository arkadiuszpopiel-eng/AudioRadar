"""
Audio device detection and selection dialog.
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QListWidget, 
                             QPushButton, QLabel, QListWidgetItem, QMessageBox)
from PyQt5.QtCore import Qt
from audioradar.audio_engine import AudioEngine
from audioradar.logger import get_logger


class DeviceManager(QDialog):
    """Audio device management dialog."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.logger = get_logger()
        self.selected_device = None
        
        self.setWindowTitle("Audio Device Manager")
        self.setModal(True)
        self.setMinimumSize(500, 400)
        
        self._setup_ui()
        self._load_devices()
    
    def _setup_ui(self):
        """Setup user interface."""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Select Audio Input Device")
        title.setStyleSheet("font-size: 14pt; font-weight: bold;")
        layout.addWidget(title)
        
        # Device list
        self.device_list = QListWidget()
        self.device_list.itemDoubleClicked.connect(self._on_device_selected)
        layout.addWidget(self.device_list)
        
        # Info label
        self.info_label = QLabel("Double-click to select a device or click Test")
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self._load_devices)
        button_layout.addWidget(self.refresh_btn)
        
        self.test_btn = QPushButton("Test Device")
        self.test_btn.clicked.connect(self._test_device)
        button_layout.addWidget(self.test_btn)
        
        button_layout.addStretch()
        
        self.select_btn = QPushButton("Select")
        self.select_btn.clicked.connect(self._on_device_selected)
        button_layout.addWidget(self.select_btn)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def _load_devices(self):
        """Load available audio devices."""
        self.device_list.clear()
        
        try:
            devices = AudioEngine.list_input_devices()
            
            if not devices:
                item = QListWidgetItem("No input devices found")
                item.setFlags(Qt.NoItemFlags)
                self.device_list.addItem(item)
                return
            
            # Add default device marker
            default_device = AudioEngine.get_default_device()
            default_index = default_device.index if default_device else None
            
            for device in devices:
                device_text = f"{device.name} ({device.channels}ch @ {int(device.sample_rate)}Hz)"
                if device.index == default_index:
                    device_text += " [DEFAULT]"
                
                item = QListWidgetItem(device_text)
                item.setData(Qt.UserRole, device.index)
                self.device_list.addItem(item)
            
            self.logger.info(f"Loaded {len(devices)} audio devices")
            
        except Exception as e:
            self.logger.error(f"Failed to load devices: {e}")
            QMessageBox.critical(self, "Error", f"Failed to load devices:\n{str(e)}")
    
    def _test_device(self):
        """Test selected device."""
        current_item = self.device_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a device to test")
            return
        
        device_index = current_item.data(Qt.UserRole)
        
        try:
            # Create temporary engine for testing
            engine = AudioEngine(device_index=device_index)
            
            # Test device
            self.info_label.setText("Testing device... Please wait 2 seconds...")
            QMessageBox.information(self, "Testing", 
                                  "Device test will record for 2 seconds.\n"
                                  "Make some noise to test the input.")
            
            success, level, message = engine.test_device(duration=2.0)
            
            if success:
                QMessageBox.information(self, "Test Result", 
                                      f"Device test successful!\n\n{message}\n"
                                      f"Average level: {level:.3f}")
            else:
                QMessageBox.warning(self, "Test Result",
                                  f"Device test failed:\n{message}")
            
            self.info_label.setText(message)
            
        except Exception as e:
            self.logger.error(f"Device test error: {e}")
            QMessageBox.critical(self, "Error", f"Device test failed:\n{str(e)}")
            self.info_label.setText("Device test failed")
    
    def _on_device_selected(self):
        """Handle device selection."""
        current_item = self.device_list.currentItem()
        if not current_item:
            return
        
        device_index = current_item.data(Qt.UserRole)
        if device_index is None:
            return
        
        self.selected_device = device_index
        self.accept()
    
    def get_selected_device(self):
        """Get selected device index."""
        return self.selected_device
