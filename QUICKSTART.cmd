@echo off
REM Quick Start Script for Audio Radar
REM This script installs dependencies and runs Audio Radar

echo ================================================
echo           Audio Radar Quick Start
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or newer from python.org
    pause
    exit /b 1
)

echo [1/4] Checking Python installation...
python --version

echo.
echo [2/4] Installing dependencies...
echo Installing audio libraries...
pip install -q sounddevice numpy scipy
if errorlevel 1 (
    echo ERROR: Failed to install audio libraries
    pause
    exit /b 1
)

echo Installing pygame (this may take a moment)...
pip install pygame --only-binary :all: -q
if errorlevel 1 (
    echo WARNING: Pre-built pygame failed, trying from source...
    pip install pygame -q
    if errorlevel 1 (
        echo.
        echo ERROR: pygame installation failed
        echo.
        echo This usually happens on newer Python versions (3.13+)
        echo.
        echo SOLUTIONS:
        echo 1. Use Python 3.11 or 3.12 (recommended)
        echo 2. Install Visual Studio Build Tools
        echo 3. Try: pip install -r requirements-windows.txt
        echo.
        echo See INSTALL.md for detailed troubleshooting
        pause
        exit /b 1
    )
)

echo.
echo [3/4] Checking audio devices...
cd audio_radar_v10\audio_radar
python main.py --list-devices

echo.
echo [4/4] Starting Audio Radar...
echo.
echo Instructions:
echo - Green bars = Footsteps
echo - Red bars = Gunshots
echo - Press Z/X to adjust bar width
echo - Press C/V to adjust bar height
echo - Press B/N to adjust transparency
echo.
pause

python main.py

pause
