import { useEffect, useState } from "react";
import {
  streamUrl,
  obtenerEstadoMonitoreo,
  iniciarMonitoreo,
  detenerMonitoreo,
} from "../services/api";

export default function ControlCamara() {
  const [activo, setActivo] = useState(false);
  const [cargando, setCargando] = useState(false);

  useEffect(() => {
    obtenerEstadoMonitoreo().then((data) => setActivo(data.activo));
  }, []);

  const alternarMonitoreo = async () => {
    setCargando(true);
    try {
      if (activo) {
        const data = await detenerMonitoreo();
        setActivo(data.activo);
      } else {
        const data = await iniciarMonitoreo();
        setActivo(data.activo);
      }
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="video-wrapper">
      {activo ? (
        <>
          <div className="video-live-tag">
            <span className="dot-pulse"></span>
            EN VIVO
          </div>
          {/* key fuerza a recargar la imagen cada vez que se reactiva */}
          <img
            key={Date.now()}
            className="video-frame"
            src={streamUrl}
            alt="Video en vivo con detecciones"
          />
        </>
      ) : (
        <div className="video-placeholder">
          <span className="video-placeholder__icono">📷</span>
          <p>La cámara está apagada</p>
        </div>
      )}

      <button
        className={`boton-camara ${activo ? "boton-camara--apagar" : "boton-camara--encender"}`}
        onClick={alternarMonitoreo}
        disabled={cargando}
      >
        {cargando ? "Procesando..." : activo ? "Detener monitoreo" : "Iniciar monitoreo"}
      </button>
    </div>
  );
}