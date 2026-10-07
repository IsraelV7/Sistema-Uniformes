from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.auth import CrearUsuario, UsuarioOut
from app.services.seguridad import hash_password
# Ya no necesitamos importar requerir_superusuario aquí

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/", response_model=UsuarioOut)
def crear_usuario(
    datos: CrearUsuario,
    db: Session = Depends(get_db)
    # ELIMINAMOS la dependencia de superusuario
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
        es_superusuario=False, # ¡IMPORTANTE! Forzamos a que sea False
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo