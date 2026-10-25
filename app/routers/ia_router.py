from fastapi import APIRouter, Request
from pydantic import BaseModel

from app.core.rate_limit import limiter
from app.services.gemini_service import (
    analizar_congestion_vial,
    consultar_asistente_rutas,
    optimizar_itinerario_multimodal,
)

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
    Consulta opciones de transporte multimodal en Medellín usando Gemini.

    Los errores del proveedor se propagan con su detalle real para que el
    frontend no muestre respuestas de "mantenimiento" que el modelo nunca dio.
    """
    respuesta = consultar_asistente_rutas(body.pregunta)
    return {
        "estado": "exitoso",
        "asistente": "TuRutaMed AI",
        "respuesta": respuesta,
    }


@router.post("/optimizar-ruta")
@limiter.limit("10/minute")
def optimizar_ruta(request: Request, body: OptimizarRutaRequest):
    """Optimiza un itinerario multimodal entre origen y destino usando Gemini AI."""
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


@router.post("/analizar-congestion")
@limiter.limit("10/minute")
def analizar_congestion(request: Request, body: AnalizarCongestionRequest):
    """Analiza alertas viales y genera un resumen predictivo de congestión."""
    respuesta = analizar_congestion_vial(body.alertas)
    return {
        "estado": "exitoso",
        "asistente": "TuRutaMed AI",
        "analisis": respuesta,
    }
