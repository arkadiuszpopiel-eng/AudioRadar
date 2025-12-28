@echo off
REM ============================================================================
REM Radar Games ML v4.3 - Windows Build Script
REM Builds standalone Windows EXE using PyInstaller
REM Platform: Windows x64 ONLY
REM Requires: Python 3.11
REM
REM PORTED FROM RadarSuite V4.2.1 RUN_BUILD_ALL_Win.cmd
REM ADAPTED FOR Radar Games ML v4.3 structure
REM ============================================================================

setlocal EnableDelayedExpansion

echo.
echo ========================================================================
echo   Radar Games ML v4.3 - Build System
echo   Building Windows standalone EXE with PyInstaller
echo   Platform: Windows x64 ONLY
echo ========================================================================
echo.

REM Get script directory
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM FIXED v4.3.1-k0006: Create centralized log directory (regression fix)
set "LOG_DIR=%SCRIPT_DIR%log"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM Set version (read from app/version.py dynamically)
for /f "delims=" %%i in ('python -c "import sys; sys.path.insert(0, 'app'); from version import __version_full__; print(__version_full__)"') do set "VERSION=%%i"
if "%VERSION%"=="" set "VERSION=v4.3.0-k0001"

set "PLATFORM=Win64"
set "BUILD_DATE=%date:~-4%-%date:~3,2%-%date:~0,2%"
set "BUILD_TIME=%time:~0,2%-%time:~3,2%-%time:~6,2%"
set "BUILD_TIME=!BUILD_TIME: =0!"

REM Log file - FIXED v4.3.1-k0006: Moved to log directory
set "LOG_FILE=%LOG_DIR%\build_windows.log"

REM Start logging
echo [%date% %time%] ============================================================ >> "%LOG_FILE%"
echo [%date% %time%] BUILD STARTED - Radar Games ML v4.3 >> "%LOG_FILE%"
echo [%date% %time%] ============================================================ >> "%LOG_FILE%"
echo [%date% %time%] Version: %VERSION% >> "%LOG_FILE%"
echo [%date% %time%] Script Directory: %SCRIPT_DIR% >> "%LOG_FILE%"
echo [%date% %time%] Build Date: %BUILD_DATE% >> "%LOG_FILE%"
echo [%date% %time%] Build Time: %BUILD_TIME% >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

echo [INFO] Radar Games ML v4.3 - Windows Build
echo [INFO] This is the WINDOWS-ONLY version
echo [%date% %time%] [INFO] Platform: Windows x64 only >> "%LOG_FILE%"
echo.

echo [STEP 1/6] Checking Python 3.11 installation...
echo [%date% %time%] [STEP 1/6] Checking Python 3.11... >> "%LOG_FILE%"

py -3.11 --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3.11 is not installed or not in PATH!
    echo [%date% %time%] [ERROR] Python 3.11 not found >> "%LOG_FILE%"
    echo.
    echo Please install Python 3.11 from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('py -3.11 --version') do set PYTHON_VERSION=%%i
echo    - Found: %PYTHON_VERSION%
echo [%date% %time%] Found: %PYTHON_VERSION% >> "%LOG_FILE%"
echo.

echo [STEP 2/6] Creating/Activating virtual environment...
echo [%date% %time%] [STEP 2/6] Creating venv... >> "%LOG_FILE%"

if not exist ".venv" (
    echo    - Creating new venv...
    echo [%date% %time%] Creating new venv... >> "%LOG_FILE%"
    py -3.11 -m venv .venv >> "%LOG_FILE%" 2>&1
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        echo [%date% %time%] [ERROR] venv creation failed >> "%LOG_FILE%"
        pause
        exit /b 1
    )
) else (
    echo    - Using existing venv
    echo [%date% %time%] Using existing venv >> "%LOG_FILE%"
)

call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    echo [%date% %time%] [ERROR] venv activation failed >> "%LOG_FILE%"
    pause
    exit /b 1
)

echo    - Virtual environment activated
echo [%date% %time%] venv activated >> "%LOG_FILE%"
echo.

echo [STEP 3/6] Upgrading pip, setuptools, wheel...
echo [%date% %time%] [STEP 3/6] Upgrading pip... >> "%LOG_FILE%"

python -m pip install --upgrade pip setuptools wheel >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo [WARNING] pip upgrade had issues, continuing...
)

echo    - pip upgraded
echo.

echo [STEP 4/6] Installing requirements...
echo [%date% %time%] [STEP 4/6] Installing requirements... >> "%LOG_FILE%"
echo.

