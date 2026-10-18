# 💾 Estrategia de Persistencia Políglota

> **Patrón:** Persistencia Políglota (Polyglot Persistence)  
> **Bases de Datos:** MySQL 8.0 (Relacional) + MongoDB Atlas (Documental/Geoespacial)  
> **Principio:** Seleccionar el motor de persistencia adecuado según la naturaleza y volumetría de los datos.  

---

## 1. Visión General

TuRutaMed implementa una **arquitectura de persistencia políglota**, desacoplando responsabilidades de acuerdo con la naturaleza y volumetría de los datos. Esta decisión arquitectónica responde a la necesidad de combinar:

- **Integridad transaccional (ACID)** para datos de identidad y seguridad.
- **Flexibilidad documental y geoespacial** para rutas, paraderos e incidencias en tiempo real.

---

## 2. Justificación de la Estrategia Políglota

| Criterio | MySQL 8.0 (Relacional) | MongoDB Atlas (Documental) |
| :--- | :--- | :--- |
| **Naturaleza de datos** | Estructurados, tabulares, relaciones fuertes | Semi-estructurados, anidados, geoespaciales |
| **Consistencia** | ACID (transacciones fuertes) | Eventual (BASE) |
| **Escalabilidad** | Vertical (escala hacia arriba) | Horizontal (sharding, replica sets) |
| **Consultas** | SQL complejo, joins, agregaciones | Documentos, índices geoespaciales, agregaciones |
| **Casos de uso** | Usuarios, roles, auditoría | Rutas, paraderos, alertas, reportes |
| **Latencia** | Baja para consultas indexadas | Baja para documentos y geoespacial |

---

## 3. Distribución de Datos por Motor

### 3.1. MySQL 8.0 — Capa Relacional Transaccional

**Responsabilidad:** Garantizar integridad referencial y propiedades ACID para identidades, credenciales y auditoría.

**Esquema Principal:**

```sql
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    contrasena_encrip VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    rol ENUM('pasajero', 'operador', 'administrador') DEFAULT 'pasajero',
    activo BOOLEAN DEFAULT TRUE,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_rol (rol)
);
```

**Datos Almacenados:**
- Identidades de usuario (email, nombre).
- Credenciales hasheadas con `bcrypt`.
- Roles de acceso (RBAC).
- Estados de cuenta (activo/inactivo).
- Auditoría de registro (fecha, IP, dispositivo).

**Ventajas:**
- Transacciones ACID para operaciones críticas.
- Integridad referencial mediante claves foráneas.
- Consultas complejas con SQL estándar.
- Madurez del ecosistema y herramientas de administración.

---

### 3.2. MongoDB Atlas — Capa NoSQL Geoespacial Distribuida

**Responsabilidad:** Almacenar documentos complejos, geometrías y datos de telemetría en tiempo real con indexación geoespacial.

**Colecciones:**

#### Colección `rutas`
```json
{
  "_id": "ObjectId",
  "nombre_ruta": "Manrique Oriental - Centro (Integrado)",
  "tipo_transporte": "Bus Colectivo",
  "origen": "Manrique Oriental",
  "destino": "Estación Parque Berrio",
  "tiempo_estimado_minutos": 25,
  "coordenadas": [-75.5583, 6.2705],
  "paraderos": [
    { "nombre": "Paradero Manrique", "coordenadas": [-75.5590, 6.2710] },
    { "nombre": "Paradero Centro", "coordenadas": [-75.5630, 6.2520] }
  ],
  "accesible": true,
  "horario": "05:00 - 23:00",
  "fecha_actualizacion": "2026-10-17T14:30:00Z"
}
```

**Índices:**
- `2dsphere` sobre `coordenadas` (búsquedas radiales).
- `text` sobre `nombre_ruta` (búsqueda full-text).
- `compound` sobre `tipo_transporte` + `accesible`.

#### Colección `alertas`
```json
{
  "_id": "ObjectId",
  "tipo_incidencia": "congestion",
  "descripcion": "Tráfico pesado por obra en la Oriental",
  "coordenadas": [-75.5636, 6.2518],
  "nombre_ruta": "Manrique Oriental - Centro (Integrado)",
  "fecha_reporte": "2026-10-17T14:30:00Z",
  "reportado_por": "usr_01",
  "estado": "activa"
}
```

**Índices:**
- `2dsphere` sobre `coordenadas`.
- `descending` sobre `fecha_reporte` (orden cronológico inverso).
- `compound` sobre `tipo_incidencia` + `estado`.

**Datos Almacenados:**
- Rutas con geometrías y paraderos.
- Alertas viales con coordenadas geoespaciales.
- Reportes ciudadanos y calificaciones.
- Historial de viajes multimodales.

**Ventajas:**
- Esquema flexible para datos anidados y heterogéneos.
- Indexación geoespacial nativa (`2dsphere`).
- Alta concurrencia de lectura/escritura.
- Escalabilidad horizontal mediante sharding.
- Replicación automática (Replica Sets) para alta disponibilidad.

