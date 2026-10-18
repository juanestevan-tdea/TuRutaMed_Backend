from datetime import UTC, datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from jose import jwt as jose_jwt
from passlib.context import CryptContext

from app.core.config import get_settings

settings = get_settings()

SECRET_KEY = settings.jwt_secret
ALGORITHM = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.jwt_expire_minutes

# Configuración de bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def obtener_hash_contrasena(contrasena: str):
    return pwd_context.hash(contrasena)


def verificar_contrasena(contrasena_plana: str, contrasena_hasheada: str):
    return pwd_context.verify(contrasena_plana, contrasena_hasheada)


def crear_access_token(data: dict) -> str:
    """Crea un access token JWT (corta duración)."""
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jose_jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def crear_refresh_token(data: dict) -> str:
    """Crea un refresh token JWT (larga duración)."""
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(days=settings.jwt_refresh_expire_days)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jose_jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def crear_token_acceso(data: dict) -> str:
    """Alias de compatibilidad."""
    return crear_access_token(data)


def decodificar_token(token: str, expected_type: str | None = None) -> dict:
    """Decodifica y valida un JWT, verificando el claim 'type' si se indica."""
    payload = jose_jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    if expected_type is not None and payload.get("type") != expected_type:
        raise JWTError("Tipo de token inválido")
    return payload


security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):  # noqa: B008
    """Dependencia que valida el JWT y retorna el payload del usuario autenticado."""
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales de seguridad",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decodificar_token(token, expected_type="access")
        if payload.get("sub") is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception from None


def verificar_rol_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):  # noqa: B008
    """Verifica que el token sea válido y pertenezca a un administrador"""
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales de seguridad",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decodificar_token(token, expected_type="access")
        rol: str = str(payload.get("rol"))

        if rol not in ("admin", "Administrador_Sistema", "operador"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado: Se requieren privilegios suficientes",
            )
        return payload
    except JWTError:
        raise credentials_exception from None
