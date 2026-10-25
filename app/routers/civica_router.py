from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session

from app.core.seguridad import get_current_user
from app.database import get_mysql_db
from app.repositories.civica_repository import CivicaRepository
from app.schemas.civica_schema import (
    RecargaCivicaRequest,
    RecargaCivicaRespuesta,
    SaldoCivicaRespuesta,
)
from app.services.civica_service import CivicaService

router = APIRouter(prefix="/civica", tags=["Tarjeta Cívica (RF-07, RF-08)"])


def get_civica_service(db: Session = Depends(get_mysql_db)) -> CivicaService:  # noqa: B008
    return CivicaService(CivicaRepository(db))


@router.get("/saldo/{tarjeta_id}", response_model=SaldoCivicaRespuesta)
def consultar_saldo(
    tarjeta_id: str = Path(..., min_length=1, max_length=32),
    service: CivicaService = Depends(get_civica_service),  # noqa: B008
):
    """Consulta el saldo de una tarjeta Cívica persistida en MySQL (RF-07)."""
    return service.consultar_saldo(tarjeta_id)


@router.post(
    "/recargar",
    response_model=RecargaCivicaRespuesta,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
def recargar_tarjeta(
    payload: RecargaCivicaRequest,
    service: CivicaService = Depends(get_civica_service),  # noqa: B008
):
    """Recarga saldo y lo persiste de forma transaccional en MySQL (RF-08)."""
    return service.recargar(payload)
