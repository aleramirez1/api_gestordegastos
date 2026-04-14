from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from app.models.grupo import (
    Grupo,
    GrupoCreate,
    GrupoUpdate,
    GastoCreate,
    GastoEdit,
    RuletaWeightedRequest,
    RuletaWeightedResult,
)
from app.crud_grupos.repository import grupo_repository

router = APIRouter(prefix="/grupos", tags=["Grupos"])


@router.post("", response_model=Grupo, status_code=status.HTTP_201_CREATED)
def crear_grupo(grupo: GrupoCreate):
    return grupo_repository.crear(grupo)


@router.get("", response_model=List[Grupo])
def listar_grupos(usuario_id: Optional[int] = None):
    if usuario_id is None:
        return grupo_repository.obtener_todos()
    return grupo_repository.obtener_por_usuario(usuario_id)


@router.get("/usuario/{usuario_id}", response_model=List[Grupo])
def listar_grupos_usuario(usuario_id: int):
    return grupo_repository.obtener_por_usuario(usuario_id)


@router.get("/{grupo_id}", response_model=Grupo)
def obtener_grupo(grupo_id: int):
    grupo = grupo_repository.obtener_por_id(grupo_id)
    if not grupo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")
    return grupo


@router.put("/{grupo_id}", response_model=Grupo)
def actualizar_grupo(grupo_id: int, grupo_update: GrupoUpdate):
    grupo = grupo_repository.actualizar(grupo_id, grupo_update)
    if not grupo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")
    return grupo


@router.delete("/{grupo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_grupo(grupo_id: int):
    if not grupo_repository.eliminar(grupo_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")


@router.post("/{grupo_id}/personas/{persona}", response_model=Grupo)
def agregar_persona(grupo_id: int, persona: str):
    grupo = grupo_repository.agregar_persona(grupo_id, persona)
    if not grupo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")
    return grupo


@router.delete("/{grupo_id}/personas/{persona}", response_model=Grupo)
def eliminar_persona(grupo_id: int, persona: str):
    grupo = grupo_repository.eliminar_persona(grupo_id, persona)
    if not grupo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")
    return grupo


@router.post("/{grupo_id}/gastos", response_model=Grupo)
def agregar_gasto(grupo_id: int, gasto: GastoCreate):
    grupo = grupo_repository.agregar_gasto(grupo_id, gasto)
    if not grupo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")
    return grupo


@router.delete("/{grupo_id}/gastos/{gasto_id}", response_model=Grupo)
def eliminar_gasto(grupo_id: int, gasto_id: int):
    grupo = grupo_repository.eliminar_gasto(grupo_id, gasto_id)
    if not grupo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")
    return grupo


@router.put("/{grupo_id}/gastos/{gasto_id}", response_model=Grupo)
def editar_gasto(grupo_id: int, gasto_id: int, gasto: GastoEdit):
    grupo = grupo_repository.editar_gasto(grupo_id, gasto_id, gasto.monto)
    if not grupo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")
    return grupo


@router.post("/{grupo_id}/ruleta/weighted", response_model=RuletaWeightedResult)
def ruleta_weighted(grupo_id: int, request: RuletaWeightedRequest):
    grupo = grupo_repository.obtener_por_id(grupo_id)
    if not grupo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")

    resultado = grupo_repository.seleccionar_pagador_weighted(
        grupo_id=grupo_id,
        anio=request.anio,
        mes=request.mes,
        suavizado=request.suavizado,
    )

    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El grupo no tiene personas para calcular la ruleta",
        )

    return {
        **resultado,
        "monto_referencia": request.monto,
    }
