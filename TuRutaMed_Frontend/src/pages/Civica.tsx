import { useState } from 'react';
import { isAxiosError } from 'axios';
import api from '../services/api';
import { getApiErrorMessage } from '../api/errors';

interface SaldoResponse {
  tarjeta_id: string;
  saldo: number;
}

interface RecargaResponse {
  saldo_nuevo: number;
  mensaje?: string;
}

export default function Civica() {
  const [tarjetaId, setTarjetaId] = useState<string>('');
  const [saldo, setSaldo] = useState<number | null>(null);
  const [monto, setMonto] = useState<string>('');
  const [loadingSaldo, setLoadingSaldo] = useState(false);
  const [loadingRecarga, setLoadingRecarga] = useState(false);
  const [error, setError] = useState<string>('');
  const [mensaje, setMensaje] = useState<string>('');

  const consultarSaldo = async () => {
    const id = tarjetaId.trim();

    if (!id) {
      setError('Ingresa un número de tarjeta.');
      setSaldo(null);
      return;
    }

    setLoadingSaldo(true);
    setError('');
    setMensaje('');

    try {
      const res = await api.get<SaldoResponse>(`/civica/saldo/${encodeURIComponent(id)}`);
      const saldoRecibido = Number(res.data?.saldo);

      if (!Number.isFinite(saldoRecibido)) {
        throw new Error('El servidor devolvió un saldo inválido.');
      }

      setSaldo(saldoRecibido);
      setMensaje('Saldo consultado.');
    } catch (err) {
      setSaldo(null);
      setError(getApiErrorMessage(err, 'No se pudo consultar el saldo.'));
    } finally {
      setLoadingSaldo(false);
    }
  };

  const recargar = async () => {
    const id = tarjetaId.trim();
    const montoNumero = Number(monto);

    if (!id || !monto) {
      setError('Completa tarjeta y monto.');
      return;
    }

    if (!Number.isFinite(montoNumero) || montoNumero <= 0) {
      setError('Ingresa un monto válido mayor a cero.');
      return;
    }

    setLoadingRecarga(true);
    setError('');
    setMensaje('');

    try {
      const res = await api.post<RecargaResponse>('/civica/recargar', {
        tarjeta_id: id,
        monto: montoNumero,
        metodo_de_pago: 'PSE',
      });
      const saldoNuevo = Number(res.data?.saldo_nuevo);

      if (!Number.isFinite(saldoNuevo)) {
        throw new Error('El servidor devolvió un saldo inválido.');
      }

      setSaldo(saldoNuevo);
      setMensaje(res.data?.mensaje || 'Recarga exitosa.');
      setMonto('');
    } catch (err) {
      if (isAxiosError(err) && err.response?.status === 401) {
        setError('Debes iniciar sesión para recargar.');
      } else {
        setError(getApiErrorMessage(err, 'No se pudo procesar la recarga.'));
      }
    } finally {
      setLoadingRecarga(false);
    }
  };

  const ocupado = loadingSaldo || loadingRecarga;
  const tarjetaEnmascarada = tarjetaId.trim()
    ? `**** **** **** ${tarjetaId.trim().slice(-4)}`
    : '**** **** **** ----';
  const saldoTexto = loadingSaldo
    ? 'Consultando...'
    : saldo !== null
      ? `$ ${saldo.toLocaleString('es-CO', { minimumFractionDigits: 2 })}`
      : '—';

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
          <p className="mt-6 text-3xl font-bold" aria-live="polite">
            {saldoTexto}
          </p>
          <p className="mt-4 text-lg font-mono tracking-widest opacity-90">
            {tarjetaEnmascarada}
          </p>
        </div>

        {/* Panel de acciones */}
        <div className="bg-white rounded-xl shadow-lg p-6 space-y-4">
          <div>
            <label
              htmlFor="numero-tarjeta"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Número de tarjeta
            </label>
            <input
              id="numero-tarjeta"
              name="numero-tarjeta"
              type="text"
              value={tarjetaId}
              onChange={(e) => {
                setTarjetaId(e.target.value);
                setSaldo(null);
                setMensaje('');
                setError('');
              }}
              disabled={ocupado}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
              placeholder="Ej. 123456"
            />
          </div>

          <button
            onClick={consultarSaldo}
            disabled={ocupado}
            className="w-full bg-gray-600 text-white py-3 rounded-lg hover:bg-gray-700 disabled:opacity-50 transition font-medium"
          >
            {loadingSaldo ? 'Consultando...' : 'Consultar Saldo'}
          </button>

          <div>
            <label
              htmlFor="monto-recarga"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Monto a recargar
            </label>
            <input
              id="monto-recarga"
              name="monto-recarga"
              type="number"
              min="1"
              value={monto}
              onChange={(e) => setMonto(e.target.value)}
              disabled={ocupado}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
              placeholder="Ej. 20000"
            />
          </div>

          <button
            onClick={recargar}
            disabled={ocupado}
            className="w-full bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 disabled:opacity-50 transition font-medium"
          >
            {loadingRecarga ? 'Recargando...' : 'Recargar Tarjeta'}
          </button>

          {error && (
            <p role="alert" className="text-center text-sm text-red-600 font-medium">
              {error}
            </p>
          )}
          {mensaje && (
            <p role="status" className="text-center text-sm text-blue-600 font-medium">
              {mensaje}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
