import { useEffect, useState, useMemo } from "react";
import api from "../services/api";
import { Bus, Accessibility, Search, AlertCircle, CheckCircle2 } from "lucide-react";

export default function RutasList() {
  const [rutas, setRutas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [query, setQuery] = useState("");

  useEffect(() => {
    let cancelled = false;
    api
      .get("/rutas", { params: { limit: 100, skip: 0 } })
      .then((res) => {
        if (cancelled) return;
        const data = Array.isArray(res.data) ? res.data : res.data?.items || [];
        setRutas(data);
      })
      .catch((err) => {
        if (cancelled) return;
        setError(err?.response?.data?.detail || err.message || "Error al cargar rutas");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const filtradas = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return rutas;
    return rutas.filter((r) => {
      const haystack = [
        r.nombre_ruta,
        r.tipo_transporte,
        r.origen,
        r.destino,
        r.estado,
        r.estado_operativo,
      ]
        .filter(Boolean)
        .join(" ")
        .toLowerCase();
      return haystack.includes(q);
    });
  }, [rutas, query]);

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-12 text-center">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-600 border-t-transparent" />
        <p className="mt-3 text-gray-500">Cargando rutas de transporte...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-12 text-center">
        <AlertCircle className="w-10 h-10 text-red-500 mx-auto" />
        <p className="mt-3 text-red-600">{error}</p>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-6">
        <h2 className="text-2xl font-bold flex items-center gap-2">
          <Bus className="w-6 h-6 text-blue-600" /> Rutas de Transporte
        </h2>
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Buscar rutas, Metro, Metrocable..."
            className="w-full pl-9 pr-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
          />
        </div>
      </div>

      {filtradas.length === 0 ? (
        <p className="text-center text-gray-500 py-8">No se encontraron rutas.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtradas.map((ruta, idx) => {
            const pmr = ruta.accesible ?? ruta.pmr ?? ruta.accesible_pmr;
            const estado = ruta.estado_operativo || ruta.estado || "Operativo";
            const operativo = /operativo|activo|disponible/i.test(estado);
            return (
              <div
                key={ruta._id || ruta.id || idx}
                className="bg-white rounded-xl shadow-md p-4 border border-gray-200 hover:shadow-lg transition flex flex-col"
              >
                <div className="flex items-start justify-between gap-2">
                  <h3 className="font-semibold text-lg text-gray-900">
                    {ruta.nombre_ruta || "Ruta sin nombre"}
                  </h3>
                  <span
                    className={`shrink-0 inline-flex items-center gap-1 text-xs px-2 py-1 rounded-full font-medium ${
                      operativo
                        ? "bg-emerald-100 text-emerald-700"
                        : "bg-amber-100 text-amber-700"
                    }`}
                  >
                    {operativo ? (
                      <CheckCircle2 className="w-3 h-3" />
                    ) : (
                      <AlertCircle className="w-3 h-3" />
                    )}
                    {estado}
                  </span>
                </div>

                <p className="text-sm text-gray-600 mt-1">{ruta.tipo_transporte}</p>
                <p className="text-sm mt-2 text-gray-700">
                  <span className="font-medium">{ruta.origen}</span>
                  <span className="mx-1 text-gray-400">→</span>
                  <span className="font-medium">{ruta.destino}</span>
                </p>
                <p className="text-sm text-gray-500 mt-1">
                  ⏱ {ruta.tiempo_estimado_minutos ?? "N/A"} min
                </p>

                <div className="mt-3 flex flex-wrap gap-2">
                  {pmr && (
                    <span className="inline-flex items-center gap-1 text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full">
                      <Accessibility className="w-3 h-3" /> Accesible PMR
                    </span>
                  )}
                  {Array.isArray(ruta.paraderos) && ruta.paraderos.length > 0 && (
                    <span className="inline-flex items-center gap-1 text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded-full">
                      {ruta.paraderos.length} paraderos
                    </span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}