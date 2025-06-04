from datetime import date
from model.ShipmentInfo import ShipmentInfo
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Cart import Cart
    from services.CartManager import CartManager

class Order:
    def __init__(self, orderId: int, customerId: int, shipmentInfo: ShipmentInfo, cart: "Cart", status: str = "Incomplete", orderDate: date = date.today()):
        self.orderId = orderId
        self.customerId = customerId
        self.orderDate = orderDate
        self.status = status
        self.shipmentInfo = shipmentInfo
        self.total = cart.getTotal()
        self.items = cart.items.copy()
        
    def getOrderSummary(self) -> str:
        summary = (
            f"Order ID: {self.orderId}\n"
            f"Customer ID: {self.customerId}\n"
            f"Date: {self.orderDate.strftime('%Y-%m-%d')}\n"
            f"Status: {self.status}\n"
            f"Total: ${self.total:.2f}\n"
            "Items:\n"
        )
        for item in self.items:
            summary += f"  - {item.product.name} x{item.quantity} = ${item.getTotal()}\n"
        return summary
    