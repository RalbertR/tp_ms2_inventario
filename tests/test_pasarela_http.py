from unittest.mock import Mock

from inventario import pasarela_http
from inventario.pasarela_http import PasarelaHttp


def test_arma_el_pedido_del_contrato_y_traduce_la_respuesta(monkeypatch):
    # Arrange
    respuesta = Mock()
    respuesta.json.return_value = {"estado": "aprobado", "id": "TX-77"}
    post = Mock(return_value=respuesta)
    monkeypatch.setattr(pasarela_http.requests, "post", post)
    pasarela = PasarelaHttp("https://pagos.example.com", "clave-test")

    # Act
    resultado = pasarela.cobrar(30500.0, "tok_visa")

    # Assert
    assert resultado.aprobado is True
    assert resultado.id_transaccion == "TX-77"
    post.assert_called_once_with(
        "https://pagos.example.com/v1/cobros",
        json={"monto": 30500.0, "token": "tok_visa"},
        headers={"Authorization": "Bearer clave-test"},
        timeout=10,
    )
