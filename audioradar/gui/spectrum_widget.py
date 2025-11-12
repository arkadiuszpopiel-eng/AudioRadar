"""
Live frequency spectrum analyzer widget.
Displays real-time frequency spectrum of audio input.
"""

import numpy as np
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QFont


class SpectrumWidget(QWidget):
    """Live frequency spectrum analyzer."""
    
    def __init__(self, sample_rate: int = 44100, parent=None):
        """
        Initialize spectrum widget.
        
        Args:
            sample_rate: Audio sample rate
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.sample_rate = sample_rate
        self.fft_size = 1024
        self.num_bars = 64
        
        # Spectrum data
        self.spectrum = np.zeros(self.num_bars)
        self.peak_hold = np.zeros(self.num_bars)
        self.peak_decay = 0.95
        
        # Colors
        self.bg_color = QColor(25, 25, 25)
        self.bar_color = QColor(0, 200, 255)
        self.peak_color = QColor(255, 100, 100)
        self.text_color = QColor(200, 200, 200)
        
        # Setup widget
        self.setMinimumHeight(150)
        self.setMaximumHeight(300)
        
        # Update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._decay_peaks)
        self.update_timer.start(50)  # 20 FPS
    
    def update_spectrum(self, audio_data: np.ndarray):
        """
        Update spectrum from audio data.
        
        Args:
            audio_data: Audio samples
        """
        if audio_data.size == 0:
            return
        
        # Convert to mono if needed
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)
        
        # Pad or truncate to FFT size
        if len(audio_data) < self.fft_size:
            audio_data = np.pad(audio_data, (0, self.fft_size - len(audio_data)))
        else:
            audio_data = audio_data[:self.fft_size]
        
        # Apply window
        window = np.hanning(self.fft_size)
        audio_data = audio_data * window
        
        # Compute FFT
        fft = np.fft.rfft(audio_data)
        magnitude = np.abs(fft)
        
        # Convert to dB
        magnitude = 20 * np.log10(magnitude + 1e-10)
        
        # Normalize
        magnitude = np.clip((magnitude + 80) / 80, 0, 1)
        
        # Group into bars
        samples_per_bar = len(magnitude) // self.num_bars
        self.spectrum = np.array([
            np.max(magnitude[i*samples_per_bar:(i+1)*samples_per_bar])
            for i in range(self.num_bars)
        ])
        
        # Update peak hold
        self.peak_hold = np.maximum(self.peak_hold, self.spectrum)
        
        self.update()
    
    def _decay_peaks(self):
        """Decay peak hold values."""
        self.peak_hold *= self.peak_decay
        self.update()
    
    def set_colors(self, theme_colors: dict):
        """Update colors from theme."""
        if 'background' in theme_colors:
            self.bg_color = theme_colors['background']
        if 'text' in theme_colors:
            self.text_color = theme_colors['text']
        self.update()
    
    def paintEvent(self, event):
        """Paint the spectrum display."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Get dimensions
        width = self.width()
        height = self.height()
        
        # Draw background
        painter.fillRect(0, 0, width, height, self.bg_color)
        
        # Calculate bar dimensions
        bar_width = width // self.num_bars
        spacing = max(1, bar_width // 10)
        actual_bar_width = bar_width - spacing
        
        # Draw frequency labels
        painter.setPen(QPen(self.text_color))
        font = QFont("Arial", 8)
        painter.setFont(font)
        
        freq_labels = ["100Hz", "1kHz", "10kHz"]
        label_positions = [0.1, 0.5, 0.9]
        
        for label, pos in zip(freq_labels, label_positions):
            x = int(width * pos)
            painter.drawText(x - 20, height - 5, 40, 15, Qt.AlignCenter, label)
        
        # Draw bars
        for i in range(self.num_bars):
            x = i * bar_width
            
            # Spectrum bar
            bar_height = int(self.spectrum[i] * (height - 20))
            y = height - 20 - bar_height
            
            # Color based on level
            if self.spectrum[i] > 0.8:
                color = QColor(255, 0, 0)
            elif self.spectrum[i] > 0.5:
                color = QColor(255, 255, 0)
            else:
                color = self.bar_color
            
            painter.fillRect(x, y, actual_bar_width, bar_height, color)
            
            # Peak hold line
            peak_y = height - 20 - int(self.peak_hold[i] * (height - 20))
            painter.setPen(QPen(self.peak_color, 2))
            painter.drawLine(x, peak_y, x + actual_bar_width, peak_y)
