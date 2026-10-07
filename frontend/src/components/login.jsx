import { useState } from "react";
import { login } from "../services/api";

export default function Login({ onLogin, onIrARecuperar }) {
  const [nombreUsuario, setNombreUsuario] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [cargando, setCargando] = useState(false);

  const manejarSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setCargando(true);
    try {
      const datos = await login(nombreUsuario, password);
      localStorage.setItem("token", datos.access_token);
      localStorage.setItem("nombre_usuario", datos.nombre_usuario);
      localStorage.setItem("es_superusuario", datos.es_superusuario);
      onLogin();
    } catch {
      setError("Usuario o contraseña incorrectos");
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="login-pantalla">
      <form className="login-tarjeta" onSubmit={manejarSubmit}>
        <h1>Sistema de Monitoreo de Uniformes</h1>
        <p className="login-subtitulo">Inicia sesión para continuar</p>

        <label>Usuario</label>
        <input value={nombreUsuario} onChange={(e) => setNombreUsuario(e.target.value)} required />

        <label>Contraseña</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />

        {error && <p className="login-error">{error}</p>}

        <button type="submit" disabled={cargando}>
          {cargando ? "Ingresando..." : "Ingresar"}
        </button>

        <button type="button" className="login-link" onClick={onIrARecuperar}>
          ¿Olvidaste tu contraseña?
        </button>
      </form>
    </div>
  );
}