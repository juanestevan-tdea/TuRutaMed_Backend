from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pymongo.errors import PyMongoError
from sqlalchemy.exc import SQLAlchemyError

def registrar_manejadores_excepciones(app):
    """Registra interceptores globales de errores para la API de TuRutaMed"""

    @app.exception_handler(RequestValidationError)
    async def validacion_error_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "estado": "error",
                "codigo": 422,
                "mensaje": "Los datos enviados no tienen el formato correcto.",
                "detalles": exc.errors()
            }
        )

    @app.exception_handler(PyMongoError)
    async def mongodb_error_handler(request: Request, exc: PyMongoError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "estado": "error",
                "codigo": 500,
                "mensaje": "Error de comunicación con la base de datos geográfica (MongoDB Atlas).",
                "detalles": str(exc)
            }
        )

    @app.exception_handler(SQLAlchemyError)
    async def mysql_error_handler(request: Request, exc: SQLAlchemyError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "estado": "error",
                "codigo": 500,
                "mensaje": "Error en el motor de usuarios y autenticación (MySQL).",
                "detalles": "Ocurrió un problema interno en el servidor."
            }
        )