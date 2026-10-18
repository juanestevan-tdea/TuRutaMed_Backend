import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from app.core.exceptions import UnauthorizedError
from app.core.seguridad import crear_refresh_token, decodificar_token
from app.services import auth_service


def test_login_returns_both_tokens():
    class U:
        email = "u@test.com"
        rol = "Usuario_Regular"

    result = auth_service.login(U())
    assert "access_token" in result
    assert "refresh_token" in result
    assert result["token_type"] == "bearer"  # noqa: S105
    assert decodificar_token(result["access_token"], expected_type="access")
    assert decodificar_token(result["refresh_token"], expected_type="refresh")


def test_refresh_returns_new_tokens():
    refresh_token = crear_refresh_token({"sub": "u@test.com", "rol": "Usuario_Regular"})

    mock_client = AsyncMock()
    mock_client.exists.return_value = 0
    with patch("app.services.auth_service.get_redis_client", return_value=mock_client):
        result = asyncio.run(auth_service.refresh(refresh_token))

    assert "access_token" in result
    assert "refresh_token" in result
    assert decodificar_token(result["access_token"], expected_type="access")


def test_refresh_blacklisted_raises():
    refresh_token = crear_refresh_token({"sub": "u@test.com", "rol": "Usuario_Regular"})

    mock_client = AsyncMock()
    mock_client.exists.return_value = 1
    with patch("app.services.auth_service.get_redis_client", return_value=mock_client):
        with pytest.raises(UnauthorizedError):
            asyncio.run(auth_service.refresh(refresh_token))


def test_logout_blacklists_token():
    refresh_token = crear_refresh_token({"sub": "u@test.com", "rol": "Usuario_Regular"})

    mock_client = AsyncMock()
    with patch("app.services.auth_service.get_redis_client", return_value=mock_client):
        asyncio.run(auth_service.logout(refresh_token))

    mock_client.setex.assert_called_once()


def test_refresh_after_logout_fails():
    refresh_token = crear_refresh_token({"sub": "u@test.com", "rol": "Usuario_Regular"})

    mock_client = AsyncMock()
    mock_client.exists.return_value = 0
    with patch("app.services.auth_service.get_redis_client", return_value=mock_client):
        asyncio.run(auth_service.logout(refresh_token))

    mock_client.exists.return_value = 1
    with patch("app.services.auth_service.get_redis_client", return_value=mock_client):
        with pytest.raises(UnauthorizedError):
            asyncio.run(auth_service.refresh(refresh_token))
