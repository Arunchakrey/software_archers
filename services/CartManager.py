from model.Cart import Cart
from model.CartItem import CartItem
from model.Product import Product
from services.OrderManager import OrderManager
from model.ShipmentInfo import ShipmentInfo
from services.Payment import Payment
import json

class CartManager:
    def __init__(self, cart: Cart):
        self.cart = cart

    def addToCart(self, product: Product, quantity: int):  
        if not product.isInStock(quantity):
            return f"{product.name} is not available"
        
        for item in self.cart.items:
            if item.product.id == product.id:
                item.quantity = quantity
                break
        else:
            cart_item = CartItem(product, quantity)
            self.cart.items.append(cart_item)
        return (f"Added {quantity} x {product.name} to your cart.")

    def removeFromCart(self, productId: int):
        self.cart.items = [item for item in self.cart.items if item.product.id != productId]
    
    def clearCart(self):
        self.cart.items = []
        return self.cart.items
        
    def viewCart(self):
        print("Cart contents:")
        for item in self.cart.items:
            print (f"item:{item.product.name}  x  quantity:{item.quantity}")
        print(f"Total: ${self.getTotal()}")
    
    def getTotal(self):
        return sum(item.getTotal() for item in self.cart.items)

    def checkout(self, customerName, address, filename="data/products.json"):
        if not self.cart.items:
            raise Exception("Cannot place an order: your cart is empty.")
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                
            for cartItem in self.cart.items:
                for prod in data:
                    if prod["id"] == cartItem.product.id:
                        if prod["quantity"] < cartItem.quantity:
                            raise ValueError(f"Not enough stock for {prod['name']}")
                        prod["quantity"] -= cartItem.quantity
                    
            with open(filename, "w") as file:
                json.dump(data, file, indent=2)
                
                from model.Order import Order
                if not self.cart.items:
                    raise Exception("Cart is empty")
                
                Payment.process()
                
                orderId = OrderManager.getNextOrderId("data/orders.txt")
                shipmentInfo = ShipmentInfo(customerName, address)
                order = Order(orderId, customerName, shipmentInfo, self.cart)
                OrderManager.saveToFile(order, "data/orders.txt")
                
                self.clearCart()
                
                print(f"Order {orderId} placed successfully.")
                return order

        except Exception as e:
            print(f"Checkout failed: {e}")
