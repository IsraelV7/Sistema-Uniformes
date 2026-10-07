export default function EstadisticasCards({ registros }) {
  const total = registros.length;
  const incorrectos = registros.filter((r) => r.cumple_normativa !== "correcto").length;
  const correctos = total - incorrectos;
  const porcentajeCumplimiento = total > 0 ? ((correctos / total) * 100).toFixed(1) : "0.0";
  const ultima = registros[0];

  const stats = [
    { label: "Total de detecciones", valor: total, color: "azul" },
    { label: "Cumplimiento", valor: `${porcentajeCumplimiento}%`, color: "verde" },
    { label: "Incumplimientos", valor: incorrectos, color: "rojo" },
    {
      label: "Última detección",
      valor: ultima ? new Date(ultima.fecha_hora + "Z").toLocaleTimeString() : "—",
      color: "gris",
    },
  ];

  return (
    <div className="stats-grid">
      {stats.map((s) => (
        <div key={s.label} className={`stat-card stat-card--${s.color}`}>
          <span className="stat-card__valor">{s.valor}</span>
          <span className="stat-card__label">{s.label}</span>
        </div>
      ))}
    </div>
  );
}