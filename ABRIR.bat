@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe goto falta
if not exist frontend\build-ui\index.html goto falta
.venv\Scripts\python.exe app.py
if errorlevel 1 pause
exit /b
:falta
echo Ejecuta PREPARAR.bat primero.
pause
