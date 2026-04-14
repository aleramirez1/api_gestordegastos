from pydantic import BaseModel, Field


class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=2)
    email: str = Field(..., min_length=5)


class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=4)


class UsuarioLogin(BaseModel):
    nombre: str
    password: str


class Usuario(UsuarioBase):
    id: int
    foto_perfil: str = ""

    class Config:
        from_attributes = True


class UsuarioResponse(UsuarioBase):
    id: int
    foto_perfil: str = ""
    token: str


class UsuarioPerfilUpdate(BaseModel):
    nombre: str = Field(..., min_length=2)
    foto_perfil: str = ""
