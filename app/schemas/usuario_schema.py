from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

# Roles que un cliente puede elegir al registrarse. Nunca incluye roles
# administrativos: esos solo se asignan fuera del flujo público (BD/seed).
RolPublico = Literal["Usuario", "Pasajero"]

ROL_POR_DEFECTO: RolPublico = "Usuario"
ROLES_PUBLICOS: frozenset[str] = frozenset({"Usuario", "Pasajero"})

# Compatibilidad con los nombres históricos del dominio.
ROLES_ALIAS: dict[str, str] = {
    "Usuario_Regular": "Usuario",
    "Pasajero_Multimodal": "Pasajero",
}


def normalizar_rol_publico(rol: str | None) -> str | None:
    """Devuelve el rol canónico permitido o None si no está en la allowlist."""
    valor = (rol or ROL_POR_DEFECTO).strip()
    valor = ROLES_ALIAS.get(valor, valor)
    return valor if valor in ROLES_PUBLICOS else None


# Esto es lo que PEDIMOS al usuario cuando se registra
class UsuarioRegistro(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    nombre: str
    email: EmailStr
    contrasena: str = Field(alias="password")
    rol: RolPublico = ROL_POR_DEFECTO

    @field_validator("rol", mode="before")
    @classmethod
    def _normalizar_rol(cls, value):
        """Normaliza aliases y deja que Literal rechace cualquier rol no público."""
        if value is None:
            return ROL_POR_DEFECTO
        if not isinstance(value, str):
            return value
        normalizado = normalizar_rol_publico(value)
        return normalizado if normalizado is not None else value


# Esto es lo que DEVOLVEMOS al usuario (jamás devolvemos la contraseña)
class UsuarioRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    email: str
    rol: str
    activo: bool
    fecha_registro: datetime


# Lo que pedimos para el Login
class UsuarioLogin(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    email: EmailStr
    contrasena: str = Field(alias="password")


# Lo que devolvemos si el login es exitoso
class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"  # noqa: S105


class RefreshTokenRequest(BaseModel):
    refresh_token: str
