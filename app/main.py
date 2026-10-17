from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models.usuario import Usuario
from app.routers import usuarios_router, rutas_router, alertas_router
from app.routers.ia_router import router as ia_router
from app.routers.civica_router import router as civica_router
from app.routers.viajes_router import router as viajes_router
from app.routers.reportes_router import router as reportes_router
from app.core.exceptions import registrar_manejadores_excepciones
from app.database_seeder import seed_rutas_if_empty
from app.database import get_mongo_db
from app.services.cache_service import get_redis_client
import asyncio

# Inicializar tablas en MySQL
Base.metadata.create_all(bind=engine)

# Instancia de la aplicación FastAPI
app = FastAPI(
    title="TuRutaMed API - Sistema de Transporte Inteligente",
    description="API REST para planificación multimodal, consulta de saldo Cívica y alertas de movilidad en el Valle de Aburrá.",
    version="2.5.0",
    openapi_tags=[
        {"name": "Usuarios", "description": "Registro, autenticación y gestión de usuarios (RBAC)."},
        {"name": "Gestión de Rutas y Transporte (MongoDB)", "description": "Consulta de rutas, paraderos y geolocalización."},
        {"name": "Modo Waze - Reportes en Tiempo Real (MongoDB)", "description": "Reporte y consulta de alertas viales geoespaciales."},
        {"name": "Tarjeta Cívica (RF-07, RF-08)", "description": "Consulta de saldo y recarga de tarjeta Cívica."},
        {"name": "Viajes y Multimodalidad (RF-03, RF-05)", "description": "Cálculo de duración e itinerarios multimodales."},
        {"name": "Reportes Ciudadanos (RF-06)", "description": "Registro de calificaciones y reportes del servicio."},
        {"name": "Inteligencia Artificial - Asistente TuRutaMed", "description": "Recomendaciones multimodales con Gemini AI."},
        {"name": "Inicio", "description": "Endpoints de salud y estado del sistema."},
    ],
)

# REGISTRAR EXCEPCIONES GLOBALES
registrar_manejadores_excepciones(app)

# MIDDLEWARE CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

# Seeder automático al iniciar si la colección está vacía (solo si Mongo está disponible)
try:
    _mongo_db = get_mongo_db()
    if _mongo_db is not None:
        seed_rutas_if_empty(_mongo_db)
except Exception as _e:
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
    except Exception:
        mongo_status = "error"

    try:
        client = await get_redis_client()
        if client is not None:
            await client.ping()
            redis_status = "connected"
    except Exception:
        redis_status = "error"

    return {
        "status": "healthy",
        "version": "2.5.0",
        "dependencies": {
            "mongodb": mongo_status,
            "redis": redis_status,
        },
    }


@app.get("/", tags=["Inicio"])
def leer_raiz():
    return {
        "mensaje": "¡Bienvenido a la API de TuRutaMed!",
        "estado": "Servidor funcionando correctamente al 100%"
    }

@app.get("/estado-roles", tags=["Pruebas"])
def probar_roles():
    return {
        "roles_soportados": ["Usuario_Regular", "Pasajero_Multimodal", "Administrador_Sistema"],
        "seguridad": "JWT Auth activo con RBAC"
    }

@app.get("/", tags=["Inicio"])
def leer_raiz():
    return {
        "mensaje": "¡Bienvenido a la API de TuRutaMed!",
        "estado": "Servidor funcionando correctamente al 100%"
    }

@app.get("/estado-roles", tags=["Pruebas"])
def probar_roles():
    return {
        "roles_soportados": ["Usuario_Regular", "Pasajero_Multimodal", "Administrador_Sistema"],
        "seguridad": "JWT Auth activo con RBAC"
    }
