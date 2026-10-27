from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ResultadoPago:
    aprobado: bool
    id_transaccion: str = ""
    motivo: str = ""


class PasarelaDePagos(ABC):
    """Contrato que el sistema espera de la API externa de pagos."""

    @abstractmethod
    def cobrar(self, monto: float, token_tarjeta: str) -> ResultadoPago: ...
