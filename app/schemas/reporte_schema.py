from pydantic import BaseModel, Field


class ReporteServicioRequest(BaseModel):
    calificacion: int = Field(
        ...,
        ge=1,
        le=5,
        json_schema_extra={"example": 5},
    )
    comentario_ciudadano: str = Field(
        ...,
        json_schema_extra={"example": "Excelente servicio, puntual y limpio."},
    )


class ReporteServicioRespuesta(BaseModel):
    calificacion: int
    comentario_ciudadano: str
    guardado: bool = True
    mensaje: str = "Reporte registrado exitosamente"
