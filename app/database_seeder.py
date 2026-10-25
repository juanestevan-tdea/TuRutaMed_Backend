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
    python -m app.database_seeder              # upsert del catálogo SITVA
    python -m app.database_seeder --force      # borra rutas actuales y deja solo el catálogo
También se invoca automáticamente desde main.py en modo upsert.
==============================================================================
"""

import argparse
from typing import Any

from app.database import get_mongo_db

# ----------------------------------------------------------------------------
# Catálogo de rutas reales del SITVA / Valle de Aburrá
# ----------------------------------------------------------------------------
SITVA_ROUTES: list[dict[str, Any]] = [
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
            {
                "nombre_paradero": "Alejandro Echavarría",
                "coordenadas": [-75.5520, 6.2360],
                "orden": 6,
            },
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


def _normalizar_coordenadas(valor: Any, contexto: str) -> list[float]:
    """Valida y normaliza un punto GeoJSON en orden [longitud, latitud]."""
    if not isinstance(valor, (list, tuple)) or len(valor) != 2:
        raise ValueError(f"{contexto}: 'coordenadas' debe ser [longitud, latitud].")
    try:
        longitud, latitud = float(valor[0]), float(valor[1])
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{contexto}: las coordenadas deben ser numéricas.") from exc
    if not -180.0 <= longitud <= 180.0:
        raise ValueError(f"{contexto}: longitud fuera de rango ({longitud}).")
    if not -90.0 <= latitud <= 90.0:
        raise ValueError(f"{contexto}: latitud fuera de rango ({latitud}).")
    return [longitud, latitud]


def _normalizar_paradero(paradero: dict[str, Any], indice: int, nombre_ruta: str) -> dict[str, Any]:
    """Deja cada paradero con un único esquema: coordenadas GeoJSON + orden."""
    contexto = f"ruta '{nombre_ruta}', paradero #{indice}"
    if not isinstance(paradero, dict):
        raise ValueError(f"{contexto}: el paradero debe ser un objeto.")

    normalizado = dict(paradero)
    if "coordenadas" in normalizado:
        coordenadas = normalizado["coordenadas"]
    elif "longitud" in normalizado and "latitud" in normalizado:
        # Migración del esquema viejo: latitud/longitud -> coordenadas.
        coordenadas = [normalizado["longitud"], normalizado["latitud"]]
    else:
        raise ValueError(f"{contexto}: falta 'coordenadas' (o 'longitud' y 'latitud').")

    normalizado.pop("latitud", None)
    normalizado.pop("longitud", None)
    normalizado["coordenadas"] = _normalizar_coordenadas(coordenadas, contexto)

    try:
        normalizado["orden"] = int(normalizado.get("orden", indice))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{contexto}: 'orden' debe ser un entero.") from exc
    return normalizado


def _normalizar_ruta(ruta: dict[str, Any]) -> dict[str, Any]:
    """Normaliza una ruta completa al esquema que espera el índice 2dsphere."""
    if not isinstance(ruta, dict):
        raise ValueError("Cada ruta del catálogo debe ser un objeto.")

    normalizada = dict(ruta)
    nombre = str(normalizada.get("nombre_ruta", "")).strip()
    if not nombre:
        raise ValueError("La ruta no tiene 'nombre_ruta'.")
    normalizada["nombre_ruta"] = nombre

    paraderos = normalizada.get("paraderos") or []
    if not isinstance(paraderos, list) or not paraderos:
        raise ValueError(f"La ruta '{nombre}' no tiene paraderos.")
    normalizada["paraderos"] = [
        _normalizar_paradero(paradero, indice, nombre)
        for indice, paradero in enumerate(paraderos, start=1)
    ]

    if "coordenadas" in normalizada:
        normalizada["coordenadas"] = _normalizar_coordenadas(
            normalizada["coordenadas"], f"ruta '{nombre}'"
        )
    else:
        normalizada["coordenadas"] = normalizada["paraderos"][0]["coordenadas"]
    normalizada.pop("latitud", None)
    normalizada.pop("longitud", None)
    return normalizada


def _validar_catalogo(rutas: list[dict[str, Any]]) -> None:
    """Falla rápido si el catálogo está vacío o tiene nombres repetidos."""
    if not rutas:
        raise ValueError("El catálogo SITVA está vacío.")
    nombres = [ruta["nombre_ruta"] for ruta in rutas]
    duplicados = sorted({nombre for nombre in nombres if nombres.count(nombre) > 1})
    if duplicados:
        raise ValueError(f"El catálogo SITVA contiene rutas duplicadas: {duplicados}")


def _asegurar_indice_geoespacial(collection: Any) -> None:
    """Crea el índice 2dsphere sobre paraderos.coordenadas (idempotente)."""
    collection.create_index(
        [("paraderos.coordenadas", "2dsphere")],
        name="paraderos.coordenadas_2dsphere",
    )


def seed_rutas_if_empty(db: Any, force: bool = False) -> int:
    """
    Sincroniza el catálogo SITVA en la colección `rutas`.

    - force=False: hace upsert de las rutas del catálogo por `nombre_ruta`.
      No borra rutas personalizadas que no estén en el catálogo.
    - force=True: elimina todas las rutas actuales y deja únicamente el catálogo
      SITVA. Es la opción para reemplazar datos viejos o con esquemas mezclados.

    Retorna el número de rutas del catálogo sincronizadas.
    """
    if db is None:
        raise RuntimeError("MongoDB no está disponible; no se puede sembrar el catálogo SITVA.")

    rutas = [_normalizar_ruta(ruta) for ruta in SITVA_ROUTES]
    _validar_catalogo(rutas)

    collection = db["rutas"]

    if force:
        eliminadas = collection.delete_many({}).deleted_count
        print(f"[Seeder] Se eliminaron {eliminadas} rutas existentes de 'rutas'.")

    # El índice debe existir antes de consultar con $near.
    _asegurar_indice_geoespacial(collection)

    for ruta in rutas:
        collection.replace_one({"nombre_ruta": ruta["nombre_ruta"]}, ruta, upsert=True)

    total = collection.count_documents({})
    print(
        f"[Seeder] Catálogo SITVA sincronizado: {len(rutas)} rutas. "
        f"Total en la colección 'rutas': {total}."
    )
    return len(rutas)


def run_seeder(force: bool = False) -> int:
    """Ejecuta el seeder de forma independiente."""
    db = get_mongo_db()
    if db is None:
        raise RuntimeError("No se pudo conectar a MongoDB. Revisa MONGO_URL.")
    return seed_rutas_if_empty(db, force=force)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sincroniza el catálogo de rutas del SITVA en MongoDB."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Borra las rutas actuales y deja únicamente el catálogo SITVA.",
    )
    args = parser.parse_args()
    run_seeder(force=args.force)


if __name__ == "__main__":
    main()
