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

from fastapi import HTTPException, status
from google import genai
from google.genai import types

from app.core.config import get_settings

settings = get_settings()


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


def obtener_modelo_disponible() -> str:
    """Consulta dinámicamente los modelos disponibles y retorna el primero que soporte generateContent."""
    fallback = settings.gemini_model
    try:
        client = _get_client()
        for modelo in client.models.list():
            nombre = getattr(modelo, "name", None) or getattr(modelo, "model", None)
            metodos = getattr(modelo, "supported_generation_methods", None) or []
            if nombre and "generateContent" in (metodos or []):
                # El nombre puede venir como 'models/gemini-...' o solo el id
                nombre_limpio = nombre.split("/")[-1] if "/" in nombre else nombre
                print(f"Usando modelo: {nombre_limpio}")
                return nombre_limpio
    except Exception as e:  # noqa: BLE001
        print(f"[IA] No se pudo listar modelos disponibles: {e}")
    print(f"Usando modelo de respaldo: {fallback}")
    return fallback


def consultar_asistente_rutas(prompt_usuario: str, modelo: str | None = None) -> str:
    """
    Consulta al asistente de IA sobre rutas y movilidad en el Valle de Aburrá.
    Usa un modelo disponible dinámicamente y hace fallback a gemini-1.5-flash si falla.
    Lanza HTTP 503 si todos los modelos fallan.
    """
    if modelo is None:
        modelo = obtener_modelo_disponible()

    modelos_a_intentar = [modelo, settings.gemini_model]
    # Eliminar duplicados manteniendo orden
    vistos = set()
    modelos_unicos = []
    for m in modelos_a_intentar:
        if m not in vistos:
            vistos.add(m)
            modelos_unicos.append(m)

    ultimo_error = None
    for modelo_actual in modelos_unicos:
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
            print(f"[IA] Respuesta generada con el modelo: {modelo_actual}")
            return str(response.text)
        except Exception as e:  # noqa: BLE001
            ultimo_error = e
            print(f"[IA] Fallo con el modelo {modelo_actual}: {e}")
            continue

    print("[IA] Todos los modelos fallaron.")
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="El servicio de IA no se encuentra disponible temporalmente.",
    ) from ultimo_error


def optimizar_itinerario_multimodal(origen: str, destino: str, alertas: list | None = None) -> str:
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
