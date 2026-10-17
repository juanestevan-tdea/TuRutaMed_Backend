from pydantic import BaseModel, Field
from typing import List, Optional


class DuracionViajeRequest(BaseModel):
    origen: str = Field(..., example="Poblado")
    destino: str = Field(..., example="Niquía")
    duracion_minutos: int = Field(..., gt=0, example=35)


class DuracionViajeRespuesta(BaseModel):
    origen: str
    destino: str
    duracion_minutos: int
    mensaje: str = "Duración calculada exitosamente"


class ViajeMultimodalRequest(BaseModel):
    secuencia_rutas: List[str] = Field(
        ..., example=["Metro Línea A", "Metrocable Línea K", "Bus Alimentador"]
    )


class ViajeMultimodalRespuesta(BaseModel):
    secuencia_rutas: List[str]
    itinerario: str
    mensaje: str = "Itinerario multimodal generado exitosamente"