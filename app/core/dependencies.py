"""Dependencias compartidas de FastAPI que combinan autenticación y MySQL."""

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.core.seguridad import get_current_user
from app.database import get_mysql_db
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository


def get_usuario_actual(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_mysql_db),
) -> Usuario:
    """Resuelve el usuario real de MySQL a partir del claim ``sub`` del JWT."""
    email = current_user.get("sub")
    if not email:
        raise UnauthorizedError(message="El token no contiene un usuario válido")

    usuario = UsuarioRepository(db).obtener_por_email(str(email))
    if usuario is None:
        raise UnauthorizedError(message="El usuario autenticado no existe")
    if usuario.activo is False:
        raise ForbiddenError(message="La cuenta del usuario está inactiva")
    return usuario
