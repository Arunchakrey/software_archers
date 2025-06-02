from model.Product import Product
from services.Catalogue import Catalogue  # assumes your catalogue class holds product list

class ProductManager:
    def __init__(self, catalogue: Catalogue):
        self.catalogue = catalogue

    def registerProduct(self, id: int, name: str, price: float, quantity: int, description: str):
        if self.catalogue.getProductById(id):
            print(f"[ERROR] Product with ID {id} already exists.")
            return
        new_product = Product(id, name, price, quantity, description)
        self.catalogue.products.append(new_product)
        print(f"[SUCCESS] Product '{name}' registered.")

    def updatePrice(self, product_id: int, new_price: float):
        product = self.catalogue.getProductById(product_id)
        if product:
            product.price = new_price
            print(f"[UPDATED] Price of '{product.name}' set to ${new_price:.2f}")
        else:
            print("[ERROR] Product not found.")

    def updateQuantity(self, product_id: int, new_quantity: int):
        product = self.catalogue.getProductById(product_id)
        if product:
            product.quantity = new_quantity
            print(f"[UPDATED] Quantity of '{product.name}' set to {new_quantity}")
        else:
            print("[ERROR] Product not found.")
