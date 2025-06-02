from datetime import datetime
from collections import defaultdict
import re


class Statistics:
    def __init__(self):
        self.period
        self.totalSales
        self.topSellingProducts = []
        
    def analyzeSales(self, startDate, endDate, filename = "data/orders.txt"):
        """get total from all orders in the order.txt file across the selected date range

        Args:
            startDate (_type_): start of the selected date range
            endDate (_type_): end of the selected date range
            filename (str, optional): Defaults to "data/orders.txt".

        Returns:
            totalSales: total from all orders in the date range
        """
        try:
            with open (filename, "r") as f:
                lines = f.readlines()
                totalSales = 0.0
                for line in lines:
                    if line.strip() and not line.strip().startswith("-"):
                        parts = line.strip().split(",")
                        orderDate = datetime.strptime(parts[2].strip(), "%Y-%m-%d").date()
                        if startDate <= orderDate <= endDate:
                            totalSales += float(parts[3])
                            
            print(f"Total revenue from {startDate} to {endDate} is ${totalSales:.2f}")
            return totalSales
        except FileNotFoundError:
            print (f"Fill '{filename}' not found.")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    
    def captureProducts(self,startDate, endDate, filename="data/orders.txt"):
        productSales = defaultdict(lambda: {
            "quantity": 0, 
            "unit_price": [],
            "total_revenue": 0.0
            })

        try:
            with open(filename, "r") as f:
                lines = f.readlines()
                valid_order = False

                for line in lines:
                    line = line.strip()
                    if not line:
                        continue

                    if not line.startswith("-"):  # It's a main order line
                        parts = line.split(",")
                        try:
                            order_date = datetime.strptime(parts[2].strip(), "%Y-%m-%d").date()
                            valid_order = startDate <= order_date <= endDate
                        except:
                            valid_order = False

                    elif line.startswith("-") and valid_order:
                        # e.g., "- Mouse x 3 = $120.00"
                        match = re.match(r"-\s*(.+?)\s+x\s+(\d+)\s+=\s+\$(\d+(?:\.\d{1,2})?)", line)
                        if match:
                            productName = match.group(1).strip()
                            quantity = int(match.group(2).strip())
                            totalPrice = float(match.group(3).strip())
                            unit_price = round(totalPrice / quantity, 2)

                            product = productSales[productName]
                            product["quantity"] += quantity
                            product["total_revenue"] += totalPrice
                            product["unit_price"].append(unit_price)

            return dict(productSales)

        except FileNotFoundError:
            print("File not found.")
            return None
        
    def findTopSellingProducts(self, startDate, endDate, top_n=None):
        try:
            productSales = self.captureProducts(startDate, endDate)
            results = sorted(productSales.items(), key=lambda x: x[1]["quantity"], reverse=True)
        except Exception as e:
            print(f"Error: {e}")
            return []

        if top_n:
            return results[:top_n]
        return results

    def generateStatistics(self, startDate, endDate, top_n=None):
        start = datetime.strptime(startDate, "%Y-%m-%d").date()
        end = datetime.strptime(endDate, "%Y-%m-%d").date()

        self.totalSales = self.analyzeSales(start, end)
        self.topSellingProducts = self.findTopSellingProducts(start, end, top_n)

        print(f"\nTop {top_n if top_n else 'all'} selling products:")
        for name, data in self.topSellingProducts:
            print(f"-{name}: {data['quantity']} units, ${data['unit_price']}/unit, ${data['total_revenue']:.2f} revenue")
