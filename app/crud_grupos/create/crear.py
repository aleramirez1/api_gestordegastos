from app.models.grupo import Grupo, GrupoCreate
from app.crud_grupos.repository import grupo_repository


def crear(grupo: GrupoCreate) -> Grupo:
    return grupo_repository.crear(grupo)
