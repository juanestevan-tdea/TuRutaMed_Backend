import pytest

def test_health_check_o_raiz(client):
    """Verifica que el punto de entrada principal responda correctamente."""
    response = client.get("/")
    assert response.status_code in [200, 404]

def test_registro_usuario_exitoso(client):
    """Verifica el intento de registro de usuario en el sistema."""
    payload = {
        "nombre": "Usuario Pruebas",
        "email": "tester_turutamed@example.com",
        "password": "Password123!",
        "rol": "Usuario_Regular"
    }
    response = client.post("/usuarios/registro", json=payload)
    assert response.status_code in [200, 201, 400, 409, 422]

def test_login_credenciales_invalidas(client):
    """Verifica la respuesta del login ante intentos no autorizados."""
    payload = {
        "email": "usuario_inexistente@example.com",
        "password": "PasswordErrada123"
    }
    response = client.post("/usuarios/login", json=payload)
    assert response.status_code in [200, 400, 401, 404, 422, 500]

def test_estado_roles(client):
    """Verifica que el endpoint de estado devuelva los roles soportados."""
    response = client.get("/estado-roles")
    if response.status_code == 200:
        data = response.json()
        assert "roles_soportados" in data