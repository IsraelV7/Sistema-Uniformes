import os
import time
import uuid
import cv2
from ultralytics import YOLO
from dotenv import load_dotenv

from app.database import SessionLocal
from app.models.registro import RegistroDeteccion
from app.config_uniformes import UNIFORMES
from app.state import estado

load_dotenv()

CAMERA_SOURCE = os.getenv("CAMERA_SOURCE", "0")
if str(CAMERA_SOURCE).isdigit():
    CAMERA_SOURCE = int(CAMERA_SOURCE)

CONFIANZA_MINIMA = 0.5
CARPETA_CAPTURAS = "capturas"
os.makedirs(CARPETA_CAPTURAS, exist_ok=True)

_modelos_cache = {}
_modelo_personas = YOLO("yolov8n.pt")


def obtener_modelo_actual():
    tipo = estado.uniforme_actual
    ruta = UNIFORMES[tipo]["model_path"]
    if ruta not in _modelos_cache:
        if os.path.exists(ruta):
            print(f"[detector] Cargando modelo de prendas para '{tipo}': {ruta}")
            _modelos_cache[ruta] = YOLO(ruta)
        else:
            print(f"[detector] AVISO: no se encontró '{ruta}' para '{tipo}'.")
            _modelos_cache[ruta] = None
    return _modelos_cache[ruta]


def _centro_dentro_de_caja(cx, cy, caja):
    x1, y1, x2, y2 = caja
    return x1 <= cx <= x2 and y1 <= cy <= y2


class RastreadorPersonas:
    """
    Tracker simple por centroide. Asigna un ID a cada persona y lo
    conserva mientras siga apareciendo cerca de su última posición,
    para NO generar un registro nuevo en cada frame por la misma persona.
    """

    def __init__(self, distancia_maxima=90, frames_para_olvidar=40):
        self.siguiente_id = 0
        self.objetos = {}
        self.distancia_maxima = distancia_maxima
        self.frames_para_olvidar = frames_para_olvidar

    def actualizar(self, centros):
        ids_asignados = [None] * len(centros)
        disponibles = list(self.objetos.keys())

        for i, centro in enumerate(centros):
            mejor_id, mejor_distancia = None, self.distancia_maxima
            for oid in disponibles:
                cx, cy = self.objetos[oid]["centro"]
                d = ((centro[0] - cx) ** 2 + (centro[1] - cy) ** 2) ** 0.5
                if d < mejor_distancia:
                    mejor_distancia, mejor_id = d, oid

            if mejor_id is not None:
                ids_asignados[i] = mejor_id
                self.objetos[mejor_id]["centro"] = centro
                self.objetos[mejor_id]["frames_perdido"] = 0
                disponibles.remove(mejor_id)
            else:
                nuevo_id = self.siguiente_id
                self.siguiente_id += 1
                self.objetos[nuevo_id] = {
                    "centro": centro, "frames_perdido": 0,
                    "ultimo_estado": None, "ultima_alerta": 0,
                }
                ids_asignados[i] = nuevo_id

        for oid in disponibles:
            self.objetos[oid]["frames_perdido"] += 1

        for oid in [o for o, d in self.objetos.items() if d["frames_perdido"] > self.frames_para_olvidar]:
            del self.objetos[oid]

        return ids_asignados

    def debe_registrar(self, id_persona, cumple, cooldown_segundos=20):
        datos = self.objetos.get(id_persona)
        if datos is None:
            return False

        ahora = time.time()
        primera_vez = datos["ultima_alerta"] == 0
        cambio_de_estado = datos["ultimo_estado"] is not None and datos["ultimo_estado"] != cumple
        paso_cooldown = ahora - datos["ultima_alerta"] > cooldown_segundos

        datos["ultimo_estado"] = cumple

        if primera_vez or cambio_de_estado or paso_cooldown:
            datos["ultima_alerta"] = ahora
            return True
        return False


rastreador = RastreadorPersonas()


def reiniciar_rastreador():
    global rastreador
    rastreador = RastreadorPersonas()
    print("[detector] Seguimiento de personas reiniciado.")


