from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_mysql_db
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario_schema import (
    Token,
    UsuarioLogin,
    UsuarioRegistro,
    UsuarioRespuesta,
)
from app.services.usuario_service import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


def get_usuario_service(db: Session = Depends(get_mysql_db)):  # noqa: B008
    repository = UsuarioRepository(db)
    return UsuarioService(repository)


@router.post("/registro", response_model=UsuarioRespuesta, status_code=status.HTTP_201_CREATED)
def registrar_usuario(
    usuario_in: UsuarioRegistro,
    service: UsuarioService = Depends(get_usuario_service),  # noqa: B008
):
    return service.registrar_usuario(usuario_in)


@router.post("/login", response_model=Token)
def iniciar_sesion(
    usuario_in: UsuarioLogin,
    service: UsuarioService = Depends(get_usuario_service),  # noqa: B008
):
    return service.iniciar_sesion(usuario_in)
