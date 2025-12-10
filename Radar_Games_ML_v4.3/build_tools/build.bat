@echo off
REM Radar Games ML v4.3.0 Build Script
REM Builds Windows executable using PyInstaller

echo ========================================
echo Radar Games ML v4.3.0 - Build Script
echo ========================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo ERROR: PyInstaller not installed!
    echo Please install: pip install pyinstaller
    pause
    exit /b 1
)

echo Cleaning previous build...
if exist dist\Radar_Games_ML rmdir /s /q dist\Radar_Games_ML
if exist build rmdir /s /q build
if exist Radar_Games_ML.exe del /q Radar_Games_ML.exe

echo.
echo Building executable...
pyinstaller build_tools\radar_games_ml.spec

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo Executable: dist\Radar_Games_ML\Radar_Games_ML.exe
echo Copy to root: Radar_Games_ML.exe
echo.
pause
