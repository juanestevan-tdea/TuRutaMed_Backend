"""Endpoints de salud para orquestadores y balanceadores de carga."""

import asyncio
import time
from typing import Any

from fastapi import APIRouter, HTTPException, Request, status
from sqlalchemy import text

from app.core.config import get_settings
from app.core.rate_limit import limiter
from app.database import engine, get_mongo_db, mongo_client
from app.services.cache_service import get_redis_client

router = APIRouter(tags=["health"])
settings = get_settings()

CHECK_TIMEOUT = 2.0


async def _check_mysql() -> float:
    """Ping a MySQL usando el engine/pool existente. Retorna latencia en ms."""

    def _ping() -> None:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

    start = time.perf_counter()
    await asyncio.wait_for(asyncio.to_thread(_ping), timeout=CHECK_TIMEOUT)
    return (time.perf_counter() - start) * 1000.0


async def _check_mongo() -> float:
    """Ping a MongoDB usando el cliente existente. Retorna latencia en ms."""
    db = get_mongo_db()
    if db is None:
        raise RuntimeError("mongo unavailable")

    def _ping() -> None:
        client = getattr(db, "client", None) or mongo_client
        if client is None:
            raise RuntimeError("mongo client unavailable")
        client.admin.command("ping")

    start = time.perf_counter()
    await asyncio.wait_for(asyncio.to_thread(_ping), timeout=CHECK_TIMEOUT)
    return (time.perf_counter() - start) * 1000.0


async def _check_redis() -> float:
    """Ping a Redis usando el cliente existente. Retorna latencia en ms."""
    start = time.perf_counter()
    client = await asyncio.wait_for(get_redis_client(), timeout=CHECK_TIMEOUT)
    await asyncio.wait_for(client.ping(), timeout=CHECK_TIMEOUT)
    return (time.perf_counter() - start) * 1000.0


@router.get("/health/live")
@limiter.limit("60/minute")
async def health_live(request: Request) -> dict[str, Any]:
    """Liveness probe: el proceso responde."""
    return {
        "status": "alive",
        "version": settings.app_version,
        "environment": settings.environment,
    }


@limiter.exempt
@router.get("/health/ready")
async def health_ready() -> dict[str, Any]:
    """Readiness probe: verifica MySQL, Mongo y Redis en paralelo."""
    mysql_task = _check_mysql()
    mongo_task = _check_mongo()
    redis_task = _check_redis()

    results = await asyncio.gather(mysql_task, mongo_task, redis_task, return_exceptions=True)

    names = ("mysql", "mongo", "redis")
    checks: dict[str, dict[str, Any]] = {}
    all_up = True
    for name, result in zip(names, results, strict=False):
        if isinstance(result, BaseException):
            checks[name] = {"status": "down"}
            all_up = False
        else:
            checks[name] = {"status": "up", "latency_ms": round(result)}

    payload = {
        "status": "ready" if all_up else "degraded",
        "checks": checks,
        "version": settings.app_version,
        "environment": settings.environment,
    }

    if not all_up:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=payload,
        )

    return payload
