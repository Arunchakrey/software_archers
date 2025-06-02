from model.Cart import Cart
from model.Product import Product

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

    def checkout(self, customer_id):
        try:
            self.cart.checkOut(customer_id)
        except Exception as e:
            print(f"Checkout failed: {e}")
