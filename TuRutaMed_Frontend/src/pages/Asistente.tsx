import { useState, useRef, useEffect, FormEvent } from 'react';
import api from '../services/api';
import { getApiErrorMessage } from '../api/errors';

interface Mensaje {
  role: 'user' | 'bot';
  text: string;
}

export default function Asistente() {
  const [mensajes, setMensajes] = useState<Mensaje[]>([
    { role: 'bot', text: '¡Hola! Soy TuRutaMed AI. ¿En qué puedo ayudarte con tu movilidad hoy?' },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [mensajes, loading]);

  const enviar = async (e?: FormEvent<HTMLFormElement>) => {
    if (e) e.preventDefault();
    if (!input.trim() || loading) return;
    const userMsg = input.trim();
    setMensajes((prev) => [...prev, { role: 'user', text: userMsg }]);
    setInput('');
    setLoading(true);
    try {
      const res = await api.post('/ia/asistente-ruta', { pregunta: userMsg });
      const respuesta = res.data?.respuesta;
      if (!respuesta) {
        throw new Error('El asistente no devolvió una respuesta.');
      }
      setMensajes((prev) => [...prev, { role: 'bot', text: respuesta }]);
    } catch (error) {
      const detalle = getApiErrorMessage(
        error,
        'No se pudo obtener respuesta del asistente.',
      );
      setMensajes((prev) => [...prev, { role: 'bot', text: `⚠️ ${detalle}` }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-[calc(100vh-64px)] flex flex-col bg-gray-100">
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {mensajes.map((m, idx) => (
          <div key={idx} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div
              className={`max-w-[75%] px-4 py-2 rounded-2xl text-sm shadow ${
                m.role === 'user'
                  ? 'bg-blue-600 text-white rounded-br-sm'
                  : 'bg-white text-gray-800 rounded-bl-sm'
              }`}
            >
              {m.text}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-white text-gray-500 px-4 py-2 rounded-2xl rounded-bl-sm shadow text-sm">
              Escribiendo
              <span className="animate-pulse">...</span>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <form onSubmit={enviar} className="border-t bg-white p-3 flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') enviar();
          }}
          placeholder="Pregunta sobre rutas, Metro, Metrocable..."
          className="flex-1 border border-gray-300 rounded-xl px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="bg-blue-600 text-white px-4 py-2 rounded-xl hover:bg-blue-700 disabled:opacity-50 transition"
        >
          🚀
        </button>
      </form>
    </div>
  );
}