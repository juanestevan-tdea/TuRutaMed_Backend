from app.database import mongo_db
from datetime import datetime
from bson import ObjectId

coleccion_alertas = mongo_db["alertas"]

# Creamos un índice geoespacial para las alertas (Modo Waze por cercanía)
coleccion_alertas.create_index([("coordenadas", "2dsphere")])

def insertar_alerta_db(alerta_data: dict):
    """Inserta una nueva incidencia o reporte ciudadano en MongoDB Atlas"""
    alerta_data["fecha_reporte"] = datetime.utcnow().isoformat()
    resultado = coleccion_alertas.insert_one(alerta_data)
    return str(resultado.inserted_id)

def obtener_alertas_db():
    """Obtiene todas las alertas e incidencias activas en la ciudad"""
    alertas = []
    for alerta in coleccion_alertas.find():
        alerta["_id"] = str(alerta["_id"])
        alertas.append(alerta)
    return alertas