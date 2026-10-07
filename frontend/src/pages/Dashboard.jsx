import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import ControlCamara from "../components/ControlCamara";
import TablaReportes from "../components/TablaReportes";
import EstadisticasCards from "../components/EstadisticasCards";
import GraficoDetecciones from "../components/GraficoDetecciones";
import SelectorUniforme from "../components/SelectorUniforme";
import CrearUsuario from "../components/CrearUsuario";
import RelojEnVivo from "../components/RelojEnVivo";
import { obtenerReportes, reiniciarSeguimiento, limpiarHistorial } from "../services/api";
import "../App.css";

export default function Dashboard({ onCerrarSesion }) {
  const [vistaActiva, setVistaActiva] = useState("monitoreo");
  const [registros, setRegistros] = useState([]);
  const esSuperusuario = localStorage.getItem("es_superusuario") === "true";
  const nombreUsuario = localStorage.getItem("nombre_usuario");

  useEffect(() => {
    const cargar = async () => setRegistros(await obtenerReportes());
    cargar();
    const intervalo = setInterval(cargar, 5000);
    return () => clearInterval(intervalo);
  }, []);

  const manejarReiniciarSeguimiento = async () => {
    await reiniciarSeguimiento();
    alert("Seguimiento de personas reiniciado.");
  };

  const manejarLimpiarHistorial = async () => {
    if (!window.confirm("¿Seguro que quieres borrar todo el historial?")) return;
    await limpiarHistorial();
    setRegistros([]);
  };

  return (
    <div className="layout">
      <Sidebar vistaActiva={vistaActiva} onCambiarVista={setVistaActiva} />

      <div className="contenido">
        <header className="dashboard__header">
          <div>
            <h1>Sistema de Monitoreo de Uniformes</h1>
            <p className="dashboard__subtitulo">Panel de control institucional</p>
          </div>
          <div className="dashboard__header-derecha">
            <RelojEnVivo />
            <span className="usuario-activo">{nombreUsuario}</span>
            <button className="boton-salir" onClick={onCerrarSesion}>Cerrar sesión</button>
          </div>
        </header>

        <main className="dashboard__content">
          {vistaActiva === "monitoreo" && (
            <>
              <EstadisticasCards registros={registros} />
              <section className="card">
                <div className="card__encabezado">
                  <h2>Monitoreo en vivo</h2>
                  <button className="boton-secundario" onClick={manejarReiniciarSeguimiento}>
                    Reiniciar seguimiento
                  </button>
                </div>
                <ControlCamara />
              </section>
              <section className="card">
                <h2>Detecciones por tipo</h2>
                <GraficoDetecciones registros={registros} />
              </section>
            </>
          )}

          {vistaActiva === "historial" && (
            <section className="card">
              <div className="card__encabezado">
                <h2>Historial de detecciones</h2>
                <button className="boton-secundario boton-peligro" onClick={manejarLimpiarHistorial}>
                  Limpiar historial
                </button>
              </div>
              <TablaReportes registros={registros} />
            </section>
          )}

          {vistaActiva === "configuracion" && (
            <>
              <div className="config-grid">
                <section className="card">
                  <h2>Uniforme a controlar</h2>
                  <SelectorUniforme />
                </section>
                <section className="card">
                  <h2>Estado del sistema</h2>
                  <ul className="lista-estado">
                    <li><strong>Usuario conectado:</strong> {nombreUsuario}</li>
                    <li><strong>Rol:</strong> {esSuperusuario ? "Superusuario" : "Operador"}</li>
                    <li><strong>Total de registros:</strong> {registros.length}</li>
                  </ul>
                </section>
              </div>

              {esSuperusuario && (
                <section className="card">
                  <CrearUsuario />
                </section>
              )}
            </>
          )}
        </main>
      </div>
    </div>
  );
}