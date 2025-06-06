from model.Product import Product
from reader.ProductReader import ProductReader  # adjust to your path

class Catalogue:
    def __init__(self, jsonFile='data/products.json'):
        self._products: list[Product] = []
        self._jsonFile = jsonFile

    def loadFromFile(self, filepath: str):
        self._products = ProductReader.readFromJson(filepath)

    def listProducts(self):
        self.loadFromFile(filepath='data/products.json')
        for product in self._products:
            print(f"\n[{product._id}] {product._name} - ${product._price:.2f} ({product._quantity} in stock)")
            print(product._description)

    def getProductById(self, productId: int):
        self.loadFromFile(filepath='data/products.json')
        for product in self._products:
            if int(product._id) == int(productId):
                return product
        return None
    

    def saveProductsToJson(self):
        import json
        with open(self._jsonFile, 'w') as file:
            json.dump([vars(prod) for prod in self._products], file, indent=2)
