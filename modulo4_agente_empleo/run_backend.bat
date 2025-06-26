@echo off
echo Activando entorno virtual...

call env\Scripts\activate

echo Entorno virtual activado.
echo Iniciando backend en puerto 8001...

uvicorn backend.main:app --reload --port 8001

pause
