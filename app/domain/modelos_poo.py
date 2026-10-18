# app/domain/modelos_poo.py
"""
==============================================================================
TuRutaMed - Módulo de Dominio Orientado a Objetos (POO)
==============================================================================
Proyecto Pedagógico Integrador (PPI) - Ingeniería en Software
Tecnológico de Antioquia (TdeA)

Codificación unificada del Diagrama de Clases UML (Sección 7.2).
Representación de la lógica de negocio para los Requisitos Funcionales RF-01 a RF-10.
==============================================================================
"""



# ============================================================================
# RF-01: Consultar rutas y horarios
# ============================================================================
class Ruta:
    """Clase base que representa una ruta del sistema de transporte público."""

    def __init__(self, nombre: str, horario: str):
        self.nombre: str = nombre
        self.horario: str = horario

    def consultar_horario(self) -> str:
        """Devuelve la información formateada de la ruta y su horario operativo."""
        return f"Ruta: {self.nombre} - Horario: {self.horario}"


# ============================================================================
# RF-09: Filtrar por accesibilidad
# (Relación UML: Herencia de la clase Ruta)
# ============================================================================
class RutaAccesible(Ruta):
    """Especialización de Ruta que añade criterios de accesibilidad física/sensorial."""

    def __init__(self, nombre: str, horario: str = "05:00 - 23:00", accesible: bool = True):
        super().__init__(nombre, horario)
        self.accesible: bool = accesible

    def cumple_filtro_accesibilidad(self) -> bool:
        """Verifica si la ruta dispone de infraestructura accesible (rampas, piso bajo)."""
        return self.accesible


# ============================================================================
# RF-02: Notificar cambios del servicio
# ============================================================================
class Notificacion:
    """Modela las alertas de servicio emitidas ante retrasos o cierres viales."""

    def __init__(self, mensaje_alerta: str):
        self.mensaje_alerta: str = mensaje_alerta
        self.leida: bool = False

    def enviar_alerta(self) -> None:
        """Despacha la notificación push o de sistema al usuario."""
        print(f"Nueva alerta de servicio: {self.mensaje_alerta}")


# ============================================================================
# RF-03: Calcular duración del trayecto
# ============================================================================
class Viaje:
    """Representa un desplazamiento individual entre un punto de origen y un destino."""

    def __init__(self, origen: str, destino: str, duracion_minutos: int):
        self.origen: str = origen
        self.destino: str = destino
        self.duracion_minutos: int = duracion_minutos

    def calcular_duracion(self) -> int:
        """Retorna la estimación del tiempo total de viaje en minutos."""
        return self.duracion_minutos


# ============================================================================
# RF-04: Consultar alternativas cercanas
# ============================================================================
class AlternativaTransporte:
    """Modela medios de transporte o paraderos cercanos según la geolocalización."""

    def __init__(self, medio: str, distancia_km: float):
        self.medio: str = medio
        self.distancia_km: float = distancia_km

    def esta_cerca(self) -> bool:
        """Determina si la alternativa se encuentra dentro del radio de cercanía (<= 2 km)."""
        return self.distancia_km <= 2.0


# ============================================================================
# RF-05: Planificar viaje multimodal
# ============================================================================
class ViajeMultimodal:
    """Compone y gestiona secuencias de rutas combinadas (Metro, Bus, Metrocable)."""

    def __init__(self, secuencia_rutas: list[str]):
        self.secuencia_rutas: list[str] = secuencia_rutas

    def mostrar_secuencia(self) -> str:
        """Genera el itinerario paso a paso de las conexiones sugeridas."""
        return f"Ruta sugerida: {' -> '.join(self.secuencia_rutas)}"


# ============================================================================
# RF-06: Calificar y reportar el servicio
# ============================================================================
class ReporteServicio:
    """Gestiona las calificaciones por estrellas y los reportes de retroalimentación ciudadana."""

    def __init__(self, calificacion: int, comentario_ciudadano: str):
        self.calificacion: int = calificacion
        self.comentario_ciudadano: str = comentario_ciudadano

    def guardar_reporte(self) -> bool:
        """Almacena el reporte del usuario en la base de datos de calidad del servicio."""
        return True


# ============================================================================
# RF-07: Consultar saldo de la tarjeta Cívica
# ============================================================================
class TarjetaCivica:
    """Modela la tarjeta de transporte Cívica y la consulta de su saldo en tiempo real."""

    def __init__(self, numero: str, saldo: float):
        self.numero: str = numero
        self.saldo: float = saldo

    def consultar_saldo(self) -> float:
        """Devuelve el saldo disponible en la cuenta o tarjeta del pasajero."""
        return self.saldo


# ============================================================================
# RF-08: Recargar tarjeta Cívica
# ============================================================================
class RecargaCivica:
    """Procesa las transacciones de recarga de saldo mediante pasarelas de pago."""

    def __init__(self, monto: float, metodo_de_pago: str):
        self.monto: float = monto
        self.metodo_de_pago: str = metodo_de_pago

    def procesar_pago(self) -> bool:
        """Valida y ejecuta la transacción con la pasarela financiera externa."""
        return True


# ============================================================================
# RF-10: Consultar historial y estadísticas
# ============================================================================
class HistorialViajes:
    """Consolida el registro histórico y las métricas estadísticas del pasajero."""

    def __init__(self, id_usuario: str, viajes_realizados: list[str]):
        self.id_usuario: str = id_usuario
        self.viajes_realizados: list[str] = viajes_realizados

    def obtener_estadisticas(self) -> list[str]:
        """Recupera la lista histórica de desplazamientos realizados por el usuario."""
        return self.viajes_realizados
