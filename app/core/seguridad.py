import os
import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

# Variables de entorno para JWT
SECRET_KEY = os.getenv("SECRET_KEY", "secreto_temporal")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# Configuración de bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def obtener_hash_contrasena(contrasena: str):
    return pwd_context.hash(contrasena)

def verificar_contrasena(contrasena_plana: str, contrasena_hasheada: str):
    return pwd_context.verify(contrasena_plana, contrasena_hasheada)

def crear_token_acceso(data: dict):
    """Fábrica de Tokens: Crea el pasaporte digital (JWT)"""
    to_encode = data.copy()
    # Le ponemos una fecha de vencimiento (ej. 1 hora)
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Sellamos el pasaporte con nuestra FIRMA SECRETA
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt as jose_jwt, JWTError

# Usamos HTTPBearer para que Swagger nos permita pegar el token directamente
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
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
        raise credentials_exception


def verificar_rol_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
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
                detail="Acceso denegado: Se requieren privilegios suficientes"
            )
        return payload
    except JWTError:
        raise credentials_exception