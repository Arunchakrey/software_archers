from datetime import datetime
from collections import defaultdict
import re

class StatisticsManager:
    def __init__(self):
        self.totalSales = 0.0
        self.topSellingProducts = []

    def analyzeSales(self, startDate, endDate, filename="data/orders.txt"):
        HEADER_RE = re.compile(
            r"^(\d+)\s*,\s*(\w+)\s*,\s*([\d\-]+)\s*,\s*([\d\.]+)(?:\s*,\s*(\w+))?"
        )

        try:
            with open(filename, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
            return 0.0

        totalSales = 0.0
        for raw in lines:
            line = raw.strip()
            if not line or line.startswith("-"): 
                # skip blank lines and separators
                continue

            m_header = HEADER_RE.match(line)
            if not m_header:
                continue

            # group(3) = date, group(4) = total
            order_date = datetime.strptime(m_header.group(3), "%Y-%m-%d").date()
            if startDate <= order_date <= endDate:
                totalSales += float(m_header.group(4))

        print(f"Total revenue from {startDate} to {endDate} is ${totalSales:.2f}")
        self.totalSales = totalSales
        return totalSales

    def captureProducts(self, startDate, endDate, filename="data/orders.txt"):
        HEADER_RE = re.compile(
            r"^(\d+)\s*,\s*(\w+)\s*,\s*([\d\-]+)\s*,\s*([\d\.]+)(?:\s*,\s*(\w+))?"
        )
        ITEM_RE = re.compile(r"^-\s*(.+?)\s+x\s+(\d+)\s+=\s*\$(\d+(?:\.\d{1,2})?)\s*$")

        productSales = defaultdict(lambda: {
            "quantity": 0,
            "unit_price": [],
            "total_revenue": 0.0
        })

        valid_order = False

        try:
            with open(filename, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
            return {}

        for raw in lines:
            line = raw.strip()
            if not line:
                continue

            # If it’s exactly the separator, reset valid_order = False
            if line.startswith("-" * 33):
                valid_order = False
                continue

            # Check for header (4‐ or 5‐field)
            m_header = HEADER_RE.match(line)
            if m_header:
                order_date = datetime.strptime(m_header.group(3), "%Y-%m-%d").date()
                valid_order = (startDate <= order_date <= endDate)
                continue

            # If we are inside a valid order, attempt to parse an item line
            if valid_order:
                m_item = ITEM_RE.match(line)
                if m_item:
                    product_name = m_item.group(1).strip()
                    qty = int(m_item.group(2))
                    line_total = float(m_item.group(3))
                    unit_price = round(line_total / qty, 2)

                    stats = productSales[product_name]
                    stats["quantity"] += qty
                    stats["total_revenue"] += line_total
                    stats["unit_price"].append(unit_price)

        return dict(productSales)

    def findTopSellingProducts(self, startDate, endDate, top_n=None, filename="data/orders.txt"):
        # Fetch the raw productSales dict
        productSales = self.captureProducts(startDate, endDate, filename)

        # Build a list of (productName, statsDict) and sort by quantity desc
        results = sorted(
            productSales.items(),
            key=lambda x: x[1]["quantity"],
            reverse=True
        )

        if top_n is not None:
            return results[:top_n]
        return results

    def generateStatistics(self, startDate, endDate, top_n=None):
        # Convert to date objects
        start = datetime.strptime(startDate, "%Y-%m-%d").date()
        end = datetime.strptime(endDate, "%Y-%m-%d").date()

        self.totalSales = self.analyzeSales(start, end)
        self.topSellingProducts = self.findTopSellingProducts(start, end, top_n)

        print(f"\nTop {top_n if top_n else 'all'} selling products:")
        for name, data in self.topSellingProducts:
            avg_unit = (
                round(sum(data["unit_price"]) / len(data["unit_price"]), 2)
                if data["unit_price"] else 0.00
            )
            print(f"- {name}: {data['quantity']} units, "
                  f"avg ${avg_unit:.2f}/unit, ${data['total_revenue']:.2f} revenue")
