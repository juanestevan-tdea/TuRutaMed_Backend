from fastapi import APIRouter, Depends, Query, status

from app.core.dependencies import get_usuario_actual
from app.database import get_mongo_db
from app.models.usuario import Usuario
from app.repositories.viaje_repository import ViajeRepository
from app.schemas.viaje_schema import (
    DuracionViajeRequest,
    DuracionViajeRespuesta,
    HistorialViajesRespuesta,
    ViajeMultimodalRequest,
    ViajeMultimodalRespuesta,
)
from app.services.viaje_service import ViajeService

router = APIRouter(prefix="/viajes", tags=["Viajes y Multimodalidad (RF-03, RF-05)"])


def get_viaje_service(db=Depends(get_mongo_db)):  # noqa: B008
    return ViajeService(ViajeRepository(db))


@router.post(
    "/calcular-duracion", response_model=DuracionViajeRespuesta, status_code=status.HTTP_200_OK
)
def calcular_duracion(
    payload: DuracionViajeRequest,
    usuario: Usuario = Depends(get_usuario_actual),  # noqa: B008
    service: ViajeService = Depends(get_viaje_service),  # noqa: B008
):
    """Calcula y persiste un viaje simple asociado al usuario autenticado (RF-03)."""
    return service.calcular_duracion(usuario, payload)


@router.post("/multimodal", response_model=ViajeMultimodalRespuesta, status_code=status.HTTP_200_OK)
def planificar_viaje_multimodal(
    payload: ViajeMultimodalRequest,
    usuario: Usuario = Depends(get_usuario_actual),  # noqa: B008
    service: ViajeService = Depends(get_viaje_service),  # noqa: B008
):
    """Construye y persiste un itinerario multimodal del usuario autenticado (RF-05)."""
    return service.planificar_multimodal(usuario, payload)


@router.get("/historial", response_model=HistorialViajesRespuesta, status_code=status.HTTP_200_OK)
def consultar_historial(
    limit: int = Query(default=10, ge=1, le=100, description="Máximo de elementos por página"),
    skip: int = Query(default=0, ge=0, description="Desplazamiento (offset)"),
    usuario: Usuario = Depends(get_usuario_actual),  # noqa: B008
    service: ViajeService = Depends(get_viaje_service),  # noqa: B008
):
    """Consulta el historial real de viajes del usuario autenticado (RF-10)."""
    return service.consultar_historial(usuario, limit=limit, skip=skip)
