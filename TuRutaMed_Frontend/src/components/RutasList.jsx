import { useEffect, useState } from "react";
import api from "../services/api";
import { Bus, Accessibility } from "lucide-react";

export default function RutasList() {
  const [rutas, setRutas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    api
      .get("/rutas", { params: { limit: 20, skip: 0 } })
      .then((res) => setRutas(res.data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="text-center py-8">Cargando rutas...</p>;
  if (error) return <p className="text-center py-8 text-red-500">{error}</p>;

  return (
    <div className="max-w-7xl mx-auto px-4 py-6">
      <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
        <Bus className="w-6 h-6" /> Rutas de Transporte
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {rutas.map((ruta, idx) => (
          <div
            key={idx}
            className="bg-white rounded-xl shadow-md p-4 border border-gray-200 hover:shadow-lg transition"
          >
            <h3 className="font-semibold text-lg">{ruta.nombre_ruta}</h3>
            <p className="text-sm text-gray-600">{ruta.tipo_transporte}</p>
            <p className="text-sm mt-1">
              {ruta.origen} → {ruta.destino}
            </p>
            <p className="text-sm text-gray-500 mt-1">
              ⏱ {ruta.tiempo_estimado_minutos} min
            </p>
            {ruta.accesible && (
              <span className="inline-flex items-center gap-1 mt-2 text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">
                <Accessibility className="w-3 h-3" /> Accesible PMR
              </span>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}