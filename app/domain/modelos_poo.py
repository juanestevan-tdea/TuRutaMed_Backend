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
        # Uso de guion bajo para indicar atributos privados (Encapsulamiento)
        self._nombre: str = nombre
        self._horario: str = horario

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def horario(self) -> str:
        return self._horario

    def consultar_horario(self) -> str:
        """Devuelve la información formateada de la ruta y su horario operativo."""
        return f"Ruta: {self._nombre} - Horario: {self._horario}"


# ============================================================================
# RF-09: Filtrar por accesibilidad
# (Relación UML: Herencia de la clase Ruta)
# ============================================================================
class RutaAccesible(Ruta):
    """Especialización de Ruta que añade criterios de accesibilidad física/sensorial."""

    def __init__(self, nombre: str, horario: str = "05:00 - 23:00", accesible: bool = True):
        super().__init__(nombre, horario)
        self._accesible: bool = accesible

    @property
    def accesible(self) -> bool:
        return self._accesible

    def cumple_filtro_accesibilidad(self) -> bool:
        """Verifica si la ruta dispone de infraestructura accesible (rampas, piso bajo)."""
        return self._accesible


# ============================================================================
# RF-02: Notificar cambios del servicio
# ============================================================================
class Notificacion:
    """Modela las alertas de servicio emitidas ante retrasos o cierres viales."""

    def __init__(self, mensaje_alerta: str):
        self._mensaje_alerta: str = mensaje_alerta
        self._leida: bool = False

    @property
    def mensaje_alerta(self) -> str:
        """Mensaje de la alerta de servicio."""
        return self._mensaje_alerta

    @property
    def leida(self) -> bool:
        """Indica si la alerta ya fue leída por el usuario."""
        return self._leida

    def enviar_alerta(self) -> dict:
        """Despacha la notificación push o de sistema al usuario."""
        # Corrección: Se reemplaza print() por retorno de estructura de datos para FastAPI
        self._leida = True
        return {
            "status": "success",
            "tipo": "alerta_servicio",
            "mensaje": self._mensaje_alerta,
            "leida": self._leida,
        }


# ============================================================================
# RF-03: Calcular duración del trayecto
# ============================================================================
class Viaje:
    """Representa un desplazamiento individual entre un punto de origen y un destino."""

    def __init__(self, origen: str, destino: str, duracion_minutos: int):
        self._origen: str = origen
        self._destino: str = destino
        self._duracion_minutos: int = duracion_minutos

    @property
    def origen(self) -> str:
        """Punto de origen del desplazamiento."""
        return self._origen

    @property
    def destino(self) -> str:
        """Punto de destino del desplazamiento."""
        return self._destino

    @property
    def duracion_minutos(self) -> int:
        """Duración estimada del desplazamiento en minutos."""
        return self._duracion_minutos

    def calcular_duracion(self) -> int:
        """Retorna la estimación del tiempo total de viaje en minutos."""
        return self._duracion_minutos


# ============================================================================
# RF-04: Consultar alternativas cercanas
# ============================================================================
class AlternativaTransporte:
    """Modela medios de transporte o paraderos cercanos según la geolocalización."""

    def __init__(self, medio: str, distancia_km: float):
        self._medio: str = medio
        self._distancia_km: float = distancia_km

    @property
    def medio(self) -> str:
        """Medio de transporte de la alternativa."""
        return self._medio

    @property
    def distancia_km(self) -> float:
        """Distancia en kilómetros hasta la alternativa."""
        return self._distancia_km

    def esta_cerca(self) -> bool:
        """Determina si la alternativa se encuentra dentro del radio de cercanía (<= 2 km)."""
        return self._distancia_km <= 2.0


