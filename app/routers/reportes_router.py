from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_usuario_actual
from app.database import get_mongo_db
from app.models.usuario import Usuario
from app.repositories.reporte_repository import ReporteRepository
from app.schemas.reporte_schema import ReporteServicioRequest, ReporteServicioRespuesta
from app.services.reporte_service import ReporteService

router = APIRouter(prefix="/reportes", tags=["Reportes Ciudadanos (RF-06)"])


def get_reporte_service(db=Depends(get_mongo_db)):  # noqa: B008
    return ReporteService(ReporteRepository(db))


@router.post("/", response_model=ReporteServicioRespuesta, status_code=status.HTTP_201_CREATED)
def registrar_reporte(
    payload: ReporteServicioRequest,
    usuario: Usuario = Depends(get_usuario_actual),  # noqa: B008
    service: ReporteService = Depends(get_reporte_service),  # noqa: B008
):
    """Persiste la calificación y el comentario del usuario autenticado (RF-06)."""
    return service.registrar(usuario, payload)
