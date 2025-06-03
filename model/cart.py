from model.CartItem import CartItem
from services.orderManager import OrderManager
from model.ShipmentInfo import ShipmentInfo
from typing import List

class Cart:
    def __init__(self):
        self.items: List[CartItem] = []
    
    def getTotal(self):
        return sum(item.getTotal() for item in self.items)
    
    def addItem(self, product, quantity):
        cart_item = CartItem(product, quantity) #change case to pascal
        if not product.isInStock(quantity):
            return f"{product.name} is not available"
        
        for item in self.items:
            if item.product.id == product.id:
                item.quantity = quantity
                break
        else:
            self.items.append(cart_item)
        
    def removeItem(self, productId):
        self.items = [item for item in self.items if item.product.id != productId]
        
    def clearCart(self):
        self.items = []
        return self.items
        
    def displayCart(self):
        print("Cart contents:")
        for item in self.items:
            print (f"item:{item.product.name}  x  quantity:{item.quantity}")
        print(f"Total: ${self.getTotal()}")
    
    def checkOut(self, customerId: int):
        from model.Order import Order
        if not self.items:
            raise Exception("Cart is empty")
    
        #Deduct stock 
        for item in self.items:
            item.product.quantity -= item.quantity
        
        orderId = OrderManager.getNextOrderId("data/orders.txt")
        shipmentInfo = ShipmentInfo("jack", "12 Hawthorn")
        order = Order(orderId, customerId, shipmentInfo, self)
         
        OrderManager.saveToFile(order, "data/orders.txt")
         
        self.clearCart()
        
        print(f"Order {orderId} placed successfully.")
        return order