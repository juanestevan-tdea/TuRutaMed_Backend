import pytest


def test_registrar_reporte_exitoso(client):
    """Verifica el registro de un reporte de servicio (RF-06)."""
    payload = {
        "calificacion": 5,
        "comentario_ciudadano": "Excelente servicio, puntual y limpio.",
    }
    response = client.post("/reportes/", json=payload)
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["guardado"] is True
    assert data["calificacion"] == 5


def test_registrar_reporte_calificacion_invalida(client):
    """Verifica que una calificación fuera de rango sea rechazada."""
    payload = {
        "calificacion": 10,
        "comentario_ciudadano": "Fuera de rango.",
    }
    response = client.post("/reportes/", json=payload)
    assert response.status_code == 422


def test_registrar_reporte_calificacion_baja(client):
    """Verifica el registro de una calificación baja válida."""
    payload = {
        "calificacion": 1,
        "comentario_ciudadano": "Servicio deficiente.",
    }
    response = client.post("/reportes/", json=payload)
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["calificacion"] == 1