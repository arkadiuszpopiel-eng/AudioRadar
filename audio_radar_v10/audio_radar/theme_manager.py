"""
AudioRadar v10.1 - Theme Manager
Provides dark theme styling for PyQt5 application
"""
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt


class ThemeManager:
    """Manages application themes and styling"""
    
    @staticmethod
    def apply_dark_theme(app: QApplication):
        """Apply dark theme to the application
        
        Args:
            app: QApplication instance
        """
        # Set dark palette
        dark_palette = QPalette()
        
        # Window colors
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        
        # Base colors (for input fields, etc.)
        dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        
        # Tooltip colors
        dark_palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        
        # Text colors
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.PlaceholderText, QColor(127, 127, 127))
        
        # Button colors
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        
        # Bright text (for disabled items)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        
        # Link colors
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.LinkVisited, QColor(94, 53, 177))
        
        # Highlight colors (cyan accent)
        dark_palette.setColor(QPalette.Highlight, QColor(0, 255, 255))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        
        # Disabled colors
        dark_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127))
        dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127))
        dark_palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127))
        dark_palette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(80, 80, 80))
        dark_palette.setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(127, 127, 127))
        
        # Apply palette
        app.setPalette(dark_palette)
        
        # Additional stylesheet for fine-tuning
        app.setStyleSheet("""
            QToolTip {
                color: #ffffff;
                background-color: #2a2a2a;
                border: 1px solid #00ffff;
                padding: 5px;
            }
            
            QTabWidget::pane {
                border: 1px solid #444;
                background-color: #353535;
            }
            
            QTabBar::tab {
                background-color: #353535;
                color: #ffffff;
                padding: 8px 20px;
                margin-right: 2px;
                border: 1px solid #444;
                border-bottom: none;
            }
            
            QTabBar::tab:selected {
                background-color: #00ffff;
                color: #000000;
                font-weight: bold;
            }
            
            QTabBar::tab:hover {
                background-color: #404040;
            }
            
            QGroupBox {
                border: 2px solid #444;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                color: #00ffff;
            }
            
            QPushButton {
                border: 2px solid #555;
                border-radius: 5px;
                padding: 5px;
                min-height: 25px;
            }
            
            QPushButton:hover {
                border: 2px solid #00ffff;
                background-color: #404040;
            }
            
            QPushButton:pressed {
                background-color: #252525;
            }
            
            QPushButton:disabled {
                border: 2px solid #333;
                color: #666;
            }
            
            QComboBox {
                border: 2px solid #555;
                border-radius: 5px;
                padding: 5px;
                background-color: #353535;
            }
            
            QComboBox:hover {
                border: 2px solid #00ffff;
            }
            
            QComboBox::drop-down {
                border: none;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #00ffff;
                margin-right: 5px;
            }
            
            QScrollBar:vertical {
                border: none;
                background-color: #353535;
                width: 12px;
                margin: 0;
            }
            
            QScrollBar::handle:vertical {
                background-color: #555;
                border-radius: 6px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #00ffff;
            }
            
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            QStatusBar {
                background-color: #2a2a2a;
                border-top: 1px solid #00ffff;
            }
        """)
    
    @staticmethod
    def apply_light_theme(app: QApplication):
        """Apply light theme to the application
        
        Args:
            app: QApplication instance
        """
        # Reset to default palette
        app.setPalette(QApplication.style().standardPalette())
        app.setStyleSheet("")


def main():
    """Test theme application"""
    import sys
    from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
    
    app = QApplication(sys.argv)
    
    # Apply dark theme
    ThemeManager.apply_dark_theme(app)
    
    # Create test window
    window = QMainWindow()
    window.setWindowTitle("Theme Test")
    window.setGeometry(100, 100, 400, 300)
    
    central = QWidget()
    layout = QVBoxLayout(central)
    
    layout.addWidget(QLabel("Dark Theme Test"))
    layout.addWidget(QPushButton("Test Button"))
    
    window.setCentralWidget(central)
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
