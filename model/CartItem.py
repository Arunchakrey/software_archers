from model.Product import Product

class CartItem:
    def __init__(self, product: Product, quantity: int):
        self._product = product
        self._quantity = quantity

    def setQuantity(self, value):
        self._quantity = value

    def getTotal(self):
        return self._product._price * self._quantity
