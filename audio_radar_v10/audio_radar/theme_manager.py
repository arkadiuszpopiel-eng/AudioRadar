"""
AudioRadar v10.0 - Theme Manager
Provides dark theme stylesheet for PyQt5
"""


class ThemeManager:
    """Manages application themes"""
    
    @staticmethod
    def apply_dark_theme(app):
        """Apply dark theme to PyQt5 application"""
        dark_stylesheet = """
        QMainWindow {
            background-color: #1e1e1e;
        }
        
        QWidget {
            background-color: #2d2d2d;
            color: #e0e0e0;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 10pt;
        }
        
        QPushButton {
            background-color: #3d3d3d;
            border: 1px solid #4d4d4d;
            border-radius: 4px;
            padding: 8px 16px;
            color: #00ffff;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: #4d4d4d;
            border-color: #00ffff;
        }
        
        QPushButton:pressed {
            background-color: #2d2d2d;
        }
        
        QPushButton:disabled {
            background-color: #2d2d2d;
            color: #666666;
            border-color: #3d3d3d;
        }
        
        QLabel {
            color: #e0e0e0;
            background-color: transparent;
        }
        
        QStatusBar {
            background-color: #1e1e1e;
            color: #00ffff;
            border-top: 1px solid #3d3d3d;
        }
        
        QTextEdit, QListWidget {
            background-color: #1e1e1e;
            color: #e0e0e0;
            border: 1px solid #3d3d3d;
            border-radius: 4px;
            padding: 4px;
        }
        
        QComboBox {
            background-color: #3d3d3d;
            border: 1px solid #4d4d4d;
            border-radius: 4px;
            padding: 4px;
            color: #e0e0e0;
        }
        
        QComboBox:hover {
            border-color: #00ffff;
        }
        
        QComboBox::drop-down {
            border: none;
        }
        
        QComboBox QAbstractItemView {
            background-color: #2d2d2d;
            color: #e0e0e0;
            selection-background-color: #3d3d3d;
            selection-color: #00ffff;
            border: 1px solid #4d4d4d;
        }
        
        QToolTip {
            background-color: #2d2d2d;
            color: #00ffff;
            border: 1px solid #00ffff;
            padding: 4px;
        }
        """
        app.setStyleSheet(dark_stylesheet)
