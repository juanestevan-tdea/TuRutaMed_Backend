import { useState, useEffect } from 'react';
import api from '../services/api';

export default function Civica() {
  const [tarjetaId, setTarjetaId] = useState<string>('123456');
  const [saldo, setSaldo] = useState<number | null>(null);
  const [monto, setMonto] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [mensaje, setMensaje] = useState<string>('');

  const consultarSaldo = async () => {
    if (!tarjetaId.trim()) {
      setError('Ingresa un número de tarjeta.');
      return;
    }
    setLoading(true);
    setError('');
    setMensaje('');
    try {
      const res = await api.get(`/civica/saldo/${encodeURIComponent(tarjetaId.trim())}`);
      setSaldo(res.data?.saldo ?? 0);
      setMensaje('Saldo actualizado.');
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'No se pudo conectar con el servidor.');
      setSaldo(null);
    } finally {
      setLoading(false);
    }
  };

  const recargar = async () => {
    if (!tarjetaId.trim() || !monto) {
      setError('Completa tarjeta y monto.');
      return;
    }
    setLoading(true);
    setError('');
    setMensaje('');
    try {
      const res = await api.post('/civica/recargar', {
        tarjeta_id: tarjetaId.trim(),
        monto: parseFloat(monto),
        metodo_de_pago: 'PSE',
      });
      setSaldo(res.data?.saldo_nuevo ?? saldo);
      setMensaje(res.data?.mensaje || 'Recarga exitosa.');
      setMonto('');
    } catch (err: any) {
      const status = err?.response?.status;
      if (status === 401) {
        setError('Debes iniciar sesión para recargar.');
      } else {
        setError(err?.response?.data?.detail || 'No se pudo conectar con el servidor.');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    consultarSaldo();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const saldoMostrado = saldo !== null ? saldo : 15500;

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
            $ {saldoMostrado.toLocaleString('es-CO', { minimumFractionDigits: 2 })}
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
          <div>
            <label htmlFor="numero-tarjeta" className="block text-sm font-medium text-gray-700 mb-1">Número de tarjeta</label>
            <input
              id="numero-tarjeta"
              name="numero-tarjeta"
              type="text"
              value={tarjetaId}
              onChange={(e) => setTarjetaId(e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <button
            onClick={consultarSaldo}
            disabled={loading}
            className="w-full bg-gray-600 text-white py-3 rounded-lg hover:bg-gray-700 disabled:opacity-50 transition font-medium"
          >
            {loading ? 'Consultando...' : 'Consultar Saldo'}
          </button>

          <div>
            <label htmlFor="monto-recarga" className="block text-sm font-medium text-gray-700 mb-1">Monto a recargar</label>
            <input
              id="monto-recarga"
              name="monto-recarga"
              type="number"
              value={monto}
              onChange={(e) => setMonto(e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Ej. 20000"
            />
          </div>

          <button
            onClick={recargar}
            disabled={loading}
            className="w-full bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 disabled:opacity-50 transition font-medium"
          >
            Recargar Tarjeta
          </button>

          {error && <p className="text-center text-sm text-red-600 font-medium">{error}</p>}
          {mensaje && <p className="text-center text-sm text-blue-600 font-medium">{mensaje}</p>}
        </div>
      </div>
    </div>
  );
}