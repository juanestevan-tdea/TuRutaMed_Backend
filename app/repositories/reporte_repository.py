"""Repositorio de reportes ciudadanos en MongoDB."""

from typing import Any

from app.core.exceptions import DomainException


class ReporteRepository:
    """Encapsula la colección ``reportes``."""

    def __init__(self, db: Any) -> None:
        self.db = db

    def _collection(self):
        if self.db is None:
            raise DomainException(
                message="Base de datos documental no disponible",
                code="DB_UNAVAILABLE",
                status_code=503,
            )
        return self.db["reportes"]

    def crear(self, documento: dict) -> str:
        resultado = self._collection().insert_one(documento)
        return str(resultado.inserted_id)

    def contar_por_usuario(self, usuario_id: int) -> int:
        return int(self._collection().count_documents({"usuario_id": usuario_id}))