def evaluar_personas(frame, modelo_prendas, prendas_requeridas, umbral):
    resultado_personas = _modelo_personas(frame, verbose=False, classes=[0])[0]
    resultado_prendas = modelo_prendas(frame, verbose=False)[0]

    detecciones_prendas = []
    for caja in resultado_prendas.boxes:
        nombre = modelo_prendas.names[int(caja.cls[0])]
        confianza = float(caja.conf[0])
        if confianza < CONFIANZA_MINIMA:
            continue
        x1, y1, x2, y2 = caja.xyxy[0].tolist()
        detecciones_prendas.append({"nombre": nombre.lower(), "cx": (x1 + x2) / 2, "cy": (y1 + y2) / 2})

    requeridas = set(p.lower() for p in prendas_requeridas)
    personas = []

    for caja_persona in resultado_personas.boxes:
        x1, y1, x2, y2 = caja_persona.xyxy[0].tolist()
        caja = (x1, y1, x2, y2)
        centro = ((x1 + x2) / 2, (y1 + y2) / 2)

        encontradas = {p["nombre"] for p in detecciones_prendas if _centro_dentro_de_caja(p["cx"], p["cy"], caja)}
        encontradas_relevantes = encontradas & requeridas
        faltantes = requeridas - encontradas_relevantes
        porcentaje = len(encontradas_relevantes) / len(requeridas) if requeridas else 1.0

        personas.append({
            "caja": caja,
            "centro": centro,
            "porcentaje": porcentaje,
            "cumple": porcentaje >= umbral,
            "faltantes": sorted(faltantes),
        })

    return personas


def dibujar_resultado(frame, personas, ids):
    for p, pid in zip(personas, ids):
        x1, y1, x2, y2 = [int(v) for v in p["caja"]]
        color = (0, 200, 0) if p["cumple"] else (0, 0, 230)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        etiqueta = f"ID{pid} {int(p['porcentaje']*100)}% {'OK' if p['cumple'] else 'INCOMPLETO'}"
        cv2.putText(frame, etiqueta, (x1, max(y1 - 8, 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    return frame


def guardar_capturas_y_registros(frame, personas, ids, tipo_uniforme):
    db = SessionLocal()
    try:
        for p, pid in zip(personas, ids):
            if not rastreador.debe_registrar(pid, p["cumple"]):
                continue  # misma persona, sin cambios relevantes: no se repite el registro

            ruta_imagen = None
            if not p["cumple"]:
                x1, y1, x2, y2 = [max(int(v), 0) for v in p["caja"]]
                recorte = frame[y1:y2, x1:x2]
                if recorte.size > 0:
                    nombre_archivo = f"{tipo_uniforme}_{pid}_{uuid.uuid4().hex[:8]}.jpg"
                    cv2.imwrite(os.path.join(CARPETA_CAPTURAS, nombre_archivo), recorte)
                    ruta_imagen = f"capturas/{nombre_archivo}"

            db.add(RegistroDeteccion(
                clase_detectada="persona",
                confianza=p["porcentaje"],
                cumple_normativa="correcto" if p["cumple"] else "incorrecto",
                camara_origen=f"camara_{CAMERA_SOURCE}",
                tipo_uniforme=tipo_uniforme,
                porcentaje_cumplimiento=round(p["porcentaje"] * 100, 1),
                prendas_faltantes=", ".join(p["faltantes"]) if p["faltantes"] else None,
                imagen_path=ruta_imagen,
            ))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"[detector] Error guardando evaluación: {e}")
    finally:
        db.close()


def generar_frames():
    cap = None
    try:
        while estado.activo:
            if cap is None:
                if isinstance(CAMERA_SOURCE, int):
                    cap = cv2.VideoCapture(CAMERA_SOURCE, cv2.CAP_DSHOW)
                else:
                    cap = cv2.VideoCapture(CAMERA_SOURCE)
                if not cap.isOpened():
                    print(f"[detector] No se pudo abrir la fuente de video: {CAMERA_SOURCE}")
                    estado.activo = False
                    break

            ret, frame = cap.read()
            if not ret:
                break

            tipo = estado.uniforme_actual
            config_tipo = UNIFORMES[tipo]
            modelo_prendas = obtener_modelo_actual()

            if modelo_prendas is not None:
                personas = evaluar_personas(
                    frame, modelo_prendas,
                    config_tipo["prendas_requeridas"],
                    config_tipo.get("umbral_cumplimiento", 0.8),
                )
                ids = rastreador.actualizar([p["centro"] for p in personas])
                guardar_capturas_y_registros(frame, personas, ids, tipo)
                frame = dibujar_resultado(frame, personas, ids)
            else:
                cv2.putText(frame, f"Sin modelo entrenado para '{tipo}'", (20, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 230), 2)

            ok, buffer = cv2.imencode(".jpg", frame)
            if not ok:
                continue

            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")
    finally:
        if cap is not None:
            cap.release()
            print("[detector] Cámara liberada.")