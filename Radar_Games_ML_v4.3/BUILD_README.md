# Radar Games ML v4.3 - Build Documentation

This document explains the build system, version management, and project structure for Radar Games ML.

## 📋 Table of Contents

- [Version Management](#version-management)
- [Project Structure](#project-structure)
- [Building on Windows](#building-on-windows)
- [Build Output](#build-output)
- [Reports Location](#reports-location)
- [Running the Application](#running-the-application)
- [Troubleshooting](#troubleshooting)

---

## 🔢 Version Management

### Single Source of Truth

**All version information is centralized in:** `app/version.py`

```python
__version__ = "4.3.0"
BUILD_NUMBER = "k0001"
__version_full__ = "4.3.0-k0001"
BUILD_TARGET = "Radar Games ML"
```

### Where Version is Used

1. **Application Runtime**: `app/core/constants.py` imports from `app/version.py`
2. **Build Scripts**: Both `build_windows.py` and `build.bat` read version dynamically
3. **Build Logs**: Version is printed at the start of every build
4. **Window Title**: Main application window shows version
5. **About Dialog**: Version displayed in UI

### Updating the Version

**To update the version for a new release:**

1. Edit `app/version.py`
2. Update `__version__`, `BUILD_NUMBER`, and add entry to `VERSION_HISTORY`
3. All build scripts will automatically use the new version
4. No need to update version numbers anywhere else!

---

## 📁 Project Structure

```
Radar_Games_ML_v4.3/
├── main.py                    # Entry point (delegates to app/main.py)
├── build_windows.py           # Python build script (recommended)
├── Radar_Games_ML.exe        # Built executable (after build)
│
├── app/                       # Main application package
│   ├── version.py            # VERSION DEFINED HERE (single source of truth)
│   ├── main.py               # Application main module
│   ├── core/                 # Core functionality
│   ├── audio/                # Audio processing
│   ├── detection/            # Detection algorithms
│   ├── ml/                   # Machine learning
│   ├── widgets/              # UI widgets
│   └── ...
│
├── build_tools/              # Build configuration
│   ├── radar_games_ml.spec  # PyInstaller spec file
│   └── build.bat            # Batch build script (alternative)
│
├── dist/                     # Build output directory
│   └── Radar_Games_ML/      # Packaged application
│       ├── Radar_Games_ML.exe
│       └── _internal/       # Dependencies and resources
│
├── Report/                   # All project reports
│   ├── Archive/             # Older version reports
│   └── *.md                 # Current reports
│
└── docs/                     # Documentation
```

---

## 🔨 Building on Windows

### Prerequisites

```bash
# Install Python 3.8+ with pip
python --version

# Install required packages
pip install PyQt5 numpy scipy sounddevice soundcard pyqtgraph PyOpenGL psutil pyinstaller
```

### Method 1: Python Build Script (Recommended)

```bash
# From project root
python build_windows.py
```

**Features:**
- ✅ Reads version from `app/version.py` automatically
- ✅ Validates dependencies before building
- ✅ Shows detailed progress and errors
- ✅ Copies EXE to project root
- ✅ Prints build summary with file sizes

### Method 2: Batch Script

```bash
# From project root
cd build_tools
build.bat
```

**Features:**
- ✅ Reads version dynamically from `app/version.py`
- ✅ Checks for PyInstaller
- ✅ Cleans previous builds
- ✅ Uses PyInstaller spec file

### Method 3: Manual PyInstaller

```bash
# From project root
pyinstaller build_tools/radar_games_ml.spec
```

---

## 📦 Build Output

### After Successful Build

**Two locations contain the application:**

1. **Project Root** (for quick testing):
   ```
   Radar_Games_ML.exe          # Standalone executable (copied here for convenience)
   ```

2. **dist/Radar_Games_ML/** (complete distribution):
   ```
   dist/Radar_Games_ML/
   ├── Radar_Games_ML.exe     # Main executable
   └── _internal/              # All dependencies, DLLs, resources
       ├── PyQt5/
       ├── numpy/
       ├── scipy/
       ├── sounddevice/
       ├── ... (other dependencies)
       └── base_library.zip
   ```

### Distribution Options

**Option A: Single File (Quick Test)**
- Share just `Radar_Games_ML.exe` from project root
- **Note**: This is just a copy; it still needs the `_internal` folder from `dist/` to run!

**Option B: Full Distribution (Recommended)**
- Share the entire `dist/Radar_Games_ML/` folder
- This contains everything needed to run the application
- Users run `Radar_Games_ML.exe` from inside this folder

### Important: _internal Folder

The `_internal` folder is **automatically created by PyInstaller** and contains:
- Python runtime
- All third-party libraries (PyQt5, numpy, scipy, etc.)
- Application resources and data files

**The EXE cannot run without the `_internal` folder!**

---

## 📊 Reports Location

### Report Directory Structure

```
Report/
├── Archive/                                      # Older versions (v4.2.x)
│   ├── AUTOMATED_QA_FINAL_REPORT_v4.2.1-k0004.md
│   ├── REFACTORING_REPORT_v4.2.1.md
│   ├── TEST_PLAN_MASTER_v4.2.1.md
│   └── WORK_SUMMARY_V4.2.md
│
└── [Current Reports]                             # v4.3.0 reports
    ├── DEEP_ANALYSIS_REPORT.md
    ├── DIAGNOSTIC_REPORT_k0003.md
    ├── GRADE_A_REPORT_k0006.md
    ├── RADAR_SPLIT_REPORT_k0007.md
    └── REFACTORING_PLAN.md
```

### Generating New Reports

When creating new reports for v4.3.0:

1. **Filename**: Use format `REPORT_NAME_v4.3.0.md` or `REPORT_NAME_k0001.md`
2. **Location**: Save to `Report/` directory
3. **Content**: Include version number in report header
4. **Old Reports**: Move previous version reports to `Report/Archive/`

### Referencing Reports in Code

```python
from pathlib import Path

# Always use this pattern
REPORT_DIR = Path(__file__).resolve().parent.parent / "Report"
report_path = REPORT_DIR / "DIAGNOSTIC_REPORT.md"
```

---

## ▶️ Running the Application

### From Source (Development)

```bash
# From project root
python main.py
```

This will:
1. Set up Python path to include `app/` directory
2. Import and run `app.main.main()`
3. Launch the PyQt5 GUI application

### From Built Executable (Production)

**Method 1: From Project Root (after build)**
```bash
# Just double-click or run:
Radar_Games_ML.exe
```

**Method 2: From dist/ folder**
```bash
cd dist/Radar_Games_ML
Radar_Games_ML.exe
```

**Important**: Make sure the `_internal/` folder is in the same directory as the EXE!

---

## 🔧 Troubleshooting

### Build Issues

**Problem**: `ERROR: Spec file not found`
- **Solution**: Make sure you're running from project root, not from `build_tools/`
- **Check**: `build_tools/radar_games_ml.spec` exists

**Problem**: `Version: v4.2.1` (wrong version in logs)
- **Solution**: The build scripts now read from `app/version.py` automatically
- **Check**: `app/version.py` has correct `__version__` and `BUILD_NUMBER`

**Problem**: `Import error: No module named 'PyQt5'`
- **Solution**: Install dependencies: `pip install -r requirements.txt` (if exists)
- **Or**: `pip install PyQt5 numpy scipy sounddevice pyqtgraph PyOpenGL psutil`

### Runtime Issues

**Problem**: EXE won't run, says "DLL not found"
- **Solution**: Make sure `_internal/` folder is next to the EXE
- **Distribution**: Share the entire `dist/Radar_Games_ML/` folder, not just the EXE

**Problem**: Application crashes on startup
- **Check logs**: Look for `super_log.txt` in the application directory
- **Run from terminal**: `Radar_Games_ML.exe` to see error messages

**Problem**: "Import error" at runtime
- **Solution**: Rebuild with latest spec file (includes all hidden imports)
- **Check**: `build_tools/radar_games_ml.spec` has your module listed in `hiddenimports`

### Version Inconsistencies

**Problem**: Different versions shown in different places
- **Root Cause**: This should not happen anymore! All versions read from `app/version.py`
- **Fix**: Update only `app/version.py`, rebuild, and verify:
  ```bash
  python -c "import sys; sys.path.insert(0, 'app'); from version import __version_full__; print(__version_full__)"
  ```

---

## 📝 Quick Reference

| What | Where | Notes |
|------|-------|-------|
| **Version Definition** | `app/version.py` | Single source of truth |
| **Entry Point** | `main.py` (root) | Delegates to `app/main.py` |
| **Build Scripts** | `build_windows.py`<br>`build_tools/build.bat` | Both read version dynamically |
| **PyInstaller Config** | `build_tools/radar_games_ml.spec` | Spec file with post-build |
| **Build Output** | `dist/Radar_Games_ML/` | Full distribution |
| **Quick EXE** | `Radar_Games_ML.exe` (root) | Copy for convenience |
| **Reports** | `Report/` | Current reports |
| **Old Reports** | `Report/Archive/` | Historical versions |
| **Logs** | `super_log.txt`<br>`log/` | Runtime logs |

---

## 🎯 Summary

1. **Version is defined ONCE** in `app/version.py`
2. **Build with** `python build_windows.py` (recommended)
3. **EXE appears** in project root after build
4. **Full distribution** is in `dist/Radar_Games_ML/`
5. **Reports go** in `Report/` directory
6. **Run with** `python main.py` (dev) or `Radar_Games_ML.exe` (prod)

---

**Last Updated**: v4.3.0-k0001
**Build System**: PyInstaller 5.x+
**Platform**: Windows x64
