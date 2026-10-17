import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import RutasList from "./components/RutasList";
import PlanificadorViaje from "./components/PlanificadorViaje";
import CivicaCard from "./components/CivicaCard";
import AsistenteChat from "./components/AsistenteChat";

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<RutasList />} />
        <Route path="/rutas" element={<RutasList />} />
        <Route path="/planificador" element={<PlanificadorViaje />} />
        <Route path="/civica" element={<CivicaCard />} />
        <Route path="/asistente" element={<AsistenteChat />} />
      </Routes>
    </BrowserRouter>
  );
}