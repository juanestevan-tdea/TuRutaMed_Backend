# 📖 Lenguaje Ubicuo (Ubiquitous Language)

> **Contexto:** Domain-Driven Design (DDD)  
> **Dominio:** Transporte Público Metropolitano del Valle de Aburrá  
> **Propósito:** Glosario de términos compartidos entre desarrolladores, stakeholders y usuarios.  

---

## 1. Visión General

El **Lenguaje Ubicuo** es un vocabulario compartido y preciso utilizado por todos los miembros del equipo (desarrolladores, analistas, stakeholders y usuarios) para describir el dominio del transporte público metropolitano. Este glosario asegura que el código, la documentación y las conversaciones utilicen los mismos términos, evitando ambigüedades y desalineaciones.

---

## 2. Términos del Dominio de Transporte

### 2.1. Infraestructura de Transporte

| Término | Definición | Contexto de Uso |
| :--- | :--- | :--- |
| **Metro de Medellín** | Sistema de transporte masivo ferroviario que conecta el norte (Niquía) con el sur (La Estrella) del Valle de Aburrá. | Rutas, estaciones, horarios |
| **Metrocable** | Sistema de teleférico integrado al Metro que conecta comunas periféricas con la red masiva (Líneas K, J, H, M, P). | Viajes multimodales, accesibilidad |
| **Tranvía de Ayacucho** | Sistema de tranvía que conecta el centro de Medellín con el oriente (San Antonio - Oriente). | Rutas, estaciones, horarios |
| **Metroplús** | Sistema de buses articulados que opera en corredores exclusivos (Autopista Sur, Calle 80). | Rutas, paraderos, horarios |
| **Bus Colectivo** | Vehículo de transporte público que opera en rutas urbanas e intermunicipales sin carril exclusivo. | Rutas, paraderos, alternativas |
| **Alimentador** | Bus que conecta barrios periféricos con estaciones del Metro o Metrocable. | Viajes multimodales, conexiones |
| **Encicla** | Sistema de bicicletas públicas compartidas del Área Metropolitana del Valle de Aburrá. | Alternativas de transporte |
| **Paradero** | Punto de parada designado para buses y vehículos de transporte público. | Geolocalización, cercanía |
| **Estación** | Infraestructura física de acceso al Metro, Metrocable o Tranvía. | Rutas, accesibilidad, PMR |
| **Nodo de Transferencia** | Punto donde el pasajero cambia de un modo de transporte a otro (ej. Estación San Antonio). | Viajes multimodales |

### 2.2. Tarjeta y Recaudo

| Término | Definición | Contexto de Uso |
| :--- | :--- | :--- |
| **Tarjeta Cívica** | Tarjeta inteligente sin contacto utilizada para pagar pasajes en el Metro de Medellín y sistemas integrados. | Saldo, recarga, validación |
| **Recarga** | Proceso de acreditación de saldo monetario a una Tarjeta Cívica mediante pasarelas de pago. | Transacciones, PSE, bancos |
| **Validador** | Dispositivo electrónico que lee la Tarjeta Cívica y descuenta el pasaje al ingresar a una estación. | Cobro, saldo, tiempo real |
| **Saldo** | Cantidad monetaria disponible en pesos colombianos (COP) en la Tarjeta Cívica. | Consulta, recarga, alertas |
| **PSE** | Pagos Seguros en Línea: sistema de pago electrónico interbancario colombiano. | Recarga, pasarela de pagos |
| **Pasarela de Pagos** | Servicio externo que procesa transacciones financieras (PSE, Redeban, tarjetas). | Recarga, confirmación, webhook |

### 2.3. Movilidad y Accesibilidad

