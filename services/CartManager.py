from model.Cart import Cart
from model.Product import Product
import json

class CartManager:
    def __init__(self, cart: Cart):
        self.cart = cart

    def addToCart(self, product: Product, quantity: int):
        result = self.cart.addItem(product, quantity)
        if result:
            print(result)
        else:
            print(f"Added {quantity} x {product.name} to your cart.")

    def removeFromCart(self, product_id: int):
        self.cart.removeItem(product_id)
        print(f"Removed product ID {product_id} from your cart.")

    def viewCart(self):
        self.cart.displayCart()

    def checkout(self, customerName, address, filename="data/products.json"):
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
                self.cart.checkOut(customerName, address)

        except Exception as e:
            print(f"Checkout failed: {e}")
