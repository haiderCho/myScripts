@echo off
setlocal

:: Create "converted" folder if it doesn't exist
if not exist "converted" (
    mkdir "converted"
)

:: Loop through all .mp4 files in the current directory
for %%f in (*.mp4) do (
    echo Processing: %%f
    ffmpeg -i "%%f" -vf "scale='if(gt(a,1),-2,1080)':'if(gt(a,1),1080,-2)'" -c:v hevc_nvenc -preset p4 -b:v 4M -c:a aac -b:a 128k "converted\_%%~nf_1080p.mp4"
)

pause
