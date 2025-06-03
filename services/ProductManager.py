from model.Product import Product
from services.Catalogue import Catalogue  # assumes your catalogue class holds product list
import os
import json

class ProductManager:
    def __init__(self, catalogue: Catalogue):
        self.catalogue = catalogue


    def append_to_json(self, product, filename='data/products.json'):
        product_dict = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": product.quantity,
            "description": product.description
        }
        # Read existing data
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                try:
                    products = json.load(file)
                except json.JSONDecodeError:
                    products = []
        else:
            products = []
        # Append and write back
        products.append(product_dict)
        with open(filename, 'w') as file:
            json.dump(products, file, indent=2)


    def registerProduct(self, id: int, name: str, price: float, quantity: int, description: str):
        if self.catalogue.getProductById(id):
            print(f"[ERROR] Product with ID {id} already exists.")
            return
        new_product = Product(id, name, price, quantity, description)
        # self.catalogue.products.append(new_product)
        self.append_to_json(new_product)
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

    def get_next_id(self, json_file):
        if not os.path.exists(json_file):
            return 1
        with open(json_file, 'r') as file:
            try:
                data = json.load(file)
                if not data:
                    return 1
                
                last_entry = data[-1]
                last_id = last_entry.get("id", 0)
                return last_id + 1
            except json.JSONDecodeError:
                return 1

