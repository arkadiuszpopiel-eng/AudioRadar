"""
AudioRadar PyQt5 v11 - Main Entry Point
Professional audio detection and visualization system.
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# Initialize comprehensive logging FIRST
from logger import init_logger

# Initialize logger at the very start
logger = init_logger("log.txt", console_output=True)

logger.log_build_start()
logger.log_build_step("Importing modules...")

try:
    from audio_radar_gui import AudioRadarGUI
    logger.log_build_step("AudioRadarGUI imported successfully")
except Exception as e:
    logger.log_build_error("Failed to import AudioRadarGUI", e)
    sys.exit(1)


def main():
    """Main application entry point."""
    logger.log_build_step("Starting Audio Radar application...")

    try:
        # Enable high DPI scaling
        if hasattr(Qt, 'AA_EnableHighDpiScaling'):
            QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

        if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
            QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

        # Create application
        app = QApplication(sys.argv)
        app.setApplicationName("Audio Radar")
        app.setOrganizationName("AudioRadar Project")

        logger.log_build_step("QApplication created successfully")

        # Create and show main window
        window = AudioRadarGUI()
        window.show()

        logger.log_build_step("Main window created and shown")
        logger.log_build_complete()

        logger.info("Audio Radar application started successfully")
        logger.info("=" * 80)

        # Run application
        exit_code = app.exec_()

        logger.info("=" * 80)
        logger.info(f"Application exited with code: {exit_code}")

        return exit_code

    except Exception as e:
        logger.log_build_error("Fatal error in main application", e)
        logger.critical(f"Application crashed: {str(e)}", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
