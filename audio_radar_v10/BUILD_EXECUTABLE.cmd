@echo off
REM =============================================================================
REM  BUILD_EXECUTABLE.cmd
REM
REM  This script creates a standalone executable for AudioRadar using PyInstaller.
REM  It will:
REM  1. Create a virtual environment (if it doesn't exist)
REM  2. Install all required dependencies including PyInstaller
REM  3. Build the executable using PyInstaller
REM  4. Place the result in the 'dist' folder
REM =============================================================================

echo ========================================
echo AudioRadar Build Script (v10)
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.11+ and add it to PATH.
    pause
    goto :EOF
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [1/4] Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        goto :EOF
    )
    echo [OK] Virtual environment created.
) else (
    echo [1/4] Virtual environment already exists.
)

REM Activate virtual environment
echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment.
    pause
    goto :EOF
)
echo [OK] Virtual environment activated.

REM Install dependencies
echo [3/4] Installing dependencies (this may take a few minutes)...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    goto :EOF
)
echo [OK] Dependencies installed.

REM Check if PyInstaller is available
python -c "import PyInstaller" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] PyInstaller not available even after installation.
    echo Please check the installation logs above for errors.
    pause
    goto :EOF
)
echo [OK] PyInstaller is available.

REM Build executable
echo [4/4] Building executable with PyInstaller...
pyinstaller --clean --noconfirm audio_radar.spec
if %errorlevel% neq 0 (
    echo [ERROR] PyInstaller build failed.
    pause
    goto :EOF
)

echo.
echo ========================================
echo [SUCCESS] Build completed!
echo ========================================
echo.
echo The executable is located in: dist\AudioRadar\AudioRadar.exe
echo.
echo To run the application:
echo   1. Navigate to: dist\AudioRadar\
echo   2. Run: AudioRadar.exe
echo.
echo Note: Make sure to copy config.json to the same directory as the executable
echo       if you want to customize settings.
echo.
pause
