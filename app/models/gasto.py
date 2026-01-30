from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class GastoBase(BaseModel):
    monto: float = Field(..., gt=0)
    descripcion: str = Field(..., min_length=1)
    quien_pago: str = Field(..., min_length=1)


class GastoCreate(GastoBase):
    pass


class GastoUpdate(BaseModel):
    monto: Optional[float] = Field(None, gt=0)
    descripcion: Optional[str] = Field(None, min_length=1)
    quien_pago: Optional[str] = Field(None, min_length=1)


class Gasto(GastoBase):
    id: int
    fecha: datetime

    class Config:
        from_attributes = True


class ResumenDeuda(BaseModel):
    persona: str
    debe: float
    descripcion: str
