import pytest

from app.core.seguridad import crear_token_acceso


@pytest.fixture
def auth_headers():
    """Genera headers con un token JWT válido para las pruebas."""
    token = crear_token_acceso(data={"sub": "test@example.com", "rol": "Usuario_Regular"})
    return {"Authorization": f"Bearer {token}"}


def test_consultar_saldo_tarjeta_nueva(client):
    """Verifica la consulta de saldo de una tarjeta Cívica nueva (saldo 0)."""
    response = client.get("/civica/saldo/999999")
    assert response.status_code == 200
    data = response.json()
    assert data["tarjeta_id"] == "999999"
    assert data["saldo"] == 0.0


def test_recarga_exitosa(client, auth_headers):
    """Verifica una recarga exitosa y la actualización del saldo."""
    payload = {
        "tarjeta_id": "888888",
        "monto": 20000.0,
        "metodo_de_pago": "PSE",
    }
    response = client.post("/civica/recargar", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["exitoso"] is True
    assert data["saldo_nuevo"] == 20000.0
    assert data["saldo_anterior"] == 0.0


def test_consultar_saldo_despues_recarga(client, auth_headers):
    """Verifica que el saldo persista tras una recarga."""
    client.post("/civica/recargar", json={
        "tarjeta_id": "777777",
        "monto": 15000.0,
        "metodo_de_pago": "Nequi",
    }, headers=auth_headers)
    response = client.get("/civica/saldo/777777")
    assert response.status_code == 200
    assert response.json()["saldo"] == 15000.0


def test_recarga_monto_invalido(client, auth_headers):
    """Verifica que un monto <= 0 sea rechazado."""
    payload = {
        "tarjeta_id": "666666",
        "monto": 0,
        "metodo_de_pago": "PSE",
    }
    response = client.post("/civica/recargar", json=payload, headers=auth_headers)
    assert response.status_code == 422