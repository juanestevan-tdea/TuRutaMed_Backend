from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.civica_schema import (
    SaldoCivicaRespuesta,
    RecargaCivicaRequest,
    RecargaCivicaRespuesta,
)
from app.domain.modelos_poo import TarjetaCivica, RecargaCivica
from app.core.seguridad import get_current_user

router = APIRouter(prefix="/civica", tags=["Tarjeta Cívica (RF-07, RF-08)"])

# Almacén en memoria para simular persistencia de tarjetas (demo/testing)
_tarjetas: dict = {}


def _obtener_o_crear_tarjeta(tarjeta_id: str) -> TarjetaCivica:
    """Obtiene una tarjeta existente o crea una nueva con saldo inicial de 0."""
    if tarjeta_id not in _tarjetas:
        _tarjetas[tarjeta_id] = TarjetaCivica(numero=tarjeta_id, saldo=0.0)
    return _tarjetas[tarjeta_id]


@router.get("/saldo/{tarjeta_id}", response_model=SaldoCivicaRespuesta)
def consultar_saldo(tarjeta_id: str):
    """Consulta el saldo disponible de una tarjeta Cívica (RF-07)."""
    tarjeta = _obtener_o_crear_tarjeta(tarjeta_id)
    return SaldoCivicaRespuesta(
        tarjeta_id=tarjeta.numero,
        saldo=tarjeta.consultar_saldo(),
    )


@router.post("/recargar", response_model=RecargaCivicaRespuesta, status_code=status.HTTP_200_OK)
def recargar_tarjeta(payload: RecargaCivicaRequest, current_user: dict = Depends(get_current_user)):
    """Procesa una recarga de saldo a una tarjeta Cívica (RF-08). Requiere JWT."""
    tarjeta = _obtener_o_crear_tarjeta(payload.tarjeta_id)
    saldo_anterior = tarjeta.consultar_saldo()

    recarga = RecargaCivica(monto=payload.monto, metodo_de_pago=payload.metodo_de_pago)
    if not recarga.procesar_pago():
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="El pago no pudo ser procesado por la pasarela.",
        )

    tarjeta.saldo += payload.monto
    _tarjetas[payload.tarjeta_id] = tarjeta

    return RecargaCivicaRespuesta(
        tarjeta_id=payload.tarjeta_id,
        monto_recargado=payload.monto,
        saldo_anterior=saldo_anterior,
        saldo_nuevo=tarjeta.consultar_saldo(),
        metodo_de_pago=payload.metodo_de_pago,
    )