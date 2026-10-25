from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class ReporteServicioRequest(BaseModel):
    calificacion: int = Field(
        ...,
        ge=1,
        le=5,
        json_schema_extra={"example": 5},
    )
    comentario_ciudadano: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        json_schema_extra={"example": "Excelente servicio, puntual y limpio."},
    )

    @field_validator("comentario_ciudadano")
    @classmethod
    def _comentario_no_vacio(cls, value: str) -> str:
        comentario = value.strip()
        if not comentario:
            raise ValueError("El comentario no puede estar vacío")
        return comentario


class ReporteServicioRespuesta(BaseModel):
    id_reporte: str | None = None
    calificacion: int
    comentario_ciudadano: str
    guardado: bool = True
    fecha_reporte: datetime | None = None
    mensaje: str = "Reporte registrado exitosamente"
