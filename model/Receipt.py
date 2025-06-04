from model.Order import Order
from typing import List

class Receipt:
    def __init__(self, order: Order):
        self.orderId: int = order.orderId
        self.name: str = order.shipmentInfo.customerName
        self.address: str = order.shipmentInfo.deliveryAddress
        self.total: float = order.total
        self.orderSummary: List = order.items

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
    