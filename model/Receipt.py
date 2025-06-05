from model.Order import Order
from typing import List

class Receipt:
    def __init__(self, order: Order):
        self._orderId: int = order.orderId
        self._name: str = order.shipmentInfo.customerName
        self._address: str = order.shipmentInfo.deliveryAddress
        self._total: float = order.total
        self._orderSummary: List = order.items

    def printReceipt(self):
        receipt = (
            "RECEIPT:\n"
            f"Order ID: {self.orderId}"
            f"Customer Name: {self.name}\n"
            f"Address: {self.address}\n"
            f"Total: {self.total:.2f}\n"
            f"Items: \n"
        )

        for item in self.orderSummary:
            receipt += f"  - {item.product.name} x{item.quantity} = ${item.getTotal():.2f}\n"

        filepath = "data/receipt.txt"

        with open(filepath, "w") as f:
            f.write(receipt)

        return receipt
    