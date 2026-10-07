"""
Script de un solo uso para crear el primer superusuario.
Correr desde backend/ con el entorno virtual activado:
    python crear_superusuario.py
"""

from app.database import SessionLocal, Base, engine
from app.models.usuario import Usuario
from app.services.seguridad import hash_password

Base.metadata.create_all(bind=engine)
db = SessionLocal()

print("=== Crear superusuario ===")
nombre_usuario = input("Nombre de usuario: ").strip()
correo = input("Correo electrónico: ").strip()
password = input("Contraseña: ").strip()

if db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first():
    print("Ya existe un usuario con ese nombre.")
else:
    db.add(Usuario(
        nombre_usuario=nombre_usuario,
        correo=correo,
        password_hash=hash_password(password),
        es_superusuario=True,
    ))
    db.commit()
    print(f"Superusuario '{nombre_usuario}' creado correctamente.")

db.close()