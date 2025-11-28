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
echo  1. User Temp folder (%%TEMP%%)
echo  2. Windows Temp folder (C:\Windows\Temp)
echo  3. Prefetch folder (C:\Windows\Prefetch)
echo  4. Recycle Bin (Optional)
echo  5. Windows Update Cache (Optional, Admin only)
echo  6. Browser caches (Optional)
echo.

:: Check for Admin rights
net session >nul 2>&1
if %errorlevel% == 0 (
    set "IS_ADMIN=1"
    echo [INFO] Running as Administrator.
) else (
    set "IS_ADMIN=0"
    echo [INFO] Running as User (Some system folders will be skipped).
)
echo.

:: Options
set "DRY_RUN=0"
set /p "dry_run_choice=Run in Dry-Run mode (simulate only)? (y/N): "
if /i "%dry_run_choice%"=="y" set "DRY_RUN=1"

set /p confirm="Do you want to continue? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo Operation cancelled.
    pause
    exit /b
)

echo.
echo Starting cleanup...
echo.

:: ================================================
:: 1. Clean User Temp Folder
:: ================================================
echo [1/5] Cleaning User Temp folder...
set "user_temp=%TEMP%"

if %DRY_RUN%==1 (
    echo   [DRY-RUN] Would delete contents of: "%user_temp%"
) else (
    del /s /f /q "%user_temp%\*" 2>nul
    for /d %%D in ("%user_temp%\*") do rd /s /q "%%D" 2>nul
    echo   Done.
)

:: ================================================
:: 2. Clean Windows Temp Folder (Admin)
:: ================================================
echo [2/5] Cleaning Windows Temp folder...
if %IS_ADMIN%==1 (
    if %DRY_RUN%==1 (
        echo   [DRY-RUN] Would delete contents of: "C:\Windows\Temp"
    ) else (
        del /s /f /q "C:\Windows\Temp\*" 2>nul
        for /d %%D in ("C:\Windows\Temp\*") do rd /s /q "%%D" 2>nul
        echo   Done.
    )
) else (
    echo   Skipping (Requires Admin).
)

:: ================================================
:: 3. Clean Prefetch (Admin)
:: ================================================
echo [3/5] Cleaning Prefetch folder...
if %IS_ADMIN%==1 (
    if %DRY_RUN%==1 (
        echo   [DRY-RUN] Would delete contents of: "C:\Windows\Prefetch"
    ) else (
        del /f /q "C:\Windows\Prefetch\*" 2>nul
        echo   Done.
    )
) else (
    echo   Skipping (Requires Admin).
)

:: ================================================
:: 4. Clean Recycle Bin
:: ================================================
echo.
set /p "clean_bin=Empty Recycle Bin? (y/N): "
if /i "%clean_bin%"=="y" (
    echo [4/5] Emptying Recycle Bin...
    if %DRY_RUN%==1 (
        echo   [DRY-RUN] Would empty Recycle Bin.
    ) else (
        rd /s /q %systemdrive%\$Recycle.Bin 2>nul
        echo   Done.
    )
) else (
    echo [4/5] Skipping Recycle Bin.
)

:: ================================================
:: 5. Clean Windows Update Cache (Admin)
:: ================================================
echo.
if %IS_ADMIN%==1 (
    set /p "clean_update=Clean Windows Update Cache (Fixes update issues)? (y/N): "
    if /i "!clean_update!"=="y" (
        echo [5/5] Cleaning Windows Update Cache...
        if %DRY_RUN%==1 (
            echo   [DRY-RUN] Would stop wuauserv, clean SoftwareDistribution, and restart wuauserv.
        ) else (
            net stop wuauserv
            del /f /s /q %windir%\SoftwareDistribution\*.*
            net start wuauserv
            echo   Done.
        )
    ) else (
        echo [5/5] Skipping Windows Update Cache.
    )
) else (
    echo [5/5] Skipping Windows Update Cache (Requires Admin).
)

:: ================================================
:: 6. Browser Caches
:: ================================================
echo.
set /p browser="Clean browser caches? (y/N): "
if /i "%browser%"=="y" (
    echo Cleaning browser caches...
    
    :: Chrome
    if exist "%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache" (
        if %DRY_RUN%==1 (
            echo   [DRY-RUN] Would clean Chrome cache.
        ) else (
            rd /s /q "%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache" 2>nul
            echo   Chrome cache cleaned.
        )
    )
    
    :: Edge
    if exist "%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache" (
        if %DRY_RUN%==1 (
            echo   [DRY-RUN] Would clean Edge cache.
        ) else (
            rd /s /q "%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache" 2>nul
            echo   Edge cache cleaned.
        )
    )
)

echo.
echo ================================================
echo   Cleanup Complete!
echo ================================================
pause
