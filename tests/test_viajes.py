import uuid

from app.database import get_mongo_db


def _sufijo() -> str:
    return uuid.uuid4().hex[:10]


def _viajes_del_usuario(usuario_id: int) -> list[dict]:
    db = get_mongo_db()
    assert db is not None, "MongoDB debe estar disponible para las pruebas"
    return list(db["viajes"].find({"usuario_id": usuario_id}))


def _viaje_por_origen(usuario_id: int, origen: str) -> dict | None:
    db = get_mongo_db()
    assert db is not None, "MongoDB debe estar disponible para las pruebas"
    return db["viajes"].find_one({"usuario_id": usuario_id, "origen": origen})


def test_calcular_duracion_persiste_en_mongo(client, auth_headers, usuario_pruebas):
    """El viaje calculado se guarda antes de responder y queda ligado al usuario."""
    origen = f"Poblado-{_sufijo()}"
    payload = {
        "origen": origen,
        "destino": "Niquía",
        "duracion_minutos": 35,
    }
    response = client.post("/viajes/calcular-duracion", json=payload, headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["duracion_minutos"] == 35
    assert data["origen"] == origen
    assert data["destino"] == "Niquía"

    documento = _viaje_por_origen(usuario_pruebas["id"], origen)
    assert documento is not None
    assert documento["tipo"] == "simple"
    assert documento["destino"] == "Niquía"
    assert documento["duracion_minutos"] == 35
    assert documento["usuario_email"] == usuario_pruebas["email"]


def test_calcular_duracion_invalida_no_persiste(client, auth_headers, usuario_pruebas):
    """Un payload inválido no debe generar un viaje en MongoDB."""
    origen = f"Poblado-{_sufijo()}"
    payload = {
        "origen": origen,
        "destino": "Niquía",
        "duracion_minutos": 0,
    }
    response = client.post("/viajes/calcular-duracion", json=payload, headers=auth_headers)

    assert response.status_code == 422
    assert _viaje_por_origen(usuario_pruebas["id"], origen) is None


def test_viaje_multimodal_persiste_en_mongo(client, auth_headers, usuario_pruebas):
    """El itinerario multimodal se guarda con su secuencia de rutas."""
    sufijo = _sufijo()
    secuencia = [f"Metro-{sufijo}", f"Metrocable-{sufijo}", f"Bus-{sufijo}"]
    response = client.post(
        "/viajes/multimodal",
        json={"secuencia_rutas": secuencia},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["secuencia_rutas"] == secuencia
    assert "Ruta sugerida" in data["itinerario"]

    documento = _viaje_por_origen(usuario_pruebas["id"], secuencia[0])
    assert documento is not None
    assert documento["tipo"] == "multimodal"
    assert documento["destino"] == secuencia[-1]
    assert documento["secuencia_rutas"] == secuencia
    assert documento["itinerario"] == data["itinerario"]


def test_viaje_multimodal_vacio_es_rechazado(client, auth_headers):
    """La secuencia debe tener al menos una ruta."""
    response = client.post(
        "/viajes/multimodal",
        json={"secuencia_rutas": []},
        headers=auth_headers,
    )
    assert response.status_code == 422


def test_historial_consulta_solo_los_viajes_del_usuario(client, auth_headers, usuario_pruebas):
    """El historial sale de MongoDB y filtra estrictamente por usuario_id."""
    sufijo = _sufijo()
    origen = f"Origen-{sufijo}"
    destino = f"Destino-{sufijo}"

    assert (
        client.post(
            "/viajes/calcular-duracion",
            json={"origen": origen, "destino": destino, "duracion_minutos": 22},
            headers=auth_headers,
        ).status_code
        == 200
    )
    assert (
        client.post(
            "/viajes/multimodal",
            json={"secuencia_rutas": [f"Metro-{sufijo}", f"Bus-{sufijo}"]},
            headers=auth_headers,
        ).status_code
        == 200
    )

    total_en_mongo = len(_viajes_del_usuario(usuario_pruebas["id"]))
    response = client.get("/viajes/historial?limit=100&skip=0", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["usuario"] == usuario_pruebas["email"]
    assert data["total"] == total_en_mongo
    assert data["limit"] == 100
    assert data["skip"] == 0
    assert data["total"] >= 2

    origenes = {item["origen"] for item in data["historial"]}
    assert origen in origenes
    assert f"Metro-{sufijo}" in origenes

    simple = next(item for item in data["historial"] if item["origen"] == origen)
    assert simple["tipo"] == "simple"
    assert simple["duracion_minutos"] == 22

    multimodal = next(item for item in data["historial"] if item["origen"] == f"Metro-{sufijo}")
    assert multimodal["tipo"] == "multimodal"
    assert multimodal["secuencia_rutas"] == [f"Metro-{sufijo}", f"Bus-{sufijo}"]


def test_historial_respeta_paginacion(client, auth_headers, usuario_pruebas):
    """El total no se recorta, pero la página sí respeta limit."""
    sufijo = _sufijo()
    creado = client.post(
        "/viajes/calcular-duracion",
        json={
            "origen": f"Paginacion-{sufijo}",
            "destino": f"Destino-{sufijo}",
            "duracion_minutos": 12,
        },
        headers=auth_headers,
    )
    assert creado.status_code == 200

    total_en_mongo = len(_viajes_del_usuario(usuario_pruebas["id"]))
    assert total_en_mongo >= 1

    response = client.get("/viajes/historial?limit=1&skip=0", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data["historial"]) == 1
    assert data["total"] == total_en_mongo


def test_viajes_requieren_token(client):
    """Calcular o planificar un viaje ya no es anónimo: se asocia a un usuario."""
    simple = client.post(
        "/viajes/calcular-duracion",
        json={"origen": "A", "destino": "B", "duracion_minutos": 10},
    )
    multimodal = client.post(
        "/viajes/multimodal",
        json={"secuencia_rutas": ["Metro A"]},
    )
    historial = client.get("/viajes/historial")

    assert simple.status_code in (401, 403)
    assert multimodal.status_code in (401, 403)
    assert historial.status_code in (401, 403)
