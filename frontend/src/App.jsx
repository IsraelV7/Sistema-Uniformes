import { useState } from "react";
import Login from "./components/login.jsx";
import RecuperarPassword from "./components/RecuperarPassword";
import Dashboard from "./pages/Dashboard";

function App() {
  const [vista, setVista] = useState(localStorage.getItem("token") ? "dashboard" : "login");

  const cerrarSesion = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("nombre_usuario");
    localStorage.removeItem("es_superusuario");
    setVista("login");
  };

  if (vista === "login") {
    return <Login onLogin={() => setVista("dashboard")} onIrARecuperar={() => setVista("recuperar")} />;
  }
  if (vista === "recuperar") {
    return <RecuperarPassword onVolver={() => setVista("login")} />;
  }
  return <Dashboard onCerrarSesion={cerrarSesion} />;
}

export default App;