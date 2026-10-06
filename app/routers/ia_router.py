import os
from fastapi import APIRouter, HTTPException
from google import genai
from pydantic import BaseModel

router = APIRouter(prefix="/ia", tags=["Inteligencia Artificial - Asistente TuRutaMed"])

# Inicializar el cliente utilizando la variable de entorno que guardaste en el .env
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

class ConsultaMovilidadRequest(BaseModel):
    pregunta: str

@router.post("/asistente-ruta")
def consultar_asistente_transporte(request: ConsultaMovilidadRequest):
    """
    Endpoint modular para consultar opciones de transporte multimodal 
    y recomendaciones en Medellín usando Gemini.
    """
    try:
        prompt_completo = (
            "Eres un asistente experto en movilidad urbana, transporte público "
            "(Metro, metrocables, buses integrados) y geolocalización en el Valle de Aburrá, Medellín. "
            f"Responde de forma clara y útil a la siguiente consulta del ciudadano: {request.pregunta}"
        )
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_completo,
        )
        return {
            "estado": "exitoso",
            "asistente": "TuRutaMed AI",
            "respuesta": response.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud con IA: {str(e)}")