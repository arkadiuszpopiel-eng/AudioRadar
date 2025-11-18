"""
Live Spectrum Analyzer Widget for AudioRadar PyQt5
Real-time frequency spectrum visualization with customizable display.
"""

import numpy as np
from scipy import signal
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QLinearGradient, QFont

from logger import get_logger


class SpectrumAnalyzerWidget(QWidget):
    """
    Live spectrum analyzer with frequency visualization.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = get_logger()
        self.logger.info("Initializing Spectrum Analyzer Widget")

        # Audio data
        self.audio_buffer = np.array([])
        self.sample_rate = 48000
        self.spectrum_data = np.array([])
        self.frequencies = np.array([])

        # Display settings
        self.num_bars = 64
        self.min_freq = 20  # Hz
        self.max_freq = 20000  # Hz
        self.smoothing = 0.7  # Smoothing factor (0-1)

        # Visual settings
        self.background_color = QColor(10, 10, 20, 255)
        self.bar_gradient_start = QColor(0, 255, 0, 255)  # Green
        self.bar_gradient_mid = QColor(255, 255, 0, 255)  # Yellow
        self.bar_gradient_end = QColor(255, 0, 0, 255)  # Red
        self.grid_color = QColor(50, 50, 70, 100)
        self.text_color = QColor(200, 200, 255, 255)

        # Smoothed spectrum for display
        self.display_spectrum = np.zeros(self.num_bars)

        # UI setup
        self.setMinimumSize(400, 200)

        # Update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update)
        self.update_timer.start(33)  # ~30 FPS

        self.logger.info("Spectrum Analyzer Widget initialized successfully")

    def update_audio_data(self, audio_data: np.ndarray, sample_rate: float):
        """Update with new audio data."""
        try:
            self.sample_rate = int(sample_rate)

            # Convert to mono if stereo
            if audio_data.ndim == 2:
                mono = np.mean(audio_data, axis=1)
            else:
                mono = audio_data.ravel()

            # Store audio buffer
            self.audio_buffer = mono

            # Calculate spectrum
            self._calculate_spectrum()

        except Exception as e:
            self.logger.error(f"Error updating spectrum analyzer", e)

    def _calculate_spectrum(self):
        """Calculate frequency spectrum from audio buffer."""
        try:
            if len(self.audio_buffer) < 512:
                return

            # Use Welch's method for power spectral density
            nperseg = min(len(self.audio_buffer), 2048)
            frequencies, psd = signal.welch(
                self.audio_buffer,
                fs=self.sample_rate,
                nperseg=nperseg,
                scaling='spectrum'
            )

            # Convert to dB scale
            psd_db = 10 * np.log10(psd + 1e-10)

            # Normalize to 0-1 range
            psd_normalized = (psd_db - psd_db.min()) / (psd_db.max() - psd_db.min() + 1e-10)

            # Resample to num_bars
            freq_bins = np.logspace(
                np.log10(self.min_freq),
                np.log10(self.max_freq),
                self.num_bars + 1
            )

            spectrum_bars = np.zeros(self.num_bars)

            for i in range(self.num_bars):
                freq_low = freq_bins[i]
                freq_high = freq_bins[i + 1]

                # Find indices in this frequency range
                idx = np.where((frequencies >= freq_low) & (frequencies < freq_high))[0]

                if len(idx) > 0:
                    # Average power in this bin
                    spectrum_bars[i] = np.mean(psd_normalized[idx])

            # Apply smoothing
            self.display_spectrum = (
                    self.smoothing * self.display_spectrum +
                    (1 - self.smoothing) * spectrum_bars
            )

            self.spectrum_data = self.display_spectrum
            self.frequencies = freq_bins[:-1]

        except Exception as e:
            self.logger.error(f"Error calculating spectrum", e)

    def paintEvent(self, event):
        """Paint the spectrum analyzer display."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()

        # Draw background
        painter.fillRect(self.rect(), self.background_color)

        # Draw grid
        self._draw_grid(painter, width, height)

        # Draw spectrum bars
        self._draw_spectrum_bars(painter, width, height)

        # Draw frequency labels
        self._draw_frequency_labels(painter, width, height)

    def _draw_grid(self, painter: QPainter, width: int, height: int):
        """Draw background grid."""
        painter.setPen(QPen(self.grid_color, 1))

        # Horizontal lines
        for i in range(1, 5):
            y = height * i // 5
            painter.drawLine(0, y, width, y)

        # Vertical lines (logarithmic frequency divisions)
        freq_markers = [100, 1000, 10000]
        for freq in freq_markers:
            if self.min_freq <= freq <= self.max_freq:
                x_pos = self._freq_to_x_position(freq, width)
                painter.drawLine(x_pos, 0, x_pos, height)

    def _freq_to_x_position(self, freq: float, width: int) -> int:
        """Convert frequency to x position."""
        log_min = np.log10(self.min_freq)
        log_max = np.log10(self.max_freq)
        log_freq = np.log10(freq)

        x_normalized = (log_freq - log_min) / (log_max - log_min)
        return int(x_normalized * width)

    def _draw_spectrum_bars(self, painter: QPainter, width: int, height: int):
        """Draw spectrum bars."""
        if len(self.display_spectrum) == 0:
            return

        bar_width = width / self.num_bars
        margin = 1  # Small margin between bars

        for i, amplitude in enumerate(self.display_spectrum):
            # Bar position and size
            x = i * bar_width
            bar_height = amplitude * (height - 20)  # Leave space for labels

            # Get color based on amplitude (gradient from green to red)
            color = self._get_bar_color(amplitude)

            # Draw bar
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawRect(
                int(x + margin),
                int(height - bar_height - 20),
                int(bar_width - 2 * margin),
                int(bar_height)
            )

            # Draw peak indicator
            if amplitude > 0.8:
                peak_color = QColor(255, 255, 255, 200)
                painter.setPen(QPen(peak_color, 2))
                peak_y = int(height - bar_height - 20)
                painter.drawLine(
                    int(x + margin),
                    peak_y,
                    int(x + bar_width - margin),
                    peak_y
                )

    def _get_bar_color(self, amplitude: float) -> QColor:
        """Get color for bar based on amplitude."""
        if amplitude < 0.5:
            # Green to Yellow
            ratio = amplitude * 2
            r = int(self.bar_gradient_start.red() * (1 - ratio) +
                    self.bar_gradient_mid.red() * ratio)
            g = int(self.bar_gradient_start.green() * (1 - ratio) +
                    self.bar_gradient_mid.green() * ratio)
            b = int(self.bar_gradient_start.blue() * (1 - ratio) +
                    self.bar_gradient_mid.blue() * ratio)
        else:
            # Yellow to Red
            ratio = (amplitude - 0.5) * 2
            r = int(self.bar_gradient_mid.red() * (1 - ratio) +
                    self.bar_gradient_end.red() * ratio)
            g = int(self.bar_gradient_mid.green() * (1 - ratio) +
                    self.bar_gradient_end.green() * ratio)
            b = int(self.bar_gradient_mid.blue() * (1 - ratio) +
                    self.bar_gradient_end.blue() * ratio)

        return QColor(r, g, b, 255)

    def _draw_frequency_labels(self, painter: QPainter, width: int, height: int):
        """Draw frequency labels."""
        painter.setPen(QPen(self.text_color, 1))
        painter.setFont(QFont("Arial", 8))

        # Draw frequency markers
        freq_labels = [
            (100, "100Hz"),
            (1000, "1kHz"),
            (10000, "10kHz")
        ]

        for freq, label in freq_labels:
            if self.min_freq <= freq <= self.max_freq:
                x_pos = self._freq_to_x_position(freq, width)
                painter.drawText(x_pos - 20, height - 5, 40, 15, Qt.AlignCenter, label)
