@echo off
setlocal enabledelayedexpansion

:: ================================================
:: Zip All Folders using 7-Zip
:: Auto-detects 7-Zip installation
:: Author: haiderCho
:: ================================================

echo.
echo ================================================
echo   Zip All Folders Script
echo ================================================
echo.

:: Try to find 7-Zip in common locations
set "zip_exe="

:: Check common installation paths
if exist "C:\Program Files\7-Zip\7z.exe" (
    set "zip_exe=C:\Program Files\7-Zip\7z.exe"
)

if exist "C:\Program Files (x86)\7-Zip\7z.exe" (
    set "zip_exe=C:\Program Files (x86)\7-Zip\7z.exe"
)

:: Check PATH
if not defined zip_exe (
    where 7z.exe >nul 2>&1
    if not errorlevel 1 (
        set "zip_exe=7z.exe"
    )
)

:: If not found, error out
if not defined zip_exe (
    echo ERROR: 7-Zip not found!
    echo.
    echo Please install 7-Zip from: https://www.7-zip.org/
    echo Or ensure 7z.exe is in your PATH
    echo.
    pause
    exit /b 1
)

echo Using 7-Zip: !zip_exe!
echo.

:: Get compression level
set "compression_level=5"
set /p comp_input="Compression level (0-9, default 5): "

if "!comp_input!" neq "" (
    if !comp_input! geq 0 if !comp_input! leq 9 (
        set "compression_level=!comp_input!"
    )
)

echo Using compression level: !compression_level!
echo.

:: Count folders
set "folder_count=0"
for /d %%X in (*) do set /a folder_count+=1

if !folder_count! equ 0 (
    echo No folders found in current directory
    pause
    exit /b 0
)

echo Found !folder_count! folder(s) to compress
echo.

:: Compress folders
set "success_count=0"
set "error_count=0"

for /d %%X in (*) do (
    echo Compressing: %%X
    
    "!zip_exe!" a "%%~X.zip" "%%~X\" -tzip -mx=!compression_level!
    
    if errorlevel 1 (
        echo   [FAILED] Error compressing %%X
        set /a error_count+=1
    ) else (
        :: Verify archive
        "!zip_exe!" t "%%~X.zip" >nul 2>&1
        if errorlevel 1 (
            echo   [FAILED] Archive verification failed for %%X
            del "%%~X.zip" 2>nul
            set /a error_count+=1
        ) else (
            echo   [OK] Created %%~X.zip
            set /a success_count+=1
        )
    )
    echo.
)

:: Summary
echo ================================================
echo   Compression Summary
echo ================================================
echo   Total folders: !folder_count!
echo   Successful:    !success_count!
echo   Failed:        !error_count!
echo ================================================
echo.

:: Optional: Delete originals
if !success_count! gtr 0 (
    set /p delete_orig="Delete successfully compressed folders? (y/N): "
    if /i "!delete_orig!"=="y" (
        echo.
        echo Deleting original folders...
        for /d %%X in (*) do (
            if exist "%%~X.zip" (
                "!zip_exe!" t "%%~X.zip" >nul 2>&1
                if not errorlevel 1 (
                    rd /s /q "%%X"
                    echo   Deleted: %%X
                )
            )
        )
    )
)

echo.
echo All operations complete
pause
