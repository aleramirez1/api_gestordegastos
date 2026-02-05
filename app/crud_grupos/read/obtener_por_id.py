from typing import Optional
from app.models.grupo import Grupo
from app.crud_grupos.repository import grupo_repository


def obtener_por_id(grupo_id: int) -> Optional[Grupo]:
    return grupo_repository.obtener_por_id(grupo_id)
