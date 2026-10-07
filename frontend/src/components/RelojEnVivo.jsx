import { useEffect, useState } from "react";

export default function RelojEnVivo() {
  const [hora, setHora] = useState(new Date());

  useEffect(() => {
    const intervalo = setInterval(() => setHora(new Date()), 1000);
    return () => clearInterval(intervalo);
  }, []);

  return <span className="reloj">{hora.toLocaleTimeString()}</span>;
}