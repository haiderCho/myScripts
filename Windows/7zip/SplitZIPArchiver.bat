@echo off
:: ===============================
:: Split ZIP Archiver using 7-Zip
:: Author: haiderCho
:: ===============================

:: Prompt user for input
set /p source_path="Enter the full path of the file or folder to compress: "
set /p archive_name="Enter the name for the archive (without extension): "
set /p split_size="Enter split size (e.g., 100M, 700M, 1G): "
set /p output_path="Enter output folder path: "

:: Ensure output directory exists
if not exist "%output_path%" (
    echo Creating output folder...
    mkdir "%output_path%"
)

:: 7-Zip command for splitting archive
echo.
echo Archiving and splitting files...
echo ------------------------------------
7z a "%output_path%\%archive_name%.7z" "%source_path%" -v%split_size% -mx=9

:: Check if successful
if %errorlevel%==0 (
    echo.
    echo ✅ Successfully created split archive:
    echo Location: %output_path%\%archive_name%.7z.*
) else (
    echo.
    echo ❌ Error: Archiving failed. Check file paths or 7-Zip installation.
)

pause
