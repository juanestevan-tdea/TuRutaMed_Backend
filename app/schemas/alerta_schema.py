
from pydantic import BaseModel, Field


class AlertaCreate(BaseModel):
    tipo_incidencia: str = Field(..., example="Congestión / Taco")
    descripcion: str = Field(..., example="Tráfico pesado por obra o manifestación en la Oriental")
    coordenadas: list[float] = Field(..., example=[-75.5636, 6.2518]) # [longitud, latitud]
    nombre_ruta: str | None = Field(None, example="Manrique Oriental - Centro (Integrado)")

class AlertaRespuesta(AlertaCreate):
    id: str | None = Field(None, alias="_id")
    fecha_reporte: str | None = None
