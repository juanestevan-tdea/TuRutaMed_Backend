from fastapi import APIRouter, Depends, status

from app.core.seguridad import get_current_user
from app.domain.modelos_poo import ReporteServicio
from app.schemas.reporte_schema import ReporteServicioRequest, ReporteServicioRespuesta

router = APIRouter(prefix="/reportes", tags=["Reportes Ciudadanos (RF-06)"])


@router.post("/", response_model=ReporteServicioRespuesta, status_code=status.HTTP_201_CREATED)
def registrar_reporte(
    payload: ReporteServicioRequest, current_user: dict = Depends(get_current_user)
):  # noqa: B008
    """Registra una calificación y comentario sobre el servicio de transporte (RF-06). Requiere JWT."""
    reporte = ReporteServicio(
        calificacion=payload.calificacion,
        comentario_ciudadano=payload.comentario_ciudadano,
    )
    guardado = reporte.guardar_reporte()
    return ReporteServicioRespuesta(
        calificacion=reporte.calificacion,
        comentario_ciudadano=reporte.comentario_ciudadano,
        guardado=guardado,
    )
