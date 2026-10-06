from fastapi import FastAPI
from app.database import engine, Base
from app.models.usuario import Usuario
from app.routers import usuarios_router, rutas_router, alertas_router
from app.routers.ia_router import router as ia_router
from app.core.exceptions import registrar_manejadores_excepciones

# Inicializar tablas en MySQL
Base.metadata.create_all(bind=engine)

# Instancia de la aplicación FastAPI
app = FastAPI(
    title="TuRutaMed API",
    description="Backend para el sistema de gestión de rutas y transporte multimodal.",
    version="1.0.0"
)

# REGISTRAR EXCEPCIONES GLOBALES
registrar_manejadores_excepciones(app)

# REGISTRO DE ROUTERS MODULARES
app.include_router(usuarios_router.router)
app.include_router(rutas_router.router)
app.include_router(alertas_router.router)
app.include_router(ia_router)

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
