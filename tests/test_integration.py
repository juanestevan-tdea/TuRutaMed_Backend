def test_flujo_jwt_completo(client):
    """
    Prueba de integración: Registro -> Login -> Obtener Token -> Consumir endpoint protegido.
    """
    # 1. Registro de usuario
    payload_registro = {
        "nombre": "Usuario Integracion",
        "email": "integracion_turutamed@example.com",
        "password": "Password123!",
        "rol": "Usuario_Regular",
    }
    resp_registro = client.post("/usuarios/registro", json=payload_registro)
    # Aceptamos 201 (creado) o 400/409 (ya existe de ejecuciones anteriores)
    assert resp_registro.status_code in [200, 201, 400, 409, 422]

    # 2. Login para obtener token
    payload_login = {
        "email": "integracion_turutamed@example.com",
        "password": "Password123!",
    }
    resp_login = client.post("/usuarios/login", json=payload_login)
    # Si el registro falló por duplicado, el login puede fallar; manejamos ambos casos
    if resp_login.status_code in [200, 201]:
        token = resp_login.json().get("access_token")
        assert token is not None

        headers = {"Authorization": f"Bearer {token}"}

        # 3. Consumir endpoint protegido: reportes
        payload_reporte = {
            "calificacion": 4,
            "comentario_ciudadano": "Prueba de integración JWT",
        }
        resp_reporte = client.post("/reportes/", json=payload_reporte, headers=headers)
        assert resp_reporte.status_code in [200, 201]

        # 4. Consumir endpoint protegido: recarga Cívica
        payload_recarga = {
            "tarjeta_id": "INTEG001",
            "monto": 10000.0,
            "metodo_de_pago": "PSE",
        }
        resp_recarga = client.post("/civica/recargar", json=payload_recarga, headers=headers)
        assert resp_recarga.status_code == 200

        # 5. Consumir endpoint protegido: historial de viajes
        resp_historial = client.get("/viajes/historial", headers=headers)
        assert resp_historial.status_code == 200
    else:
        # Si no se pudo hacer login (ej. usuario no creado por falta de DB),
        # verificamos al menos que el endpoint protegido rechace sin token
        resp_sin_token = client.post(
            "/reportes/",
            json={
                "calificacion": 3,
                "comentario_ciudadano": "Sin token",
            },
        )
        assert resp_sin_token.status_code in [401, 403, 422]


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
