@echo off
title AudioRadar v10.0
color 0B

echo ================================================================
echo   AudioRadar v10.0 - Optimized Core
echo ================================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Install Python 3.9+ from https://www.python.org
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Install dependencies
echo [INFO] Checking dependencies...
pip install -q PyQt5 pyaudiowpatch sounddevice numpy scipy psutil pygame

REM Launch
echo [INFO] Starting AudioRadar v10.0...
echo.
python main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Application failed!
    pause
)
