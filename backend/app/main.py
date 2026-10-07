from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.models import registro, usuario, pin_recuperacion
from app.routers import deteccion, reportes, config, auth, usuarios

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Monitoreo de Uniformes")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(deteccion.router)
app.include_router(reportes.router)
app.include_router(config.router)

app.mount("/capturas", StaticFiles(directory="capturas"), name="capturas")


@app.get("/")
def raiz():
    return {"mensaje": "Sistema de Monitoreo de Uniformes - API activa"}