from typing import Optional
from app.models.grupo import Grupo, GastoCreate
from app.crud_grupos.repository import grupo_repository


def agregar_gasto(grupo_id: int, gasto: GastoCreate) -> Optional[Grupo]:
    return grupo_repository.agregar_gasto(grupo_id, gasto)
