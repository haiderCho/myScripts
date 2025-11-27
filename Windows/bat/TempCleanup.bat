@echo off
setlocal enabledelayedexpansion

:: ================================================
:: Enhanced Temporary Files Cleanup Script
:: Author: haiderCho
:: ================================================

echo.
echo ================================================
echo   Windows Temporary Files Cleanup Utility
echo ================================================
echo.
echo This script will clean:
echo  1. User Temp folder (%TEMP%)
echo  2. Windows Temp folder (C:\Windows\Temp)
echo  3. Prefetch folder (C:\Windows\Prefetch)
echo  4. Browser caches (optional)
echo.

:: Confirmation prompt
set /p confirm="Do you want to continue? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo Operation cancelled.
    pause
    exit /b
)

echo.
echo Starting cleanup...
echo.

:: Calculate initial sizes (approximate)
set "total_freed=0"

:: ================================================
:: 1. Clean User Temp Folder
:: ================================================
echo [1/3] Cleaning User Temp folder...
set "user_temp=%TEMP%"

:: Count files before
for /f %%A in ('dir /a-d /s /b "%user_temp%" 2^>nul ^| find /c /v ""') do set "before_count=%%A"

:: Delete files (suppress errors for locked files)
del /s /f /q "%user_temp%\*" 2>nul

:: Delete empty directories
for /d %%D in ("%user_temp%\*") do (
    rd /s /q "%%D" 2>nul
)

:: Count files after
for /f %%A in ('dir /a-d /s /b "%user_temp%" 2^>nul ^| find /c /v ""') do set "after_count=%%A"

set /a "cleaned=before_count-after_count"
echo    Removed approximately %cleaned% files/folders
echo    (Some files may be locked by running programs)

:: ================================================
:: 2. Clean Windows Temp Folder (if admin)
:: ================================================
echo [2/3] Cleaning Windows Temp folder...

:: Check if running as admin
net session >nul 2>&1
if %errorlevel% == 0 (
    echo    Running with administrator privileges...
    
    del /s /f /q "C:\Windows\Temp\*" 2>nul
    
    for /d %%D in ("C:\Windows\Temp\*") do (
        rd /s /q "%%D" 2>nul
    )
    
    echo    Windows Temp cleaned
) else (
    echo    Skipping (requires administrator privileges)
    echo    Run as administrator to clean this location
)

:: ================================================
:: 3. Clean Prefetch (if admin)
:: ================================================
echo [3/3] Cleaning Prefetch folder...

net session >nul 2>&1
if %errorlevel% == 0 (
    del /f /q "C:\Windows\Prefetch\*" 2>nul
    echo    Prefetch cleaned
) else (
    echo    Skipping (requires administrator privileges)
)

:: ================================================
:: Optional: Browser Caches
:: ================================================
echo.
set /p browser="Clean browser caches? (Y/N): "
if /i "%browser%"=="Y" (
    echo Cleaning browser caches...
    
    :: Chrome
    if exist "%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache" (
        rd /s /q "%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache" 2>nul
        echo    Chrome cache cleaned
    )
    
    :: Edge
    if exist "%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache" (
        rd /s /q "%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache" 2>nul
        echo    Edge cache cleaned
    )
    
    :: Firefox
    if exist "%LOCALAPPDATA%\Mozilla\Firefox\Profiles" (
        for /d %%D in ("%LOCALAPPDATA%\Mozilla\Firefox\Profiles\*") do (
            if exist "%%D\cache2" (
                rd /s /q "%%D\cache2" 2>nul
            )
        )
        echo    Firefox cache cleaned
    )
)

:: ================================================
:: Summary
:: ================================================
echo.
echo ================================================
echo   Cleanup Complete!
echo ================================================
echo.
echo NOTE: Some files may not have been deleted because:
echo  - They are currently in use by running programs
echo  - They require administrator privileges
echo  - They are protected system files
echo.
echo TIP: For best results:
echo  - Close all browsers and programs
echo  - Run this script as Administrator
echo.

pause
