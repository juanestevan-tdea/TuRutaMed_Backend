import { useState } from "react";
import api from "../services/api";
import { Send, Bot, User } from "lucide-react";

export default function AsistenteChat() {
  const [messages, setMessages] = useState([
    { role: "bot", text: "¡Hola! Soy TuRutaMed AI. ¿En qué puedo ayudarte con tu movilidad hoy?" },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const enviar = async () => {
    if (!input.trim()) return;
    const userMsg = input.trim();
    setMessages((prev) => [...prev, { role: "user", text: userMsg }]);
    setInput("");
    setLoading(true);
    try {
      const res = await api.post("/ia/asistente-ruta", { pregunta: userMsg });
      setMessages((prev) => [...prev, { role: "bot", text: res.data.respuesta }]);
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
      <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
        <Bot className="w-6 h-6" /> Asistente de Movilidad IA
      </h2>
      <div className="bg-white rounded-xl shadow-md flex flex-col h-[500px]">
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex items-start gap-2 ${msg.role === "user" ? "justify-end" : ""}`}
            >
              {msg.role === "bot" && <Bot className="w-5 h-5 text-blue-600 mt-1" />}
              <div
                className={`px-3 py-2 rounded-lg max-w-[80%] text-sm ${
                  msg.role === "user"
                    ? "bg-blue-600 text-white"
                    : "bg-gray-100 text-gray-800"
                }`}
              >
                {msg.text}
              </div>
              {msg.role === "user" && <User className="w-5 h-5 text-gray-600 mt-1" />}
            </div>
          ))}
          {loading && (
            <div className="flex items-center gap-2">
              <Bot className="w-5 h-5 text-blue-600" />
              <span className="text-sm text-gray-500 animate-pulse">Pensando...</span>
            </div>
          )}
        </div>
        <div className="border-t p-3 flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && enviar()}
            placeholder="Pregunta sobre rutas, Metro, Metrocable..."
            className="flex-1 border rounded-lg px-3 py-2 text-sm"
          />
          <button
            onClick={enviar}
            disabled={loading}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}