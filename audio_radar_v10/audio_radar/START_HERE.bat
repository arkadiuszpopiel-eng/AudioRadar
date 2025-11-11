@echo off
REM ============================================================================
REM  START_HERE.bat - AudioRadar v10.2 COMPLETE Launcher
REM
REM  This script installs dependencies and launches AudioRadar v10.2.
REM  It will install PyQt5, sounddevice, and numpy if not already present.
REM ============================================================================

echo ========================================
echo   AudioRadar v10.2 COMPLETE
echo ========================================
echo.

echo [1/2] Installing dependencies...
python -m pip install --user PyQt5 sounddevice numpy
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install dependencies.
    echo Please ensure Python is installed and in your PATH.
    pause
    exit /b 1
)

echo.
echo [2/2] Starting AudioRadar v10.2...
echo.

REM Run the application using __main__.py
python audio_radar\__main__.py

if %errorlevel% neq 0 (
    echo.
    echo Application exited with error code %errorlevel%
    echo Check the console output for details.
)

echo.
echo Application closed.
pause
