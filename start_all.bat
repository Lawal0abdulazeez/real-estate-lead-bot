@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Python virtual environment not found in .venv
    pause
    exit /b 1
)

".venv\Scripts\python.exe" run_all.py
