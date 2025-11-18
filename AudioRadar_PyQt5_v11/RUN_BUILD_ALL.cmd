@echo off
REM ============================================================================
REM AudioRadar PyQt5 v11 - Build and Package Script
REM Automatically installs dependencies, tests, and creates ZIP archive
REM ============================================================================

setlocal EnableDelayedExpansion

echo.
echo ========================================================================
echo   AUDIO RADAR v11 - PyQt5 Professional Edition
echo   Build and Package Script
echo ========================================================================
echo.

REM Get script directory
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Set version
set "VERSION=v11"
set "BUILD_DATE=%date:~-4%-%date:~3,2%-%date:~0,2%"
set "BUILD_TIME=%time:~0,2%-%time:~3,2%-%time:~6,2%"
set "BUILD_TIME=!BUILD_TIME: =0!"

REM Log file
set "LOG_FILE=build_log.txt"

REM Start logging
echo [%date% %time%] ====== BUILD STARTED ====== > "%LOG_FILE%"
echo [%date% %time%] Version: %VERSION% >> "%LOG_FILE%"
echo [%date% %time%] Script Directory: %SCRIPT_DIR% >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

echo [STEP 1/6] Checking Python installation...
echo [%date% %time%] [STEP 1/6] Checking Python installation... >> "%LOG_FILE%"

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo [%date% %time%] [ERROR] Python not found in PATH >> "%LOG_FILE%"
    echo.
    echo Please install Python 3.7 or newer from https://www.python.org/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo    - Found: %PYTHON_VERSION%
echo [%date% %time%] Found: %PYTHON_VERSION% >> "%LOG_FILE%"
echo.

echo [STEP 2/6] Checking pip installation...
echo [%date% %time%] [STEP 2/6] Checking pip installation... >> "%LOG_FILE%"

python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not installed!
    echo [%date% %time%] [ERROR] pip not found >> "%LOG_FILE%"
    echo.
    echo Installing pip...
    python -m ensurepip --upgrade
)

echo    - pip is available
echo [%date% %time%] pip is available >> "%LOG_FILE%"
echo.

echo [STEP 3/6] Installing/Upgrading required packages...
echo [%date% %time%] [STEP 3/6] Installing required packages... >> "%LOG_FILE%"
echo.

echo    - Installing numpy...
echo [%date% %time%] Installing numpy... >> "%LOG_FILE%"
python -m pip install --upgrade numpy >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo [WARNING] numpy installation had warnings, continuing...
)

echo    - Installing scipy...
echo [%date% %time%] Installing scipy... >> "%LOG_FILE%"
python -m pip install --upgrade scipy >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo [WARNING] scipy installation had warnings, continuing...
)

echo    - Installing sounddevice...
echo [%date% %time%] Installing sounddevice... >> "%LOG_FILE%"
python -m pip install --upgrade sounddevice >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo [WARNING] sounddevice installation had warnings, continuing...
)

echo    - Installing PyQt5...
echo [%date% %time%] Installing PyQt5... >> "%LOG_FILE%"
python -m pip install --upgrade PyQt5 >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo [WARNING] PyQt5 installation had warnings, continuing...
)

echo.
echo    All packages installed successfully!
echo [%date% %time%] All packages installed >> "%LOG_FILE%"
echo.

echo [STEP 4/6] Verifying installation...
echo [%date% %time%] [STEP 4/6] Verifying installation... >> "%LOG_FILE%"

REM Test imports
python -c "import numpy; import scipy; import sounddevice; from PyQt5 import QtWidgets; print('All modules imported successfully')" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Module verification failed!
    echo [%date% %time%] [ERROR] Module verification failed >> "%LOG_FILE%"
    echo.
    echo Some required modules could not be imported.
    echo Please check the build_log.txt for details.
    pause
    exit /b 1
)

echo    - All required modules verified
echo [%date% %time%] All modules verified successfully >> "%LOG_FILE%"
echo.

echo [STEP 5/6] Running quick syntax check...
echo [%date% %time%] [STEP 5/6] Running syntax check... >> "%LOG_FILE%"

REM Check syntax of main files
python -m py_compile main.py 2>> "%LOG_FILE%"
if errorlevel 1 (
    echo [ERROR] Syntax error in main.py
    echo [%date% %time%] [ERROR] Syntax error in main.py >> "%LOG_FILE%"
    pause
    exit /b 1
)

python -m py_compile audio_radar_gui.py 2>> "%LOG_FILE%"
python -m py_compile audio_manager.py 2>> "%LOG_FILE%"
python -m py_compile sound_detector.py 2>> "%LOG_FILE%"
python -m py_compile radar_widget.py 2>> "%LOG_FILE%"
python -m py_compile spectrum_analyzer.py 2>> "%LOG_FILE%"
python -m py_compile theme_manager.py 2>> "%LOG_FILE%"
python -m py_compile config_manager.py 2>> "%LOG_FILE%"
python -m py_compile logger.py 2>> "%LOG_FILE%"

echo    - All Python files passed syntax check
echo [%date% %time%] All files passed syntax check >> "%LOG_FILE%"
echo.

echo [STEP 6/6] Creating ZIP archive...
echo [%date% %time%] [STEP 6/6] Creating ZIP archive... >> "%LOG_FILE%"

REM Create archive name
set "ARCHIVE_NAME=AudioRadar_PyQt5_%VERSION%_%BUILD_DATE%_%BUILD_TIME%.zip"

REM Check if PowerShell is available (for ZIP creation)
where powershell >nul 2>&1
if errorlevel 1 (
    echo [WARNING] PowerShell not found, ZIP creation skipped
    echo [%date% %time%] [WARNING] PowerShell not available for ZIP creation >> "%LOG_FILE%"
    goto :SKIP_ZIP
)

