class Product:
    def __init__(self, name: str , price: float, quantity: int, description: str, id: int = None):
        
        self.name = name
        self.price = price
        self.quantity = quantity
        self.description =description
        self.id = id
        
    #property
    def getProductName(self):
        return self.name
    
    def getProductPrice(self):
        return self.price
    
    def setProductName(self, value):
        self.name = value
    
    def setProductPrice(self, value):
        self.price = int(value)

    def setProductQuantity(self, value):
        self.quantity = int(value)
    
    def isInStock(self, quantity: int = 1):
        return self.quantity >= quantity
    
    
        
        