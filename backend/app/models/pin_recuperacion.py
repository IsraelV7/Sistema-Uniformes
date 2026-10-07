from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from app.database import Base


class PinRecuperacion(Base):
    __tablename__ = "pines_recuperacion"

    id = Column(Integer, primary_key=True, index=True)
    correo = Column(String, nullable=False, index=True)
    pin = Column(String, nullable=False)
    expira = Column(DateTime, nullable=False)
    usado = Column(Boolean, default=False)
    creado = Column(DateTime, default=datetime.utcnow)