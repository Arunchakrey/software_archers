class Product:

    def __init__(self, id: int, name: str, price: float, quantity: int, description: str):
        self._id = id
        self._name = name
        self._price = price
        self._quantity = quantity
        self._description = description
    def getProductName(self):
        return self._name

    def getProductPrice(self):
        return self._price

    def setProductName(self, value):
        self._name = value

    def setProductPrice(self, value):
        self._price = float(value)

    def setProductQuantity(self, value):
        self._quantity = int(value)

    def isInStock(self, quantity: int = 1):
        return self._quantity >= quantity
