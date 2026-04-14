from fastapi import APIRouter, HTTPException, status
from app.models.usuario import Usuario, UsuarioPerfilUpdate
from app.repositories.usuario_repository import usuario_repository

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.put("/{usuario_id}", response_model=Usuario)
def actualizar_perfil(usuario_id: int, usuario_update: UsuarioPerfilUpdate):
    actualizado = usuario_repository.actualizar_perfil(
        usuario_id=usuario_id,
        nombre=usuario_update.nombre,
        foto_perfil=usuario_update.foto_perfil,
    )
    if not actualizado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return actualizado
