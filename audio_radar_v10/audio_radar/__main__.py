"""Entry point for AudioRadar v10.2 COMPLETE.

This module launches the PyQt5 GUI application. Run with:

    python -m audio_radar
    
or:

    python __main__.py
"""

import sys

try:
    from PyQt5.QtWidgets import QApplication
except ImportError:
    print("ERROR: PyQt5 is not installed.")
    print("Please install required dependencies:")
    print("  python -m pip install PyQt5 sounddevice numpy")
    sys.exit(1)

from theme_manager import ThemeManager
from gui import MainWindow


def main():
    """Launch the AudioRadar v10.2 GUI application."""
    app = QApplication(sys.argv)
    app.setApplicationName("AudioRadar v10.2 COMPLETE")
    
    # Apply dark theme
    ThemeManager.apply_dark_theme(app)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()