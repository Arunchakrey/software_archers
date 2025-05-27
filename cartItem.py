from product import Product

class CartItem:
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity
#property
    def setQuantity(self, value):
        self.quantity = value
        
    def getTotal(self):
        return self.product.price * self.quantity