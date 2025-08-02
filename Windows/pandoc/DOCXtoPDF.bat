# Requires Word installed (or install wkhtmltopdf and use --pdf-engine=wkhtmltopdf as fallback)

@echo off
for %%f in (*.docx) do (
    pandoc "%%f" -o "%%~nf.pdf"
)
pause
