from model.Product import Product
from services.Catalogue import Catalogue
import os
import json

class ProductManager:
    def __init__(self, catalogue: Catalogue):
        self._catalogue = catalogue

    def appendToJson(self, product, filename='data/products.json'):
        productDict = {
            "_id": product._id,
            "_name": product._name,
            "_price": product._price,
            "_quantity": product._quantity,
            "_description": product._description
        }
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                try:
                    products = json.load(file)
                except json.JSONDecodeError:
                    products = []
        else:
            products = []
        products.append(productDict)
        with open(filename, 'w') as file:
            json.dump(products, file, indent=2)

    def registerProduct(self, id: int, name: str, price: float, quantity: int, description: str):
        if self._catalogue.getProductById(id):
            print(f"[ERROR] Product with ID {id} already exists.")
            return
        #for loading updated product.JSON during runtime
        self._catalogue.loadFromFile("data/products.json")
        existing = [p for p in self._catalogue._products if p._name == name and p._description == description]
        if existing:
            print(f"[ERROR] Product with name '{name}' and same description already exists.")
            return
        newProduct = Product(id, name, price, quantity, description)
        self.appendToJson(newProduct)
        print(f"[SUCCESS] Product '{name}' registered.")

    def updatePrice(self, productId: int, newPrice: float):
        product = self._catalogue.getProductById(productId)
        if product:
            product.setProductPrice(newPrice)
            self._catalogue.saveProductsToJson()
            print(f"[UPDATED] Price of '{product._name}' set to ${newPrice:.2f}")
        else:
            print("[ERROR] Product not found.")

    def updateQuantity(self, productId: int, newQuantity: int):
        product = self._catalogue.getProductById(productId)
        if product:
            product.setProductQuantity(newQuantity)
            self._catalogue.saveProductsToJson()
            print(f"[UPDATED] Quantity of '{product._name}' set to {newQuantity}")
        else:
            print("[ERROR] Product not found.")

    def getNextId(self, jsonFile):
        if not os.path.exists(jsonFile):
            return 1
        with open(jsonFile, 'r') as file:
            try:
                data = json.load(file)
                if not data:
                    return 1
                usedIds = sorted(p.get("_id", 0) for p in data)
                for i in range(1, usedIds[-1] + 2):
                    if i not in usedIds:
                        return i
            except json.JSONDecodeError:
                return 1
    
    def deleteProduct(self, productId: int, filename='data/products.json'):
            if not os.path.exists(filename):
                print("[ERROR] Product file not found.")
                return

            with open(filename, 'r') as file:
                try:
                    products = json.load(file)
                except json.JSONDecodeError:
                    print("[ERROR] Failed to parse product file.")
                    return

            newProducts = [p for p in products if p.get("_id") != productId]

            if len(newProducts) == len(products):
                print("[ERROR] Product ID not found.")
                return

            with open(filename, 'w') as file:
                json.dump(newProducts, file, indent=2)

            self._catalogue.loadFromFile(filename)
            print(f"[DELETED] Product with ID {productId} has been removed.")
