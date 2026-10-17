import { useState } from "react";
import api from "../services/api";
import { CreditCard, Wallet, RefreshCw, ShieldCheck, AlertCircle } from "lucide-react";

export default function CivicaCard() {
  const [tarjetaId, setTarjetaId] = useState("");
  const [saldo, setSaldo] = useState(null);
  const [monto, setMonto] = useState("");
  const [metodo, setMetodo] = useState("PSE");
  const [loading, setLoading] = useState(false);
  const [mensaje, setMensaje] = useState("");
  const [error, setError] = useState("");

  const consultarSaldo = async () => {
    if (!tarjetaId.trim()) {
      setError("Ingresa el número de tarjeta.");
      return;
    }
    setLoading(true);
    setMensaje("");
    setError("");
    try {
      const res = await api.get(`/civica/saldo/${encodeURIComponent(tarjetaId.trim())}`);
      setSaldo(res.data.saldo);
    } catch (err) {
      setError(err?.response?.data?.detail || "Error al consultar saldo.");
      setSaldo(null);
    } finally {
      setLoading(false);
    }
  };

  const recargar = async () => {
    if (!tarjetaId.trim() || !monto) {
      setError("Completa tarjeta y monto.");
      return;
    }
    setLoading(true);
    setMensaje("");
    setError("");
    try {
      const res = await api.post("/civica/recargar", {
        tarjeta_id: tarjetaId.trim(),
        monto: parseFloat(monto),
        metodo_de_pago: metodo,
      });
      setSaldo(res.data.saldo_nuevo);
      setMensaje(
        res.data.mensaje || `Recarga exitosa. Nuevo saldo: $${Number(res.data.saldo_nuevo).toLocaleString()}`
      );
      setMonto("");
    } catch (err) {
      setError(err?.response?.data?.detail || "Error en la recarga. ¿Iniciaste sesión?");
    } finally {
      setLoading(false);
    }
  };

  const hasToken = !!localStorage.getItem("turutamed_token");

  return (
    <div className="max-w-md mx-auto px-4 py-6">
      <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
        <CreditCard className="w-6 h-6 text-blue-600" /> Tarjeta Cívica
      </h2>

      {/* Visual card */}
      <div className="relative overflow-hidden rounded-2xl shadow-xl mb-6 bg-gradient-to-br from-emerald-600 via-emerald-500 to-yellow-400 text-white p-6">
        <div className="absolute -top-6 -right-6 w-24 h-24 rounded-full bg-white/20" />
        <div className="absolute bottom-0 left-0 w-32 h-32 rounded-full bg-black/10" />
        <div className="relative">
          <div className="flex items-center justify-between">
            <span className="text-sm font-semibold tracking-wide">METRO DE MEDELLÍN</span>
            <span className="text-xs opacity-80">Cívica</span>
          </div>
          <div className="mt-6 flex items-center gap-3">
            <div className="w-10 h-8 rounded bg-yellow-300/90 shadow-inner" />
            <span className="text-xs opacity-80">Tarjeta de transporte</span>
          </div>
          <p className="mt-6 text-lg font-mono tracking-widest">
            {tarjetaId ? tarjetaId.replace(/(.{4})/g, "$1 ").trim() : "•••• •••• •••• ••••"}
          </p>
          <div className="mt-4 flex items-end justify-between">
            <div>
              <p className="text-xs opacity-80">Saldo disponible</p>
              <p className="text-2xl font-bold">
                {saldo !== null ? `$${Number(saldo).toLocaleString()}` : "$•••••"}
              </p>
            </div>
            <div className="text-right">
              <p className="text-xs opacity-80">Moneda</p>
              <p className="font-semibold">COP</p>
            </div>
          </div>
        </div>
      </div>

      {!hasToken && (
        <div className="mb-4 flex items-start gap-2 text-sm text-amber-700 bg-amber-50 border border-amber-200 rounded-lg p-3">
          <AlertCircle className="w-4 h-4 mt-0.5 shrink-0" />
          <span>
            No hay sesión activa. Inicia sesión en la barra superior para recargar (el saldo se puede consultar sin token).
          </span>
        </div>
      )}

      <div className="bg-white rounded-xl shadow-md p-6 space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Número de tarjeta</label>
          <input
            type="text"
            placeholder="Ej. 123456"
            value={tarjetaId}
            onChange={(e) => setTarjetaId(e.target.value)}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <button
          onClick={consultarSaldo}
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center justify-center gap-2 font-medium"
        >
          <Wallet className="w-4 h-4" /> Consultar Saldo
        </button>

        {saldo !== null && (
          <div className="text-center py-2">
            <p className="text-3xl font-bold text-green-600">${Number(saldo).toLocaleString()}</p>
            <p className="text-sm text-gray-500">Saldo disponible (COP)</p>
          </div>
        )}

        <hr className="border-gray-200" />

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Monto a recargar</label>
          <input
            type="number"
            min="1"
            placeholder="Monto en COP"
            value={monto}
            onChange={(e) => setMonto(e.target.value)}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Método de pago</label>
          <select
            value={metodo}
            onChange={(e) => setMetodo(e.target.value)}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="PSE">PSE</option>
            <option value="Nequi">Nequi</option>
            <option value="Bancolombia">Bancolombia</option>
          </select>
        </div>

        <button
          onClick={recargar}
          disabled={loading}
          className="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 disabled:opacity-50 flex items-center justify-center gap-2 font-medium"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} /> Recargar
        </button>

        {hasToken && (
          <p className="flex items-center justify-center gap-1 text-xs text-green-600">
            <ShieldCheck className="w-3 h-3" /> Sesión JWT activa
          </p>
        )}

        {mensaje && (
          <p className="text-center text-sm text-blue-600 font-medium">{mensaje}</p>
        )}
        {error && (
          <p className="text-center text-sm text-red-600 font-medium">{error}</p>
        )}
      </div>
    </div>
  );
}