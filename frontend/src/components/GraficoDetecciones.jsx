import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";

export default function GraficoDetecciones({ registros }) {
  const conteoPorClase = registros.reduce((acc, r) => {
    acc[r.clase_detectada] = (acc[r.clase_detectada] || 0) + 1;
    return acc;
  }, {});

  const datos = Object.entries(conteoPorClase).map(([clase, cantidad]) => ({
    clase,
    cantidad,
  }));

  if (datos.length === 0) {
    return <p className="sin-registros">Aún no hay datos suficientes para graficar.</p>;
  }

  return (
    <ResponsiveContainer width="100%" height={240}>
      <BarChart data={datos}>
        <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
        <XAxis dataKey="clase" tick={{ fontSize: 12 }} />
        <YAxis allowDecimals={false} tick={{ fontSize: 12 }} />
        <Tooltip />
        <Bar dataKey="cantidad" fill="#1b3a2b" radius={[6, 6, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}