@echo off
setlocal enabledelayedexpansion

:: ================================================
:: YT-DLP Wrapper
:: Supports Audio/Video selection and Quality
:: Author: haiderCho
:: ================================================

set /p "url=Enter URL (Video or Playlist): "
if "%url%"=="" goto :eof

echo.
echo Choose Format:
echo 1. Audio (MP3) - Default
echo 2. Video (MP4/MKV)
set /p "fmt=Select (1-2): "

if "%fmt%"=="2" (
    echo.
    echo Choose Video Quality:
    echo 1. Best Available (Default)
    echo 2. 1080p
    echo 3. 720p
    set /p "qual=Select (1-3): "
    
    set "args="
    if "!qual!"=="2" set "args=-f "bestvideo[height<=1080]+bestaudio/best[height<=1080]""
    if "!qual!"=="3" set "args=-f "bestvideo[height<=720]+bestaudio/best[height<=720]""
    
    echo Downloading Video...
    yt-dlp !args! --embed-thumbnail --add-metadata --merge-output-format mp4 "%url%"
) else (
    echo Downloading Audio (MP3)...
    yt-dlp -x --audio-format mp3 --embed-thumbnail --add-metadata "%url%"
)

echo Done.
pause
