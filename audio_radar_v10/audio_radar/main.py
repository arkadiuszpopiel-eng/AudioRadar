"""
AudioRadar v10.0 - Main Entry Point
Launches PyQt5 GUI with modern dark theme
"""
import sys
import os

def main():
    """Main entry point"""
    print("=" * 70)
    print("  AudioRadar v10.0 - Optimized Core + Modern GUI")
    print("=" * 70)
    print()
    
    # Check PyQt5
    try:
        from PyQt5.QtWidgets import QApplication
        print("[OK] PyQt5 loaded")
    except ImportError:
        print("[ERROR] PyQt5 not installed!")
        print("[INFO] Run: pip install PyQt5")
        return 1
    
    # Import modules
    try:
        from gui import MainWindow
        print("[OK] GUI module loaded")
        from theme_manager import ThemeManager
        print("[OK] Theme manager loaded")
    except ImportError as e:
        print(f"[ERROR] Import failed: {e}")
        return 1
    
    # Create app
    app = QApplication(sys.argv)
    app.setApplicationName("AudioRadar")
    app.setApplicationVersion("10.0")
    
    # Apply dark theme
    ThemeManager.apply_dark_theme(app)
    print("[OK] Dark theme applied")
    
    # Show window
    window = MainWindow()
    window.show()
    print("[OK] GUI ready!")
    print("\nShortcuts: SPACE=START/STOP, F5=Refresh")
    
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
