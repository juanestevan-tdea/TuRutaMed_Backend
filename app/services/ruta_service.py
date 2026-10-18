"""Capa de servicio para el dominio de Rutas (MongoDB)."""

from app.repositories.ruta_repository import RutaRepository


class RutaService:
    def __init__(self, repository: RutaRepository) -> None:
        self.repository = repository

    def registrar_ruta(self, ruta_data: dict) -> str:
        return self.repository.crear_ruta(ruta_data)

    def listar_rutas(self) -> list[dict]:
        return self.repository.obtener_todas()

    def buscar_cercanas(self, longitud: float, latitud: float) -> list[dict]:
        return self.repository.obtener_rutas_cercanas(longitud, latitud)
