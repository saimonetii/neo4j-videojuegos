@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Instalando dependencias (solo la primera vez en cada computadora)...
python -m pip install -r requirements.txt
echo.
if not exist .env echo FALTA el archivo .env: copialo de tu otra computadora a esta carpeta.
pause
