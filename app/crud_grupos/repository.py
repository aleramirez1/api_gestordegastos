from typing import Optional, List
from datetime import datetime
import random
import json
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

        personas_ya_recibieron = []
        raw_personas_ya_recibieron = g.get("personas_ya_recibieron")
        if raw_personas_ya_recibieron:
            try:
                parsed = json.loads(raw_personas_ya_recibieron)
                if isinstance(parsed, list):
                    personas_ya_recibieron = [str(nombre) for nombre in parsed]
            except (TypeError, ValueError):
                personas_ya_recibieron = []

        return Grupo(
            id=g["id"], nombre=g["nombre"], usuario_id=g["usuario_id"],
            fecha_creacion=g["fecha_creacion"],
            personas=personas,
            is_ahorro=bool(g.get("is_ahorro", 0)),
            meta_ahorro=float(g.get("meta_ahorro", 0.0) or 0.0),
            personas_ya_recibieron=personas_ya_recibieron,
            gastos=gastos,
        )

    def crear(self, grupo: GrupoCreate) -> Grupo:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO grupos (nombre, usuario_id, is_ahorro, meta_ahorro, personas_ya_recibieron)
            VALUES (?, ?, ?, ?, ?)
            """,
            (grupo.nombre, grupo.usuario_id, int(grupo.is_ahorro), grupo.meta_ahorro, json.dumps([])),
        )
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

    def obtener_todos(self) -> List[Grupo]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM grupos")
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
        if grupo_update.is_ahorro is not None:
            cursor.execute("UPDATE grupos SET is_ahorro = ? WHERE id = ?", (int(grupo_update.is_ahorro), grupo_id))
        if grupo_update.meta_ahorro is not None:
            cursor.execute("UPDATE grupos SET meta_ahorro = ? WHERE id = ?", (grupo_update.meta_ahorro, grupo_id))
        if grupo_update.personas_ya_recibieron is not None:
            cursor.execute(
                "UPDATE grupos SET personas_ya_recibieron = ? WHERE id = ?",
                (json.dumps(grupo_update.personas_ya_recibieron), grupo_id),
            )
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

    def calcular_probabilidades_pago_mes(
        self,
        grupo_id: int,
        anio: Optional[int] = None,
        mes: Optional[int] = None,
        suavizado: float = 0.05,
    ) -> dict:
        fecha_actual = datetime.now()
        anio_objetivo = anio or fecha_actual.year
        mes_objetivo = mes or fecha_actual.month
        periodo = f"{anio_objetivo:04d}-{mes_objetivo:02d}"

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT nombre FROM personas_grupo WHERE grupo_id = ?", (grupo_id,))
        personas = [row["nombre"] for row in cursor.fetchall()]

        if not personas:
            conn.close()
            return {"anio": anio_objetivo, "mes": mes_objetivo, "probabilidades": []}

        totales_por_persona = {persona: 0.0 for persona in personas}

        cursor.execute(
            """
            SELECT persona, COALESCE(SUM(monto), 0) as total_pagado
            FROM gastos
            WHERE grupo_id = ?
              AND strftime('%Y-%m', fecha) = ?
            GROUP BY persona
            """,
            (grupo_id, periodo),
        )

        for row in cursor.fetchall():
            persona = row["persona"]
            if persona in totales_por_persona:
                totales_por_persona[persona] = float(row["total_pagado"] or 0.0)

        conn.close()

        total_pagado_mes = sum(totales_por_persona.values())
        objetivo_equilibrado = total_pagado_mes / len(personas) if personas else 0.0

        detalles = []
        for persona in personas:
            pagado = totales_por_persona[persona]
            deficit = max(objetivo_equilibrado - pagado, 0.0)
            peso = deficit + suavizado
            detalles.append({"persona": persona, "pagado_mes": round(pagado, 2), "peso": peso})

        suma_pesos = sum(item["peso"] for item in detalles)
        if suma_pesos <= 0:
            prob_uniforme = 1 / len(detalles)
            for item in detalles:
                item["probabilidad"] = prob_uniforme
        else:
            for item in detalles:
                item["probabilidad"] = item["peso"] / suma_pesos

        return {"anio": anio_objetivo, "mes": mes_objetivo, "probabilidades": detalles}

    def seleccionar_pagador_weighted(
        self,
        grupo_id: int,
        anio: Optional[int] = None,
        mes: Optional[int] = None,
        suavizado: float = 0.05,
    ) -> Optional[dict]:
        resultado = self.calcular_probabilidades_pago_mes(
            grupo_id=grupo_id,
            anio=anio,
            mes=mes,
            suavizado=suavizado,
        )
        probabilidades = resultado["probabilidades"]

        if not probabilidades:
            return None

        personas = [item["persona"] for item in probabilidades]
        pesos = [item["peso"] for item in probabilidades]
        persona_seleccionada = random.choices(personas, weights=pesos, k=1)[0]

        return {
            "persona_seleccionada": persona_seleccionada,
            "anio": resultado["anio"],
            "mes": resultado["mes"],
            "probabilidades": probabilidades,
        }


grupo_repository = GrupoRepository()
