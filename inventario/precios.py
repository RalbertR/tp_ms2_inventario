CUPON_BIENVENIDA = "BIENVENIDA10"
MINIMO_PARA_CUPON = 20000
MINIMO_ENVIO_GRATIS = 50000
ENVIO_AMBA = 3500
ENVIO_INTERIOR = 6500
ZONA_AMBA = {"CABA", "Buenos Aires"}


def calcular_total(
    subtotal: float,
    cupon: str | None = None,
    cliente_frecuente: bool = False,
    provincia: str = "CABA",
) -> float:
    """Aplica los descuentos y el costo de envío al subtotal de una compra.

    El cupón de bienvenida descuenta 10% si el subtotal llega al mínimo, y el
    cliente frecuente suma 5% más. Si el total con descuentos no llega al
    mínimo de envío gratis, se cobra el envío según la zona.
    """
    descuento = 0.0
    if cupon == CUPON_BIENVENIDA and subtotal >= MINIMO_PARA_CUPON:
        descuento = subtotal * 0.10
    if cliente_frecuente:
        descuento += subtotal * 0.05
    total = subtotal - descuento
    if total < MINIMO_ENVIO_GRATIS:
        if provincia in ZONA_AMBA:
            total += ENVIO_AMBA
        else:
            total += ENVIO_INTERIOR
    return round(total, 2)
