# app/services/gemini_service.py
"""
==============================================================================
TuRutaMed - Servicio de Inteligencia Artificial (Google Gemini)
==============================================================================
Integra el modelo Gemini 2.5 Flash para asistencia en movilidad urbana,
optimización de rutas multimodales y análisis de congestión vial.

Dependencia: google-genai
==============================================================================
"""

import os
from typing import Optional
from fastapi import HTTPException, status
from google import genai
from google.genai import types


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
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "La variable de entorno GEMINI_API_KEY no está configurada."
        )
    return genai.Client(api_key=api_key)


def consultar_asistente_rutas(prompt_usuario: str, modelo: str = "gemini-2.5-flash") -> str:
    """
    Consulta al asistente de IA sobre rutas y movilidad en el Valle de Aburrá.
    Lanza HTTP 503 si el servicio externo no está disponible.
    """
    try:
        client = _get_client()
        response = client.models.generate_content(
            model=modelo,
            contents=prompt_usuario,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.7,
                max_output_tokens=1024,
            ),
        )
        return response.text
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="El servicio de IA no se encuentra disponible temporalmente.",
        ) from e


def optimizar_itinerario_multimodal(
    origen: str, destino: str, alertas: Optional[list] = None
) -> str:
    """
    Solicita a Gemini la optimización de un itinerario multimodal entre dos puntos.
    Lanza HTTP 503 si el servicio externo no está disponible.
    """
    try:
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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="El servicio de IA no se encuentra disponible temporalmente.",
        ) from e


def analizar_congestion_vial(alertas: list) -> str:
    """
    Analiza un conjunto de alertas viales y genera un resumen predictivo.
    Lanza HTTP 503 si el servicio externo no está disponible.
    """
    try:
        prompt = (
            "Analiza las siguientes alertas viales reportadas por ciudadanos en "
            "el Valle de Aburrá y genera un resumen de la situación de tráfico, "
            "identificando zonas críticas y recomendaciones para los operadores:\n"
            + "\n".join(str(a) for a in alertas)
        )
        return consultar_asistente_rutas(prompt)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="El servicio de IA no se encuentra disponible temporalmente.",
        ) from e