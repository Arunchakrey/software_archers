class ShipmentInfo:
    def __init__(self, customerName: str, deliveryAddress: str):
        self.customerName = customerName
        self.deliveryAddress = deliveryAddress
    
    def getDeliveryLabel(self) -> str:
        return (f"  -Customer: {self.customerName}     Address:{self.deliveryAddress}\n")