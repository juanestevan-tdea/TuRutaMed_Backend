"""Capa de servicio para el dominio de Usuarios."""

from app.core.exceptions import ConflictError, UnauthorizedError, ValidationError
from app.core.seguridad import (
    obtener_hash_contrasena,
    verificar_contrasena,
)
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario_schema import (
    Token,
    UsuarioLogin,
    UsuarioRegistro,
    normalizar_rol_publico,
)
from app.services.auth_service import login as crear_tokens_login


class UsuarioService:
    def __init__(self, repository: UsuarioRepository) -> None:
        self.repository = repository

    def registrar_usuario(self, usuario_in: UsuarioRegistro) -> Usuario:
        # Defensa en profundidad: aunque el schema ya valida, el servicio nunca
        # confía en un rol recibido del cliente.
        rol = normalizar_rol_publico(usuario_in.rol)
        if rol is None:
            raise ValidationError(
                message="Rol no permitido. Solo se puede registrar como 'Usuario' o 'Pasajero'.",
                code="INVALID_ROLE",
            )

        existente = self.repository.obtener_por_email(usuario_in.email)
        if existente is not None:
            raise ConflictError(message="Este correo electrónico ya está registrado.")

        clave_segura = obtener_hash_contrasena(usuario_in.contrasena)
        nuevo_usuario = Usuario(
            nombre=usuario_in.nombre,
            email=usuario_in.email,
            contrasena_encriptada=clave_segura,
            rol=rol,
        )
        return self.repository.crear_usuario(nuevo_usuario)

    def iniciar_sesion(self, usuario_in: UsuarioLogin) -> Token:
        usuario_bd = self.repository.obtener_por_email(usuario_in.email)
        if usuario_bd is None:
            raise UnauthorizedError(message="Correo o contraseña incorrectos")

        if not verificar_contrasena(usuario_in.contrasena, str(usuario_bd.contrasena_encriptada)):
            raise UnauthorizedError(message="Correo o contraseña incorrectos")

        tokens = crear_tokens_login(usuario_bd)
        return Token(**tokens)
