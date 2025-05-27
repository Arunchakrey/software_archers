class OrderManager:
    # def __init__(self):
    #     pass
    
    # def isOrderId(self, value, orderId ) -> bool:
    #     try:
    #         return int(value) == int(orderId)
    #     except ValueError:
    #         return False
    @staticmethod
    def saveToFile(order, filepath="orders.txt"):
        with open(filepath, "a") as f:
            f.write(f"{order.orderId}, {order.customerId}, {order.orderDate}, {order.total:.2f}\n")
            for item in order.items:
                f.write(f"  -{item.product.name} x {item.quantity} = ${item.getTotal():.2F}\n")
            f.write("---------------------------------")
    
    @staticmethod
    def getNextOrderId(filepath="orders.txt") -> int:
        try:
            with open(filepath, "r") as f:
                lines = f.readlines()
                for line in reversed(lines):
                    if line.strip() and not line.strip().startswith("-"):  # Look for main order line
                        parts = line.strip().split(",")
                        if parts[0].strip().isdigit():
                            return int(parts[0]) + 1
            return 1  # If no valid order found
        except FileNotFoundError:
            return 1  # If file doesn't exist
