from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base


class TarjetaCivicaDB(Base):
    """Tarjeta Cívica persistida en MySQL.

    El saldo se almacena con ``Numeric`` para evitar los errores de redondeo
    típicos de los tipos de punto flotante en operaciones monetarias.
    """

    __tablename__ = "tarjetas_civicas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    numero: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)
    saldo: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=Decimal("0.00"))
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
