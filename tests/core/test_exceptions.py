from fastapi.testclient import TestClient

from app.core.exceptions import ConflictError, NotFoundError
from app.main import app


@app.get("/_test/not-found")
def _raise_not_found():
    raise NotFoundError(message="recurso no encontrado")


@app.get("/_test/conflict")
def _raise_conflict():
    raise ConflictError(message="estado en conflicto")


def test_not_found_handler(client: TestClient):
    response = client.get("/_test/not-found")
    assert response.status_code == 404
    assert response.json() == {"error": {"code": "NOT_FOUND", "message": "recurso no encontrado"}}


def test_conflict_handler(client: TestClient):
    response = client.get("/_test/conflict")
    assert response.status_code == 409
    assert response.json() == {"error": {"code": "CONFLICT", "message": "estado en conflicto"}}
