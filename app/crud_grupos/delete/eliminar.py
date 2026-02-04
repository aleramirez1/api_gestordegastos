from app.crud_grupos.repository import grupo_repository


def eliminar(grupo_id: int) -> bool:
    return grupo_repository.eliminar(grupo_id)
