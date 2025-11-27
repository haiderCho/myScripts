@echo off
echo ============================================
echo  FULL PYTHON 3.13 PURGE - WINDOWS
echo ============================================
echo Running with admin rights is required.
echo.

:: --- Kill any running python process ---
echo Stopping Python processes...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM python3.exe >nul 2>&1
taskkill /F /IM py.exe >nul 2>&1

:: --- Remove standard install directories ---
echo Removing install directories...
rmdir /s /q "C:\Python313"
rmdir /s /q "C:\Python\Python313"
rmdir /s /q "%LocalAppData%\Programs\Python\Python313"
rmdir /s /q "%LocalAppData%\Programs\Python"
rmdir /s /q "%LocalAppData%\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_*"

:: --- Remove Windows Store Python stubs ---
echo Removing Windows Store Python stubs...
del /f /q "%LocalAppData%\Microsoft\WindowsApps\python.exe" >nul 2>&1
del /f /q "%LocalAppData%\Microsoft\WindowsApps\python3.exe" >nul 2>&1
del /f /q "%LocalAppData%\Microsoft\WindowsApps\python3.13.exe" >nul 2>&1
del /f /q "%LocalAppData%\Microsoft\WindowsApps\python3.13*" >nul 2>&1

:: --- Remove AppData python directories ---
echo Removing AppData Python folders...
rmdir /s /q "%AppData%\Python" >nul 2>&1
rmdir /s /q "%LocalAppData%\Python" >nul 2>&1

:: --- Remove pip cache ---
echo Removing pip cache...
rmdir /s /q "%LocalAppData%\pip" >nul 2>&1
rmdir /s /q "%UserProfile%\AppData\Local\Temp\pip*" >nul 2>&1

:: --- Remove py launcher ---
echo Removing Python launcher...
del /f /q "C:\Windows\py.exe" >nul 2>&1
del /f /q "C:\Windows\pyw.exe" >nul 2>&1

:: --- Remove registry entries for Python 3.13 ---
echo Cleaning registry entries...
reg delete "HKCU\Software\Python\PythonCore\3.13" /f >nul 2>&1
reg delete "HKLM\Software\Python\PythonCore\3.13" /f >nul 2>&1
reg delete "HKLM\Software\WOW6432Node\Python\PythonCore\3.13" /f >nul 2>&1
reg delete "HKCU\Software\Python" /f >nul 2>&1

:: --- Remove PATH entries containing Python or Python313 ---
echo Cleaning PATH...
setlocal EnableDelayedExpansion

set "newpath="
for %%A in ("%PATH:;=","%") do (
    echo %%~A | findstr /I "Python" >nul
    if errorlevel 1 (
        if defined newpath (
            set "newpath=!newpath!;%%~A"
        ) else (
            set "newpath=%%~A"
        )
    )
)

:: Apply new PATH
if defined newpath (
    echo Updating PATH...
    setx PATH "!newpath!" >nul
)

endlocal

:: --- Final verification ---
echo.
echo ============================================
echo Python 3.13 Removal Complete
echo ============================================
echo Run the following to verify:
echo   python --version
echo   py --version
echo Both should report "not recognized".
echo.
pause
