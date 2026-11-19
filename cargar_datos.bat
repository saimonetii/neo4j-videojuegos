@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Cargando datos de ejemplo en AuraDB...
python -m database.seed
echo.
pause
