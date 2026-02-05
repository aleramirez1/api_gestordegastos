from typing import List
from app.models.grupo import Grupo
from app.crud_grupos.repository import grupo_repository


def obtener_todos() -> List[Grupo]:
    return grupo_repository.obtener_todos()
