import pytest
from app.core.seguridad import crear_token_acceso


@pytest.fixture
def auth_headers():
    """Genera headers con un token JWT válido para las pruebas."""
    token = crear_token_acceso(data={"sub": "test@example.com", "rol": "Usuario_Regular"})
    return {"Authorization": f"Bearer {token}"}


def test_registrar_reporte_exitoso(client, auth_headers):
    """Verifica el registro de un reporte de servicio (RF-06)."""
    payload = {
        "calificacion": 5,
        "comentario_ciudadano": "Excelente servicio, puntual y limpio.",
    }
    response = client.post("/reportes/", json=payload, headers=auth_headers)
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["guardado"] is True
    assert data["calificacion"] == 5


def test_registrar_reporte_calificacion_invalida(client, auth_headers):
    """Verifica que una calificación fuera de rango sea rechazada."""
    payload = {
        "calificacion": 10,
        "comentario_ciudadano": "Fuera de rango.",
    }
    response = client.post("/reportes/", json=payload, headers=auth_headers)
    assert response.status_code == 422


def test_registrar_reporte_calificacion_baja(client, auth_headers):
    """Verifica el registro de una calificación baja válida."""
    payload = {
        "calificacion": 1,
        "comentario_ciudadano": "Servicio deficiente.",
    }
    response = client.post("/reportes/", json=payload, headers=auth_headers)
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["calificacion"] == 1