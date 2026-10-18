from fastapi.testclient import TestClient

from app.core.rate_limit import limiter


def test_rate_limit_health_live(client: TestClient):
    limiter.reset()
    statuses = []
    for _ in range(61):
        response = client.get("/health/live")
        statuses.append(response.status_code)
    assert 429 in statuses


def test_rate_limit_ia(client: TestClient):
    limiter.reset()
    statuses = []
    for _ in range(11):
        response = client.post("/ia/optimizar-ruta", json={"origen": "A", "destino": "B"})
        statuses.append(response.status_code)
    assert 429 in statuses