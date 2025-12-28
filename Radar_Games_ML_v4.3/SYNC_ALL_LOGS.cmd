@echo off
REM ============================================================================
REM Radar Games ML v4.3.1-k0006 - Manual Log Sync Script
REM Copies all logs from log/ and raport/ to all_logs/ for easy review
REM ============================================================================

echo.
echo ========================================================================
echo   Radar Games ML v4.3.1-k0006 - Log Synchronization
echo   Copying all logs to all_logs/ directory...
echo ========================================================================
echo.

python -c "from app.core.log_aggregator import aggregate_all_existing_logs, create_readme; print('Creating all_logs/ directory...'); create_readme(); print('Copying logs...'); summary = aggregate_all_existing_logs(); print('\nSummary:'); print(f'  Runtime logs: {len(summary[\"runtime\"])} files'); print(f'  Build logs: {len(summary[\"build\"])} files'); print(f'  SelfTest logs: {len(summary[\"selftest\"])} files'); print(f'  ML Training reports: {len(summary[\"ml_training\"])} files'); print('\nDone! Check all_logs/ directory for consolidated logs.')"

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to sync logs
    echo Make sure you're in the Radar_Games_ML_v4.3 directory
    pause
    exit /b 1
)

echo.
echo ========================================================================
echo   SUCCESS! All logs copied to all_logs/ directory
echo ========================================================================
echo.
echo You can now review all logs in:
echo   all_logs\runtime\     - Runtime logs
echo   all_logs\build\       - Build logs
echo   all_logs\selftest\    - Test logs
echo   all_logs\ml_training\ - ML training reports
echo.
echo See all_logs\README.txt for more information
echo.
pause
