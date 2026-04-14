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
            "INSERT INTO usuarios (nombre, email, password, foto_perfil) VALUES (?, ?, ?, ?)",
            (usuario.nombre, usuario.email, self._hash_password(usuario.password), "")
        )
        usuario_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return Usuario(id=usuario_id, nombre=usuario.nombre, email=usuario.email, foto_perfil="")

    def buscar_por_id(self, usuario_id: int) -> Optional[dict]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def buscar_por_nombre(self, nombre: str) -> Optional[dict]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nombre = ?", (nombre,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def verificar_password(self, nombre: str, password: str) -> Optional[Usuario]:
        usuario = self.buscar_por_nombre(nombre)
        if usuario and usuario["password"] == self._hash_password(password):
            return Usuario(
                id=usuario["id"],
                nombre=usuario["nombre"],
                email=usuario["email"],
                foto_perfil=usuario.get("foto_perfil") or "",
            )
        return None

    def actualizar_perfil(self, usuario_id: int, nombre: str, foto_perfil: str) -> Optional[Usuario]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE usuarios SET nombre = ?, foto_perfil = ? WHERE id = ?",
            (nombre, foto_perfil, usuario_id),
        )

        if cursor.rowcount == 0:
            conn.close()
            return None

        cursor.execute("SELECT id, nombre, email, foto_perfil FROM usuarios WHERE id = ?", (usuario_id,))
        row = cursor.fetchone()
        conn.commit()
        conn.close()

        if not row:
            return None

        data = dict(row)
        return Usuario(
            id=data["id"],
            nombre=data["nombre"],
            email=data["email"],
            foto_perfil=data.get("foto_perfil") or "",
        )


usuario_repository = UsuarioRepository()
