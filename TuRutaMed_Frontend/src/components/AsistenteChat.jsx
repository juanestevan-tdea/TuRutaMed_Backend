import { useState, useRef, useEffect } from "react";
import api from "../services/api";
import { Send, Bot, User, ChevronDown, ChevronUp, Sparkles } from "lucide-react";

export default function AsistenteChat() {
  const [messages, setMessages] = useState([
    { role: "bot", text: "¡Hola! Soy TuRutaMed AI. ¿En qué puedo ayudarte con tu movilidad hoy?" },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [expanded, setExpanded] = useState(true);
  const scrollRef = useRef(null);

  useEffect(() => {
    if (expanded && scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, expanded]);

  const enviar = async () => {
    if (!input.trim() || loading) return;
    const userMsg = input.trim();
    setMessages((prev) => [...prev, { role: "user", text: userMsg }]);
    setInput("");
    setLoading(true);
    try {
      const res = await api.post("/ia/asistente-ruta", { pregunta: userMsg });
      const respuesta = res.data?.respuesta || res.data?.itinerario || "Sin respuesta.";
      setMessages((prev) => [...prev, { role: "bot", text: respuesta }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Lo siento, el servicio de IA no está disponible temporalmente." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto px-4 py-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold flex items-center gap-2">
          <Bot className="w-6 h-6 text-blue-600" /> Asistente de Movilidad IA
        </h2>
        <button
          onClick={() => setExpanded((v) => !v)}
          className="flex items-center gap-1 text-sm text-gray-600 hover:text-blue-600 transition"
        >
          {expanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          {expanded ? "Ocultar" : "Mostrar"} chat
        </button>
      </div>

      <div className="bg-white rounded-2xl shadow-md overflow-hidden border border-gray-200">
        {expanded && (
          <>
            <div
              ref={scrollRef}
              className="h-[460px] overflow-y-auto p-4 space-y-3 bg-gradient-to-b from-gray-50 to-white"
            >
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex items-end gap-2 ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                >
                  {msg.role === "bot" && (
                    <span className="shrink-0 inline-flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600">
                      <Bot className="w-4 h-4" />
                    </span>
                  )}
                  <div
                    className={`px-4 py-2 rounded-2xl max-w-[80%] text-sm leading-relaxed shadow-sm ${
                      msg.role === "user"
                        ? "bg-blue-600 text-white rounded-br-sm"
                        : "bg-white text-gray-800 border border-gray-200 rounded-bl-sm"
                    }`}
                  >
                    {msg.text}
                  </div>
                  {msg.role === "user" && (
                    <span className="shrink-0 inline-flex items-center justify-center w-8 h-8 rounded-full bg-gray-200 text-gray-600">
                      <User className="w-4 h-4" />
                    </span>
                  )}
                </div>
              ))}
              {loading && (
                <div className="flex items-end gap-2">
                  <span className="shrink-0 inline-flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600">
                    <Bot className="w-4 h-4" />
                  </span>
                  <div className="px-4 py-2 rounded-2xl bg-white border border-gray-200 text-sm text-gray-500 italic">
                    <Sparkles className="w-4 h-4 inline mr-1 animate-pulse" />
                    Pensando...
                  </div>
                </div>
              )}
            </div>

            <div className="border-t border-gray-200 p-3 flex gap-2 bg-white">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && enviar()}
                placeholder="Pregunta sobre rutas, Metro, Metrocable..."
                className="flex-1 border border-gray-300 rounded-xl px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button
                onClick={enviar}
                disabled={loading || !input.trim()}
                className="bg-blue-600 text-white px-4 py-2 rounded-xl hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition flex items-center gap-1"
              >
                <Send className="w-4 h-4" />
              </button>
            </div>
          </>
        )}

        {!expanded && (
          <button
            onClick={() => setExpanded(true)}
            className="w-full py-3 text-sm text-blue-600 hover:bg-blue-50 transition flex items-center justify-center gap-2"
          >
            <Bot className="w-4 h-4" /> Abrir chat con el asistente
          </button>
        )}
      </div>
    </div>
  );
}