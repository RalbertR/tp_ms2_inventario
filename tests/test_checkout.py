from unittest.mock import Mock

import pytest

from inventario.checkout import Checkout
from inventario.errores import PagoRechazadoError, StockInsuficienteError
from inventario.inventory_manager import InventoryManager
from inventario.pagos import PasarelaDePagos, ResultadoPago


class PasarelaStub(PasarelaDePagos):
    """Devuelve siempre la respuesta enlatada que se le pasa, sin red ni lógica."""

    def __init__(self, respuesta: ResultadoPago) -> None:
        self._respuesta = respuesta

    def cobrar(self, monto: float, token_tarjeta: str) -> ResultadoPago:
        return self._respuesta


def inventario_con(producto_id: str, cantidad: int) -> InventoryManager:
    inventario = InventoryManager()
    inventario.update_stock(producto_id, cantidad)
    return inventario


# Stubs: fijan lo que contesta la API para ver cómo reacciona el checkout.


def test_pago_aprobado_descuenta_el_stock_y_devuelve_el_comprobante():
    # Arrange
    inventario = inventario_con("PROD-001", 50)
    pasarela = PasarelaStub(ResultadoPago(aprobado=True, id_transaccion="TX-123"))
    checkout = Checkout(inventario, pasarela)

    # Act
    comprobante = checkout.confirmar_compra("PROD-001", 2, 30000, "tok_visa")

    # Assert
    assert inventario.stock["PROD-001"] == 48
    assert comprobante.total == 60000
    assert comprobante.id_transaccion == "TX-123"


def test_pago_rechazado_no_descuenta_el_stock():
    # Arrange
    inventario = inventario_con("PROD-001", 50)
    rechazo = ResultadoPago(aprobado=False, motivo="fondos insuficientes")
    checkout = Checkout(inventario, PasarelaStub(rechazo))

    # Act
    with pytest.raises(PagoRechazadoError, match="fondos insuficientes"):
        checkout.confirmar_compra("PROD-001", 2, 30000, "tok_visa")

    # Assert
    assert inventario.stock["PROD-001"] == 50


# Mocks: registran cómo el checkout usa la API para auditar el protocolo.


def test_cobra_una_sola_vez_y_con_el_total_ya_calculado():
    # Arrange
    inventario = inventario_con("PROD-001", 50)
    pasarela = Mock(spec=PasarelaDePagos)
    pasarela.cobrar.return_value = ResultadoPago(aprobado=True, id_transaccion="TX-9")
    checkout = Checkout(inventario, pasarela)

    # Act
    checkout.confirmar_compra("PROD-001", 1, 30000, "tok_visa", cupon="BIENVENIDA10")

    # Assert
    pasarela.cobrar.assert_called_once_with(30500.0, "tok_visa")


def test_sin_stock_suficiente_no_llega_a_cobrar():
    # Arrange
    inventario = inventario_con("PROD-001", 1)
    pasarela = Mock(spec=PasarelaDePagos)
    checkout = Checkout(inventario, pasarela)

    # Act
    with pytest.raises(StockInsuficienteError):
        checkout.confirmar_compra("PROD-001", 3, 30000, "tok_visa")

    # Assert
    pasarela.cobrar.assert_not_called()
