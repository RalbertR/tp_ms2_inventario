import pytest

from inventario.errores import ProductoInexistenteError, StockInsuficienteError
from inventario.inventory_manager import InventoryManager
from inventario.stock_observer import StockObserver


class ObservadorEspia(StockObserver):
    """Guarda cada aviso que recibe para poder revisarlos en el Assert."""

    def __init__(self) -> None:
        self.avisos: list[tuple[str, int]] = []

    def on_low_stock(self, product_id: str, quantity: int) -> None:
        self.avisos.append((product_id, quantity))


def test_venta_descuenta_las_unidades_vendidas():
    # Arrange
    manager = InventoryManager()
    manager.update_stock("PROD-001", 50)

    # Act
    manager.sell_product("PROD-001", 15)

    # Assert
    assert manager.stock["PROD-001"] == 35


def test_venta_que_deja_stock_bajo_avisa_a_cada_observador():
    # Arrange
    manager = InventoryManager()
    manager.update_stock("PROD-001", 50)
    email, reposicion = ObservadorEspia(), ObservadorEspia()
    manager.subscribe(email)
    manager.subscribe(reposicion)

    # Act
    manager.sell_product("PROD-001", 45)

    # Assert
    assert email.avisos == [("PROD-001", 5)]
    assert reposicion.avisos == [("PROD-001", 5)]


def test_venta_que_no_baja_del_umbral_no_avisa():
    # Arrange
    manager = InventoryManager()
    manager.update_stock("PROD-001", 50)
    espia = ObservadorEspia()
    manager.subscribe(espia)

    # Act
    manager.sell_product("PROD-001", 40)

    # Assert
    assert espia.avisos == []


def test_vender_todo_el_stock_lo_deja_en_cero():
    # Arrange
    manager = InventoryManager()
    manager.update_stock("PROD-001", 50)
    espia = ObservadorEspia()
    manager.subscribe(espia)

    # Act
    manager.sell_product("PROD-001", 50)

    # Assert
    assert manager.stock["PROD-001"] == 0
    assert espia.avisos == [("PROD-001", 0)]


def test_venta_mayor_al_stock_se_rechaza_sin_tocar_el_stock():
    # Arrange
    manager = InventoryManager()
    manager.update_stock("PROD-001", 3)
    espia = ObservadorEspia()
    manager.subscribe(espia)

    # Act
    with pytest.raises(StockInsuficienteError) as error:
        manager.sell_product("PROD-001", 5)

    # Assert
    assert str(error.value) == ("Stock insuficiente de PROD-001: se pidieron 5 y hay 3")
    assert manager.stock["PROD-001"] == 3
    assert espia.avisos == []


@pytest.mark.parametrize("cantidad", [0, -5])
def test_cantidad_cero_o_negativa_se_rechaza(cantidad):
    # Arrange
    manager = InventoryManager()
    manager.update_stock("PROD-001", 50)

    # Act
    with pytest.raises(ValueError, match="tiene que ser positiva"):
        manager.sell_product("PROD-001", cantidad)

    # Assert
    assert manager.stock["PROD-001"] == 50


def test_vender_un_producto_inexistente_da_un_error_claro():
    # Arrange
    manager = InventoryManager()

    # Act
    with pytest.raises(ProductoInexistenteError) as error:
        manager.sell_product("PROD-999", 1)

    # Assert
    assert str(error.value) == "No existe el producto PROD-999 en el inventario"
    assert manager.stock == {}


class ObservadorRoto(StockObserver):
    def on_low_stock(self, product_id: str, quantity: int) -> None:
        raise ConnectionError("error de red simulado")


def test_un_observador_que_falla_no_corta_el_aviso_a_los_demas(caplog):
    # Arrange
    manager = InventoryManager()
    manager.update_stock("PROD-001", 50)
    antes, despues = ObservadorEspia(), ObservadorEspia()
    manager.subscribe(antes)
    manager.subscribe(ObservadorRoto())
    manager.subscribe(despues)

    # Act
    manager.sell_product("PROD-001", 45)

    # Assert
    assert antes.avisos == [("PROD-001", 5)]
    assert despues.avisos == [("PROD-001", 5)]
    assert "ObservadorRoto falló al avisar stock bajo de PROD-001" in caplog.text
    assert caplog.records[0].exc_info is not None


def test_un_observador_desuscripto_deja_de_recibir_avisos():
    # Arrange
    manager = InventoryManager()
    manager.update_stock("PROD-001", 50)
    espia = ObservadorEspia()
    manager.subscribe(espia)
    manager.unsubscribe(espia)

    # Act
    manager.sell_product("PROD-001", 45)

    # Assert
    assert espia.avisos == []
