# 🚍 TuRutaMed Backend API

> Sistema integral y plataforma backend de alta disponibilidad para la gestión inteligente del transporte público multimodal, geolocalización geoespacial de paraderos y reportes viales comunitarios en tiempo real en el **Valle de Aburrá (Medellín, Antioquia)**.

---

## 1. INTRODUCCIÓN

**TuRutaMed** es una solución tecnológica diseñada para transformar la experiencia de movilidad urbana de los millones de ciudadanos que transitan diariamente por el Área Metropolitana del **Valle de Aburrá**, conectando nodos clave como Medellín, Bello, Itagüí, Envigado, Sabaneta, Copacabana, La Estrella, Caldas, Girardota y Barbosa.

El ecosistema de transporte en la región integra sistemas masivos (Metro de Medellín, Metrocable, Tranvía, Metroplús) junto con una densa red de rutas integradas, buses colectivos y alimentadores. Frente a este reto de interconexión y variabilidad de tráfico en corredores críticos (Autopista Sur, Avenida Oriental, Calle San Juan, Avenida Las Vegas, entre otros), **TuRutaMed Backend** suministra una arquitectura robusta, escalable y moderna que provee:

- **Identidad, autenticación y gobernanza:** Administración centralizada de usuarios bajo esquemas criptográficos y control de acceso basado en roles (**RBAC**).
- **Cartografía y transporte multimodal:** Almacenamiento, consulta y cálculo de cercanía de rutas urbanas con paraderos georreferenciados mediante coordenadas exactas `[longitud, latitud]`.
- **Modo Waze (Reportes ciudadanos en tiempo real):** Telemetría colaborativa para el reporte y difusión de incidentes viales (congestión, siniestros, desvíos, bloqueos u obras) con indexación espacial.
- **Resiliencia operativa:** Manejador unificado de excepciones para garantizar contratos de respuesta JSON predecibles frente a anomalías de validación o fallas en bases de datos.

---

## 2. STACK TECNOLÓGICO

A continuación se detalla la suite de tecnologías, bibliotecas y herramientas que componen el núcleo de la API:

