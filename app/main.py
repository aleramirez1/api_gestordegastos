from fastapi import FastAPI
from app.controllers.gasto_controller import router as gasto_router
from app.controllers.resumen_controller import router as resumen_router
from app.middlewares import setup_cors

app = FastAPI(
    title="API Gestor de Gastos Compartidos",
    description="API para gestionar gastos compartidos entre amigos",
    version="1.0.0"
)

setup_cors(app)

app.include_router(gasto_router)
app.include_router(resumen_router)


@app.get("/", tags=["Root"])
def read_root():
    return {
        "mensaje": "API Gestor de Gastos Compartidos",
        "version": "1.0.0",
        "documentacion": "/docs"
    }
