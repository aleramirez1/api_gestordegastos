from typing import List, Dict, Optional
from app.models import Gasto, GastoCreate, GastoUpdate, ResumenDeuda
from app.repositories import GastoRepository
from collections import defaultdict


class GastoService:
    def __init__(self, repository: GastoRepository):
        self.repository = repository

    def crear_gasto(self, gasto: GastoCreate) -> Gasto:
        return self.repository.crear(gasto)

    def obtener_gastos(self) -> List[Gasto]:
        return self.repository.obtener_todos()

    def obtener_gasto_por_id(self, gasto_id: int) -> Optional[Gasto]:
        return self.repository.obtener_por_id(gasto_id)

    def actualizar_gasto(self, gasto_id: int, gasto_update: GastoUpdate) -> Optional[Gasto]:
        return self.repository.actualizar(gasto_id, gasto_update)

    def eliminar_gasto(self, gasto_id: int) -> bool:
        return self.repository.eliminar(gasto_id)

    def calcular_resumen_deudas(self) -> Dict:
        gastos = self.repository.obtener_todos()
        
        if not gastos:
            return {
                "total_gastado": 0,
                "monto_por_persona": 0,
                "num_personas": 0,
                "personas": [],
                "deudas": []
            }
        
        total_gastado = sum(gasto.monto for gasto in gastos)
        
        deudas = []
        for gasto in gastos:
            if gasto.tipo == "te_deben":
                deudas.append(ResumenDeuda(
                    persona=gasto.quien_pago,
                    debe=gasto.monto,
                    descripcion=f"{gasto.quien_pago} te debe ${gasto.monto:.2f}"
                ))
            else:
                deudas.append(ResumenDeuda(
                    persona=gasto.quien_pago,
                    debe=gasto.monto,
                    descripcion=f"Tu debes a {gasto.quien_pago} ${gasto.monto:.2f}"
                ))
        
        return {
            "total_gastado": round(total_gastado, 2),
            "monto_por_persona": 0,
            "num_personas": len(set(g.quien_pago for g in gastos)),
            "personas": list(set(g.quien_pago for g in gastos)),
            "deudas": deudas
        }
