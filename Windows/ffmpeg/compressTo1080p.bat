@echo off
setlocal enabledelayedexpansion

:: Set output folder
set "output_dir=compressed"

:: Create output directory if not exists
if not exist "%output_dir%" mkdir "%output_dir%"

for %%F in (*.mp4 *.mov *.mkv *.avi) do (
    echo Processing: %%F

    :: Get video resolution
    for /f "tokens=1,2 delims=:" %%A in ('ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0:s=x "%%F"') do (
        set "width=%%A"
        set "height=%%B"
    )

    :: Check if width and height are both less than or equal to 1920x1080
    if !width! lss 1920 if !height! lss 1080 (
        echo Skipping %%F (already 1080p or lower)
        echo.
        goto :continue
    )

    :: Set output file path
    set "output_file=%output_dir%\%%~nF_compressed.mp4"

    :: Compress to 1080p using NVENC and auto-scale
    ffmpeg -hwaccel cuda -i "%%F" -vf "scale='if(gt(a,16/9),1920,-2)':'if(gt(a,16/9),-2,1080)',transpose=0" -c:v h264_nvenc -preset slow -b:v 5M -c:a copy "!output_file!" -y

    :: Compare file sizes
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
