from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.auth import CrearUsuario, UsuarioOut
from app.services.seguridad import hash_password
from app.dependencies import requerir_superusuario

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/", response_model=UsuarioOut)
def crear_usuario(
    datos: CrearUsuario,
    db: Session = Depends(get_db),
    _: Usuario = Depends(requerir_superusuario),  # SOLO un superusuario puede crear usuarios
):
    existe = db.query(Usuario).filter(
        (Usuario.nombre_usuario == datos.nombre_usuario) | (Usuario.correo == datos.correo)
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese nombre o correo")

    nuevo = Usuario(
        nombre_usuario=datos.nombre_usuario,
        correo=datos.correo,
        password_hash=hash_password(datos.password),
        es_superusuario=datos.es_superusuario,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo