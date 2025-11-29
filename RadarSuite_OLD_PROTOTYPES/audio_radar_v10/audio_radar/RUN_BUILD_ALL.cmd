@echo off
REM =============================================================================
REM  RUN_BUILD_ALL.cmd
REM
REM  This batch script installs Python dependencies and launches the Audio
REM  Radar application. It is designed for Windows systems. The script
REM  installs required packages in the current user’s environment via pip
REM  and then runs the program. Logs are written by the Python application
REM  itself into a versioned log file inside the ``audio_radar`` folder
REM  (for example ``log_v9.txt``). No console output is redirected to
REM  the log file here to avoid conflicts when the Python logger writes
REM  concurrently.
REM =============================================================================

echo Installing dependencies...
python -m pip install --user numpy sounddevice pygame
if %errorlevel% neq 0 (
    echo Failed to install dependencies. See the console output for details.
    pause
    goto :EOF
)

echo Starting Audio Radar (version v10)...
REM Run the main script. It will handle both module and script execution.
python main.py

echo Application exited. Refer to the versioned log file in the audio_radar directory for details.
pause