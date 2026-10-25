import uuid

from app.database import SessionLocal, get_mongo_db
from app.models.civica import TarjetaCivicaDB


def _sufijo() -> str:
    return uuid.uuid4().hex[:10]


def test_flujo_jwt_completo_persiste_en_bases_reales(client):
    """Registro -> login -> reporte, recarga y viajes con persistencia verificable."""
    sufijo = _sufijo()
    email = f"integracion_{sufijo}@example.com"
    contrasena = "Password123!"  # noqa: S105

    registro = client.post(
        "/usuarios/registro",
        json={
            "nombre": "Usuario Integracion",
            "email": email,
            "password": contrasena,
            "rol": "Usuario",
        },
    )
    assert registro.status_code == 201, registro.text
    usuario_id = registro.json()["id"]

    login = client.post("/usuarios/login", json={"email": email, "password": contrasena})
    assert login.status_code == 200, login.text
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Reporte en MongoDB
    comentario = f"Prueba de integración {sufijo}"
    reporte = client.post(
        "/reportes/",
        json={"calificacion": 4, "comentario_ciudadano": comentario},
        headers=headers,
    )
    assert reporte.status_code == 201, reporte.text
    mongo = get_mongo_db()
    assert mongo is not None
    assert mongo["reportes"].find_one(
        {"usuario_id": usuario_id, "comentario_ciudadano": comentario}
    )

    # Recarga en MySQL
    tarjeta_id = f"INT{sufijo}"
    recarga = client.post(
        "/civica/recargar",
        json={"tarjeta_id": tarjeta_id, "monto": 10000.0, "metodo_de_pago": "PSE"},
        headers=headers,
    )
    assert recarga.status_code == 200, recarga.text
    with SessionLocal() as db:
        tarjeta = db.query(TarjetaCivicaDB).filter(TarjetaCivicaDB.numero == tarjeta_id).one()
        assert float(tarjeta.saldo) == 10000.0

    # Viajes en MongoDB
    origen = f"Origen-{sufijo}"
    viaje = client.post(
        "/viajes/calcular-duracion",
        json={"origen": origen, "destino": f"Destino-{sufijo}", "duracion_minutos": 18},
        headers=headers,
    )
    assert viaje.status_code == 200, viaje.text

    ruta_metro = f"Metro-{sufijo}"
    multimodal = client.post(
        "/viajes/multimodal",
        json={"secuencia_rutas": [ruta_metro, f"Bus-{sufijo}"]},
        headers=headers,
    )
    assert multimodal.status_code == 200, multimodal.text

    total_mongo = mongo["viajes"].count_documents({"usuario_id": usuario_id})
    historial = client.get("/viajes/historial?limit=100&skip=0", headers=headers)
    assert historial.status_code == 200, historial.text
    data = historial.json()
    assert data["usuario"] == email
    assert data["total"] == total_mongo
    assert {item["origen"] for item in data["historial"]} >= {origen, ruta_metro}


def test_endpoint_protegido_sin_token(client):
    """Verifica que un endpoint protegido rechace solicitudes sin token JWT."""
    payload = {
        "calificacion": 5,
        "comentario_ciudadano": "Sin autenticación",
    }
    response = client.post("/reportes/", json=payload)
    assert response.status_code in [401, 403]


def test_endpoint_protegido_token_invalido(client):
    """Verifica que un token inválido sea rechazado."""
    headers = {"Authorization": "Bearer token_invalido_12345"}
    payload = {
        "calificacion": 5,
        "comentario_ciudadano": "Token inválido",
    }
    response = client.post("/reportes/", json=payload, headers=headers)
    assert response.status_code in [401, 403]
