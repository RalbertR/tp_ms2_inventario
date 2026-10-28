TASA_TARJETA_EN_CUOTAS = 0.08
TASA_TARJETA_UN_PAGO = 0.04
TASAS_POR_MEDIO = {"transferencia": 0.01, "efectivo": 0}
TASA_OTROS_MEDIOS = 0.05
RECARGO_INTERIOR = 500
MONTO_MINIMO_RECARGO = 100000


def calcular_comision(venta: dict) -> float:
    """Comisión del medio de pago, con recargo en ventas grandes fuera de CABA."""
    if venta["medio"] == "tarjeta":
        en_cuotas = venta["cuotas"] > 1
        tasa = TASA_TARJETA_EN_CUOTAS if en_cuotas else TASA_TARJETA_UN_PAGO
    else:
        tasa = TASAS_POR_MEDIO.get(venta["medio"], TASA_OTROS_MEDIOS)
    comision = venta["monto"] * tasa
    if venta["provincia"] != "CABA" and venta["monto"] > MONTO_MINIMO_RECARGO:
        comision += RECARGO_INTERIOR
    return comision


def generar_reporte(ventas: list[dict], titulo: str) -> str:
    """Detalle de las ventas pagadas y anuladas, con total, comisiones y neto."""
    total = 0
    comisiones = 0
    lineas = [titulo]
    for venta in ventas:
        if venta["estado"] == "anulada":
            lineas.append(f"{venta['producto']} | ANULADA")
        elif venta["estado"] == "pagada":
            comision = calcular_comision(venta)
            total += venta["monto"]
            comisiones += comision
            lineas.append(
                f"{venta['producto']} | {venta['monto']} | {round(comision, 2)}"
            )
    lineas.append(f"Total: {total}")
    lineas.append(f"Comisiones: {round(comisiones, 2)}")
    lineas.append(f"Neto: {round(total - comisiones, 2)}")
    return "\n".join(lineas)


def reporte_mensual(ventas: list[dict], mes: str) -> str:
    return generar_reporte(ventas, f"Reporte mensual de ventas - {mes}")


def reporte_semanal(ventas: list[dict], semana: int) -> str:
    return generar_reporte(ventas, f"Reporte semanal de ventas - semana {semana}")
