import { useState } from "react";
import api from "../services/api";
import { Train, Clock, Route } from "lucide-react";

export default function PlanificadorViaje() {
  const [origen, setOrigen] = useState("");
  const [destino, setDestino] = useState("");
  const [duracion, setDuracion] = useState(null);
  const [multimodal, setMultimodal] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const calcularDuracion = async () => {
    if (!origen || !destino) {
      setError("Completa origen y destino.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const res = await api.post("/viajes/calcular-duracion", {
        origen,
        destino,
        duracion_minutos: 30,
      });
      setDuracion(res.data);
    } catch (err) {
      setError(err?.response?.data?.detail || "No se pudo calcular la duración.");
    } finally {
      setLoading(false);
    }
  };

  const planificarMultimodal = async () => {
    if (!origen || !destino) {
      setError("Completa origen y destino.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const res = await api.post("/viajes/multimodal", {
        secuencia_rutas: [`${origen} → ${destino} (Metro)`, "Metrocable", "Bus Alimentador"],
      });
      setMultimodal(res.data);
    } catch (err) {
      setError(err?.response?.data?.detail || "No se pudo planificar el viaje.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto px-4 py-6">
      <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
        <Route className="w-6 h-6" /> Planificador de Viaje
      </h2>
      <div className="bg-white rounded-xl shadow-md p-6 space-y-4">
        <input
          type="text"
          placeholder="Origen (ej. Poblado)"
          value={origen}
          onChange={(e) => setOrigen(e.target.value)}
          className="w-full border rounded-lg px-3 py-2"
        />
        <input
          type="text"
          placeholder="Destino (ej. Niquía)"
          value={destino}
          onChange={(e) => setDestino(e.target.value)}
          className="w-full border rounded-lg px-3 py-2"
        />
        <div className="flex gap-3">
          <button
            onClick={calcularDuracion}
            disabled={loading}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2"
          >
            <Clock className="w-4 h-4" /> Calcular Duración
          </button>
          <button
            onClick={planificarMultimodal}
            disabled={loading}
            className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 disabled:opacity-50 flex items-center gap-2"
          >
            <Train className="w-4 h-4" /> Plan Multimodal
          </button>
        </div>

        {error && (
          <p className="text-sm text-red-600 font-medium">{error}</p>
        )}

        {duracion && (
          <div className="mt-4 p-3 bg-blue-50 rounded-lg">
            <p className="font-medium">{duracion.origen} → {duracion.destino}</p>
            <p className="text-sm text-gray-600">Duración estimada: {duracion.duracion_minutos} min</p>
          </div>
        )}

        {multimodal && (
          <div className="mt-4 p-3 bg-green-50 rounded-lg">
            <p className="font-medium">Itinerario sugerido:</p>
            <p className="text-sm text-gray-600">{multimodal.itinerario}</p>
          </div>
        )}
      </div>
    </div>
  );
}