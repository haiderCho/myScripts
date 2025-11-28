@echo off
setlocal enabledelayedexpansion

:: ================================================
:: Universal Video Compressor (FFmpeg)
:: Consolidates 1080p/4K/H265 compression scripts
:: Author: haiderCho
:: ================================================

:: Check for FFmpeg
where ffmpeg >nul 2>&1
if errorlevel 1 (
    echo [ERROR] FFmpeg not found! Please install it or add to PATH.
    pause
    exit /b 1
)

:: Output folder
set "OUT_DIR=compressed"
if not exist "%OUT_DIR%" mkdir "%OUT_DIR%"

:: 1. Determine Input (Drag & Drop or Interactive)
set "targets="
if "%~1"=="" (
    echo No files dropped. Scanning current directory for video files...
    for %%F in (*.mp4 *.mkv *.mov *.avi *.flv *.wmv) do (
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

:: 2. Configuration Menu (if not hardcoded preference)
echo.
echo ================================================
echo   Video Compression Settings
echo ================================================
echo.

:: Hardware Acceleration Detection
set "hw_accel=none"
ffmpeg -hwaccels 2>nul | findstr /i "cuda" >nul && set "hw_accel=cuda"
if "!hw_accel!"=="none" ffmpeg -hwaccels 2>nul | findstr /i "qsv" >nul && set "hw_accel=qsv"
if "!hw_accel!"=="none" ffmpeg -hwaccels 2>nul | findstr /i "amf" >nul && set "hw_accel=amf"

echo Detected Hardware Acceleration: !hw_accel!
echo.

echo Choose Target Resolution:
echo 1. 1080p (Full HD) - Default
echo 2. 720p (HD)
echo 3. Original (No resizing)
set /p "res_choice=Select (1-3): "
set "scale_filter=scale='if(gt(a,16/9),1920,-2)':'if(gt(a,16/9),-2,1080)'"
if "!res_choice!"=="2" set "scale_filter=scale='if(gt(a,16/9),1280,-2)':'if(gt(a,16/9),-2,720)'"
if "!res_choice!"=="3" set "scale_filter="

echo.
echo Choose Codec:
echo 1. H.265 (HEVC) - High Efficiency (Smaller size, slower) - Default
echo 2. H.264 (AVC) - High Compatibility (Larger size, faster)
set /p "codec_choice=Select (1-2): "

:: Set Encoder and Bitrate based on HW Accel and Codec
set "vcodec=libx265"
set "preset=medium"
set "bitrate=4M"

if "!codec_choice!"=="2" (
    :: H.264
    if "!hw_accel!"=="cuda" ( set "vcodec=h264_nvenc" & set "preset=p4" )
    if "!hw_accel!"=="qsv"  ( set "vcodec=h264_qsv" & set "preset=medium" )
    if "!hw_accel!"=="amf"  ( set "vcodec=h264_amf" & set "preset=balanced" )
    if "!hw_accel!"=="none" ( set "vcodec=libx264" & set "preset=medium" )
    set "bitrate=5M"
) else (
    :: H.265 (Default)
    if "!hw_accel!"=="cuda" ( set "vcodec=hevc_nvenc" & set "preset=p4" )
    if "!hw_accel!"=="qsv"  ( set "vcodec=hevc_qsv" & set "preset=medium" )
    if "!hw_accel!"=="amf"  ( set "vcodec=hevc_amf" & set "preset=balanced" )
    if "!hw_accel!"=="none" ( set "vcodec=libx265" & set "preset=medium" )
    set "bitrate=3M"
)

echo.
echo Settings: Res=!res_choice!, Codec=!vcodec!, HW=!hw_accel!
echo.

:: 3. Processing Loop
for %%T in (!targets!) do (
    set "file_path=%%~fT"
    set "file_name=%%~nT"
    set "file_ext=%%~xT"
    set "out_file=%OUT_DIR%\!file_name!_comp.mp4"
    
    echo Processing: "!file_name!!file_ext!"
    
    :: Construct FFmpeg command
    set "cmd_ffmpeg=ffmpeg -y -i "!file_path!""
    if "!hw_accel!"=="cuda" set "cmd_ffmpeg=!cmd_ffmpeg! -hwaccel cuda"
    if "!hw_accel!"=="qsv"  set "cmd_ffmpeg=!cmd_ffmpeg! -hwaccel qsv"
    
    if defined scale_filter set "cmd_ffmpeg=!cmd_ffmpeg! -vf "!scale_filter!""
    
    set "cmd_ffmpeg=!cmd_ffmpeg! -c:v !vcodec! -preset !preset! -b:v !bitrate! -c:a aac -b:a 128k "!out_file!""
    
    :: Execute
    !cmd_ffmpeg! >nul 2>&1
    
    if errorlevel 1 (
        echo   [FAILED] Encoding failed.
        if exist "!out_file!" del "!out_file!"
    ) else (
        :: Size Comparison
        for %%I in ("!file_path!") do set "orig_size=%%~zI"
        for %%J in ("!out_file!") do set "new_size=%%~zJ"
        
        if !new_size! gtr !orig_size! (
            echo   [WARN] Compressed file is larger. Discarding.
            del "!out_file!"
        ) else (
            set /a saved=!orig_size!-!new_size!
            set /a percent=!saved!*100/!orig_size!
            echo   [OK] Saved !percent!%% size.
        )
    )
    echo.
)

echo Done.
pause
