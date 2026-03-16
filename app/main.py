from fastapi import FastAPI
from app.controllers.auth_controller import router as auth_router
from app.crud_grupos.router import router as grupo_router
from app.middlewares.cors import setup_cors
from app.database import init_db

app = FastAPI(title="API Gestor de Gastos", version="1.0.0")

setup_cors(app)
init_db()

app.include_router(auth_router)
app.include_router(grupo_router)


@app.get("/")
def read_root():
    return {"mensaje": "API Gestor de Gastos", "version": "1.0.0", "docs": "/docs"}
