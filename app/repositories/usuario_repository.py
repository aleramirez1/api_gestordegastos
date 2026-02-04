from typing import Optional, List
from app.models.usuario import Usuario, UsuarioCreate
from datetime import datetime
import hashlib


class UsuarioRepository:
    def __init__(self):
        self._usuarios: List[dict] = []
        self._counter = 0

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def crear(self, usuario: UsuarioCreate) -> Usuario:
        self._counter += 1
        nuevo = {
            "id": self._counter,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "password": self._hash_password(usuario.password)
        }
        self._usuarios.append(nuevo)
        return Usuario(id=nuevo["id"], nombre=nuevo["nombre"], email=nuevo["email"])

    def buscar_por_email(self, email: str) -> Optional[dict]:
        for u in self._usuarios:
            if u["email"] == email:
                return u
        return None

    def verificar_password(self, email: str, password: str) -> Optional[Usuario]:
        usuario = self.buscar_por_email(email)
        if usuario and usuario["password"] == self._hash_password(password):
            return Usuario(id=usuario["id"], nombre=usuario["nombre"], email=usuario["email"])
        return None


usuario_repository = UsuarioRepository()
