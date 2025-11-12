:: ===============================
:: Zip All Folders using 7-Zip
:: Author: haiderCho
:: ===============================

@echo off
setlocal enabledelayedexpansion

rem Compress each folder in the current directory into a zip file using 7-Zip
for /d %%X in (*) do (
    echo Compressing: %%X
    "C:\Program Files\7-Zip\7z.exe" a "%%~X.zip" "%%~X\" -tzip -mx=5 >nul
)
echo All folders compressed.
endlocal
