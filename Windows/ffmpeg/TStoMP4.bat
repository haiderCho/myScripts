@echo off
setlocal enabledelayedexpansion

for %%f in (*.ts) do (
    set "input=%%f"
    set "base=%%~nf"
    set "temp=!base!_temp.mp4"
    set "final=!base!.mp4"

    echo Processing "!input!"...

    ffmpeg -y -err_detect ignore_err -i "!input!" ^
        -c:v hevc_nvenc -b:v 1424k -maxrate 1500k -bufsize 3000k -preset slow ^
        -c:a aac -b:a 128k "!temp!"

    if exist "!temp!" (
        del "!input!"
        ren "!temp!" "!final!"
    )
)

echo Done.
pause
