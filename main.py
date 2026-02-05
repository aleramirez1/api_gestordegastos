import sys
sys.path.insert(0, ".")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="API Gestor de Gastos")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.controllers.auth_controller import router as auth_router
from app.crud_grupos.router import router as grupo_router

app.include_router(auth_router)
app.include_router(grupo_router)


@app.get("/")
def root():
    return {"mensaje": "API Gestor de Gastos"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
