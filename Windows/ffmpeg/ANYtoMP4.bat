@echo off
setlocal enabledelayedexpansion
for %%A in (*.mkv *.avi *.mov *.flv *.wmv) do (
    ffmpeg -i "%%A" -c:v libx264 -c:a aac -strict experimental "%%~nA.mp4"
)
pause
