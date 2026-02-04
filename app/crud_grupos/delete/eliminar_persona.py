from typing import Optional
from app.models.grupo import Grupo
from app.crud_grupos.repository import grupo_repository


def eliminar_persona(grupo_id: int, persona: str) -> Optional[Grupo]:
    return grupo_repository.eliminar_persona(grupo_id, persona)
