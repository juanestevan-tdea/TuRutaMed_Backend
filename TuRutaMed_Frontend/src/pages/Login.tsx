import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api/client'; // Asegúrate de que esta ruta sea la correcta a tu cliente Axios
import { getApiErrorMessage } from '../api/errors';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [cargando, setCargando] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault(); // Evita que la página se recargue
    setError('');
    setCargando(true);

    try {
      // Endpoint de autenticación en FastAPI
      const response = await api.post('/usuarios/login', {
        email: email,
        password: password,
      });

      // Guardamos los tokens en el localStorage (tanto access_token como token para compatibilidad)
      const accessToken = response.data.access_token || response.data.token;
      const refreshToken = response.data.refresh_token;

      if (accessToken) {
        localStorage.setItem('access_token', accessToken);
        localStorage.setItem('token', accessToken);
      }
      if (refreshToken) {
        localStorage.setItem('refresh_token', refreshToken);
      }

      // Redirigimos al usuario a la ruta principal
      navigate('/');

    } catch (err: unknown) {
      setError(
        getApiErrorMessage(err, 'Error al iniciar sesión. Verifica tus credenciales.'),
      );
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-md p-8 bg-white rounded-lg shadow-md">
        <h1 className="text-2xl font-bold text-center text-blue-900 mb-6">TuRutaMed</h1>

        {error && (
          <div className="mb-4 text-sm text-red-600 bg-red-100 p-2 rounded">
            {error}
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-3 py-2 mt-1 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="tu@email.com"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Contraseña</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-3 py-2 mt-1 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="********"
            />
          </div>

          <button
            type="submit"
            disabled={cargando}
            className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-md disabled:opacity-50"
          >
            {cargando ? 'Iniciando...' : 'Iniciar sesión'}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-gray-600">
          ¿No tienes cuenta?{' '}
          <Link
            to="/registro"
            className="font-semibold text-blue-600 hover:text-blue-700 hover:underline"
          >
            Regístrate
          </Link>
        </p>
      </div>
    </div>
  );
}