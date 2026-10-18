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


def crear_token_acceso(data: dict):
    """Fábrica de Tokens: Crea el pasaporte digital (JWT)"""
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jose_jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


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
        payload = jose_jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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
        payload = jose_jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        rol: str = payload.get("rol")

        if rol not in ("admin", "Administrador_Sistema", "operador"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado: Se requieren privilegios suficientes",
            )
        return payload
    except JWTError:
        raise credentials_exception from None
