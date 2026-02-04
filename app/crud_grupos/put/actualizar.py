from typing import Optional
from app.models.grupo import Grupo, GrupoUpdate
from app.crud_grupos.repository import grupo_repository


def actualizar(grupo_id: int, grupo_update: GrupoUpdate) -> Optional[Grupo]:
    return grupo_repository.actualizar(grupo_id, grupo_update)
