from typing import Optional, List
from app.models.grupo import Grupo, GrupoCreate, GrupoUpdate, GastoGrupo, GastoCreate
from app.database import get_connection


class GrupoRepository:
    def _row_to_grupo(self, g: dict, cursor) -> Grupo:
        cursor.execute("SELECT nombre FROM personas_grupo WHERE grupo_id = ?", (g["id"],))
        personas = [r["nombre"] for r in cursor.fetchall()]
        cursor.execute("SELECT * FROM gastos WHERE grupo_id = ?", (g["id"],))
        gastos = [
            GastoGrupo(
                id=ga["id"], persona=ga["persona"], monto=float(ga["monto"]),
                descripcion=ga["descripcion"] or "", tipo=ga["tipo"], fecha=ga["fecha"]
            )
            for ga in cursor.fetchall()
        ]
        return Grupo(
            id=g["id"], nombre=g["nombre"], usuario_id=g["usuario_id"],
            fecha_creacion=g["fecha_creacion"], personas=personas, gastos=gastos
        )

    def crear(self, grupo: GrupoCreate) -> Grupo:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO grupos (nombre, usuario_id) VALUES (?, ?)", (grupo.nombre, grupo.usuario_id))
        grupo_id = cursor.lastrowid
        for persona in grupo.personas:
            cursor.execute("INSERT INTO personas_grupo (grupo_id, nombre) VALUES (?, ?)", (grupo_id, persona))
        conn.commit()
        conn.close()
        return self.obtener_por_id(grupo_id)

    def obtener_por_usuario(self, usuario_id: int) -> List[Grupo]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM grupos WHERE usuario_id = ?", (usuario_id,))
        grupos_data = [dict(r) for r in cursor.fetchall()]
        grupos = [self._row_to_grupo(g, cursor) for g in grupos_data]
        conn.close()
        return grupos

    def obtener_por_id(self, grupo_id: int) -> Optional[Grupo]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM grupos WHERE id = ?", (grupo_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return None
        grupo = self._row_to_grupo(dict(row), cursor)
        conn.close()
        return grupo

    def actualizar(self, grupo_id: int, grupo_update: GrupoUpdate) -> Optional[Grupo]:
        conn = get_connection()
        cursor = conn.cursor()
        if grupo_update.nombre:
            cursor.execute("UPDATE grupos SET nombre = ? WHERE id = ?", (grupo_update.nombre, grupo_id))
        if grupo_update.personas is not None:
            cursor.execute("DELETE FROM personas_grupo WHERE grupo_id = ?", (grupo_id,))
            for persona in grupo_update.personas:
                cursor.execute("INSERT INTO personas_grupo (grupo_id, nombre) VALUES (?, ?)", (grupo_id, persona))
        conn.commit()
        conn.close()
        return self.obtener_por_id(grupo_id)

    def eliminar(self, grupo_id: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM grupos WHERE id = ?", (grupo_id,))
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        return affected > 0

    def agregar_persona(self, grupo_id: int, persona: str) -> Optional[Grupo]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO personas_grupo (grupo_id, nombre) VALUES (?, ?)", (grupo_id, persona))
        conn.commit()
        conn.close()
        return self.obtener_por_id(grupo_id)

    def eliminar_persona(self, grupo_id: int, persona: str) -> Optional[Grupo]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM personas_grupo WHERE grupo_id = ? AND nombre = ?", (grupo_id, persona))
        conn.commit()
        conn.close()
        return self.obtener_por_id(grupo_id)

    def agregar_gasto(self, grupo_id: int, gasto: GastoCreate) -> Optional[Grupo]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO gastos (grupo_id, persona, monto, descripcion, tipo) VALUES (?, ?, ?, ?, ?)",
            (grupo_id, gasto.persona, gasto.monto, gasto.descripcion, gasto.tipo)
        )
        conn.commit()
        conn.close()
        return self.obtener_por_id(grupo_id)

    def eliminar_gasto(self, grupo_id: int, gasto_id: int) -> Optional[Grupo]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM gastos WHERE id = ? AND grupo_id = ?", (gasto_id, grupo_id))
        conn.commit()
        conn.close()
        return self.obtener_por_id(grupo_id)

    def editar_gasto(self, grupo_id: int, gasto_id: int, nuevo_monto: float) -> Optional[Grupo]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE gastos SET monto = ? WHERE id = ? AND grupo_id = ?", (nuevo_monto, gasto_id, grupo_id))
        conn.commit()
        conn.close()
        return self.obtener_por_id(grupo_id)


grupo_repository = GrupoRepository()
