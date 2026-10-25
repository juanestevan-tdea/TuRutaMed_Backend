# Comandos de Ejecución y Desarrollo - TuRutaMed (Windows)

Este documento contiene los comandos exactos y la guía paso a paso para levantar y probar tanto el **Backend** como el **Frontend** de TuRutaMed en entornos Windows (PowerShell / CMD).

---

## 1. Backend (FastAPI + Python 3.12+)

### Prerrequisitos

- Python instalado y accesible en PATH (`python --version`)
- Servicios de infraestructura corriendo (Docker o locales): MySQL en puerto 3306, MongoDB en puerto 27017 y Redis en puerto 6379.

### Pasos en PowerShell

1. Abrir terminal en la raíz del proyecto (`TuRutaMed_Backend`).
2. Activar el entorno virtual de Python:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. Ejecutar el servidor Uvicorn:

   ```powershell
   uvicorn app.main:app --reload --port 8000
   ```

   *(También se puede especificar el host si se desea: `uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`)*

4. Documentación interactiva del API:
   - **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
   - **Healthcheck:** [http://127.0.0.1:8000/health/live](http://127.0.0.1:8000/health/live)

5. Ejecutar la suite de pruebas del Backend:

   ```powershell
   .\venv\Scripts\pytest
   ```

---

## 2. Frontend (React + Vite + TypeScript + Tailwind)

### Prerrequisitos

- Node.js 18+ y npm (`node -v`, `npm -v`)

### Pasos en PowerShell

1. Ingresar al directorio del frontend:

   ```powershell
   cd TuRutaMed_Frontend
   ```

2. Instalar dependencias (solo la primera vez o si cambian paquetes):

   ```powershell
   npm install
   ```

3. Iniciar el servidor de desarrollo Vite:

   ```powershell
   npm run dev
   ```

   *Acceso al frontend:* [http://localhost:5173](http://localhost:5173)

4. Verificar linter y TypeScript:

   ```powershell
   npm run lint
   npm run build
   ```

---

## 3. Comandos Rápidos en una sola línea (PowerShell)

- **Backend:**

  ```powershell
  uvicorn app.main:app --reload --port 8000
  ```

- **Frontend:**

  ```powershell
  cd TuRutaMed_Frontend && npm run dev
  ```
