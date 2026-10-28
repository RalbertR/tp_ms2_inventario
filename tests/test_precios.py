from inventario.precios import calcular_total


def test_cupon_y_cliente_frecuente_en_amba():
    # Arrange
    subtotal, cupon, frecuente, provincia = 30000, "BIENVENIDA10", True, "CABA"

    # Act
    total = calcular_total(subtotal, cupon, frecuente, provincia)

    # Assert
    assert total == 29000.0


def test_cupon_y_cliente_frecuente_en_el_interior():
    # Arrange
    subtotal, cupon, frecuente, provincia = 30000, "BIENVENIDA10", True, "Córdoba"

    # Act
    total = calcular_total(subtotal, cupon, frecuente, provincia)

    # Assert
    assert total == 32000.0


def test_compra_grande_sin_descuentos_no_paga_envio():
    # Arrange
    subtotal = 60000

    # Act
    total = calcular_total(subtotal)

    # Assert
    assert total == 60000.0


def test_cupon_con_subtotal_bajo_no_descuenta():
    # Arrange
    subtotal, cupon = 15000, "BIENVENIDA10"

    # Act
    total = calcular_total(subtotal, cupon)

    # Assert
    assert total == 18500.0
