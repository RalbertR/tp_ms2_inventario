from inventario.stock_observer import StockObserver

REORDER_QUANTITY = 100


class EmailAlertObserver(StockObserver):
    def on_low_stock(self, product_id: str, quantity: int) -> None:
        print(f"Email: stock bajo de {product_id}, quedan {quantity} unidades")


class AnalyticsObserver(StockObserver):
    def on_low_stock(self, product_id: str, quantity: int) -> None:
        print(f"Analytics: evento de stock bajo registrado para {product_id}")


class ReplenishObserver(StockObserver):
    def on_low_stock(self, product_id: str, quantity: int) -> None:
        print(f"Reposición: orden de {REORDER_QUANTITY} unidades para {product_id}")
