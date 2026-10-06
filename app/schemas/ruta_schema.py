from pydantic import BaseModel, Field
from typing import List, Optional

class Paradero(BaseModel):
    nombre_paradero: str
    # En GeoJSON y MongoDB, el orden obligatorio es [longitud, latitud]
    # Longitud de Medellín gira al rededor de -75.56, Latitud alrededor de 6.25
    coordenadas: List[float] = Field(..., example=[-75.5583, 6.2705])
    orden: int

class RutaCreate(BaseModel):
    nombre_ruta: str = Field(..., example="Manrique Oriental - Centro (Integrado)")
    tipo_transporte: str = Field(..., example="Bus Colectivo")
    origen: str = Field(..., example="Manrique Oriental")
    destino: str = Field(..., example="Estación Parque Berrio")
    tiempo_estimado_minutos: int = Field(..., example=25)
    paraderos: List[Paradero] = []

class RutaRespuesta(RutaCreate):
    id: Optional[str] = Field(None, alias="_id")