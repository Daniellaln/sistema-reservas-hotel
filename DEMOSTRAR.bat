@echo off
chcp 65001 >nul
cd /d "%~dp0..\proyecto"
if exist .venv\Scripts\python.exe (
  .venv\Scripts\python.exe -X utf8 -B "%~dp0demostrar.py"
) else (
  python -X utf8 -B "%~dp0demostrar.py"
)
if errorlevel 1 goto error
echo Demostracion Python completada.
pause
exit /b 0
:error
echo No se pudo completar la demostracion. Revisa el mensaje anterior.
pause
exit /b 1
