"""Repositorio del historial de viajes en MongoDB."""

from typing import Any

from app.core.exceptions import DomainException


class ViajeRepository:
    """Encapsula la colección ``viajes``."""

    def __init__(self, db: Any) -> None:
        self.db = db

    def _collection(self):
        if self.db is None:
            raise DomainException(
                message="Base de datos documental no disponible",
                code="DB_UNAVAILABLE",
                status_code=503,
            )
        return self.db["viajes"]

    def crear(self, documento: dict) -> str:
        resultado = self._collection().insert_one(documento)
        return str(resultado.inserted_id)

    def listar_por_usuario(self, usuario_id: int, *, skip: int, limit: int) -> list[dict]:
        documentos: list[dict] = []
        cursor = (
            self._collection()
            .find({"usuario_id": usuario_id})
            .sort([("fecha_creacion", -1), ("_id", -1)])
            .skip(skip)
            .limit(limit)
        )
        for documento in cursor:
            documento["_id"] = str(documento["_id"])
            documentos.append(documento)
        return documentos

    def contar_por_usuario(self, usuario_id: int) -> int:
        return int(self._collection().count_documents({"usuario_id": usuario_id}))
