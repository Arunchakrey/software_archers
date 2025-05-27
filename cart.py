from cartItem import CartItem
from typing import List

class Cart:
    def __init__(self):
        self.items: List[CartItem] = []
    
    def getTotal(self):
        return sum(item.getTotal() for item in self.items)
    
    def addItem(self, product, quantity):
        cart_item = CartItem(product, quantity)
        if not product.isInStock(quantity):
            return f"{product.name} is not available"
        
        for item in self.items:
            if item.product.name == product.name:
                item.quantity = quantity
                break
        else:
            self.items.append(cart_item)
        
    def removeItem(self, productId):
        self.items = [item for item in self.items if item.product.id != productId]
        
    def displayCart(self):
        print("Cart contents:")
        for item in self.items:
            print (f"item:{item.product.name}  x  quantity:{item.quantity}")
        print(f"Total: ${self.getTotal()}")
         