def reporte_mensual(ventas, mes):
    total = 0
    comisiones = 0
    lineas = ["Reporte mensual de ventas - " + mes]
    for v in ventas:
        if v["estado"] == "pagada":
            if v["medio"] == "tarjeta":
                if v["cuotas"] > 1:
                    comision = v["monto"] * 0.08
                else:
                    comision = v["monto"] * 0.04
            elif v["medio"] == "transferencia":
                comision = v["monto"] * 0.01
            elif v["medio"] == "efectivo":
                comision = 0
            else:
                comision = v["monto"] * 0.05
            if v["provincia"] != "CABA" and v["monto"] > 100000:
                comision = comision + 500
            total = total + v["monto"]
            comisiones = comisiones + comision
            lineas.append(
                v["producto"]
                + " | "
                + str(v["monto"])
                + " | "
                + str(round(comision, 2))
            )
        elif v["estado"] == "anulada":
            lineas.append(v["producto"] + " | ANULADA")
    lineas.append("Total: " + str(total))
    lineas.append("Comisiones: " + str(round(comisiones, 2)))
    lineas.append("Neto: " + str(round(total - comisiones, 2)))
    return "\n".join(lineas)


def reporte_semanal(ventas, semana):
    total = 0
    comisiones = 0
    lineas = ["Reporte semanal de ventas - semana " + str(semana)]
    for v in ventas:
        if v["estado"] == "pagada":
            if v["medio"] == "tarjeta":
                if v["cuotas"] > 1:
                    comision = v["monto"] * 0.08
                else:
                    comision = v["monto"] * 0.04
            elif v["medio"] == "transferencia":
                comision = v["monto"] * 0.01
            elif v["medio"] == "efectivo":
                comision = 0
            else:
                comision = v["monto"] * 0.05
            if v["provincia"] != "CABA" and v["monto"] > 100000:
                comision = comision + 500
            total = total + v["monto"]
            comisiones = comisiones + comision
            lineas.append(
                v["producto"]
                + " | "
                + str(v["monto"])
                + " | "
                + str(round(comision, 2))
            )
        elif v["estado"] == "anulada":
            lineas.append(v["producto"] + " | ANULADA")
    lineas.append("Total: " + str(total))
    lineas.append("Comisiones: " + str(round(comisiones, 2)))
    lineas.append("Neto: " + str(round(total - comisiones, 2)))
    return "\n".join(lineas)
