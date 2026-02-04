from typing import Optional
from app.models.grupo import Grupo
from app.crud_grupos.repository import grupo_repository


def eliminar_gasto(grupo_id: int, gasto_id: int) -> Optional[Grupo]:
    return grupo_repository.eliminar_gasto(grupo_id, gasto_id)
