@echo off
setlocal

set "out=output.txt"
> "%out%" echo.

for %%F in (*,*) do (
    echo %%~nxF >> "%out%"
)

echo Done.
