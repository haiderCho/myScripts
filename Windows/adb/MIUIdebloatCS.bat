@echo off
setlocal EnableDelayedExpansion
title MIUI Debloat Manager v2.1 (SAFE MODE)

:: Set working directory to script location
cd /d "%~dp0"

:: Add current directory to PATH (so it finds adb.exe if bundled)
set "PATH=%PATH%;%~dp0"

:: Configuration
set "BACKUP_FILE=removed_packages.log"
set "LOG_FILE=debloat_manager.log"

:: Simple safe date/time (robust against locales)
set "LOG_DATE=%DATE% %TIME%"

:: Initial Setup
color 0B
cls
set "TARGET_USER=0"

:CHECK_ADB
cls
echo ===================================================
echo        MIUI DEBLOAT MANAGER v2.3 (SAFE)
echo ===================================================
echo [!] Checking ADB connection...
echo.

:: Initialize ADB_CMD
set "ADB_CMD="

:: 1. Check SYSTEM PATH
where adb >nul 2>&1
if %errorlevel% equ 0 (
    for /f "usebackq tokens=*" %%i in (`where adb`) do (
        set "ADB_CMD=%%i"
        echo [INFO] Found 'adb' in PATH: %%i
        goto VERIFY_ADB
    )
)

:: 2. Check current directory
if exist "%~dp0adb.exe" (
    echo [INFO] Found 'adb' in script folder.
    set "ADB_CMD=%~dp0adb.exe"
    goto VERIFY_ADB
)

:: 3. Check Chocolatey (Standard & custom install paths)
if exist "%ProgramData%\chocolatey\bin\adb.exe" (
    echo [INFO] Found 'adb' in Chocolatey bin.
    set "ADB_CMD=%ProgramData%\chocolatey\bin\adb.exe"
    goto VERIFY_ADB
)
if exist "%ProgramData%\chocolatey\lib\adb\tools\adb.exe" (
    echo [INFO] Found 'adb' in Chocolatey tools.
    set "ADB_CMD=%ProgramData%\chocolatey\lib\adb\tools\adb.exe"
    goto VERIFY_ADB
)

:: 4. Check Android SDK (Local AppData)
if exist "%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe" (
    echo [INFO] Found 'adb' in Android SDK.
    set "ADB_CMD=%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe"
    goto VERIFY_ADB
)

:: 5. Check Common Program Files
if exist "%ProgramFiles(x86)%\Android\android-sdk\platform-tools\adb.exe" (
    set "ADB_CMD=%ProgramFiles(x86)%\Android\android-sdk\platform-tools\adb.exe"
    goto VERIFY_ADB
)

:: If we reached here, ADB is missing
echo [ERROR] 'adb.exe' not found in PATH or common locations!
echo.
echo Locations checked:
echo  - System PATH
echo  - %~dp0
echo  - %ProgramData%\chocolatey
echo  - %LOCALAPPDATA%\Android\Sdk
echo.
echo Please install ADB using Chocolatey: choco install adb
echo OR download Platform Tools and place adb.exe here.
echo.
pause
exit /b

:VERIFY_ADB
:: Verify the found command works
echo [DEBUG] Verifying ADB binary...
call "%ADB_CMD%" version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Found ADB at "%ADB_CMD%" but it failed to run.
    pause
    exit /b
)

echo [DEBUG] Starting ADB server...
call "%ADB_CMD%" start-server >nul 2>&1
call "%ADB_CMD%" devices > devices.tmp
findstr /C:"device" devices.tmp | findstr /V "List" >nul
if %errorlevel% neq 0 (
    echo [ERROR] No device detected or unauthorized!
    echo.
    echo 1. Check if USB Debugging is ON in Developer Options.
    echo 2. Check if cable is connected properly.
    echo 3. Check ADB authorization popup on phone.
    echo.
    if exist devices.tmp del devices.tmp
    pause
    goto CHECK_ADB
)
if exist devices.tmp del devices.tmp

:: Get Device Info
set "BRAND="
set "MODEL="
set "MIUI_VER="

:: Get Device Info
set "BRAND="
set "MODEL="
set "MIUI_VER="
set "BRAND_TMP=brand.tmp"

echo [DEBUG] Fetching device properties...
call "%ADB_CMD%" shell getprop ro.product.brand > "%BRAND_TMP%"
set /p BRAND=<"%BRAND_TMP%"
if exist "%BRAND_TMP%" del "%BRAND_TMP%"

