from app.domain.modelos_poo import (
    AlternativaTransporte,
    HistorialViajes,
    Notificacion,
    RecargaCivica,
    ReporteServicio,
    Ruta,
    RutaAccesible,
    TarjetaCivica,
    Viaje,
    ViajeMultimodal,
)


def test_rf01_consultar_rutas():
    ruta = Ruta("Manrique - Centro", "05:00 - 22:30")
    assert "Manrique - Centro" in ruta.consultar_horario()


def test_rf02_notificacion():
    noti = Notificacion("Retraso en la línea A")
    assert noti.leida is False


def test_rf03_duracion_viaje():
    viaje = Viaje("Poblado", "Niquía", 35)
    assert viaje.calcular_duracion() == 35


def test_rf04_alternativa_cercana():
    alt = AlternativaTransporte("Metro", 1.2)
    assert alt.esta_cerca() is True


def test_rf05_viaje_multimodal():
    viaje_m = ViajeMultimodal(["Metro Linea A", "Metrocable Linea K"])
    assert "Ruta sugerida" in viaje_m.mostrar_secuencia()


def test_rf06_reporte_servicio():
    reporte = ReporteServicio(5, "Excelente servicio")
    assert reporte.guardar_reporte() is True


def test_rf07_tarjeta_civica():
    tarjeta = TarjetaCivica("123456", 15000.0)
    assert tarjeta.consultar_saldo() == 15000.0


def test_rf08_recarga_civica():
    recarga = RecargaCivica(20000.0, "PSE")
    assert recarga.procesar_pago() is True


def test_rf09_ruta_accesible():
    ruta_acc = RutaAccesible("San Javier - Cable", True)
    assert ruta_acc.cumple_filtro_accesibilidad() is True


def test_rf10_historial_viajes():
    historial = HistorialViajes("usr_01", ["Viaje 1", "Viaje 2"])
    assert len(historial.obtener_estadisticas()) == 2
