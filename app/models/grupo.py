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
    is_ahorro: bool = False
    meta_ahorro: float = 0.0


class GrupoCreate(GrupoBase):
    usuario_id: int


class GrupoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1)
    personas: Optional[List[str]] = None
    personas_ya_recibieron: Optional[List[str]] = None
    is_ahorro: Optional[bool] = None
    meta_ahorro: Optional[float] = None


class GastoCreate(BaseModel):
    persona: str
    monto: float
    descripcion: str = ""
    tipo: str = "te_deben"


class GastoEdit(BaseModel):
    monto: float


class RuletaWeightedRequest(BaseModel):
    monto: float = Field(..., gt=0)
    anio: Optional[int] = Field(None, ge=2000, le=2100)
    mes: Optional[int] = Field(None, ge=1, le=12)
    suavizado: float = Field(0.05, gt=0)


class ProbabilidadPersona(BaseModel):
    persona: str
    pagado_mes: float
    peso: float
    probabilidad: float


class RuletaWeightedResult(BaseModel):
    persona_seleccionada: str
    anio: int
    mes: int
    monto_referencia: float
    probabilidades: List[ProbabilidadPersona]


class Grupo(GrupoBase):
    id: int
    usuario_id: int
    fecha_creacion: datetime
    personas_ya_recibieron: List[str] = []
    gastos: List[GastoGrupo] = []

    class Config:
        from_attributes = True
