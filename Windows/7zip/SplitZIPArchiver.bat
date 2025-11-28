@echo off
setlocal enabledelayedexpansion

:: ===============================
:: Split ZIP Archiver using 7-Zip
:: Supports Drag & Drop
:: Author: haiderCho
:: ===============================

:: Find 7-Zip
set "zip_exe="
if exist "C:\Program Files\7-Zip\7z.exe" set "zip_exe=C:\Program Files\7-Zip\7z.exe"
if not defined zip_exe if exist "C:\Program Files (x86)\7-Zip\7z.exe" set "zip_exe=C:\Program Files (x86)\7-Zip\7z.exe"
if not defined zip_exe (
    where 7z.exe >nul 2>&1
    if not errorlevel 1 set "zip_exe=7z.exe"
)
if not defined zip_exe (
    echo 7-Zip not found!
    pause
    exit /b 1
)

:: Check for Drag & Drop
set "source_path="
if not "%~1"=="" (
    set "source_path=%~f1"
)

:: If no drag & drop, prompt
if not defined source_path (
    set /p "source_path=Enter the full path of the file or folder to compress: "
)

:: Remove quotes if present
set "source_path=!source_path:"=!"

if not exist "!source_path!" (
    echo Error: Path not found: "!source_path!"
    pause
    exit /b 1
)

:: Get default name from source
for %%I in ("!source_path!") do set "default_name=%%~nI"

echo.
set /p "archive_name=Enter archive name (default: !default_name!): "
if "!archive_name!"=="" set "archive_name=!default_name!"

echo.
set /p "split_size=Enter split size (e.g., 100M, 700M, 1G): "
if "!split_size!"=="" (
    echo Error: Split size required.
    pause
    exit /b 1
)

echo.
set /p "output_path=Enter output folder path (default: current): "
if "!output_path!"=="" set "output_path=%~dp0"

:: Ensure output directory exists
if not exist "!output_path!" mkdir "!output_path!"

:: 7-Zip command
echo.
echo Archiving and splitting...
echo ------------------------------------
"!zip_exe!" a "!output_path!\!archive_name!.7z" "!source_path!" -v!split_size! -mx=9

if %errorlevel%==0 (
    echo.
    echo ✅ Successfully created split archive.
) else (
    echo.
    echo ❌ Error: Archiving failed.
)

pause
