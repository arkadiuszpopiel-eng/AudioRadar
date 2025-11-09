"""Theme management for AudioRadar v10.0 PyQt5 interface.

This module provides a centralized theme management system with a dark theme
featuring cyan accents. The dark theme is optimized for low-light gaming
environments and reduces eye strain during extended use.

The ThemeManager class provides static methods to apply themes to PyQt5
applications. The architecture is designed to be extensible for future
light theme support.
"""

from __future__ import annotations
from typing import Optional

# v10.0: PyQt5 imports for theme application
try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtGui import QPalette, QColor
    from PyQt5.QtCore import Qt
    PYQT5_AVAILABLE = True
except ImportError:
    QApplication = None  # type: ignore
    PYQT5_AVAILABLE = False


class ThemeManager:
    """Manage application themes for AudioRadar.
    
    This class provides static methods to apply consistent styling across
    the entire application. The dark theme uses a cyan accent color (#0d7377)
    that provides good contrast while being easy on the eyes.
    
    All widgets receive comprehensive styling through Qt Style Sheets (QSS)
    to ensure a cohesive visual experience.
    """
    
    # v10.0: Theme color definitions
    ACCENT_COLOR = "#0d7377"  # Cyan accent
    DARK_BG = "#1e1e1e"  # Main background
    DARKER_BG = "#151515"  # Darker background for contrast
    LIGHT_TEXT = "#e0e0e0"  # Primary text
    DIM_TEXT = "#888888"  # Secondary text
    BORDER_COLOR = "#2d2d2d"  # Widget borders
    HOVER_COLOR = "#0a5a5d"  # Hover state for accent elements
    DISABLED_COLOR = "#3a3a3a"  # Disabled widgets
    
    @staticmethod
    def apply_dark_theme(app: QApplication) -> bool:
        """Apply dark theme with cyan accents to the application.
        
        This method configures both the QPalette for native Qt widgets and
        applies a comprehensive QSS stylesheet for custom styling. The theme
        covers all major widget types including buttons, input fields, lists,
        sliders, and status indicators.
        
        Parameters
        ----------
        app : QApplication
            The PyQt5 application instance to theme.
        
        Returns
        -------
        bool
            True if theme was applied successfully, False if PyQt5 is unavailable.
        """
        if not PYQT5_AVAILABLE or app is None:
            return False
        
        try:
            # v10.0: Configure base palette for Qt widgets
            palette = QPalette()
            
            # Window and base colors
            palette.setColor(QPalette.Window, QColor(ThemeManager.DARK_BG))
            palette.setColor(QPalette.WindowText, QColor(ThemeManager.LIGHT_TEXT))
            palette.setColor(QPalette.Base, QColor(ThemeManager.DARKER_BG))
            palette.setColor(QPalette.AlternateBase, QColor(ThemeManager.DARK_BG))
            
            # Text colors
            palette.setColor(QPalette.Text, QColor(ThemeManager.LIGHT_TEXT))
            palette.setColor(QPalette.BrightText, Qt.white)
            palette.setColor(QPalette.ToolTipBase, QColor(ThemeManager.DARKER_BG))
            palette.setColor(QPalette.ToolTipText, QColor(ThemeManager.LIGHT_TEXT))
            
            # Button colors
            palette.setColor(QPalette.Button, QColor(ThemeManager.DARK_BG))
            palette.setColor(QPalette.ButtonText, QColor(ThemeManager.LIGHT_TEXT))
            
            # Highlight colors (selection, focus)
            palette.setColor(QPalette.Highlight, QColor(ThemeManager.ACCENT_COLOR))
            palette.setColor(QPalette.HighlightedText, Qt.white)
            
            # Disabled state
            palette.setColor(QPalette.Disabled, QPalette.Text, QColor(ThemeManager.DIM_TEXT))
            palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(ThemeManager.DIM_TEXT))
            palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(ThemeManager.DIM_TEXT))
            
            app.setPalette(palette)
            
            # v10.0: Apply comprehensive QSS stylesheet
            stylesheet = f"""
                /* Main Window and Widgets */
                QMainWindow {{
                    background-color: {ThemeManager.DARK_BG};
                }}
                
                QWidget {{
                    background-color: {ThemeManager.DARK_BG};
                    color: {ThemeManager.LIGHT_TEXT};
                    font-family: 'Segoe UI', Arial, sans-serif;
                    font-size: 9pt;
                }}
                
                /* Push Buttons */
                QPushButton {{
                    background-color: {ThemeManager.DARKER_BG};
                    color: {ThemeManager.LIGHT_TEXT};
                    border: 1px solid {ThemeManager.BORDER_COLOR};
                    border-radius: 4px;
                    padding: 6px 12px;
                    min-width: 80px;
                    font-weight: bold;
                }}
                
                QPushButton:hover {{
                    background-color: {ThemeManager.ACCENT_COLOR};
                    border-color: {ThemeManager.ACCENT_COLOR};
                }}
                
                QPushButton:pressed {{
                    background-color: {ThemeManager.HOVER_COLOR};
                }}
                
                QPushButton:disabled {{
                    background-color: {ThemeManager.DISABLED_COLOR};
                    color: {ThemeManager.DIM_TEXT};
                    border-color: {ThemeManager.DISABLED_COLOR};
                }}
                
                /* ComboBox (Dropdown) */
                QComboBox {{
                    background-color: {ThemeManager.DARKER_BG};
                    color: {ThemeManager.LIGHT_TEXT};
                    border: 1px solid {ThemeManager.BORDER_COLOR};
                    border-radius: 4px;
                    padding: 4px 8px;
                    min-width: 150px;
                }}
                
                QComboBox:hover {{
                    border-color: {ThemeManager.ACCENT_COLOR};
                }}
                
                QComboBox::drop-down {{
                    border: none;
                    width: 20px;
                }}
                
                QComboBox::down-arrow {{
                    image: none;
                    border-left: 4px solid transparent;
                    border-right: 4px solid transparent;
                    border-top: 5px solid {ThemeManager.LIGHT_TEXT};
                    margin-right: 5px;
                }}
                
                QComboBox QAbstractItemView {{
                    background-color: {ThemeManager.DARKER_BG};
                    color: {ThemeManager.LIGHT_TEXT};
                    selection-background-color: {ThemeManager.ACCENT_COLOR};
                    border: 1px solid {ThemeManager.BORDER_COLOR};
                }}
                
                /* Spin Box */
                QSpinBox {{
                    background-color: {ThemeManager.DARKER_BG};
                    color: {ThemeManager.LIGHT_TEXT};
                    border: 1px solid {ThemeManager.BORDER_COLOR};
                    border-radius: 4px;
                    padding: 4px 8px;
                }}
                
                QSpinBox:hover {{
                    border-color: {ThemeManager.ACCENT_COLOR};
                }}
                
                /* Labels */
                QLabel {{
                    background: transparent;
                    color: {ThemeManager.LIGHT_TEXT};
                }}
                
                /* Group Box */
                QGroupBox {{
                    border: 1px solid {ThemeManager.BORDER_COLOR};
                    border-radius: 5px;
                    margin-top: 10px;
                    padding-top: 10px;
                    font-weight: bold;
                }}
                
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                    color: {ThemeManager.ACCENT_COLOR};
                }}
                
                /* Status Bar */
                QStatusBar {{
                    background-color: {ThemeManager.DARKER_BG};
                    color: {ThemeManager.LIGHT_TEXT};
                    border-top: 1px solid {ThemeManager.BORDER_COLOR};
                }}
                
                QStatusBar::item {{
                    border: none;
                }}
                
                /* List Widget */
                QListWidget {{
                    background-color: {ThemeManager.DARKER_BG};
                    color: {ThemeManager.LIGHT_TEXT};
                    border: 1px solid {ThemeManager.BORDER_COLOR};
                    border-radius: 4px;
                }}
                
                QListWidget::item:selected {{
                    background-color: {ThemeManager.ACCENT_COLOR};
                }}
                
                QListWidget::item:hover {{
                    background-color: {ThemeManager.HOVER_COLOR};
                }}
                
                /* Slider */
                QSlider::groove:horizontal {{
                    height: 6px;
                    background: {ThemeManager.DARKER_BG};
                    border: 1px solid {ThemeManager.BORDER_COLOR};
                    border-radius: 3px;
                }}
                
                QSlider::handle:horizontal {{
                    background: {ThemeManager.ACCENT_COLOR};
                    border: 1px solid {ThemeManager.ACCENT_COLOR};
                    width: 14px;
                    margin: -5px 0;
                    border-radius: 7px;
                }}
                
                QSlider::handle:horizontal:hover {{
                    background: {ThemeManager.HOVER_COLOR};
                }}
                
                /* Scroll Bar */
                QScrollBar:vertical {{
                    background: {ThemeManager.DARKER_BG};
                    width: 12px;
                    border: none;
                }}
                
                QScrollBar::handle:vertical {{
                    background: {ThemeManager.BORDER_COLOR};
                    border-radius: 6px;
                    min-height: 20px;
                }}
                
                QScrollBar::handle:vertical:hover {{
                    background: {ThemeManager.ACCENT_COLOR};
                }}
                
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                    height: 0px;
                }}
                
                /* Tool Tip */
                QToolTip {{
                    background-color: {ThemeManager.DARKER_BG};
                    color: {ThemeManager.LIGHT_TEXT};
                    border: 1px solid {ThemeManager.ACCENT_COLOR};
                    padding: 4px;
                    border-radius: 3px;
                }}
                
                /* Menu Bar */
                QMenuBar {{
                    background-color: {ThemeManager.DARKER_BG};
                    color: {ThemeManager.LIGHT_TEXT};
                }}
                
                QMenuBar::item:selected {{
                    background-color: {ThemeManager.ACCENT_COLOR};
                }}
                
                QMenu {{
                    background-color: {ThemeManager.DARKER_BG};
                    color: {ThemeManager.LIGHT_TEXT};
                    border: 1px solid {ThemeManager.BORDER_COLOR};
                }}
                
                QMenu::item:selected {{
                    background-color: {ThemeManager.ACCENT_COLOR};
                }}
            """
            
            app.setStyleSheet(stylesheet)
            return True
            
        except Exception as e:
            # If theme application fails, continue without theme
            return False
    
    @staticmethod
    def get_accent_color() -> str:
        """Get the current accent color hex code.
        
        Returns
        -------
        str
            Hex color code for the accent color.
        """
        return ThemeManager.ACCENT_COLOR
