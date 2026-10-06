from fastapi import APIRouter, status
from typing import List
from app.schemas.alerta_schema import AlertaCreate, AlertaRespuesta
from app.models.alerta_mongo import insertar_alerta_db, obtener_alertas_db

router = APIRouter(prefix="/alertas", tags=["Modo Waze - Reportes en Tiempo Real (MongoDB)"])

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def reportar_incidencia(alerta: AlertaCreate):
    """Permite a un usuario reportar un evento vial o congestión en tiempo real (Estilo Waze)"""
    alerta_dict = alerta.dict(by_alias=True)
    nuevo_id = insertar_alerta_db(alerta_dict)
    return {
        "mensaje": "¡Incidencia reportada con éxito en la red de TuRutaMed!",
        "id_alerta": nuevo_id
    }

@router.get("/", response_model=List[dict])
def listar_alertas():
    """Consulta el listado de todas las alertas y reportes activos en la ciudad"""
    return obtener_alertas_db()