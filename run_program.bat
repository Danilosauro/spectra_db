@echo off
setlocal

where python3 >nul 2>&1
if %errorlevel% equ 0 (
    python3 scripts\initial_screen.py
    exit /b %errorlevel%
)

where python >nul 2>&1
if %errorlevel% equ 0 (
    python scripts\initial_screen.py
    exit /b %errorlevel%
)

echo Python não está instalado. Por favor, instale o Python para rodar este programa.
exit /b 1
