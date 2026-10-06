def test_health_check_o_raiz(client):
    """
    Verifica que la API responda correctamente en su punto de entrada principal.
    """
    response = client.get("/")
    # El endpoint "/" retorna 200 con mensaje de bienvenida
    assert response.status_code == 200
    assert "mensaje" in response.json()

def test_login_credenciales_invalidas(client):
    """
    Prueba el comportamiento del endpoint de login ante credenciales erróneas.
    """
    # El schema UsuarioLogin espera email y contrasena
    response = client.post("/usuarios/login", json={
        "email": "usuario_falso@turutamed.com",
        "contrasena": "PasswordInvalido123*"
    })
    # Debe retornar 401 Unauthorized ante credenciales inexistentes/inválidas
    assert response.status_code == 401

def test_login_esquema_invalido(client):
    """
    Prueba el comportamiento de validación Pydantic ante campos incompletos o erróneos.
    """
    # Enviamos payload con campo erróneo ('password' en vez de 'contrasena')
    response = client.post("/usuarios/login", json={
        "email": "usuario_falso@turutamed.com",
        "password": "PasswordInvalido123*"
    })
    # Retorna 422 Unprocessable Entity manejado por el interceptor global
    assert response.status_code in [401, 422]

def test_asistente_ia_validacion_esquema(client):
    """
    Verifica que el endpoint /ia/asistente-ruta valide el esquema del body (pregunta).
    """
    response = client.post("/ia/asistente-ruta", json={})
    # Al no enviar el campo 'pregunta' requerido, debe retornar 422
    assert response.status_code == 422
