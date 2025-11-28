@echo off
setlocal enabledelayedexpansion

:: ================================================
:: Open Set Websites
:: Reads from websites.txt or uses defaults
:: Author: haiderCho
:: ================================================

set "listfile=%~dp0websites.txt"

if exist "%listfile%" (
    echo Reading from websites.txt...
    for /f "usebackq delims=" %%A in ("%listfile%") do (
        if not "%%A"=="" (
            echo Opening: %%A
            start "" "%%A"
        )
    )
) else (
    echo websites.txt not found. Using defaults...
    start https://github.com/haiderCho
    start https://www.stackoverflow.com
)

exit /b
