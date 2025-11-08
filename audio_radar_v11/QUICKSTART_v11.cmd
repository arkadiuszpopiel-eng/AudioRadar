@echo off
REM AudioRadar v11 - Quick Start Script for Windows
REM This script automatically installs dependencies and runs AudioRadar v11

echo ========================================
echo    AudioRadar v11 - Quick Start
echo ========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.11 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    pause
    exit /b 1
)

echo [OK] Python is installed
python --version
echo.

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo Detected Python version: %PYVER%
echo.

REM Install dependencies
echo [STEP 1/3] Installing dependencies...
echo.
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [WARNING] Some packages failed to install with standard method
    echo Trying alternative installation...
    python -m pip install numpy sounddevice
    python -m pip install pygame --only-binary :all:
)
echo.

REM Navigate to audio_radar directory
echo [STEP 2/3] Navigating to audio_radar directory...
cd audio_radar
if errorlevel 1 (
    echo [ERROR] Could not find audio_radar directory!
    pause
    exit /b 1
)
echo.

REM Run AudioRadar v11
echo [STEP 3/3] Starting AudioRadar v11...
echo.
echo ========================================
echo    AudioRadar v11 is starting!
echo ========================================
echo.
echo GUI Interface will open shortly...
echo Check the window for controls and stats!
echo.
echo Press Ctrl+C or close the GUI window to exit.
echo.

python -m audio_radar

REM Handle exit
echo.
echo ========================================
echo    AudioRadar v11 has stopped
echo ========================================
echo.
echo Check audioradar_v11.log for detailed logs
echo.
pause
