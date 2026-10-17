import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';
import RouteSearchPanel from '../components/RouteSearchPanel';

let DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconAnchor: [12, 41],
});
L.Marker.prototype.options.icon = DefaultIcon;

export default function Home() {
  const medellin: [number, number] = [6.2442, -75.5812];
  const tdea: [number, number] = [6.270, -75.566];

  return (
    <div className="h-[calc(100vh-64px)] w-full relative">
      <RouteSearchPanel />
      <MapContainer center={medellin} zoom={13} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={tdea}>
          <Popup>Tecnológico de Antioquia</Popup>
        </Marker>
      </MapContainer>
    </div>
  );
}