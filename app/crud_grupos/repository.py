from typing import Optional, List
from app.models.grupo import Grupo, GrupoCreate, GrupoUpdate, GastoGrupo, GastoCreate
from datetime import datetime


class GrupoRepository:
    def __init__(self):
        self._grupos: List[dict] = []
        self._counter = 0
        self._gasto_counter = 0

    def crear(self, grupo: GrupoCreate) -> Grupo:
        self._counter += 1
        nuevo = {
            "id": self._counter,
            "nombre": grupo.nombre,
            "personas": grupo.personas,
            "fecha_creacion": datetime.now(),
            "gastos": []
        }
        self._grupos.append(nuevo)
        return Grupo(**nuevo)

    def obtener_todos(self) -> List[Grupo]:
        return [Grupo(**g) for g in self._grupos]

    def obtener_por_id(self, grupo_id: int) -> Optional[Grupo]:
        for g in self._grupos:
            if g["id"] == grupo_id:
                return Grupo(**g)
        return None

    def actualizar(self, grupo_id: int, grupo_update: GrupoUpdate) -> Optional[Grupo]:
        for g in self._grupos:
            if g["id"] == grupo_id:
                if grupo_update.nombre is not None:
                    g["nombre"] = grupo_update.nombre
                if grupo_update.personas is not None:
                    g["personas"] = grupo_update.personas
                return Grupo(**g)
        return None

    def eliminar(self, grupo_id: int) -> bool:
        for i, g in enumerate(self._grupos):
            if g["id"] == grupo_id:
                self._grupos.pop(i)
                return True
        return False

    def agregar_persona(self, grupo_id: int, persona: str) -> Optional[Grupo]:
        for g in self._grupos:
            if g["id"] == grupo_id:
                if persona not in g["personas"]:
                    g["personas"].append(persona)
                return Grupo(**g)
        return None

    def eliminar_persona(self, grupo_id: int, persona: str) -> Optional[Grupo]:
        for g in self._grupos:
            if g["id"] == grupo_id:
                if persona in g["personas"]:
                    g["personas"].remove(persona)
                return Grupo(**g)
        return None

    def agregar_gasto(self, grupo_id: int, gasto: GastoCreate) -> Optional[Grupo]:
        for g in self._grupos:
            if g["id"] == grupo_id:
                self._gasto_counter += 1
                nuevo_gasto = {
                    "id": self._gasto_counter,
                    "persona": gasto.persona,
                    "monto": gasto.monto,
                    "descripcion": gasto.descripcion,
                    "tipo": gasto.tipo,
                    "fecha": datetime.now()
                }
                g["gastos"].append(nuevo_gasto)
                return Grupo(**g)
        return None

    def eliminar_gasto(self, grupo_id: int, gasto_id: int) -> Optional[Grupo]:
        for g in self._grupos:
            if g["id"] == grupo_id:
                for i, gasto in enumerate(g["gastos"]):
                    if gasto["id"] == gasto_id:
                        g["gastos"].pop(i)
                        return Grupo(**g)
        return None


grupo_repository = GrupoRepository()
