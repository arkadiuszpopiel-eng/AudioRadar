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


def print_header():
    """Print build header with version info"""
    print("=" * 80)
    print(f"{BUILD_TARGET} - Windows Build Script")
    print("=" * 80)
    print(f"Version: {VERSION}")
    print(f"Build Number: {BUILD_NUMBER}")
    print(f"Project Root: {PROJECT_ROOT}")
    print("=" * 80)
    print()


def check_pyinstaller():
    """Check if PyInstaller is installed"""
    print("Checking PyInstaller installation...")
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__} found")
        return True
    except ImportError:
        print("✗ ERROR: PyInstaller not installed!")
        print("  Please install: pip install pyinstaller")
        return False


def check_spec_file():
    """Check if spec file exists"""
    spec_file = PROJECT_ROOT / "build_tools" / "radar_games_ml.spec"
    print(f"\nChecking spec file: {spec_file}")

    if not spec_file.exists():
        print(f"✗ ERROR: Spec file not found!")
        print(f"  Expected: {spec_file}")
        print("\nAlternatives:")
        print("  1. Create the spec file using: pyinstaller --name Radar_Games_ML main.py")
        print("  2. Check if spec file has a different name in build_tools/")
        return False

    print(f"✓ Spec file found")
    return spec_file


def clean_build_artifacts():
    """Clean previous build artifacts"""
    print("\nCleaning previous build artifacts...")

    artifacts = [
        PROJECT_ROOT / "build",
        PROJECT_ROOT / "dist" / "Radar_Games_ML",
        PROJECT_ROOT / "Radar_Games_ML.exe",
        PROJECT_ROOT / "__pycache__",
    ]

    for artifact in artifacts:
        if artifact.exists():
            if artifact.is_dir():
                shutil.rmtree(artifact)
                print(f"  Removed directory: {artifact.name}")
            else:
                artifact.unlink()
                print(f"  Removed file: {artifact.name}")

    print("✓ Cleanup complete")


def run_pyinstaller(spec_file):
    """Run PyInstaller with the spec file"""
    print("\n" + "=" * 80)
    print("Building executable with PyInstaller...")
    print("=" * 80)
    print()

    cmd = ["pyinstaller", str(spec_file)]
    print(f"Command: {' '.join(cmd)}")
    print()

    try:
        result = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=False  # Show output in real-time
        )
        print("\n✓ PyInstaller build completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ ERROR: PyInstaller build failed with code {e.returncode}")
        return False
    except FileNotFoundError:
        print("\n✗ ERROR: pyinstaller command not found!")
        print("  Make sure PyInstaller is installed and in your PATH")
        return False


def copy_exe_to_root():
    """Copy final EXE to project root"""
    print("\nCopying executable to project root...")

    exe_source = PROJECT_ROOT / "dist" / "Radar_Games_ML" / "Radar_Games_ML.exe"
    exe_dest = PROJECT_ROOT / "Radar_Games_ML.exe"

    if not exe_source.exists():
        print(f"✗ ERROR: Built executable not found at: {exe_source}")
        return False

    try:
        shutil.copy2(exe_source, exe_dest)
        print(f"✓ Copied: {exe_source.name} -> {exe_dest}")

        # Verify file size
        size_mb = exe_dest.stat().st_size / (1024 * 1024)
        print(f"  Size: {size_mb:.2f} MB")
        return True
    except Exception as e:
        print(f"✗ ERROR: Failed to copy executable: {e}")
        return False


def print_summary():
    """Print build summary"""
    exe_path = PROJECT_ROOT / "Radar_Games_ML.exe"
    dist_path = PROJECT_ROOT / "dist" / "Radar_Games_ML"

    print("\n" + "=" * 80)
    print("BUILD COMPLETE!")
    print("=" * 80)
    print(f"Version: {VERSION}")
    print(f"\nExecutable Location:")
    print(f"  Main: {exe_path}")
    print(f"  Dist: {dist_path}")
    print(f"\nTo run the application:")
    print(f"  Double-click: {exe_path.name}")
    print(f"  Or from terminal: .\\{exe_path.name}")
    print("\nNote: The dist/ folder contains the full distribution with")
    print("      all dependencies. You can distribute the entire")
    print("      dist/Radar_Games_ML/ folder, or just the EXE from root.")
    print("=" * 80)


def main():
    """Main build process"""
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
        print("\n✗ BUILD FAILED!")
        sys.exit(1)

    # Step 5: Copy EXE to root
    if not copy_exe_to_root():
        print("\n⚠ WARNING: Build succeeded but EXE copy failed")
        print("  You can find the executable in: dist/Radar_Games_ML/")

    # Step 6: Print summary
    print_summary()

    print("\n✓ Build process completed successfully!")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nBuild interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n✗ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
