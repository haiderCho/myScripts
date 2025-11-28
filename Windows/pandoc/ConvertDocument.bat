@echo off
setlocal enabledelayedexpansion

:: ================================================
:: Universal Document Converter (Pandoc)
:: Consolidates PDF/TEX/DOCX/MD conversions
:: Author: haiderCho
:: ================================================

:: Check for Pandoc
where pandoc >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Pandoc not found!
    pause
    exit /b 1
)

:: 1. Determine Input
set "targets="
if "%~1"=="" (
    echo No files dropped. Scanning current directory for documents...
    for %%F in (*.docx *.md *.txt *.rst *.html) do (
        set "targets=!targets! "%%~fF""
    )
) else (
    :args_loop
    if "%~1"=="" goto :args_done
    if exist "%~1" set "targets=!targets! "%~1""
    shift
    goto :args_loop
    :args_done
)

if "!targets!"=="" (
    echo No document files found.
    pause
    exit /b 0
)

:: 2. Choose Output Format
echo.
echo Choose Output Format:
echo 1. PDF (Requires PDF Engine)
echo 2. LaTeX (.tex)
echo 3. Word (.docx)
echo 4. Markdown (.md)
echo 5. HTML
set /p "fmt_choice=Select (1-5): "

set "out_ext=.pdf"
if "!fmt_choice!"=="2" set "out_ext=.tex"
if "!fmt_choice!"=="3" set "out_ext=.docx"
if "!fmt_choice!"=="4" set "out_ext=.md"
if "!fmt_choice!"=="5" set "out_ext=.html"

:: 3. PDF Engine Detection (if PDF selected)
set "pdf_engine="
if "!out_ext!"==".pdf" (
    echo.
    echo Detecting PDF engines...
    
    where wkhtmltopdf >nul 2>&1 && set "pdf_engine=wkhtmltopdf" && echo   [OK] wkhtmltopdf
    where pdflatex >nul 2>&1 && set "pdf_engine=pdflatex" && echo   [OK] pdflatex
    where xelatex >nul 2>&1 && set "pdf_engine=xelatex" && echo   [OK] xelatex
    where lualatex >nul 2>&1 && set "pdf_engine=lualatex" && echo   [OK] lualatex
    
    if not defined pdf_engine (
        echo   [WARN] No PDF engine found. Conversion might fail unless using Word COM.
    ) else (
        echo   Using: !pdf_engine!
    )
)

:: 4. Processing
for %%T in (!targets!) do (
    set "file_path=%%~fT"
    set "file_name=%%~nT"
    set "out_file=%%~dpT!file_name!!out_ext!"
    
    echo Converting: "%%~nxT" to "!out_ext!"
    
    if "!out_ext!"==".pdf" (
        :: PDF Conversion Logic
        if defined pdf_engine (
            pandoc "!file_path!" -o "!out_file!" --pdf-engine=!pdf_engine!
        ) else (
            :: Fallback to Word COM if input is DOCX and no engine
            if /i "%%~xT"==".docx" (
                 powershell -Command "$word = New-Object -ComObject Word.Application; $word.Visible = $false; $doc = $word.Documents.Open('!file_path!'); $doc.SaveAs([ref]'!out_file!', [ref]17); $doc.Close(); $word.Quit()" 2>nul
            ) else (
                pandoc "!file_path!" -o "!out_file!"
            )
        )
    ) else (
        :: Other formats
        pandoc -s "!file_path!" -o "!out_file!"
    )
    
    if errorlevel 1 (
        echo   [FAILED] Conversion failed.
    ) else (
        echo   [OK] Success.
    )
    echo.
)

echo Done.
pause
