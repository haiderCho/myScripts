@echo off
setlocal enabledelayedexpansion

for %%f in (*.ts) do (
    echo Processing "%%f"...
    ffmpeg -y -err_detect ignore_err -i "%%f" -c copy "%%~nf_clean.ts"
    
    if exist "%%~nf_clean.ts" (
        del "%%f"
        ren "%%~nf_clean.ts" "%%~nxf"
    )
)

echo Done.
pause
