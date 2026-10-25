"""Capa de servicio para la tarjeta Cívica (MySQL)."""

from decimal import ROUND_HALF_UP, Decimal

from app.core.exceptions import DomainException
from app.domain.modelos_poo import RecargaCivica
from app.repositories.civica_repository import CivicaRepository
from app.schemas.civica_schema import (
    RecargaCivicaRequest,
    RecargaCivicaRespuesta,
    SaldoCivicaRespuesta,
)

CENTAVOS = Decimal("0.01")


def _a_decimal(valor: object) -> Decimal:
    return Decimal(str(valor or 0)).quantize(CENTAVOS, rounding=ROUND_HALF_UP)


class CivicaService:
    def __init__(self, repository: CivicaRepository) -> None:
        self.repository = repository

    def consultar_saldo(self, tarjeta_id: str) -> SaldoCivicaRespuesta:
        tarjeta = self.repository.obtener_o_crear(tarjeta_id)
        return SaldoCivicaRespuesta(
            tarjeta_id=tarjeta.numero,
            saldo=float(_a_decimal(tarjeta.saldo)),
        )

    def recargar(self, payload: RecargaCivicaRequest) -> RecargaCivicaRespuesta:
        tarjeta = self.repository.obtener_para_actualizar(payload.tarjeta_id)
        saldo_anterior = _a_decimal(tarjeta.saldo)

        recarga = RecargaCivica(monto=payload.monto, metodo_de_pago=payload.metodo_de_pago)
        if not recarga.es_valida():
            raise DomainException(
                message="La solicitud de recarga no es válida.",
                code="INVALID_RECHARGE",
                status_code=422,
            )

        monto = _a_decimal(payload.monto)
        tarjeta.saldo = saldo_anterior + monto
        self.repository.guardar(tarjeta)

        return RecargaCivicaRespuesta(
            tarjeta_id=tarjeta.numero,
            monto_recargado=float(monto),
            saldo_anterior=float(saldo_anterior),
            saldo_nuevo=float(_a_decimal(tarjeta.saldo)),
            metodo_de_pago=payload.metodo_de_pago,
        )
