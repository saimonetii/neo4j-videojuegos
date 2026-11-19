@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Iniciando GameGraph... (no cierres esta ventana durante la demo)
start "" cmd /c "timeout /t 6 >nul & start http://127.0.0.1:5000"
python run.py
echo.
pause
