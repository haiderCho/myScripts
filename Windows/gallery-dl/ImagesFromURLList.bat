@echo off
setlocal enabledelayedexpansion

:: ================================================
:: Gallery-DL Wrapper
:: Reads from urls.txt or prompts for URL
:: Author: haiderCho
:: ================================================

set "listfile=urls.txt"

if exist "%listfile%" (
    echo Reading from %listfile%...
    for /f "usebackq delims=" %%A in ("%listfile%") do (
        echo Downloading: %%A
        gallery-dl "%%A"
    )
) else (
    echo %listfile% not found.
    set /p "url=Enter URL to download: "
    if not "!url!"=="" (
        gallery-dl "!url!"
    )
)

echo Done.
pause
