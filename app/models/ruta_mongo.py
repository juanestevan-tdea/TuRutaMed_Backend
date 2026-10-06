from app.database import mongo_db
from bson import ObjectId

coleccion_rutas = mongo_db["rutas"]

# CREAMOS EL ÍNDICE GEOESPACIAL 
# Esto le permite a MongoDB hacer búsquedas de mapas ultrarrápidas
coleccion_rutas.create_index([("paraderos.coordenadas", "2dsphere")])

def insertar_ruta_db(ruta_data: dict):
    """Inserta una nueva ruta de transporte con geolocalización en MongoDB Atlas"""
    resultado = coleccion_rutas.insert_one(ruta_data)
    return str(resultado.inserted_id)

def obtener_todas_las_rutas_db():
    """Consulta todas las rutas geolocalizadas disponibles"""
    rutas = []
    for ruta in coleccion_rutas.find():
        ruta["_id"] = str(ruta["_id"])
        rutas.append(ruta)
    return rutas
def buscar_paraderos_cercanos_db(longitud: float, latitud: float, max_distancia_metros: int = 3000):
    """
    Busca rutas que contengan paraderos cercanos a una coordenada dada (Estilo Google Maps)
    por defecto en un radio de 3000 metros (3 km).
    """
    query = {
        "paraderos.coordenadas": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [longitud, latitud]
                },
                "$maxDistance": max_distancia_metros
            }
        }
    }
    rutas = []
    for ruta in coleccion_rutas.find(query):
        ruta["_id"] = str(ruta["_id"])
        rutas.append(ruta)
    return rutas