# app/services/cache_service.py
"""
==============================================================================
TuRutaMed - Servicio de Caché con Redis
==============================================================================
Estrategia asincrónica para cachear consultas frecuentes de rutas durante
5 minutos, reduciendo la carga sobre MongoDB.
==============================================================================
"""

import os
import json
import hashlib
from typing import Any, Optional
from functools import wraps

try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

from fastapi import HTTPException, status

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
CACHE_TTL = 300  # 5 minutos en segundos

_redis_client = None


async def get_redis_client():
    """Obtiene el cliente Redis asíncrono (singleton). Lanza 503 si no está disponible."""
    global _redis_client
    if not REDIS_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="El servicio de caché no se encuentra disponible temporalmente.",
        )
    if _redis_client is None:
        try:
            _redis_client = redis.from_url(REDIS_URL, decode_responses=True)
            await _redis_client.ping()
        except Exception as e:
            _redis_client = None
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="El servicio de caché no se encuentra disponible temporalmente.",
            ) from e
    return _redis_client


async def cache_get(key: str) -> Optional[Any]:
    """Obtiene un valor del caché. Retorna None si no existe o Redis no está disponible."""
    try:
        client = await get_redis_client()
    except HTTPException:
        return None
    try:
        value = await client.get(key)
        if value is not None:
            return json.loads(value)
    except Exception:
        pass
    return None


async def cache_set(key: str, value: Any, ttl: int = CACHE_TTL) -> bool:
    """Guarda un valor en el caché con TTL. Retorna True si se guardó exitosamente."""
    try:
        client = await get_redis_client()
    except HTTPException:
        return False
    try:
        await client.set(key, json.dumps(value, default=str), ex=ttl)
        return True
    except Exception:
        return False


async def cache_delete(key: str) -> bool:
    """Elimina una clave del caché."""
    try:
        client = await get_redis_client()
    except HTTPException:
        return False
    try:
        await client.delete(key)
        return True
    except Exception:
        return False


def make_cache_key(prefix: str, *args, **kwargs) -> str:
    """Genera una clave de caché determinista a partir de los argumentos."""
    raw = f"{prefix}:{args}:{sorted(kwargs.items())}"
    return f"turutamed:{hashlib.md5(raw.encode()).hexdigest()}"


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