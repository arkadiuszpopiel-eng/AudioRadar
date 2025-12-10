#!/usr/bin/env python3
"""
Radar Games ML - Windows Build Script
Builds standalone Windows executable using PyInstaller

Features:
- Reads version from app/version.py (single source of truth)
- Validates environment and dependencies
- Runs PyInstaller with proper spec file
- Copies final EXE to project root
- Cleans up build artifacts
"""

import sys
import shutil
import subprocess
import logging
import platform
from datetime import datetime
from pathlib import Path

# Add app directory to path for version import
PROJECT_ROOT = Path(__file__).parent
APP_DIR = PROJECT_ROOT / "app"
sys.path.insert(0, str(APP_DIR))

# Import version from single source of truth
try:
    from version import __version__, __version_full__, BUILD_NUMBER, BUILD_TARGET
    VERSION = __version_full__
except ImportError as e:
    print(f"ERROR: Could not import version from app/version.py: {e}")
    print("Make sure app/version.py exists and is valid!")
    sys.exit(1)

from app.core.paths import LOG_DIR, BUILD_LOG_FILE, REPORT_DIR

DIST_DIR_NAME = "Radar_Games_ML"
EXE_NAME = "Radar_Games_ML.exe"
DIST_DIR = PROJECT_ROOT / "dist" / DIST_DIR_NAME
INTERNAL_DIR = DIST_DIR / "_internal"
ROOT_EXE = PROJECT_ROOT / EXE_NAME
ROOT_INTERNAL = PROJECT_ROOT / "_internal"
BUILD_REPORT = REPORT_DIR / "build_report.txt"

logger = logging.getLogger("build_windows")
logger.setLevel(logging.DEBUG)