| Término | Definición | Contexto de Uso |
| :--- | :--- | :--- |
| **PMR** | Personas con Movilidad Reducida: usuarios que requieren adaptaciones de accesibilidad (rampas, ascensores, piso bajo). | Filtro de accesibilidad, rutas |
| **Ruta Accesible** | Ruta o estación que cuenta con infraestructura para PMR (rampas, elevadores, buses de piso bajo). | RF-09, filtrado, inclusión |
| **Caminabilidad** | Distancia peatonal máxima aceptable para considerar una alternativa de transporte como "cercana" (≤ 2 km). | RF-04, proximidad |
| **Geolocalización** | Posicionamiento geográfico del usuario mediante coordenadas `[longitud, latitud]`. | Paraderos, rutas cercanas, alertas |
| **Radio de Proximidad** | Distancia máxima (en metros) para considerar un punto de interés como cercano al usuario. | Consultas `$near`, geoespacial |

### 2.4. Telemetría y Reportes

| Término | Definición | Contexto de Uso |
| :--- | :--- | :--- |
| **Modo Waze** | Funcionalidad colaborativa que permite a los usuarios reportar incidentes viales en tiempo real. | Alertas, congestión, bloqueos |
| **Alerta Vial** | Notificación de un incidente de tránsito (congestión, siniestro, desvío, bloqueo, obra). | RF-02, reporte ciudadano |
| **Incidencia** | Evento que afecta el flujo normal del tránsito o el servicio de transporte. | Alertas, análisis, IA |
| **Calificación** | Valoración numérica (1-5 estrellas) del servicio de transporte por parte del ciudadano. | RF-06, calidad, métricas |
| **Reporte Ciudadano** | Retroalimentación textual y cuantitativa del pasajero sobre la calidad del servicio. | RF-06, dashboard, análisis |

### 2.5. Planificación y Ruteo

| Término | Definición | Contexto de Uso |
| :--- | :--- | :--- |
| **Viaje Multimodal** | Itinerario que combina múltiples modos de transporte (Metro + Metrocable + Bus + Encicla). | RF-05, optimización, IA |
| **Secuencia de Rutas** | Lista ordenada cronológicamente de los tramos que componen un viaje multimodal. | `ViajeMultimodal`, itinerario |
| **Tramo** | Segmento individual de un viaje que utiliza un solo modo de transporte. | Secuencia, conexión, transferencia |
| **Duración Estimada** | Tiempo proyectado en minutos para completar un trayecto en condiciones normales. | RF-03, planificación |
| **Origen** | Punto de partida del viaje (estación, paradero o dirección). | Viaje, ruteo, geolocalización |
| **Destino** | Punto de arribo del viaje (estación, paradero o dirección). | Viaje, ruteo, geolocalización |

---

## 3. Términos Técnicos y de Arquitectura

### 3.1. Arquitectura y Patrones

| Término | Definición | Contexto de Uso |
| :--- | :--- | :--- |
| **Arquitectura Hexagonal** | Patrón que organiza el sistema en capas concéntricas protegiendo el dominio de dependencias externas. | Puertos, adaptadores, dominio |
| **Puerto (Port)** | Interfaz que define un contrato de comunicación entre el dominio y el exterior. | Servicios, adaptadores |
| **Adaptador (Adapter)** | Implementación concreta de un puerto que conecta con una tecnología específica. | Routers, DB connectors, APIs |
| **Dominio (Domain)** | Núcleo de negocio con entidades y reglas, libre de dependencias externas. | `modelos_poo.py`, DDD |
| **Servicio de Aplicación** | Orquestador de casos de uso que coordina entidades de dominio y adaptadores. | `app/services/` |
| **DTO (Data Transfer Object)** | Objeto que transporta datos entre capas sin lógica de negocio. | Pydantic schemas, API |
| **RBAC** | Role-Based Access Control: control de acceso basado en roles (pasajero, operador, administrador). | Seguridad, autorización |
| **JWT** | JSON Web Token: token firmado criptográficamente para autenticación stateless. | Seguridad, sesiones |
| **DRY** | Don't Repeat Yourself: principio de fuente única de verdad. | `modelos_poo.py` |

### 3.2. Persistencia y Datos

