"""AudioRadar v10.2 - PyQt5 Entry Point"""
import sys
import os
from PyQt5.QtWidgets import QApplication

# Add current directory to path for module imports
sys.path.insert(0, os.path.dirname(__file__))

def main():
    print("AudioRadar v10.2 starting...")
    try:
        import gui
        import theme_manager
    except ImportError as e:
        print(f"Import error: {e}")
        return 1
    
    app = QApplication(sys.argv)
    theme_manager.ThemeManager.apply_dark_theme(app)
    window = gui.MainWindow()
    window.setWindowTitle("AudioRadar v10.2")
    window.show()
    print("GUI ready!")
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())