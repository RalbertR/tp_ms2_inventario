import logging

from inventario.stock_observer import StockObserver

LOW_STOCK_THRESHOLD = 10

logger = logging.getLogger(__name__)


class InventoryManager:
    def __init__(self) -> None:
        self.stock: dict[str, int] = {}
        self._observers: list[StockObserver] = []

    def subscribe(self, observer: StockObserver) -> None:
        self._observers.append(observer)

    def unsubscribe(self, observer: StockObserver) -> None:
        self._observers.remove(observer)

    def update_stock(self, product_id: str, quantity: int) -> None:
        self.stock[product_id] = quantity
        self._check_low_stock(product_id)

    def sell_product(self, product_id: str, sold: int) -> None:
        self.stock[product_id] -= sold
        self._check_low_stock(product_id)

    def _check_low_stock(self, product_id: str) -> None:
        quantity = self.stock[product_id]
        if quantity < LOW_STOCK_THRESHOLD:
            self._notify(product_id, quantity)

    def _notify(self, product_id: str, quantity: int) -> None:
        for observer in self._observers:
            try:
                observer.on_low_stock(product_id, quantity)
            except Exception as error:
                logger.error(
                    "%s falló al avisar stock bajo de %s: %s",
                    type(observer).__name__,
                    product_id,
                    error,
                )
