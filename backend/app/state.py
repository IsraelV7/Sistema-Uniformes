"""
state.py
---------
Guarda el "estado en vivo" del sistema: si el monitoreo está
encendido o apagado, y qué uniforme se está controlando ahora mismo.
Es un objeto en memoria, compartido por toda la app mientras corre.
"""


class EstadoSistema:
    def __init__(self):
        self.activo = False               # ¿la cámara está transmitiendo?
        self.uniforme_actual = "traje"     # uniforme seleccionado por defecto


estado = EstadoSistema()