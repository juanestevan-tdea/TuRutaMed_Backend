"""Capa de servicio para los reportes ciudadanos (MongoDB)."""

from datetime import UTC, datetime

from app.models.usuario import Usuario
from app.repositories.reporte_repository import ReporteRepository
from app.schemas.reporte_schema import ReporteServicioRequest, ReporteServicioRespuesta


class ReporteService:
    def __init__(self, repository: ReporteRepository) -> None:
        self.repository = repository

    def registrar(
        self, usuario: Usuario, payload: ReporteServicioRequest
    ) -> ReporteServicioRespuesta:
        fecha_reporte = datetime.now(UTC)
        documento = {
            "usuario_id": usuario.id,
            "usuario_email": usuario.email,
            "calificacion": payload.calificacion,
            "comentario_ciudadano": payload.comentario_ciudadano,
            "fecha_reporte": fecha_reporte,
        }
        id_reporte = self.repository.crear(documento)
        return ReporteServicioRespuesta(
            id_reporte=id_reporte,
            calificacion=payload.calificacion,
            comentario_ciudadano=payload.comentario_ciudadano,
            guardado=True,
            fecha_reporte=fecha_reporte,
        )
