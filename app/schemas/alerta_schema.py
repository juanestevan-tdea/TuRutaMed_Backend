from pydantic import BaseModel, Field
from typing import List, Optional

class AlertaCreate(BaseModel):
    tipo_incidencia: str = Field(..., example="Congestión / Taco")
    descripcion: str = Field(..., example="Tráfico pesado por obra o manifestación en la Oriental")
    coordenadas: List[float] = Field(..., example=[-75.5636, 6.2518]) # [longitud, latitud]
    nombre_ruta: Optional[str] = Field(None, example="Manrique Oriental - Centro (Integrado)")

class AlertaRespuesta(AlertaCreate):
    id: Optional[str] = Field(None, alias="_id")
    fecha_reporte: Optional[str] = None