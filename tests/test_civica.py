import uuid

from app.database import SessionLocal
from app.models.civica import TarjetaCivicaDB


def _numero_tarjeta() -> str:
    """Genera un número único para aislar cada prueba en MySQL."""
    return f"T{uuid.uuid4().hex[:12]}"


def _saldo_en_bd(numero: str) -> float | None:
    """Lee el saldo desde una sesión nueva, fuera de la identidad de la API."""
    with SessionLocal() as db:
        tarjeta = db.query(TarjetaCivicaDB).filter(TarjetaCivicaDB.numero == numero).first()
        return None if tarjeta is None else float(tarjeta.saldo)


def test_consultar_saldo_tarjeta_nueva_persiste_en_mysql(client):
    """La primera consulta crea la tarjeta con saldo 0 en MySQL."""
    numero = _numero_tarjeta()
    response = client.get(f"/civica/saldo/{numero}")

    assert response.status_code == 200
    data = response.json()
    assert data["tarjeta_id"] == numero
    assert data["saldo"] == 0.0
    assert _saldo_en_bd(numero) == 0.0


def test_recarga_exitosa_persiste_saldo_en_mysql(client, auth_headers):
    """Una recarga actualiza el saldo en la base de datos, no en memoria."""
    numero = _numero_tarjeta()
    payload = {
        "tarjeta_id": numero,
        "monto": 20000.0,
        "metodo_de_pago": "PSE",
    }
    response = client.post("/civica/recargar", json=payload, headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["exitoso"] is True
    assert data["saldo_nuevo"] == 20000.0
    assert data["saldo_anterior"] == 0.0
    assert _saldo_en_bd(numero) == 20000.0

    consulta = client.get(f"/civica/saldo/{numero}")
    assert consulta.json()["saldo"] == 20000.0


def test_recarga_acumula_saldo_y_sobrevive_a_otra_consulta(client, auth_headers):
    """Dos recargas se acumulan en la misma fila de MySQL."""
    numero = _numero_tarjeta()

    primera = client.post(
        "/civica/recargar",
        json={"tarjeta_id": numero, "monto": 15000.0, "metodo_de_pago": "Nequi"},
        headers=auth_headers,
    )
    assert primera.status_code == 200
    assert primera.json()["saldo_nuevo"] == 15000.0

    segunda = client.post(
        "/civica/recargar",
        json={"tarjeta_id": numero, "monto": 5000.0, "metodo_de_pago": "PSE"},
        headers=auth_headers,
    )
    assert segunda.status_code == 200
    assert segunda.json()["saldo_anterior"] == 15000.0
    assert segunda.json()["saldo_nuevo"] == 20000.0

    assert _saldo_en_bd(numero) == 20000.0


def test_recarga_monto_invalido_no_crea_tarjeta(client, auth_headers):
    """El schema rechaza montos <= 0 antes de tocar la base de datos."""
    numero = _numero_tarjeta()
    payload = {
        "tarjeta_id": numero,
        "monto": 0,
        "metodo_de_pago": "PSE",
    }
    response = client.post("/civica/recargar", json=payload, headers=auth_headers)

    assert response.status_code == 422
    assert _saldo_en_bd(numero) is None


def test_recarga_metodo_pago_vacio_no_crea_tarjeta(client, auth_headers):
    """Un método de pago vacío se rechaza antes de escribir en MySQL."""
    numero = _numero_tarjeta()
    response = client.post(
        "/civica/recargar",
        json={"tarjeta_id": numero, "monto": 1000, "metodo_de_pago": "   "},
        headers=auth_headers,
    )

    assert response.status_code == 422
    assert _saldo_en_bd(numero) is None


def test_recarga_requiere_token(client):
    """La recarga no permite escribir saldo sin un JWT válido."""
    response = client.post(
        "/civica/recargar",
        json={"tarjeta_id": _numero_tarjeta(), "monto": 1000, "metodo_de_pago": "PSE"},
    )
    assert response.status_code in (401, 403)
