# app/services/gemini_service.py
"""
==============================================================================
TuRutaMed - Servicio de Inteligencia Artificial (Google Gemini)
==============================================================================
Integra el modelo Gemini para asistencia en movilidad urbana,
optimización de rutas multimodales y análisis de congestión vial.

Dependencia: google-genai
==============================================================================
"""

import logging

from google import genai
from google.genai import types

from app.core.config import get_settings
from app.core.exceptions import DomainException

logger = logging.getLogger(__name__)

settings = get_settings()

# Modelos vigentes según la documentación de Gemini API (octubre 2026).
# El primero es el más económico y con mejor disponibilidad para este caso de uso.
MODELOS_RESPALDO = (
    "gemini-3.5-flash-lite",
    "gemini-3.8-flash",
    "gemini-flash-latest",
)


# Prompt de sistema experto en transporte metropolitano del Valle de Aburrá
SYSTEM_PROMPT = (
    "Eres TuRutaMed AI, un asistente experto en movilidad urbana y transporte "
    "público del Área Metropolitana del Valle de Aburrá (Medellín, Antioquia, "
    "Colombia). Conoces en profundidad el sistema integrado de transporte: "
    "Metro de Medellín (Líneas A y B), Metrocable (Líneas K, J, H, M, P), "
    "Tranvía de Ayacucho, Metroplús, buses integrados y alimentadores. "
    "También conoces las tarjetas Cívica, la geolocalización de paraderos, "
    "las rutas accesibles para personas con movilidad reducida (PMR) y los "
    "incidentes viales en tiempo real (Modo Waze). "
    "Responde de forma clara, concisa y útil, priorizando la seguridad del "
    "pasajero y la eficiencia del desplazamiento. Siempre ofrece alternativas "
    "multimodales cuando sea posible. Responde en español."
)


def _get_client() -> genai.Client:
    """Obtiene el cliente de Gemini configurado con la API key del entorno."""
    api_key = settings.gemini_api_key
    if not api_key:
        raise RuntimeError("La variable de entorno GEMINI_API_KEY no está configurada.")
    return genai.Client(api_key=api_key)


def _modelos_a_intentar(modelo: str | None = None) -> list[str]:
    """Construye la lista de modelos sin duplicados, respetando configuración y respaldos."""
    candidatos = [modelo, settings.gemini_model, *MODELOS_RESPALDO]
    vistos: set[str] = set()
    modelos: list[str] = []
    for candidato in candidatos:
        if not candidato or candidato in vistos:
            continue
        vistos.add(candidato)
        modelos.append(candidato)
    return modelos


def _resumen_error(error: Exception | None) -> str:
    """Resume el error real de Gemini para mostrarlo al cliente sin volcar trazas."""
    if error is None:
        return "Error desconocido al consultar Gemini."
    detalle = " ".join(str(error).split())
    return f"{detalle[:500]}..." if len(detalle) > 500 else detalle


def consultar_asistente_rutas(prompt_usuario: str, modelo: str | None = None) -> str:
    """
    Consulta al asistente de IA sobre rutas y movilidad en el Valle de Aburrá.

    Intenta el modelo configurado y luego los modelos vigentes de respaldo. Si
    todos fallan, propaga un 503 con el detalle real del último error para que
    el frontend pueda informarlo sin ocultarlo tras un mensaje de mantenimiento.
    """
    modelos = _modelos_a_intentar(modelo)

    ultimo_error: Exception | None = None
    for modelo_actual in modelos:
        try:
            client = _get_client()
            response = client.models.generate_content(
                model=modelo_actual,
                contents=prompt_usuario,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.7,
                    max_output_tokens=1024,
                ),
            )
            texto = (response.text or "").strip()
            if not texto:
                raise RuntimeError("Gemini devolvió una respuesta vacía.")
            logger.info("[IA] Respuesta generada con el modelo: %s", modelo_actual)
            return texto
        except Exception as e:  # noqa: BLE001
            ultimo_error = e
            logger.warning("[IA] Fallo con el modelo %s: %s", modelo_actual, e)

    detalle = _resumen_error(ultimo_error)
    logger.error("[IA] Todos los modelos de Gemini fallaron: %s", detalle)
    raise DomainException(
        message=(
            "No se pudo obtener respuesta de Gemini. "
            f"Modelos intentados: {', '.join(modelos)}. Detalle: {detalle}"
        ),
        code="AI_SERVICE_UNAVAILABLE",
        status_code=503,
    ) from ultimo_error


def optimizar_itinerario_multimodal(origen: str, destino: str, alertas: list | None = None) -> str:
    """
    Solicita a Gemini la optimización de un itinerario multimodal entre dos puntos.
    Lanza HTTP 503 si el servicio externo no está disponible.
    """
    alertas_texto = ""
    if alertas:
        alertas_texto = "\nAlertas viales activas: " + "; ".join(str(a) for a in alertas)

    prompt = (
        f"Planifica el mejor itinerario de transporte público multimodal "
        f"desde '{origen}' hasta '{destino}' en el Valle de Aburrá. "
        f"Incluye combinaciones de Metro, Metrocable, Tranvía, Metroplús y "
        f"buses integrados. Indica tiempos estimados y puntos de transferencia. "
        f"Considera accesibilidad (PMR) si es relevante.{alertas_texto}"
    )
    return consultar_asistente_rutas(prompt)


def analizar_congestion_vial(alertas: list) -> str:
    """
    Analiza un conjunto de alertas viales y genera un resumen predictivo.
    Lanza HTTP 503 si el servicio externo no está disponible.
    """
    prompt = (
        "Analiza las siguientes alertas viales reportadas por ciudadanos en "
        "el Valle de Aburrá y genera un resumen de la situación de tráfico, "
        "identificando zonas críticas y recomendaciones para los operadores:\n"
        + "\n".join(str(a) for a in alertas)
    )
    return consultar_asistente_rutas(prompt)
