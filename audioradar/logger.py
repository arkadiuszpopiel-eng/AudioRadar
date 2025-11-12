"""
Thread-safe logging system for Audio Radar.
Provides centralized logging with file and console output.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from threading import Lock

# Global logger instance
_logger = None
_logger_lock = Lock()

LOG_FILE = Path(__file__).parent.parent / "log.txt"
LOG_FORMAT = "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

class ThreadSafeLogger:
    """Thread-safe wrapper for Python logger."""
    
    def __init__(self, logger):
        self.logger = logger
        self.lock = Lock()
    
    def _log(self, level, msg, *args, **kwargs):
        """Thread-safe logging method."""
        with self.lock:
            self.logger.log(level, msg, *args, **kwargs)
    
    def debug(self, msg, *args, **kwargs):
        self._log(logging.DEBUG, msg, *args, **kwargs)
    
    def info(self, msg, *args, **kwargs):
        self._log(logging.INFO, msg, *args, **kwargs)
    
    def warning(self, msg, *args, **kwargs):
        self._log(logging.WARNING, msg, *args, **kwargs)
    
    def error(self, msg, *args, **kwargs):
        self._log(logging.ERROR, msg, *args, **kwargs)
    
    def critical(self, msg, *args, **kwargs):
        self._log(logging.CRITICAL, msg, *args, **kwargs)
    
    def exception(self, msg, *args, **kwargs):
        """Log exception with traceback."""
        with self.lock:
            self.logger.exception(msg, *args, **kwargs)


def setup_logging(level=logging.INFO):
    """
    Setup logging configuration.
    
    Args:
        level: Logging level (default: INFO)
    
    Returns:
        ThreadSafeLogger instance
    """
    global _logger
    
    with _logger_lock:
        if _logger is not None:
            return _logger
        
        # Create logger
        logger = logging.getLogger("audioradar")
        logger.setLevel(level)
        logger.handlers.clear()
        
        # File handler
        try:
            file_handler = logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8')
            file_handler.setLevel(level)
            file_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            print(f"Warning: Could not create log file: {e}")
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.WARNING)  # Only warnings and above to console
        console_formatter = logging.Formatter("%(levelname)s: %(message)s")
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        _logger = ThreadSafeLogger(logger)
        
        # Log startup info
        _logger.info("=" * 80)
        _logger.info(f"Logging initialized - {datetime.now().strftime(DATE_FORMAT)}")
        _logger.info(f"Log file: {LOG_FILE.absolute()}")
        _logger.info("=" * 80)
        
        return _logger


def get_logger():
    """
    Get the global logger instance.
    
    Returns:
        ThreadSafeLogger instance
    """
    global _logger
    
    if _logger is None:
        return setup_logging()
    
    return _logger
