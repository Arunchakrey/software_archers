from datetime import date
from model.ShipmentInfo import ShipmentInfo
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Cart import Cart

class Order:
    def __init__(self, orderId: int, customerId: int, shipmentInfo: ShipmentInfo, cart: "Cart", status: str = "Incomplete", orderDate: date = date.today()):
        self._orderId = orderId
        self._customerId = customerId
        self._orderDate = orderDate
        self._status = status
        self._shipmentInfo = shipmentInfo
        self._total = cart.getTotal()
        self._items = cart._items.copy()

    def getOrderSummary(self) -> str:
        summary = (
            f"Order ID: {self._orderId}\n"
            f"Customer ID: {self._customerId}\n"
            f"Date: {self._orderDate.strftime('%Y-%m-%d')}\n"
            f"Status: {self._status}\n"
            f"Total: ${self._total:.2f}\n"
            "Items:\n"
        )
        for item in self._items:
            summary += f"  - {item._product._name} x{item._quantity} = ${item.getTotal():.2f}\n"
        return summary
