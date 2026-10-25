# app/services/cache_service.py
"""
==============================================================================
TuRutaMed - Servicio de Caché con Redis
==============================================================================
Estrategia asincrónica para cachear consultas frecuentes de rutas durante
5 minutos, reduciendo la carga sobre MongoDB.
==============================================================================
"""

import hashlib
import json
from functools import wraps
from typing import Any

try:
    import redis.asyncio as redis

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

from app.core.config import get_settings
from app.core.exceptions import DomainException

settings = get_settings()
REDIS_URL = settings.redis_url
CACHE_TTL = 300  # 5 minutos en segundos

_redis_client = None


async def get_redis_client():
    """Obtiene el cliente Redis asíncrono (singleton). Lanza 503 si no está disponible."""
    global _redis_client
    if not REDIS_AVAILABLE:
        raise DomainException(
            message="El servicio de caché no se encuentra disponible temporalmente.",
            code="CACHE_UNAVAILABLE",
            status_code=503,
        )
    if _redis_client is None:
        try:
            # El caché es opcional: si Redis no está disponible, no debe bloquear
            # la petición durante el timeout TCP por defecto.
            _redis_client = redis.from_url(
                REDIS_URL,
                decode_responses=True,
                socket_connect_timeout=1,
                socket_timeout=1,
            )
            await _redis_client.ping()
        except Exception as e:
            _redis_client = None
            raise DomainException(
                message="El servicio de caché no se encuentra disponible temporalmente.",
                code="CACHE_UNAVAILABLE",
                status_code=503,
            ) from e
    return _redis_client


async def cache_get(key: str) -> Any | None:
    """Obtiene un valor del caché. Retorna None si no existe o Redis no está disponible."""
    try:
        client = await get_redis_client()
    except DomainException:  # noqa: BLE001
        return None
    try:
        value = await client.get(key)
        if value is not None:
            return json.loads(value)
    except Exception:  # noqa: BLE001
        return None
    return None


async def cache_set(key: str, value: Any, ttl: int = CACHE_TTL) -> bool:
    """Guarda un valor en el caché con TTL. Retorna True si se guardó exitosamente."""
    try:
        client = await get_redis_client()
    except DomainException:  # noqa: BLE001
        return False
    try:
        await client.set(key, json.dumps(value, default=str), ex=ttl)
        return True
    except Exception:  # noqa: BLE001
        return False


async def cache_delete(key: str) -> bool:
    """Elimina una clave del caché."""
    try:
        client = await get_redis_client()
    except DomainException:  # noqa: BLE001
        return False
    try:
        await client.delete(key)
        return True
    except Exception:  # noqa: BLE001
        return False


def make_cache_key(prefix: str, *args, **kwargs) -> str:
    """Genera una clave de caché determinista a partir de los argumentos."""
    raw = f"{prefix}:{args}:{sorted(kwargs.items())}"
    return f"turutamed:{hashlib.md5(raw.encode(), usedforsecurity=False).hexdigest()}"  # noqa: S324


def cached(prefix: str, ttl: int = CACHE_TTL):
    """Decorador para cachear resultados de funciones asíncronas."""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = make_cache_key(prefix, *args, **kwargs)
            cached_value = await cache_get(cache_key)
            if cached_value is not None:
                return cached_value
            result = await func(*args, **kwargs)
            await cache_set(cache_key, result, ttl)
            return result

        return wrapper

    return decorator
