# 🏛️ TuRutaMed - Software Design Document (SDD)

> **Documento de Diseño de Software y Arquitectura de Sistemas**  
> **Proyecto:** TuRutaMed Backend  
> **Dominio:** Plataforma Inteligente de Transporte Público Metropolitano del Valle de Aburrá  
> **Estándar:** Modelo C4 (Context, Container, Component, Code) & Arquitectura Hexagonal / DDD  

---

## 1. Visión General y Propósito

El presente repositorio de documentación técnica compila la arquitectura, diseño conceptual, contratos de dominio y especificación de componentes de **TuRutaMed Backend**.

El objetivo central del sistema es proveer una plataforma de alta disponibilidad, orientada a microservicios y persistencia políglota, para articular la red multimodal de transporte del Área Metropolitana del Valle de Aburrá (Metro de Medellín, Metrocable, Tranvía, Metroplús, buses colectivos y rutas integradas), integrando telemetría comunitaria en tiempo real ("Modo Waze") y analítica asistida por Inteligencia Artificial generativa.

---

## 2. Estructura de Navegación del SDD

La documentación se organiza bajo una estructura modular que acompaña los distintos niveles de abstracción arquitectónica:

```text
SDD/
├── README.md                      # Índice maestro, visión general y matriz de trazabilidad
├── C4/                            # Vistas arquitectónicas basadas en el modelo C4
│   ├── 01-nivel-1-contexto.md     # Nivel 1: Diagrama de Contexto del Sistema e integraciones
│   ├── 02-nivel-2-contenedores.md # Nivel 2: Aplicaciones, APIs y almacenes de persistencia
│   └── 03-nivel-3-componentes.md   # Nivel 3: Puertos, servicios y routers internos
├── domain/                        # Modelo de Dominio y Reglas de Negocio (Core DDD)
│   ├── Domain-Model.md            # Especificación POO y UML de las 10 entidades
│   └── Ubiquitous-Language.md     # Glosario y lenguaje ubicuo metropolitano
├── Software Architecture/         # Decisiones de diseño y patrones fundamentales
│   ├── hexagonal-architecture.md  # Separación entre Núcleo, Puertos y Adaptadores
│   └── persistence-strategy.md    # Estrategia políglota (MySQL ACID + MongoDB Geoespacial)
└── Adapters/                      # Adaptadores primarios (HTTP REST) y secundarios (DB, APIs)
    ├── Primary-Adapters.md        # Routers FastAPI y controladores de entrada
    └── Secondary-Adapters.md      # Clientes PyMongo, SQLAlchemy y Google Gemini API
```

---

## 3. Matriz de Trazabilidad de Requisitos Funcionales (RF-01 a RF-10)

El núcleo de negocio de TuRutaMed responde a 10 Requisitos Funcionales unificados en `app/domain/modelos_poo.py`:

| Requisito Funcional | Denominación Oficial | Entidad POO de Dominio | Responsabilidad Técnica | Mapeo / Adaptador |
| :--- | :--- | :--- | :--- | :--- |
| **RF-01** | Consultar rutas y horarios | `Ruta` | Catálogo de itinerarios operativos y nombres de líneas. | MongoDB (`rutas`) / `rutas_router` |
| **RF-02** | Notificar cambios de servicio | `Notificacion` | Alertas viales ante bloqueos, obras o desvíos comunitarios. | MongoDB (`alertas`) / `alertas_router` |
| **RF-03** | Calcular duración del trayecto | `Viaje` | Estimación temporal en minutos entre nodos origen y destino. | Servicio de cálculo / Algoritmo Geo |
| **RF-04** | Consultar alternativas cercanas | `AlternativaTransporte` | Proximidad geoespacial ($\le 2\text{ km}$) de paraderos o estaciones. | MongoDB `$near` (`2dsphere`) |
| **RF-05** | Planificar viaje multimodal | `ViajeMultimodal` | Concatenación ordenada de tramos (Metro, Cable, Colectivo). | Gemini AI / Algoritmo de ruteo |
| **RF-06** | Calificar y reportar servicio | `ReporteServicio` | Registro de valoración cualitativa y cuantitativa (1-5 estrellas). | MongoDB (`reportes`) / API |
| **RF-07** | Consultar saldo tarjeta Cívica | `TarjetaCivica` | Estado de saldo en tiempo real para validadores Metro. | Gateway Cívica / Endpoint seguro |
| **RF-08** | Recargar tarjeta Cívica | `RecargaCivica` | Integración transaccional con pasarelas de pago (PSE/Bancos). | Gateway Financiero / Transacciones |
| **RF-09** | Filtrar por accesibilidad | `RutaAccesible` | Especialización de `Ruta` con atributos PMR (movilidad reducida). | MongoDB (`rutas.accesible`) |
| **RF-10** | Consultar historial y estadísticas | `HistorialViajes` | Métricas y trazabilidad de desplazamientos por usuario. | Persistencia de viajes / Dashboard |

---

## 4. Pilares Arquitectónicos y Principios Inviolables

1. **Arquitectura Hexagonal (Ports & Adapters):**
   - **Dominio Puro (`app/domain/`):** Aislado de librerías externas o frameworks; sin acoplamiento a FastAPI ni Pymongo.
   - **Puertos y Servicios de Aplicación (`app/services/`):** Orquestación de casos de uso y llamadas a servicios de IA.
   - **Adaptadores Primarios (`app/routers/`):** Controladores FastAPI que gestionan protocolos HTTP/JSON y autenticación JWT.
   - **Adaptadores Secundarios (`app/models/`, `app/database.py`):** Conectores a bases de datos relacionales y NoSQL.

2. **Fuente Única de Verdad (Single Source of Truth - DRY):**
   - El archivo `app/domain/modelos_poo.py` concentra las 10 entidades de dominio base. Ningún modelo debe duplicar la lógica de negocio nuclear.

3. **Tipado Estático y Resiliencia:**
   - Tipado estricto mediante `typing` estándar (`str`, `int`, `float`, `bool`, `List`, `Optional`, `Dict`).
   - Manejador centralizado de excepciones en `app/core/exceptions.py` con códigos semánticos REST.

4. **Persistencia Políglota Estratégica:**
   - **MySQL 8.0:** Garantía ACID e integridad referencial para cuentas de usuario, contraseñas hasheadas (`bcrypt`) y roles de acceso (**RBAC**).
   - **MongoDB Atlas:** Modelo documental para geolocalización indexada (`2dsphere`), geometrías GeoJSON e incidentes en tiempo real.