call "%ADB_CMD%" shell getprop ro.product.model > "%BRAND_TMP%"
set /p MODEL=<"%BRAND_TMP%"
if exist "%BRAND_TMP%" del "%BRAND_TMP%"

call "%ADB_CMD%" shell getprop ro.miui.ui.version.name > "%BRAND_TMP%"
set /p MIUI_VER=<"%BRAND_TMP%"
if exist "%BRAND_TMP%" del "%BRAND_TMP%"

:: Safety Check - Xiaomi Device Only (Logic Fix)
if "%BRAND%"=="" (
    echo [WARNING] Could not detect device brand.
    set "BRAND=Unknown"
)

echo "%BRAND%" | findstr /I "Xiaomi POCO Redmi" >nul
if %errorlevel% neq 0 (
    echo [WARNING] This device - %BRAND% %MODEL% - does not appear to be a Xiaomi device.
    echo This tool is designed for MIUI/HyperOS only.
    echo.
    set /p "CONFIRM=Type 'YES' to continue anyway (Risk of damage): "
    if /I not "!CONFIRM!"=="YES" exit
)

:MENU
cls
echo ===================================================
echo        MIUI DEBLOAT MANAGER v2.3 (SAFE)
echo ===================================================
echo Device     : %BRAND% %MODEL%
echo MIUI Ver   : %MIUI_VER%
echo Target User: %TARGET_USER%
echo Status     : CONNECTED
echo Log File   : %LOG_FILE%
echo ===================================================
echo.
echo [1] SAFE DEBLOAT (Analytics, Ads, MSA, etc.)
echo [2] REMOVE TRACKING (Google/Xiaomi Telemetry)
echo [3] REMOVE JUNK APPS (FmRadio, Compass, etc.)
echo [4] RESTORE REMOVED PACKAGES
echo [5] EXPORT INSTALLED APPS LIST
echo [C] CHANGE TARGET USER (Second Space)
echo [E] EXIT
echo.
set /p "choice=Select Option: "

if /I "%choice%"=="1" goto SAFE_LIST
if /I "%choice%"=="2" goto TRACKING_LIST
if /I "%choice%"=="3" goto JUNK_LIST
if /I "%choice%"=="4" goto RESTORE
if /I "%choice%"=="5" goto EXPORT
if /I "%choice%"=="C" goto CHANGE_USER
if /I "%choice%"=="E" exit
goto MENU

:: ===================================================
:: LOGIC FUNCTIONS
:: ===================================================

:REMOVE_PACKAGE
set "PKG=%~1"
set "DESC=%~2"

echo.
echo [-] Checking %PKG%...
call "%ADB_CMD%" shell pm list packages --user %TARGET_USER% | findstr "^package:%PKG%$" >nul
if !errorlevel! neq 0 (
    echo     [SKIP] Not installed or already removed.
    exit /b
)

echo     Found: !DESC!
echo     Uninstalling...
call "%ADB_CMD%" shell pm uninstall --user %TARGET_USER% %PKG% > "uninstall.log" 2>&1

findstr /C:"Success" "uninstall.log" >nul
if !errorlevel! equ 0 (
    echo     [SUCCESS] Uninstalled %PKG%
    echo [%LOG_DATE%] REMOVED: %PKG% (!DESC!) >> "%BACKUP_FILE%"
    echo [%LOG_DATE%] SUCCESS: %PKG% >> "%LOG_FILE%"
) else (
    echo     [FAIL] Could not uninstall %PKG%
    type "uninstall.log"
    echo [%LOG_DATE%] FAIL: %PKG% >> "%LOG_FILE%"
)
if exist "uninstall.log" del "uninstall.log"
exit /b

:: ===================================================
:: LISTS
:: ===================================================

:SAFE_LIST
cls
echo ===================================================
echo               SAFE DEBLOAT
echo ===================================================
echo Removing Analytics, Ads, and useless daemons...
echo.

call :REMOVE_PACKAGE com.miui.analytics "MIUI Analytics"
call :REMOVE_PACKAGE com.miui.msa.global "MIUI MSA - Ads"
call :REMOVE_PACKAGE com.xiaomi.discover "Xiaomi Discover"
call :REMOVE_PACKAGE com.mi.appfinder "App Finder"
call :REMOVE_PACKAGE com.mi.globalminusscreen "App Vault"
call :REMOVE_PACKAGE com.miui.miservice "Services and Feedback"
call :REMOVE_PACKAGE com.miui.android.fashiongallery "Wallpaper Carousel"
call :REMOVE_PACKAGE com.miui.yellowpage "Yellow Pages"
call :REMOVE_PACKAGE com.miui.phrase "Frequent Phrases"
call :REMOVE_PACKAGE com.miui.thirdappassistant "Third App Assistant"
call :REMOVE_PACKAGE com.google.android.printservice.recommendation "Print Recommendations"
call :REMOVE_PACKAGE com.facebook.services "Facebook Services"
call :REMOVE_PACKAGE com.facebook.system "Facebook System"
call :REMOVE_PACKAGE com.facebook.appmanager "Facebook App Manager"
call :REMOVE_PACKAGE com.netflix.partner.activation "Netflix Activation"

