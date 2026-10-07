from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.database import Base


class RegistroDeteccion(Base):
    __tablename__ = "registros_deteccion"

    id = Column(Integer, primary_key=True, index=True)
    clase_detectada = Column(String, nullable=False)
    confianza = Column(Float, nullable=False)
    cumple_normativa = Column(String, nullable=False)
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    camara_origen = Column(String, default="laptop")
    tipo_uniforme = Column(String, default="traje")
    porcentaje_cumplimiento = Column(Float, nullable=True)
    prendas_faltantes = Column(String, nullable=True)
    imagen_path = Column(String, nullable=True)   # NUEVO: evidencia fotográfica