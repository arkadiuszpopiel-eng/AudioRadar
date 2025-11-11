"""Dark theme manager for AudioRadar v10.2.

This module provides a dark theme stylesheet for the PyQt5 GUI.
"""

def get_dark_theme() -> str:
    """Return dark theme stylesheet for PyQt5 application.
    
    Returns
    -------
    str
        CSS-like stylesheet for PyQt5 widgets.
    """
    return """
    QMainWindow {
        background-color: #1e1e1e;
    }
    QWidget {
        background-color: #1e1e1e;
        color: #d4d4d4;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 10pt;
    }
    QLabel {
        color: #d4d4d4;
        background-color: transparent;
    }
    QPushButton {
        background-color: #0e639c;
        color: white;
        border: 1px solid #0e639c;
        border-radius: 4px;
        padding: 6px 12px;
        min-width: 80px;
    }
    QPushButton:hover {
        background-color: #1177bb;
        border: 1px solid #1177bb;
    }
    QPushButton:pressed {
        background-color: #0d5689;
    }
    QPushButton:disabled {
        background-color: #3e3e3e;
        color: #808080;
        border: 1px solid #3e3e3e;
    }
    QComboBox {
        background-color: #3c3c3c;
        border: 1px solid #555555;
        border-radius: 4px;
        padding: 4px;
        color: #d4d4d4;
    }
    QComboBox:hover {
        border: 1px solid #0e639c;
    }
    QComboBox::drop-down {
        border: none;
    }
    QComboBox::down-arrow {
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid #d4d4d4;
        margin-right: 5px;
    }
    QSlider::groove:horizontal {
        border: 1px solid #3c3c3c;
        height: 8px;
        background: #3c3c3c;
        border-radius: 4px;
    }
    QSlider::handle:horizontal {
        background: #0e639c;
        border: 1px solid #0e639c;
        width: 18px;
        margin: -5px 0;
        border-radius: 9px;
    }
    QSlider::handle:horizontal:hover {
        background: #1177bb;
        border: 1px solid #1177bb;
    }
    QProgressBar {
        border: 1px solid #3c3c3c;
        border-radius: 4px;
        text-align: center;
        background-color: #3c3c3c;
    }
    QProgressBar::chunk {
        background-color: #0e639c;
        border-radius: 3px;
    }
    QTextEdit, QPlainTextEdit {
        background-color: #252526;
        border: 1px solid #3c3c3c;
        border-radius: 4px;
        color: #d4d4d4;
        padding: 4px;
    }
    QGroupBox {
        border: 1px solid #3c3c3c;
        border-radius: 4px;
        margin-top: 8px;
        padding-top: 8px;
        font-weight: bold;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 5px;
        color: #d4d4d4;
    }
    QStatusBar {
        background-color: #007acc;
        color: white;
    }
    """


class ThemeManager:
    """Manager for application themes."""
    
    @staticmethod
    def apply_dark_theme(app):
        """Apply dark theme to the application.
        
        Parameters
        ----------
        app : QApplication
            The Qt application instance to theme.
        """
        app.setStyleSheet(get_dark_theme())
