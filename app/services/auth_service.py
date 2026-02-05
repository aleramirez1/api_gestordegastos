from typing import Optional
from app.models.usuario import Usuario, UsuarioCreate, UsuarioResponse
from app.repositories.usuario_repository import UsuarioRepository
import hashlib
import time


class AuthService:
    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def _generar_token(self, usuario_id: int) -> str:
        data = f"{usuario_id}-{time.time()}"
        return hashlib.md5(data.encode()).hexdigest()

    def registrar(self, usuario: UsuarioCreate) -> Optional[UsuarioResponse]:
        existente = self.repository.buscar_por_nombre(usuario.nombre)
        if existente:
            return None
        
        nuevo = self.repository.crear(usuario)
        token = self._generar_token(nuevo.id)
        return UsuarioResponse(
            id=nuevo.id,
            nombre=nuevo.nombre,
            email=nuevo.email,
            token=token
        )

    def login(self, nombre: str, password: str) -> Optional[UsuarioResponse]:
        usuario = self.repository.verificar_password(nombre, password)
        if not usuario:
            return None
        
        token = self._generar_token(usuario.id)
        return UsuarioResponse(
            id=usuario.id,
            nombre=usuario.nombre,
            email=usuario.email,
            token=token
        )
