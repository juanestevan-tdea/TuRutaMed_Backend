from unittest.mock import MagicMock

import pytest

from app.core.exceptions import ConflictError, UnauthorizedError
from app.schemas.usuario_schema import UsuarioLogin, UsuarioRegistro
from app.services.usuario_service import UsuarioService


def _registro() -> UsuarioRegistro:
    return UsuarioRegistro(
        nombre="Test User",
        email="test@example.com",
        password="secret123",  # noqa: S106
        rol="Usuario_Regular",
    )


def test_registrar_usuario_conflict():
    repo = MagicMock()
    repo.obtener_por_email.return_value = MagicMock()  # ya existe
    service = UsuarioService(repo)

    with pytest.raises(ConflictError):
        service.registrar_usuario(_registro())

    repo.crear_usuario.assert_not_called()


def test_registrar_usuario_crea():
    repo = MagicMock()
    repo.obtener_por_email.return_value = None
    repo.crear_usuario.return_value = MagicMock()
    service = UsuarioService(repo)

    service.registrar_usuario(_registro())

    repo.crear_usuario.assert_called_once()


def test_iniciar_sesion_no_user():
    repo = MagicMock()
    repo.obtener_por_email.return_value = None
    service = UsuarioService(repo)

    with pytest.raises(UnauthorizedError):
        service.iniciar_sesion(UsuarioLogin(email="x@y.com", password="pw"))  # noqa: S106
