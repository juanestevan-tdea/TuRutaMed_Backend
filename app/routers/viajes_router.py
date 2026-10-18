from fastapi import APIRouter, Depends, Query, status

from app.core.seguridad import get_current_user
from app.domain.modelos_poo import Viaje, ViajeMultimodal
from app.schemas.viaje_schema import (
    DuracionViajeRequest,
    DuracionViajeRespuesta,
    ViajeMultimodalRequest,
    ViajeMultimodalRespuesta,
)

router = APIRouter(prefix="/viajes", tags=["Viajes y Multimodalidad (RF-03, RF-05)"])


@router.post("/calcular-duracion", response_model=DuracionViajeRespuesta, status_code=status.HTTP_200_OK)
def calcular_duracion(payload: DuracionViajeRequest):
    """Estima la duración de un viaje entre origen y destino (RF-03)."""
    viaje = Viaje(
        origen=payload.origen,
        destino=payload.destino,
        duracion_minutos=payload.duracion_minutos,
    )
    return DuracionViajeRespuesta(
        origen=viaje.origen,
        destino=viaje.destino,
        duracion_minutos=viaje.calcular_duracion(),
    )


@router.post("/multimodal", response_model=ViajeMultimodalRespuesta, status_code=status.HTTP_200_OK)
def planificar_viaje_multimodal(payload: ViajeMultimodalRequest):
    """Construye un itinerario combinado Metro/Bus/Cable (RF-05)."""
    viaje_m = ViajeMultimodal(secuencia_rutas=payload.secuencia_rutas)
    return ViajeMultimodalRespuesta(
        secuencia_rutas=viaje_m.secuencia_rutas,
        itinerario=viaje_m.mostrar_secuencia(),
    )


@router.get("/historial", status_code=status.HTTP_200_OK)
def consultar_historial(
    limit: int = Query(default=10, ge=1, le=100, description="Máximo de elementos por página"),
    skip: int = Query(default=0, ge=0, description="Desplazamiento (offset)"),
    current_user: dict = Depends(get_current_user),  # noqa: B008
):
    """Consulta el historial de viajes del usuario autenticado (RF-10). Requiere JWT. Con paginación."""
    historial = []
    paginated = historial[skip:skip + limit]
    return {
        "usuario": current_user.get("sub"),
        "historial": paginated,
        "total": len(historial),
        "limit": limit,
        "skip": skip,
        "mensaje": "Historial consultado exitosamente",
    }