REM Install from requirements-windows.txt (WINDOWS-SPECIFIC)
if exist "requirements-windows.txt" (
    echo    - Installing from requirements-windows.txt (Windows optimized^)...
    echo [%date% %time%] Installing from requirements-windows.txt >> "%LOG_FILE%"
    pip install -r requirements-windows.txt >> "%LOG_FILE%" 2>&1
    if errorlevel 1 (
        echo [ERROR] Failed to install requirements from requirements-windows.txt
        echo [%date% %time%] [ERROR] Requirements installation failed >> "%LOG_FILE%"
        pause
        exit /b 1
    )
) else if exist "requirements.txt" (
    echo    - Installing from requirements.txt...
    echo [%date% %time%] Installing from requirements.txt >> "%LOG_FILE%"
    pip install -r requirements.txt >> "%LOG_FILE%" 2>&1
    if errorlevel 1 (
        echo [ERROR] Failed to install requirements from requirements.txt
        echo [%date% %time%] [ERROR] Requirements installation failed >> "%LOG_FILE%"
        pause
        exit /b 1
    )
) else (
    echo [ERROR] No requirements file found!
    echo [%date% %time%] [ERROR] No requirements file found >> "%LOG_FILE%"
    pause
    exit /b 1
)

echo.
echo    All Python requirements installed
echo [%date% %time%] All requirements installed >> "%LOG_FILE%"
echo.

REM FIXED v4.3.1-k0013: Ensure ML dependencies are installed (auto-install from PyPI)
echo    - Ensuring ML dependencies (joblib, scikit-learn)...
echo [%date% %time%] Installing ML dependencies... >> "%LOG_FILE%"
pip install --quiet joblib scikit-learn >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo [WARNING] ML dependencies install had issues, continuing...
    echo [%date% %time%] [WARNING] ML dependencies install issues >> "%LOG_FILE%"
) else (
    echo    - ML dependencies installed successfully
    echo [%date% %time%] ML dependencies installed >> "%LOG_FILE%"
)
echo.

echo [STEP 5/6] Verifying installation...
echo [%date% %time%] [STEP 5/6] Verifying installation... >> "%LOG_FILE%"

REM Verify modules without initializing native libraries (sounddevice/soundcard)
REM FIXED v4.3.1-k0013: Added joblib and sklearn to verification
python -c "import sys; import importlib.util; modules=['PyQt5', 'pyqtgraph', 'OpenGL', 'numpy', 'scipy', 'sounddevice', 'soundcard', 'psutil', 'PyInstaller', 'joblib', 'sklearn']; failed=[]; [failed.append(m) if importlib.util.find_spec(m) is None else print(f'OK: {m}') for m in modules]; sys.exit(1) if failed else print('All modules installed OK')" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo [ERROR] Module verification failed!
    echo [%date% %time%] [ERROR] Module verification failed >> "%LOG_FILE%"
    echo.
    echo Some required modules could not be imported.
    echo Please check %LOG_FILE% for details.
    echo.
    echo Common fixes:
    echo   - Ensure you have Visual C++ Redistributable installed
    echo   - Try running as Administrator
    echo   - Check Windows Defender / Antivirus settings
    pause
    exit /b 1
)

REM Note: sounddevice may require PortAudio DLL at runtime
REM This verification only checks if the Python package is installed
echo    - All modules verified successfully (package check only)
echo    - Note: sounddevice/soundcard require PortAudio DLL at runtime
echo [%date% %time%] All modules verified (package check only) >> "%LOG_FILE%"
echo.

REM Verify PyInstaller is installed
echo    - Checking PyInstaller...
python -c "import PyInstaller; print(f'PyInstaller {PyInstaller.__version__}')" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo [ERROR] PyInstaller not available!
    echo [ERROR] Try: python -m pip install pyinstaller
    echo [%date% %time%] [ERROR] PyInstaller module not found >> "%LOG_FILE%"
    pause
    exit /b 1
)
python -c "import PyInstaller; print('   - PyInstaller version:', PyInstaller.__version__)"
echo [%date% %time%] PyInstaller available >> "%LOG_FILE%"
echo.
echo [STEP 6/6] Building EXE with PyInstaller...
echo [%date% %time%] [STEP 6/6] Building EXE... >> "%LOG_FILE%"
echo.

REM Clean previous build
if exist "build" (
    echo    - Cleaning old build directory...
    rmdir /s /q build
)

