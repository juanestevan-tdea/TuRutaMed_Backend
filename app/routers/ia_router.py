from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

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
def consultar_asistente_transporte(request: ConsultaMovilidadRequest):
    """
    Endpoint modular para consultar opciones de transporte multimodal
    y recomendaciones en Medellín usando Gemini.
    Implementa un patrón de fallback para no romper la experiencia del usuario.
    """
    try:
        respuesta = consultar_asistente_rutas(request.pregunta)
        return {
            "estado": "exitoso",
            "asistente": "TuRutaMed AI",
            "respuesta": respuesta,
        }
    except Exception as e:  # noqa: BLE001
        print(f"Error real de la IA: {e}")
        return {
            "estado": "fallback",
            "asistente": "TuRutaMed AI",
            "respuesta": "En este momento mis servidores de IA están en mantenimiento, pero te sugiero tomar la Línea A del Metro.",
        }


@router.post("/optimizar-ruta")
def optimizar_ruta(request: OptimizarRutaRequest):
    """Optimiza un itinerario multimodal entre origen y destino usando Gemini AI."""
    try:
        respuesta = optimizar_itinerario_multimodal(
            origen=request.origen,
            destino=request.destino,
            alertas=request.alertas,
        )
        return {
            "estado": "exitoso",
            "asistente": "TuRutaMed AI",
            "itinerario": respuesta,
        }
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Error al optimizar la ruta: {e!s}")


@router.post("/analizar-congestion")
def analizar_congestion(request: AnalizarCongestionRequest):
    """Analiza alertas viales y genera un resumen predictivo de congestión."""
    try:
        respuesta = analizar_congestion_vial(request.alertas)
        return {
            "estado": "exitoso",
            "asistente": "TuRutaMed AI",
            "analisis": respuesta,
        }
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Error al analizar congestión: {e!s}")
