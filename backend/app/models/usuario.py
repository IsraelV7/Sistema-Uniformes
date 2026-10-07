from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String, unique=True, nullable=False, index=True)
    correo = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    es_superusuario = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)