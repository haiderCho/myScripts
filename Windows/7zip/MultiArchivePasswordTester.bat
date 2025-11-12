@echo off
setlocal enabledelayedexpansion

:: Folder setup
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

set "PASSLIST=passwords.txt"
if not exist "%PASSLIST%" (
  echo [ERROR] passwords.txt not found in %SCRIPT_DIR%
  pause
  exit /b
)

:: Try find 7z
set "SEVENZIP=C:\Program Files\7-Zip\7z.exe"
if not exist "%SEVENZIP%" (
  where 7z >nul 2>&1
  if errorlevel 1 (
    echo [ERROR] 7z not found. Please install 7-Zip or fix the SEVENZIP path.
    pause
    exit /b
  )
  set "SEVENZIP=7z"
)

set "OUTDIR=%SCRIPT_DIR%extracted"
if not exist "%OUTDIR%" mkdir "%OUTDIR%"

set "LOGFILE=%SCRIPT_DIR%attempts.log"
set "CSVFILE=%SCRIPT_DIR%attempts.csv"
echo "archive","password","success" > "%CSVFILE%"
echo ==== Run at %DATE% %TIME% ==== > "%LOGFILE%"

:: Supported extensions
set "EXTS=rar zip 7z tar gz tgz bz2 xz iso"

for %%E in (%EXTS%) do (
  for %%A in (*.%%E) do (
    if exist "%%~fA" (
      echo Processing: %%~nxA
      echo --- Archive: %%~nxA --- >> "%LOGFILE%"
      set "FOUND_PASS="
      for /f "usebackq delims=" %%P in ("%PASSLIST%") do (
        set "PW=%%P"
        if not "!PW!"=="" (
          set "FIRST=!PW:~0,1!"
          if not "!FIRST!"=="#" if not "!FIRST!"==";" (
            "%SEVENZIP%" t -p"!PW!" "%%~fA" >nul 2>&1
            if !errorlevel! equ 0 (
              echo SUCCESS - %%~nxA : !PW!
              echo SUCCESS - %%~nxA : !PW! >> "%LOGFILE%"
              echo "%%~nxA","!PW!",1>> "%CSVFILE%"
              if not defined FOUND_PASS set "FOUND_PASS=!PW!"
            ) else (
              echo "%%~nxA","!PW!",0>> "%CSVFILE%"
            )
          )
        )
      )
      if defined FOUND_PASS (
        echo Extracting %%~nxA ...
        "%SEVENZIP%" x -y -o"%OUTDIR%\%%~nA" -p"%FOUND_PASS%" "%%~fA" >> "%LOGFILE%" 2>&1
        if errorlevel 1 (
          echo [WARN] Extraction failed for %%~nxA >> "%LOGFILE%"
        ) else (
          echo Extracted to "%OUTDIR%\%%~nA" >> "%LOGFILE%"
        )
      ) else (
        echo [INFO] No password worked for %%~nxA >> "%LOGFILE%"
      )
      echo. >> "%LOGFILE%"
    )
  )
)

echo ==== Finished at %DATE% %TIME% ==== >> "%LOGFILE%"
echo Done. Results saved to:
echo   %CSVFILE%
echo   %LOGFILE%
pause
endlocal
exit /b