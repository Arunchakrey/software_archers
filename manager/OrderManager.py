# services/OrderManager.py

from datetime import datetime
from typing import List

from model.Order import Order
from model.ShipmentInfo import ShipmentInfo
from reader.OrderReader import OrderReader

class OrderManager:
    @staticmethod
    def saveToFile(order, filepath="data/orders.txt"):
        """
        Appends one order to orders.txt with this structure:

        <orderId>, <customerId>, <YYYY-MM-DD>, <total>, <status>
          -Customer: <customerId>     Address:<address>
          -<product name> x <quantity> = $<line_total>
          -<product name> x <quantity> = $<line_total>
        ---------------------------------
        """
        with open(filepath, "a") as f:
            # 1) Header line
            f.write(f"{order.orderId}, {order.customerId}, {order.orderDate}, {order.total:.2f}, {order.status}\n")

            # 2) Shipment line
            f.write(order.shipmentInfo.getDeliveryLabel())

            # 3) Each item line
            for item in order.items:
                line_total = item.getTotal()
                f.write(f"  -{item.product.name} x {item.quantity} = ${line_total:.2f}\n")

            # 4) Separator
            f.write("---------------------------------\n")

    @staticmethod
    def getNextOrderId(filepath="data/orders.txt") -> int:
        """
        Returns (max existing orderId + 1). If file missing or empty, returns 1.
        Relies on OrderReader.readAllOrders().
        """
        all_orders = OrderReader.readAllOrders(filepath)
        if not all_orders:
            return 1
        max_id = max(o.orderId for o in all_orders)
        return max_id + 1

    @staticmethod
    def updateOrderStatus(orderId: int, newStatus: str, filename="data/orders.txt") -> bool:
        """
        Reads all orders via OrderReader, updates the matching order’s status in memory,
        then rewrites the entire file with the new statuses. Returns True on success, False if not found.
        """
        # 1) Read all existing orders
        all_orders = OrderReader.readAllOrders(filename)

        found = False
        for o in all_orders:
            if o.orderId == orderId:
                o.status = newStatus
                found = True
                break

        if not found:
            print(f"Order ID {orderId} not found in '{filename}'.")
            return False

        # 2) Rewrite the entire file with updated statuses
        with open(filename, "w") as f:
            for o in all_orders:
                # Header
                f.write(f"{o.orderId}, {o.customerId}, {o.orderDate}, {o.total:.2f}, {o.status}\n")
                # Shipment
                f.write(o.shipmentInfo.getDeliveryLabel())
                # Items
                for item in o.items:
                    line_total = item.getTotal()
                    f.write(f"  -{item.product.name} x {item.quantity} = ${line_total:.2f}\n")
                # Separator
                f.write("---------------------------------\n")

        return True

    @staticmethod
    def getOrdersByCustomerName(account, filename="data/orders.txt") -> List[Order]:
        """
        Returns a list of Order objects for which order.customerId == account.username.
        Simply delegates to OrderReader.getOrdersByCustomer().
        """
        return OrderReader.getOrdersByCustomer(account.username, filename)

    @staticmethod
    def displayOrders(account):
        """
        Fetches and prints each past order’s summary for this customer.
        """
        orders = OrderManager.getOrdersByCustomerName(account)
        if not orders:
            print("No past orders found.")
            return

        print(f"\n=== Past Orders for {account.username} ===")
        for order in orders:
            print(order.getOrderSummary())
            print()  # blank line between orders
