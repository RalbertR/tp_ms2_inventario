from abc import ABC, abstractmethod


class StockObserver(ABC):
    @abstractmethod
    def on_low_stock(self, product_id: str, quantity: int) -> None: ...
