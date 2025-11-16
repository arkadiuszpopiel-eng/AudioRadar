"""
Comprehensive Logging System for AudioRadar PyQt5
Logs everything from build process to runtime with timestamps and detailed information.
"""

import logging
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Optional
import traceback


class ComprehensiveLogger:
    """Comprehensive logging system that tracks everything from build to runtime."""

    def __init__(self, log_file: str = "log.txt", console_output: bool = True):
        """
        Initialize comprehensive logger.

        Args:
            log_file: Path to log file
            console_output: Whether to output to console as well
        """
        self.log_file = Path(log_file)
        self.console_output = console_output

        # Create log file directory if it doesn't exist
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self.logger = logging.getLogger('AudioRadar')
        self.logger.setLevel(logging.DEBUG)

        # Clear existing handlers
        self.logger.handlers = []

        # File handler - logs everything
        file_handler = logging.FileHandler(self.log_file, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        # Console handler - logs INFO and above
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_formatter = logging.Formatter('[%(levelname)s] %(message)s')
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)

        # Log session start
        self._log_separator()
        self.info("=" * 80)
        self.info(f"AudioRadar PyQt5 v11 - Session started at {datetime.now()}")
        self.info("=" * 80)
        self._log_system_info()

    def _log_separator(self):
        """Log a separator line."""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write("\n" + "=" * 80 + "\n")

    def _log_system_info(self):
        """Log system information."""
        self.info("System Information:")
        self.info(f"  Python version: {sys.version}")
        self.info(f"  Platform: {sys.platform}")
        self.info(f"  Working directory: {os.getcwd()}")
        self.info(f"  Log file: {self.log_file.resolve()}")

    def debug(self, message: str):
        """Log debug message."""
        self.logger.debug(message)

    def info(self, message: str):
        """Log info message."""
        self.logger.info(message)

    def warning(self, message: str):
        """Log warning message."""
        self.logger.warning(message)

    def error(self, message: str, exc_info: Optional[Exception] = None):
        """Log error message with optional exception info."""
        self.logger.error(message)
        if exc_info:
            self.logger.error(f"Exception: {exc_info}")
            self.logger.error(traceback.format_exc())

    def critical(self, message: str, exc_info: Optional[Exception] = None):
        """Log critical message with optional exception info."""
        self.logger.critical(message)
        if exc_info:
            self.logger.critical(f"Exception: {exc_info}")
            self.logger.critical(traceback.format_exc())

    def log_build_start(self):
        """Log build process start."""
        self.info("=" * 80)
        self.info("BUILD PROCESS STARTED")
        self.info("=" * 80)

    def log_build_step(self, step: str):
        """Log a build step."""
        self.info(f"[BUILD] {step}")

    def log_build_complete(self):
        """Log build process completion."""
        self.info("=" * 80)
        self.info("BUILD PROCESS COMPLETED SUCCESSFULLY")
        self.info("=" * 80)

    def log_build_error(self, error: str, exc: Optional[Exception] = None):
        """Log build error."""
        self.error(f"[BUILD ERROR] {error}", exc)

    def log_audio_device(self, device_info: dict):
        """Log audio device information."""
        self.info("Audio Device Detected:")
        for key, value in device_info.items():
            self.info(f"  {key}: {value}")

    def log_detection(self, detection_type: str, direction: float, distance: float, confidence: float):
        """Log sound detection event."""
        self.debug(
            f"DETECTION: Type={detection_type}, "
            f"Direction={direction:.1f}°, "
            f"Distance={distance:.1f}m, "
            f"Confidence={confidence:.2f}"
        )

    def log_performance(self, metric: str, value: float, unit: str = ""):
        """Log performance metric."""
        self.debug(f"PERFORMANCE: {metric} = {value:.3f} {unit}")

    def close(self):
        """Close logger and write final messages."""
        self.info("=" * 80)
        self.info(f"AudioRadar PyQt5 v11 - Session ended at {datetime.now()}")
        self.info("=" * 80)
        for handler in self.logger.handlers:
            handler.close()


# Global logger instance
_global_logger: Optional[ComprehensiveLogger] = None


def get_logger() -> ComprehensiveLogger:
    """Get or create global logger instance."""
    global _global_logger
    if _global_logger is None:
        _global_logger = ComprehensiveLogger()
    return _global_logger


def init_logger(log_file: str = "log.txt", console_output: bool = True) -> ComprehensiveLogger:
    """Initialize global logger."""
    global _global_logger
    _global_logger = ComprehensiveLogger(log_file, console_output)
    return _global_logger
