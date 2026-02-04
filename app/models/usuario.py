from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=2)
    email: str = Field(..., min_length=5)


class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=4)


class UsuarioLogin(BaseModel):
    email: str
    password: str


class Usuario(UsuarioBase):
    id: int

    class Config:
        from_attributes = True


class UsuarioResponse(UsuarioBase):
    id: int
    token: str
