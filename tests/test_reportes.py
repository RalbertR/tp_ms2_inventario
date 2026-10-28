"""Tests de caracterización del módulo de reportes heredado.

Fijan la salida exacta del módulo tal como llegó del sistema anterior, para que
el refactor no cambie ni un carácter de los reportes.
"""

from inventario.reportes import reporte_mensual, reporte_semanal


def venta(producto, monto, medio, cuotas, provincia, estado="pagada"):
    return {
        "producto": producto,
        "monto": monto,
        "medio": medio,
        "cuotas": cuotas,
        "provincia": provincia,
        "estado": estado,
    }


VENTAS = [
    venta("Monitor 24", 150000, "tarjeta", 6, "Córdoba"),
    venta("Teclado mecánico", 40000, "tarjeta", 1, "CABA"),
    venta("Mouse inalámbrico", 20000, "transferencia", 1, "Mendoza"),
    venta("Cable HDMI", 5000, "efectivo", 1, "CABA"),
    venta("Webcam", 30000, "billetera", 1, "CABA"),
    venta("Parlante", 25000, "tarjeta", 3, "CABA", estado="anulada"),
    venta("Auriculares", 18000, "efectivo", 1, "CABA", estado="pendiente"),
]

DETALLE = [
    "Monitor 24 | 150000 | 12500.0",
    "Teclado mecánico | 40000 | 1600.0",
    "Mouse inalámbrico | 20000 | 200.0",
    "Cable HDMI | 5000 | 0",
    "Webcam | 30000 | 1500.0",
    "Parlante | ANULADA",
    "Total: 245000",
    "Comisiones: 15800.0",
    "Neto: 229200.0",
]


def test_reporte_mensual_aplica_cada_comision_y_el_recargo_del_interior():
    # Arrange
    ventas = VENTAS

    # Act
    reporte = reporte_mensual(ventas, "octubre 2026")

    # Assert
    assert reporte.splitlines() == [
        "Reporte mensual de ventas - octubre 2026",
        *DETALLE,
    ]


def test_reporte_semanal_calcula_igual_que_el_mensual():
    # Arrange
    ventas = VENTAS

    # Act
    reporte = reporte_semanal(ventas, 43)

    # Assert
    assert reporte.splitlines() == [
        "Reporte semanal de ventas - semana 43",
        *DETALLE,
    ]


def test_reporte_sin_ventas_muestra_totales_en_cero():
    # Arrange
    ventas = []

    # Act
    reporte = reporte_mensual(ventas, "noviembre 2026")

    # Assert
    assert reporte.splitlines() == [
        "Reporte mensual de ventas - noviembre 2026",
        "Total: 0",
        "Comisiones: 0",
        "Neto: 0",
    ]
