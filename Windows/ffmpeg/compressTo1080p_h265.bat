@echo off
setlocal enabledelayedexpansion

:: Set output folder
set "output_dir=compressed"

:: Create output directory if not exists
if not exist "%output_dir%" mkdir "%output_dir%"

for %%F in (*.mp4 *.mov *.mkv *.avi) do (
    echo Processing: %%F

    :: Get resolution using ffprobe
    for /f "tokens=1,2 delims=x" %%A in ('ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0:s=x "%%F"') do (
        set "width=%%A"
        set "height=%%B"
    )

    :: Check if video is already 1080p or lower
    if !width! lss 1920 if !height! lss 1080 (
        echo Skipping %%F (already 1080p or lower)
        echo.
        goto :continue
    )

    :: Set output file path
    set "output_file=%output_dir%\%%~nF_compressed.mp4"

    :: Compress using HEVC (H.265) with NVENC, auto-scale to 1080p max, keep orientation
    ffmpeg -hwaccel cuda -i "%%F" -vf "scale='if(gt(a,16/9),1920,-2)':'if(gt(a,16/9),-2,1080)'" ^
        -c:v hevc_nvenc -preset slow -b:v 4M -c:a copy -movflags +faststart "!output_file!" -y

    :: Get original and compressed sizes
    for %%I in ("%%F") do set "orig_size=%%~zI"
    for %%J in ("!output_file!") do set "new_size=%%~zJ"

    if !new_size! gtr !orig_size! (
        echo Compressed file is larger. Deleting "!output_file!" and skipping.
        del "!output_file!"
    ) else (
        echo Compression successful for %%F
    )

    echo.

    :continue
)

echo All done.
pause
