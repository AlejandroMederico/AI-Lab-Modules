# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importamos Base y engine para crear las tablas
from backend.database import Base, engine

# Importamos las rutas de autenticación
from backend.auth import routes as auth_routes

# Crea las tablas si aún no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Agente IA – Backend")

# ────────────────────────────────
# Configuración de CORS
# ────────────────────────────────
# Durante el desarrollo dejamos "*" para no tener problemas
# Luego puedes restringir a ["http://localhost:5173"] o tu dominio
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ────────────────────────────────
# Incluir routers
# ────────────────────────────────
app.include_router(auth_routes.router)


# Ruta raíz opcional
@app.get("/")
def read_root():
    return {"msg": "API del Agente IA funcionando ✅"}
