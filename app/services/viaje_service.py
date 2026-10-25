"""Capa de servicio para viajes e historial (MongoDB)."""

from datetime import UTC, datetime

from app.domain.modelos_poo import Viaje, ViajeMultimodal
from app.models.usuario import Usuario
from app.repositories.viaje_repository import ViajeRepository
from app.schemas.viaje_schema import (
    DuracionViajeRequest,
    DuracionViajeRespuesta,
    HistorialViajesRespuesta,
    ViajeHistorialItem,
    ViajeMultimodalRequest,
    ViajeMultimodalRespuesta,
)


class ViajeService:
    def __init__(self, repository: ViajeRepository) -> None:
        self.repository = repository

    def calcular_duracion(
        self, usuario: Usuario, payload: DuracionViajeRequest
    ) -> DuracionViajeRespuesta:
        viaje = Viaje(
            origen=payload.origen,
            destino=payload.destino,
            duracion_minutos=payload.duracion_minutos,
        )
        duracion = viaje.calcular_duracion()

        self.repository.crear(
            {
                "usuario_id": usuario.id,
                "usuario_email": usuario.email,
                "tipo": "simple",
                "origen": viaje.origen,
                "destino": viaje.destino,
                "duracion_minutos": duracion,
                "secuencia_rutas": None,
                "itinerario": None,
                "fecha_creacion": datetime.now(UTC),
            }
        )

        return DuracionViajeRespuesta(
            origen=viaje.origen,
            destino=viaje.destino,
            duracion_minutos=duracion,
        )

    def planificar_multimodal(
        self, usuario: Usuario, payload: ViajeMultimodalRequest
    ) -> ViajeMultimodalRespuesta:
        viaje_m = ViajeMultimodal(secuencia_rutas=payload.secuencia_rutas)
        itinerario = viaje_m.mostrar_secuencia()

        self.repository.crear(
            {
                "usuario_id": usuario.id,
                "usuario_email": usuario.email,
                "tipo": "multimodal",
                "origen": viaje_m.secuencia_rutas[0],
                "destino": viaje_m.secuencia_rutas[-1],
                "duracion_minutos": None,
                "secuencia_rutas": viaje_m.secuencia_rutas,
                "itinerario": itinerario,
                "fecha_creacion": datetime.now(UTC),
            }
        )

        return ViajeMultimodalRespuesta(
            secuencia_rutas=viaje_m.secuencia_rutas,
            itinerario=itinerario,
        )

    def consultar_historial(
        self, usuario: Usuario, limit: int, skip: int
    ) -> HistorialViajesRespuesta:
        total = self.repository.contar_por_usuario(usuario.id)
        documentos = self.repository.listar_por_usuario(usuario.id, skip=skip, limit=limit)
        historial = [
            ViajeHistorialItem(
                id=documento["_id"],
                tipo=documento.get("tipo", "simple"),
                origen=documento.get("origen"),
                destino=documento.get("destino"),
                duracion_minutos=documento.get("duracion_minutos"),
                secuencia_rutas=documento.get("secuencia_rutas"),
                itinerario=documento.get("itinerario"),
                fecha_creacion=documento.get("fecha_creacion"),
            )
            for documento in documentos
        ]
        return HistorialViajesRespuesta(
            usuario=usuario.email,
            historial=historial,
            total=total,
            limit=limit,
            skip=skip,
        )
