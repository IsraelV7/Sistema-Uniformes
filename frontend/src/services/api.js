import axios from "axios";

const API_URL = "http://localhost:8000";

function authHeaders() {
  const token = localStorage.getItem("token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export const streamUrl = `${API_URL}/deteccion/stream`;

export async function login(nombre_usuario, password) {
  const respuesta = await axios.post(`${API_URL}/auth/login`, { nombre_usuario, password });
  return respuesta.data;
}

export async function solicitarRecuperacion(correo) {
  const respuesta = await axios.post(`${API_URL}/auth/recuperar`, { correo });
  return respuesta.data;
}

export async function verificarPin(correo, pin) {
  const respuesta = await axios.post(`${API_URL}/auth/verificar-pin`, { correo, pin });
  return respuesta.data;
}

export async function resetearPassword(correo, pin, nueva_password) {
  const respuesta = await axios.post(`${API_URL}/auth/resetear-password`, { correo, pin, nueva_password });
  return respuesta.data;
}

export async function crearUsuario(datos) {
  const respuesta = await axios.post(`${API_URL}/usuarios/`, datos, { headers: authHeaders() });
  return respuesta.data;
}

export async function obtenerReportes(tipoUniforme = null) {
  const params = tipoUniforme ? { tipo_uniforme: tipoUniforme } : {};
  const respuesta = await axios.get(`${API_URL}/reportes/`, { params });
  return respuesta.data;
}

export async function limpiarHistorial() {
  const respuesta = await axios.delete(`${API_URL}/reportes/`, { headers: authHeaders() });
  return respuesta.data;
}

export async function obtenerUniformes() {
  const respuesta = await axios.get(`${API_URL}/config/uniformes`);
  return respuesta.data;
}

export async function seleccionarUniforme(tipo) {
  const respuesta = await axios.post(`${API_URL}/config/uniformes/seleccionar`, { tipo });
  return respuesta.data;
}

export async function obtenerEstadoMonitoreo() {
  const respuesta = await axios.get(`${API_URL}/deteccion/estado`);
  return respuesta.data;
}

export async function iniciarMonitoreo() {
  const respuesta = await axios.post(`${API_URL}/deteccion/iniciar`);
  return respuesta.data;
}

export async function detenerMonitoreo() {
  const respuesta = await axios.post(`${API_URL}/deteccion/detener`);
  return respuesta.data;
}

export async function reiniciarSeguimiento() {
  const respuesta = await axios.post(`${API_URL}/deteccion/reiniciar-seguimiento`, {}, { headers: authHeaders() });
  return respuesta.data;
}