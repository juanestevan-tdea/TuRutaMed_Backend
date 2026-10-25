import uuid

from app.database import get_mongo_db


def _comentario_unico(prefijo: str) -> str:
    return f"{prefijo} {uuid.uuid4().hex}"


def _reporte_en_mongo(usuario_id: int, comentario: str) -> dict | None:
    db = get_mongo_db()
    assert db is not None, "MongoDB debe estar disponible para las pruebas"
    return db["reportes"].find_one({"usuario_id": usuario_id, "comentario_ciudadano": comentario})


def test_registrar_reporte_exitoso_persiste_en_mongo(client, auth_headers, usuario_pruebas):
    """El reporte se inserta en MongoDB y queda asociado al usuario del JWT."""
    comentario = _comentario_unico("Excelente servicio")
    payload = {
        "calificacion": 5,
        "comentario_ciudadano": comentario,
    }
    response = client.post("/reportes/", json=payload, headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert data["guardado"] is True
    assert data["id_reporte"]
    assert data["calificacion"] == 5

    documento = _reporte_en_mongo(usuario_pruebas["id"], comentario)
    assert documento is not None
    assert documento["calificacion"] == 5
    assert documento["usuario_email"] == usuario_pruebas["email"]
    assert documento["fecha_reporte"] is not None


def test_registrar_reporte_calificacion_invalida_no_persiste(client, auth_headers, usuario_pruebas):
    """Una calificación fuera de 1..5 se rechaza antes de escribir en MongoDB."""
    comentario = _comentario_unico("Fuera de rango")
    payload = {
        "calificacion": 10,
        "comentario_ciudadano": comentario,
    }
    response = client.post("/reportes/", json=payload, headers=auth_headers)

    assert response.status_code == 422
    assert _reporte_en_mongo(usuario_pruebas["id"], comentario) is None


def test_registrar_reporte_calificacion_baja_persiste(client, auth_headers, usuario_pruebas):
    """Una calificación baja válida también se guarda realmente."""
    comentario = _comentario_unico("Servicio deficiente")
    payload = {
        "calificacion": 1,
        "comentario_ciudadano": comentario,
    }
    response = client.post("/reportes/", json=payload, headers=auth_headers)

    assert response.status_code == 201
    assert response.json()["calificacion"] == 1

    documento = _reporte_en_mongo(usuario_pruebas["id"], comentario)
    assert documento is not None
    assert documento["calificacion"] == 1


def test_registrar_reporte_comentario_vacio_no_persiste(client, auth_headers, usuario_pruebas):
    """Un comentario vacío no debe generar un documento huérfano."""
    payload = {
        "calificacion": 4,
        "comentario_ciudadano": "   ",
    }
    response = client.post("/reportes/", json=payload, headers=auth_headers)

    assert response.status_code == 422
    assert _reporte_en_mongo(usuario_pruebas["id"], "   ") is None
