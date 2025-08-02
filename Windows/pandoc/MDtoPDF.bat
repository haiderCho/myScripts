@echo off
for %%f in (*.md) do (
    pandoc "%%f" -o "%%~nf.pdf"
)
pause
