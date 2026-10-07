import { useState } from "react";

export default function TablaReportes({ registros }) {
  const [filtro, setFiltro] = useState("todos");

  const filtrados =
    filtro === "todos"
      ? registros
      : registros.filter((r) => r.cumple_normativa === filtro);

  return (
    <>
      <div className="filtros">
        <button
          className={filtro === "todos" ? "filtro-btn activo" : "filtro-btn"}
          onClick={() => setFiltro("todos")}
        >
          Todos
        </button>
        <button
          className={filtro === "correcto" ? "filtro-btn activo" : "filtro-btn"}
          onClick={() => setFiltro("correcto")}
        >
          Correctos
        </button>
        <button
          className={filtro === "incorrecto" ? "filtro-btn activo" : "filtro-btn"}
          onClick={() => setFiltro("incorrecto")}
        >
          Incorrectos
        </button>
      </div>

      {filtrados.length === 0 ? (
        <p className="sin-registros">No hay registros para este filtro.</p>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Fecha</th>
                <th>Clase detectada</th>
                <th>Confianza</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              {filtrados.map((r) => (
                <tr key={r.id}>
                  <td>{new Date(r.fecha_hora + "Z").toLocaleString()}</td>
                  <td>{r.clase_detectada}</td>
                  <td>{(r.confianza * 100).toFixed(1)}%</td>
                  <td>
                    <span
                      className={`estado ${
                        r.cumple_normativa === "correcto"
                          ? "estado--correcto"
                          : "estado--incorrecto"
                      }`}
                    >
                      {r.cumple_normativa}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
}