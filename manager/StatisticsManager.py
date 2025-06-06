from datetime import datetime
from collections import defaultdict
from reader.OrderReader import OrderReader

class StatisticsManager:
    def __init__(self):
        self._totalSales = 0.0
        self._topSellingProducts = []

    def analyzeSales(self, startDate, endDate, filename="data/orders.txt"):
        allOrders = OrderReader.readAllOrders(filename)
        total = 0.0
        for order in allOrders:
            if startDate <= order._orderDate <= endDate:
                total += order._total
        self._totalSales = total
        print(f"Total revenue from {startDate} to {endDate} is ${total:.2f}")
        return total

    def captureProducts(self, startDate, endDate, filename="data/orders.txt"):
        allOrders = OrderReader.readAllOrders(filename)
        productSales = defaultdict(lambda: {
            "quantity": 0,
            "unit_price": [],
            "total_revenue": 0.0
        })

        for order in allOrders:
            if startDate <= order._orderDate <= endDate:
                for item in order._items:
                    name = item._product._name
                    qty = item._quantity
                    total = item.getTotal()
                    unit = round(total / qty, 2)
                    stats = productSales[name]
                    stats["quantity"] += qty
                    stats["total_revenue"] += total
                    stats["unit_price"].append(unit)

        return dict(productSales)

    def findTopSellingProducts(self, startDate, endDate, topN=None, filename="data/orders.txt"):
        stats = self.captureProducts(startDate, endDate, filename)
        ranked = sorted(stats.items(), key=lambda x: x[1]["quantity"], reverse=True)
        return ranked[:topN] if topN else ranked

    def generateStatistics(self, startDate, endDate, topN=None):
        start = datetime.strptime(startDate, "%Y-%m-%d").date()
        end = datetime.strptime(endDate, "%Y-%m-%d").date()
        self._totalSales = self.analyzeSales(start, end)
        self._topSellingProducts = self.findTopSellingProducts(start, end, topN)
        
        print(f"\nTop {topN if topN else 'all'} selling products:")
        for name, data in self._topSellingProducts:
            avg = round(sum(data["unit_price"]) / len(data["unit_price"]), 2) if data["unit_price"] else 0
            print(f"- {name}: {data['quantity']} units, avg ${avg:.2f}/unit, ${data['total_revenue']:.2f} revenue")
