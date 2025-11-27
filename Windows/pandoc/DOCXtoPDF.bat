@echo off
setlocal enabledelayedexpansion

:: ================================================
:: DOCX to PDF Converter using Pandoc
:: Supports multiple PDF engines with auto-detection
:: Author: haiderCho
:: ================================================

echo.
echo ================================================
echo   DOCX to PDF Converter
echo ================================================
echo.

:: Check if Pandoc is installed
where pandoc >nul 2>&1
if errorlevel 1 (
    echo ERROR: Pandoc is not installed or not in PATH
    echo.
    echo Please install Pandoc from: https://pandoc.org/installing.html
    echo.
    pause
    exit /b 1
)

echo Pandoc found: 
pandoc --version | findstr /R "^pandoc "
echo.

:: Detect available PDF engines
echo Detecting PDF engines...

set "engines_found=0"
set "engines_list="

:: Check for wkhtmltopdf
where wkhtmltopdf >nul 2>&1
if not errorlevel 1 (
    set /a engines_found+=1
    set "engines_list=!engines_list! wkhtmltopdf"
    echo   [OK] wkhtmltopdf found
)

:: Check for pdflatex
where pdflatex >nul 2>&1
if not errorlevel 1 (
    set /a engines_found+=1
    set "engines_list=!engines_list! pdflatex"
    echo   [OK] pdflatex found
)

:: Check for lualatex
where lualatex >nul 2>&1
if not errorlevel 1 (
    set /a engines_found+=1
    set "engines_list=!engines_list! lualatex"
    echo   [OK] lualatex found
)

:: Check for xelatex
where xelatex >nul 2>&1
if not errorlevel 1 (
    set /a engines_found+=1
    set "engines_list=!engines_list! xelatex"
    echo   [OK] xelatex found
)

:: Check for Microsoft Word (via PowerShell COM)
powershell -Command "try { New-Object -ComObject Word.Application | Out-Null; exit 0 } catch { exit 1 }" >nul 2>&1
if not errorlevel 1 (
    set /a engines_found+=1
    set "engines_list=!engines_list! word"
    echo   [OK] Microsoft Word found
)

if !engines_found! equ 0 (
    echo.
    echo ERROR: No PDF engine found!
    echo.
    echo Please install one of the following:
    echo   - wkhtmltopdf: https://wkhtmltopdf.org/
    echo   - LaTeX (pdflatex, xelatex, lualatex^): https://miktex.org/
    echo   - Microsoft Word
    echo.
    pause
    exit /b 1
)

echo.
echo Found !engines_found! PDF engine(s):!engines_list!
echo.

:: Select default engine (first available in priority order)
if defined engines_list (
    for %%E in (!engines_list!) do (
        if not defined pdf_engine (
            set "pdf_engine=%%E"
        )
    )
)

echo Using PDF engine: !pdf_engine!
echo.

:: Count DOCX files
set "file_count=0"
for %%f in (*.docx) do set /a file_count+=1

if !file_count! equ 0 (
    echo No .docx files found in current directory
    pause
    exit /b 0
)

echo Found !file_count! file(s) to convert
echo.

:: Convert files
set "success_count=0"
set "error_count=0"

for %%f in (*.docx) do (
    echo Converting: %%f
    
    if "!pdf_engine!"=="word" (
        REM Use PowerShell with Word COM object
        powershell -Command "$word = New-Object -ComObject Word.Application; $word.Visible = $false; $doc = $word.Documents.Open('%%~ff'); $doc.SaveAs([ref]'%%~dpnf.pdf', [ref]17); $doc.Close(); $word.Quit()" 2>nul
    ) else (
        REM Use Pandoc with specified engine
        pandoc "%%f" -o "%%~nf.pdf" --pdf-engine=!pdf_engine! 2>nul
    )
    
    if errorlevel 1 (
        echo   [FAILED] Error converting %%f
        set /a error_count+=1
    ) else (
        if exist "%%~nf.pdf" (
            echo   [OK] Created %%~nf.pdf
            set /a success_count+=1
        ) else (
            echo   [FAILED] Output file not created
            set /a error_count+=1
        )
    )
    echo.
)

:: Summary
echo ================================================
echo   Conversion Summary
echo ================================================
echo   Total files: !file_count!
echo   Successful:  !success_count!
echo   Failed:      !error_count!
echo ================================================
echo.

pause
