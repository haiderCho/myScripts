@echo off
setlocal enabledelayedexpansion

:: ================================================
:: Clean TS Files
:: Remuxes .ts files to fix errors/timestamps
:: Author: haiderCho
:: ================================================

for %%f in (*.ts) do (
    echo Processing "%%f"...
    ffmpeg -y -err_detect ignore_err -i "%%f" -c copy "%%~nf_clean.ts"
    
    if errorlevel 1 (
        echo   [FAILED] FFmpeg error.
    ) else (
        if exist "%%~nf_clean.ts" (
            del "%%f"
            ren "%%~nf_clean.ts" "%%~nxf"
            echo   [OK] Cleaned.
        )
    )
)

echo Done.
pause
