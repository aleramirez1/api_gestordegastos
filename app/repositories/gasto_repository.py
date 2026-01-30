from typing import List, Optional
from app.models import Gasto, GastoCreate, GastoUpdate
from datetime import datetime


class GastoRepository:
    def __init__(self):
        self.gastos: List[Gasto] = []
        self.next_id: int = 1

    def crear(self, gasto: GastoCreate) -> Gasto:
        nuevo_gasto = Gasto(
            id=self.next_id,
            monto=gasto.monto,
            descripcion=gasto.descripcion,
            quien_pago=gasto.quien_pago,
            fecha=datetime.now()
        )
        self.gastos.append(nuevo_gasto)
        self.next_id += 1
        return nuevo_gasto

    def obtener_todos(self) -> List[Gasto]:
        return self.gastos

    def obtener_por_id(self, gasto_id: int) -> Optional[Gasto]:
        for gasto in self.gastos:
            if gasto.id == gasto_id:
                return gasto
        return None

    def actualizar(self, gasto_id: int, gasto_update: GastoUpdate) -> Optional[Gasto]:
        gasto = self.obtener_por_id(gasto_id)
        if not gasto:
            return None
        
        if gasto_update.monto is not None:
            gasto.monto = gasto_update.monto
        if gasto_update.descripcion is not None:
            gasto.descripcion = gasto_update.descripcion
        if gasto_update.quien_pago is not None:
            gasto.quien_pago = gasto_update.quien_pago
        
        return gasto

    def eliminar(self, gasto_id: int) -> bool:
        gasto = self.obtener_por_id(gasto_id)
        if gasto:
            self.gastos.remove(gasto)
            return True
        return False


gasto_repository = GastoRepository()
