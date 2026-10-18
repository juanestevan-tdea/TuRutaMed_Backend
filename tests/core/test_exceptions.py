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
    body = response.json()
    assert body["type"] == "https://turutamed.com/errors/NOT_FOUND"
    assert body["title"] == "NOT_FOUND"
    assert body["status"] == 404
    assert body["detail"] == "recurso no encontrado"
    assert body["instance"] == "/_test/not-found"


def test_conflict_handler(client: TestClient):
    response = client.get("/_test/conflict")
    assert response.status_code == 409
    body = response.json()
    assert body["type"] == "https://turutamed.com/errors/CONFLICT"
    assert body["title"] == "CONFLICT"
    assert body["status"] == 409
    assert body["detail"] == "estado en conflicto"
    assert body["instance"] == "/_test/conflict"
