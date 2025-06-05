import json
from model.Product import Product

class ProductReader:
    @staticmethod
    def readFromJson(filepath: str) -> list:
        products = []
        try:
            with open(filepath, "r") as file:
                data = json.load(file)
                for item in data:
                    product = Product(
                        id=item["_id"],
                        name=item["_name"],
                        price=item["_price"],
                        quantity=int(item["_quantity"]),
                        description=item["_description"]
                    )
                    products.append(product)
        except FileNotFoundError:
            print(f"File not found: {filepath}")
        except json.JSONDecodeError:
            print("Error parsing JSON file.")
        except KeyError as e:
            print(f"Missing key in product data: {e}")
        return products
