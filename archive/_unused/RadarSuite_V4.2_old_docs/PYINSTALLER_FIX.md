# PyInstaller Error Fix - RadarSuite Final

## Problem

You encountered the error: **[ERROR] PyInstaller not available**

This error occurs when:
1. PyInstaller is not installed in your Python environment
2. You're running the Windows build script (`RUN_BUILD_ALL.cmd`) on a Linux/macOS system
3. The PyInstaller command is not in your PATH

## Solution

### For Linux/macOS Users

Use the new **RUN_BUILD_ALL.sh** script instead of the .cmd file:

```bash
# Navigate to the RadarSuite_Final directory
cd RadarSuite_Final

# Make the script executable (first time only)
chmod +x RUN_BUILD_ALL.sh

# Run the build script
./RUN_BUILD_ALL.sh
```

The script will:
1. Check for Python 3.11
2. Create a virtual environment (.venv)
3. Install all dependencies including PyInstaller
4. Build the standalone executable
5. Package it into a ZIP file

### For Windows Users

Use the existing **RUN_BUILD_ALL.cmd** script:

```cmd
REM Navigate to the RadarSuite_Final directory
cd RadarSuite_Final

REM Run the build script
RUN_BUILD_ALL.cmd
```

## Manual Fix (If scripts don't work)

If the automated scripts fail, you can build manually:

### 1. Create and activate virtual environment

**Linux/macOS:**
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```cmd
py -3.11 -m venv .venv
.venv\Scripts\activate.bat
```

### 2. Install dependencies

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 3. Verify PyInstaller is installed

```bash
pyinstaller --version
```

If this command fails, install PyInstaller manually:
```bash
pip install pyinstaller>=6.0.0
```

### 4. Build the executable

```bash
pyinstaller --clean --noconfirm build_tools/radarsuite.spec
```

### 5. Run the application

**Linux/macOS:**
```bash
cd dist/RadarSuite_Final
./RadarSuite_Final
```

**Windows:**
```cmd
cd dist\RadarSuite_Final
RadarSuite_Final.exe
```

## System Requirements

### Required Software

- **Python 3.11** (specifically version 3.11, not 3.10 or 3.12)
- **pip** (Python package installer)
- **venv** (Python virtual environment module)

### System Dependencies (Linux only)

For audio support on Linux, install PortAudio:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install portaudio19-dev python3.11 python3.11-venv
```

**Fedora:**
```bash
sudo dnf install portaudio-devel python3.11
```

**Arch Linux:**
```bash
sudo pacman -S portaudio python311
```

For OpenGL support (3D radar visualization):
```bash
sudo apt install libgl1-mesa-glx  # Ubuntu/Debian
```

### Python Dependencies (Installed automatically by scripts)

- PyQt5 >= 5.15.0
- pyqtgraph >= 0.13.0
- PyOpenGL + PyOpenGL_accelerate
- numpy >= 1.21.0
- scipy >= 1.7.0
- sounddevice >= 0.4.0
- soundcard >= 0.4.0
- psutil >= 5.9.0
- **pyinstaller >= 6.0.0** (This fixes the error!)

## Troubleshooting

### Error: "Python 3.11 not found"

**Solution:** Install Python 3.11:
- Ubuntu/Debian: `sudo apt install python3.11 python3.11-venv`
- macOS: `brew install python@3.11`
- Windows: Download from https://www.python.org/downloads/

### Error: "PyInstaller not available" (after installation)

**Solution:** The virtual environment might not be activated properly.

1. Deactivate and reactivate:
   ```bash
   deactivate
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate.bat  # Windows
   ```

2. Verify installation:
   ```bash
   pip list | grep pyinstaller
   ```

3. If still not found, install directly:
   ```bash
   pip install --upgrade pyinstaller
   ```

### Error: "Module verification failed"

This means one of the required Python packages couldn't be imported.

**Linux users:** Install system dependencies:
```bash
sudo apt install portaudio19-dev libgl1-mesa-glx
```

**All users:** Check the log file:
```bash
cat super_log.txt | grep ERROR
```

### Error during PyInstaller build

1. Check the detailed log:
   ```bash
   tail -50 super_log.txt
   ```

2. Try building with more verbose output:
   ```bash
   pyinstaller --clean --noconfirm --log-level DEBUG build_tools/radarsuite.spec
   ```

3. Clean all build artifacts and try again:
   ```bash
   rm -rf build dist *.spec
   ./RUN_BUILD_ALL.sh
   ```

### Executable doesn't run

1. Check if it was built:
   ```bash
   ls -lh dist/RadarSuite_Final/RadarSuite_Final*
   ```

2. Make it executable (Linux/macOS only):
   ```bash
   chmod +x dist/RadarSuite_Final/RadarSuite_Final
   ```

3. Run from terminal to see error messages:
   ```bash
   cd dist/RadarSuite_Final
   ./RadarSuite_Final
   ```

## What's New in This Fix

1. **RUN_BUILD_ALL.sh** - New Linux/macOS build script with:
   - Automatic Python 3.11 detection
   - Better error handling and colored output
   - System-specific commands for Linux/macOS
   - Detailed logging to super_log.txt

2. **Updated requirements.txt** - Ensures PyInstaller 6.0+ is installed

3. **Better error messages** - Clear instructions for common issues

## Quick Reference

| Platform | Build Script | Output Location |
|----------|--------------|-----------------|
| Linux/macOS | `./RUN_BUILD_ALL.sh` | `dist/RadarSuite_Final/RadarSuite_Final` |
| Windows | `RUN_BUILD_ALL.cmd` | `dist\RadarSuite_Final\RadarSuite_Final.exe` |

## Need More Help?

1. Check the build log: `cat super_log.txt`
2. Verify Python version: `python --version` (should be 3.11.x)
3. Check installed packages: `pip list`
4. Test PyInstaller: `pyinstaller --version`

If you continue to have issues, please provide:
- Your operating system and version
- Python version (`python --version`)
- Contents of `super_log.txt`
- Error messages you're seeing
