from unittest.mock import patch

from fastapi.testclient import TestClient

from app.api.v1 import health as health_module


def test_health_live(client: TestClient):
    response = client.get("/health/live")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "alive"
    assert "version" in body
    assert "environment" in body


def test_health_ready_ok(client: TestClient):
    with (
        patch.object(health_module, "_check_mysql", return_value=5.0),
        patch.object(health_module, "_check_mongo", return_value=6.0),
        patch.object(health_module, "_check_redis", return_value=2.0),
    ):
        response = client.get("/health/ready")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ready"
    assert body["checks"]["mysql"]["status"] == "up"
    assert body["checks"]["mongo"]["status"] == "up"
    assert body["checks"]["redis"]["status"] == "up"


def test_health_ready_failure(client: TestClient):
    def _fail():
        raise RuntimeError("boom")

    with (
        patch.object(health_module, "_check_mysql", side_effect=_fail),
        patch.object(health_module, "_check_mongo", return_value=6.0),
        patch.object(health_module, "_check_redis", return_value=2.0),
    ):
        response = client.get("/health/ready")
    assert response.status_code == 503
    body = response.json()
    # FastAPI wraps HTTPException detail under "detail"
    detail = body.get("detail", body)
    assert detail["status"] == "degraded"
    assert detail["checks"]["mysql"]["status"] == "down"
    assert detail["checks"]["mongo"]["status"] == "up"
