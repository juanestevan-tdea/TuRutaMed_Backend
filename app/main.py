from fastapi import FastAPI
from app.database import engine, Base
from app.models.usuario import Usuario  # Importamos nuestro nuevo molde
from fastapi import FastAPI
from app.database import engine, Base
from app.models.usuario import Usuario
from app.routers import usuarios_router, rutas_router
from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.ruta_schema import RutaCreate, RutaRespuesta
from app.models.ruta_mongo import insertar_ruta_db, obtener_todas_las_rutas_db
Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/rutas", tags=["Gestión de Rutas y Transporte (MongoDB)"])

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_ruta(ruta: RutaCreate):
    """Crea una nueva ruta de transporte público con sus paraderos geolocalizados"""
    ruta_dict = ruta.dict(by_alias=True)
    nuevo_id = insertar_ruta_db(ruta_dict)
    return {
        "mensaje": "¡Ruta creada exitosamente en MongoDB Atlas!",
        "id_ruta": nuevo_id
    }

@router.get("/", response_model=List[dict])
def listar_rutas():
    """Obtiene el listado completo de rutas de transporte registradas"""
    rutas = obtener_todas_las_rutas_db()
    return rutas

# ¡La magia de SQLAlchemy! 
# Esto revisa MySQL y si la tabla "usuarios" no existe, la crea automáticamente.
Base.metadata.create_all(bind=engine)

# Inicializamos la aplicación FastAPI
app = FastAPI(
    title="TuRutaMed API",
    description="Backend para el sistema de gestión de rutas y transporte multimodal.",
    version="1.0.0"
)

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
        "seguridad": "JWT Auth en construcción"
    }
    

app = FastAPI(
    title="TuRutaMed API",
    description="Backend para el sistema de gestión de rutas y transporte multimodal.",
    version="1.0.0"
)

# CONECTAMOS LAS RUTAS DE USUARIOS AL SERVIDOR
app.include_router(usuarios_router.router)

@app.get("/", tags=["Inicio"])
def leer_raiz():
    return {"mensaje": "¡Bienvenido a la API de TuRutaMed!"}
    

app = FastAPI(
    title="TuRutaMed API",
    description="Backend para el sistema de gestión de rutas y transporte multimodal.",
    version="1.0.0"
)

# CONECTAMOS LOS ROUTERS AL SERVIDOR
app.include_router(usuarios_router.router)
app.include_router(rutas_router.router)  # <--- INCLUIMOS LAS RUTAS DE TRANSPORTE

@app.get("/", tags=["Inicio"])
def leer_raiz():
    return {"mensaje": "¡Bienvenido a la API de TuRutaMed!"}
from fastapi import FastAPI
from app.database import engine, Base
from app.models.usuario import Usuario
from app.routers import usuarios_router, rutas_router, alertas_router  # <--- IMPORTAR ALERTAS

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TuRutaMed API",
    description="Backend para el sistema de gestión de rutas y transporte multimodal.",
    version="1.0.0"
)

app.include_router(usuarios_router.router)
app.include_router(rutas_router.router)
app.include_router(alertas_router.router)  # <--- INCLUIR EN EL APP

@app.get("/", tags=["Inicio"])
def leer_raiz():
    return {"mensaje": "¡Bienvenido a la API de TuRutaMed!"}

from fastapi import FastAPI
from app.database import engine, Base
from app.models.usuario import Usuario
from app.routers import usuarios_router, rutas_router, alertas_router
from app.core.exceptions import registrar_manejadores_excepciones  # <--- IMPORTAR

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TuRutaMed API",
    description="Backend para el sistema de gestión de rutas y transporte multimodal.",
    version="1.0.0"
)

# REGISTRAR EXCEPCIONES GLOBALES
registrar_manejadores_excepciones(app)

app.include_router(usuarios_router.router)
app.include_router(rutas_router.router)
app.include_router(alertas_router.router)

@app.get("/", tags=["Inicio"])
def leer_raiz():
    return {"mensaje": "¡Bienvenido a la API de TuRutaMed!"}