@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Bajando la ultima version desde GitHub...
git pull
echo.
echo Actualizando portadas en AuraDB (sin borrar tus datos)...
python -m database.seed --keep
echo.
pause
