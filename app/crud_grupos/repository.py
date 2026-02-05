from typing import Optional, List
from app.models.grupo import Grupo, GrupoCreate, GrupoUpdate, GastoGrupo, GastoCreate
from app.database import get_connection
from datetime import datetime


class GrupoRepository:
    def crear(self, grupo: GrupoCreate) -> Grupo:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO grupos (nombre) VALUES (%s)", (grupo.nombre,))
        grupo_id = cursor.lastrowid
        for persona in grupo.personas:
            cursor.execute("INSERT INTO personas_grupo (grupo_id, nombre) VALUES (%s, %s)", (grupo_id, persona))
        conn.commit()
        cursor.close()
        conn.close()
        return self.obtener_por_id(grupo_id)

    def obtener_todos(self) -> List[Grupo]:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM grupos")
        grupos_data = cursor.fetchall()
        grupos = []
        for g in grupos_data:
            cursor.execute("SELECT nombre FROM personas_grupo WHERE grupo_id = %s", (g["id"],))
            personas = [p["nombre"] for p in cursor.fetchall()]
            cursor.execute("SELECT * FROM gastos WHERE grupo_id = %s", (g["id"],))
            gastos = [GastoGrupo(id=ga["id"], persona=ga["persona"], monto=float(ga["monto"]), descripcion=ga["descripcion"] or "", tipo=ga["tipo"], fecha=ga["fecha"]) for ga in cursor.fetchall()]
            grupos.append(Grupo(id=g["id"], nombre=g["nombre"], fecha_creacion=g["fecha_creacion"], personas=personas, gastos=gastos))
        cursor.close()
        conn.close()
        return grupos

    def obtener_por_id(self, grupo_id: int) -> Optional[Grupo]:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM grupos WHERE id = %s", (grupo_id,))
        g = cursor.fetchone()
        if not g:
            cursor.close()
            conn.close()
            return None
        cursor.execute("SELECT nombre FROM personas_grupo WHERE grupo_id = %s", (grupo_id,))
        personas = [p["nombre"] for p in cursor.fetchall()]
        cursor.execute("SELECT * FROM gastos WHERE grupo_id = %s", (grupo_id,))
        gastos = [GastoGrupo(id=ga["id"], persona=ga["persona"], monto=float(ga["monto"]), descripcion=ga["descripcion"] or "", tipo=ga["tipo"], fecha=ga["fecha"]) for ga in cursor.fetchall()]
        cursor.close()
        conn.close()
        return Grupo(id=g["id"], nombre=g["nombre"], fecha_creacion=g["fecha_creacion"], personas=personas, gastos=gastos)

    def actualizar(self, grupo_id: int, grupo_update: GrupoUpdate) -> Optional[Grupo]:
        conn = get_connection()
        cursor = conn.cursor()
        if grupo_update.nombre:
            cursor.execute("UPDATE grupos SET nombre = %s WHERE id = %s", (grupo_update.nombre, grupo_id))
        if grupo_update.personas is not None:
            cursor.execute("DELETE FROM personas_grupo WHERE grupo_id = %s", (grupo_id,))
            for persona in grupo_update.personas:
                cursor.execute("INSERT INTO personas_grupo (grupo_id, nombre) VALUES (%s, %s)", (grupo_id, persona))
        conn.commit()
        cursor.close()
        conn.close()
        return self.obtener_por_id(grupo_id)

    def eliminar(self, grupo_id: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM grupos WHERE id = %s", (grupo_id,))
        affected = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return affected > 0

    def agregar_persona(self, grupo_id: int, persona: str) -> Optional[Grupo]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO personas_grupo (grupo_id, nombre) VALUES (%s, %s)", (grupo_id, persona))
        conn.commit()
        cursor.close()
        conn.close()
        return self.obtener_por_id(grupo_id)

    def eliminar_persona(self, grupo_id: int, persona: str) -> Optional[Grupo]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM personas_grupo WHERE grupo_id = %s AND nombre = %s", (grupo_id, persona))
        conn.commit()
        cursor.close()
        conn.close()
        return self.obtener_por_id(grupo_id)

    def agregar_gasto(self, grupo_id: int, gasto: GastoCreate) -> Optional[Grupo]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO gastos (grupo_id, persona, monto, descripcion, tipo) VALUES (%s, %s, %s, %s, %s)", (grupo_id, gasto.persona, gasto.monto, gasto.descripcion, gasto.tipo))
        conn.commit()
        cursor.close()
        conn.close()
        return self.obtener_por_id(grupo_id)

    def eliminar_gasto(self, grupo_id: int, gasto_id: int) -> Optional[Grupo]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM gastos WHERE id = %s AND grupo_id = %s", (gasto_id, grupo_id))
        conn.commit()
        cursor.close()
        conn.close()
        return self.obtener_por_id(grupo_id)


grupo_repository = GrupoRepository()
