"""Configuración de rate limiting con slowapi + Redis."""

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import get_settings

settings = get_settings()

# Usar Redis si está disponible; si no, memoria (útil en tests sin Redis).
storage_uri: str | None = settings.redis_url
try:
    import redis as _redis

    _client = _redis.from_url(settings.redis_url)
    _client.ping()
except Exception:  # noqa: BLE001
    storage_uri = None

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=storage_uri,
    default_limits=["60/minute"],
)
