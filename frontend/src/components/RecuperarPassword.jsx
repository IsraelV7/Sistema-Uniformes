import { useState } from "react";
import { solicitarRecuperacion, verificarPin, resetearPassword } from "../services/api";

export default function RecuperarPassword({ onVolver }) {
  const [paso, setPaso] = useState(1);
  const [correo, setCorreo] = useState("");
  const [pin, setPin] = useState("");
  const [nuevaPassword, setNuevaPassword] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [error, setError] = useState("");
  const [cargando, setCargando] = useState(false);

  const enviarCorreo = async (e) => {
    e.preventDefault();
    setCargando(true);
    setError("");
    try {
      await solicitarRecuperacion(correo);
      setMensaje("Si el correo existe, te enviamos un código de 6 dígitos.");
      setPaso(2);
    } catch {
      setError("No se pudo enviar el código. Intenta de nuevo.");
    } finally {
      setCargando(false);
    }
  };

  const confirmarCambio = async (e) => {
    e.preventDefault();
    setCargando(true);
    setError("");
    try {
      await verificarPin(correo, pin);
      await resetearPassword(correo, pin, nuevaPassword);
      setMensaje("Contraseña actualizada. Ya puedes iniciar sesión.");
      setTimeout(onVolver, 2000);
    } catch {
      setError("Código incorrecto o expirado.");
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="login-pantalla">
      <form className="login-tarjeta" onSubmit={paso === 1 ? enviarCorreo : confirmarCambio}>
        <h1>Recuperar contraseña</h1>

        {paso === 1 && (
          <>
            <label>Correo electrónico</label>
            <input type="email" value={correo} onChange={(e) => setCorreo(e.target.value)} required />
          </>
        )}

        {paso === 2 && (
          <>
            <label>Código de 6 dígitos</label>
            <input value={pin} onChange={(e) => setPin(e.target.value)} maxLength={6} required />
            <label>Nueva contraseña</label>
            <input type="password" value={nuevaPassword} onChange={(e) => setNuevaPassword(e.target.value)} required />
          </>
        )}

        {mensaje && <p className="login-mensaje">{mensaje}</p>}
        {error && <p className="login-error">{error}</p>}

        <button type="submit" disabled={cargando}>
          {cargando ? "Procesando..." : paso === 1 ? "Enviar código" : "Cambiar contraseña"}
        </button>

        <button type="button" className="login-link" onClick={onVolver}>
          Volver a iniciar sesión
        </button>
      </form>
    </div>
  );
}