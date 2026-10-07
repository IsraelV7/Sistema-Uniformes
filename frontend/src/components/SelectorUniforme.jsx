import { useEffect, useState } from "react";
import { obtenerUniformes, seleccionarUniforme, obtenerEstadoMonitoreo } from "../services/api";

export default function SelectorUniforme() {
  const [uniformes, setUniformes] = useState([]);
  const [seleccionado, setSeleccionado] = useState("traje");
  const [guardando, setGuardando] = useState(false);

  useEffect(() => {
    obtenerUniformes().then(setUniformes);
    obtenerEstadoMonitoreo().then((data) => setSeleccionado(data.uniforme_actual));
  }, []);

  const manejarCambio = async (e) => {
    const tipo = e.target.value;
    setGuardando(true);
    try {
      await seleccionarUniforme(tipo);
      setSeleccionado(tipo);
    } finally {
      setGuardando(false);
    }
  };

  return (
    <div className="selector-uniforme">
      <label htmlFor="uniforme">Uniforme a controlar hoy:</label>
      <select id="uniforme" value={seleccionado} onChange={manejarCambio} disabled={guardando}>
        {uniformes.map((u) => (
          <option key={u.id} value={u.id}>
            {u.nombre}
          </option>
        ))}
      </select>
      {guardando && <span className="selector-uniforme__estado">Aplicando cambio...</span>}
    </div>
  );
}