echo.
echo [DONE] Safe debloat complete.
pause
goto MENU

:TRACKING_LIST
cls
echo ===================================================
echo            TRACKING AND TELEMETRY
echo ===================================================
echo Removing Google/Xiaomi diagnostic tools...
echo.

call :REMOVE_PACKAGE com.google.android.adservices.api "Google Ad Services"
call :REMOVE_PACKAGE com.google.android.feedback "Google Feedback"
call :REMOVE_PACKAGE com.miui.bugreport "MIUI Bug Report"
call :REMOVE_PACKAGE com.miui.misightservice "Mi Sight Service"
call :REMOVE_PACKAGE com.miui.daemon "MIUI Daemon"
call :REMOVE_PACKAGE com.qualcomm.qti.optinoverlay "Qualcomm Opt-In"

echo.
echo [DONE] Tracking removal complete.
pause
goto MENU

:JUNK_LIST
cls
echo ===================================================
echo               REMOVE JUNK APPS
echo ===================================================
echo Removing default apps often considered bloat...
echo.

:: call :REMOVE_PACKAGE com.miui.compass "Compass"
:: call :REMOVE_PACKAGE com.miui.scanner "Scanner"
:: call :REMOVE_PACKAGE com.miui.screenrecorder "Screen Recorder"
call :REMOVE_PACKAGE com.miui.fm "FM Radio"
:: call :REMOVE_PACKAGE com.miui.notes "Notes"
call :REMOVE_PACKAGE com.miui.videoplayer "Mi Video"
call :REMOVE_PACKAGE com.miui.player "Mi Music"
call :REMOVE_PACKAGE com.android.browser "Mi Browser"
call :REMOVE_PACKAGE com.miui.browser "Mi Browser Global"
call :REMOVE_PACKAGE com.mi.globalbrowser "Mi Browser (Standard)"
call :REMOVE_PACKAGE com.xiaomi.payment "Mi Coin / Payment"
call :REMOVE_PACKAGE com.google.android.youtube "YouTube"
call :REMOVE_PACKAGE com.google.android.apps.youtube.music "YouTube Music"

echo.
echo [DONE] Junk removal complete.
pause
goto MENU

:RESTORE
cls
echo ===================================================
echo              RESTORE PACKAGES
echo ===================================================
if not exist "%BACKUP_FILE%" (
    echo [ERROR] No backup log found (%BACKUP_FILE%).
    pause
    goto MENU
)

echo Reading from %BACKUP_FILE%...
echo.

for /f "tokens=4" %%a in ('findstr "REMOVED:" "%BACKUP_FILE%"') do (
    echo Restoring %%a...
    call "%ADB_CMD%" shell cmd package install-existing %%a
)

echo.
echo [DONE] Restore process finished.
pause
goto MENU

:EXPORT
cls
echo Exporting installed packages to installed_apps.txt...
call "%ADB_CMD%" shell pm list packages --user %TARGET_USER% > installed_apps.txt
echo [DONE] Saved to installed_apps.txt
pause
goto MENU

:CHANGE_USER
cls
echo ===================================================
echo               CHANGE TARGET USER
echo ===================================================
echo Current Target: User %TARGET_USER%
echo.
echo Common User IDs:
echo   - 0   : Main User (Default)
echo   - 10  : Second Space / Work Profile
echo   - 11+ : Additional Users
echo.
echo [L] List available users (via ADB)
echo [B] Back to Menu
echo.

set /p "CU_CHOICE=Select Option or type user ID (e.g., 10): "

if /I "%CU_CHOICE%"=="B" goto MENU
if /I "%CU_CHOICE%"=="L" (
    echo.
    call "%ADB_CMD%" shell pm list users
    echo.
    pause
    goto CHANGE_USER
)

:: Simple validaton: Check if numeric
set "TARGET_USER=%CU_CHOICE%"
echo.
echo Target User set to: %TARGET_USER%
pause
goto MENU
