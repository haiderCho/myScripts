@echo off
setlocal enabledelayedexpansion

:: ================================================
:: Zip All Folders (Enhanced)
:: Auto-detects 7-Zip, supports Drag & Drop
:: Author: haiderCho
:: ================================================

echo.
echo ================================================
echo   Zip All Folders Script
echo ================================================
echo.

:: 1. Setup Logging
set "LOGFILE=%~dp0zip_log.txt"
echo [%DATE% %TIME%] Script started > "%LOGFILE%"

:: 2. Find 7-Zip
set "zip_exe="
if exist "C:\Program Files\7-Zip\7z.exe" set "zip_exe=C:\Program Files\7-Zip\7z.exe"
if not defined zip_exe if exist "C:\Program Files (x86)\7-Zip\7z.exe" set "zip_exe=C:\Program Files (x86)\7-Zip\7z.exe"
if not defined zip_exe (
    where 7z.exe >nul 2>&1
    if not errorlevel 1 set "zip_exe=7z.exe"
)

if not defined zip_exe (
    echo [ERROR] 7-Zip not found!
    echo [ERROR] 7-Zip not found! >> "%LOGFILE%"
    pause
    exit /b 1
)
echo Using 7-Zip: "!zip_exe!"
echo Using 7-Zip: "!zip_exe!" >> "%LOGFILE%"

:: 3. Determine Targets (Current Dir or Dragged Items)
set "targets="
if "%~1"=="" (
    :: No arguments, process all folders in current directory
    echo Mode: Current Directory Scan
    for /d %%D in (*) do (
        set "targets=!targets! "%%~fD""
    )
) else (
    :: Arguments provided (Drag & Drop)
    echo Mode: Drag & Drop
    :args_loop
    if "%~1"=="" goto :args_done
    if exist "%~1" (
        if exist "%~1\" (
            :: It's a directory
            set "targets=!targets! "%~1""
        ) else (
            echo Skipping file: "%~nx1" (Only folders supported)
        )
    )
    shift
    goto :args_loop
    :args_done
)

if "!targets!"=="" (
    echo No folders to compress.
    pause
    exit /b 0
)

:: 4. Compression Loop
set "compression_level=5"
echo.
set /p "comp_input=Compression level (0-9, default 5): "
if not "!comp_input!"=="" set "compression_level=!comp_input!"
echo Using compression level: !compression_level! >> "%LOGFILE%"

for %%T in (!targets!) do (
    set "folder_path=%%~fT"
    set "folder_name=%%~nT"
    set "parent_dir=%%~dpT"
    
    echo.
    echo Compressing: "!folder_name!"
    echo [%DATE% %TIME%] Compressing: "!folder_path!" >> "%LOGFILE%"
    
    pushd "!parent_dir!"
    "!zip_exe!" a "!folder_name!.zip" "!folder_name!\" -tzip -mx=!compression_level! >> "%LOGFILE%" 2>&1
    
    if errorlevel 1 (
        echo   [FAILED] Error compressing "!folder_name!"
        echo   [FAILED] Error compressing "!folder_name!" >> "%LOGFILE%"
    ) else (
        echo   [OK] Created "!folder_name!.zip"
        echo   [OK] Created "!folder_name!.zip" >> "%LOGFILE%"
    )
    popd
)

echo.
echo ================================================
echo   Operation Complete
echo ================================================
echo Log saved to: "%LOGFILE%"
pause
