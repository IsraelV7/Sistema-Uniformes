from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class RegistroDeteccionOut(BaseModel):
    id: int
    clase_detectada: str
    confianza: float
    cumple_normativa: str
    fecha_hora: datetime
    camara_origen: str
    tipo_uniforme: str
    porcentaje_cumplimiento: Optional[float] = None
    prendas_faltantes: Optional[str] = None
    imagen_path: Optional[str] = None

    class Config:
        from_attributes = True