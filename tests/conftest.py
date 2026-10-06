import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="session")
def client():
    """
    Crea una instancia de TestClient basada en la aplicación principal de FastAPI.
    Se comparte a lo largo de la sesión de pruebas para optimizar el rendimiento.
    """
    with TestClient(app) as c:
        yield c
