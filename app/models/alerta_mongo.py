import logging
from datetime import UTC, datetime

from app.database import mongo_db

logger = logging.getLogger(__name__)

coleccion_alertas = mongo_db["alertas"] if mongo_db is not None else None

# Creamos un índice geoespacial para las alertas (Modo Waze por cercanía)
if coleccion_alertas is not None:
    try:
        coleccion_alertas.create_index([("coordenadas", "2dsphere")])
    except Exception as e:  # noqa: BLE001
        logger.warning("No se pudo inicializar el índice 2dsphere en alertas: %s", e)


def insertar_alerta_db(alerta_data: dict):
    """Inserta una nueva incidencia o reporte ciudadano en MongoDB Atlas"""
    alerta_data["fecha_reporte"] = datetime.now(UTC).isoformat()
    resultado = coleccion_alertas.insert_one(alerta_data)
    return str(resultado.inserted_id)


def obtener_alertas_db():
    """Obtiene todas las alertas e incidencias activas en la ciudad"""
    alertas = []
    for alerta in coleccion_alertas.find():
        alerta["_id"] = str(alerta["_id"])
        alertas.append(alerta)
    return alertas
