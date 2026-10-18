from pydantic import BaseModel, Field


class ReporteServicioRequest(BaseModel):
    calificacion: int = Field(..., ge=1, le=5, example=5)
    comentario_ciudadano: str = Field(..., example="Excelente servicio, puntual y limpio.")


class ReporteServicioRespuesta(BaseModel):
    calificacion: int
    comentario_ciudadano: str
    guardado: bool = True
    mensaje: str = "Reporte registrado exitosamente"
