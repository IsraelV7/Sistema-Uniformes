from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.config_uniformes import UNIFORMES
from app.state import estado

router = APIRouter(prefix="/config", tags=["Configuración"])


class SeleccionUniforme(BaseModel):
    tipo: str


@router.get("/uniformes")
def listar_uniformes():
    """Devuelve la lista de uniformes disponibles para el selector del frontend."""
    return [
        {"id": clave, "nombre": datos["nombre"]}
        for clave, datos in UNIFORMES.items()
    ]


@router.post("/uniformes/seleccionar")
def seleccionar_uniforme(seleccion: SeleccionUniforme):
    if seleccion.tipo not in UNIFORMES:
        raise HTTPException(status_code=400, detail="Tipo de uniforme no reconocido")

    estado.uniforme_actual = seleccion.tipo
    return {"uniforme_actual": estado.uniforme_actual}