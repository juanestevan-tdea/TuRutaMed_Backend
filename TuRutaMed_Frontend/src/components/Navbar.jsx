import { Link } from "react-router-dom";
import { Train, Bus, CreditCard, MessageSquare, Menu } from "lucide-react";
import { useState } from "react";

export default function Navbar() {
  const [open, setOpen] = useState(false);

  return (
    <nav className="bg-blue-700 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 font-bold text-xl">
          <Train className="w-6 h-6" />
          TuRutaMed
        </Link>
        <button className="md:hidden" onClick={() => setOpen(!open)}>
          <Menu className="w-6 h-6" />
        </button>
        <div className={`${open ? "block" : "hidden"} md:flex gap-6 mt-2 md:mt-0`}>
          <Link to="/rutas" className="hover:text-blue-200 flex items-center gap-1">
            <Bus className="w-4 h-4" /> Rutas
          </Link>
          <Link to="/planificador" className="hover:text-blue-200 flex items-center gap-1">
            <Train className="w-4 h-4" /> Planificador
          </Link>
          <Link to="/civica" className="hover:text-blue-200 flex items-center gap-1">
            <CreditCard className="w-4 h-4" /> Cívica
          </Link>
          <Link to="/asistente" className="hover:text-blue-200 flex items-center gap-1">
            <MessageSquare className="w-4 h-4" /> Asistente IA
          </Link>
        </div>
      </div>
    </nav>
  );
}