REM Create temp directory for archive
set "TEMP_DIR=AudioRadar_PyQt5_%VERSION%_temp"
if exist "%TEMP_DIR%" (
    echo    - Removing old temp directory...
    rmdir /s /q "%TEMP_DIR%"
)

echo    - Creating temp directory...
mkdir "%TEMP_DIR%"

REM Copy files to temp directory
echo    - Copying files...
echo [%date% %time%] Copying files to temp directory... >> "%LOG_FILE%"

copy /y "main.py" "%TEMP_DIR%\" >> "%LOG_FILE%"
copy /y "audio_radar_gui.py" "%TEMP_DIR%\" >> "%LOG_FILE%"
copy /y "audio_manager.py" "%TEMP_DIR%\" >> "%LOG_FILE%"
copy /y "sound_detector.py" "%TEMP_DIR%\" >> "%LOG_FILE%"
copy /y "radar_widget.py" "%TEMP_DIR%\" >> "%LOG_FILE%"
copy /y "spectrum_analyzer.py" "%TEMP_DIR%\" >> "%LOG_FILE%"
copy /y "theme_manager.py" "%TEMP_DIR%\" >> "%LOG_FILE%"
copy /y "config_manager.py" "%TEMP_DIR%\" >> "%LOG_FILE%"
copy /y "logger.py" "%TEMP_DIR%\" >> "%LOG_FILE%"
copy /y "requirements.txt" "%TEMP_DIR%\" >> "%LOG_FILE%"
copy /y "README_PL.txt" "%TEMP_DIR%\" >> "%LOG_FILE%"
copy /y "RUN_BUILD_ALL.cmd" "%TEMP_DIR%\" >> "%LOG_FILE%"
copy /y "%LOG_FILE%" "%TEMP_DIR%\" >> "%LOG_FILE%"

REM Create default config if doesn't exist
if not exist "%TEMP_DIR%\config.json" (
    echo {> "%TEMP_DIR%\config.json"
    echo   "audio": {>> "%TEMP_DIR%\config.json"
    echo     "input_device_index": -1,>> "%TEMP_DIR%\config.json"
    echo     "sample_rate": 48000,>> "%TEMP_DIR%\config.json"
    echo     "block_size": 2048,>> "%TEMP_DIR%\config.json"
    echo     "channels": 2>> "%TEMP_DIR%\config.json"
    echo   },>> "%TEMP_DIR%\config.json"
    echo   "detection": {>> "%TEMP_DIR%\config.json"
    echo     "walking_enabled": true,>> "%TEMP_DIR%\config.json"
    echo     "running_enabled": true,>> "%TEMP_DIR%\config.json"
    echo     "shooting_enabled": true,>> "%TEMP_DIR%\config.json"
    echo     "confidence_threshold": 0.5>> "%TEMP_DIR%\config.json"
    echo   },>> "%TEMP_DIR%\config.json"
    echo   "radar": {>> "%TEMP_DIR%\config.json"
    echo     "opacity": 0.9,>> "%TEMP_DIR%\config.json"
    echo     "fade_duration": 2.0>> "%TEMP_DIR%\config.json"
    echo   },>> "%TEMP_DIR%\config.json"
    echo   "ui": {>> "%TEMP_DIR%\config.json"
    echo     "theme": "dark">> "%TEMP_DIR%\config.json"
    echo   }>> "%TEMP_DIR%\config.json"
    echo }>> "%TEMP_DIR%\config.json"
)

REM Remove old archive if exists
if exist "%ARCHIVE_NAME%" (
    echo    - Removing old archive...
    del /f "%ARCHIVE_NAME%"
)

REM Create ZIP archive using PowerShell
echo    - Creating ZIP archive: %ARCHIVE_NAME%
echo [%date% %time%] Creating ZIP: %ARCHIVE_NAME% >> "%LOG_FILE%"

powershell -command "Compress-Archive -Path '%TEMP_DIR%\*' -DestinationPath '%ARCHIVE_NAME%' -Force" >> "%LOG_FILE%" 2>&1

if errorlevel 1 (
    echo [ERROR] Failed to create ZIP archive
    echo [%date% %time%] [ERROR] ZIP creation failed >> "%LOG_FILE%"
) else (
    echo    - ZIP archive created successfully!
    echo [%date% %time%] ZIP created successfully >> "%LOG_FILE%"

    REM Get file size
    for %%A in ("%ARCHIVE_NAME%") do set "ZIP_SIZE=%%~zA"
    echo    - Archive size: !ZIP_SIZE! bytes
    echo [%date% %time%] Archive size: !ZIP_SIZE! bytes >> "%LOG_FILE%"
)

REM Clean up temp directory
echo    - Cleaning up...
rmdir /s /q "%TEMP_DIR%"

:SKIP_ZIP

echo.
echo ========================================================================
echo   BUILD COMPLETED SUCCESSFULLY!
echo ========================================================================
echo.
echo Build Information:
echo   - Version: %VERSION%
echo   - Date: %BUILD_DATE%
echo   - Time: %BUILD_TIME%
if exist "%ARCHIVE_NAME%" (
    echo   - Archive: %ARCHIVE_NAME%
)
echo   - Log: %LOG_FILE%
echo.
echo To run the program:
echo   python main.py
echo.
echo All build information has been saved to %LOG_FILE%
echo A comprehensive runtime log will be created in log.txt when you run the program.
echo.
echo ========================================================================

echo [%date% %time%] ====== BUILD COMPLETED SUCCESSFULLY ====== >> "%LOG_FILE%"

pause
