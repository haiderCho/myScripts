@echo off
for %%f in (*.md) do (
    pandoc -s "%%f" -o "%%~nf.tex"
)
pause
