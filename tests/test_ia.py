from app.core.exceptions import DomainException


def test_asistente_propaga_error_real_de_gemini(client, monkeypatch):
    """El endpoint no debe convertir fallos de Gemini en respuestas falsas."""

    def fallo_gemini(*args, **kwargs):
        raise DomainException(
            message=(
                "No se pudo obtener respuesta de Gemini. "
                "Modelos intentados: gemini-3.5-flash-lite. "
                "Detalle: 404 NOT_FOUND modelo retirado."
            ),
            code="AI_SERVICE_UNAVAILABLE",
            status_code=503,
        )

    monkeypatch.setattr("app.routers.ia_router.consultar_asistente_rutas", fallo_gemini)

    response = client.post(
        "/ia/asistente-ruta",
        json={"pregunta": "¿Cómo llego a Laureles?"},
    )

    assert response.status_code == 503
    data = response.json()
    assert data["title"] == "AI_SERVICE_UNAVAILABLE"
    assert "404 NOT_FOUND modelo retirado" in data["detail"]
    assert "mantenimiento" not in data["detail"]
