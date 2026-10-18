import { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';
import api from '../services/api';
import RouteSearchPanel from '../components/RouteSearchPanel';

const DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconAnchor: [12, 41],
});
L.Marker.prototype.options.icon = DefaultIcon;

interface Paradero {
  nombre_paradero?: string;
  coordenadas?: [number, number];
  latitud?: number;
  longitud?: number;
  orden?: number;
}

interface Ruta {
  _id?: string;
  id?: string;
  nombre_ruta?: string;
  tipo_transporte?: string;
  paraderos?: Paradero[];
}

const colorPorTipo = (tipo: string): string => {
  const t = (tipo || '').toLowerCase();
  if (t.includes('metro') && !t.includes('cable') && !t.includes('bus')) return '#0056A6';
  if (t.includes('tranv')) return '#00875A';
  if (t.includes('cable')) return '#F59E0B';
  if (t.includes('bus')) return '#8B5CF6';
  return '#6B7280';
};

const toLatLng = (p: Paradero): [number, number] | null => {
  if (p?.coordenadas && Array.isArray(p.coordenadas) && p.coordenadas.length >= 2) {
    return [p.coordenadas[1], p.coordenadas[0]];
  }
  if (typeof p?.latitud === 'number' && typeof p?.longitud === 'number') {
    return [p.latitud, p.longitud];
  }
  return null;
};

function MapController({ rutaSeleccionada }: { rutaSeleccionada: Ruta | null }) {
  const map = useMap();
  useEffect(() => {
    if (!rutaSeleccionada) return;
    const paraderos = (rutaSeleccionada.paraderos || []).slice().sort((a, b) => (a?.orden ?? 0) - (b?.orden ?? 0));
    const coords = paraderos.map(toLatLng).filter((c): c is [number, number] => c !== null);
    if (coords.length === 0) return;
    const bounds = L.latLngBounds(coords);
    map.fitBounds(bounds, { padding: [50, 50] });
  }, [rutaSeleccionada, map]);
  return null;
}

export default function Home() {
  const [rutas, setRutas] = useState<Ruta[]>([]);
  const [loading, setLoading] = useState(true);
  const [rutaSeleccionada, setRutaSeleccionada] = useState<Ruta | null>(null);
  const medellin: [number, number] = [6.2442, -75.5812];

  useEffect(() => {
    let cancelled = false;
    api
      .get('/rutas', { params: { limit: 100, skip: 0 } })
      .then((res) => {
        if (cancelled) return;
        const data = Array.isArray(res.data) ? res.data : [];
        setRutas(data);
      })
      .catch(() => {
        if (!cancelled) setRutas([]);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const isSeleccionada = (r: Ruta) => rutaSeleccionada && (r._id || r.id) === (rutaSeleccionada._id || rutaSeleccionada.id);

  return (
    <div className="h-[calc(100vh-64px)] w-full relative">
      <RouteSearchPanel setRutaSeleccionada={setRutaSeleccionada} />
      {loading && (
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-[1001] bg-white px-4 py-2 rounded shadow">
          Cargando rutas...
        </div>
      )}
      <MapContainer center={medellin} zoom={13} style={{ height: '100%', width: '100%' }}>
        <MapController rutaSeleccionada={rutaSeleccionada} />
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {rutas.map((ruta, idx) => {
          const paraderos = (ruta.paraderos || []).slice().sort((a, b) => (a?.orden ?? 0) - (b?.orden ?? 0));
          const coords = paraderos.map(toLatLng).filter((c): c is [number, number] => c !== null);
          const selected = isSeleccionada(ruta);
          const color = selected ? '#EF4444' : colorPorTipo(ruta.tipo_transporte || '');
          return (
            <span key={ruta._id || ruta.id || idx}>
              {coords.length > 1 && (
                <Polyline
                  positions={coords}
                  pathOptions={{ color, weight: selected ? 8 : 4, opacity: selected ? 1 : 0.5 }}
                />
              )}
              {paraderos.map((p, i) => {
                const pos = toLatLng(p);
                if (!pos) return null;
                return (
                  <Marker key={`${ruta._id || idx}-${i}`} position={pos}>
                    <Popup>{p?.nombre_paradero || 'Paradero'}</Popup>
                  </Marker>
                );
              })}
            </span>
          );
        })}
      </MapContainer>
    </div>
  );
}