@echo off
REM ============================================================================
REM  PACK_ZIP.cmd - AudioRadar v10.2 COMPLETE Packager
REM
REM  This script creates a distributable ZIP archive containing the complete
REM  AudioRadar v10.2 application and documentation.
REM ============================================================================

echo ========================================
echo   AudioRadar v10.2 ZIP Packager
echo ========================================
echo.

set OUTPUT_ZIP=AudioRadar_v10.2_COMPLETE.zip
set TEMP_DIR=AudioRadar_v10.2_COMPLETE

echo Creating temporary directory...
if exist %TEMP_DIR% rmdir /s /q %TEMP_DIR%
mkdir %TEMP_DIR%

echo Copying application files...
xcopy /E /I /Y audio_radar %TEMP_DIR%\audio_radar

echo Copying documentation and scripts...
copy /Y START_HERE.bat %TEMP_DIR%\
copy /Y RUN_BUILD_ALL.cmd %TEMP_DIR%\
copy /Y PACK_ZIP.cmd %TEMP_DIR%\
copy /Y README_PL.txt %TEMP_DIR%\
copy /Y QUICK_START.txt %TEMP_DIR%\
copy /Y TROUBLESHOOTING.txt %TEMP_DIR%\
copy /Y CHANGELOG.txt %TEMP_DIR%\
copy /Y VERSION.txt %TEMP_DIR%\

echo Creating ZIP archive...
powershell -Command "Compress-Archive -Path '%TEMP_DIR%\*' -DestinationPath '%OUTPUT_ZIP%' -Force"

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS: Created %OUTPUT_ZIP%
) else (
    echo.
    echo ERROR: Failed to create ZIP archive
)

echo Cleaning up temporary directory...
rmdir /s /q %TEMP_DIR%

echo.
echo Done.
pause
