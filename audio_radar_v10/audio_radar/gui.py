"""PyQt5 GUI for AudioRadar v10.2"""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QFormLayout, 
    QLabel, QComboBox, QPushButton, QHBoxLayout, QSlider
)
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    """Main window for AudioRadar application"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AudioRadar v10.2")
        self.setGeometry(100, 100, 600, 400)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Form layout for controls
        layout = QFormLayout()
        main_layout.addLayout(layout)
        
        # ===== DEVICE SELECTION =====
        self.lbl_device = QLabel("Audio Device:")
        self.combo_device = QComboBox()
        self.combo_device.addItem("Default Device", None)
        layout.addRow(self.lbl_device, self.combo_device)
        
        # ===== GAIN CONTROL =====
        self.lbl_gain = QLabel("Input Gain:")
        self.slider_gain = QSlider(Qt.Horizontal)
        self.slider_gain.setMinimum(1)
        self.slider_gain.setMaximum(100)
        self.slider_gain.setValue(10)
        self.slider_gain.valueChanged.connect(self.on_gain_changed)
        
        self.lbl_gain_value = QLabel("1.0x")
        self.lbl_gain_value.setStyleSheet("color: #0d7377; font-weight: bold;")
        
        gain_layout = QHBoxLayout()
        gain_layout.addWidget(self.slider_gain)
        gain_layout.addWidget(self.lbl_gain_value)
        
        # Add to layout (adjust for your layout type)
        layout.addRow(self.lbl_gain, gain_layout)
        
        # ===== THRESHOLD CONTROL =====
        self.lbl_threshold = QLabel("Detection Threshold:")
        self.slider_threshold = QSlider(Qt.Horizontal)
        self.slider_threshold.setMinimum(1)
        self.slider_threshold.setMaximum(200)
        self.slider_threshold.setValue(50)
        self.slider_threshold.valueChanged.connect(self.on_threshold_changed)
        
        self.lbl_threshold_value = QLabel("0.050")
        self.lbl_threshold_value.setStyleSheet("color: #0d7377; font-weight: bold;")
        
        threshold_layout = QHBoxLayout()
        threshold_layout.addWidget(self.slider_threshold)
        threshold_layout.addWidget(self.lbl_threshold_value)
        
        layout.addRow(self.lbl_threshold, threshold_layout)
        
        # Initialize
        self.current_gain = 1.0
        self.current_threshold = 0.050
        
        # ===== CONTROL BUTTONS =====
        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        
        self.btn_start = QPushButton("Start")
        self.btn_stop = QPushButton("Stop")
        self.btn_stop.setEnabled(False)
        
        button_layout.addWidget(self.btn_start)
        button_layout.addWidget(self.btn_stop)
        button_layout.addStretch()
        
        # ===== STATUS LABEL =====
        self.lbl_status = QLabel("Ready")
        self.lbl_status.setStyleSheet("color: #0d7377; font-weight: bold;")
        main_layout.addWidget(self.lbl_status)
        
        main_layout.addStretch()
    
    def on_gain_changed(self, value):
        """Update gain"""
        gain = value / 10.0
        self.lbl_gain_value.setText(f"{gain:.1f}x")
        self.current_gain = gain
        
    def on_threshold_changed(self, value):
        """Update threshold"""
        threshold = value / 1000.0
        self.lbl_threshold_value.setText(f"{threshold:.3f}")
        self.current_threshold = threshold
