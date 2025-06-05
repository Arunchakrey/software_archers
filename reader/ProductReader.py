import json
from model.Product import Product  # adjust import path based on your structure

class ProductReader:
    @staticmethod
    def readFromJson(filepath: str) -> list:
        products = []
        try:
            with open(filepath, "r") as file:
                data = json.load(file)
                for item in data:
                    product = Product(
                        id=item["id"],
                        name=item["name"],
                        price=item["price"],
                        quantity=item["quantity"],
                        description=item["description"]
                    )
                    products.append(product)
        except FileNotFoundError:
            print(f"File not found: {filepath}")
        except json.JSONDecodeError:
            print("Error parsing JSON file.")
        except KeyError as e:
            print(f"Missing key in product data: {e}")
        return products
