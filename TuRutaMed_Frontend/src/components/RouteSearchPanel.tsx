import { useState, FormEvent } from 'react';
import api from '../services/api';

interface Ruta {
  _id?: string;
  id?: string;
  nombre_ruta?: string;
  tiempo_estimado_minutos?: number;
  costo?: number;
  tipo_transporte?: string;
}

export default function RouteSearchPanel() {
  const [origen, setOrigen] = useState('');
  const [destino, setDestino] = useState('');
  const [rutas, setRutas] = useState<Ruta[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const buscar = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const res = await api.get('/rutas', { params: { limit: 20, skip: 0 } });
      const data = Array.isArray(res.data) ? res.data : [];
      setRutas(data);
    } catch (err) {
      setError('No se pudieron obtener las rutas.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="absolute top-4 left-4 z-[1000] w-96 bg-white p-4 rounded-lg shadow-xl max-h-[80vh] overflow-hidden flex flex-col">
      <h2 className="text-lg font-bold text-gray-800 mb-3">Planificar Viaje</h2>
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

      <div className="mt-4 overflow-y-auto flex-1 space-y-2">
        {loading && <p className="text-sm text-gray-500">Buscando...</p>}
        {!loading && rutas.length === 0 && (
          <p className="text-sm text-gray-400">Sin resultados aún.</p>
        )}
        {rutas.map((ruta, idx) => (
          <div
            key={ruta._id || ruta.id || idx}
            className="border border-gray-200 rounded-lg p-3 hover:shadow-md transition"
          >
            <p className="font-semibold text-gray-800">
              {ruta.nombre_ruta || 'Ruta sin nombre'}
            </p>
            <p className="text-sm text-gray-600">
              ⏱ {ruta.tiempo_estimado_minutos ?? 'N/A'} min
            </p>
            <p className="text-sm text-gray-600">
              💲 {ruta.costo ?? 'N/A'}
            </p>
            {ruta.tipo_transporte && (
              <p className="text-xs text-gray-400 mt-1">{ruta.tipo_transporte}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}