| Término | Definición | Contexto de Uso |
| :--- | :--- | :--- |
| **Persistencia Políglota** | Uso de múltiples motores de base de datos según la naturaleza de los datos. | MySQL + MongoDB |
| **ACID** | Atomicity, Consistency, Isolation, Durability: propiedades de transacciones relacionales. | MySQL, integridad |
| **BASE** | Basically Available, Soft state, Eventual consistency: propiedades de sistemas NoSQL. | MongoDB, escalabilidad |
| **2dsphere** | Índice geoespacial de MongoDB para consultas de proximidad en esfera terrestre. | `$near`, geolocalización |
| **GeoJSON** | Formato estándar para representar datos geoespaciales (Point, Polygon, LineString). | Coordenadas, rutas |
| **Replica Set** | Conjunto de nodos MongoDB que replican datos para alta disponibilidad. | MongoDB Atlas, failover |
| **Sharding** | Particionamiento horizontal de datos para escalabilidad. | MongoDB, volumetría |

### 3.3. Inteligencia Artificial

| Término | Definición | Contexto de Uso |
| :--- | :--- | :--- |
| **Gemini AI** | Modelo de lenguaje generativo de Google (gemini-2.5-flash) para optimización de rutas. | IA Service, recomendaciones |
| **Prompt Contextual** | Instrucción estructurada enviada a Gemini con telemetría vial y alertas. | Optimización, análisis |
| **Optimización Multimodal** | Proceso de IA que sugiere la mejor combinación de transportes para un viaje. | RF-05, ViajeMultimodal |
| **Análisis Predictivo** | Predicción de congestión vial a partir de alertas ciudadanas históricas. | IA, dashboard, operadores |

---

## 4. Mapeo de Términos a Entidades de Dominio

| Término de Negocio | Entidad POO | Requisito Funcional |
| :--- | :--- | :--- |
| Ruta / Línea de transporte | `Ruta` | RF-01 |
| Ruta con accesibilidad PMR | `RutaAccesible` | RF-09 |
| Alerta / Notificación de servicio | `Notificacion` | RF-02 |
| Trayecto / Desplazamiento | `Viaje` | RF-03 |
| Paradero / Estación cercana | `AlternativaTransporte` | RF-04 |
| Itinerario combinado | `ViajeMultimodal` | RF-05 |
| Calificación / Reporte | `ReporteServicio` | RF-06 |
| Tarjeta Cívica | `TarjetaCivica` | RF-07 |
| Recarga de saldo | `RecargaCivica` | RF-08 |
| Historial de viajes | `HistorialViajes` | RF-10 |

---

## 5. Convenciones de Nombrado

### 5.1. Entidades y Clases
- **PascalCase** para clases: `RutaAccesible`, `TarjetaCivica`, `HistorialViajes`.
- **snake_case** para atributos y métodos: `consultar_horario`, `esta_cerca`, `viajes_realizados`.
- **Nombres descriptivos** que reflejen el dominio: `cumple_filtro_accesibilidad` en lugar de `check`.

### 5.2. Routers y Servicios
- **Sufijo `_router`** para adaptadores primarios: `usuarios_router`, `rutas_router`.
- **Sufijo `_service`** para servicios de aplicación: `usuarios_service`, `rutas_service`.
- **Sufijo `_adapter`** para adaptadores secundarios: `mysql_adapter`, `mongo_adapter`.

### 5.3. DTOs (Pydantic)
- **Sufijo `Create`** para payloads de creación: `RutaCreate`, `AlertaCreate`.
- **Sufijo `Respuesta`** para respuestas: `UsuarioRespuesta`, `RutaRespuesta`.
- **Sufijo `Request`/`Response`** para endpoints de IA: `OptimizarRutaRequest`.

---

## 6. Reglas de Comunicación

1. **Un término, un significado:** Cada término del lenguaje ubicuo tiene una única definición en todo el sistema.
2. **Código refleja el dominio:** Los nombres de clases, métodos y variables deben usar el lenguaje ubicuo.
3. **Documentación alineada:** Toda documentación SDD utiliza los términos definidos en este glosario.
4. **Evolución controlada:** Nuevos términos se agregan a este glosario antes de implementarse en código.
5. **Traducción prohibida:** No se traducen términos técnicos ni de dominio al inglés en el código (ej. usar `RutaAccesible`, no `AccessibleRoute`).