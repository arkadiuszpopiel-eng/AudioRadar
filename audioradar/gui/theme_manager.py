"""
Theme manager for Audio Radar GUI.
Handles dark and light themes.
"""

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt


class ThemeManager:
    """Manages application themes."""
    
    DARK_THEME = "dark"
    LIGHT_THEME = "light"
    
    @staticmethod
    def apply_theme(app: QApplication, theme: str = DARK_THEME):
        """
        Apply theme to application.
        
        Args:
            app: QApplication instance
            theme: Theme name ('dark' or 'light')
        """
        if theme == ThemeManager.DARK_THEME:
            ThemeManager._apply_dark_theme(app)
        else:
            ThemeManager._apply_light_theme(app)
    
    @staticmethod
    def _apply_dark_theme(app: QApplication):
        """Apply dark theme."""
        palette = QPalette()
        
        # Base colors
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        
        # Disabled colors
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127))
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127))
        
        app.setPalette(palette)
        
        # Additional stylesheet
        app.setStyleSheet("""
            QToolTip {
                color: #ffffff;
                background-color: #2a82da;
                border: 1px solid white;
            }
            QPushButton {
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 5px;
                background-color: #3d3d3d;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
            }
            QPushButton:pressed {
                background-color: #2d2d2d;
            }
            QGroupBox {
                border: 1px solid #555555;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
            }
        """)
    
    @staticmethod
    def _apply_light_theme(app: QApplication):
        """Apply light theme."""
        palette = QPalette()
        
        # Base colors
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.WindowText, Qt.black)
        palette.setColor(QPalette.Base, Qt.white)
        palette.setColor(QPalette.AlternateBase, QColor(233, 233, 233))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.black)
        palette.setColor(QPalette.Text, Qt.black)
        palette.setColor(QPalette.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ButtonText, Qt.black)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(0, 0, 255))
        palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
        palette.setColor(QPalette.HighlightedText, Qt.white)
        
        # Disabled colors
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(120, 120, 120))
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(120, 120, 120))
        
        app.setPalette(palette)
        
        # Additional stylesheet
        app.setStyleSheet("""
            QToolTip {
                color: #000000;
                background-color: #ffffcc;
                border: 1px solid black;
            }
            QPushButton {
                border: 1px solid #cccccc;
                border-radius: 3px;
                padding: 5px;
                background-color: #f0f0f0;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
            QGroupBox {
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
            }
        """)
    
    @staticmethod
    def get_radar_colors(theme: str) -> dict:
        """
        Get radar-specific colors for theme.
        
        Args:
            theme: Theme name
        
        Returns:
            Dictionary of color values
        """
        if theme == ThemeManager.DARK_THEME:
            return {
                'background': QColor(25, 25, 25, 200),
                'grid': QColor(80, 80, 80),
                'text': QColor(200, 200, 200),
                'footstep': QColor(0, 255, 0),
                'running': QColor(255, 255, 0),
                'gunshot': QColor(255, 0, 0),
            }
        else:
            return {
                'background': QColor(240, 240, 240, 200),
                'grid': QColor(180, 180, 180),
                'text': QColor(50, 50, 50),
                'footstep': QColor(0, 200, 0),
                'running': QColor(200, 200, 0),
                'gunshot': QColor(200, 0, 0),
            }
