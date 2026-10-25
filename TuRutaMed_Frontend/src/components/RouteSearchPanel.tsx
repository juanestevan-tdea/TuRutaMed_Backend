import { useState, FormEvent } from 'react';
import api from '../services/api';

interface Ruta {
  _id?: string;
  id?: string;
  nombre_ruta?: string;
  origen?: string;
  destino?: string;
  tiempo_estimado_minutos?: number;
  tipo_transporte?: string;
  paraderos?: { nombre_paradero?: string }[];
  llegada_minutos?: number;
}

export const claveRuta = (
  ruta: { _id?: string; id?: string; nombre_ruta?: string },
  idx = 0,
): string => ruta._id || ruta.id || ruta.nombre_ruta || `ruta-${idx}`;

interface Props {
  setRutaSeleccionada: (ruta: Ruta | null) => void;
  llegadas?: Record<string, number>;
}

export default function RouteSearchPanel({ setRutaSeleccionada, llegadas = {} }: Props) {
  const [origen, setOrigen] = useState('');
  const [destino, setDestino] = useState('');
  const [resultados, setResultados] = useState<Ruta[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [buscado, setBuscado] = useState(false);

  const buscar = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setBuscado(true);
    try {
      const res = await api.get('/rutas/', { params: { limit: 100, skip: 0 } });
      const data: Ruta[] = Array.isArray(res.data) ? res.data : [];
      const o = origen.trim().toLowerCase();
      const d = destino.trim().toLowerCase();
      const filtradas = data
        .filter((r) => {
          const haystack = [
            r.origen,
            r.destino,
            ...(r.paraderos || []).map((p: { nombre_paradero?: string }) => p?.nombre_paradero),
          ]
            .filter(Boolean)
            .join(' ')
            .toLowerCase();
          if (o === '' && d === '') return true;
          if (o !== '' && d !== '') return haystack.includes(o) || haystack.includes(d);
          if (o !== '') return haystack.includes(o);
          return haystack.includes(d);
        })
        .map((ruta, idx) => ({
          ...ruta,
          llegada_minutos:
            llegadas[claveRuta(ruta, idx)] ?? Math.floor(Math.random() * 13) + 3,
        }));
      setResultados(filtradas);
    } catch {
      setError('No se pudieron obtener las rutas.');
      setResultados([]);
    } finally {
      setLoading(false);
    }
  };

  const limpiar = () => {
    setOrigen('');
    setDestino('');
    setResultados([]);
    setBuscado(false);
    setRutaSeleccionada(null);
  };

  return (
    <div className="absolute top-4 left-4 z-[1000] w-96 bg-white p-4 rounded-lg shadow-xl max-h-[80vh] overflow-hidden flex flex-col">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-lg font-bold text-gray-800">Planificar Viaje</h2>
        <button
          onClick={limpiar}
          className="text-gray-400 hover:text-gray-700 text-sm"
          aria-label="Limpiar búsqueda"
        >
          ✕
        </button>
      </div>
      <form onSubmit={buscar} className="space-y-3">
        <input
          type="text"
          value={origen}
          onChange={(e) => setOrigen(e.target.value)}
          placeholder="Origen"
          className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <input
          type="text"
          value={destino}
          onChange={(e) => setDestino(e.target.value)}
          placeholder="Destino"
          className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 transition"
        >
          {loading ? 'Buscando...' : 'Buscar Rutas'}
        </button>
      </form>

      {error && <p className="text-sm text-red-600 mt-2">{error}</p>}

      <div className="mt-4 max-h-64 overflow-y-auto space-y-2">
        {loading && <p className="text-sm text-gray-500">Buscando...</p>}
        {!loading && buscado && resultados.length === 0 && (
          <div className="flex flex-col items-center text-gray-400 py-4">
            <span className="text-3xl mb-2">🚌</span>
            <p className="text-sm">No se encontraron rutas cercanas.</p>
          </div>
        )}
        {!buscado && !loading && (
          <p className="text-sm text-gray-400">Sin resultados aún.</p>
        )}
        {resultados.map((ruta, idx) => (
          <div
            key={ruta._id || ruta.id || idx}
            onClick={() => setRutaSeleccionada(ruta)}
            className="border border-gray-200 rounded-lg p-3 hover:shadow-md transition cursor-pointer"
          >
            <p className="font-semibold text-gray-800">
              {ruta.nombre_ruta || 'Ruta sin nombre'}
            </p>
            <p className="text-sm text-gray-600">
              ⏱ {ruta.tiempo_estimado_minutos ?? 'N/A'} min
            </p>
            <p className="text-sm font-semibold text-green-700">
              🕒 Llega en {ruta.llegada_minutos ?? 3} min
            </p>
            {ruta.tipo_transporte && (
              <span className="inline-block mt-1 text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full">
                {ruta.tipo_transporte}
              </span>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}