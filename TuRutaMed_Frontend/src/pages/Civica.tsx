import { useState } from 'react';
import api from '../services/api';

export default function Civica() {
  const [saldo, setSaldo] = useState<number>(15500);
  const [loading, setLoading] = useState(false);
  const [mensaje, setMensaje] = useState('');

  const consultarSaldo = async () => {
    setLoading(true);
    setMensaje('');
    try {
      await api.get('/civica/saldo/123456');
      setMensaje('Saldo actualizado.');
    } catch {
      setTimeout(() => {
        setSaldo(15500);
        setMensaje('Saldo actualizado (Simulado).');
        setLoading(false);
      }, 800);
      return;
    }
    setLoading(false);
  };

  return (
    <div className="flex justify-center items-center min-h-[calc(100vh-64px)] bg-gray-100 px-4">
      <div className="w-full max-w-md space-y-6">
        {/* Tarjeta física */}
        <div className="bg-gradient-to-br from-blue-800 to-indigo-900 rounded-2xl shadow-2xl p-6 text-white w-96 max-w-full mx-auto">
          <div className="flex items-center justify-between">
            <span className="text-sm font-semibold tracking-wide">TuRutaMed</span>
            <span className="text-xs opacity-80">Tarjeta Cívica</span>
          </div>
          <div className="mt-6">
            <div className="bg-yellow-400 rounded-md w-10 h-8 shadow-inner" />
          </div>
          <p className="mt-6 text-3xl font-bold">
            $ {saldo.toLocaleString('es-CO', { minimumFractionDigits: 2 })}
          </p>
          <p className="mt-4 text-lg font-mono tracking-widest opacity-90">
            **** **** **** 4321
          </p>
          <p className="mt-2 text-sm font-semibold tracking-wide opacity-80">
            JUAN ESTEVAN SANCHEZ
          </p>
        </div>

        {/* Panel de acciones */}
        <div className="bg-white rounded-xl shadow-lg p-6 space-y-4">
          <button
            onClick={consultarSaldo}
            disabled={loading}
            className="w-full bg-gray-600 text-white py-3 rounded-lg hover:bg-gray-700 disabled:opacity-50 transition font-medium"
          >
            {loading ? 'Consultando...' : 'Consultar Saldo'}
          </button>
          <button
            className="w-full bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 transition font-medium"
          >
            Recargar Tarjeta
          </button>
          {mensaje && <p className="text-center text-sm text-blue-600 font-medium">{mensaje}</p>}
        </div>
      </div>
    </div>
  );
}