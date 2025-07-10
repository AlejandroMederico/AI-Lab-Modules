@echo off
echo ================================
echo Iniciando FullStack (Backend + Frontend)
echo ================================

:: 1. Iniciar backend en nueva ventana
start cmd /k "echo Iniciando backend... & call env\Scripts\activate & pip install -r requirements.txt & uvicorn backend.main:app --reload --port 8001"

:: 2. Instalar dependencias frontend si hace falta
cd frontend
echo Instalando dependencias de frontend...
call npm install

:: 3. Iniciar frontend en nueva ventana
start cmd /k "echo Iniciando frontend... & npm run dev"

cd ..