def setup_logging():
    """Configure logging to both console and file."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
    )

    file_handler = logging.FileHandler(BUILD_LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger.addHandler(console)


def print_header():
    """Print build header with version info"""
    logger.info("=" * 80)
    logger.info(f"{BUILD_TARGET} - Windows Build Script")
    logger.info("=" * 80)
    logger.info(f"Version: {VERSION}")
    logger.info(f"Build Number: {BUILD_NUMBER}")
    logger.info(f"Project Root: {PROJECT_ROOT}")
    logger.info(f"Python: {sys.version}")
    logger.info(f"Platform: {platform.platform()} ({platform.machine()})")
    logger.info("=" * 80)


def check_pyinstaller():
    """Check if PyInstaller is installed"""
    logger.info("Checking PyInstaller installation...")
    try:
        import PyInstaller
        logger.info(f"✓ PyInstaller {PyInstaller.__version__} found")
        return True
    except ImportError:
        logger.error("✗ ERROR: PyInstaller not installed! Please install: pip install pyinstaller")
        return False


def check_spec_file():
    """Check if spec file exists"""
    spec_file = PROJECT_ROOT / "build_tools" / "radar_games_ml.spec"
    logger.info(f"Checking spec file: {spec_file}")

    if not spec_file.exists():
        logger.error("✗ ERROR: Spec file not found!")
        logger.error(f"Expected: {spec_file}")
        logger.info("Alternatives:")
        logger.info("  1. Create the spec file using: pyinstaller --name Radar_Games_ML main.py")
        logger.info("  2. Check if spec file has a different name in build_tools/")
        return False

    logger.info("✓ Spec file found")
    return spec_file


def clean_build_artifacts():
    """Clean previous build artifacts"""
    logger.info("Cleaning previous build artifacts...")

    artifacts = [
        PROJECT_ROOT / "build",
        DIST_DIR,
        ROOT_EXE,
        ROOT_INTERNAL,
        PROJECT_ROOT / "__pycache__",
    ]

    for artifact in artifacts:
        if artifact.exists():
            if artifact.is_dir():
                shutil.rmtree(artifact)
                logger.info(f"  Removed directory: {artifact}")
            else:
                artifact.unlink()
                logger.info(f"  Removed file: {artifact}")

    logger.info("✓ Cleanup complete")


def run_pyinstaller(spec_file):
    """Run PyInstaller with the spec file"""
    logger.info("=" * 80)
    logger.info("Building executable with PyInstaller...")
    logger.info("=" * 80)

    cmd = ["pyinstaller", str(spec_file)]
    logger.info(f"Command: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=False  # Show output in real-time
        )
        logger.info("✓ PyInstaller build completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"✗ ERROR: PyInstaller build failed with code {e.returncode}")
        return False
    except FileNotFoundError:
        logger.error("✗ ERROR: pyinstaller command not found! Make sure PyInstaller is installed and in your PATH")
        return False


def copy_exe_to_root():
    """Copy final EXE to project root"""
    logger.info("Copying executable to project root...")

    exe_source = DIST_DIR / EXE_NAME

    if not exe_source.exists():
        logger.error(f"✗ ERROR: Built executable not found at: {exe_source}")
        return False

    try:
        shutil.copy2(exe_source, ROOT_EXE)
        logger.info(f"✓ Copied: {exe_source.name} -> {ROOT_EXE}")

        # Verify file size
        size_mb = ROOT_EXE.stat().st_size / (1024 * 1024)
        logger.info(f"  Size: {size_mb:.2f} MB")

        # Copy bundled runtime directory (_internal)
        if INTERNAL_DIR.exists():
            if ROOT_INTERNAL.exists():
                shutil.rmtree(ROOT_INTERNAL)
            shutil.copytree(INTERNAL_DIR, ROOT_INTERNAL)
            python_dll = ROOT_INTERNAL / "python311.dll"
            status = "present" if python_dll.exists() else "missing"
            logger.info(f"  Copied _internal -> {ROOT_INTERNAL} (python311.dll {status})")
        else:
            logger.warning(f"_internal directory not found at {INTERNAL_DIR}")
        return True
    except Exception as e:
        logger.error(f"✗ ERROR: Failed to copy executable: {e}")
        return False


def print_summary():
    """Print build summary"""
    logger.info("=" * 80)
    logger.info("BUILD COMPLETE!")
    logger.info("=" * 80)
    logger.info(f"Version: {VERSION}")
    logger.info("Executable Location:")
    logger.info(f"  Main: {ROOT_EXE}")
    logger.info(f"  Dist: {DIST_DIR}")
    logger.info("To run the application:")
    logger.info(f"  Double-click: {ROOT_EXE.name}")
    logger.info(f"  Or from terminal: .\\{ROOT_EXE.name}")
    logger.info("Note: The dist/ folder contains the full distribution with all dependencies.")


def verify_distribution():
    """Validate that critical build artifacts exist and log a report."""
    logger.info("Validating build output layout...")
    checks = []
    missing = []

    artifacts = [
        (DIST_DIR, "Distribution directory"),
        (DIST_DIR / EXE_NAME, "Built executable in dist"),
        (INTERNAL_DIR, "Bundled runtime directory (_internal)"),
        (INTERNAL_DIR / "python311.dll", "Bundled Python runtime"),
        (DIST_DIR / "Qt5Core.dll", "Qt5Core.dll"),
        (DIST_DIR / "Qt5Widgets.dll", "Qt5Widgets.dll"),
    ]

    for path, description in artifacts:
        exists = path.exists()
        status = "OK" if exists else "MISSING"
        line = f"[{status}] {description}: {path}"
        checks.append(line)
        if not exists:
            missing.append(description)
        logger.info(line)

    report_lines = [
        "Radar Games ML - Windows Build Verification",
        f"Timestamp: {datetime.utcnow().isoformat()}Z",
        f"Version: {VERSION}",
        "",
        "Checks:",
        *checks,
        "",
    ]

    if missing:
        report_lines.append(f"FAILURE: Missing artifacts: {', '.join(missing)}")
        logger.error(f"Build verification failed: missing {', '.join(missing)}")
    else:
        report_lines.append("SUCCESS: All critical artifacts present.")
        logger.info("Build verification succeeded. All critical artifacts present.")

    BUILD_REPORT.write_text("\n".join(report_lines), encoding="utf-8")
    return not missing


def main():
    """Main build process"""
    setup_logging()
    print_header()

    # Step 1: Check dependencies
    if not check_pyinstaller():
        sys.exit(1)

    # Step 2: Check spec file
    spec_file = check_spec_file()
    if not spec_file:
        sys.exit(1)

    # Step 3: Clean previous builds
    clean_build_artifacts()

    # Step 4: Run PyInstaller
    if not run_pyinstaller(spec_file):
        logger.error("✗ BUILD FAILED!")
        sys.exit(1)

    # Step 5: Copy EXE to root
    if not copy_exe_to_root():
        logger.warning("⚠ WARNING: Build succeeded but EXE copy failed")
        logger.warning(f"You can find the executable in: {DIST_DIR}")

    verify_distribution()

    # Step 6: Print summary
    print_summary()

    logger.info("✓ Build process completed successfully!")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.warning("Build interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.exception(f"✗ FATAL ERROR: {e}")
        sys.exit(1)
