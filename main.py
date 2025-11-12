"""
Audio Radar - Main Entry Point
Python 3.11.9
Generated: 2025-11-12 21:48:06 UTC

This is the main entry point for the Audio Radar application.
It initializes logging, loads configuration, and launches the PyQt5 GUI.
"""

import sys
import traceback
from pathlib import Path

# Add audioradar package to path
sys.path.insert(0, str(Path(__file__).parent))

from audioradar.logger import setup_logging, get_logger
from audioradar.config import Config

def main():
    """Main application entry point."""
    # Setup logging first
    logger = setup_logging()
    logger.info("=" * 60)
    logger.info("Audio Radar Application Starting")
    logger.info("=" * 60)
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Working directory: {Path.cwd()}")
    
    try:
        # Import PyQt5 (lazy import to ensure logging is setup first)
        from PyQt5.QtWidgets import QApplication
        from audioradar.gui.main_window import MainWindow
        
        logger.info("Initializing PyQt5 application...")
        
        # Load configuration
        config = Config()
        logger.info("Configuration loaded successfully")
        
        # Create Qt application
        app = QApplication(sys.argv)
        app.setApplicationName("Audio Radar")
        app.setOrganizationName("AudioRadar")
        
        logger.info("Creating main window...")
        window = MainWindow(config)
        window.show()
        
        logger.info("Application started successfully")
        logger.info("=" * 60)
        
        # Run application event loop
        sys.exit(app.exec_())
        
    except ImportError as e:
        logger.error(f"Failed to import required module: {e}")
        logger.error("Please ensure all dependencies are installed: pip install -r requirements.txt")
        logger.error(traceback.format_exc())
        print("\nERROR: Missing required dependencies!")
        print(f"Details: {e}")
        print("\nPlease run: pip install -r requirements.txt")
        return 1
        
    except Exception as e:
        logger.error(f"Fatal error during startup: {e}")
        logger.error(traceback.format_exc())
        print(f"\nFATAL ERROR: {e}")
        print("\nCheck log.txt for details")
        return 1

if __name__ == "__main__":
    sys.exit(main())
