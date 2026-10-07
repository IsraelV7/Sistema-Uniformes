import os
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "cambia_esto")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
EXPIRE_MINUTOS = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verificar_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def crear_token(datos: dict) -> str:
    datos_copia = datos.copy()
    datos_copia["exp"] = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTOS)
    return jwt.encode(datos_copia, SECRET_KEY, algorithm=ALGORITHM)


def decodificar_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None