@echo off
setlocal enabledelayedexpansion

:: ================================================
:: Video Compression to 1080p with Smart Encoding
:: Supports both NVIDIA NVENC and CPU fallback
:: Author: haiderCho
:: ================================================

:: Set output folder
set "output_dir=compressed"

:: Create output directory if not exists
if not exist "%output_dir%" mkdir "%output_dir%"

echo.
echo ================================================
echo   Video Compression to 1080p
echo ================================================
echo.

:: Test CUDA availability
echo Testing for NVIDIA GPU acceleration...
ffmpeg -hwaccels 2>nul | findstr /i "cuda" >nul
if errorlevel 1 (
    set "use_cuda=0"
    echo   No CUDA support detected - using CPU encoding
) else (
    set "use_cuda=1"
    echo   CUDA detected - will attempt GPU acceleration
)
echo.

for %%F in (*.mp4 *.mov *.mkv *.avi *.flv *.wmv) do (
    echo Processing: %%F

    :: Get video resolution and codec
    for /f "tokens=1,2 delims=x" %%A in ('ffprobe -v error -select_streams v:0 -show_entries stream^=width^,height -of csv^=p^=0:s^=x "%%F" 2^>nul') do (
        set "width=%%A"
        set "height=%%B"
    )
    
    :: Check if probe succeeded
    if not defined width (
        echo   ERROR: Could not read video properties
        echo.
        goto :continue
    )

    :: Check if already 1080p or lower
    if !width! leq 1920 if !height! leq 1080 (
        echo   Skipping: Already 1080p or lower (!width!x!height!)
        echo.
        goto :continue
    )

    echo   Original resolution: !width!x!height!

    :: Set output file path
    set "output_file=%output_dir%\%%~nF_1080p.mp4"

    :: Try GPU encoding first if available
    if !use_cuda! equ 1 (
        echo   Attempting NVENC GPU encoding...
        
        ffmpeg -hwaccel cuda -i "%%F" ^
            -vf "scale='if(gt(a,16/9),1920,-2)':'if(gt(a,16/9),-2,1080)'" ^
            -c:v h264_nvenc -preset slow -b:v 5M ^
            -c:a copy "!output_file!" -y 2>nul
        
        if errorlevel 1 (
            echo   NVENC failed, falling back to CPU...
            goto :cpu_encode
        ) else (
            echo   NVENC encoding successful
            goto :check_size
        )
    )

    :cpu_encode
    echo   Using CPU encoding...
    
    :: Ask user for encoding mode
    if not defined encoding_mode (
        echo.
        echo   Choose encoding mode:
        echo   1. CRF (Constant Rate Factor) - Better quality, variable size
        echo   2. Bitrate - Predictable size, variable quality
        echo.
        set /p mode_choice="   Select mode (1/2, default 1): "
        
        if "!mode_choice!"=="2" (
            set "encoding_mode=bitrate"
        ) else (
            set "encoding_mode=crf"
        )
    )
    
    if "!encoding_mode!"=="crf" (
        :: CRF mode (better quality)
        ffmpeg -i "%%F" ^
            -vf "scale='if(gt(a,16/9),1920,-2)':'if(gt(a,16/9),-2,1080)'" ^
            -c:v libx264 -preset medium -crf 23 ^
            -c:a copy "!output_file!" -y
    ) else (
        :: Bitrate mode
        ffmpeg -i "%%F" ^
            -vf "scale='if(gt(a,16/9),1920,-2)':'if(gt(a,16/9),-2,1080)'" ^
            -c:v libx264 -preset medium -b:v 5M ^
            -c:a copy "!output_file!" -y
    )
    
    if errorlevel 1 (
        echo   ERROR: Encoding failed
        echo.
        goto :continue
    )

    :check_size
    :: Compare file sizes
    for %%I in ("%%F") do set "orig_size=%%~zI"
    for %%J in ("!output_file!") do set "new_size=%%~zJ"

    if !new_size! gtr !orig_size! (
        echo   Compressed file is larger than original
        echo   Deleting output and keeping original
        del "!output_file!"
    ) else (
        set /a saved=!orig_size!-!new_size!
        set /a saved_mb=!saved!/1048576
        set /a percent=!saved!*100/!orig_size!
        echo   Compression successful! Saved !saved_mb! MB (!percent!%%)
    )

    echo.

    :continue
)

echo ================================================
echo   All processing complete
echo ================================================
pause
