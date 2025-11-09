"""Theme Manager for AudioRadar v10.2"""
from PyQt5.QtWidgets import QApplication


class ThemeManager:
    """Manages application themes and styling"""
    
    @staticmethod
    def apply_dark_theme(app: QApplication):
        """Apply dark theme to the application"""
        dark_stylesheet = """
        QWidget {
            background-color: #1e1e1e;
            color: #e0e0e0;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 10pt;
        }
        QLabel {
            color: #e0e0e0;
        }
        QPushButton {
            background-color: #2d2d2d;
            border: 1px solid #3d3d3d;
            padding: 5px 15px;
            border-radius: 3px;
        }
        QPushButton:hover {
            background-color: #3d3d3d;
        }
        QPushButton:pressed {
            background-color: #0d7377;
        }
        QComboBox {
            background-color: #2d2d2d;
            border: 1px solid #3d3d3d;
            padding: 3px;
            border-radius: 3px;
        }
        QSlider::groove:horizontal {
            border: 1px solid #3d3d3d;
            height: 8px;
            background: #2d2d2d;
            margin: 2px 0;
            border-radius: 4px;
        }
        QSlider::handle:horizontal {
            background: #0d7377;
            border: 1px solid #0d7377;
            width: 18px;
            margin: -5px 0;
            border-radius: 9px;
        }
        QSlider::handle:horizontal:hover {
            background: #14b8be;
        }
        """
        app.setStyleSheet(dark_stylesheet)
