@echo off
setlocal

:: Define input/output folders
set "input_folder=%cd%\input"
set "output_folder=%cd%\output"

:: Make sure folders exist
if not exist "%input_folder%" mkdir "%input_folder%"
if not exist "%output_folder%" mkdir "%output_folder%"

echo ========================================
echo Batch Compress 4K -> 1080p (NVENC) with FFmpeg
echo ========================================

:: Process MP4 and MKV
for %%F in ("%input_folder%\*.mp4" "%input_folder%\*.mkv") do (
    if exist "%%~F" (
        echo Processing: %%~nxF
        ffmpeg -y -hwaccel cuda -i "%%~F" ^
            -vf "scale=1920:1080:flags=lanczos" ^
            -c:v h264_nvenc -preset p7 -rc:v vbr -cq 23 -b:v 8M -maxrate 12M -bufsize 24M ^
            -c:a copy ^
            "%output_folder%\%%~nF_1080p.mp4"
    )
)

echo ========================================
echo All files processed. Check the "output" folder.
echo ========================================
pause
