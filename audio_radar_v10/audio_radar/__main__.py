"""
AudioRadar v10.1 - Main Entry Point
Launches PyQt5 GUI with audio testing tools
NO PYGAME - PyQt5 ONLY
"""
import sys
import os

def main():
    """Launch PyQt5 GUI"""
    print("=" * 70)
    print("  AudioRadar v10.1 - PyQt5 GUI + Testing Tools")
    print("=" * 70)
    print()
    
    # Check PyQt5
    try:
        from PyQt5.QtWidgets import QApplication
        print("[OK] PyQt5 available")
    except ImportError:
        print("[ERROR] PyQt5 not found!")
        print("Install: pip install PyQt5")
        input("Press Enter to exit...")
        return 1
    
    # Import GUI (NOT visualization!)
    try:
        # First try relative import (when run as module)
        try:
            from . import gui
            print("[OK] GUI module loaded (relative import)")
        except ImportError:
            # Fall back to absolute import (when run directly)
            import gui
            print("[OK] GUI module loaded (absolute import)")
    except ImportError as e:
        print(f"[ERROR] Cannot import gui.py: {e}")
        print(f"Working directory: {os.getcwd()}")
        print(f"Python path: {sys.path[:3]}")
        if os.path.exists('gui.py'):
            print("[OK] gui.py exists in current directory")
        else:
            print("[ERROR] gui.py not found!")
        input("Press Enter to exit...")
        return 1
    
    # Import theme
    try:
        try:
            from . import theme_manager
            print("[OK] Theme manager loaded (relative import)")
        except ImportError:
            import theme_manager
            print("[OK] Theme manager loaded (absolute import)")
        has_theme = True
    except ImportError:
        print("[WARN] Theme manager not found - using default theme")
        has_theme = False
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("AudioRadar")
    app.setApplicationVersion("10.1")
    
    # Apply dark theme
    if has_theme:
        theme_manager.ThemeManager.apply_dark_theme(app)
        print("[OK] Dark theme applied")
    
    # Create main window
    try:
        window = gui.MainWindow()
        window.show()
        print("[OK] PyQt5 GUI ready!")
        print()
        print("Features:")
        print("  - Press SPACE: START/STOP")
        print("  - Press F5: Refresh devices")
        print("  - Click TEST: Audio level test")
        print()
    except Exception as e:
        print(f"[ERROR] Failed to create GUI window: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
        return 1
    
    # Run application
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())