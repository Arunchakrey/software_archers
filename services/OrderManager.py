import re
from datetime import datetime
from typing import List

from model.Order import Order
from model.Cart import Cart
from model.CartItem import CartItem
from model.Product import Product
from model.ShipmentInfo import ShipmentInfo

class OrderManager:
    @staticmethod
    def saveToFile(order, filepath="data/orders.txt"):
        """
        Appends one order to orders.txt with this exact structure:

        1, alice, 2025-05-28, 250.00
          -Customer: alice     Address:vic
          -Iphone 10 x 1 = $200.00
          -Gaming Chair x 1 = $50.00
        ---------------------------------
        """
        with open(filepath, "a") as f:
            # 1) Header: orderId, customerId, orderDate, total
            f.write(f"{order.orderId}, {order.customerId}, {order.orderDate}, {order.total:.2f}\n")
            # 2) Shipment line
            shipmentLabel = order.shipmentInfo.getDeliveryLabel()
            f.write(shipmentLabel)
            # 3) Each item line: "-<product name> x <quantity> = $<line_total>"
            for item in order.items:
                line_total = item.getTotal()
                f.write(f"  -{item.product.name} x {item.quantity} = ${line_total:.2f}\n")
            # 4) Separator
            f.write("---------------------------------\n")

    @staticmethod
    def getNextOrderId(filepath="data/orders.txt") -> int:
        """
        Reads orders.txt from bottom to top, finds the last header line
        (format: "<orderId>, <username>, <YYYY-MM-DD>, <total>"),
        and returns (thatOrderId + 1). If the file does not exist or no
        valid header is found, returns 1.
        """
        try:
            with open(filepath, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            return 1

        for line in reversed(lines):
            stripped = line.strip()
            # Skip blank lines and separators
            if not stripped or stripped.startswith("-"):
                continue
            parts = [p.strip() for p in stripped.split(",")]
            if parts and parts[0].isdigit():
                return int(parts[0]) + 1

        return 1

    @staticmethod
    def getOrdersByCustomerName(account, filename="data/orders.txt") -> List[Order]:
        """
        Parses orders.txt and returns a list of Order objects for which
        order.customerId == account._username.  Expects exactly this format:

        1, alice, 2025-05-28, 250.00
          -Customer: alice     Address:vic
          -Iphone 10 x 1 = $200.00
          -Gaming Chair x 1 = $50.00
        ---------------------------------
        """
        orders: List[Order] = []

        # (1) Header: "<orderId>, <username>, <YYYY-MM-DD>, <total>"
        HEADER_RE = re.compile(r"^(\d+)\s*,\s*(\w+)\s*,\s*([\d\-]+)\s*,\s*([\d\.]+)\s*$")
        # (2) Shipment: "-Customer: <username>     Address:<address>"
        SHIP_RE   = re.compile(r"^-\s*Customer:\s*(\w+)\s+Address:(.+)$")
        # (3) Item: "-<product name> x <quantity> = $<line_total>"
        ITEM_RE   = re.compile(r"^-\s*(.+?)\s+x\s+(\d+)\s+=\s*\$(\d+(?:\.\d{1,2})?)\s*$")

        try:
            with open(filename, "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
            return []

        current_order = None
        current_cart = None

        for raw in lines:
            line = raw.rstrip("\n")
            if not line.strip():
                continue  # skip blank lines

            # (A) Check for a header line: "1, alice, 2025-05-28, 250.00"
            m_header = HEADER_RE.match(line)
            if m_header:
                order_id  = int(m_header.group(1))
                cust_name = m_header.group(2)
                date_str  = m_header.group(3)
                total_amt = float(m_header.group(4))

                if cust_name == account._username:
                    # If we were building a previous order, finalize it now:
                    if current_order is not None:
                        # Copy item‐snapshot into the Order, then recalc total
                        current_order.items = current_cart.items.copy()
                        current_order.total = sum(it.getTotal() for it in current_cart.items)
                        orders.append(current_order)

                    current_cart = Cart()
                    parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    # Placeholder ShipmentInfo; will set address next
                    shipment = ShipmentInfo(cust_name, "")

                    # Construct a new Order with an empty cart for now
                    current_order = Order(
                        order_id,
                        cust_name,
                        shipment,
                        current_cart,
                        "Incomplete",   # default status
                        parsed_date
                    )
                    # We will overwrite .items and .total once all item-lines are read.
                else:
                    # Header for a different user → reset state
                    current_order = None
                    current_cart  = None

                continue  # move to next line

            # (B) If we have an active order (header matched this account), parse shipment or item lines
            if current_order is not None:
                stripped = line.strip()

                # (B1) Shipment line: "-Customer: alice     Address:vic"
                m_ship = SHIP_RE.match(stripped)
                if m_ship:
                    ship_name = m_ship.group(1)
                    address   = m_ship.group(2).strip()
                    current_order.shipmentInfo = ShipmentInfo(ship_name, address)
                    continue

                # (B2) Item line: "-Iphone 10 x 1 = $200.00"
                m_item = ITEM_RE.match(stripped)
                if m_item:
                    prod_name  = m_item.group(1).strip()
                    qty        = int(m_item.group(2))
                    line_total = float(m_item.group(3))
                    # Compute unit price as a float
                    unit_price = round(line_total / qty, 2)

                    # Create a minimal Product stub using float(unit_price)
                    prod = Product(prod_name, unit_price, 0, "")
                    cart_item = CartItem(prod, qty)
                    current_cart.items.append(cart_item)
                    continue

                # (B3) Separator line: "---------------------------------"
                if stripped.startswith("-" * 33):
                    # Before appending, finalize items & total
                    current_order.items = current_cart.items.copy()
                    total_list = []
                    for it in current_cart.items:
                        try:
                            total_list.append(float(it.getTotal()))
                        except ValueError:
                            continue
                    current_order.total = sum(total_list)

                    orders.append(current_order)

                    current_order = None
                    current_cart  = None
                    continue

        # (C) If the file ends without a trailing separator, finalize the last order
        if current_order is not None and current_cart is not None:
            current_order.items = current_cart.items.copy()
            total_list = []
            for it in current_cart.items:
                try:
                    total_list.append(float(it.getTotal()))
                except ValueError:
                    continue
            current_order.total = sum(total_list)
            orders.append(current_order)

        return orders

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
