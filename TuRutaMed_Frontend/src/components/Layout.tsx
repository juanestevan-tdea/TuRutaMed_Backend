import { Outlet, Link, useNavigate } from 'react-router-dom';

export default function Layout() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/');
  };

  return (
    <div className="min-h-screen flex flex-col">
      <nav className="bg-white shadow-md h-16 flex items-center px-6">
        <div className="flex items-center justify-between w-full">
          <Link to="/home" className="text-xl font-bold text-blue-600">
            TuRutaMed
          </Link>
          <div className="flex items-center gap-6">
            <Link to="/home" className="text-gray-700 hover:text-blue-600 font-medium">
              Mapa
            </Link>
            <Link to="/rutas" className="text-gray-700 hover:text-blue-600 font-medium">
              Rutas
            </Link>
            <Link to="/tarjeta" className="text-gray-700 hover:text-blue-600 font-medium">
              Mi Tarjeta
            </Link>
            <button
              onClick={handleLogout}
              className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition"
            >
              Cerrar Sesión
            </button>
          </div>
        </div>
      </nav>
      <main className="flex-1">
        <Outlet />
      </main>
    </div>
  );
}