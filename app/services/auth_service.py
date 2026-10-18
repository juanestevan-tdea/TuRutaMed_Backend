"""Servicio de autenticación: tokens y revocación (blacklist)."""

import time
from typing import Any

from app.core.exceptions import UnauthorizedError
from app.core.seguridad import (
    crear_access_token,
    crear_refresh_token,
    decodificar_token,
)
from app.services.cache_service import get_redis_client


async def _is_blacklisted(token: str) -> bool:
    try:
        client = await get_redis_client()
    except Exception:  # noqa: BLE001
        return False
    try:
        return bool(await client.exists(f"blacklist:{token}"))
    except Exception:  # noqa: BLE001
        return False


def login(usuario: Any) -> dict[str, str]:
    data = {"sub": usuario.email, "rol": usuario.rol}
    access = crear_access_token(data)
    refresh = crear_refresh_token(data)
    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer",
    }


async def refresh(refresh_token: str) -> dict[str, str]:
    try:
        payload = decodificar_token(refresh_token, expected_type="refresh")
    except Exception:  # noqa: BLE001
        raise UnauthorizedError(message="Refresh token inválido o expirado") from None

    if await _is_blacklisted(refresh_token):
        raise UnauthorizedError(message="Refresh token revocado")

    data = {"sub": payload.get("sub"), "rol": payload.get("rol")}
    access = crear_access_token(data)
    new_refresh = crear_refresh_token(data)
    return {
        "access_token": access,
        "refresh_token": new_refresh,
        "token_type": "bearer",
    }


async def logout(refresh_token: str) -> None:
    try:
        payload = decodificar_token(refresh_token, expected_type="refresh")
    except Exception:  # noqa: BLE001
        return
    exp = payload.get("exp")
    if not exp:
        return
    ttl = int(exp - time.time())
    if ttl <= 0:
        return
    try:
        client = await get_redis_client()
        await client.setex(f"blacklist:{refresh_token}", ttl, "1")
    except Exception:  # noqa: BLE001
        return
