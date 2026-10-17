import { Link, useLocation } from "react-router-dom";
import {
  Train,
  Bus,
  CreditCard,
  MessageSquare,
  Menu,
  X,
  LogIn,
  LogOut,
  User,
} from "lucide-react";
import { useState, useEffect } from "react";

const NAV_ITEMS = [
  { to: "/rutas", label: "Rutas", icon: Bus },
  { to: "/planificador", label: "Planificador", icon: Train },
  { to: "/civica", label: "Cívica", icon: CreditCard },
  { to: "/asistente", label: "Asistente IA", icon: MessageSquare },
];

export default function Navbar() {
  const [open, setOpen] = useState(false);
  const [token, setToken] = useState(() => localStorage.getItem("turutamed_token"));
  const location = useLocation();

  useEffect(() => {
    const sync = () => setToken(localStorage.getItem("turutamed_token"));
    window.addEventListener("storage", sync);
    return () => window.removeEventListener("storage", sync);
  }, []);

  const handleLogin = () => {
    const demoToken = "demo.jwt.token.turutamed";
    localStorage.setItem("turutamed_token", demoToken);
    setToken(demoToken);
  };

  const handleLogout = () => {
    localStorage.removeItem("turutamed_token");
    setToken(null);
  };

  return (
    <nav className="sticky top-0 z-50 bg-gray-900/95 backdrop-blur text-white shadow-lg border-b border-gray-800">
      <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 font-bold text-xl tracking-tight">
          <span className="inline-flex items-center justify-center w-9 h-9 rounded-lg bg-blue-600">
            <Train className="w-5 h-5" />
          </span>
          TuRutaMed
        </Link>

        <button
          className="md:hidden p-2 rounded-lg hover:bg-gray-800"
          onClick={() => setOpen(!open)}
          aria-label="Menú"
        >
          {open ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>

        <div className="hidden md:flex items-center gap-2">
          {NAV_ITEMS.map(({ to, label, icon: Icon }) => {
            const active = location.pathname === to;
            return (
              <Link
                key={to}
                to={to}
                className={`flex items-center gap-1 px-3 py-2 rounded-lg text-sm font-medium transition ${
                  active
                    ? "bg-blue-600 text-white"
                    : "text-gray-300 hover:text-white hover:bg-gray-800"
                }`}
              >
                <Icon className="w-4 h-4" /> {label}
              </Link>
            );
          })}

          <div className="ml-2 pl-2 border-l border-gray-700">
            {token ? (
              <div className="flex items-center gap-2">
                <span className="flex items-center gap-1 text-xs text-green-400">
                  <User className="w-4 h-4" /> Autenticado
                </span>
                <button
                  onClick={handleLogout}
                  className="flex items-center gap-1 px-3 py-2 rounded-lg text-sm text-gray-300 hover:text-white hover:bg-gray-800 transition"
                >
                  <LogOut className="w-4 h-4" /> Salir
                </button>
              </div>
            ) : (
              <button
                onClick={handleLogin}
                className="flex items-center gap-1 px-3 py-2 rounded-lg text-sm bg-blue-600 text-white hover:bg-blue-700 transition"
              >
                <LogIn className="w-4 h-4" /> Iniciar sesión
              </button>
            )}
          </div>
        </div>
      </div>

      {open && (
        <div className="md:hidden px-4 pb-3 space-y-1 border-t border-gray-800">
          {NAV_ITEMS.map(({ to, label, icon: Icon }) => (
            <Link
              key={to}
              to={to}
              onClick={() => setOpen(false)}
              className="flex items-center gap-2 px-3 py-2 rounded-lg text-gray-300 hover:text-white hover:bg-gray-800"
            >
              <Icon className="w-4 h-4" /> {label}
            </Link>
          ))}
          <div className="pt-2 border-t border-gray-800">
            {token ? (
              <button
                onClick={() => {
                  handleLogout();
                  setOpen(false);
                }}
                className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-gray-300 hover:text-white hover:bg-gray-800"
              >
                <LogOut className="w-4 h-4" /> Cerrar sesión
              </button>
            ) : (
              <button
                onClick={() => {
                  handleLogin();
                  setOpen(false);
                }}
                className="w-full flex items-center gap-2 px-3 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700"
              >
                <LogIn className="w-4 h-4" /> Iniciar sesión
              </button>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}