"""Repositorio de acceso a datos para el dominio de Rutas (MongoDB)."""

from typing import Any

from app.core.exceptions import DomainException


class RutaRepository:
    """Encapsula las consultas a MongoDB relacionadas con rutas."""

    def __init__(self, db: Any) -> None:
        self.db = db

    def _collection(self):
        if self.db is None:
            raise DomainException(
                message="Base de datos no disponible", code="DB_UNAVAILABLE", status_code=503
            )
        return self.db["rutas"]

    def crear_ruta(self, ruta_data: dict) -> str:
        resultado = self._collection().insert_one(ruta_data)
        return str(resultado.inserted_id)

    def obtener_todas(self) -> list[dict]:
        rutas: list[dict] = []
        for ruta in self._collection().find():
            ruta["_id"] = str(ruta["_id"])
            rutas.append(ruta)
        return rutas

    def obtener_rutas_cercanas(
        self, longitud: float, latitud: float, max_distancia: int = 3000
    ) -> list[dict]:
        query = {
            "paraderos.coordenadas": {
                "$near": {
                    "$geometry": {"type": "Point", "coordinates": [longitud, latitud]},
                    "$maxDistance": max_distancia,
                }
            }
        }
        rutas: list[dict] = []
        for ruta in self._collection().find(query):
            ruta["_id"] = str(ruta["_id"])
            rutas.append(ruta)
        return rutas
