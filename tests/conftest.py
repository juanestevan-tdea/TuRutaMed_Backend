import uuid

import pytest
from fastapi.testclient import TestClient

from app.core.rate_limit import limiter
from app.main import app


@pytest.fixture(autouse=True)
def _reset_rate_limiter():
    limiter.reset()
    yield


@pytest.fixture(scope="session")
def client():
    """
    Crea una instancia de TestClient basada en la aplicación principal de FastAPI.
    Se comparte a lo largo de la sesión de pruebas para optimizar el rendimiento.
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def usuario_pruebas(client):
    """Registra y autentica un usuario real único para las pruebas de persistencia."""
    sufijo = uuid.uuid4().hex[:12]
    email = f"pytest_{sufijo}@example.com"
    contrasena = "Password123!"  # noqa: S105

    registro = client.post(
        "/usuarios/registro",
        json={
            "nombre": "Usuario Persistencia",
            "email": email,
            "password": contrasena,
            "rol": "Usuario",
        },
    )
    assert registro.status_code == 201, registro.text

    login = client.post(
        "/usuarios/login",
        json={"email": email, "password": contrasena},
    )
    assert login.status_code == 200, login.text

    token = login.json()["access_token"]
    return {
        "id": registro.json()["id"],
        "email": email,
        "password": contrasena,
        "token": token,
        "headers": {"Authorization": f"Bearer {token}"},
    }


@pytest.fixture
def auth_headers(usuario_pruebas):
    """Headers con un JWT de un usuario que existe realmente en MySQL."""
    return usuario_pruebas["headers"]
