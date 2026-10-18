"""Configuración de logging estructurado en JSON para TuRutaMed."""

import logging
from contextvars import ContextVar

from pythonjsonlogger.jsonlogger import JsonFormatter

request_id_ctx_var: ContextVar[str] = ContextVar("request_id", default="-")


class RequestIDFilter(logging.Filter):
    """Inyecta el request_id del ContextVar en cada LogRecord."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_ctx_var.get()
        return True


def configure_logging() -> None:
    """Configura el logger raíz con formato JSON."""
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s",
        rename_fields={"asctime": "timestamp"},
    )
    handler.setFormatter(formatter)
    handler.addFilter(RequestIDFilter())

    root.handlers = [handler]
    root.addFilter(RequestIDFilter())
