import random
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.models.pin_recuperacion import PinRecuperacion
from app.schemas.auth import (
    LoginRequest, TokenResponse, SolicitarRecuperacion,
    VerificarPin, ResetearPassword,
)
from app.services.seguridad import verificar_password, crear_token, hash_password
from app.services.correo import enviar_pin

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=TokenResponse)
def login(datos: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.nombre_usuario == datos.nombre_usuario).first()

    if not usuario or not verificar_password(datos.password, usuario.password_hash):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    token = crear_token({"sub": usuario.nombre_usuario})
    return TokenResponse(
        access_token=token,
        es_superusuario=usuario.es_superusuario,
        nombre_usuario=usuario.nombre_usuario,
    )


@router.post("/recuperar")
def solicitar_recuperacion(datos: SolicitarRecuperacion, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.correo == datos.correo).first()
    if not usuario:
        return {"mensaje": "Si el correo existe, se envió un código de verificación"}

    pin = f"{random.randint(0, 999999):06d}"
    registro = PinRecuperacion(
        correo=datos.correo,
        pin=pin,
        expira=datetime.utcnow() + timedelta(minutes=10),
    )
    db.add(registro)
    db.commit()

    try:
        enviar_pin(datos.correo, pin)
    except Exception as e:
        print(f"[auth] Error enviando correo: {e}")
        raise HTTPException(status_code=500, detail="No se pudo enviar el correo. Revisa la configuración SMTP.")

    return {"mensaje": "Si el correo existe, se envió un código de verificación"}


@router.post("/verificar-pin")
def verificar_pin(datos: VerificarPin, db: Session = Depends(get_db)):
    registro = (
        db.query(PinRecuperacion)
        .filter(PinRecuperacion.correo == datos.correo, PinRecuperacion.pin == datos.pin, PinRecuperacion.usado == False)
        .order_by(PinRecuperacion.creado.desc())
        .first()
    )
    if not registro or registro.expira < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Código inválido o expirado")
    return {"valido": True}


@router.post("/resetear-password")
def resetear_password(datos: ResetearPassword, db: Session = Depends(get_db)):
    registro = (
        db.query(PinRecuperacion)
        .filter(PinRecuperacion.correo == datos.correo, PinRecuperacion.pin == datos.pin, PinRecuperacion.usado == False)
        .order_by(PinRecuperacion.creado.desc())
        .first()
    )
    if not registro or registro.expira < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Código inválido o expirado")

    usuario = db.query(Usuario).filter(Usuario.correo == datos.correo).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.password_hash = hash_password(datos.nueva_password)
    registro.usado = True
    db.commit()

    return {"mensaje": "Contraseña actualizada correctamente"}