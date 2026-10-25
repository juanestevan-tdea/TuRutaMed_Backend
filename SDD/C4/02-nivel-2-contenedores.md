# 📦 C4 Architecture - Nivel 2: Diagrama de Contenedores

> **Sistema:** TuRutaMed Backend  
> **Nivel de Abstracción:** C4 Nivel 2 - Containers  
> **Alcance:** Aplicaciones, APIs, almacenes de persistencia y servicios externos que componen la solución.  

---

## 1. Descripción del Nivel

El diagrama de contenedores descompone el sistema TuRutaMed Backend en sus principales unidades de despliegue (contenedores), mostrando cómo interactúan entre sí y con sistemas externos. Cada contenedor representa una aplicación ejecutable, una base de datos o un servicio de infraestructura autónomo.

---

## 2. Diagrama de Contenedores (Mermaid C4)

```mermaid
C4Container
    title Diagrama de Contenedores de TuRutaMed (C4 - Nivel 2)

    Person(pasajero, "Pasajero / Ciudadano", "Usuario final del transporte metropolitano.")
    Person(admin, "Operador / Administrador", "Supervisor técnico del sistema.")

    Enterprise_Boundary(turutamed, "Ecosistema TuRutaMed") {

        Container(api, "TuRutaMed API", "Python / FastAPI", "Provee endpoints REST protegidos por JWT, valida DTOs con Pydantic y orquesta casos de uso de negocio.")

        ContainerDb(mysql, "Base de Datos Relacional", "MySQL 8.0 / SQLAlchemy", "Almacena identidades de usuario, credenciales hasheadas con bcrypt, roles RBAC y auditoría de registro.")

        ContainerDb(mongo, "Base de Datos Documental", "MongoDB Atlas / PyMongo", "Almacena rutas, paraderos georreferenciados (GeoJSON), alertas, reportes y datos multimodales con índices 2dsphere.")

        Container(ia_adapter, "Adaptador de Inteligencia Artificial", "Python / google-genai", "Cliente SDK para Google Gemini 3.5 Flash-Lite. Interpreta telemetría vial y optimiza itinerarios multimodales.")

        Container(auth_module, "Módulo de Seguridad", "Python / Passlib + PyJWT", "Gestiona hashing de contraseñas, emisión y validación de tokens JWT (HS256) y control de roles.")
    }

    System_Ext(gemini_ia, "Google Gemini AI", "Servicio cloud de IA generativa.")
    System_Ext(metro_civica, "Sistema Metro Cívica", "Recaudo y validación de tarjetas de transporte.")
    System_Ext(pasarela_pagos, "Pasarela de Pagos (PSE)", "Procesamiento de recargas monetarias.")
    System_Ext(datos_abiertos, "APIs Abiertas Valle de Aburrá", "Repositorio gubernamental de datos geoespaciales.")

    Rel(pasajero, api, "Consume servicios de ruteo, reportes y saldo", "HTTPS / JSON REST")
    Rel(admin, api, "Administra rutas y modera alertas", "HTTPS / JSON REST")

    Rel(api, mysql, "Lee y escribe usuarios y roles", "TCP / SQLAlchemy ORM")
    Rel(api, mongo, "Lee y escribe rutas, alertas y reportes", "TCP / PyMongo Driver")
    Rel(api, auth_module, "Delega autenticación y autorización", "Llamada interna")
    Rel(api, ia_adapter, "Solicita optimización de itinerarios", "Llamada interna")

    Rel(ia_adapter, gemini_ia, "Envía prompts contextuales", "HTTPS / SDK google-genai")
    Rel(api, metro_civica, "Consulta saldo de tarjeta Cívica", "HTTPS / REST API")
    Rel(api, pasarela_pagos, "Procesa recargas de saldo", "HTTPS / Webhooks")
    Rel(api, datos_abiertos, "Sincroniza paraderos y trazados", "HTTPS / GeoJSON")
```

---

## 3. Catálogo de Contenedores

