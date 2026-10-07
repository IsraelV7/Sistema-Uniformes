"""
config_uniformes.py
---------------------
Define, por cada uniforme, qué prendas son obligatorias (deben
coincidir en minúsculas con los nombres de clase que usaste en
Roboflow) y qué porcentaje mínimo de esas prendas debe detectarse
en una persona para considerarla "correcta".
"""

import os
from dotenv import load_dotenv

load_dotenv()

UNIFORMES = {
    "traje": {
        "nombre": "Uniforme de Traje",
        "model_path": os.getenv("MODEL_PATH_TRAJE", "../ml/models/traje/best.pt"),
        "prendas_requeridas": ["saco", "pantalon"],   # AJUSTA a tus nombres exactos de clase
        "umbral_cumplimiento": 0.8,                    # 0.8 = debe tener al menos 80% de las prendas
    },
    "deportivo": {
        "nombre": "Uniforme Deportivo",
        "model_path": os.getenv("MODEL_PATH_DEPORTIVO", "../ml/models/deportivo/best.pt"),
        "prendas_requeridas": ["buzo", "tenis"],
        "umbral_cumplimiento": 0.8,
    },
    "multicam": {
        "nombre": "Uniforme Multicam",
        "model_path": os.getenv("MODEL_PATH_MULTICAM", "../ml/models/multicam/best.pt"),
        "prendas_requeridas": ["multicam"],
        "umbral_cumplimiento": 0.8,
    },
}