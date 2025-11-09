@echo off
REM ============================================================================
REM AudioRadar v10.0 - Windows Launcher Script
REM ============================================================================

title AudioRadar v10.0 Launcher
color 0B
echo.
echo ===============================================================================
echo                       AudioRadar v10.0 - Optimized Core
echo ===============================================================================
echo.

REM Check for portable executable
if exist "portable\AudioRadar.exe" (
    echo [INFO] Found portable executable: portable\AudioRadar.exe
    echo [INFO] Launching portable version...
    echo.
    cd portable
    start AudioRadar.exe
    timeout /t 2 /nobreak >nul
    exit
)

REM Fallback to Python source
echo [INFO] Portable executable not found, using Python source...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.11+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [OK] Python found:
python --version
echo.

REM Check if PyQt5 is installed
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] PyQt5 is not installed.
    echo.
    echo Do you want to install required dependencies now? (Y/N)
    set /p INSTALL_DEPS="Install dependencies? (Y/N): "
    
    if /i "%INSTALL_DEPS%"=="Y" (
        echo.
        echo [INFO] Installing dependencies...
        echo.
        cd audio_radar
        python -m pip install --upgrade pip
        python -m pip install -r requirements.txt
        cd ..
        echo.
        echo [OK] Dependencies installed successfully!
        echo.
    ) else (
        echo.
        echo [WARNING] Skipping dependency installation.
        echo The application may not work correctly without dependencies.
        echo.
    )
)

REM Launch application
echo [INFO] Launching AudioRadar v10.0...
echo.
cd audio_radar
python -m audio_radar

REM Check exit code
if errorlevel 1 (
    echo.
    echo [ERROR] Application exited with error!
    echo Check log_v10.txt for details.
    echo.
    pause
    exit /b 1
)

echo.
echo [INFO] Application closed normally.
timeout /t 2 /nobreak >nul
