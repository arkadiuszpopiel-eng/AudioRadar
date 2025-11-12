"""
Advanced circular radar visualization widget.
Displays detected audio events in 360-degree view with decay animations.
"""

import math
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, QPointF, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath
from typing import List, Tuple
import time


class RadarEvent:
    """Represents an event on the radar."""
    
    def __init__(self, event_type: str, angle: float, distance: float, 
                 confidence: float, timestamp: float):
        self.type = event_type
        self.angle = angle  # 0-360 degrees
        self.distance = distance  # 0-1 (0=far, 1=close)
        self.confidence = confidence  # 0-1
        self.timestamp = timestamp
        self.age = 0.0  # seconds since detection
    
    def update_age(self, current_time: float):
        """Update event age."""
        self.age = current_time - self.timestamp
    
    def get_opacity(self, decay_time: float) -> float:
        """Get opacity based on age and decay time."""
        if self.age >= decay_time:
            return 0.0
        return 1.0 - (self.age / decay_time)


class RadarWidget(QWidget):
    """Advanced circular radar visualization."""
    
    # Signals
    eventClicked = pyqtSignal(str, float, float)  # type, angle, distance
    
    def __init__(self, size: int = 400, transparency: int = 80, parent=None):
        """
        Initialize radar widget.
        
        Args:
            size: Radar diameter in pixels
            transparency: Transparency percentage (10-100)
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.radar_size = size
        self.transparency = max(10, min(100, transparency))
        self.decay_time = 2.0  # seconds
        
        # Event storage
        self.events: List[RadarEvent] = []
        
        # Colors
        self.colors = {
            'footstep': QColor(0, 255, 0),
            'running': QColor(255, 255, 0),
            'gunshot': QColor(255, 0, 0),
        }
        
        # Theme colors (will be updated by theme manager)
        self.bg_color = QColor(25, 25, 25, 200)
        self.grid_color = QColor(80, 80, 80)
        self.text_color = QColor(200, 200, 200)
        
        # Setup widget
        self.setMinimumSize(size, size)
        self.setMaximumSize(size * 2, size * 2)
        
        # Update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_events)
        self.update_timer.start(33)  # ~30 FPS
        
        self.setMouseTracking(True)
    
    def add_event(self, event_type: str, angle: float, distance: float, 
                  confidence: float = 1.0):
        """
        Add event to radar.
        
        Args:
            event_type: 'footstep', 'running', or 'gunshot'
            angle: Direction in degrees (0-360)
            distance: Distance (0-1, where 1 is closest)
            confidence: Detection confidence (0-1)
        """
        event = RadarEvent(event_type, angle, distance, confidence, time.time())
        self.events.append(event)
        
        # Limit number of events
        if len(self.events) > 100:
            self.events = self.events[-100:]
        
        self.update()
    
    def clear_events(self):
        """Clear all events from radar."""
        self.events.clear()
        self.update()
    
    def set_decay_time(self, decay_time: float):
        """Set event decay time in seconds."""
        self.decay_time = max(0.5, decay_time)
    
    def set_transparency(self, transparency: int):
        """Set radar transparency (10-100)."""
        self.transparency = max(10, min(100, transparency))
        self.update()
    
    def set_colors(self, theme_colors: dict):
        """Update colors from theme."""
        if 'background' in theme_colors:
            self.bg_color = theme_colors['background']
        if 'grid' in theme_colors:
            self.grid_color = theme_colors['grid']
        if 'text' in theme_colors:
            self.text_color = theme_colors['text']
        if 'footstep' in theme_colors:
            self.colors['footstep'] = theme_colors['footstep']
        if 'running' in theme_colors:
            self.colors['running'] = theme_colors['running']
        if 'gunshot' in theme_colors:
            self.colors['gunshot'] = theme_colors['gunshot']
        
        self.update()
    
    def _update_events(self):
        """Update event ages and remove old events."""
        current_time = time.time()
        
        # Update ages and remove expired events
        self.events = [
            event for event in self.events
            if (event.update_age(current_time) or True) and event.age < self.decay_time
        ]
        
        self.update()
    
    def paintEvent(self, event):
        """Paint the radar display."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Get widget dimensions
        width = self.width()
        height = self.height()
        size = min(width, height)
        center_x = width // 2
        center_y = height // 2
        radius = (size // 2) - 20
        
        # Apply transparency
        opacity = self.transparency / 100.0
        
        # Draw background
        bg = QColor(self.bg_color)
        bg.setAlpha(int(bg.alpha() * opacity))
        painter.fillRect(0, 0, width, height, bg)
        
        # Draw radar circles
        self._draw_radar_circles(painter, center_x, center_y, radius)
        
        # Draw cardinal directions
        self._draw_directions(painter, center_x, center_y, radius)
        
        # Draw events
        self._draw_events(painter, center_x, center_y, radius)
        
        # Draw center dot
        painter.setPen(QPen(self.text_color, 2))
        painter.setBrush(QBrush(self.text_color))
        painter.drawEllipse(QPointF(center_x, center_y), 3, 3)
    
    def _draw_radar_circles(self, painter: QPainter, cx: int, cy: int, radius: int):
        """Draw concentric circles."""
        painter.setPen(QPen(self.grid_color, 1, Qt.DotLine))
        painter.setBrush(Qt.NoBrush)
        
        # Draw 4 circles at 25%, 50%, 75%, 100%
        for i in range(1, 5):
            r = radius * i // 4
            painter.drawEllipse(QPointF(cx, cy), r, r)
    
    def _draw_directions(self, painter: QPainter, cx: int, cy: int, radius: int):
        """Draw cardinal direction lines and labels."""
        painter.setPen(QPen(self.grid_color, 1))
        font = QFont("Arial", 10)
        painter.setFont(font)
        
        directions = [
            (0, "N"),
            (90, "E"),
            (180, "S"),
            (270, "W"),
        ]
        
        for angle, label in directions:
            # Convert to radians (0 degrees = North = up)
            rad = math.radians(angle - 90)
            
            # Line endpoints
            x1 = cx + int(radius * 0.9 * math.cos(rad))
            y1 = cy + int(radius * 0.9 * math.sin(rad))
            x2 = cx + int(radius * math.cos(rad))
            y2 = cy + int(radius * math.sin(rad))
            
            painter.drawLine(x1, y1, x2, y2)
            
            # Label position
            label_x = cx + int(radius * 1.1 * math.cos(rad))
            label_y = cy + int(radius * 1.1 * math.sin(rad))
            
            # Draw label
            painter.setPen(QPen(self.text_color))
            painter.drawText(label_x - 10, label_y - 10, 20, 20, 
                           Qt.AlignCenter, label)
            painter.setPen(QPen(self.grid_color, 1))
    
    def _draw_events(self, painter: QPainter, cx: int, cy: int, radius: int):
        """Draw events on radar."""
        for event in self.events:
            opacity = event.get_opacity(self.decay_time)
            if opacity <= 0:
                continue
            
            # Get event color
            color = self.colors.get(event.type, QColor(255, 255, 255))
            color = QColor(color)
            color.setAlpha(int(255 * opacity))
            
            # Calculate position
            # angle 0 = North (up), angle increases clockwise
            angle_rad = math.radians(event.angle - 90)
            distance_pixels = radius * event.distance
            
            x = cx + int(distance_pixels * math.cos(angle_rad))
            y = cy + int(distance_pixels * math.sin(angle_rad))
            
            # Draw event marker
            size = int(10 + event.confidence * 10)
            
            painter.setPen(QPen(color, 2))
            painter.setBrush(QBrush(color))
            
            if event.type == 'footstep':
                # Circle for footstep
                painter.drawEllipse(QPointF(x, y), size // 2, size // 2)
            elif event.type == 'running':
                # Larger pulsing circle for running
                pulse_size = size + int(5 * math.sin(event.age * 10))
                painter.drawEllipse(QPointF(x, y), pulse_size // 2, pulse_size // 2)
            elif event.type == 'gunshot':
                # Star for gunshot
                self._draw_star(painter, x, y, size, color)
    
    def _draw_star(self, painter: QPainter, x: int, y: int, size: int, color: QColor):
        """Draw a star shape."""
        path = QPainterPath()
        points = 5
        outer_radius = size
        inner_radius = size // 2
        
        for i in range(points * 2):
            angle = math.pi * i / points - math.pi / 2
            radius = outer_radius if i % 2 == 0 else inner_radius
            px = x + int(radius * math.cos(angle))
            py = y + int(radius * math.sin(angle))
            
            if i == 0:
                path.moveTo(px, py)
            else:
                path.lineTo(px, py)
        
        path.closeSubpath()
        painter.fillPath(path, QBrush(color))
    
    def resizeEvent(self, event):
        """Handle widget resize."""
        super().resizeEvent(event)
        self.update()
