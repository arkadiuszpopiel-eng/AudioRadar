# AudioRadar Build Instructions

## Fix for "[ERROR] PyInstaller not available"

This document explains how to fix the PyInstaller error and build AudioRadar as a standalone executable.

## Problem

The error "[ERROR] PyInstaller not available" occurs when PyInstaller is not installed in your Python environment. PyInstaller is required to package the Python application into a standalone executable (.exe on Windows).

## Solution

We've created the following files to fix this issue:

1. **requirements.txt** - Lists all required Python packages including PyInstaller
2. **audio_radar.spec** - PyInstaller configuration file
3. **BUILD_EXECUTABLE.cmd** - Automated build script for Windows
4. **BUILD_EXECUTABLE.sh** - Automated build script for Linux/Mac

## Building the Executable

### On Windows

1. Open Command Prompt or PowerShell
2. Navigate to the `audio_radar_v10` directory:
   ```cmd
   cd path\to\AudioRadar\audio_radar_v10
   ```

3. Run the build script:
   ```cmd
   BUILD_EXECUTABLE.cmd
   ```

4. The script will:
   - Create a virtual environment
   - Install all dependencies including PyInstaller
   - Build the executable
   - Place the result in `dist\AudioRadar\AudioRadar.exe`

### On Linux/Mac

1. Open Terminal
2. Navigate to the `audio_radar_v10` directory:
   ```bash
   cd path/to/AudioRadar/audio_radar_v10
   ```

3. Make the script executable:
   ```bash
   chmod +x BUILD_EXECUTABLE.sh
   ```

4. Run the build script:
   ```bash
   ./BUILD_EXECUTABLE.sh
   ```

5. The script will:
   - Create a virtual environment
   - Install all dependencies including PyInstaller
   - Build the executable
   - Place the result in `dist/AudioRadar/AudioRadar`

## Manual Installation (Alternative)

If you prefer to install PyInstaller manually:

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   venv\Scripts\activate.bat  # On Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Build with PyInstaller:
   ```bash
   pyinstaller --clean --noconfirm audio_radar.spec
   ```

## Running the Application

### From Source (Development)

```bash
# Install dependencies first
pip install -r requirements.txt

# Run directly
python -m audio_radar

# Or from the audio_radar directory
cd audio_radar
python main.py
```

### From Executable (After Build)

**Windows:**
```cmd
cd dist\AudioRadar
AudioRadar.exe
```

**Linux/Mac:**
```bash
cd dist/AudioRadar
./AudioRadar
```

## Configuration

The application uses `config.json` for configuration. To customize settings:

1. Copy `audio_radar/config.json` to the same directory as your executable
2. Edit the values:
   - `input_device`: Audio input device index (null for default)
   - `output_device`: Audio output device index (null for default)
   - `bar_width`: Width of direction bars in pixels
   - `bar_height`: Height of direction bars in pixels
   - `transparency`: Bar opacity (0-255)

To list available audio devices:
```bash
AudioRadar.exe --list-devices  # Windows
./AudioRadar --list-devices    # Linux/Mac
```

## Troubleshooting

### PyInstaller not found after installation

If you still get the error after running the build script, try:

1. Close and reopen your terminal/command prompt
2. Ensure you're in the virtual environment (you should see `(venv)` in your prompt)
3. Verify PyInstaller is installed:
   ```bash
   pip list | grep pyinstaller  # Linux/Mac
   pip list | findstr pyinstaller  # Windows
   ```

### Build fails with import errors

Make sure all dependencies are installed:
```bash
pip install -r requirements.txt --upgrade
```

### Executable doesn't run

1. Check that all dependencies are included in `audio_radar.spec`
2. Try running with console mode to see error messages
3. Ensure config.json is in the same directory as the executable

## Additional Information

- **Version**: v10
- **Python Version Required**: 3.11+
- **Platform Support**: Windows, Linux, macOS
- **Build Type**: OneFolder (all files in one directory)

For more information, see the main README.md file.
