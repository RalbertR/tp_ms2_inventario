class StockInsuficienteError(Exception):
    def __init__(self, producto_id: str, pedido: int, disponible: int) -> None:
        super().__init__(
            f"Stock insuficiente de {producto_id}: "
            f"se pidieron {pedido} y hay {disponible}"
        )
        self.producto_id = producto_id
        self.pedido = pedido
        self.disponible = disponible


class PagoRechazadoError(Exception):
    pass
