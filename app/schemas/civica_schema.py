
from pydantic import BaseModel, Field


class SaldoCivicaRespuesta(BaseModel):
    tarjeta_id: str = Field(..., example="123456")
    saldo: float = Field(..., example=15000.0)
    moneda: str = Field(default="COP", example="COP")


class RecargaCivicaRequest(BaseModel):
    tarjeta_id: str = Field(..., example="123456")
    monto: float = Field(..., gt=0, example=20000.0)
    metodo_de_pago: str = Field(..., example="PSE")


class RecargaCivicaRespuesta(BaseModel):
    tarjeta_id: str
    monto_recargado: float
    saldo_anterior: float
    saldo_nuevo: float
    metodo_de_pago: str
    exitoso: bool = True
    mensaje: str = "Recarga procesada exitosamente"
