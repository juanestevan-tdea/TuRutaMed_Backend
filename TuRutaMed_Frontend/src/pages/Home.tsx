import { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';
import api from '../services/api';
import RouteSearchPanel from '../components/RouteSearchPanel';

let DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconAnchor: [12, 41],
});
L.Marker.prototype.options.icon = DefaultIcon;

interface Paradero {
  nombre_paradero: string;
  coordenadas: [number, number];
  orden: number;
}

interface Ruta {
  _id?: string;
  id?: string;
  nombre_ruta: string;
  tipo_transporte: string;
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

export default function Home() {
  const [rutas, setRutas] = useState<Ruta[]>([]);
  const [loading, setLoading] = useState(true);
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

  return (
    <div className="h-[calc(100vh-64px)] w-full relative">
      <RouteSearchPanel />
      {loading && (
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-[1001] bg-white px-4 py-2 rounded shadow">
          Cargando rutas...
        </div>
      )}
      <MapContainer center={medellin} zoom={13} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {rutas.map((ruta, idx) => {
          const paraderos = (ruta.paraderos || []).slice().sort((a, b) => (a.orden ?? 0) - (b.orden ?? 0));
          const coords: [number, number][] = paraderos.map((p) => [p.coordenadas[1], p.coordenadas[0]]);
          const color = colorPorTipo(ruta.tipo_transporte);
          return (
            <span key={ruta._id || ruta.id || idx}>
              {coords.length > 1 && (
                <Polyline positions={coords} pathOptions={{ color, weight: 4, opacity: 0.8 }} />
              )}
              {paraderos.map((p, i) => (
                <Marker key={`${ruta._id || idx}-${i}`} position={[p.coordenadas[1], p.coordenadas[0]]}>
                  <Popup>{p.nombre_paradero}</Popup>
                </Marker>
              ))}
            </span>
          );
        })}
      </MapContainer>
    </div>
  );
}