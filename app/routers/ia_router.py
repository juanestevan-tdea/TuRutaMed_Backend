import logging

from fastapi import APIRouter, Request
from pydantic import BaseModel

from app.core.exceptions import DomainException
from app.core.rate_limit import limiter
from app.services.gemini_service import (
    analizar_congestion_vial,
    consultar_asistente_rutas,
    optimizar_itinerario_multimodal,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ia", tags=["Inteligencia Artificial - Asistente TuRutaMed"])


class ConsultaMovilidadRequest(BaseModel):
    pregunta: str


class OptimizarRutaRequest(BaseModel):
    origen: str
    destino: str
    alertas: list = []


class AnalizarCongestionRequest(BaseModel):
    alertas: list = []


@router.post("/asistente-ruta")
@limiter.limit("10/minute")
def consultar_asistente_transporte(request: Request, body: ConsultaMovilidadRequest):
    """
    Endpoint modular para consultar opciones de transporte multimodal
    y recomendaciones en Medellín usando Gemini.
    Implementa un patrón de fallback para no romper la experiencia del usuario.
    """
    try:
        respuesta = consultar_asistente_rutas(body.pregunta)
        return {
            "estado": "exitoso",
            "asistente": "TuRutaMed AI",
            "respuesta": respuesta,
        }
    except Exception as e:  # noqa: BLE001
        logger.warning("Fallo en servicio de IA, activando fallback: %s", e)
        return {
            "estado": "fallback",
            "asistente": "TuRutaMed AI",
            "respuesta": "En este momento mis servidores de IA están en mantenimiento, pero te sugiero tomar la Línea A del Metro.",
        }


@router.post("/optimizar-ruta")
@limiter.limit("10/minute")
def optimizar_ruta(request: Request, body: OptimizarRutaRequest):
    """Optimiza un itinerario multimodal entre origen y destino usando Gemini AI."""
    try:
        respuesta = optimizar_itinerario_multimodal(
            origen=body.origen,
            destino=body.destino,
            alertas=body.alertas,
        )
        return {
            "estado": "exitoso",
            "asistente": "TuRutaMed AI",
            "itinerario": respuesta,
        }
    except Exception as e:  # noqa: BLE001
        raise DomainException(
            message=f"Error al optimizar la ruta: {e!s}",
            code="AI_SERVICE_ERROR",
            status_code=500,
        ) from e


@router.post("/analizar-congestion")
@limiter.limit("10/minute")
def analizar_congestion(request: Request, body: AnalizarCongestionRequest):
    """Analiza alertas viales y genera un resumen predictivo de congestión."""
    try:
        respuesta = analizar_congestion_vial(body.alertas)
        return {
            "estado": "exitoso",
            "asistente": "TuRutaMed AI",
            "analisis": respuesta,
        }
    except Exception as e:  # noqa: BLE001
        raise DomainException(
            message=f"Error al analizar congestión: {e!s}",
            code="AI_SERVICE_ERROR",
            status_code=500,
        ) from e
