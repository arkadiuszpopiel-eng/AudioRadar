"""AudioRadar v10.0 - Direct GUI Launcher"""
import sys
from PyQt5.QtWidgets import QApplication

def main():
    print("[AudioRadar v10.0] Starting GUI...")
    
    from gui import MainWindow
    from theme_manager import ThemeManager
    
    app = QApplication(sys.argv)
    ThemeManager.apply_dark_theme(app)
    
    window = MainWindow()
    window.show()
    
    print("[OK] Ready! (SPACE=START/STOP, F5=Refresh)")
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
