from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.registro import RegistroDeteccion
from app.schemas.deteccion import RegistroDeteccionOut
from app.dependencies import obtener_usuario_actual
from app.models.usuario import Usuario

router = APIRouter(prefix="/reportes", tags=["Reportes"])


@router.get("/", response_model=List[RegistroDeteccionOut])
def listar_registros(
    tipo_uniforme: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(RegistroDeteccion)
    if tipo_uniforme:
        query = query.filter(RegistroDeteccion.tipo_uniforme == tipo_uniforme)
    return query.order_by(RegistroDeteccion.fecha_hora.desc()).limit(100).all()


@router.delete("/")
def limpiar_historial(db: Session = Depends(get_db), _: Usuario = Depends(obtener_usuario_actual)):
    db.query(RegistroDeteccion).delete()
    db.commit()
    return {"mensaje": "Historial eliminado"}