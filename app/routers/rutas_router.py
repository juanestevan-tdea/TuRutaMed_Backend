from fastapi import APIRouter, Depends, Query, status

from app.core.seguridad import verificar_rol_admin
from app.database import get_mongo_db
from app.repositories.ruta_repository import RutaRepository
from app.schemas.ruta_schema import RutaCreate
from app.services.cache_service import cache_get, cache_set, make_cache_key
from app.services.ruta_service import RutaService

router = APIRouter(prefix="/rutas", tags=["Gestión de Rutas y Transporte (MongoDB)"])


def get_ruta_service(db=Depends(get_mongo_db)):  # noqa: B008
    return RutaService(RutaRepository(db))


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_ruta(
    ruta: RutaCreate,
    admin: dict = Depends(verificar_rol_admin),  # noqa: B008
    service: RutaService = Depends(get_ruta_service),  # noqa: B008
):
    """Crea una nueva ruta de transporte público (solo administradores)."""
    ruta_dict = ruta.dict(by_alias=True)
    nuevo_id = service.registrar_ruta(ruta_dict)
    return {
        "mensaje": "¡Ruta creada exitosamente en MongoDB Atlas!",
        "id_ruta": nuevo_id,
    }


@router.get("/", response_model=list[dict])
async def listar_rutas(
    limit: int = Query(default=10, ge=1, le=100, description="Máximo de elementos por página"),
    skip: int = Query(default=0, ge=0, description="Desplazamiento (offset)"),
    service: RutaService = Depends(get_ruta_service),  # noqa: B008
):
    """Obtiene el listado de rutas de transporte (público, con caché y paginación)."""
    cache_key = make_cache_key("rutas:all", limit=limit, skip=skip)
    cached = await cache_get(cache_key)
    if cached is not None:
        return cached
    rutas = service.listar_rutas()
    paginated = rutas[skip : skip + limit]
    await cache_set(cache_key, paginated)
    return paginated


@router.get("/cercanos", response_model=list[dict])
async def consultar_rutas_cercanas(
    longitud: float,
    latitud: float,
    limit: int = Query(default=10, ge=1, le=100, description="Máximo de elementos por página"),
    skip: int = Query(default=0, ge=0, description="Desplazamiento (offset)"),
    service: RutaService = Depends(get_ruta_service),  # noqa: B008
):
    """Busca rutas cercanas a una ubicación dada (público, con caché y paginación)."""
    cache_key = make_cache_key(
        "rutas:cercanos", longitud=longitud, latitud=latitud, limit=limit, skip=skip
    )
    cached = await cache_get(cache_key)
    if cached is not None:
        return cached
    rutas = service.buscar_cercanas(longitud, latitud)
    paginated = rutas[skip : skip + limit]
    await cache_set(cache_key, paginated)
    return paginated
