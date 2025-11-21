"""
RadarSuite v3.5.0 - Radar Widgets
"""

import math
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QSlider, QCheckBox, QSpinBox, QGroupBox, QFormLayout
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QPalette

from core import log, tr, VERSION, TOAST_DURATION_MS, TOAST_MAX_COUNT


class DetachableRadarWidget(QWidget):
    """
    Independent radar widget that can be detached from main window
    Works even when main window is minimized
    """

    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window | Qt.WindowStaysOnTopHint)
        log("DetachableRadarWidget.__init__", "INFO")

        self.setWindowTitle(f"{tr('radar')} - RadarSuite {VERSION}")
        self.setGeometry(100, 100, 500, 500)

        # Frameless mode
        self.is_frameless = False

        # Opacity
        self.window_opacity = 1.0
        self.setWindowOpacity(self.window_opacity)

        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Radar plot
        self.radar = RadarWidget()
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



class RadarWidget(pg.PlotWidget):
    """Radar visualization using pyqtgraph"""

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


# ============================================================================
# 3D SPHERE RADAR WIDGET (v3.0.4 - Module 4)
# ============================================================================


class Radar3DWidget(gl.GLViewWidget):
    """
    3D Sphere Radar visualization using OpenGL
    Provides full 3D spatial awareness with azimuth, elevation, and distance
    Interactive rotation and zoom for better threat assessment
    """

    def __init__(self):
        super().__init__()
        log("Radar3DWidget.__init__", "INFO")

        # Visual settings
        self.setBackgroundColor('#050505')
        self.setCameraPosition(distance=150, elevation=20, azimuth=45)

        # Create sphere grid (distance rings at 25m, 50m, 75m, 100m)
        self.sphere_items = []
        for radius in [25, 50, 75, 100]:
            # Create wireframe sphere
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

        # Create coordinate axes
        axis_length = 110
        axis_width = 2

        # X axis (red) - Left/Right
        x_axis = gl.GLLinePlotItem(
            pos=np.array([[0, 0, 0], [axis_length, 0, 0]]),
            color=(1, 0, 0, 0.8),
            width=axis_width,
            antialias=True
        )
        self.addItem(x_axis)

        # Y axis (green) - Forward/Backward
        y_axis = gl.GLLinePlotItem(
            pos=np.array([[0, 0, 0], [0, axis_length, 0]]),
            color=(0, 1, 0, 0.8),
            width=axis_width,
            antialias=True
        )
        self.addItem(y_axis)

        # Z axis (blue) - Up/Down
        z_axis = gl.GLLinePlotItem(
            pos=np.array([[0, 0, 0], [0, 0, axis_length]]),
            color=(0, 0, 1, 0.8),
            width=axis_width,
            antialias=True
        )
        self.addItem(z_axis)

        # Create horizontal grid at z=0
        grid = gl.GLGridItem()
        grid.scale(10, 10, 1)
        grid.setColor((0.3, 0.3, 0.3, 0.5))
        self.addItem(grid)

        # Target scatter plot (multiple targets support)
        self.targets = []
        self.target_scatter = gl.GLScatterPlotItem(
            pos=np.array([[0, 0, 0]]),
            color=(1, 0, 0, 0),  # Initially invisible
            size=12,
            pxMode=True
        )
        self.addItem(self.target_scatter)

        # Sweep indicator (rotating line on horizontal plane)
        self.sweep_line_3d = gl.GLLinePlotItem(
            pos=np.array([[0, 0, 0], [0, 100, 0]]),
            color=(0, 1, 0, 0.6),
            width=2,
            antialias=True
        )
        self.addItem(self.sweep_line_3d)
        self.sweep_angle = 0

    def update_sweep(self, angle_deg):
        """Update 3D sweep line angle (rotates on horizontal plane)"""
        self.sweep_angle = angle_deg
        angle_rad = math.radians(angle_deg - 90)

        # Sweep on XY plane
        x = 100 * math.cos(angle_rad)
        y = 100 * math.sin(angle_rad)

        self.sweep_line_3d.setData(
            pos=np.array([[0, 0, 0], [x, y, 0]]),
            color=(0, 1, 0, 0.6),
            width=2
        )

    def update_target(self, angle_deg, distance, elevation_deg=0):
        """
        Update target position in 3D space

        Args:
            angle_deg: Horizontal angle (azimuth) in degrees (0-360)
            distance: Distance in meters (0-100)
            elevation_deg: Vertical angle in degrees (-90 to +90)
                          Negative = below, Positive = above, 0 = horizontal
        """
        if angle_deg is None or distance is None:
            # Clear targets
            self.target_scatter.setData(
                pos=np.array([[0, 0, 0]]),
                color=(1, 0, 0, 0)  # Invisible
            )
            self.targets = []
            return

        # Clamp values
        distance = max(5, min(100, distance))
        elevation_deg = max(-90, min(90, elevation_deg))

        # Convert spherical to Cartesian coordinates
        # Azimuth: angle_deg (0° = forward/+Y, 90° = right/+X)
        # Elevation: elevation_deg (positive = up/+Z, negative = down/-Z)
        angle_rad = math.radians(angle_deg - 90)
        elevation_rad = math.radians(elevation_deg)

        # Calculate 3D position
        # horizontal_distance is the projection on the XY plane
        horizontal_distance = distance * math.cos(elevation_rad)
        x = horizontal_distance * math.cos(angle_rad)
        y = horizontal_distance * math.sin(angle_rad)
        z = distance * math.sin(elevation_rad)

        # Update target (single target for now, multi-target in Module 5)
        self.targets = [(x, y, z)]

        # Set target color based on elevation
        if elevation_deg > 15:
            color = (1, 0.5, 0, 1)  # Orange for above
        elif elevation_deg < -15:
            color = (0.5, 0, 1, 1)  # Purple for below
        else:
            color = (1, 0, 0, 1)  # Red for horizontal

        self.target_scatter.setData(
            pos=np.array([[x, y, z]]),
            color=color,
            size=12
        )

    def add_target(self, angle_deg, distance, elevation_deg=0, color=None):
        """
        Add a target to the 3D radar (for multi-target support in Module 5)

        Args:
            angle_deg: Horizontal angle (azimuth)
            distance: Distance in meters
            elevation_deg: Vertical angle (elevation)
            color: RGBA tuple (optional)
        """
        # Convert to 3D coordinates
        angle_rad = math.radians(angle_deg - 90)
        elevation_rad = math.radians(elevation_deg)

        horizontal_distance = distance * math.cos(elevation_rad)
        x = horizontal_distance * math.cos(angle_rad)
        y = horizontal_distance * math.sin(angle_rad)
        z = distance * math.sin(elevation_rad)

        self.targets.append((x, y, z))

        # Update scatter plot with all targets
        if self.targets:
            positions = np.array(self.targets)
            colors = np.array([(1, 0, 0, 1)] * len(self.targets)) if color is None else np.array([color] * len(self.targets))

            self.target_scatter.setData(
                pos=positions,
                color=colors,
                size=12
            )

    def clear_targets(self):
        """Clear all targets from the radar"""
        self.targets = []
        self.target_scatter.setData(
            pos=np.array([[0, 0, 0]]),
            color=(1, 0, 0, 0)
        )


# ============================================================================
# MULTI-TARGET TRACKER (v3.0.5 - Module 5)
# ============================================================================




