@echo off
title AudioRadar v10.1
color 0B

echo ===============================================================================
echo    AudioRadar v10.1 - PyQt5 GUI
echo ===============================================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found
    pause
    exit /b 1
)

echo [OK] Python found
echo.

pip install -q PyQt5 pyaudiowpatch sounddevice numpy scipy psutil

echo [INFO] Starting GUI...
python __main__.py

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start
    pause
)
