#!/usr/bin/env python3
"""
Radar Games ML - Build Verification Utility

Validates that the PyInstaller output contains critical artifacts such as
python311.dll and Qt runtime libraries. Produces a human-readable report in
reports/build_report.txt and mirrors the status to stdout for quick checks.
"""

import sys
import platform
from datetime import datetime

from app.core.paths import APP_ROOT, REPORT_DIR, LOG_DIR

DIST_DIR_NAME = "Radar_Games_ML"
EXE_NAME = "Radar_Games_ML.exe"
DIST_DIR = APP_ROOT / "dist" / DIST_DIR_NAME
INTERNAL_DIR = DIST_DIR / "_internal"
REPORT_PATH = REPORT_DIR / "build_report.txt"


def _write(message: str):
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with REPORT_PATH.open("a", encoding="utf-8") as handle:
        handle.write(message + "\n")


def verify() -> bool:
    REPORT_PATH.write_text("", encoding="utf-8")
    header = [
        "Radar Games ML - Build Verification",
        f"Timestamp: {datetime.utcnow().isoformat()}Z",
        f"Platform: {platform.platform()} ({platform.machine()})",
        f"Python: {sys.version.split()[0]}",
        "",
    ]
    for line in header:
        _write(line)

    checks = [
        (DIST_DIR, "Distribution directory"),
        (DIST_DIR / EXE_NAME, "Executable"),
        (INTERNAL_DIR, "_internal runtime directory"),
        (INTERNAL_DIR / "python311.dll", "Bundled python311.dll"),
        (DIST_DIR / "Qt5Core.dll", "Qt5Core.dll"),
        (DIST_DIR / "Qt5Widgets.dll", "Qt5Widgets.dll"),
    ]

    missing = []
    _write("Checks:")
    for path, description in checks:
        status = "OK" if path.exists() else "MISSING"
        line = f"[{status}] {description}: {path}"
        _write(line)
        print(line)
        if status == "MISSING":
            missing.append(description)

    _write("")
    if missing:
        _write(f"FAILURE: Missing artifacts: {', '.join(missing)}")
    else:
        _write("SUCCESS: All critical artifacts present.")

    return not missing


if __name__ == "__main__":
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    success = verify()
    sys.exit(0 if success else 1)
