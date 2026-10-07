from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.services.seguridad import decodificar_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def obtener_usuario_actual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
    error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    datos = decodificar_token(token)
    if datos is None:
        raise error

    usuario = db.query(Usuario).filter(Usuario.nombre_usuario == datos.get("sub")).first()
    if usuario is None:
        raise error
    return usuario


def requerir_superusuario(usuario: Usuario = Depends(obtener_usuario_actual)) -> Usuario:
    if not usuario.es_superusuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Se requiere ser superusuario")
    return usuario