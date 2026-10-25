"""Repositorio de acceso a datos para las tarjetas Cívica (MySQL)."""

from decimal import Decimal

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.civica import TarjetaCivicaDB


class CivicaRepository:
    """Encapsula las consultas y escrituras de tarjetas Cívica."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def obtener_por_numero(self, numero: str, *, bloquear: bool = False) -> TarjetaCivicaDB | None:
        query = self.db.query(TarjetaCivicaDB).filter(TarjetaCivicaDB.numero == numero)
        if bloquear:
            query = query.with_for_update()
        return query.first()

    def crear(self, numero: str, saldo: Decimal = Decimal("0.00")) -> TarjetaCivicaDB:
        tarjeta = TarjetaCivicaDB(numero=numero, saldo=saldo)
        self.db.add(tarjeta)
        self.db.commit()
        self.db.refresh(tarjeta)
        return tarjeta

    def obtener_o_crear(self, numero: str) -> TarjetaCivicaDB:
        """Obtiene la tarjeta o la crea, tolerando dos peticiones concurrentes."""
        tarjeta = self.obtener_por_numero(numero)
        if tarjeta is not None:
            return tarjeta

        try:
            return self.crear(numero)
        except IntegrityError:
            # Otra petición creó la misma tarjeta entre la consulta y el insert.
            self.db.rollback()
            tarjeta = self.obtener_por_numero(numero)
            if tarjeta is None:
                raise
            return tarjeta

    def obtener_para_actualizar(self, numero: str) -> TarjetaCivicaDB:
        """Obtiene la tarjeta bloqueando la fila para una recarga segura."""
        tarjeta = self.obtener_por_numero(numero, bloquear=True)
        if tarjeta is not None:
            return tarjeta
        return self.obtener_o_crear(numero)

    def guardar(self, tarjeta: TarjetaCivicaDB) -> TarjetaCivicaDB:
        self.db.commit()
        self.db.refresh(tarjeta)
        return tarjeta

    def rollback(self) -> None:
        self.db.rollback()
