import { useState } from "react";
import { crearUsuario } from "../services/api";

export default function CrearUsuario() {
  const [form, setForm] = useState({ nombre_usuario: "", correo: "", password: "", es_superusuario: false });
  const [mensaje, setMensaje] = useState("");
  const [error, setError] = useState("");

  const manejarSubmit = async (e) => {
    e.preventDefault();
    setMensaje("");
    setError("");
    try {
      await crearUsuario(form);
      setMensaje(`Usuario '${form.nombre_usuario}' creado correctamente.`);
      setForm({ nombre_usuario: "", correo: "", password: "", es_superusuario: false });
    } catch {
      setError("No se pudo crear el usuario (¿nombre o correo repetido?).");
    }
  };

  return (
    <form className="form-crear-usuario" onSubmit={manejarSubmit}>
      <h3>Crear nuevo usuario</h3>
      <input placeholder="Nombre de usuario" value={form.nombre_usuario}
        onChange={(e) => setForm({ ...form, nombre_usuario: e.target.value })} required />
      <input type="email" placeholder="Correo" value={form.correo}
        onChange={(e) => setForm({ ...form, correo: e.target.value })} required />
      <input type="password" placeholder="Contraseña" value={form.password}
        onChange={(e) => setForm({ ...form, password: e.target.value })} required />
      <label className="checkbox-superusuario">
        <input type="checkbox" checked={form.es_superusuario}
          onChange={(e) => setForm({ ...form, es_superusuario: e.target.checked })} />
        Es superusuario
      </label>
      {mensaje && <p className="login-mensaje">{mensaje}</p>}
      {error && <p className="login-error">{error}</p>}
      <button type="submit">Crear usuario</button>
    </form>
  );
}