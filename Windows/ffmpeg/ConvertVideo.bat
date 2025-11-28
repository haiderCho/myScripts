@echo off
setlocal enabledelayedexpansion

:: ================================================
:: Universal Video Converter (FFmpeg)
:: Consolidates format conversion scripts
:: Author: haiderCho
:: ================================================

:: Check for FFmpeg
where ffmpeg >nul 2>&1
if errorlevel 1 (
    echo [ERROR] FFmpeg not found!
    pause
    exit /b 1
)

:: 1. Determine Input
set "targets="
if "%~1"=="" (
    echo No files dropped. Scanning current directory for video files...
    for %%F in (*.mkv *.avi *.mov *.flv *.wmv *.ts) do (
        set "targets=!targets! "%%~fF""
    )
) else (
    :args_loop
    if "%~1"=="" goto :args_done
    if exist "%~1" set "targets=!targets! "%~1""
    shift
    goto :args_loop
    :args_done
)

if "!targets!"=="" (
    echo No video files found.
    pause
    exit /b 0
)

:: 2. Menu
echo.
echo Choose Output Format:
echo 1. MP4 (Default)
echo 2. MKV
echo 3. AVI
set /p "fmt_choice=Select (1-3): "
set "out_ext=.mp4"
if "!fmt_choice!"=="2" set "out_ext=.mkv"
if "!fmt_choice!"=="3" set "out_ext=.avi"

echo.
echo Choose Mode:
echo 1. Re-encode (H.264 + AAC) - Slower, compatible
echo 2. Stream Copy (Remux) - Fast, keeps quality (might fail if incompatible)
set /p "mode_choice=Select (1-2): "

:: 3. Processing
for %%T in (!targets!) do (
    set "file_path=%%~fT"
    set "file_name=%%~nT"
    set "out_file=%%~dpT!file_name!!out_ext!"
    
    echo Converting: "%%~nxT" to "!out_ext!"
    
    if "!mode_choice!"=="2" (
        :: Stream Copy
        ffmpeg -y -i "!file_path!" -c copy -map 0 "!out_file!"
    ) else (
        :: Re-encode
        ffmpeg -y -i "!file_path!" -c:v libx264 -preset fast -crf 23 -c:a aac -b:a 128k "!out_file!"
    )
    
    if errorlevel 1 (
        echo   [FAILED] Conversion failed.
    ) else (
        echo   [OK] Success.
    )
    echo.
)

echo Done.
pause
