from unittest.mock import MagicMock

from app.services.ruta_service import RutaService


def test_listar_rutas_delega():
    repo = MagicMock()
    repo.obtener_todas.return_value = [{"_id": "1"}]
    service = RutaService(repo)

    result = service.listar_rutas()

    repo.obtener_todas.assert_called_once()
    assert result == [{"_id": "1"}]


def test_buscar_cercanas_delega():
    repo = MagicMock()
    repo.obtener_rutas_cercanas.return_value = []
    service = RutaService(repo)

    result = service.buscar_cercanas(-75.5, 6.2)

    repo.obtener_rutas_cercanas.assert_called_once_with(-75.5, 6.2)
    assert result == []


def test_registrar_ruta_delega():
    repo = MagicMock()
    repo.crear_ruta.return_value = "abc123"
    service = RutaService(repo)

    result = service.registrar_ruta({"nombre": "Ruta 1"})

    repo.crear_ruta.assert_called_once_with({"nombre": "Ruta 1"})
    assert result == "abc123"
