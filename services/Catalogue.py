from model.Product import Product
from reader.ProductReader import ProductReader  # adjust to your path

class Catalogue:
    def __init__(self, json_file='data/products.json'):
        self._products: list[Product] = []
        self._json_file = json_file

    def loadFromFile(self, filepath: str):
        self._products = ProductReader.readFromJson(filepath)

    def listProducts(self):
        self.loadFromFile(filepath='data/products.json')
        for product in self._products:
            print(f"\n[{product.id}] {product.name} - ${product.price:.2f} ({product.quantity} in stock)")

    def getProductById(self, product_id: int):
        self.loadFromFile(filepath='data/products.json')
        for product in self._products:
            if int(product.id) == int(product_id):
                return product
        return None
    

    def save_products_to_json(self):
        import json
        with open(self._json_file, 'w') as file:
            json.dump([vars(prod) for prod in self._products], file, indent=2)
