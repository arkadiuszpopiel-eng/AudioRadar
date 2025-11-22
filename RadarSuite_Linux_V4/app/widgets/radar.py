"""
RadarSuite v3.5.0 - Military Sci-Fi HUD Radar
Ultra-readable military radar interface with Walk/Run/Shot indicators
"""

import math
import time
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QGridLayout, QSizePolicy)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPoint, QRectF, QPointF
from PyQt5.QtGui import (QPainter, QColor, QPen, QBrush, QPalette, QFont,
                         QLinearGradient, QRadialGradient, QPainterPath,
                         QPolygonF)

from core import log, tr, VERSION


# =============================================================================
# TARGET STATE ICONS - Walk / Run / Shot
# =============================================================================

class TargetState:
    """Target movement states"""
    UNKNOWN = 0
    WALK = 1
    RUN = 2
    SHOT = 3

    LABELS = {
        UNKNOWN: "???",
        WALK: "WALK",
        RUN: "RUN",
        SHOT: "SHOT"
    }

    COLORS = {
        UNKNOWN: QColor(100, 100, 100),
        WALK: QColor(0, 200, 100),      # Green
        RUN: QColor(255, 200, 0),       # Yellow/Orange
        SHOT: QColor(255, 50, 50)       # Red
    }


# =============================================================================
# MILITARY SCI-FI HUD RADAR WIDGET
# =============================================================================

