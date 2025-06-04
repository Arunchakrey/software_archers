from datetime import datetime
from collections import defaultdict
import re

class StatisticsManager:
    def __init__(self):
        self.totalSales = 0.0
        self.topSellingProducts = []

    def analyzeSales(self, startDate, endDate, filename="data/orders.txt"):
        """
        Reads only header lines in [startDate, endDate] range and sums the <total>:
        Header format: "<orderId>, <customerId>, <YYYY-MM-DD>, <total>"
        """
        HEADER_RE = re.compile(r"^(\d+)\s*,\s*(\w+)\s*,\s*([\d\-]+)\s*,\s*([\d\.]+)\s*$")

        try:
            with open(filename, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
            return None

        totalSales = 0.0
        for raw in lines:
            line = raw.strip()
            if not line or line.startswith("-"):
                continue

            m_header = HEADER_RE.match(line)
            if m_header:
                order_date = datetime.strptime(m_header.group(3), "%Y-%m-%d").date()
                if startDate <= order_date <= endDate:
                    totalSales += float(m_header.group(4))

        print(f"Total revenue from {startDate} to {endDate} is ${totalSales:.2f}")
        return totalSales

    def captureProducts(self, startDate, endDate, filename="data/orders.txt"):
        """
        Returns a dict mapping productName -> {quantity, [unit_price], total_revenue},
        using only item lines whose parent order’s date is inside [startDate, endDate].

        Item line format: "-<product name> x <quantity> = $<line_total>"
        """
        HEADER_RE = re.compile(r"^(\d+)\s*,\s*(\w+)\s*,\s*([\d\-]+)\s*,\s*([\d\.]+)\s*$")
        ITEM_RE   = re.compile(r"^-\s*(.+?)\s+x\s+(\d+)\s+=\s*\$(\d+(?:\.\d{1,2})?)\s*$")

        productSales = defaultdict(lambda: {
            "quantity": 0,
            "unit_price": [],
            "total_revenue": 0.0
        })

        try:
            with open(filename, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
            return None

        valid_order = False
        for raw in lines:
            line = raw.strip()
            if not line:
                continue

            # (1) Header line sets valid_order flag
            m_header = HEADER_RE.match(line)
            if m_header:
                order_date = datetime.strptime(m_header.group(3), "%Y-%m-%d").date()
                valid_order = (startDate <= order_date <= endDate)
                continue

            # (2) If valid_order, parse item lines
            if valid_order:
                m_item = ITEM_RE.match(line)
                if m_item:
                    product_name = m_item.group(1).strip()
                    qty = int(m_item.group(2))
                    total_price = float(m_item.group(3))
                    unit_price = round(total_price / qty, 2)

                    stats = productSales[product_name]
                    stats["quantity"] += qty
                    stats["total_revenue"] += total_price
                    stats["unit_price"].append(unit_price)

        return dict(productSales)

    def findTopSellingProducts(self, startDate, endDate, top_n=None):
        """
        Returns a list of (productName, statsDict) sorted by statsDict["quantity"] descending.
        """
        try:
            productSales = self.captureProducts(startDate, endDate)
            results = sorted(
                productSales.items(),
                key=lambda x: x[1]["quantity"],
                reverse=True
            )
        except Exception as e:
            print(f"Error: {e}")
            return []

        if top_n:
            return results[:top_n]
        return results

    def generateStatistics(self, startDate, endDate, top_n=None):
        """
        Prints total sales and top‐n selling products for orders in the given date range.
        """
        start = datetime.strptime(startDate, "%Y-%m-%d").date()
        end = datetime.strptime(endDate,   "%Y-%m-%d").date()

        self.totalSales        = self.analyzeSales(start, end)
        self.topSellingProducts = self.findTopSellingProducts(start, end, top_n)

        print(f"\nTop {top_n if top_n else 'all'} selling products:")
        for name, data in self.topSellingProducts:
            avg_unit = (
                round(sum(data["unit_price"]) / len(data["unit_price"]), 2)
                if data["unit_price"] else 0.0
            )
            print(f"- {name}: {data['quantity']} units, "
                  f"avg ${avg_unit:.2f}/unit, ${data['total_revenue']:.2f} revenue")
