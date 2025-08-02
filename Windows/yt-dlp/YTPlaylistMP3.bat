@echo off
set /p url="Enter Playlist URL: "
yt-dlp -x --audio-format mp3 --embed-thumbnail --add-metadata "%url%"
pause
