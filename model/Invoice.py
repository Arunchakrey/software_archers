from model.Cart import Cart
from typing import List

class Invoice:
    def __init__(self, cart: Cart):
        self._total: float = cart.getTotal()
        self._items: List = cart._items

    def printInvoice(self):
        invoice = (
            "Invoice:\n"
            f"Amount Due: ${self._total:.2f}\n"
            "Items:\n"
        )
        for item in self._items:
            invoice += f"  - {item._product._name} x{item._quantity} = ${item.getTotal():.2f}\n"

        with open("data/invoice.txt", "w") as f:
            f.write(invoice)