if exist "dist" (
    echo    - Cleaning old dist directory...
    rmdir /s /q dist
)

if exist "Radar_Games_ML.exe" (
    echo    - Removing old EXE from root...
    del /q Radar_Games_ML.exe
)

echo    - Running PyInstaller...
echo [%date% %time%] Running PyInstaller with spec file... >> "%LOG_FILE%"

REM v4.3: Uses radarsuite_windows.spec (ported from v4.2.1)
python -m PyInstaller --clean --noconfirm build_tools\radarsuite_windows.spec >> "%LOG_FILE%" 2>&1

if errorlevel 1 (
    echo [ERROR] PyInstaller build failed!
    echo [%date% %time%] [ERROR] PyInstaller failed >> "%LOG_FILE%"
    echo.
    echo Build failed. Check %LOG_FILE% for details.
    echo.
    echo Last 30 lines of log:
    powershell -Command "Get-Content '%LOG_FILE%' -Tail 30"
    pause
    exit /b 1
)

echo.
echo    - EXE built successfully!
echo [%date% %time%] PyInstaller build completed >> "%LOG_FILE%"

REM Verify EXE exists
set "APP_DIR=dist\Radar_Games_ML"
if not exist "%APP_DIR%\Radar_Games_ML.exe" (
    echo [ERROR] EXE not found in dist!
    echo [%date% %time%] [ERROR] EXE not found >> "%LOG_FILE%"
    pause
    exit /b 1
)

echo    - EXE location: %APP_DIR%\Radar_Games_ML.exe
echo [%date% %time%] EXE created: %APP_DIR%\Radar_Games_ML.exe >> "%LOG_FILE%"

REM Verify EXE was copied to root by post-build script in spec file
if exist "Radar_Games_ML.exe" (
    echo    - EXE also copied to project root: Radar_Games_ML.exe
    echo [%date% %time%] EXE copied to root: Radar_Games_ML.exe >> "%LOG_FILE%"
    for %%A in ("Radar_Games_ML.exe") do set "EXE_SIZE=%%~zA"
) else (
    for %%A in ("%APP_DIR%\Radar_Games_ML.exe") do set "EXE_SIZE=%%~zA"
)

echo    - EXE size: !EXE_SIZE! bytes
echo [%date% %time%] EXE size: !EXE_SIZE! bytes >> "%LOG_FILE%"
echo.

echo.
echo ========================================================================
echo   BUILD COMPLETED SUCCESSFULLY!
echo ========================================================================
echo.
echo Build Information:
echo   - Version: %VERSION%
echo   - Date: %BUILD_DATE%
echo   - Time: %BUILD_TIME%
echo   - Python: %PYTHON_VERSION%
echo.
echo Output:
echo   - EXE Directory: %APP_DIR%
echo   - EXE File: Radar_Games_ML.exe
echo   - EXE Size: !EXE_SIZE! bytes
if exist "Radar_Games_ML.exe" (
    echo   - Quick Launch: Radar_Games_ML.exe (copied to root)
)
echo.
echo Logs:
echo   - Build Log: %LOG_FILE%
echo   - Runtime log will be created as super_log.txt when you run the EXE
echo.
echo To run the application:
if exist "Radar_Games_ML.exe" (
    echo   Quick: Double-click Radar_Games_ML.exe in this directory
    echo   Or:    1. Go to: %APP_DIR%
    echo          2. Double-click: Radar_Games_ML.exe
) else (
    echo   1. Go to: %APP_DIR%
    echo   2. Double-click: Radar_Games_ML.exe
)
echo.
echo ========================================================================

echo [%date% %time%] ============================================================ >> "%LOG_FILE%"
echo [%date% %time%] BUILD COMPLETED SUCCESSFULLY >> "%LOG_FILE%"
echo [%date% %time%] ============================================================ >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

REM ADDED v4.3.1-k0006: Copy build log to centralized all_logs/ for easy review
echo [%date% %time%] Copying build log to all_logs/... >> "%LOG_FILE%"
python -c "from pathlib import Path; from app.core.log_aggregator import copy_to_all_logs; copy_to_all_logs(Path('log/build_windows.log'), 'build')" 2>nul
if errorlevel 1 (
    echo [%date% %time%] Warning: Could not copy to all_logs/ ^(optional^) >> "%LOG_FILE%"
) else (
    echo [%date% %time%] Build log copied to all_logs/build/ >> "%LOG_FILE%"
)

pause
