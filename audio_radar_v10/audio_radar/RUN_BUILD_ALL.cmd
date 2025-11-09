@echo off
REM =============================================================================
REM  RUN_BUILD_ALL.cmd
REM
REM  This batch script installs Python dependencies and launches the Audio
REM  Radar v10.1 application with PyQt5 GUI. It is designed for Windows 
REM  systems. The script installs required packages in the current user's 
REM  environment via pip and then runs the program.
REM =============================================================================

echo ===============================================================================
echo   AudioRadar v10.1 - PyQt5 GUI Installation
echo ===============================================================================
echo.

echo [1/3] Checking Python...
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python 3.8 or newer.
    pause
    goto :EOF
)
echo.

echo [2/3] Installing dependencies...
echo Installing: PyQt5, sounddevice, numpy, scipy, psutil, pyaudiowpatch
python -m pip install --user PyQt5 sounddevice numpy scipy psutil pyaudiowpatch
if %errorlevel% neq 0 (
    echo [WARN] Some packages failed to install. Trying to continue anyway...
)
echo.

echo [3/3] Starting AudioRadar v10.1 PyQt5 GUI...
REM Run the __main__.py which launches PyQt5 GUI
python __main__.py

echo.
echo Application exited.
pause