class MilitaryHUDRadar(QWidget):
    """
    Military Sci-Fi HUD Radar Display

    Features:
    - Central radar with concentric circles and grid
    - Walk/Run/Shot target icons with labels
    - Left panel: Target list with distance/speed
    - Right panel: Tactical data and system status
    - Bottom panel: Status bar (LOCK, SCAN, RANGE)
    """

    target_clicked = pyqtSignal(int)  # Signal when target is clicked

    def __init__(self, parent=None):
        super().__init__(parent)
        log("MilitaryHUDRadar.__init__", "INFO")

        self.setMinimumSize(600, 500)
        self.setStyleSheet("background-color: #030508;")

        # Colors
        self.COLOR_BG = QColor(3, 5, 8)
        self.COLOR_GRID = QColor(0, 60, 80, 80)
        self.COLOR_GRID_MAJOR = QColor(0, 100, 120, 120)
        self.COLOR_SWEEP = QColor(0, 255, 100, 150)
        self.COLOR_TEXT = QColor(0, 200, 150)
        self.COLOR_TEXT_DIM = QColor(0, 120, 100)
        self.COLOR_ACCENT = QColor(0, 255, 200)
        self.COLOR_WARNING = QColor(255, 200, 0)
        self.COLOR_DANGER = QColor(255, 50, 50)

        # Fonts
        self.FONT_MAIN = QFont("Consolas", 9)
        self.FONT_LABEL = QFont("Consolas", 8)
        self.FONT_STATUS = QFont("Consolas", 10, QFont.Bold)
        self.FONT_TITLE = QFont("Consolas", 11, QFont.Bold)

        # Radar state
        self.sweep_angle = 0
        self.radar_radius = 180
        self.max_distance = 100  # meters

        # Targets: list of dict {id, angle, distance, state, speed, label}
        self.targets = []
        self.selected_target_id = None

        # System status
        self.scan_mode = "ACTIVE"
        self.lock_status = "SCANNING"
        self.range_mode = "100m"

        # Animation timer
        self.sweep_timer = QTimer()
        self.sweep_timer.timeout.connect(self._update_sweep)
        self.sweep_timer.start(50)  # 20 FPS sweep

        # Performance tracking
        self.last_update_time = time.time()
        self.fps = 0

    def _update_sweep(self):
        """Update sweep line animation"""
        self.sweep_angle = (self.sweep_angle + 3) % 360
        self.update()

    # =========================================================================
    # TARGET MANAGEMENT
    # =========================================================================

    def add_target(self, target_id, angle, distance, state=TargetState.UNKNOWN,
                   speed=0, label=""):
        """Add or update a target on the radar"""
        # Check if target exists
        for t in self.targets:
            if t['id'] == target_id:
                t['angle'] = angle
                t['distance'] = min(distance, self.max_distance)
                t['state'] = state
                t['speed'] = speed
                t['label'] = label
                t['last_seen'] = time.time()
                return

        # Add new target
        self.targets.append({
            'id': target_id,
            'angle': angle,
            'distance': min(distance, self.max_distance),
            'state': state,
            'speed': speed,
            'label': label,
            'last_seen': time.time()
        })

    def update_target(self, target_id, angle=None, distance=None, state=None,
                      speed=None):
        """Update specific target properties"""
        for t in self.targets:
            if t['id'] == target_id:
                if angle is not None:
                    t['angle'] = angle
                if distance is not None:
                    t['distance'] = min(distance, self.max_distance)
                if state is not None:
                    t['state'] = state
                if speed is not None:
                    t['speed'] = speed
                t['last_seen'] = time.time()
                return

    def remove_target(self, target_id):
        """Remove target from radar"""
        self.targets = [t for t in self.targets if t['id'] != target_id]

    def clear_targets(self):
        """Clear all targets"""
        self.targets = []

    def set_system_status(self, scan_mode=None, lock_status=None, range_mode=None):
        """Update system status indicators"""
        if scan_mode:
            self.scan_mode = scan_mode
        if lock_status:
            self.lock_status = lock_status
        if range_mode:
            self.range_mode = range_mode

    # =========================================================================
    # PAINTING
    # =========================================================================

    def paintEvent(self, event):
        """Main paint event - draws entire HUD"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)

        # Get dimensions
        w = self.width()
        h = self.height()

        # Calculate radar center and radius
        panel_width = 150
        status_height = 40
        radar_area_w = w - panel_width * 2
        radar_area_h = h - status_height
        self.radar_radius = min(radar_area_w, radar_area_h) // 2 - 20
        center_x = w // 2
        center_y = (h - status_height) // 2

        # Draw background
        painter.fillRect(0, 0, w, h, self.COLOR_BG)

        # Draw components
        self._draw_radar_grid(painter, center_x, center_y)
        self._draw_sweep_line(painter, center_x, center_y)
        self._draw_targets(painter, center_x, center_y)
        self._draw_left_panel(painter, panel_width)
        self._draw_right_panel(painter, w, panel_width)
        self._draw_status_bar(painter, w, h, status_height)
        self._draw_corner_decorations(painter, w, h)

    def _draw_radar_grid(self, painter, cx, cy):
        """Draw radar grid with concentric circles and coordinate lines"""
        r = self.radar_radius

        # Background glow
        gradient = QRadialGradient(cx, cy, r)
        gradient.setColorAt(0, QColor(0, 30, 40, 60))
        gradient.setColorAt(0.7, QColor(0, 20, 30, 30))
        gradient.setColorAt(1, QColor(0, 10, 15, 10))
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(cx - r, cy - r, r * 2, r * 2)

        # Concentric circles
        for i, ratio in enumerate([0.25, 0.5, 0.75, 1.0]):
            radius = int(r * ratio)
            if ratio == 1.0:
                painter.setPen(QPen(self.COLOR_GRID_MAJOR, 2))
            else:
                painter.setPen(QPen(self.COLOR_GRID, 1))
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(cx - radius, cy - radius, radius * 2, radius * 2)

            # Distance labels
            dist_label = f"{int(self.max_distance * ratio)}m"
            painter.setFont(self.FONT_LABEL)
            painter.setPen(self.COLOR_TEXT_DIM)
            painter.drawText(cx + 5, cy - radius + 12, dist_label)

        # Radial lines (every 30 degrees)
        painter.setPen(QPen(self.COLOR_GRID, 1))
        for angle in range(0, 360, 30):
            rad = math.radians(angle - 90)
            x1 = cx + int(r * 0.1 * math.cos(rad))
            y1 = cy + int(r * 0.1 * math.sin(rad))
            x2 = cx + int(r * math.cos(rad))
            y2 = cy + int(r * math.sin(rad))
            painter.drawLine(x1, y1, x2, y2)

        # Cardinal direction labels
        painter.setFont(self.FONT_STATUS)
        painter.setPen(self.COLOR_TEXT)
        offset = r + 15
        painter.drawText(cx - 5, cy - offset, "N")
        painter.drawText(cx - 5, cy + offset + 10, "S")
        painter.drawText(cx + offset, cy + 5, "E")
        painter.drawText(cx - offset - 10, cy + 5, "W")

        # Cross-hair at center
        painter.setPen(QPen(self.COLOR_ACCENT, 1))
        ch_size = 10
        painter.drawLine(cx - ch_size, cy, cx + ch_size, cy)
        painter.drawLine(cx, cy - ch_size, cx, cy + ch_size)

    def _draw_sweep_line(self, painter, cx, cy):
        """Draw rotating sweep line with trail effect"""
        r = self.radar_radius

        # Trail effect (fading arc)
        for i in range(30):
            trail_angle = self.sweep_angle - i * 2
            alpha = int(150 * (1 - i / 30))
            rad = math.radians(trail_angle - 90)
            x = cx + int(r * math.cos(rad))
            y = cy + int(r * math.sin(rad))
            painter.setPen(QPen(QColor(0, 255, 100, alpha), 1))
            painter.drawLine(cx, cy, x, y)

        # Main sweep line
        rad = math.radians(self.sweep_angle - 90)
        x = cx + int(r * math.cos(rad))
        y = cy + int(r * math.sin(rad))
        painter.setPen(QPen(self.COLOR_SWEEP, 2))
        painter.drawLine(cx, cy, x, y)

    def _draw_targets(self, painter, cx, cy):
        """Draw all targets with state icons"""
        r = self.radar_radius

        for target in self.targets:
            # Calculate position
            angle_rad = math.radians(target['angle'] - 90)
            dist_ratio = target['distance'] / self.max_distance
            tx = cx + int(r * dist_ratio * math.cos(angle_rad))
            ty = cy + int(r * dist_ratio * math.sin(angle_rad))

            # Get state color
            state_color = TargetState.COLORS.get(target['state'], self.COLOR_TEXT)

            # Draw target based on state
            if target['state'] == TargetState.WALK:
                self._draw_walk_icon(painter, tx, ty, state_color)
            elif target['state'] == TargetState.RUN:
                self._draw_run_icon(painter, tx, ty, state_color)
            elif target['state'] == TargetState.SHOT:
                self._draw_shot_icon(painter, tx, ty, state_color)
            else:
                # Unknown - simple dot
                painter.setBrush(QBrush(state_color))
                painter.setPen(QPen(state_color.lighter(150), 2))
                painter.drawEllipse(tx - 6, ty - 6, 12, 12)

            # Draw state label
            label = TargetState.LABELS.get(target['state'], "???")
            painter.setFont(self.FONT_LABEL)
            painter.setPen(state_color)
            painter.drawText(tx + 12, ty + 4, label)

            # Draw target ID/label if exists
            if target['label']:
                painter.drawText(tx + 12, ty + 16, target['label'])

    def _draw_walk_icon(self, painter, x, y, color):
        """Draw walking person silhouette"""
        painter.setPen(QPen(color, 2))
        painter.setBrush(Qt.NoBrush)

        # Head
        painter.drawEllipse(x - 3, y - 12, 6, 6)

        # Body
        painter.drawLine(x, y - 6, x, y + 2)

        # Arms (one forward, one back)
        painter.drawLine(x, y - 4, x - 5, y - 1)
        painter.drawLine(x, y - 4, x + 4, y - 6)

        # Legs (walking stance)
        painter.drawLine(x, y + 2, x - 4, y + 10)
        painter.drawLine(x, y + 2, x + 4, y + 10)

        # Glow effect
        painter.setPen(QPen(QColor(color.red(), color.green(), color.blue(), 50), 6))
        painter.drawEllipse(x - 8, y - 14, 16, 26)

    def _draw_run_icon(self, painter, x, y, color):
        """Draw running person silhouette"""
        painter.setPen(QPen(color, 2))
        painter.setBrush(Qt.NoBrush)

        # Head (leaning forward)
        painter.drawEllipse(x + 2, y - 12, 6, 6)

        # Body (angled forward)
        painter.drawLine(x + 5, y - 6, x - 2, y + 2)

        # Arms (dynamic running pose)
        painter.drawLine(x + 1, y - 3, x - 6, y - 8)
        painter.drawLine(x + 1, y - 3, x + 8, y)

        # Legs (wide running stride)
        painter.drawLine(x - 2, y + 2, x - 8, y + 10)
        painter.drawLine(x - 2, y + 2, x + 6, y + 8)

        # Speed lines
        painter.setPen(QPen(QColor(color.red(), color.green(), color.blue(), 100), 1))
        painter.drawLine(x - 10, y - 2, x - 15, y - 2)
        painter.drawLine(x - 10, y + 2, x - 14, y + 2)
        painter.drawLine(x - 10, y + 6, x - 13, y + 6)

        # Glow effect
        painter.setPen(QPen(QColor(color.red(), color.green(), color.blue(), 50), 6))
        painter.drawEllipse(x - 10, y - 14, 20, 26)

    def _draw_shot_icon(self, painter, x, y, color):
        """Draw bullet/shot icon"""
        painter.setPen(QPen(color, 2))
        painter.setBrush(QBrush(color))

        # Bullet shape (pointed oval)
        path = QPainterPath()
        path.moveTo(x + 8, y)
        path.lineTo(x - 4, y - 4)
        path.lineTo(x - 6, y)
        path.lineTo(x - 4, y + 4)
        path.closeSubpath()
        painter.drawPath(path)

        # Muzzle flash lines
        painter.setPen(QPen(color.lighter(150), 1))
        painter.drawLine(x - 8, y, x - 14, y)
        painter.drawLine(x - 7, y - 3, x - 12, y - 5)
        painter.drawLine(x - 7, y + 3, x - 12, y + 5)

        # Impact ring effect
        painter.setPen(QPen(QColor(255, 100, 100, 80), 2))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(x - 10, y - 10, 20, 20)

    def _draw_left_panel(self, painter, panel_width):
        """Draw left panel - Target list"""
        h = self.height() - 40
        x = 5
        y = 5

        # Panel background
        painter.fillRect(x, y, panel_width - 10, h - 10,
                        QColor(0, 15, 20, 200))
        painter.setPen(QPen(self.COLOR_GRID_MAJOR, 1))
        painter.drawRect(x, y, panel_width - 10, h - 10)

        # Title
        painter.setFont(self.FONT_TITLE)
        painter.setPen(self.COLOR_ACCENT)
        painter.drawText(x + 10, y + 20, "TARGETS")

        # Separator line
        painter.setPen(QPen(self.COLOR_GRID, 1))
        painter.drawLine(x + 5, y + 28, x + panel_width - 15, y + 28)

        # Target list
        painter.setFont(self.FONT_LABEL)
        ty = y + 45
        for i, target in enumerate(self.targets[:8]):  # Max 8 targets shown
            state_color = TargetState.COLORS.get(target['state'], self.COLOR_TEXT_DIM)
            state_label = TargetState.LABELS.get(target['state'], "???")

            # Status indicator
            painter.setBrush(QBrush(state_color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(x + 10, ty - 4, 6, 6)

            # Target info
            painter.setPen(state_color)
            painter.drawText(x + 20, ty,
                           f"T{target['id']:02d} {target['distance']:.0f}m")
            painter.setPen(self.COLOR_TEXT_DIM)
            painter.drawText(x + 20, ty + 12,
                           f"{state_label} {target['speed']:.1f}m/s")

            ty += 32

        # Count
        painter.setFont(self.FONT_LABEL)
        painter.setPen(self.COLOR_TEXT_DIM)
        painter.drawText(x + 10, h - 20, f"COUNT: {len(self.targets)}")

    def _draw_right_panel(self, painter, w, panel_width):
        """Draw right panel - Tactical data"""
        h = self.height() - 40
        x = w - panel_width + 5
        y = 5

        # Panel background
        painter.fillRect(x, y, panel_width - 10, h - 10,
                        QColor(0, 15, 20, 200))
        painter.setPen(QPen(self.COLOR_GRID_MAJOR, 1))
        painter.drawRect(x, y, panel_width - 10, h - 10)

        # Title
        painter.setFont(self.FONT_TITLE)
        painter.setPen(self.COLOR_ACCENT)
        painter.drawText(x + 10, y + 20, "TACTICAL")

        # Separator
        painter.setPen(QPen(self.COLOR_GRID, 1))
        painter.drawLine(x + 5, y + 28, x + panel_width - 15, y + 28)

        # System data
        painter.setFont(self.FONT_LABEL)
        ty = y + 50

        # Mode
        painter.setPen(self.COLOR_TEXT_DIM)
        painter.drawText(x + 10, ty, "MODE:")
        painter.setPen(self.COLOR_ACCENT)
        painter.drawText(x + 55, ty, self.scan_mode)
        ty += 20

        # Range
        painter.setPen(self.COLOR_TEXT_DIM)
        painter.drawText(x + 10, ty, "RANGE:")
        painter.setPen(self.COLOR_TEXT)
        painter.drawText(x + 55, ty, self.range_mode)
        ty += 20

        # Lock status
        painter.setPen(self.COLOR_TEXT_DIM)
        painter.drawText(x + 10, ty, "LOCK:")
        if "LOCK" in self.lock_status:
            painter.setPen(self.COLOR_DANGER)
        else:
            painter.setPen(self.COLOR_TEXT)
        painter.drawText(x + 55, ty, self.lock_status)
        ty += 30

        # Separator
        painter.setPen(QPen(self.COLOR_GRID, 1))
        painter.drawLine(x + 5, ty - 5, x + panel_width - 15, ty - 5)
        ty += 15

        # Statistics
        painter.setPen(self.COLOR_TEXT_DIM)
        painter.drawText(x + 10, ty, "STATISTICS")
        ty += 18

        walk_count = sum(1 for t in self.targets if t['state'] == TargetState.WALK)
        run_count = sum(1 for t in self.targets if t['state'] == TargetState.RUN)
        shot_count = sum(1 for t in self.targets if t['state'] == TargetState.SHOT)

        painter.setPen(TargetState.COLORS[TargetState.WALK])
        painter.drawText(x + 10, ty, f"WALK: {walk_count}")
        ty += 16
        painter.setPen(TargetState.COLORS[TargetState.RUN])
        painter.drawText(x + 10, ty, f"RUN:  {run_count}")
        ty += 16
        painter.setPen(TargetState.COLORS[TargetState.SHOT])
        painter.drawText(x + 10, ty, f"SHOT: {shot_count}")

        # FPS counter at bottom
        current_time = time.time()
        if current_time - self.last_update_time > 0:
            self.fps = 1.0 / (current_time - self.last_update_time + 0.001)
        self.last_update_time = current_time

        painter.setPen(self.COLOR_TEXT_DIM)
        painter.drawText(x + 10, h - 20, f"FPS: {self.fps:.0f}")

    def _draw_status_bar(self, painter, w, h, bar_height):
        """Draw bottom status bar"""
        y = h - bar_height

        # Background
        painter.fillRect(0, y, w, bar_height, QColor(0, 20, 25, 230))
        painter.setPen(QPen(self.COLOR_GRID_MAJOR, 1))
        painter.drawLine(0, y, w, y)

        # Status items
        painter.setFont(self.FONT_STATUS)
        items = [
            ("SCAN", self.scan_mode == "ACTIVE", 50),
            ("LOCK", "LOCK" in self.lock_status, 150),
            ("RANGE", True, 250),
            ("AUDIO", True, 350),
            ("SYS", True, 450),
        ]

        for label, active, x_pos in items:
            if active:
                # Active indicator box
                painter.fillRect(x_pos - 5, y + 8, 60, 24,
                               QColor(0, 60, 50, 150))
                painter.setPen(self.COLOR_ACCENT)
            else:
                painter.setPen(self.COLOR_TEXT_DIM)

            painter.drawText(x_pos, y + 26, label)

        # Timestamp
        painter.setPen(self.COLOR_TEXT_DIM)
        timestamp = time.strftime("%H:%M:%S")
        painter.drawText(w - 80, y + 26, timestamp)

    def _draw_corner_decorations(self, painter, w, h):
        """Draw sci-fi corner decorations"""
        painter.setPen(QPen(self.COLOR_GRID_MAJOR, 2))
        corner_size = 20

        # Top-left
        painter.drawLine(0, corner_size, 0, 0)
        painter.drawLine(0, 0, corner_size, 0)

        # Top-right
        painter.drawLine(w - corner_size, 0, w, 0)
        painter.drawLine(w, 0, w, corner_size)

        # Bottom-left
        painter.drawLine(0, h - corner_size, 0, h)
        painter.drawLine(0, h, corner_size, h)

        # Bottom-right
        painter.drawLine(w - corner_size, h, w, h)
        painter.drawLine(w, h - corner_size, w, h)


# =============================================================================
# DETACHABLE RADAR WINDOW
# =============================================================================

class DetachableRadarWidget(QWidget):
    """
    Independent radar widget that can be detached from main window
    Works even when main window is minimized
    """

    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window | Qt.WindowStaysOnTopHint)
        log("DetachableRadarWidget.__init__", "INFO")

        self.setWindowTitle(f"{tr('radar')} - RadarSuite {VERSION}")
        self.setGeometry(100, 100, 700, 600)

        # Frameless mode
        self.is_frameless = False

        # Opacity
        self.window_opacity = 1.0
        self.setWindowOpacity(self.window_opacity)

        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Military HUD Radar (new style)
        self.radar = MilitaryHUDRadar()
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


# =============================================================================
# LEGACY RADAR WIDGET (for compatibility)
# =============================================================================

class RadarWidget(pg.PlotWidget):
    """Legacy Radar visualization using pyqtgraph - kept for compatibility"""

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


# =============================================================================
# 3D SPHERE RADAR WIDGET (v3.0.4 - Module 4)
# =============================================================================

class Radar3DWidget(gl.GLViewWidget):
    """
    3D Sphere Radar visualization using OpenGL
    Provides full 3D spatial awareness with azimuth, elevation, and distance
    """

    def __init__(self):
        super().__init__()
        log("Radar3DWidget.__init__", "INFO")

        self.setBackgroundColor('#050505')
        self.setCameraPosition(distance=150, elevation=20, azimuth=45)

        # Create sphere grid
        self.sphere_items = []
        for radius in [25, 50, 75, 100]:
            md = gl.MeshData.sphere(rows=20, cols=20, radius=radius)
            sphere = gl.GLMeshItem(
                meshdata=md,
                color=(0, 0.4, 0.8, 0.15),
                shader='balloon',
                drawEdges=True,
                edgeColor=(0, 0.4, 0.8, 0.3),
                smooth=False
            )
            self.addItem(sphere)
            self.sphere_items.append(sphere)

        # Coordinate axes
        axis_length = 110
        axis_width = 2

        x_axis = gl.GLLinePlotItem(
            pos=np.array([[0, 0, 0], [axis_length, 0, 0]]),
            color=(1, 0, 0, 0.8), width=axis_width, antialias=True
        )
        self.addItem(x_axis)

        y_axis = gl.GLLinePlotItem(
            pos=np.array([[0, 0, 0], [0, axis_length, 0]]),
            color=(0, 1, 0, 0.8), width=axis_width, antialias=True
        )
        self.addItem(y_axis)

        z_axis = gl.GLLinePlotItem(
            pos=np.array([[0, 0, 0], [0, 0, axis_length]]),
            color=(0, 0, 1, 0.8), width=axis_width, antialias=True
        )
        self.addItem(z_axis)

        # Grid
        grid = gl.GLGridItem()
        grid.scale(10, 10, 1)
        grid.setColor((0.3, 0.3, 0.3, 0.5))
        self.addItem(grid)

        # Target scatter
        self.targets = []
        self.target_scatter = gl.GLScatterPlotItem(
            pos=np.array([[0, 0, 0]]),
            color=(1, 0, 0, 0), size=12, pxMode=True
        )
        self.addItem(self.target_scatter)

        # Sweep line
        self.sweep_line_3d = gl.GLLinePlotItem(
            pos=np.array([[0, 0, 0], [0, 100, 0]]),
            color=(0, 1, 0, 0.6), width=2, antialias=True
        )
        self.addItem(self.sweep_line_3d)
        self.sweep_angle = 0

    def update_sweep(self, angle_deg):
        """Update 3D sweep line angle"""
        self.sweep_angle = angle_deg
        angle_rad = math.radians(angle_deg - 90)
        x = 100 * math.cos(angle_rad)
        y = 100 * math.sin(angle_rad)
        self.sweep_line_3d.setData(
            pos=np.array([[0, 0, 0], [x, y, 0]]),
            color=(0, 1, 0, 0.6), width=2
        )

    def update_target(self, angle_deg, distance, elevation_deg=0):
        """Update target position in 3D space"""
        if angle_deg is None or distance is None:
            self.target_scatter.setData(
                pos=np.array([[0, 0, 0]]),
                color=(1, 0, 0, 0)
            )
            self.targets = []
            return

        distance = max(5, min(100, distance))
        elevation_deg = max(-90, min(90, elevation_deg))

        angle_rad = math.radians(angle_deg - 90)
        elevation_rad = math.radians(elevation_deg)

        horizontal_distance = distance * math.cos(elevation_rad)
        x = horizontal_distance * math.cos(angle_rad)
        y = horizontal_distance * math.sin(angle_rad)
        z = distance * math.sin(elevation_rad)

        self.targets = [(x, y, z)]

        if elevation_deg > 15:
            color = (1, 0.5, 0, 1)
        elif elevation_deg < -15:
            color = (0.5, 0, 1, 1)
        else:
            color = (1, 0, 0, 1)

        self.target_scatter.setData(
            pos=np.array([[x, y, z]]),
            color=color, size=12
        )

    def clear_targets(self):
        """Clear all targets"""
        self.targets = []
        self.target_scatter.setData(
            pos=np.array([[0, 0, 0]]),
            color=(1, 0, 0, 0)
        )
