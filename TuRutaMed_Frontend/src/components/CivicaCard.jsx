import { useState } from "react";
import api from "../services/api";
import { CreditCard, Wallet, RefreshCw } from "lucide-react";

export default function CivicaCard() {
  const [tarjetaId, setTarjetaId] = useState("");
  const [saldo, setSaldo] = useState(null);
  const [monto, setMonto] = useState("");
  const [metodo, setMetodo] = useState("PSE");
  const [loading, setLoading] = useState(false);
  const [mensaje, setMensaje] = useState("");

  const consultarSaldo = async () => {
    if (!tarjetaId) return;
    setLoading(true);
    setMensaje("");
    try {
      const res = await api.get(`/civica/saldo/${tarjetaId}`);
      setSaldo(res.data.saldo);
    } catch (err) {
      setMensaje("Error al consultar saldo.");
    } finally {
      setLoading(false);
    }
  };

  const recargar = async () => {
    if (!tarjetaId || !monto) return;
    setLoading(true);
    setMensaje("");
    try {
      const res = await api.post("/civica/recargar", {
        tarjeta_id: tarjetaId,
        monto: parseFloat(monto),
        metodo_de_pago: metodo,
      });
      setSaldo(res.data.saldo_nuevo);
      setMensaje(`Recarga exitosa. Nuevo saldo: $${res.data.saldo_nuevo}`);
    } catch (err) {
      setMensaje(err.response?.data?.detail || "Error en la recarga.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto px-4 py-6">
      <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
        <CreditCard className="w-6 h-6" /> Tarjeta Cívica
      </h2>
      <div className="bg-white rounded-xl shadow-md p-6 space-y-4">
        <input
          type="text"
          placeholder="Número de tarjeta"
          value={tarjetaId}
          onChange={(e) => setTarjetaId(e.target.value)}
          className="w-full border rounded-lg px-3 py-2"
        />
        <button
          onClick={consultarSaldo}
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center justify-center gap-2"
        >
          <Wallet className="w-4 h-4" /> Consultar Saldo
        </button>

        {saldo !== null && (
          <div className="text-center py-2">
            <p className="text-3xl font-bold text-green-600">${saldo.toLocaleString()}</p>
            <p className="text-sm text-gray-500">Saldo disponible (COP)</p>
          </div>
        )}

        <hr />

        <input
          type="number"
          placeholder="Monto a recargar"
          value={monto}
          onChange={(e) => setMonto(e.target.value)}
          className="w-full border rounded-lg px-3 py-2"
        />
        <select
          value={metodo}
          onChange={(e) => setMetodo(e.target.value)}
          className="w-full border rounded-lg px-3 py-2"
        >
          <option value="PSE">PSE</option>
          <option value="Nequi">Nequi</option>
          <option value="Bancolombia">Bancolombia</option>
        </select>
        <button
          onClick={recargar}
          disabled={loading}
          className="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 disabled:opacity-50 flex items-center justify-center gap-2"
        >
          <RefreshCw className="w-4 h-4" /> Recargar
        </button>

        {mensaje && (
          <p className="text-center text-sm text-blue-600 font-medium">{mensaje}</p>
        )}
      </div>
    </div>
  );
}