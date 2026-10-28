from inventario.observers import (
    AnalyticsObserver,
    EmailAlertObserver,
    ReplenishObserver,
)


def test_cada_observador_publica_su_aviso(capsys):
    # Arrange
    observadores = [EmailAlertObserver(), AnalyticsObserver(), ReplenishObserver()]

    # Act
    for observador in observadores:
        observador.on_low_stock("PROD-001", 5)

    # Assert
    assert capsys.readouterr().out.splitlines() == [
        "Email: stock bajo de PROD-001, quedan 5 unidades",
        "Analytics: evento de stock bajo registrado para PROD-001",
        "Reposición: orden de 100 unidades para PROD-001",
    ]
