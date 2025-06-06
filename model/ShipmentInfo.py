class ShipmentInfo:
    def __init__(self, customerName: str, deliveryAddress: str):
        self._customerName = customerName
        self._deliveryAddress = deliveryAddress

    def getDeliveryLabel(self) -> str:
        return f"  -Customer: {self._customerName}     Address:{self._deliveryAddress}\n"
