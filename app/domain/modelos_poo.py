# app/domain/modelos_poo.py
"""
Representación en Python de los Requisitos Funcionales (RF-01 a RF-10)
para el proyecto TuRutaMed (POO - Tercer Semestre PPI).
"""

# RF-01 – Consultar rutas y horarios
class Ruta:
    def __init__(self, nombre: str, horario: str):
        self.nombre = nombre
        self.horario = horario

    def consultar_horario(self) -> str:
        return f"Ruta: {self.nombre} - Horario: {self.horario}"


# RF-02 – Notificar cambios del servicio
class Notificacion:
    def __init__(self, mensaje_alerta: str):
        self.mensaje_alerta = mensaje_alerta
        self.leida = False

    def enviar_alerta(self) -> None:
        print(f"Nueva alerta de servicio: {self.mensaje_alerta}")


# RF-03 – Calcular duración del trayecto
class Viaje:
    def __init__(self, origen: str, destino: str, duracion_minutos: int):
        self.origen = origen
        self.destino = destino
        self.duracion_minutos = duracion_minutos

    def calcular_duracion(self) -> int:
        return self.duracion_minutos


# RF-04 – Consultar alternativas cercanas
class AlternativaTransporte:
    def __init__(self, medio: str, distancia_km: float):
        self.medio = medio
        self.distancia_km = distancia_km

    def esta_cerca(self) -> bool:
        return self.distancia_km <= 2.0


# RF-05 – Planificar viaje multimodal
class ViajeMultimodal:
    def __init__(self, secuencia_rutas: list[str]):
        self.secuencia_rutas = secuencia_rutas

    def mostrar_secuencia(self) -> str:
        return f"Ruta sugerida: {' -> '.join(self.secuencia_rutas)}"


# RF-06 – Calificar y reportar el servicio
class ReporteServicio:
    def __init__(self, calificacion: int, comentario_ciudadano: str):
        self.calificacion = calificacion
        self.comentario_ciudadano = comentario_ciudadano

    def guardar_reporte(self) -> bool:
        # Lógica de registro en base de datos
        return True


# RF-07 – Consultar saldo de la tarjeta Cívica
class TarjetaCivica:
    def __init__(self, numero: str, saldo: float):
        self.numero = numero
        self.saldo = saldo

    def consultar_saldo(self) -> float:
        return self.saldo


# RF-08 – Recargar tarjeta Cívica
class RecargaCivica:
    def __init__(self, monto: float, metodo_de_pago: str):
        self.monto = monto
        self.metodo_de_pago = metodo_de_pago

    def procesar_pago(self) -> bool:
        # Conexión con la pasarela de pagos
        return True


# RF-09 – Aplicar filtro de accesibilidad
class RutaAccesible:
    def __init__(self, nombre: str, accesible: bool):
        self.nombre = nombre
        self.accesible = accesible

    def cumple_filtro_accesibilidad(self) -> bool:
        return self.accesible


# RF-10 – Consultar historial y estadísticas
class HistorialViajes:
    def __init__(self, id_usuario: str, viajes_realizados: list[str]):
        self.id_usuario = id_usuario
        self.viajes_realizados = viajes_realizados

    def obtener_estadisticas(self) -> list[str]:
        return self.viajes_realizados