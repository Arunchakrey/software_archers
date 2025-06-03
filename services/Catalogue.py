from model.Product import Product
from services.ProductReader import ProductReader  # adjust to your path

class Catalogue:
    def __init__(self):
        self.products: list[Product] = []

    def loadFromFile(self, filepath: str):
        self.products = ProductReader.readFromJson(filepath)

    def listProducts(self):
        self.loadFromFile(filepath='data/products.json')
        for product in self.products:
            print(f"\n[{product.id}] {product.name} - ${product.price:.2f} ({product.quantity} in stock)")

    def getProductById(self, product_id: int):
        for product in self.products:
            if product.id == product_id:
                return product
        return None
