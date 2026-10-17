# app/database_seeder.py
"""
==============================================================================
TuRutaMed - Seeder de Datos Reales del SITVA (Sistema Integrado de Transporte
del Valle de Aburrá)
==============================================================================
Puebla la colección `rutas` de MongoDB con información realista de las líneas
del Metro, Metrocable, Tranvía y buses integrados de Medellín, incluyendo
marcas de accesibilidad (RF-09).

Ejecución:
    python -m app.database_seeder
o se invoca automáticamente desde main.py si la colección está vacía.
==============================================================================
"""

from typing import List, Dict, Any
from app.database import get_mongo_db


# ----------------------------------------------------------------------------
# Catálogo de rutas reales del SITVA / Valle de Aburrá
# ----------------------------------------------------------------------------
SITVA_ROUTES: List[Dict[str, Any]] = [
    # ---------------- Metro de Medellín ----------------
    {
        "nombre_ruta": "Línea A: Niquía - La Estrella",
        "tipo_transporte": "Metro",
        "origen": "Niquía",
        "destino": "La Estrella",
        "tiempo_estimado_minutos": 45,
        "coordenadas": [-75.5420, 6.3370],  # Niquía
        "paraderos": [
            {"nombre_paradero": "Niquía", "coordenadas": [-75.5420, 6.3370], "orden": 1},
            {"nombre_paradero": "Bello", "coordenadas": [-75.5560, 6.3330], "orden": 2},
            {"nombre_paradero": "Madera", "coordenadas": [-75.5600, 6.3150], "orden": 3},
            {"nombre_paradero": "Acevedo", "coordenadas": [-75.5610, 6.2980], "orden": 4},
            {"nombre_paradero": "Tricentenario", "coordenadas": [-75.5620, 6.2850], "orden": 5},
            {"nombre_paradero": "Caribe", "coordenadas": [-75.5640, 6.2780], "orden": 6},
            {"nombre_paradero": "Universidad", "coordenadas": [-75.5660, 6.2700], "orden": 7},
            {"nombre_paradero": "Hospital", "coordenadas": [-75.5680, 6.2620], "orden": 8},
            {"nombre_paradero": "Prado", "coordenadas": [-75.5700, 6.2550], "orden": 9},
            {"nombre_paradero": "Parque Berrío", "coordenadas": [-75.5710, 6.2500], "orden": 10},
            {"nombre_paradero": "San Antonio", "coordenadas": [-75.5720, 6.2460], "orden": 11},
            {"nombre_paradero": "Alpujarra", "coordenadas": [-75.5730, 6.2400], "orden": 12},
            {"nombre_paradero": "Exposiciones", "coordenadas": [-75.5750, 6.2320], "orden": 13},
            {"nombre_paradero": "Industriales", "coordenadas": [-75.5780, 6.2250], "orden": 14},
            {"nombre_paradero": "Poblado", "coordenadas": [-75.5790, 6.2100], "orden": 15},
            {"nombre_paradero": "Ayurá", "coordenadas": [-75.5810, 6.1950], "orden": 16},
            {"nombre_paradero": "Envigado", "coordenadas": [-75.5830, 6.1750], "orden": 17},
            {"nombre_paradero": "Itagüí", "coordenadas": [-75.5850, 6.1620], "orden": 18},
            {"nombre_paradero": "Sabaneta", "coordenadas": [-75.5870, 6.1520], "orden": 19},
            {"nombre_paradero": "La Estrella", "coordenadas": [-75.5890, 6.1450], "orden": 20},
        ],
        "accesible": True,
        "horario": "04:30 - 23:00",
    },
    {
        "nombre_ruta": "Línea B: San Antonio - San Javier",
        "tipo_transporte": "Metro",
        "origen": "San Antonio",
        "destino": "San Javier",
        "tiempo_estimado_minutos": 12,
        "coordenadas": [-75.5720, 6.2460],  # San Antonio
        "paraderos": [
            {"nombre_paradero": "San Antonio", "coordenadas": [-75.5720, 6.2460], "orden": 1},
            {"nombre_paradero": "Cisneros", "coordenadas": [-75.5760, 6.2480], "orden": 2},
            {"nombre_paradero": "Suramericana", "coordenadas": [-75.5800, 6.2500], "orden": 3},
            {"nombre_paradero": "Estadio", "coordenadas": [-75.5840, 6.2520], "orden": 4},
            {"nombre_paradero": "Floresta", "coordenadas": [-75.5880, 6.2540], "orden": 5},
            {"nombre_paradero": "Santa Lucía", "coordenadas": [-75.5920, 6.2560], "orden": 6},
            {"nombre_paradero": "San Javier", "coordenadas": [-75.5960, 6.2580], "orden": 7},
        ],
        "accesible": True,
        "horario": "04:30 - 23:00",
    },
    # ---------------- Metrocables ----------------
    {
        "nombre_ruta": "Metrocable Línea K: Acevedo - Santo Domingo",
        "tipo_transporte": "Metrocable",
        "origen": "Acevedo",
        "destino": "Santo Domingo",
        "tiempo_estimado_minutos": 12,
        "coordenadas": [-75.5610, 6.2980],  # Acevedo
        "paraderos": [
            {"nombre_paradero": "Acevedo", "coordenadas": [-75.5610, 6.2980], "orden": 1},
            {"nombre_paradero": "Andalucía", "coordenadas": [-75.5550, 6.3050], "orden": 2},
            {"nombre_paradero": "Popular", "coordenadas": [-75.5480, 6.3120], "orden": 3},
            {"nombre_paradero": "Santo Domingo", "coordenadas": [-75.5420, 6.3180], "orden": 4},
        ],
        "accesible": True,
        "horario": "04:30 - 23:00",
    },
    {
        "nombre_ruta": "Metrocable Línea J: San Javier - La Aurora",
        "tipo_transporte": "Metrocable",
        "origen": "San Javier",
        "destino": "La Aurora",
        "tiempo_estimado_minutos": 10,
        "coordenadas": [-75.5960, 6.2580],  # San Javier
        "paraderos": [
            {"nombre_paradero": "San Javier", "coordenadas": [-75.5960, 6.2580], "orden": 1},
            {"nombre_paradero": "Juan XXIII", "coordenadas": [-75.6000, 6.2620], "orden": 2},
            {"nombre_paradero": "Vallejuelos", "coordenadas": [-75.6040, 6.2660], "orden": 3},
            {"nombre_paradero": "La Aurora", "coordenadas": [-75.6080, 6.2700], "orden": 4},
        ],
        "accesible": True,
        "horario": "04:30 - 23:00",
    },
    # ---------------- Tranvía de Ayacucho ----------------
    {
        "nombre_ruta": "Tranvía de Ayacucho: San Antonio - Oriente",
        "tipo_transporte": "Tranvía",
        "origen": "San Antonio",
        "destino": "Oriente",
        "tiempo_estimado_minutos": 15,
        "coordenadas": [-75.5720, 6.2460],  # San Antonio
        "paraderos": [
            {"nombre_paradero": "San Antonio", "coordenadas": [-75.5720, 6.2460], "orden": 1},
            {"nombre_paradero": "Bicentenario", "coordenadas": [-75.5680, 6.2440], "orden": 2},
            {"nombre_paradero": "Buenos Aires", "coordenadas": [-75.5640, 6.2420], "orden": 3},
            {"nombre_paradero": "Miraflores", "coordenadas": [-75.5600, 6.2400], "orden": 4},
            {"nombre_paradero": "Loyola", "coordenadas": [-75.5560, 6.2380], "orden": 5},
            {"nombre_paradero": "Alejandro Echavarría", "coordenadas": [-75.5520, 6.2360], "orden": 6},
            {"nombre_paradero": "Oriente", "coordenadas": [-75.5480, 6.2340], "orden": 7},
        ],
        "accesible": True,
        "horario": "05:00 - 23:00",
    },
    # ---------------- Buses Integrados ----------------
    {
        "nombre_ruta": "Bus Integrado C6-010: Manrique - Centro",
        "tipo_transporte": "Bus Integrado",
        "origen": "Manrique Oriental",
        "destino": "Centro (Parque Berrío)",
        "tiempo_estimado_minutos": 25,
        "coordenadas": [-75.5583, 6.2705],
        "paraderos": [
            {"nombre_paradero": "Manrique Oriental", "coordenadas": [-75.5583, 6.2705], "orden": 1},
            {"nombre_paradero": "Aranjuez", "coordenadas": [-75.5620, 6.2680], "orden": 2},
            {"nombre_paradero": "Moravia", "coordenadas": [-75.5660, 6.2650], "orden": 3},
            {"nombre_paradero": "Universidad", "coordenadas": [-75.5660, 6.2700], "orden": 4},
            {"nombre_paradero": "Parque Berrío", "coordenadas": [-75.5710, 6.2500], "orden": 5},
        ],
        "accesible": True,
        "horario": "05:00 - 22:30",
    },
    {
        "nombre_ruta": "Bus Integrado C3-001: Castilla - Centro",
        "tipo_transporte": "Bus Integrado",
        "origen": "Castilla",
        "destino": "Centro (San Antonio)",
        "tiempo_estimado_minutos": 20,
        "coordenadas": [-75.5750, 6.2850],
        "paraderos": [
            {"nombre_paradero": "Castilla", "coordenadas": [-75.5750, 6.2850], "orden": 1},
            {"nombre_paradero": "Floresta", "coordenadas": [-75.5880, 6.2540], "orden": 2},
            {"nombre_paradero": "Estadio", "coordenadas": [-75.5840, 6.2520], "orden": 3},
            {"nombre_paradero": "San Antonio", "coordenadas": [-75.5720, 6.2460], "orden": 4},
        ],
        "accesible": False,
        "horario": "05:00 - 22:00",
    },
    {
        "nombre_ruta": "Bus Alimentador 301: Santo Domingo - Popular",
        "tipo_transporte": "Bus Alimentador",
        "origen": "Santo Domingo",
        "destino": "Popular",
        "tiempo_estimado_minutos": 15,
        "coordenadas": [-75.5420, 6.3180],
        "paraderos": [
            {"nombre_paradero": "Santo Domingo", "coordenadas": [-75.5420, 6.3180], "orden": 1},
            {"nombre_paradero": "Popular", "coordenadas": [-75.5480, 6.3120], "orden": 2},
        ],
        "accesible": True,
        "horario": "04:30 - 23:00",
    },
    {
        "nombre_ruta": "Bus Alimentador 302: San Javier - La Aurora",
        "tipo_transporte": "Bus Alimentador",
        "origen": "San Javier",
        "destino": "La Aurora",
        "tiempo_estimado_minutos": 12,
        "coordenadas": [-75.5960, 6.2580],
        "paraderos": [
            {"nombre_paradero": "San Javier", "coordenadas": [-75.5960, 6.2580], "orden": 1},
            {"nombre_paradero": "Juan XXIII", "coordenadas": [-75.6000, 6.2620], "orden": 2},
            {"nombre_paradero": "La Aurora", "coordenadas": [-75.6080, 6.2700], "orden": 3},
        ],
        "accesible": False,
        "horario": "05:00 - 22:30",
    },
]


def seed_rutas_if_empty(db) -> int:
    """
    Puebla la colección `rutas` si está vacía.
    Retorna el número de documentos insertados.
    """
    collection = db["rutas"]
    if collection.count_documents({}) > 0:
        print("[Seeder] La colección 'rutas' ya contiene datos. Se omite el seeding.")
        return 0

    result = collection.insert_many(SITVA_ROUTES)
    inserted = len(result.inserted_ids)
    print(f"[Seeder] Se insertaron {inserted} rutas del SITVA en MongoDB.")
    return inserted


def run_seeder():
    """Ejecuta el seeder de forma independiente."""
    db = get_mongo_db()
    seed_rutas_if_empty(db)


if __name__ == "__main__":
    run_seeder()