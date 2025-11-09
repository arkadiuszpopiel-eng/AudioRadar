@echo off
REM =============================================================================
REM  RUN_BUILD_ALL.cmd
REM
REM  This batch script installs Python dependencies, builds executable with
REM  PyInstaller (optional), and launches the AudioRadar v10.0 GUI application.
REM  It is designed for Windows systems.
REM =============================================================================

echo ================================================================
echo   AudioRadar v10.0 - Build and Run Script
echo ================================================================
echo.

REM Check for build argument
if "%1"=="build" goto BUILD

:RUN
echo Installing dependencies...
python -m pip install --user PyQt5 numpy sounddevice pygame psutil scipy pyaudiowpatch
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies. See the console output for details.
    pause
    goto :EOF
)

echo.
echo [OK] Dependencies installed
echo.
echo Starting AudioRadar v10.0 GUI...
REM Run the main script. It will handle both module and script execution.
python main.py

echo.
echo Application exited. Refer to log_v10.txt for details.
pause
goto :EOF

:BUILD
echo [INFO] Building executable with PyInstaller...
echo.

REM Install PyInstaller
python -m pip install --user pyinstaller
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install PyInstaller
    pause
    goto :EOF
)

REM Build executable
pyinstaller --noconfirm ^
    --onefile ^
    --windowed ^
    --name AudioRadar_v10_GUI ^
    --add-data "theme_manager.py;." ^
    --add-data "performance_monitor.py;." ^
    --add-data "gui.py;." ^
    --add-data "audio_capture.py;." ^
    --add-data "sound_analysis.py;." ^
    --add-data "README_PL.txt;." ^
    --add-data "QUICK_START.txt;." ^
    --hidden-import PyQt5 ^
    --hidden-import PyQt5.QtWidgets ^
    --hidden-import PyQt5.QtCore ^
    --hidden-import PyQt5.QtGui ^
    --hidden-import sounddevice ^
    --hidden-import numpy ^
    --hidden-import scipy ^
    --hidden-import psutil ^
    main.py

if %errorlevel% neq 0 (
    echo [ERROR] Build failed!
    pause
    goto :EOF
)

echo.
echo [OK] Build complete! Executable in dist\AudioRadar_v10_GUI.exe
pause
goto :EOF
