from fastapi import APIRouter
from app.services import GastoService
from app.repositories import gasto_repository

router = APIRouter(prefix="/resumen", tags=["Resumen"])

gasto_service = GastoService(gasto_repository)


@router.get("")
def obtener_resumen():
    return gasto_service.calcular_resumen_deudas()
