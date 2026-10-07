from pydantic import BaseModel, EmailStr
from typing import Optional


class LoginRequest(BaseModel):
    nombre_usuario: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    es_superusuario: bool
    nombre_usuario: str


class SolicitarRecuperacion(BaseModel):
    correo: EmailStr


class VerificarPin(BaseModel):
    correo: EmailStr
    pin: str


class ResetearPassword(BaseModel):
    correo: EmailStr
    pin: str
    nueva_password: str


class CrearUsuario(BaseModel):
    nombre_usuario: str
    correo: EmailStr
    password: str
    es_superusuario: Optional[bool] = False


class UsuarioOut(BaseModel):
    id: int
    nombre_usuario: str
    correo: EmailStr
    es_superusuario: bool

    class Config:
        from_attributes = True