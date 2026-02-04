from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class GastoGrupo(BaseModel):
    id: int
    persona: str
    monto: float
    descripcion: str
    tipo: str
    fecha: datetime


class GrupoBase(BaseModel):
    nombre: str = Field(..., min_length=1)
    personas: List[str] = Field(default=[])


class GrupoCreate(GrupoBase):
    pass


class GrupoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1)
    personas: Optional[List[str]] = None


class GastoCreate(BaseModel):
    persona: str
    monto: float
    descripcion: str = ""
    tipo: str = "te_deben"


class Grupo(GrupoBase):
    id: int
    fecha_creacion: datetime
    gastos: List[GastoGrupo] = []

    class Config:
        from_attributes = True
