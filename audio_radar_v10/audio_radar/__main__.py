"""Entry point for running the Audio Radar package as a module.

This file allows you to start the application by running

    python -m audio_radar

from the root of the unpacked archive. In v10.0, this launches the
optimized PyQt5 GUI with performance monitoring and dark theme.
See ``README.md`` for more details.
"""

import sys
import logging
from pathlib import Path

# v10.0: Try to import PyQt5 GUI components
try:
    from PyQt5.QtWidgets import QApplication, QMessageBox
    PYQT5_AVAILABLE = True
except ImportError:
    QApplication = None  # type: ignore
    QMessageBox = None  # type: ignore
    PYQT5_AVAILABLE = False

# v10.0: Import theme manager and performance monitor
# Note: PerformanceMonitor is imported and used by gui.MainWindow
try:
    from .theme_manager import ThemeManager
    THEME_MANAGER_AVAILABLE = True
except ImportError:
    ThemeManager = None  # type: ignore
    THEME_MANAGER_AVAILABLE = False

try:
    from .gui import MainWindow
    GUI_AVAILABLE = True
except ImportError:
    MainWindow = None  # type: ignore
    GUI_AVAILABLE = False

# Fallback to old pygame version if PyQt5 not available
from .main import main as pygame_main


# v10.0: Enhanced exception hook for detailed error reporting
def exception_hook(exctype, value, traceback_obj):
    """Global exception handler for uncaught exceptions."""
    import traceback
    
    # Format the exception
    tb_lines = traceback.format_exception(exctype, value, traceback_obj)
    tb_text = ''.join(tb_lines)
    
    # Log the error
    logging.error(f"Uncaught exception:\n{tb_text}")
    
    # Show error dialog if PyQt5 is available
    if PYQT5_AVAILABLE and QMessageBox:
        try:
            error_msg = f"Wystąpił nieoczekiwany błąd:\n\n{exctype.__name__}: {value}"
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle("Błąd AudioRadar v10.0")
            msg_box.setText(error_msg)
            msg_box.setDetailedText(tb_text)
            msg_box.exec_()
        except Exception:
            # If dialog fails, just print to stderr
            print(tb_text, file=sys.stderr)
    else:
        # Print to stderr if no GUI available
        print(tb_text, file=sys.stderr)


def main() -> None:
    """Main entry point for AudioRadar v10.0."""
    # v10.0: Setup logging
    log_file = Path(__file__).parent / "log_v10.txt"
    logging.basicConfig(
        filename=str(log_file),
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    logging.info("AudioRadar v10.0 starting")
    
    # v10.0: Install custom exception hook
    sys.excepthook = exception_hook
    
    # Check if PyQt5 GUI is available
    if PYQT5_AVAILABLE and GUI_AVAILABLE and MainWindow:
        # v10.0: Launch PyQt5 GUI
        try:
            app = QApplication(sys.argv)
            app.setApplicationName("AudioRadar v10.0")
            app.setApplicationVersion("10.0")
            
            # v10.0: Apply dark theme
            if THEME_MANAGER_AVAILABLE and ThemeManager:
                if ThemeManager.apply_dark_theme(app):
                    logging.info("Dark theme applied successfully")
                else:
                    logging.warning("Failed to apply dark theme")
            
            # Create logger for main window
            logger = logging.getLogger("AudioRadar")
            
            # Create and show main window
            window = MainWindow(logger=logger)
            window.show()
            
            logging.info("PyQt5 GUI initialized successfully")
            
            # Run application event loop
            sys.exit(app.exec_())
        
        except Exception as e:
            logging.error(f"Failed to start PyQt5 GUI: {e}")
            print(f"Błąd uruchamiania GUI: {e}", file=sys.stderr)
            print("Spróbuj zainstalować wymagane zależności: pip install PyQt5 pyaudiowpatch psutil")
            sys.exit(1)
    else:
        # Fallback to pygame version
        logging.info("PyQt5 not available, falling back to pygame version")
        print("PyQt5 nie jest dostępne, uruchamianie wersji pygame...")
        print("Aby użyć pełnej wersji v10.0, zainstaluj: pip install PyQt5 pyaudiowpatch psutil")
        pygame_main()


if __name__ == '__main__':
    main()