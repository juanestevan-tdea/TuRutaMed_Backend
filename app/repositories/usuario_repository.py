"""Repositorio de acceso a datos para el dominio de Usuarios."""

from sqlalchemy.orm import Session

from app.models.usuario import Usuario


class UsuarioRepository:
    """Encapsula las consultas SQL relacionadas con usuarios."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def obtener_por_email(self, email: str) -> Usuario | None:
        return self.db.query(Usuario).filter(Usuario.email == email).first()

    def crear_usuario(self, usuario: Usuario) -> Usuario:
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario
