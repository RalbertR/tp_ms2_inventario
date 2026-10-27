from dataclasses import dataclass

from inventario.errores import PagoRechazadoError, StockInsuficienteError
from inventario.inventory_manager import InventoryManager
from inventario.pagos import PasarelaDePagos
from inventario.precios import calcular_total


@dataclass
class Comprobante:
    producto_id: str
    cantidad: int
    total: float
    id_transaccion: str


class Checkout:
    def __init__(self, inventario: InventoryManager, pasarela: PasarelaDePagos) -> None:
        self._inventario = inventario
        self._pasarela = pasarela

    def confirmar_compra(
        self,
        producto_id: str,
        cantidad: int,
        precio_unitario: float,
        token_tarjeta: str,
        cupon: str | None = None,
        cliente_frecuente: bool = False,
        provincia: str = "CABA",
    ) -> Comprobante:
        disponible = self._inventario.stock.get(producto_id, 0)
        if cantidad > disponible:
            raise StockInsuficienteError(producto_id, cantidad, disponible)
        total = calcular_total(
            cantidad * precio_unitario, cupon, cliente_frecuente, provincia
        )
        resultado = self._pasarela.cobrar(total, token_tarjeta)
        if not resultado.aprobado:
            raise PagoRechazadoError(resultado.motivo)
        self._inventario.sell_product(producto_id, cantidad)
        return Comprobante(producto_id, cantidad, total, resultado.id_transaccion)
