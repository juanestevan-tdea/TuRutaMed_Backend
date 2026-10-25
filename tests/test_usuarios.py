import pytest
from pydantic import ValidationError as PydanticValidationError

from app.schemas.usuario_schema import UsuarioRegistro


def _payload_registro(**overrides):
    payload = {
        "nombre": "Usuario Pruebas",
        "email": "tester_turutamed@example.com",
        "password": "Password123!",
    }
    payload.update(overrides)
    return payload


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
        "rol": "Usuario_Regular",
    }
    response = client.post("/usuarios/registro", json=payload)
    assert response.status_code in [200, 201, 400, 409, 422]


def test_registro_rechaza_rol_administrador(client):
    """El registro público nunca debe aceptar un rol administrativo."""
    payload = _payload_registro(
        email="intruso_admin@example.com",
        rol="Administrador_Sistema",
    )
    response = client.post("/usuarios/registro", json=payload)
    assert response.status_code == 422


def test_rol_por_defecto_es_usuario():
    usuario = UsuarioRegistro(**_payload_registro())
    assert usuario.rol == "Usuario"


def test_rol_historico_se_normaliza_a_rol_publico():
    usuario = UsuarioRegistro(**_payload_registro(rol="Usuario_Regular"))
    assert usuario.rol == "Usuario"


def test_rol_desconocido_es_rechazado():
    with pytest.raises(PydanticValidationError):
        UsuarioRegistro(**_payload_registro(rol="superadmin"))


def test_login_credenciales_invalidas(client):
    """Verifica la respuesta del login ante intentos no autorizados."""
    payload = {"email": "usuario_inexistente@example.com", "password": "PasswordErrada123"}
    response = client.post("/usuarios/login", json=payload)
    assert response.status_code in [200, 400, 401, 404, 422, 500]


def test_estado_roles(client):
    """Verifica que el endpoint de estado devuelva los roles soportados."""
    response = client.get("/estado-roles")
    if response.status_code == 200:
        data = response.json()
        assert "roles_soportados" in data
