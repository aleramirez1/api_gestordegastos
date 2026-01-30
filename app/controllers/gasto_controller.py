from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models import Gasto, GastoCreate, GastoUpdate
from app.services import GastoService
from app.repositories import gasto_repository

router = APIRouter(prefix="/gastos", tags=["Gastos"])

gasto_service = GastoService(gasto_repository)


@router.post("", response_model=Gasto, status_code=status.HTTP_201_CREATED)
def crear_gasto(gasto: GastoCreate):
    return gasto_service.crear_gasto(gasto)


@router.get("", response_model=List[Gasto])
def obtener_gastos():
    return gasto_service.obtener_gastos()


@router.get("/{gasto_id}", response_model=Gasto)
def obtener_gasto(gasto_id: int):
    gasto = gasto_service.obtener_gasto_por_id(gasto_id)
    if not gasto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gasto con ID {gasto_id} no encontrado"
        )
    return gasto


@router.put("/{gasto_id}", response_model=Gasto)
def actualizar_gasto(gasto_id: int, gasto_update: GastoUpdate):
    gasto = gasto_service.actualizar_gasto(gasto_id, gasto_update)
    if not gasto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gasto con ID {gasto_id} no encontrado"
        )
    return gasto


@router.delete("/{gasto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_gasto(gasto_id: int):
    if not gasto_service.eliminar_gasto(gasto_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gasto con ID {gasto_id} no encontrado"
        )
    return None
