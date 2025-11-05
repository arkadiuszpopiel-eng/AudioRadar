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
pip install -q sounddevice numpy scipy pygame
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
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
