class Product:
    def __init__(self, id: int, name: str , price: float, quantity: int, description: str):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.description =description
        
    #property
    def getProductName(self):
        return self.name
    
    def getProductPrice(self):
        return self.price
    
    def setProductName(self, value):
        self.name = value
    
    def setProductPrice(self, value):
        self.price = int(value)
    
    def isInStock(self, quantity: int = 1):
        return self.quantity >= quantity
    
    
        
        