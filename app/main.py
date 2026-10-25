import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from prometheus_fastapi_instrumentator import Instrumentator
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.api.v1.health import router as health_router
from app.core.config import get_settings
from app.core.exceptions import registrar_manejadores_excepciones
from app.core.logging import configure_logging
from app.core.middleware import RequestIDMiddleware
from app.core.rate_limit import limiter
from app.database import Base, engine, get_mongo_db
from app.database_seeder import seed_rutas_if_empty
from app.routers import alertas_router, rutas_router, usuarios_router
from app.routers.civica_router import router as civica_router
from app.routers.ia_router import router as ia_router
from app.routers.reportes_router import router as reportes_router
from app.routers.viajes_router import router as viajes_router
from app.services.cache_service import get_redis_client

logger = logging.getLogger(__name__)

configure_logging()

settings = get_settings()

# Inicializar tablas en MySQL.
# No debe bloquear el arranque: si MySQL está caído, /health/live debe seguir respondiendo.
try:
    Base.metadata.create_all(bind=engine)
except Exception as exc:  # noqa: BLE001
    logger.warning(
        "No se pudieron inicializar las tablas de MySQL; la API arrancará en modo "
        "degradado y los endpoints que usan MySQL fallarán: %s",
        exc,
    )

# Instancia de la aplicación FastAPI
app = FastAPI(
    title=settings.app_name,
    description="API REST para planificacion multimodal, consulta de saldo Civica y alertas de movilidad en el Valle de Aburra.",
    version=settings.app_version,
    openapi_tags=[
        {
            "name": "Usuarios",
            "description": "Registro, autenticación y gestión de usuarios (RBAC).",
        },
        {
            "name": "Gestión de Rutas y Transporte (MongoDB)",
            "description": "Consulta de rutas, paraderos y geolocalización.",
        },
        {
            "name": "Modo Waze - Reportes en Tiempo Real (MongoDB)",
            "description": "Reporte y consulta de alertas viales geoespaciales.",
        },
        {
            "name": "Tarjeta Cívica (RF-07, RF-08)",
            "description": "Consulta de saldo y recarga de tarjeta Cívica.",
        },
        {
            "name": "Viajes y Multimodalidad (RF-03, RF-05)",
            "description": "Cálculo de duración e itinerarios multimodales.",
        },
        {
            "name": "Reportes Ciudadanos (RF-06)",
            "description": "Registro de calificaciones y reportes del servicio.",
        },
        {
            "name": "Inteligencia Artificial - Asistente TuRutaMed",
            "description": "Recomendaciones multimodales con Gemini AI.",
        },
        {"name": "Inicio", "description": "Endpoints de salud y estado del sistema."},
    ],
)

# REGISTRAR EXCEPCIONES GLOBALES
registrar_manejadores_excepciones(app)

# Health checks (sin prefijo de versión para orquestadores)
app.include_router(health_router)

app.state.limiter = limiter
app.add_middleware(RequestIDMiddleware)
app.add_middleware(SlowAPIMiddleware)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "type": "https://turutamed.com/errors/RATE_LIMIT_EXCEEDED",
            "title": "Too Many Requests",
            "status": 429,
            "detail": "Rate limit exceeded. Please try again later.",
            "instance": str(request.url.path),
        },
    )


# MIDDLEWARE CORS
# Vite puede abrirse como localhost o como 127.0.0.1: ambos orígenes deben
# funcionar siempre, además de los configurados en CORS_ORIGINS.
CORS_ORIGINS_LOCALES = (
    "http://localhost:5173",
    "http://127.0.0.1:5173",
)
cors_origins = list(dict.fromkeys([*settings.cors_origins, *CORS_ORIGINS_LOCALES]))

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REGISTRO DE ROUTERS MODULARES
app.include_router(usuarios_router.router)
app.include_router(rutas_router.router)
app.include_router(alertas_router.router)
app.include_router(ia_router)
app.include_router(civica_router)
app.include_router(viajes_router)
app.include_router(reportes_router)

# Alias versionado /api/v1 para consumo del frontend (mantiene rutas raíz para compatibilidad con tests)
for _r in (
    usuarios_router.router,
    rutas_router.router,
    alertas_router.router,
    ia_router,
    civica_router,
    viajes_router,
    reportes_router,
):
    app.include_router(_r, prefix="/api/v1")

# Seeder automático al iniciar: sincroniza (upsert) el catálogo SITVA y asegura
# el índice 2dsphere. No borra rutas personalizadas; para un reset total:
#   python -m app.database_seeder --force
try:
    _mongo_db = get_mongo_db()
    if _mongo_db is not None:
        seed_rutas_if_empty(_mongo_db)
except Exception as _e:  # noqa: BLE001
    print(f"[Seeder] No se pudo ejecutar el seeder automatico: {_e}")


@app.get("/api/v1/health", tags=["Inicio"])
async def health_check():
    """Verificación del estado del sistema y sus dependencias."""
    mongo_status = "disconnected"
    redis_status = "disconnected"
    try:
        db = get_mongo_db()
        if db is not None:
            db.client.admin.command("ping")
            mongo_status = "connected"
    except Exception:  # noqa: BLE001
        mongo_status = "error"

    try:
        client = await get_redis_client()
        if client is not None:
            await client.ping()
            redis_status = "connected"
    except Exception:  # noqa: BLE001
        redis_status = "error"

    return {
        "status": "healthy",
        "version": settings.app_version,
        "dependencies": {
            "mongodb": mongo_status,
            "redis": redis_status,
        },
    }


@app.get("/", tags=["Inicio"])
def leer_raiz():
    return {
        "mensaje": "¡Bienvenido a la API de TuRutaMed!",
        "estado": "Servidor funcionando correctamente al 100%",
    }


@app.get("/estado-roles", tags=["Pruebas"])
def probar_roles():
    return {
        "roles_soportados": ["Usuario", "Pasajero", "Administrador_Sistema"],
        "roles_registro": ["Usuario", "Pasajero"],
        "seguridad": (
            "JWT Auth activo con RBAC; el registro público no permite roles administrativos"
        ),
    }


# Métricas Prometheus (interno, sin rate limit)
Instrumentator().instrument(app)


@app.get("/metrics", include_in_schema=False)
@limiter.exempt
def metrics(request: Request):
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
