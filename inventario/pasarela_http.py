import requests

from inventario.pagos import PasarelaDePagos, ResultadoPago


class PasarelaHttp(PasarelaDePagos):
    """Cliente HTTP de la API de pagos. El contrato está en docs/contrato_pagos.md."""

    def __init__(self, url_base: str, api_key: str, timeout: float = 10) -> None:
        self._url_base = url_base
        self._api_key = api_key
        self._timeout = timeout

    def cobrar(self, monto: float, token_tarjeta: str) -> ResultadoPago:
        respuesta = requests.post(
            f"{self._url_base}/v1/cobros",
            json={"monto": monto, "token": token_tarjeta},
            headers={"Authorization": f"Bearer {self._api_key}"},
            timeout=self._timeout,
        )
        datos = respuesta.json()
        return ResultadoPago(
            aprobado=datos["estado"] == "aprobado",
            id_transaccion=datos.get("id", ""),
            motivo=datos.get("motivo", ""),
        )
