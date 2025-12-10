#!/usr/bin/env python3
"""
Radar Games ML - Lightweight diagnostics runner.

Bootstraps the UI in offscreen mode to validate that the main window and
critical tabs (including ML training) build without raising exceptions.
Logs results to logs/diagnostics.log.
"""

import os
import sys
import traceback
import platform
from datetime import datetime

from PyQt5.QtWidgets import QApplication

from app.core import ConfigManager, configure_services
from app.core.logger import log
from app.core.paths import DIAGNOSTICS_LOG_FILE, LOG_DIR
from app.main import MainWindow, apply_dark_theme


def write_log(message: str) -> None:
    """Append a message to the diagnostics log."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(DIAGNOSTICS_LOG_FILE, "a", encoding="utf-8") as handle:
        handle.write(message + "\n")
    log(message, "INFO")


def main() -> int:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    timestamp = datetime.utcnow().isoformat() + "Z"
    header = (
        f"[Diagnostics] {timestamp} | Python {sys.version.split()[0]} | "
        f"Platform {platform.platform()} ({platform.machine()})"
    )
    write_log(header)

    try:
        app = QApplication([])
        apply_dark_theme(app)

        cfg_manager = ConfigManager()
        config = cfg_manager.load()
        container = configure_services(config)

        window = MainWindow(container=container)
        window.show()
        app.processEvents()

        write_log("Main window initialized successfully (offscreen mode)")
        return 0
    except Exception as exc:  # pylint: disable=broad-except
        trace = traceback.format_exc()
        write_log(f"Diagnostics failed: {exc}\n{trace}")
        return 1
    finally:
        try:
            if 'app' in locals():
                app.quit()
        except Exception:
            pass


if __name__ == "__main__":
    sys.exit(main())
