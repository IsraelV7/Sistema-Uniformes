export default function Sidebar({ vistaActiva, onCambiarVista }) {
  const items = [
    { id: "monitoreo", etiqueta: "Monitoreo", icono: "🎥" },
    { id: "historial", etiqueta: "Historial", icono: "🕑" },
    { id: "configuracion", etiqueta: "Configuración", icono: "⚙️" },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar__logo">🛡️</div>
      <nav>
        {items.map((item, i) => (
          <button
            key={item.id}
            className={`sidebar__item ${i % 2 === 0 ? "sidebar__item--azul" : "sidebar__item--amarillo"} ${
              vistaActiva === item.id ? "activo" : ""
            }`}
            onClick={() => onCambiarVista(item.id)}
          >
            <span className="sidebar__icono">{item.icono}</span>
            {item.etiqueta}
          </button>
        ))}
      </nav>
    </aside>
  );
}