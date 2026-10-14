@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe python -m venv .venv
if errorlevel 1 goto error
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto error
pushd frontend
call npm ci
if errorlevel 1 goto front_error
call npm run build
if errorlevel 1 goto front_error
popd
echo Preparacion completada. Abre ABRIR.bat.
pause
exit /b 0
:front_error
popd
:error
echo No se pudo preparar. Revisa Python, Node.js y la conexion.
pause
exit /b 1
