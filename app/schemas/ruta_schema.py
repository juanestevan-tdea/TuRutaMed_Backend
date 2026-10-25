from pydantic import BaseModel, Field


class Paradero(BaseModel):
    nombre_paradero: str
    # En GeoJSON y MongoDB, el orden obligatorio es [longitud, latitud]
    # Longitud de Medellín gira al rededor de -75.56, Latitud alrededor de 6.25
    coordenadas: list[float] = Field(
        ...,
        json_schema_extra={"example": [-75.5583, 6.2705]},
    )
    orden: int


class RutaCreate(BaseModel):
    nombre_ruta: str = Field(
        ...,
        json_schema_extra={"example": "Manrique Oriental - Centro (Integrado)"},
    )
    tipo_transporte: str = Field(
        ...,
        json_schema_extra={"example": "Bus Colectivo"},
    )
    origen: str = Field(
        ...,
        json_schema_extra={"example": "Manrique Oriental"},
    )
    destino: str = Field(
        ...,
        json_schema_extra={"example": "Estación Parque Berrio"},
    )
    tiempo_estimado_minutos: int = Field(
        ...,
        json_schema_extra={"example": 25},
    )
    paraderos: list[Paradero] = []


class RutaRespuesta(RutaCreate):
    id: str | None = Field(None, alias="_id")
