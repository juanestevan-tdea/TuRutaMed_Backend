from datetime import datetime

from pydantic import BaseModel, Field


class DuracionViajeRequest(BaseModel):
    origen: str = Field(
        ...,
        json_schema_extra={"example": "Poblado"},
    )
    destino: str = Field(
        ...,
        json_schema_extra={"example": "Niquía"},
    )
    duracion_minutos: int = Field(
        ...,
        gt=0,
        json_schema_extra={"example": 35},
    )


class DuracionViajeRespuesta(BaseModel):
    origen: str
    destino: str
    duracion_minutos: int
    mensaje: str = "Duración calculada exitosamente"


class ViajeMultimodalRequest(BaseModel):
    secuencia_rutas: list[str] = Field(
        ...,
        min_length=1,
        json_schema_extra={"example": ["Metro Línea A", "Metrocable Línea K", "Bus Alimentador"]},
    )


class ViajeMultimodalRespuesta(BaseModel):
    secuencia_rutas: list[str]
    itinerario: str
    mensaje: str = "Itinerario multimodal generado exitosamente"


class ViajeHistorialItem(BaseModel):
    id: str
    tipo: str
    origen: str | None = None
    destino: str | None = None
    duracion_minutos: int | None = None
    secuencia_rutas: list[str] | None = None
    itinerario: str | None = None
    fecha_creacion: datetime | None = None


class HistorialViajesRespuesta(BaseModel):
    usuario: str
    historial: list[ViajeHistorialItem]
    total: int
    limit: int
    skip: int
    mensaje: str = "Historial consultado exitosamente"
