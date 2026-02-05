from fastapi import FastAPI
from app.controllers.auth_controller import router as auth_router
from app.crud_grupos.router import router as grupo_router
from app.middlewares.cors import setup_cors
import uvicorn

app = FastAPI(
    title="API Gestor de Gastos Compartidos",
    description="API para gestionar gastos compartidos entre amigos",
    version="1.0.0"
)

setup_cors(app)

app.include_router(auth_router)
app.include_router(grupo_router)


@app.get("/", tags=["Root"])
def read_root():
    return {
        "mensaje": "API Gestor de Gastos Compartidos",
        "version": "1.0.0",
        "documentacion": "/docs"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
