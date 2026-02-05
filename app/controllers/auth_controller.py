from fastapi import APIRouter, HTTPException, status
from app.models.usuario import UsuarioCreate, UsuarioLogin, UsuarioResponse
from app.services.auth_service import AuthService
from app.repositories.usuario_repository import usuario_repository

router = APIRouter(prefix="/auth", tags=["Autenticacion"])

auth_service = AuthService(usuario_repository)


@router.post("/registro", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar(usuario: UsuarioCreate):
    resultado = auth_service.registrar(usuario)
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre ya esta registrado"
        )
    return resultado


@router.post("/login", response_model=UsuarioResponse)
def login(credenciales: UsuarioLogin):
    resultado = auth_service.login(credenciales.nombre, credenciales.password)
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas"
        )
    return resultado
