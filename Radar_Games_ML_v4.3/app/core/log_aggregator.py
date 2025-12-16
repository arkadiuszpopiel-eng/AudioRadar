"""
Radar Games ML v4.3.1-k0006 - Log Aggregator
Automatic log copying to centralized all_logs/ directory for easy review

CREATED v4.3.1-k0006: User request for convenient log viewing
- Copies ALL logs to all_logs/ without changing original structure
- Preserves log/ and raport/ directories untouched
- Easy access to all logs in one place
"""

import shutil
from pathlib import Path
from typing import Optional


def get_all_logs_dir() -> Path:
    """
    Get centralized all_logs directory in project root

    Returns:
        Path: all_logs/ directory (auto-created)
    """
    from .paths import APP_ROOT

    all_logs = APP_ROOT / "all_logs"
    all_logs.mkdir(exist_ok=True)

    # Create subdirectories for organization
    (all_logs / "runtime").mkdir(exist_ok=True)
    (all_logs / "build").mkdir(exist_ok=True)
    (all_logs / "selftest").mkdir(exist_ok=True)
    (all_logs / "ml_training").mkdir(exist_ok=True)

    return all_logs


def copy_to_all_logs(source_path: Path, category: str = "runtime") -> Optional[Path]:
    """
    Copy log file to centralized all_logs directory

    Args:
        source_path: Source log file path
        category: Log category (runtime, build, selftest, ml_training)

    Returns:
        Path: Destination path in all_logs/ or None if failed
    """
    if not source_path.exists():
        return None

    try:
        all_logs = get_all_logs_dir()
        category_dir = all_logs / category

        # Copy file preserving name
        dest_path = category_dir / source_path.name
        shutil.copy2(str(source_path), str(dest_path))

        return dest_path
    except Exception as e:
        # Silent fail - aggregation is optional, don't break main logging
        print(f"[log_aggregator] Warning: Could not copy {source_path.name}: {e}")
        return None


def aggregate_all_existing_logs() -> dict:
    """
    Copy all existing logs from log/ and raport/ to all_logs/
    Useful for initial setup or manual sync

    Returns:
        dict: Summary of copied files by category
    """
    from .paths import LOG_DIR, REPORT_DIR

    summary = {
        "runtime": [],
        "build": [],
        "selftest": [],
        "ml_training": []
    }

    # Runtime logs
    for log_file in LOG_DIR.glob("*.txt"):
        if log_file.name.startswith("selftest"):
            continue  # Handle separately
        dest = copy_to_all_logs(log_file, "runtime")
        if dest:
            summary["runtime"].append(log_file.name)

    # Build logs
    for log_file in LOG_DIR.glob("*.log"):
        dest = copy_to_all_logs(log_file, "build")
        if dest:
            summary["build"].append(log_file.name)

    # Selftest logs
    for log_file in LOG_DIR.glob("selftest_*.log"):
        dest = copy_to_all_logs(log_file, "selftest")
        if dest:
            summary["selftest"].append(log_file.name)

    # Selftest reports
    for report_file in REPORT_DIR.glob("selftest_report_*.txt"):
        dest = copy_to_all_logs(report_file, "selftest")
        if dest:
            summary["selftest"].append(report_file.name)

    # ML training reports
    for report_file in REPORT_DIR.glob("ml_training_*.json"):
        dest = copy_to_all_logs(report_file, "ml_training")
        if dest:
            summary["ml_training"].append(report_file.name)

    return summary


def create_readme() -> None:
    """Create README in all_logs/ explaining the structure"""
    all_logs = get_all_logs_dir()
    readme_path = all_logs / "README.txt"

    readme_content = """
========================================================================
Radar Games ML v4.3.1-k0006 - Centralized Logs Viewer
========================================================================

Ten folder zawiera KOPIE wszystkich logów z projektu dla wygodnego
przeglądu. Oryginalne logi pozostają w swoich lokalizacjach:
- log/ (runtime logs, build logs)
- raport/ (test reports, ML reports)

STRUKTURA:
----------

all_logs/
├── runtime/          - Logi działania programu
│   ├── super_log.txt
│   └── legacy_super_log_v2.3.0.txt
│
├── build/            - Logi kompilacji/budowy
│   ├── build_windows.log
│   ├── build_fixed.log
│   └── build_all.log
│
├── selftest/         - Logi testów (przycisk TEST)
│   ├── selftest_YYYYMMDD_HHMMSS.log
│   └── selftest_report_YYYYMMDD_HHMMSS.txt
│
└── ml_training/      - Raporty treningu ML
    └── ml_training_profile_name.json


WAŻNE:
------
- To są tylko KOPIE - możesz je bezpiecznie usunąć
- Oryginalne logi są w log/ i raport/
- Folder odświeża się automatycznie przy każdym zapisie
- Jeśli chcesz odświeżyć wszystko ręcznie:
  python -c "from app.core.log_aggregator import aggregate_all_existing_logs; aggregate_all_existing_logs()"


AUTOR: Claude Code v4.3.1-k0006
DATA: 2025-12-15
"""

    readme_path.write_text(readme_content, encoding="utf-8")


# Auto-create on import
try:
    all_logs_dir = get_all_logs_dir()
    create_readme()
except Exception:
    pass  # Silent fail during imports


__all__ = [
    'get_all_logs_dir',
    'copy_to_all_logs',
    'aggregate_all_existing_logs',
    'create_readme',
]
