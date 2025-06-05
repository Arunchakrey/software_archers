from model.Cart import Cart
from model.CartItem import CartItem
from model.Product import Product
from model.Receipt import Receipt
from model.Invoice import Invoice
from manager.OrderManager import OrderManager
from model.ShipmentInfo import ShipmentInfo
from services.Payment import Payment
import json

class CartManager:
    def __init__(self, cart: Cart):
        self._cart = cart

    def addToCart(self, product: Product, quantity: int):  
        if not product.isInStock(quantity):
            return f"{product._name} is not available"
        
        for item in self._cart._items:
            if item._product._id == product._id:
                item._quantity = quantity
                break
        else:
            cartItem = CartItem(product, quantity)
            self._cart._items.append(cartItem)
        return f"Added {quantity} x {product._name} to your cart."

    def removeFromCart(self, productId: int):
        self._cart._items = [item for item in self._cart._items if item._product._id != productId]
    
    def clearCart(self):
        self._cart._items = []
        return self._cart._items
        
    def viewCart(self):
        print("Cart contents:")
        for item in self._cart._items:
            print(f"item: {item._product._name}  x  quantity: {item._quantity}")
        print(f"Total: ${self.getTotal()}")

        invoice = Invoice(self._cart)
        print(invoice.printInvoice())
    
    def getTotal(self):
        return sum(item.getTotal() for item in self._cart._items)

    def checkout(self, customerName, address, filename="data/products.json"):
        if not self._cart._items:
            raise Exception("Cannot place an order: your cart is empty.")
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                
            for cartItem in self._cart._items:
                for prod in data:
                    if prod["_id"] == cartItem._product._id:
                        if prod["_quantity"] < cartItem._quantity:
                            raise ValueError(f"Not enough stock for {prod['_name']}")
                        prod["_quantity"] -= cartItem._quantity
                    
            with open(filename, "w") as file:
                json.dump(data, file, indent=2)
                
            from model.Order import Order
            
            Payment.process()
            
            orderId = OrderManager.getNextOrderId("data/orders.txt")
            shipmentInfo = ShipmentInfo(customerName, address)
            order = Order(orderId, customerName, shipmentInfo, self._cart)
            
            OrderManager.saveToFile(order, "data/orders.txt")

            receipt = Receipt(order)
            print(receipt.printReceipt())
            self.clearCart()
            print(f"Order {orderId} placed successfully.")
            return order

        except Exception as e:
            print(f"Checkout failed: {e}")
