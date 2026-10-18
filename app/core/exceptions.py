import logging
from typing import Any

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pymongo.errors import PyMongoError
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


class DomainException(Exception):
    """Excepción base del dominio, desacoplada de HTTP."""

    def __init__(
        self,
        message: str,
        code: str = "DOMAIN_ERROR",
        status_code: int = 400,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code


class NotFoundError(DomainException):
    def __init__(
        self,
        message: str = "Recurso no encontrado",
        code: str = "NOT_FOUND",
        status_code: int = 404,
    ) -> None:
        super().__init__(message, code, status_code)


class ConflictError(DomainException):
    def __init__(
        self,
        message: str = "Conflicto de estado",
        code: str = "CONFLICT",
        status_code: int = 409,
    ) -> None:
        super().__init__(message, code, status_code)


class UnauthorizedError(DomainException):
    def __init__(
        self,
        message: str = "No autorizado",
        code: str = "UNAUTHORIZED",
        status_code: int = 401,
    ) -> None:
        super().__init__(message, code, status_code)


class ForbiddenError(DomainException):
    def __init__(
        self,
        message: str = "Acceso denegado",
        code: str = "FORBIDDEN",
        status_code: int = 403,
    ) -> None:
        super().__init__(message, code, status_code)


class ValidationError(DomainException):
    def __init__(
        self,
        message: str = "Datos inválidos",
        code: str = "VALIDATION_ERROR",
        status_code: int = 422,
    ) -> None:
        super().__init__(message, code, status_code)


def registrar_manejadores_excepciones(app: Any) -> None:
    """Registra interceptores globales de errores para la API de TuRutaMed"""

    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException):
        logger.error("DomainException [%s]: %s", exc.code, exc.message)
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "type": f"https://turutamed.com/errors/{exc.code}",
                "title": exc.code,
                "status": exc.status_code,
                "detail": exc.message,
                "instance": str(request.url.path),
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validacion_error_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "estado": "error",
                "codigo": 422,
                "mensaje": "Los datos enviados no tienen el formato correcto.",
                "detalles": exc.errors(),
            },
        )

    @app.exception_handler(PyMongoError)
    async def mongodb_error_handler(request: Request, exc: PyMongoError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "estado": "error",
                "codigo": 500,
                "mensaje": "Error de comunicación con la base de datos geográfica (MongoDB Atlas).",
                "detalles": str(exc),
            },
        )

    @app.exception_handler(SQLAlchemyError)
    async def mysql_error_handler(request: Request, exc: SQLAlchemyError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "estado": "error",
                "codigo": 500,
                "mensaje": "Error en el motor de usuarios y autenticación (MySQL).",
                "detalles": "Ocurrió un problema interno en el servidor.",
            },
        )
