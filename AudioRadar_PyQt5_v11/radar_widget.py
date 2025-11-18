"""
Advanced Radar Visualization Widget for AudioRadar PyQt5
Detachable, resizable, transparent radar display with directional tracking.
"""

import math
import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QPoint, QRect, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QRadialGradient, QPainterPath, QFont

from sound_detector import SoundDetection, SoundType
from logger import get_logger


class RadarWidget(QWidget):
    """
    Advanced radar widget with directional visualization.
    Can be used as standalone detachable window.
    """

    # Signals
    detection_displayed = pyqtSignal(SoundDetection)

    def __init__(self, parent=None, detached=False):
        super().__init__(parent)
        self.logger = get_logger()
        self.logger.info("Initializing Radar Widget")

        self.detached = detached
        self.opacity = 0.9  # Default opacity

        # Active detections (with fade time)
        self.active_detections = []  # List of (detection, fade_start_time, duration)
        self.fade_duration = 2.0  # seconds

        # Visual settings
        self.radar_colors = {
            SoundType.WALKING: QColor(0, 255, 0, 200),  # Green
            SoundType.RUNNING: QColor(255, 165, 0, 200),  # Orange
            SoundType.SHOOTING: QColor(255, 0, 0, 220),  # Red
        }

        self.background_color = QColor(10, 10, 20, 200)
        self.grid_color = QColor(0, 100, 200, 100)
        self.text_color = QColor(200, 200, 255, 255)

        # Setup UI
        self.setMinimumSize(300, 300)
        if detached:
            self.setWindowTitle("Audio Radar")
            self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)
        else:
            self.setFixedSize(400, 400)

        # Update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update)
        self.update_timer.start(33)  # ~30 FPS

        # For dragging detached window
        self.dragging = False
        self.drag_position = QPoint()

        self.logger.info("Radar Widget initialized successfully")

    def set_opacity(self, opacity: float):
        """Set radar opacity (0.0 - 1.0)."""
        self.opacity = max(0.0, min(1.0, opacity))
        if self.detached:
            self.setWindowOpacity(self.opacity)
        self.update()

    def add_detection(self, detection: SoundDetection):
        """Add a new detection to display on radar."""
        import time
        self.active_detections.append((detection, time.time(), self.fade_duration))
        self.detection_displayed.emit(detection)
        self.logger.debug(f"Detection added to radar: {detection.sound_type.value} at {detection.direction:.1f}°")

    def paintEvent(self, event):
        """Paint the radar display."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Get widget size
        width = self.width()
        height = self.height()
        center_x = width // 2
        center_y = height // 2
        radius = min(width, height) // 2 - 20

        # Draw background
        if not self.detached:
            painter.fillRect(self.rect(), self.background_color)
        else:
            # Rounded background for detached mode
            path = QPainterPath()
            path.addRoundedRect(0, 0, width, height, 10, 10)
            painter.fillPath(path, self.background_color)

        # Draw radar circles
        self._draw_radar_grid(painter, center_x, center_y, radius)

        # Draw direction markers
        self._draw_direction_markers(painter, center_x, center_y, radius)

        # Draw detections
        self._draw_detections(painter, center_x, center_y, radius)

        # Draw center dot
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(100, 200, 255, 255)))
        painter.drawEllipse(center_x - 5, center_y - 5, 10, 10)

    def _draw_radar_grid(self, painter: QPainter, center_x: int, center_y: int, radius: int):
        """Draw radar grid circles."""
        painter.setPen(QPen(self.grid_color, 1))
        painter.setBrush(Qt.NoBrush)

        # Draw concentric circles
        for i in range(1, 5):
            r = radius * i // 4
            painter.drawEllipse(center_x - r, center_y - r, r * 2, r * 2)

        # Draw crosshair lines
        painter.drawLine(center_x, center_y - radius, center_x, center_y + radius)
        painter.drawLine(center_x - radius, center_y, center_x + radius, center_y)

        # Draw diagonal lines
        diag_offset = int(radius * 0.707)  # cos(45°) = sin(45°) ≈ 0.707
        painter.drawLine(center_x - diag_offset, center_y - diag_offset,
                         center_x + diag_offset, center_y + diag_offset)
        painter.drawLine(center_x - diag_offset, center_y + diag_offset,
                         center_x + diag_offset, center_y - diag_offset)

    def _draw_direction_markers(self, painter: QPainter, center_x: int, center_y: int, radius: int):
        """Draw direction markers (N, E, S, W)."""
        painter.setPen(QPen(self.text_color, 1))
        painter.setFont(QFont("Arial", 10, QFont.Bold))

        markers = [
            (0, "N", 0, -radius - 10),
            (90, "E", radius + 10, 0),
            (180, "S", 0, radius + 15),
            (270, "W", -radius - 15, 0)
        ]

        for angle, label, offset_x, offset_y in markers:
            painter.drawText(center_x + offset_x - 10, center_y + offset_y - 5, 20, 20,
                             Qt.AlignCenter, label)

    def _draw_detections(self, painter: QPainter, center_x: int, center_y: int, radius: int):
        """Draw active detections on radar."""
        import time
        current_time = time.time()

        # Remove expired detections
        self.active_detections = [
            d for d in self.active_detections
            if current_time - d[1] < d[2]
        ]

        for detection, start_time, duration in self.active_detections:
            # Calculate fade factor
            elapsed = current_time - start_time
            fade_factor = 1.0 - (elapsed / duration)
            fade_factor = max(0.0, min(1.0, fade_factor))

            # Get color for this detection type
            color = self.radar_colors.get(detection.sound_type, QColor(255, 255, 255, 200))

            # Adjust alpha based on fade
            alpha = int(color.alpha() * fade_factor)
            color.setAlpha(alpha)

            # Calculate position on radar
            # Direction: 0° = North (top), 90° = East (right), etc.
            # Convert to radians (0° = top, clockwise)
            angle_rad = math.radians(detection.direction - 90)  # -90 to make 0° point up

            # Distance scaling (logarithmic for better visualization)
            # Map distance (0-100m) to radius (0-radius)
            max_distance = 50.0  # meters
            distance_normalized = min(detection.distance / max_distance, 1.0)
            distance_radius = distance_normalized * radius

            # Calculate point position
            point_x = center_x + int(distance_radius * math.cos(angle_rad))
            point_y = center_y + int(distance_radius * math.sin(angle_rad))

            # Draw detection indicator
            self._draw_detection_indicator(
                painter, point_x, point_y, detection, color, fade_factor
            )

            # Draw direction line
            painter.setPen(QPen(color, 2))
            painter.drawLine(center_x, center_y, point_x, point_y)

    def _draw_detection_indicator(self, painter: QPainter, x: int, y: int,
                                   detection: SoundDetection, color: QColor, fade_factor: float):
        """Draw detection indicator at specified position."""
        # Draw pulsing circle
        base_size = 15
        pulse_size = int(base_size * (1.0 + 0.3 * (1.0 - fade_factor)))

        # Outer glow
        gradient = QRadialGradient(x, y, pulse_size)
        glow_color = QColor(color)
        glow_color.setAlpha(int(100 * fade_factor))
        gradient.setColorAt(0, color)
        gradient.setColorAt(1, glow_color)

        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(gradient))
        painter.drawEllipse(x - pulse_size, y - pulse_size, pulse_size * 2, pulse_size * 2)

        # Inner dot
        painter.setBrush(QBrush(color))
        dot_size = base_size // 2
        painter.drawEllipse(x - dot_size, y - dot_size, dot_size * 2, dot_size * 2)

        # Draw icon based on type
        self._draw_type_icon(painter, x, y - pulse_size - 10, detection.sound_type, color, fade_factor)

        # Draw distance text
        painter.setPen(QPen(color, 1))
        painter.setFont(QFont("Arial", 8))
        distance_text = f"{detection.distance:.1f}m"
        painter.drawText(x - 20, y + pulse_size + 5, 40, 15, Qt.AlignCenter, distance_text)

        # Draw velocity indicator (arrow)
        if abs(detection.velocity) > 0.5:
            self._draw_velocity_arrow(painter, x, y, detection.velocity, color, fade_factor)

    def _draw_type_icon(self, painter: QPainter, x: int, y: int, sound_type: SoundType,
                        color: QColor, fade_factor: float):
        """Draw icon representing sound type."""
        painter.setPen(QPen(color, 2))
        painter.setFont(QFont("Arial", 10, QFont.Bold))

        if sound_type == SoundType.WALKING:
            icon = "W"
        elif sound_type == SoundType.RUNNING:
            icon = "R"
        elif sound_type == SoundType.SHOOTING:
            icon = "S"
        else:
            icon = "?"

        painter.drawText(x - 10, y - 5, 20, 20, Qt.AlignCenter, icon)

    def _draw_velocity_arrow(self, painter: QPainter, x: int, y: int, velocity: float,
                             color: QColor, fade_factor: float):
        """Draw arrow indicating approach/retreat velocity."""
        arrow_length = min(abs(velocity) * 5, 20)
        arrow_color = QColor(color)
        arrow_color.setAlpha(int(150 * fade_factor))

        painter.setPen(QPen(arrow_color, 2))

        if velocity > 0:  # Approaching
            painter.drawLine(x, y - 5, x, y - 5 - int(arrow_length))
            # Arrow head
            painter.drawLine(x, y - 5 - int(arrow_length), x - 3, y - 2 - int(arrow_length))
            painter.drawLine(x, y - 5 - int(arrow_length), x + 3, y - 2 - int(arrow_length))
        else:  # Retreating
            painter.drawLine(x, y + 5, x, y + 5 + int(arrow_length))
            # Arrow head
            painter.drawLine(x, y + 5 + int(arrow_length), x - 3, y + 2 + int(arrow_length))
            painter.drawLine(x, y + 5 + int(arrow_length), x + 3, y + 2 + int(arrow_length))

    # Mouse events for dragging detached window
    def mousePressEvent(self, event):
        """Handle mouse press for dragging."""
        if self.detached and event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging."""
        if self.detached and self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        """Handle mouse release."""
        if self.detached:
            self.dragging = False
            event.accept()
