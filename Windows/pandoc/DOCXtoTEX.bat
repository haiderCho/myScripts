@echo off
for %%f in (*.docx) do (
    pandoc -s "%%f" -o "%%~nf.tex"
)
pause
