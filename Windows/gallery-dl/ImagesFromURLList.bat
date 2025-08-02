@echo off
for /f "usebackq delims=" %%A in ("urls.txt") do (
    gallery-dl "%%A"
)
pause
