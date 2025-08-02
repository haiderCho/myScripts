@echo off
setlocal enabledelayedexpansion

REM List of extensions to convert
set exts=md docx html txt rst

for %%e in (%exts%) do (
    for %%f in (*.`%%e`) do (
        pandoc -s "%%f" -o "%%~nf.tex"
    )
)

pause