---

## 4. Patrones de Acceso a Datos

### 4.1. Consulta de Rutas Cercanas (RF-01, RF-04)

```python
# MongoDB: Búsqueda radial con $near
db.rutas.find(
    {
        "coordenadas": {
            "$near": {
                "$geometry": {"type": "Point", "coordinates": [lon, lat]},
                "$maxDistance": 2000,  # 2 km en metros
            }
        }
    }
)
```

### 4.2. Consulta de Alertas Cercanas (RF-02)

```python
# MongoDB: Alertas en radio de proximidad
db.alertas.find(
    {
        "coordenadas": {
            "$near": {
                "$geometry": {"type": "Point", "coordinates": [lon, lat]},
                "$maxDistance": 5000,  # 5 km en metros
            }
        },
        "estado": "activa",
    }
).sort("fecha_reporte", -1).limit(20)
```

### 4.3. Autenticación de Usuario (RF implícito)

```python
# MySQL: Consulta por email
SELECT id, email, contrasena_encrip, rol, activo
FROM usuarios
WHERE email = ? AND activo = TRUE;
```

### 4.4. Filtrado por Accesibilidad (RF-09)

```python
# MongoDB: Rutas accesibles
db.rutas.find(
    {
        "accesible": True,
        "coordenadas": {
            "$near": {
                "$geometry": {"type": "Point", "coordinates": [lon, lat]},
                "$maxDistance": 2000,
            }
        },
    }
)
```

---

## 5. Sincronización y Consistencia

### 5.1. Consistencia Eventual entre Motores

- **MySQL** es la fuente de verdad para identidades y roles.
- **MongoDB** es la fuente de verdad para rutas, alertas y datos geoespaciales.
- No existe sincronización bidireccional entre motores; cada uno gestiona su dominio de datos.

### 5.2. Transacciones Distribuidas (Futuro)

Para operaciones que requieran consistencia entre ambos motores (ej. recarga Cívica que actualiza saldo y registra transacción), se considera implementar:

- **Saga Pattern:** Secuencia de transacciones locales con compensación.
- **Outbox Pattern:** Registro de eventos en tabla MySQL con publicación asíncrona a MongoDB.

---

## 6. Estrategia de Backup y Recuperación

| Motor | Estrategia | Frecuencia | Retención |
| :--- | :--- | :--- | :--- |
| MySQL 8.0 | Dump completo (`mysqldump`) | Diario (02:00 UTC) | 30 días |
| MySQL 8.0 | Binlog (Point-in-Time Recovery) | Continuo | 7 días |
| MongoDB Atlas | Snapshots automáticos | Cada 6 horas | 30 días |
| MongoDB Atlas | Oplog (Point-in-Time Recovery) | Continuo | 24 horas |

---

## 7. Monitoreo y Observabilidad

### 7.1. Métricas de Base de Datos

- **MySQL:** Conexiones activas, queries lentas, tamaño de tablas, latencia de transacciones.
- **MongoDB:** Operaciones por segundo, latencia de consultas geoespaciales, tamaño de colecciones, uso de índices.

### 7.2. Alertas

- **MySQL:** Conexiones > 80% del pool, queries > 1s, espacio en disco < 20%.
- **MongoDB:** Latencia de consultas > 100ms, uso de memoria > 80%, fallos de replicación.

### 7.3. Endpoint de Salud

```
GET /health
Response: {
    "status": "healthy",
    "mysql": "connected",
    "mongodb": "connected",
    "gemini": "available"
}
```

---

## 8. Escalabilidad y Evolución

### 8.1. Escalabilidad Horizontal

- **MongoDB:** Sharding por `coordenadas` (geohash) para distribuir datos geoespaciales.
- **MySQL:** Read replicas para consultas de solo lectura; escritura en instancia primaria.

### 8.2. Caché (Futuro)

- **Redis:** Caché de rutas frecuentes y sesiones de usuario.
- **TTL:** 5 minutos para rutas, 1 hora para sesiones.

### 8.3. Migración de Esquemas

- **MySQL:** Alembic (migraciones versionadas con SQLAlchemy).
- **MongoDB:** Migraciones manuales con scripts Python; validación de esquema con JSON Schema (opcional).

---

## 9. Convenciones de Implementación

1. **Separación de Conexiones:** Cada motor tiene su propio módulo de conexión en `app/database.py`.
2. **Pool de Conexiones:** Configurado por motor con límites de pool y timeouts.
3. **Transacciones:** MySQL usa transacciones explícitas; MongoDB usa sesiones para operaciones multi-documento.
4. **Mapeo de Entidades:** Los adaptadores secundarios mapean entre modelos de persistencia y entidades de dominio.
5. **Testing:** Pruebas de integración con bases de datos en memoria (SQLite para MySQL, mongomock para MongoDB).