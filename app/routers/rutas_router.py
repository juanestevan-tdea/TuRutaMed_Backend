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

from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List
from app.schemas.ruta_schema import RutaCreate, RutaRespuesta
from app.models.ruta_mongo import (
    insertar_ruta_db,
    obtener_todas_las_rutas_db,
    buscar_paraderos_cercanos_db,
)
from app.core.seguridad import verificar_rol_admin
from app.services.cache_service import cache_get, cache_set, make_cache_key

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
async def listar_rutas(
    limit: int = Query(default=10, ge=1, le=100, description="Máximo de elementos por página"),
    skip: int = Query(default=0, ge=0, description="Desplazamiento (offset)"),
):
    """Obtiene el listado completo de rutas de transporte registradas (Público). Con caché Redis (5 min) y paginación."""
    cache_key = make_cache_key("rutas:all", limit=limit, skip=skip)
    cached = await cache_get(cache_key)
    if cached is not None:
        return cached
    rutas = obtener_todas_las_rutas_db()
    paginated = rutas[skip:skip + limit]
    await cache_set(cache_key, paginated)
    return paginated


@router.get("/cercanos", response_model=List[dict])
async def consultar_rutas_cercanas(
    longitud: float,
    latitud: float,
    limit: int = Query(default=10, ge=1, le=100, description="Máximo de elementos por página"),
    skip: int = Query(default=0, ge=0, description="Desplazamiento (offset)"),
):
    """Busca rutas cercanas a una ubicación dada (Público). Con caché Redis (5 min) y paginación."""
    cache_key = make_cache_key("rutas:cercanos", longitud=longitud, latitud=latitud, limit=limit, skip=skip)
    cached = await cache_get(cache_key)
    if cached is not None:
        return cached
    rutas = buscar_paraderos_cercanos_db(longitud, latitud)
    paginated = rutas[skip:skip + limit]
    await cache_set(cache_key, paginated)
    return paginated