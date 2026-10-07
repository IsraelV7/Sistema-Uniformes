from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.services import detector as detector_service
from app.state import estado
from app.dependencies import obtener_usuario_actual
from app.models.usuario import Usuario

router = APIRouter(prefix="/deteccion", tags=["Detección"])


@router.get("/stream")
def video_stream():
    return StreamingResponse(
        detector_service.generar_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


@router.post("/iniciar")
def iniciar_monitoreo():
    estado.activo = True
    return {"activo": estado.activo}


@router.post("/detener")
def detener_monitoreo():
    estado.activo = False
    return {"activo": estado.activo}


@router.get("/estado")
def obtener_estado():
    return {"activo": estado.activo, "uniforme_actual": estado.uniforme_actual}


@router.post("/reiniciar-seguimiento")
def reiniciar_seguimiento(_: Usuario = Depends(obtener_usuario_actual)):
    detector_service.reiniciar_rastreador()
    return {"mensaje": "Seguimiento reiniciado"}