@echo off
REM Radar Games ML v4.3.1 - Simple Launcher
REM Double-click this file to start the application

echo.
echo ================================================
echo   Radar Games ML v4.3.1 - Starting...
echo ================================================
echo.

REM Navigate to the app directory
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.11 from python.org
    echo.
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking dependencies...
python -c "import joblib, sklearn, numpy, scipy, sounddevice, PyQt5" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installing missing dependencies...
    echo This will only happen once!
    echo.
    pip install joblib scikit-learn numpy scipy sounddevice PyQt5 pyqtgraph soundcard psutil
    echo.
    echo Dependencies installed!
    echo.
)

REM Start the application
echo Starting Radar Games ML...
echo.

REM Run as Python module (required for absolute imports)
python -m app.main

REM If there was an error, keep window open
if errorlevel 1 (
    echo.
    echo ================================================
    echo   An error occurred!
    echo ================================================
    echo.
    pause
)
