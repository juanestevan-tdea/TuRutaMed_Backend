import { Outlet, NavLink, useNavigate } from 'react-router-dom';

const linkClass = ({ isActive }: { isActive: boolean }) =>
  `font-medium transition ${isActive ? 'text-blue-600 underline' : 'text-gray-700 hover:text-blue-600'}`;

export default function Layout() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('token');
    localStorage.removeItem('refresh_token');
    navigate('/login');
  };

  return (
    <div className="min-h-screen flex flex-col">
      <nav className="bg-white shadow-md h-16 flex items-center px-6">
        <div className="flex items-center justify-between w-full">
          <NavLink to="/" className="text-xl font-bold text-blue-600 whitespace-nowrap">
            TuRutaMed
          </NavLink>
          <div className="flex items-center gap-6 whitespace-nowrap">
            <NavLink to="/" className={linkClass}>
              Mapa
            </NavLink>
            <NavLink to="/civica" className={linkClass}>
              Mi Tarjeta
            </NavLink>
            <NavLink to="/asistente" className={linkClass}>
              Asistente IA
            </NavLink>
            <button
              onClick={handleLogout}
              className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition whitespace-nowrap"
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