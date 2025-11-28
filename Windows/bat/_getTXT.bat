@echo off
setlocal

:: ================================================
:: Get File List to TXT
:: Usage: _getTXT.bat [filter] [output_file]
:: Default: *.* output.txt
:: Author: haiderCho
:: ================================================

set "filter=*.*"
set "out=output.txt"

if not "%~1"=="" set "filter=%~1"
if not "%~2"=="" set "out=%~2"

echo Listing "%filter%" to "%out%"...
> "%out%" echo File List generated on %DATE% %TIME%
>> "%out%" echo ----------------------------------------

for %%F in (%filter%) do (
    echo %%~nxF >> "%out%"
)

echo Done.
