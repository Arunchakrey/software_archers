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
            f.write(f"{order._orderId}, {order._customerId}, {order._orderDate}, {order._total:.2f}, {order._status}\n")
            f.write(order._shipmentInfo.getDeliveryLabel())
            for item in order._items:
                f.write(f"  -{item._product._name} x {item._quantity} = ${item.getTotal():.2f}\n")
            f.write("---------------------------------\n")

    @staticmethod
    def getNextOrderId(filepath="data/orders.txt") -> int:
        """
        Returns (max existing orderId + 1). If file missing or empty, returns 1.
        Relies on OrderReader.readAllOrders().
        """
        allOrder = OrderReader.readAllOrders(filepath)
        if not allOrder:
            return 1
        maxId = max(o._orderId for o in allOrder)
        return maxId + 1

    @staticmethod
    def updateOrderStatus(orderId: int, newStatus: str, filename="data/orders.txt") -> bool:
        """
        Reads all orders via OrderReader, updates the matching order’s status in memory,
        then rewrites the entire file with the new statuses. Returns True on success, False if not found.
        """
        allOrders = OrderReader.readAllOrders(filename)
        found = False
        for o in allOrders:
            if o._orderId == orderId:
                o._status = newStatus
                found = True
                break
        if not found:
            print(f"Order ID {orderId} not found in '{filename}'.")
            return False

        with open(filename, "w") as f:
            for o in allOrders:
                f.write(f"{o._orderId}, {o._customerId}, {o._orderDate}, {o._total:.2f}, {o._status}\n")
                f.write(o._shipmentInfo.getDeliveryLabel())
                for item in o._items:
                    f.write(f"  -{item._product._name} x {item._quantity} = ${item.getTotal():.2f}\n")
                f.write("---------------------------------\n")
        return True

    @staticmethod
    def getOrdersByCustomerName(account, filename="data/orders.txt") -> List[Order]:
        """
        Returns a list of Order objects for which order.customerId == account.username.
        Simply delegates to OrderReader.getOrdersByCustomer().
        """
        return OrderReader.getOrdersByCustomer(account._username, filename)

    @staticmethod
    def displayOrders(account):
        """
        Fetches and prints each past order’s summary for this customer.
        """
        orders = OrderManager.getOrdersByCustomerName(account)
        if not orders:
            print("No past orders found.")
            return

        print(f"\n=== Past Orders for {account._username} ===")
        for order in orders:
            print(order.getOrderSummary())
            print()  # blank line between orders
