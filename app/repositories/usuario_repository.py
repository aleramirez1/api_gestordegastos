from typing import Optional
from app.models.usuario import Usuario, UsuarioCreate
from app.database import get_connection
import hashlib


class UsuarioRepository:
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def crear(self, usuario: UsuarioCreate) -> Usuario:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
            (usuario.nombre, usuario.email, self._hash_password(usuario.password))
        )
        usuario_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return Usuario(id=usuario_id, nombre=usuario.nombre, email=usuario.email)

    def buscar_por_email(self, email: str) -> Optional[dict]:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        return usuario

    def verificar_password(self, email: str, password: str) -> Optional[Usuario]:
        usuario = self.buscar_por_email(email)
        if usuario and usuario["password"] == self._hash_password(password):
            return Usuario(id=usuario["id"], nombre=usuario["nombre"], email=usuario["email"])
        return None


usuario_repository = UsuarioRepository()
