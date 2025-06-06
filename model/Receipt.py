from model.Order import Order
from typing import List

class Receipt:
    def __init__(self, order: Order):
        self._orderId: int = order._orderId
        self._name: str = order._shipmentInfo._customerName
        self._address: str = order._shipmentInfo._deliveryAddress
        self._total: float = order._total
        self._orderSummary: List = order._items

    def printReceipt(self):
        receipt = (
            "RECEIPT:\n"
            f"Order ID: {self._orderId}\n"
            f"Customer Name: {self._name}\n"
            f"Address: {self._address}\n"
            f"Total: ${self._total:.2f}\n"
            f"Items:\n"
        )
        for item in self._orderSummary:
            receipt += f"  - {item._product._name} x{item._quantity} = ${item.getTotal():.2f}\n"

        filepath = "data/receipt.txt"
        with open(filepath, "w") as f:
            f.write(receipt)

        return receipt
