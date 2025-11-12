@echo off
setlocal enabledelayedexpansion

:: Audio Radar - Complete Build Script
:: Python 3.11.9 Required
:: Generated: 2025-11-12 21:48:06 UTC

echo ========================================
echo Audio Radar - Build System
echo ========================================
echo Start Time: %date% %time%
echo.

:: Initialize log file
set LOG_FILE=log.txt
echo ======================================== > %LOG_FILE%
echo Audio Radar Build Log >> %LOG_FILE%
echo Start Time: %date% %time% >> %LOG_FILE%
echo ======================================== >> %LOG_FILE%
echo. >> %LOG_FILE%

echo [Step 1/8] Checking Python version...
python --version >> %LOG_FILE% 2>&1
if errorlevel 1 (
    echo ERROR: Python not found! >> %LOG_FILE%
    echo ERROR: Python not found! Install Python 3.11.9 first.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Detected Python version: %PYTHON_VERSION% >> %LOG_FILE%
echo Python version: %PYTHON_VERSION%

echo. >> %LOG_FILE%
echo [Step 2/8] Creating virtual environment...
if exist venv (
    echo Removing old virtual environment... >> %LOG_FILE%
    rmdir /s /q venv >> %LOG_FILE% 2>&1
)
python -m venv venv >> %LOG_FILE% 2>&1
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment! >> %LOG_FILE%
    echo ERROR: Failed to create virtual environment!
    pause
    exit /b 1
)
echo Virtual environment created successfully. >> %LOG_FILE%

echo. >> %LOG_FILE%
echo [Step 3/8] Activating virtual environment...
call venv\Scripts\activate.bat >> %LOG_FILE% 2>&1
echo Virtual environment activated. >> %LOG_FILE%

echo. >> %LOG_FILE%
echo [Step 4/8] Upgrading pip...
python -m pip install --upgrade pip >> %LOG_FILE% 2>&1
echo Pip upgraded successfully. >> %LOG_FILE%

echo. >> %LOG_FILE%
echo [Step 5/8] Installing dependencies...
pip install -r requirements.txt >> %LOG_FILE% 2>&1
if errorlevel 1 (
    echo ERROR: Failed to install dependencies! >> %LOG_FILE%
    echo ERROR: Failed to install dependencies!
    echo Check log.txt for details.
    pause
    exit /b 1
)
echo All dependencies installed successfully. >> %LOG_FILE%

echo. >> %LOG_FILE%
echo [Step 6/8] Creating directory structure...
if not exist build mkdir build >> %LOG_FILE% 2>&1
if not exist audioradar\resources mkdir audioradar\resources >> %LOG_FILE% 2>&1
echo Directory structure created. >> %LOG_FILE%

echo. >> %LOG_FILE%
echo [Step 7/8] Running tests...
python -c "import PyQt5; print('PyQt5 imported successfully')" >> %LOG_FILE% 2>&1
python -c "import numpy; print('NumPy imported successfully')" >> %LOG_FILE% 2>&1
python -c "import sounddevice; print('SoundDevice imported successfully')" >> %LOG_FILE% 2>&1
python -c "import scipy; print('SciPy imported successfully')" >> %LOG_FILE% 2>&1
echo All module tests passed. >> %LOG_FILE%

echo. >> %LOG_FILE%
echo [Step 8/8] Building executable...
pyinstaller --noconfirm --onefile --windowed ^
    --name "AudioRadar" ^
    --icon=NONE ^
    --add-data "audioradar;audioradar" ^
    --hidden-import=PyQt5 ^
    --hidden-import=numpy ^
    --hidden-import=sounddevice ^
    --hidden-import=scipy ^
    main.py >> %LOG_FILE% 2>&1

if errorlevel 1 (
    echo WARNING: PyInstaller failed or not installed. Running in script mode. >> %LOG_FILE%
    echo WARNING: PyInstaller failed. Running in script mode.
) else (
    echo Executable built successfully. >> %LOG_FILE%
    echo Executable location: dist\AudioRadar.exe
)

echo. >> %LOG_FILE%
echo ======================================== >> %LOG_FILE%
echo Build completed: %date% %time% >> %LOG_FILE%
echo ======================================== >> %LOG_FILE%

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo Log file: log.txt
echo.
echo Starting Audio Radar...
echo. >> %LOG_FILE%
echo [RUNTIME] Starting Audio Radar application... >> %LOG_FILE%

python main.py >> %LOG_FILE% 2>&1

pause