### 3.1. TuRutaMed API (Contenedor Principal)
- **Tecnología:** Python 3.11+ / FastAPI / Uvicorn
- **Responsabilidad:**
  - Exponer endpoints REST documentados mediante OpenAPI/Swagger.
  - Validar payloads de entrada/salida con Pydantic (DTOs).
  - Orquestar casos de uso invocando puertos del dominio y adaptadores secundarios.
  - Manejar excepciones centralizadas con códigos REST semánticos.
- **Puertos de Entrada:** `/usuarios`, `/rutas`, `/alertas`, `/ia`, `/` (health check).
- **Protocolo:** HTTPS (TLS 1.3) en producción; HTTP en desarrollo local.

### 3.2. Base de Datos Relacional (MySQL 8.0)
- **Tecnología:** MySQL 8.0 / SQLAlchemy ORM / PyMySQL Driver
- **Responsabilidad:**
  - Garantizar propiedades ACID para identidades de usuario.
  - Almacenar credenciales cifradas con `bcrypt` y control de acceso por roles (RBAC).
  - Auditoría de registro y estados de cuenta.
- **Esquema Principal:** Tabla `usuarios` (`id` PK, `email` unique, `contrasena_encrip`, `rol`, `activo`, `fecha_registro`).
- **Acceso:** Sesiones unitarias inyectadas mediante `get_mysql_db` (`Depends` de FastAPI).

### 3.3. Base de Datos Documental (MongoDB Atlas)
- **Tecnología:** MongoDB Atlas Cloud / PyMongo Driver
- **Responsabilidad:**
  - Almacenar documentos complejos y anidados: geometrías de rutas, paraderos ordenados, incidencias.
  - Soportar consultas geoespaciales de proximidad (`$near`, `$geometry: Point`, `$maxDistance`).
  - Alta concurrencia de lectura/escritura para datos de telemetría en tiempo real.
- **Colecciones:** `rutas`, `alertas` (con índice `2dsphere`).
- **Acceso:** Cliente PyMongo compartido con gestión de conexión en `app/database.py`.

### 3.4. Módulo de Seguridad (Auth)
- **Tecnología:** Passlib (bcrypt) / PyJWT / Python-Jose
- **Responsabilidad:**
  - Hashing y verificación de contraseñas con salazón adaptativa.
  - Generación y decodificación de tokens JWT firmados con `HS256`.
  - Validación de roles (`pasajero`, `operador`, `administrador`) en endpoints protegidos.
- **Integración:** Inyectado como dependencia en routers que requieren autenticación.

### 3.5. Adaptador de Inteligencia Artificial
- **Tecnología:** Python / SDK `google-genai` (modelo `gemini-3.5-flash-lite`)
- **Responsabilidad:**
  - Construir prompts contextuales con telemetría vial y alertas ciudadanas.
  - Solicitar al modelo la optimización de itinerarios multimodales (`ViajeMultimodal`).
  - Interpretar respuestas generativas y mapearlas a entidades de dominio.
- **Integración:** Servicio de aplicación invocado por los routers de IA (`app/routers/ia_router.py`).

---

## 4. Tecnologías y Decisiones de Infraestructura

| Contenedor | Imagen / Runtime | Puerto Interno | Persistencia |
| :--- | :--- | :--- | :--- |
| TuRutaMed API | `python:3.11-slim` + Uvicorn | 8000 | Ephemeral |
| MySQL 8.0 | `mysql:8.0` | 3306 | Volumen persistente |
| MongoDB Atlas | Cluster Cloud | 27017 | Cloud (Replica Set) |
| Módulo de Seguridad | In-process (librería) | N/A | N/A |
| Adaptador IA | In-process (librería) | N/A | N/A |

---

## 5. Comunicación entre Contenedores

- **Síncrona:** HTTP/HTTPS REST entre API y sistemas externos.
- **Interna:** Llamadas directas en proceso (Python) entre routers, servicios y adaptadores.
- **Asíncrona (futuro):** Colas de mensajes (RabbitMQ/Kafka) para procesamiento de alertas masivas y notificaciones push.
- **Persistencia:** Conexiones TCP directas gestionadas por SQLAlchemy (MySQL) y PyMongo (MongoDB).