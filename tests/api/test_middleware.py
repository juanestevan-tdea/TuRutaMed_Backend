from fastapi.testclient import TestClient


def test_response_includes_request_id(client: TestClient):
    response = client.get("/health/live")
    assert "X-Request-ID" in response.headers


def test_request_id_echoed(client: TestClient):
    custom_id = "test-request-id-123"
    response = client.get("/health/live", headers={"X-Request-ID": custom_id})
    assert response.headers["X-Request-ID"] == custom_id
