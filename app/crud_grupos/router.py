from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.grupo import Grupo, GrupoCreate, GrupoUpdate, GastoCreate
from app.crud_grupos.read.obtener_todos import obtener_todos
from app.crud_grupos.read.obtener_por_id import obtener_por_id
from app.crud_grupos.create.crear import crear
from app.crud_grupos.create.agregar_persona import agregar_persona
from app.crud_grupos.create.agregar_gasto import agregar_gasto
from app.crud_grupos.update.actualizar import actualizar
from app.crud_grupos.delete.eliminar import eliminar
from app.crud_grupos.delete.eliminar_persona import eliminar_persona
from app.crud_grupos.delete.eliminar_gasto import eliminar_gasto

router = APIRouter(prefix="/grupos", tags=["Grupos"])


@router.post("", response_model=Grupo, status_code=status.HTTP_201_CREATED)
def crear_grupo(grupo: GrupoCreate):
    return crear(grupo)


@router.get("", response_model=List[Grupo])
def listar_grupos():
    return obtener_todos()


@router.get("/{grupo_id}", response_model=Grupo)
def obtener_grupo(grupo_id: int):
    grupo = obtener_por_id(grupo_id)
    if not grupo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")
    return grupo


@router.put("/{grupo_id}", response_model=Grupo)
def actualizar_grupo(grupo_id: int, grupo_update: GrupoUpdate):
    grupo = actualizar(grupo_id, grupo_update)
    if not grupo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")
    return grupo


@router.delete("/{grupo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_grupo(grupo_id: int):
    if not eliminar(grupo_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")


@router.post("/{grupo_id}/personas/{persona}", response_model=Grupo)
def agregar_persona_grupo(grupo_id: int, persona: str):
    grupo = agregar_persona(grupo_id, persona)
    if not grupo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")
    return grupo


@router.delete("/{grupo_id}/personas/{persona}", response_model=Grupo)
def eliminar_persona_grupo(grupo_id: int, persona: str):
    grupo = eliminar_persona(grupo_id, persona)
    if not grupo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")
    return grupo


@router.post("/{grupo_id}/gastos", response_model=Grupo)
def agregar_gasto_grupo(grupo_id: int, gasto: GastoCreate):
    grupo = agregar_gasto(grupo_id, gasto)
    if not grupo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")
    return grupo


@router.delete("/{grupo_id}/gastos/{gasto_id}", response_model=Grupo)
def eliminar_gasto_grupo(grupo_id: int, gasto_id: int):
    grupo = eliminar_gasto(grupo_id, gasto_id)
    if not grupo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")
    return grupo