# ============================================================================
# RF-05: Planificar viaje multimodal
# ============================================================================
class ViajeMultimodal:
    """Compone y gestiona secuencias de rutas combinadas (Metro, Bus, Metrocable)."""

    def __init__(self, secuencia_rutas: list[str]):
        self._secuencia_rutas: list[str] = secuencia_rutas

    @property
    def secuencia_rutas(self) -> list[str]:
        """Rutas que componen el itinerario multimodal, en orden."""
        return self._secuencia_rutas

    def mostrar_secuencia(self) -> str:
        """Genera el itinerario paso a paso de las conexiones sugeridas."""
        return f"Ruta sugerida: {' -> '.join(self._secuencia_rutas)}"


# ============================================================================
# RF-06: Calificar y reportar el servicio
# ============================================================================
class ReporteServicio:
    """Gestiona las calificaciones por estrellas y los reportes de retroalimentación ciudadana."""

    def __init__(self, calificacion: int, comentario_ciudadano: str):
        self._calificacion: int = calificacion
        self._comentario_ciudadano: str = comentario_ciudadano

    @property
    def calificacion(self) -> int:
        """Calificación del servicio, de 1 a 5."""
        return self._calificacion

    @property
    def comentario_ciudadano(self) -> str:
        """Comentario dejado por el ciudadano."""
        return self._comentario_ciudadano

    def guardar_reporte(self) -> bool:
        """Almacena el reporte del usuario en la base de datos de calidad del servicio."""
        # Corrección: Se añade validación de dominio en lugar de return True quemado
        if self._calificacion < 1 or self._calificacion > 5:
            return False  # Calificación inválida
        if not self._comentario_ciudadano.strip():
            return False  # Comentario vacío

        # Aquí iría la lógica de conexión a la base de datos
        return True


# ============================================================================
# RF-07: Consultar saldo de la tarjeta Cívica
# ============================================================================
class TarjetaCivica:
    """Modela la tarjeta de transporte Cívica y la consulta de su saldo en tiempo real."""

    def __init__(self, numero: str, saldo: float):
        self._numero: str = numero
        self._saldo: float = saldo

    @property
    def numero(self) -> str:
        """Número identificador de la tarjeta Cívica."""
        return self._numero

    @property
    def saldo(self) -> float:
        """Saldo disponible en la tarjeta."""
        return self._saldo

    @saldo.setter
    def saldo(self, nuevo_saldo: float) -> None:
        self._saldo = nuevo_saldo

    def consultar_saldo(self) -> float:
        """Devuelve el saldo disponible en la cuenta o tarjeta del pasajero."""
        return self._saldo


# ============================================================================
# RF-08: Recargar tarjeta Cívica
# ============================================================================
class RecargaCivica:
    """Procesa las transacciones de recarga de saldo mediante pasarelas de pago."""

    def __init__(self, monto: float, metodo_de_pago: str):
        self._monto: float = monto
        self._metodo_de_pago: str = metodo_de_pago

    @property
    def monto(self) -> float:
        """Monto de la recarga."""
        return self._monto

    @property
    def metodo_de_pago(self) -> str:
        """Método de pago utilizado (PSE, tarjeta, Nequi, etc.)."""
        return self._metodo_de_pago

    def procesar_pago(self) -> bool:
        """Valida y ejecuta la transacción con la pasarela financiera externa."""
        # Corrección: Se añade validación de monto negativo o cero
        if self._monto <= 0:
            return False  # Transacción rechazada por monto inválido

        # Aquí iría la conexión con la pasarela de pagos (PSE/Tarjeta)
        return True


# ============================================================================
# RF-10: Consultar historial y estadísticas
# ============================================================================
class HistorialViajes:
    """Consolida el registro histórico y las métricas estadísticas del pasajero."""

    def __init__(self, id_usuario: str, viajes_realizados: list[str]):
        self._id_usuario: str = id_usuario
        self._viajes_realizados: list[str] = viajes_realizados

    @property
    def id_usuario(self) -> str:
        """Identificador del usuario dueño del historial."""
        return self._id_usuario

    @property
    def viajes_realizados(self) -> list[str]:
        """Lista de viajes realizados por el usuario."""
        return self._viajes_realizados

    def obtener_estadisticas(self) -> list[str]:
        """Recupera la lista histórica de desplazamientos realizados por el usuario."""
        return self._viajes_realizados
