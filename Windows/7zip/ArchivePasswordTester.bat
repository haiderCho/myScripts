@echo off
setlocal enabledelayedexpansion

:: ---------------------------
:: Auto-detect files in folder
:: ---------------------------
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

:: Try to find first .rar file
set "ARCHIVE="
for %%F in (*.rar) do (
  set "ARCHIVE=%%~fF"
  goto :found_archive
)
:found_archive

:: Try to find passwords.txt first, otherwise first .txt that's not this .bat
set "PASSLIST="
if exist "passwords.txt" set "PASSLIST=%~dp0passwords.txt"
if not defined PASSLIST (
  for %%T in (*.txt) do (
    if /i not "%%~nT%%~xT"=="%~n0%~x0" (
      set "PASSLIST=%%~fT"
      goto :found_pass
    )
  )
)
:found_pass

:: Output dir and 7z path (edit if needed)
set "OUTDIR=%SCRIPT_DIR%extracted"
set "SEVENZIP=C:\Program Files\7-Zip\7z.exe"

:: If 7z not found at the default, try to use 7z from PATH
if not exist "%SEVENZIP%" (
  where 7z >nul 2>&1
  if not errorlevel 1 (
    set "SEVENZIP=7z"
  )
)

:: Log file
set "LOGFILE=%SCRIPT_DIR%attempts.log"
echo ===== Password attempt run at %DATE% %TIME% =====> "%LOGFILE%"

:: Basic checks
if not defined ARCHIVE (
  echo ERROR: No .rar archive found in "%SCRIPT_DIR%". >> "%LOGFILE%"
  echo ERROR: No .rar archive found in "%SCRIPT_DIR%".
  pause
  exit /b 1
)
if not defined PASSLIST (
  echo ERROR: No .txt password list found in "%SCRIPT_DIR%". >> "%LOGFILE%"
  echo ERROR: No .txt password list found in "%SCRIPT_DIR%".
  pause
  exit /b 1
)
if not exist "%SEVENZIP%" (
  echo WARNING: 7z not found at "%SEVENZIP%". Please install 7-Zip or update the script. >> "%LOGFILE%"
  echo WARNING: 7z not found at "%SEVENZIP%". Make sure 7z.exe is installed and either update the SEVENZIP path in the script or add 7z to PATH.
  pause
  exit /b 1
)

if not exist "%OUTDIR%" mkdir "%OUTDIR%"

echo Archive: %ARCHIVE% >> "%LOGFILE%"
echo Password list: %PASSLIST% >> "%LOGFILE%"
echo 7z path: %SEVENZIP% >> "%LOGFILE%"
echo Output dir: %OUTDIR% >> "%LOGFILE%"
echo. >> "%LOGFILE%"

:: Iterate through each password (each line)
set "FOUND="
for /f "usebackq delims=" %%P in ("%PASSLIST%") do (
  set "PW=%%P"
  :: remove trailing CR if any
  set "PW=!PW:~0,512!"
  echo Trying: [!PW!] >> "%LOGFILE%"
  "%SEVENZIP%" t -p"!PW!" "%ARCHIVE%" >nul 2>&1
  if not errorlevel 1 (
    echo SUCCESS: password found: !PW! >> "%LOGFILE%"
    echo.
    echo SUCCESS: password found: !PW!
    set "FOUND=!PW!"
    goto :EXTRACT
  )
)

:EXTRACT
if defined FOUND (
  echo Extracting to "%OUTDIR%"...
  "%SEVENZIP%" x -y -o"%OUTDIR%" -p"%FOUND%" "%ARCHIVE%"
  if errorlevel 1 (
    echo Extraction failed even after finding password. See attempts.log for details. >> "%LOGFILE%"
    echo Extraction failed.
  ) else (
    echo Extraction succeeded. Files written to: "%OUTDIR%". >> "%LOGFILE%"
    echo Extraction succeeded. Files written to: "%OUTDIR%".
  )
  echo Finished at %DATE% %TIME% >> "%LOGFILE%"
) else (
  echo No password in list succeeded. >> "%LOGFILE%"
  echo No password in list succeeded.
  echo Finished at %DATE% %TIME% >> "%LOGFILE%"
)

pause
endlocal
exit /b 0
