from pydantic import BaseModel, Field, field_validator


class SaldoCivicaRespuesta(BaseModel):
    tarjeta_id: str = Field(
        ...,
        json_schema_extra={"example": "123456"},
    )
    saldo: float = Field(
        ...,
        json_schema_extra={"example": 15000.0},
    )
    moneda: str = Field(
        default="COP",
        json_schema_extra={"example": "COP"},
    )


class RecargaCivicaRequest(BaseModel):
    tarjeta_id: str = Field(
        ...,
        min_length=1,
        max_length=32,
        json_schema_extra={"example": "123456"},
    )
    monto: float = Field(
        ...,
        ge=0.01,
        le=9_999_999_999.99,
        json_schema_extra={"example": 20000.0},
    )
    metodo_de_pago: str = Field(
        ...,
        min_length=1,
        json_schema_extra={"example": "PSE"},
    )

    @field_validator("metodo_de_pago")
    @classmethod
    def _metodo_no_vacio(cls, value: str) -> str:
        metodo = value.strip()
        if not metodo:
            raise ValueError("El método de pago no puede estar vacío")
        return metodo


class RecargaCivicaRespuesta(BaseModel):
    tarjeta_id: str
    monto_recargado: float
    saldo_anterior: float
    saldo_nuevo: float
    metodo_de_pago: str
    exitoso: bool = True
    mensaje: str = "Recarga procesada exitosamente"
