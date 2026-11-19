@echo off
chcp 65001 >nul
cd /d "%~dp0"
if exist .git (
  echo Buscando actualizaciones en GitHub...
  git pull --ff-only
)
echo Iniciando GameGraph... (no cierres esta ventana durante la demo)
start "" cmd /c "timeout /t 8 >/dev/null & start http://127.0.0.1:5000"
python run.py
echo.
pause
