from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.ruta_schema import RutaCreate, RutaRespuesta
from app.models.ruta_mongo import insertar_ruta_db, obtener_todas_las_rutas_db



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

# Asegúrate de importar la función buscar_paraderos_cercanos_db desde app.models.ruta_mongo
from app.models.ruta_mongo import (
    insertar_ruta_db, 
    obtener_todas_las_rutas_db, 
    buscar_paraderos_cercanos_db
)

# (Mantén tus rutas anteriores y añade esta nueva)

@router.get("/cercanos", response_model=List[dict])
def consultar_rutas_cercanas(longitud: float, latitud: float):
    """
    Busca las rutas de transporte público cuyos paraderos estén cerca 
    de la ubicación enviada (ej. Longitud: -75.5451, Latitud: 6.2752).
    """
    rutas = buscar_paraderos_cercanos_db(longitud, latitud)
    return rutas

from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.schemas.ruta_schema import RutaCreate, RutaRespuesta
from app.models.ruta_mongo import (
    insertar_ruta_db, 
    obtener_todas_las_rutas_db, 
    buscar_paraderos_cercanos_db
)
# Importamos la seguridad para verificar que sea administrador
from app.core.seguridad import verificar_rol_admin

router = APIRouter(prefix="/rutas", tags=["Gestión de Rutas y Transporte (MongoDB)"])

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_ruta(ruta: RutaCreate, admin: dict = Depends(verificar_rol_admin)):
    """
    Crea una nueva ruta de transporte público. 
    ¡Protegido! Solo accesible para usuarios con rol de administrador (JWT).
    """
    ruta_dict = ruta.dict(by_alias=True)
    nuevo_id = insertar_ruta_db(ruta_dict)
    return {
        "mensaje": "¡Ruta creada exitosamente por el administrador en MongoDB Atlas!",
        "id_ruta": nuevo_id
    }

@router.get("/", response_model=List[dict])
def listar_rutas():
    """Obtiene el listado completo de rutas de transporte registradas (Público)"""
    rutas = obtener_todas_las_rutas_db()
    return rutas

@router.get("/cercanos", response_model=List[dict])
def consultar_rutas_cercanas(longitud: float, latitud: float):
    """Busca rutas cercanas a una ubicación dada (Público)"""
    rutas = buscar_paraderos_cercanos_db(longitud, latitud)
    return rutas