import { Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Home from './pages/Home';
import Civica from './pages/Civica';
import Asistente from './pages/Asistente';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route path="/home" element={<Home />} />
        <Route path="/rutas" element={<div className="p-6 text-xl">Rutas</div>} />
        <Route path="/tarjeta" element={<div className="p-6 text-xl">Mi Tarjeta</div>} />
        <Route path="/civica" element={<Civica />} />
        <Route path="/asistente" element={<Asistente />} />
      </Route>
    </Routes>
  );
}