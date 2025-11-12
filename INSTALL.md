# Audio Radar - Installation Guide

## Quick Start (Windows)

### Method 1: Automated Installation (Recommended)

1. **Extract Package**
   ```
   Extract AudioRadar.zip to a folder (e.g., C:\AudioRadar)
   ```

2. **Run Build Script**
   ```
   Double-click: RUN_BUILD_ALL.cmd
   ```
   
   The script will:
   - ✅ Check Python installation
   - ✅ Create virtual environment
   - ✅ Install all dependencies
   - ✅ Test modules
   - ✅ Launch application

3. **Done!**
   - Application starts automatically
   - Check log.txt for any issues

### Method 2: Manual Installation

1. **Check Python Version**
   ```cmd
   python --version
   ```
   Required: Python 3.11.9 (or 3.11.x)

2. **Create Virtual Environment**
   ```cmd
   python -m venv venv
   ```

3. **Activate Virtual Environment**
   ```cmd
   venv\Scripts\activate
   ```

4. **Install Dependencies**
   ```cmd
   pip install -r requirements.txt
   ```

5. **Run Application**
   ```cmd
   python main.py
   ```

## System Requirements

### Minimum Requirements
- **OS:** Windows 10 or Windows 11
- **Python:** 3.11.9 (or 3.11.x)
- **RAM:** 2 GB
- **Disk:** 500 MB free space
- **Audio:** Any input device

### Recommended Requirements
- **OS:** Windows 11
- **Python:** 3.11.9
- **RAM:** 4 GB
- **Disk:** 1 GB free space
- **Audio:** Sound Blaster Z SE or 5.1/7.1 capable device

## Dependencies

All dependencies are installed automatically via requirements.txt:

```
PyQt5==5.15.10          # GUI framework
numpy==1.24.3           # Numerical computing
sounddevice==0.4.6      # Audio I/O
scipy==1.11.4           # Signal processing
pyaudio==0.2.14         # Alternative audio interface
pyinstaller==6.3.0      # Executable builder (optional)
```

## Installation Verification

### Test Installation

Run the test script:
```cmd
python test_structure.py
```

Expected output:
```
✅ All tests passed!
```

### Test Audio Device

1. Launch application:
   ```cmd
   python main.py
   ```

2. Click "Audio" → "Select Device..."

3. Select your device

4. Click "Test Device"

Expected: "Device test successful"

## Common Issues

### Python Not Found

**Error:** `'python' is not recognized as an internal or external command`

**Solution:**
1. Install Python 3.11.9 from python.org
2. During installation, check "Add Python to PATH"
3. Restart command prompt

### Missing Dependencies

**Error:** `No module named 'PyQt5'` or similar

**Solution:**
```cmd
pip install -r requirements.txt
```

### Virtual Environment Error

**Error:** Cannot create virtual environment

**Solution:**
```cmd
# Use pip to install virtualenv
pip install virtualenv

# Create venv with virtualenv
virtualenv venv
```

### Audio Device Not Found

**Error:** No input devices found

**Solution:**
1. Check Windows Sound Settings
2. Enable microphone/input device
3. Check device drivers
4. Restart application

### PyInstaller Build Fails

**Note:** This is expected and not critical

The application runs perfectly in script mode:
```cmd
python main.py
```

PyInstaller is optional for creating standalone executables.

## Uninstallation

### Remove Application

1. Delete the AudioRadar folder
2. That's it! No registry entries or system modifications

### Remove Virtual Environment

Already in the folder - deleted with step 1

### Clean System

If you want to remove Python packages installed globally:
```cmd
pip uninstall PyQt5 numpy sounddevice scipy pyaudio pyinstaller
```

## Network Installation

### Installing on Multiple Computers

1. Install on first computer using Method 1
2. Copy entire folder to other computers
3. On each computer:
   ```cmd
   venv\Scripts\activate
   python main.py
   ```

No reinstallation needed - virtual environment is portable!

## Advanced Configuration

### Custom Python Location

If Python is not in PATH:
```cmd
C:\Path\To\Python\python.exe -m venv venv
```

### Custom Installation Location

Install anywhere you want:
```cmd
# Example: D:\MyApps\AudioRadar
cd D:\MyApps\AudioRadar
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Development Installation

For development/modification:
```cmd
# Clone or extract source
cd AudioRadar

# Create development venv
python -m venv venv-dev
venv-dev\Scripts\activate

# Install in editable mode
pip install -e .

# Install dev dependencies
pip install pytest black pylint
```

## Portable Installation

### Creating Portable Package

1. Install normally
2. Copy entire folder to USB drive
3. On any Windows PC:
   ```cmd
   X:\AudioRadar\venv\Scripts\activate
   X:\AudioRadar\python main.py
   ```

### Building Standalone Executable

Use PyInstaller (included):
```cmd
venv\Scripts\activate
pyinstaller --noconfirm --onefile --windowed ^
    --name "AudioRadar" ^
    --add-data "audioradar;audioradar" ^
    main.py
```

Executable will be in `dist\AudioRadar.exe`

## Troubleshooting Installation

### Check Python Installation
```cmd
python --version
python -m pip --version
```

### Check Installed Packages
```cmd
pip list
```

### Reinstall Package
```cmd
pip install --force-reinstall PyQt5
```

### Clean Reinstall
```cmd
# Remove venv
rmdir /s /q venv

# Recreate
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### View Installation Log

All installation steps are logged to `log.txt`

Check for errors:
```cmd
type log.txt | findstr ERROR
```

## Getting Help

1. Check log.txt for errors
2. Review NEW_README.md for usage
3. Run test_structure.py to verify installation
4. Check GitHub issues
5. Contact support with log.txt contents

## License

MIT License - See NEW_README.md for details

---

**Note:** This installation guide is for Windows. For Linux/Mac, replace:
- `venv\Scripts\activate` with `source venv/bin/activate`
- `RUN_BUILD_ALL.cmd` needs to be converted to bash script
