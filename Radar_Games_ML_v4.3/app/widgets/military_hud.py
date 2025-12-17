"""
Radar Games ML v4.2.1-k0006 - MilitaryHUDRadar

FIXED v4.2.1-k0006: Extracted from radar.py for improved modularity
Split radar.py (1674 lines) into focused, single-responsibility modules
"""

from typing import Optional
import math
import time

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import (QPainter, QColor, QPen, QBrush, QFont,
                         QRadialGradient, QPainterPath)

from core import log, tr
from .target_state import TargetState


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

        # Colors - IMPROVED v4.3.1-k0007: Better contrast for readability
        self.COLOR_BG = QColor(3, 5, 8)
        self.COLOR_GRID = QColor(0, 80, 100, 120)         # was 60, 80, 80 - brighter grid
        self.COLOR_GRID_MAJOR = QColor(0, 150, 180, 180)  # was 100, 120, 120 - much brighter
        self.COLOR_SWEEP = QColor(0, 255, 100, 150)
        self.COLOR_TEXT = QColor(0, 255, 200)             # was 200, 150 - brighter
        self.COLOR_TEXT_DIM = QColor(0, 180, 150)         # was 120, 100 - 50% brighter
        self.COLOR_ACCENT = QColor(0, 255, 200)
        self.COLOR_WARNING = QColor(255, 200, 0)
        self.COLOR_DANGER = QColor(255, 50, 50)
        self.COLOR_DISTANCE_LABEL = QColor(100, 200, 255) # NEW: distinct blue for distance labels

        # Fonts - IMPROVED v4.3.1-k0007: +30-50% larger for better readability
        self.FONT_MAIN = QFont("Consolas", 12)     # was 9
        self.FONT_LABEL = QFont("Consolas", 11)    # was 8
        self.FONT_STATUS = QFont("Consolas", 13, QFont.Bold)  # was 10
        self.FONT_TITLE = QFont("Consolas", 15, QFont.Bold)   # was 11

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

    def update_sweep(self, angle_deg):
        """Update sweep angle from external source (main tick)"""
        self.sweep_angle = angle_deg % 360
        self.update()

    # =========================================================================
    # TARGET MANAGEMENT
    # =========================================================================

    def add_target(
        self,
        target_id: int,
        angle: float,
        distance: float,
        state: int = TargetState.UNKNOWN,
        speed: float = 0.0,
        label: str = ""
    ) -> None:
        """Add or update a target on the radar (v4.2.1: type hints)."""
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

    def update_target(self, angle_deg, distance):
        """
        Update/add primary target position (compatible with main.py interface)

        Args:
            angle_deg: Angle in degrees (or None to clear)
            distance: Distance value (or None to clear)
        """
        if angle_deg is None or distance is None:
            # Clear primary target
            self.targets = [t for t in self.targets if t['id'] != 0]
            return

        # Update or add primary target (id=0)
        for t in self.targets:
            if t['id'] == 0:
                t['angle'] = angle_deg
                t['distance'] = min(distance, self.max_distance)
                t['last_seen'] = time.time()
                return

        # Add new primary target
        self.targets.append({
            'id': 0,
            'angle': angle_deg,
            'distance': min(distance, self.max_distance),
            'state': TargetState.UNKNOWN,
            'speed': 0,
            'label': 'TARGET',
            'last_seen': time.time()
        })

    def update_target_by_id(self, target_id, angle=None, distance=None, state=None,
                      speed=None):
        """Update specific target properties by ID"""
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

    def remove_target(self, target_id: int) -> None:
        """Remove target from radar (v4.2.1: type hints)."""
        self.targets = [t for t in self.targets if t['id'] != target_id]

    def clear_targets(self) -> None:
        """Clear all targets (v4.2.1: type hints)."""
        self.targets = []

    def cleanup_stale_targets(self, max_age_seconds: float = 3.0) -> None:
        """
        Remove targets that haven't been updated recently (FIXED v4.2.0)
        Defensive cleanup for stuck targets on radar UI
        """
        current_time = time.time()
        before_count = len(self.targets)
        self.targets = [t for t in self.targets
                       if (current_time - t.get('last_seen', current_time)) < max_age_seconds]
        removed = before_count - len(self.targets)
        if removed > 0:
            from core.logger import log
            log(f"MilitaryHUDRadar: Cleaned {removed} stale targets (>{max_age_seconds}s old)", "DEBUG")

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
        self._draw_legend(painter, w, h)  # ADDED v4.3.1-k0007: Icon legend

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

            # Distance labels - IMPROVED v4.3.1-k0007: Distinct color, larger font
            dist_label = f"{int(self.max_distance * ratio)}m"
            painter.setFont(self.FONT_LABEL)  # Now 11pt instead of 8pt
            painter.setPen(self.COLOR_DISTANCE_LABEL)  # Distinct blue instead of dim cyan
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
        """Draw walking person silhouette - IMPROVED v4.3.1-k0007: 50% larger, brighter glow"""
        painter.setPen(QPen(color, 2))
        painter.setBrush(Qt.NoBrush)

        # Head - 50% larger
        painter.drawEllipse(x - 4, y - 18, 9, 9)  # was (x-3, y-12, 6, 6)

        # Body - 50% longer
        painter.drawLine(x, y - 9, x, y + 3)  # was (x, y-6, x, y+2)

        # Arms (one forward, one back) - scaled proportionally
        painter.drawLine(x, y - 6, x - 7, y - 1)  # was (x, y-4, x-5, y-1)
        painter.drawLine(x, y - 6, x + 6, y - 9)  # was (x, y-4, x+4, y-6)

        # Legs (walking stance) - scaled proportionally
        painter.drawLine(x, y + 3, x - 6, y + 15)  # was (x, y+2, x-4, y+10)
        painter.drawLine(x, y + 3, x + 6, y + 15)  # was (x, y+2, x+4, y+10)

        # Glow effect - 2x brighter (100 alpha instead of 50), larger area
        painter.setPen(QPen(QColor(color.red(), color.green(), color.blue(), 100), 8))
        painter.drawEllipse(x - 12, y - 21, 24, 39)  # was (x-8, y-14, 16, 26)

    def _draw_run_icon(self, painter, x, y, color):
        """Draw running person silhouette - IMPROVED v4.3.1-k0007: 50% larger, brighter glow"""
        painter.setPen(QPen(color, 2))
        painter.setBrush(Qt.NoBrush)

        # Head (leaning forward) - 50% larger
        painter.drawEllipse(x + 3, y - 18, 9, 9)  # was (x+2, y-12, 6, 6)

        # Body (angled forward) - scaled proportionally
        painter.drawLine(x + 7, y - 9, x - 3, y + 3)  # was (x+5, y-6, x-2, y+2)

        # Arms (dynamic running pose) - scaled proportionally
        painter.drawLine(x + 1, y - 4, x - 9, y - 12)  # was (x+1, y-3, x-6, y-8)
        painter.drawLine(x + 1, y - 4, x + 12, y)  # was (x+1, y-3, x+8, y)

        # Legs (wide running stride) - scaled proportionally
        painter.drawLine(x - 3, y + 3, x - 12, y + 15)  # was (x-2, y+2, x-8, y+10)
        painter.drawLine(x - 3, y + 3, x + 9, y + 12)  # was (x-2, y+2, x+6, y+8)

        # Speed lines - brighter and more visible
        painter.setPen(QPen(QColor(color.red(), color.green(), color.blue(), 150), 2))  # was 100 alpha, 1px
        painter.drawLine(x - 15, y - 3, x - 22, y - 3)  # was (x-10, y-2, x-15, y-2)
        painter.drawLine(x - 15, y + 3, x - 21, y + 3)  # was (x-10, y+2, x-14, y+2)
        painter.drawLine(x - 15, y + 9, x - 19, y + 9)  # was (x-10, y+6, x-13, y+6)

        # Glow effect - 2x brighter (100 alpha instead of 50), larger area
        painter.setPen(QPen(QColor(color.red(), color.green(), color.blue(), 100), 8))
        painter.drawEllipse(x - 15, y - 21, 30, 39)  # was (x-10, y-14, 20, 26)

    def _draw_shot_icon(self, painter, x, y, color):
        """Draw bullet/shot icon - IMPROVED v4.3.1-k0007: 50% larger, brighter effects"""
        painter.setPen(QPen(color, 2))
        painter.setBrush(QBrush(color))

        # Bullet shape (pointed oval) - 50% larger
        path = QPainterPath()
        path.moveTo(x + 12, y)  # was x+8
        path.lineTo(x - 6, y - 6)  # was x-4, y-4
        path.lineTo(x - 9, y)  # was x-6
        path.lineTo(x - 6, y + 6)  # was x-4, y+4
        path.closeSubpath()
        painter.drawPath(path)

        # Muzzle flash lines - longer and brighter
        painter.setPen(QPen(color.lighter(150), 2))  # was 1px thick
        painter.drawLine(x - 12, y, x - 21, y)  # was (x-8, y, x-14, y)
        painter.drawLine(x - 10, y - 4, x - 18, y - 7)  # was (x-7, y-3, x-12, y-5)
        painter.drawLine(x - 10, y + 4, x - 18, y + 7)  # was (x-7, y+3, x-12, y+5)

        # Impact ring effect - larger and brighter
        painter.setPen(QPen(QColor(255, 100, 100, 120), 3))  # was 80 alpha, 2px
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(x - 15, y - 15, 30, 30)  # was (x-10, y-10, 20, 20)

    def _draw_left_panel(self, painter, panel_width):
        """Draw left panel - Target list"""
        h = self.height() - 40
        x = 5
        y = 5

        # Panel background - IMPROVED v4.3.1-k0007: Higher opacity for better text contrast
        painter.fillRect(x, y, panel_width - 10, h - 10,
                        QColor(0, 20, 30, 240))  # was (0, 15, 20, 200) - now 94% opaque
        painter.setPen(QPen(self.COLOR_GRID_MAJOR, 1))
        painter.drawRect(x, y, panel_width - 10, h - 10)

        # Title
        painter.setFont(self.FONT_TITLE)
        painter.setPen(self.COLOR_ACCENT)
        painter.drawText(x + 10, y + 20, tr('targets'))

        # Separator line
        painter.setPen(QPen(self.COLOR_GRID, 1))
        painter.drawLine(x + 5, y + 28, x + panel_width - 15, y + 28)

        # Target list - IMPROVED v4.3.1-k0007: Better spacing, show more targets
        painter.setFont(self.FONT_LABEL)  # Now 11pt instead of 8pt
        ty = y + 50
        for i, target in enumerate(self.targets[:10]):  # Max 10 targets shown (was 8)
            state_color = TargetState.COLORS.get(target['state'], self.COLOR_TEXT_DIM)
            state_label = TargetState.LABELS.get(target['state'], "???")

            # Status indicator - slightly larger
            painter.setBrush(QBrush(state_color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(x + 10, ty - 5, 8, 8)  # was 6x6

            # Target info
            painter.setPen(state_color)
            painter.drawText(x + 22, ty + 2,
                           f"T{target['id']:02d} {target['distance']:.0f}m")
            painter.setPen(self.COLOR_TEXT_DIM)
            painter.drawText(x + 22, ty + 14,
                           f"{state_label} {target['speed']:.1f}m/s")

            ty += 40  # was 32 - 25% more spacing

        # Count - IMPROVED v4.3.1-k0007: Show overflow indicator
        painter.setFont(self.FONT_LABEL)
        if len(self.targets) > 10:
            painter.setPen(self.COLOR_WARNING)
            painter.drawText(x + 10, h - 35, f"▼ +{len(self.targets) - 10} more")
            painter.setPen(self.COLOR_TEXT_DIM)
        else:
            painter.setPen(self.COLOR_TEXT_DIM)
        painter.drawText(x + 10, h - 20, f"{tr('count')}: {len(self.targets)}")

    def _draw_right_panel(self, painter, w, panel_width):
        """Draw right panel - Tactical data"""
        h = self.height() - 40
        x = w - panel_width + 5
        y = 5

        # Panel background - IMPROVED v4.3.1-k0007: Higher opacity for better text contrast
        painter.fillRect(x, y, panel_width - 10, h - 10,
                        QColor(0, 20, 30, 240))  # was (0, 15, 20, 200) - now 94% opaque
        painter.setPen(QPen(self.COLOR_GRID_MAJOR, 1))
        painter.drawRect(x, y, panel_width - 10, h - 10)

        # Title
        painter.setFont(self.FONT_TITLE)
        painter.setPen(self.COLOR_ACCENT)
        painter.drawText(x + 10, y + 20, tr('tactical'))

        # Separator
        painter.setPen(QPen(self.COLOR_GRID, 1))
        painter.drawLine(x + 5, y + 28, x + panel_width - 15, y + 28)

        # System data
        painter.setFont(self.FONT_LABEL)
        ty = y + 50

        # Mode
        painter.setPen(self.COLOR_TEXT_DIM)
        painter.drawText(x + 10, ty, tr('mode_label'))
        painter.setPen(self.COLOR_ACCENT)
        painter.drawText(x + 55, ty, self.scan_mode)
        ty += 20

        # Range
        painter.setPen(self.COLOR_TEXT_DIM)
        painter.drawText(x + 10, ty, tr('range_label'))
        painter.setPen(self.COLOR_TEXT)
        painter.drawText(x + 55, ty, self.range_mode)
        ty += 20

        # Lock status
        painter.setPen(self.COLOR_TEXT_DIM)
        painter.drawText(x + 10, ty, tr('lock_label'))
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
        painter.drawText(x + 10, ty, tr('statistics'))
        ty += 18

        walk_count = sum(1 for t in self.targets if t['state'] == TargetState.WALK)
        run_count = sum(1 for t in self.targets if t['state'] == TargetState.RUN)
        shot_count = sum(1 for t in self.targets if t['state'] == TargetState.SHOT)

        painter.setPen(TargetState.COLORS[TargetState.WALK])
        painter.drawText(x + 10, ty, f"{tr('walk')}: {walk_count}")
        ty += 16
        painter.setPen(TargetState.COLORS[TargetState.RUN])
        painter.drawText(x + 10, ty, f"{tr('run')}:  {run_count}")
        ty += 16
        painter.setPen(TargetState.COLORS[TargetState.SHOT])
        painter.drawText(x + 10, ty, f"{tr('shot')}: {shot_count}")

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
            (tr('scan'), self.scan_mode == "ACTIVE", 50),
            (tr('lock'), "LOCK" in self.lock_status, 150),
            (tr('range'), True, 250),
            (tr('audio'), True, 350),
            (tr('system'), True, 450),
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

    def _draw_legend(self, painter, w, h):
        """Draw legend showing target types - ADDED v4.3.1-k0007: Better UX"""
        legend_width = 160
        legend_height = 110
        x = w - legend_width - 10
        y = h - legend_height - 50  # Above status bar

        # Legend background
        painter.fillRect(x, y, legend_width, legend_height,
                        QColor(0, 20, 30, 240))
        painter.setPen(QPen(self.COLOR_GRID_MAJOR, 1))
        painter.drawRect(x, y, legend_width, legend_height)

        # Title
        painter.setFont(self.FONT_STATUS)
        painter.setPen(self.COLOR_ACCENT)
        painter.drawText(x + 10, y + 20, tr('legend'))

        # Separator
        painter.setPen(QPen(self.COLOR_GRID, 1))
        painter.drawLine(x + 5, y + 26, x + legend_width - 5, y + 26)

        # Legend items
        painter.setFont(self.FONT_LABEL)
        legend_y = y + 45

        # Walk
        self._draw_walk_icon(painter, x + 25, legend_y,
                            TargetState.COLORS[TargetState.WALK])
        painter.setPen(TargetState.COLORS[TargetState.WALK])
        painter.drawText(x + 50, legend_y + 5, tr('walk'))
        legend_y += 26

        # Run
        self._draw_run_icon(painter, x + 25, legend_y,
                           TargetState.COLORS[TargetState.RUN])
        painter.setPen(TargetState.COLORS[TargetState.RUN])
        painter.drawText(x + 50, legend_y + 5, tr('run'))
        legend_y += 26

        # Shot
        self._draw_shot_icon(painter, x + 25, legend_y,
                            TargetState.COLORS[TargetState.SHOT])
        painter.setPen(TargetState.COLORS[TargetState.SHOT])
        painter.drawText(x + 50, legend_y + 5, tr('shot'))


# =============================================================================
# MINIMAL RADAR WIDGET (RADAR ONLY - NO PANELS)
# =============================================================================

