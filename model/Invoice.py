from model.Cart import Cart
from typing import List

class Invoice:
    def __init__(self, cart: Cart):
        self._total: float = cart.getTotal()
        self._items: List = cart.items

    def printInvoice(self):
        invoice = (
            "Invoice:\n"
            f"Amount Due: ${self.total:.2f}\n"
            f"Items: \n"
        )

        for item in self.items:
            invoice += f"  - {item.product.name} x{item.quantity} = ${item.getTotal():.2f}\n"

        filepath = "data/invoice.txt"

        with open(filepath, "w") as f:
            f.write(invoice)
 