import re
from datetime import datetime
from typing import List

from model.Order import Order
from model.Cart import Cart
from model.CartItem import CartItem
from model.Product import Product
from model.ShipmentInfo import ShipmentInfo

class OrderReader:
    """
    Responsible for reading and parsing 'data/orders.txt' into Order objects.
    """

    # Matches a header with 4 or 5 fields:
    #   <orderId>, <customerId>, <YYYY-MM-DD>, <total>[, <status>]
    HEADER_RE = re.compile(
        r"^(\d+)\s*,\s*(\w+)\s*,\s*([\d\-]+)\s*,\s*([\d\.]+)(?:\s*,\s*(\w+))?"
    )

    # Matches shipment line:
    #   -Customer: <username>     Address:<address>
    SHIP_RE = re.compile(r"^-\s*Customer:\s*(\w+)\s+Address:(.+)$")

    # Matches item line:
    #   -<product name> x <quantity> = $<line_total>
    ITEM_RE = re.compile(r"^-\s*(.+?)\s+x\s+(\d+)\s+=\s*\$(\d+(?:\.\d{1,2})?)\s*$")

    @staticmethod
    def readAllOrders(filename="data/orders.txt") -> List[Order]:
        """
        Reads the entire orders.txt and returns a list of Order objects
        (with their CartItems attached), in the order they appear.
        """
        orders: List[Order] = []

        try:
            with open(filename, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            return orders

        current_order = None
        current_cart  = None

        for raw in lines:
            line = raw.rstrip("\n")
            if not line.strip():
                # skip blank lines
                continue

            #Check for a header line (4 or 5 comma-separated fields)
            m_header = OrderReader.HEADER_RE.match(line.strip())
            if m_header:
                order_id   = int(m_header.group(1))
                cust_name  = m_header.group(2)
                date_str   = m_header.group(3)
                total_amt  = float(m_header.group(4))
                status_txt = m_header.group(5) if m_header.group(5) else "Unknown"
                order_date = datetime.strptime(date_str, "%Y-%m-%d").date()

                # If we were in the middle of building a previous order, finalize it now:
                if current_order is not None and current_cart is not None:
                    current_order._items = current_cart._items.copy()
                    current_order._total = sum(it.getTotal() for it in current_cart._items)
                    orders.append(current_order)

                # Start a new Cart + Order (with empty items for now)
                current_cart = Cart()
                shipment = ShipmentInfo(cust_name, "")
                current_order = Order(
                    order_id,
                    cust_name,
                    shipment,
                    current_cart,
                    status_txt,
                    order_date
                )
                continue  # Move on to next line

            #If we have an active order being built, parse shipment / item / separator
            if current_order is not None and current_cart is not None:
                stripped = line.strip()

                # Shipment line
                m_ship = OrderReader.SHIP_RE.match(stripped)
                if m_ship:
                    ship_name = m_ship.group(1)
                    address   = m_ship.group(2).strip()
                    current_order._shipmentInfo = ShipmentInfo(ship_name, address)
                    continue

                # Item line
                m_item = OrderReader.ITEM_RE.match(stripped)
                if m_item:
                    prod_name  = m_item.group(1).strip()
                    qty        = int(m_item.group(2))
                    line_total = float(m_item.group(3))
                    unit_price = round(line_total / qty, 2)

                    # Create a minimal Product stub for the CartItem
                    prod = Product(id, prod_name, unit_price, 0, "")
                    cart_item = CartItem(prod, qty)
                    current_cart._items.append(cart_item)
                    continue

                # Separator line "---------------------------------"
                if stripped.startswith("-" * 33):
                    current_order._items = current_cart._items.copy()
                    current_order._total = sum(it.getTotal() for it in current_cart._items)
                    orders.append(current_order)

                    current_order = None
                    current_cart  = None
                    continue

                # Any other line: ignore
                continue

        # At end of file, if an order was in progress but never closed by a separator:
        if current_order is not None and current_cart is not None:
            current_order._items = current_cart._items.copy()
            current_order._total = sum(it.getTotal() for it in current_cart._items)
            orders.append(current_order)

        return orders

    @staticmethod
    def printOrders(orders: List[Order]):
        """
        Nicely prints a list of Order objects.
        """
        if not orders:
            print("No orders found.")
            return

        for order in orders:
            print("="*40)
            print(f"Order ID:   {order.orderId}")
            print(f"Customer:   {order.customerId}")
            print(f"Date:       {order.orderDate}")
            print(f"Status:     {order.status}")
            print(f"Shipment to: {order.shipmentInfo.customerName}")
            print(f"Address:     {order.shipmentInfo.deliveryAddress}")
            print("- Items:")
            for item in order.items:
                product = item.product
                print(f"   {product.name} x {item.quantity} @ ${product.price:.2f} each = ${item.getTotal():.2f}")
            print(f"Total:      ${order.total:.2f}")
            print("="*40)
            print()

    @staticmethod
    def getOrdersByCustomer(username: str, filename="data/orders.txt") -> List[Order]:
        """
        Returns only those Order objects whose customerId matches `username`.
        """
        return [order for order in OrderReader.readAllOrders(filename) if order._customerId == username]
    
    @staticmethod
    def printOrders(orders: List[Order]):
        """
        Nicely prints a list of Order objects.
        """
        if not orders:
            print("No orders found.")
            return

        for order in orders:
            print("="*40)
            print(f"Order ID:   {order._orderId}")
            print(f"Customer:   {order._customerId}")
            print(f"Date:       {order._orderDate}")
            print(f"Status:     {order._status}")
            print(f"Shipment to: {order._shipmentInfo._customerName}")
            print(f"Address:     {order._shipmentInfo._deliveryAddress}")
            print("- Items:")
            for item in order._items:
                product = item._product
                print(f"   {product._name} x {item._quantity} @ ${product._price:.2f} each = ${item.getTotal():.2f}")
            print(f"Total:      ${order._total:.2f}")
            print("="*40)
            print()
