from fastapi.testclient import TestClient


def test_metrics_endpoint(client: TestClient):
    # Generar al menos una petición para que exista la métrica
    client.get("/health/live")
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text
