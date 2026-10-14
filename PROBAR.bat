@echo off
cd /d "%~dp0"
if exist .venv\Scripts\python.exe (
  .venv\Scripts\python.exe -m unittest discover -s tests -v
) else (
  python -m unittest discover -s tests -v
)
if errorlevel 1 goto error
echo Pruebas Python aprobadas.
pause
exit /b 0
:error
echo Hay pruebas pendientes o fallidas.
pause
exit /b 1