| Componente / Capa | Tecnología | Versión | Descripción y Propósito |
| :--- | :--- | :--- | :--- |
| **Framework Web** | [FastAPI](https://fastapi.tiangolo.com/) | `^0.142.2` | Framework asíncrono en Python de alto rendimiento basado en Starlette y estándares abiertos OpenAPI y JSON Schema. |
| **Servidor ASGI** | [Uvicorn](https://www.uvicorn.org/) | `^0.54.0` | Servidor ASGI ultrarrápido para Python basado en uvloop y httptools, ideal para cargas concurrentes. |
| **Validación y DTOs** | [Pydantic](https://docs.pydantic.dev/) | `^2.13.5` | Motor de parsing, validación estricta de tipos de datos de entrada/salida y definición de esquemas de API. |
| **Base de Datos Relacional** | [MySQL](https://www.mysql.com/) / [PyMySQL](https://pymysql.readthedocs.io/) | `8.0` / Driver | Persistencia ACID para gestión de cuentas de usuario, credenciales, estados de cuenta y roles de seguridad. |
| **ORM Relacional** | [SQLAlchemy](https://www.sqlalchemy.org/) | `^2.1.3` | Capa de abstracción objeto-relacional para mapeo declarativo de modelos (`Base`), sesiones transaccionales y migraciones automáticas de esquema. |
| **Base de Datos NoSQL** | [MongoDB Atlas](https://www.mongodb.com/atlas) | Cloud Cluster | Base de datos documental orientada a GeoJSON, alta concurrencia de lectura/escritura y esquemas flexibles de rutas e incidencias. |
| **Driver NoSQL** | [PyMongo](https://pymongo.readthedocs.io/) | `^4.18.2` | Driver oficial de MongoDB en Python con soporte nativo para índices espaciales `2dsphere` y operadores `$near`. |
| **Seguridad Criptográfica** | [Passlib](https://passlib.readthedocs.io/) + [Bcrypt](https://pypi.org/project/bcrypt/) | `1.7.4` / `5.0.0` | Algoritmo de hashing robusto con salazón adaptativa (adaptive salting) para contraseñas de usuarios. |
| **Autorización y Tokens** | [PyJWT](https://pyjwt.readthedocs.io/) / [Python-Jose](https://python-jose.readthedocs.io/) | `^2.15.1` | Generación, firmado y decodificación de tokens de acceso criptográficos **JWT (JSON Web Tokens)** con algoritmo `HS256`. |
| **Configuración** | [Python-Dotenv](https://pypi.org/project/python-dotenv/) | `^1.2.4` | Carga de variables de entorno desde `.env` para preservar la regla de los doce factores (12-Factor App). |

---

## 3. ARQUITECTURA DEL SISTEMA

TuRutaMed implementa un patrón de **Arquitectura de Persistencia Políglota / Híbrida**, desacoplando responsabilidades de acuerdo con la naturaleza y volumetría de los datos:

1. **Capa Relacional Transaccional (MySQL 8.0):**
   - Garantiza la integridad referencial y las propiedades ACID para identidades, credenciales cifradas, auditoría de registro y esquemas de privilegios (**RBAC**).
   - Manejada a través de sesiones unitarias (`get_mysql_db`) provistas por SQLAlchemy mediante inyección de dependencias (`Depends`).

2. **Capa NoSQL Geoespacial Distribuida (MongoDB Atlas Cloud):**
   - Almacena documentos complejos y anidados: geometrías de rutas, colecciones de paraderos ordenados e incidencias dinámicas en tiempo real.
   - Aplica indexación esférica de dos dimensiones (`2dsphere`) para procesar consultas de proximidad euclidiana/geodésica (`$near`, `$geometry: Point`, `$maxDistance`) con latencias de milisegundos.

### Diagrama Textual de Arquitectura

```text
                                       ┌──────────────────────────────────────────────┐
                                       │              CLIENTES / FRONTEND             │
                                       │  (App Móvil Flutter / Web App / Postman)     │
                                       └──────────────────────┬───────────────────────┘
                                                              │ HTTP / HTTPS (JSON)
                                                              ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                       FASTAPI CORE APPLICATION                                         │
│                                                                                                        │
│   ┌────────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              INTERCEPTOR GLOBAL DE EXCEPCIONES                                 │   │
│   │             (RequestValidationError 422, PyMongoError 500, SQLAlchemyError 500)                │   │
│   └────────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                              │                                         │
│   ┌──────────────────────────────────────────────────────────┼─────────────────────────────────────┐   │
│   │                   SISTEMA DE SEGURIDAD & AUTENTICACIÓN (JWT / HTTPBearer)                      │   │
│   │                    [verificar_contrasena]  [crear_token_acceso]  [verificar_rol_admin]         │   │
│   └──────────────────────────────────────────────────────────┼─────────────────────────────────────┘   │
│                                                              │                                         │
│               ┌──────────────────────────────┬───────────────┴──────────────┬──────────────────────┐   │
│               │                              │                              │                      │   │
│               ▼                              ▼                              ▼                      ▼   │
│      ┌─────────────────┐            ┌─────────────────┐            ┌─────────────────┐    ┌────────┴─┐ │
│      │ usuarios_router │            │  rutas_router   │            │ alertas_router  │    │ / (Raíz) │ │
│      └────────┬────────┘            └────────┬────────┘            └────────┬────────┘    └──────────┘ │
│               │                              │                              │                          │
│               │ DTOs (Pydantic)              │ DTOs (Pydantic)              │ DTOs (Pydantic)          │
│               │ UsuarioRegistro / Login      │ RutaCreate / RutaRespuesta   │ AlertaCreate / Respuesta │
│               ▼                              ▼                              ▼                          │
│      ┌─────────────────┐            ┌─────────────────┐            ┌─────────────────┐                 │
│      │ SessionLocal    │            │ Colección Rutas │            │ Colecc. Alertas │                 │
│      │ (SQLAlchemy ORM)│            │ (Índice 2dsphere│            │ (Índice 2dsphere│                 │
│      └────────┬────────┘            └────────┬────────┘            └────────┬────────┘                 │
└───────────────┼──────────────────────────────┼──────────────────────────────┼──────────────────────────┘
                │                              │                              │
                ▼                              ▼                              ▼
    ┌────────────────────────┐   ┌────────────────────────────────────────────────────────┐
    │     MOTOR MySQL 8.0    │   │               CLUSTER MONGODB ATLAS                    │
    │     (Base Relacional)  │   │              (NoSQL Documental Cloud)                  │
    │                        │   │                                                        │
    │   Tabla: `usuarios`    │   │   Colección: `rutas`     Colección: `alertas`          │
    │   - id (PK)            │   │   - nombre_ruta          - tipo_incidencia             │
    │   - email (Unique)     │   │   - tipo_transporte      - coordenadas [Lon, Lat]      │
    │   - contrasena_encrip  │   │   - paraderos: [         - fecha_reporte (ISO)         │
    │   - rol (RBAC)         │   │       coordenadas [X,Y]                                │
    │   - activo / fecha_reg │   │     ] (2dsphere index)     (2dsphere index)            │
    └────────────────────────┘   └────────────────────────────────────────────────────────┘
```

---

## 4. ESTRUCTURA DEL PROYECTO

El código fuente está estructurado de manera modular y desacoplada, separando la lógica de configuración, modelos de datos, esquemas de transferencia y controladores de ruta:

```text
TuRutaMed_Backend/
│
├── .env                              # Archivo de variables de entorno (Credenciales, JWT, DB URLs)
├── .gitignore                         # Archivos y rutas excluidas del control de versiones git
├── requirements.txt                   # Manifiesto de dependencias de Python del proyecto
├── README.md                          # Documentación técnica corporativa de la API
│
├── tests/                             # Suite de pruebas unitarias y de integración (pytest)
│   ├── __init__.py                    # Inicializador del paquete de tests
│   ├── conftest.py                    # Fixtures globales (TestClient de FastAPI)
│   └── test_usuarios.py               # Casos de prueba para endpoints de salud y autenticación
│
└── app/                               # Paquete principal del aplicativo backend
    ├── __init__.py                    # Inicializador de paquete Python
    ├── database.py                    # Motores de base de datos (Engine SQLAlchemy y MongoClient Atlas)
    ├── main.py                        # Punto de entrada de la aplicación FastAPI, routers y middlewares
    │
    ├── core/                          # Núcleo de servicios transversales del sistema
    │   ├── __init__.py                # Inicializador de módulo core
    │   ├── exceptions.py              # Interceptores globales de excepciones (422, PyMongo, SQLAlchemy)
    │   └── seguridad.py               # Hashing Passlib/Bcrypt, emisión de JWT y guardia RBAC HTTPBearer
    │
    ├── models/                        # Capa de persistencia y modelos de datos
    │   ├── __init__.py                # Inicializador de módulo models
    │   ├── alerta_mongo.py            # Operaciones PyMongo e índice 2dsphere para colección 'alertas'
    │   ├── ruta_mongo.py              # Operaciones PyMongo e índice 2dsphere para colección 'rutas'
    │   └── usuario.py                 # Modelo declarativo SQLAlchemy para tabla relacional 'usuarios'
    │
    ├── routers/                       # Controladores de endpoints y capa HTTP (APIRouters)
    │   ├── __init__.py                # Inicializador de módulo routers
    │   ├── alertas_router.py          # Endpoints de reportes de tráfico en tiempo real (Modo Waze)
    │   ├── ia_router.py               # Asistente de movilidad con Google Gemini AI (Google GenAI)
    │   ├── rutas_router.py            # Endpoints de consulta y registro geoespacial de rutas
    │   └── usuarios_router.py         # Endpoints de registro y login de usuarios con generación de JWT
    │
    └── schemas/                       # Esquemas de validación y DTOs basados en Pydantic
        ├── __init__.py                # Inicializador de módulo schemas
        ├── alerta_schema.py           # DTOs para creación y respuesta de incidencias ciudadanas
        ├── ruta_schema.py             # DTOs para validación de rutas y coordenadas de paraderos
        └── usuario_schema.py          # DTOs de registro, respuesta segura de usuario y login token
```

---

## 5. FLUJO DE UNA PETICIÓN HTTP

Para ilustrar el funcionamiento interno y la rigurosa separación de capas, a continuación se desglosan dos flujos emblemáticos del sistema:

### Caso 1: Flujo de Autenticación y Creación de Ruta (RBAC + MongoDB)

```text
[Cliente HTTP] 
   │
   │ 1. POST /usuarios/login (Envía email + contraseña plana)
   ▼
[usuarios_router.py]
   │ 2. Consulta usuario en MySQL mediante SQLAlchemy Session (get_mysql_db)
   │ 3. core/seguridad.py ejecuta `verificar_contrasena(plana, hash_bd)` con bcrypt
   │ 4. Si es válida, `crear_token_acceso(payload={"sub": email, "rol": rol})` emite JWT firmado
   ▼
[Cliente HTTP recibe Token Bearer]
   │
   │ 5. POST /rutas/ (Envía Header: `Authorization: Bearer <TOKEN>` + Body: RutaCreate JSON)
   ▼
[Seguridad / RBAC]
   │ 6. Inyección de dependencia `Depends(verificar_rol_admin)`
   │ 7. Decodifica token con SECRET_KEY y ALGORITHM (`HS256`)
   │ 8. Verifica claim `rol == "admin"`:
   │      - Si token expiró o firma no coincide -> HTTP 401 Unauthorized
   │      - Si rol != "admin" -> HTTP 403 Forbidden ("Acceso denegado")
   ▼
[Validación Pydantic: ruta_schema.py]
   │ 9. Valida tipos, nombres y formato de coordenadas de paraderos `[longitud, latitud]`
   │      - Si hay error de formato -> Dispara RequestValidationError -> Interceptor HTTP 422
   ▼
[rutas_router.py & ruta_mongo.py]
   │ 10. Ejecuta `coleccion_rutas.insert_one(ruta_dict)` en MongoDB Atlas
   │ 11. Aprovecha el índice preexistente `paraderos.coordenadas: 2dsphere`
   ▼
[Respuesta JSON al Cliente]
   HTTP 201 Created -> { "mensaje": "¡Ruta creada exitosamente...!", "id_ruta": "65b9..." }
```

### Caso 2: Reporte Ciudadano en Tiempo Real (Modo Waze) y Búsqueda Espacial

```text
[Usuario en Vía]
   │ 1. POST /alertas/ (JSON: tipo_incidencia, descripción, coordenadas=[-75.5636, 6.2518])
   ▼
[alertas_router.py & alerta_schema.py]
   │ 2. Pydantic valida estructura y tipos de datos
   │ 3. `alerta_mongo.py` añade timestamp ISO `fecha_reporte = datetime.utcnow().isoformat()`
   │ 4. Inserta el documento en colección `alertas` indizada con `2dsphere`
   ▼
[Respuesta Inmediata HTTP 201] -> {"mensaje": "¡Incidencia reportada con éxito...!", "id_alerta": "..."}

[Otros Pasajeros Consultando Rutas Cercanas]
   │ 1. GET /rutas/cercanos?longitud=-75.5583&latitud=6.2705
   ▼
[rutas_router.py -> buscar_paraderos_cercanos_db]
   │ 2. Ejecuta query geoespacial MongoDB:
   │    { "paraderos.coordenadas": { "$near": { "$geometry": { "type": "Point", "coordinates": [X, Y] }, "$maxDistance": 3000 } } }
   ▼
[Respuesta HTTP 200] -> Listado de rutas ordenadas cronológicamente por proximidad física (radio 3 km).
```

---

## 6. MÓDULOS Y ENDPOINTS

A continuación se presenta la matriz completa de endpoints expuestos por la API, organizados por módulo de negocio:

### 6.1 Módulo: Raíz e Información (`/`)

| Método | Endpoint | Descripción | Formato Body / Parámetros | Nivel de Acceso | Código HTTP Éxito |
| :---: | :--- | :--- | :--- | :---: | :---: |
| `GET` | `/` | Comprobación de estado operativo de la API. | Ninguno | **Público** | `200 OK` |
| `GET` | `/docs` | Documentación interactiva Swagger UI. | Ninguno | **Público** | `200 OK` |
| `GET` | `/redoc` | Documentación técnica alternativa ReDoc. | Ninguno | **Público** | `200 OK` |

### 6.2 Módulo: Gestión de Usuarios y Autenticación (`/usuarios`)

| Método | Endpoint | Descripción | Esquema Body (Entrada) | Nivel de Acceso | Código HTTP Éxito |
| :---: | :--- | :--- | :--- | :---: | :---: |
| `POST` | `/usuarios/registro` | Registra un nuevo usuario con contraseña encriptada (bcrypt). | `UsuarioRegistro` (nombre, email, contrasena, rol) | **Público** | `201 Created` |
| `POST` | `/usuarios/login` | Autentica credenciales y genera token de acceso JWT. | `UsuarioLogin` (email, contrasena) | **Público** | `200 OK` |

### 6.3 Módulo: Gestión de Rutas y Transporte (`/rutas`)

| Método | Endpoint | Descripción | Parámetros / Body | Nivel de Acceso | Código HTTP Éxito |
| :---: | :--- | :--- | :--- | :---: | :---: |
| `GET` | `/rutas/` | Lista todas las rutas de transporte del Valle de Aburrá. | Ninguno | **Público** | `200 OK` |
| `GET` | `/rutas/cercanos` | Búsqueda geoespacial `$near` de rutas por paraderos en radio de 3 km. | `longitud` (float), `latitud` (float) vía Query Params | **Público** | `200 OK` |
| `POST` | `/rutas/` | Registra una nueva ruta multimodal con paraderos geolocalizados. | Header `Authorization: Bearer <JWT>` + `RutaCreate` Body | **Admin (RBAC)** | `201 Created` |

### 6.4 Módulo: Modo Waze - Reportes en Tiempo Real (`/alertas`)

| Método | Endpoint | Descripción | Esquema Body (Entrada) | Nivel de Acceso | Código HTTP Éxito |
| :---: | :--- | :--- | :--- | :---: | :---: |
| `GET` | `/alertas/` | Lista todas las incidencias viales y alertas ciudadanas activas. | Ninguno | **Público** | `200 OK` |
| `POST` | `/alertas/` | Emite un nuevo reporte vial comunitario geolocalizado en la red. | `AlertaCreate` (tipo, descripción, coordenadas, ruta) | **Público** | `201 Created` |

### 6.5 Módulo: Inteligencia Artificial - Asistente TuRutaMed (`/ia`)

| Método | Endpoint | Descripción | Esquema Body (Entrada) | Nivel de Acceso | Código HTTP Éxito |
| :---: | :--- | :--- | :--- | :---: | :---: |
| `POST` | `/ia/asistente-ruta` | Consultas de movilidad y recomendaciones multimodales con Gemini 2.5 Flash. | `ConsultaMovilidadRequest` (`pregunta`: str) | **Público** | `200 OK` |

---

## 7. SEGURIDAD Y CONTROL DE ROLES

El subsistema de seguridad de TuRutaMed (`app/core/seguridad.py`) está diseñado bajo estándares modernos de la industria para APIs RESTful:

### 7.1 Criptografía y Almacenamiento Seguro de Contraseñas
- Se emplea la biblioteca **Passlib** enlazada con el motor nativo **Bcrypt** (`CryptContext(schemes=["bcrypt"], deprecated="auto")`).
- Nunca se almacenan contraseñas en texto plano. Cada contraseña ingresada sufre un proceso de dispersión unidireccional con sal aleatoria antes de persistirse en la columna `contrasena_encriptada` de MySQL.
- En el inicio de sesión, `verificar_contrasena` compara la cadena suministrada con el hash almacenado mediante comparación en tiempo constante para mitigar ataques de temporización (*timing attacks*).

### 7.2 Emisión y Validación de Tokens JWT
- Tras autenticarse exitosamente en `/usuarios/login`, el método `crear_token_acceso` ensambla un **JSON Web Token (JWT)** con:
  - `sub`: Identificador principal del usuario (correo electrónico).
  - `rol`: Rol del usuario en el sistema (`Usuario_Regular`, `Pasajero_Multimodal` o `admin`).
  - `exp`: Tiempo de caducidad fijado en UTC (`ACCESS_TOKEN_EXPIRE_MINUTES`).
- El token es firmado criptográficamente con una clave privada (`SECRET_KEY`) utilizando el algoritmo simétrico `HS256`.

### 7.3 Control de Acceso Basado en Roles (RBAC) y `HTTPBearer`
- Se utiliza el esquema `HTTPBearer` de FastAPI, permitiendo que clientes y la interfaz Swagger UI envíen el token en la cabecera estándar:
  ```http
  Authorization: Bearer <token_jwt_aqui>
  ```
- **Guardia de Autorización (`verificar_rol_admin`):**
  Actúa como interceptor en endpoints protegidos (ej. `POST /rutas/`). Decodifica el token, evalúa su firma y valida que el campo `rol` coincida exactamente con `"admin"`. En caso contrario, eleva una excepción `HTTPException(403, detail="Acceso denegado: Se requieren privilegios de administrador")`.

---

## 8. MANEJO GLOBAL DE EXCEPCIONES

Para cumplir con estándares empresariales de fiabilidad, TuRutaMed incorpora un interceptor centralizado (`app/core/exceptions.py`) registrado en el ciclo de vida de la aplicación mediante `registrar_manejadores_excepciones(app)`.

Este mecanismo captura excepciones en tiempo de ejecución y traduce fallos internos en respuestas JSON estandarizadas y predecibles, evitando fugas de información (*stack traces*) al cliente:

```text
Cliente HTTP
     │
     ▼
[Petición entrante] ──> [FastAPI Middleware Pipeline]
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
   [Error de Validación]            [Error en Base de Datos]
            │                                 │
            ├─ RequestValidationError         ├─ PyMongoError (MongoDB Atlas)
            │  -> Retorna HTTP 422            │  -> Retorna HTTP 500
            │                                 └─ SQLAlchemyError (MySQL)
            │                                    -> Retorna HTTP 500
            ▼                                 ▼
     ┌──────────────────────────────────────────────┐
     │           JSON Estandarizado Cliente         │
     │  { "estado": "error", "codigo": ..., ... }   │
     └──────────────────────────────────────────────┘
```

### Respuestas Estandarizadas por Excepción

#### 1. Error de Validación de Datos (`RequestValidationError` -> HTTP 422)
Se activa cuando el payload de una petición no respeta los tipos de datos o campos requeridos por los esquemas Pydantic:
```json
{
  "estado": "error",
  "codigo": 422,
  "mensaje": "Los datos enviados no tienen el formato correcto.",
  "detalles": [
    {
      "loc": ["body", "coordenadas"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### 2. Error de Red / Persistencia NoSQL (`PyMongoError` -> HTTP 500)
Se produce cuando se interrumpe la comunicación con el clúster de MongoDB Atlas o se produce un conflicto en consultas geoespaciales:
```json
{
  "estado": "error",
  "codigo": 500,
  "mensaje": "Error de comunicación con la base de datos geográfica (MongoDB Atlas).",
  "detalles": "ServerSelectionTimeoutError: No replica set members match selector..."
}
```

#### 3. Error en Motor Relacional (`SQLAlchemyError` -> HTTP 500)
Captura caídas del servicio MySQL, inconsistencias de clave foránea o problemas de conexión relacional, protegiendo los detalles internos del motor:
```json
{
  "estado": "error",
  "codigo": 500,
  "mensaje": "Error en el motor de usuarios y autenticación (MySQL).",
  "detalles": "Ocurrió un problema interno en el servidor."
}
```

---

## 9. GUÍA DE EJECUCIÓN LOCAL

Sigue atentamente este manual paso a paso para desplegar y ejecutar el backend de TuRutaMed en tu entorno local de desarrollo.

### 9.1 Requisitos Previos

- **Python:** Versión `3.10` o superior instalada.
- **MySQL Server:** Instancia local de MySQL 8.0 activa (puerto por defecto `3306`).
- **Cluster MongoDB Atlas:** Cuenta activa con una base de datos documental y credenciales válidas (o MongoDB Community local).
- **Git:** Herramienta de control de versiones.

---

### 9.2 Paso 1: Clonación del Repositorio

Abre una terminal y clona el proyecto en tu máquina local:

```bash
git clone https://github.com/tu-usuario-o-organizacion/TuRutaMed_Backend.git
cd TuRutaMed_Backend
```

---

### 9.3 Paso 2: Creación y Activación del Entorno Virtual

Es altamente recomendable aislar los paquetes del sistema dentro de un entorno virtual:

- **En Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```

- **En Windows (CMD):**
  ```cmd
  python -m venv venv
  .\venv\Scripts\activate.bat
  ```

- **En Linux / macOS (Bash o Zsh):**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

---

### 9.4 Paso 3: Instalación de Dependencias

Instala todas las librerías necesarias especificadas en `requirements.txt`:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> **Nota:** Si utilizas MySQL con SQLAlchemy, asegúrate de tener instalado el conector `pymysql` o `mysqlclient`. Puedes verificarlo ejecutando:
> ```bash
> pip install pymysql cryptography
> ```

---

### 9.5 Paso 4: Configuración de Variables de Entorno (`.env`)

Crea un archivo llamado `.env` en la raíz del proyecto (junto a `requirements.txt`) con la siguiente plantilla de configuración:

```env
# ==========================================
# CONFIGURACIÓN DE BASE DE DATOS MySQL (Local)
# ==========================================
# Formato: mysql+pymysql://<usuario>:<password>@<host>:<puerto>/<nombre_db>
MYSQL_URL=mysql+pymysql://root:tu_password_mysql@localhost:3306/turutamed_db

# ==========================================
# CONFIGURACIÓN DE BASE DE DATOS MongoDB (Atlas Nube)
# ==========================================
# Connection String provisto por MongoDB Atlas
MONGO_URI=mongodb+srv://<usuario>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
MONGO_DB_NAME=turutamed_db

# ==========================================
# CONFIGURACIÓN DE SEGURIDAD (Tokens JWT)
# ==========================================
# Clave privada para la firma criptográfica de los tokens
SECRET_KEY=TuRutaMed_Super_Firma_Secreta_Medellin_2026
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

> ⚠️ **IMPORTANTE:** Antes de levantar la API, asegúrate de que la base de datos `turutamed_db` existe en tu servidor MySQL:
> ```sql
> CREATE DATABASE IF NOT EXISTS turutamed_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
> ```
> Las tablas e índices espaciales se generarán automáticamente en el primer arranque de la aplicación gracias a SQLAlchemy y PyMongo.

---

### 9.6 Paso 5: Ejecución del Servidor ASGI (Uvicorn)

Inicia el servidor de desarrollo con recarga automática en caliente (*hot-reload*):

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Si el servidor arranca satisfactoriamente, observarás en la consola los mensajes de confirmación de conexión:
```text
INFO:     Will watch for changes in: ['...']
✅ Conexión preparada para MySQL local
✅ Conexión exitosa a MongoDB Atlas (Base de datos: turutamed_db)
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

### 9.7 Paso 6: Verificación y Documentación Interactiva

Abre tu navegador web de preferencia para interactuar con la plataforma:

- **Swagger UI Interactivo:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Documentación ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **Endpoint Healthcheck (Raíz):** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 10. AUTORES Y CRÉDITOS

El proyecto **TuRutaMed Backend** ha sido concebido, diseñado y desarrollado en el marco formativo y de investigación tecnológica de la:

**Institución Universitaria Tecnológico de Antioquia (TdeA)**  
*Facultad de Ingeniería — Medellín, Colombia*  
*Programa de Ingeniería de Software / Informática*

### Equipo de Desarrollo e Ingeniería

- **Juan Esteban Sánchez Duque** — *Arquitectura de Software, Backend Engineering, Seguridad JWT/RBAC e Integración Geoespacial* (T-DEA)
- **Equipo de Desarrollo TuRutaMed** — *Colaboradores y Semillero de Innovación en Transporte Inteligente del TdeA*

---

*TuRutaMed — Optimizando la movilidad, conectando el Valle de Aburrá.*
