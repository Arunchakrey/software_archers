from model.AdminAccount import AdminAccount
from services.Catalogue import Catalogue
from reader.OrderReader import OrderReader

class AdminMenu:
    """
    Handles the interactive loop for an AdminAccount.
    """

    def __init__(self, account: AdminAccount, catalogue: Catalogue, productsFilename: str):
        self._account = account
        self._catalogue = catalogue
        self._productsFilename = productsFilename

    def run(self):
        """
        Runs the admin menu loop until the admin chooses to log out.
        """
        print(f"\nWelcome, {self._account.username}! (Admin Mode)\n")

        while True:
            print("--- Admin Menu ---")
            print("1. View Products")
            print("2. Edit Products")
            print("3. Generate Statistics")
            print("4. Manage Shipment Status")
            print("5. Log out")

            choice = input("Choose an option: ").strip()
            if choice == "1":
                # View all products
                self._catalogue.listProducts()

            elif choice == "2":
                self.editProducts()

            elif choice == "3":
                self.generateStatistics()

            elif choice == "4":
                self.manageShipmentStatus()
                
            elif choice == "5":
                print("Logging out of Admin Menu.\n")
                break

            else:
                print("Invalid option. Please choose 1–5.\n")
        
    def editProducts(self):
        """
        Sub‐menu for editing products (register new, update quantity, update price).
        """
        while True:
            print("\n--- Edit Products ---")
            print("1. View Products")
            print("2. Register New Product")
            print("3. Update Product Quantity")
            print("4. Update Product Price")
            print("5. Delete Product")
            print("6. Return to Admin Menu")

            sub = input("Choose an option: ").strip()

            if sub == "1":
                self._catalogue.listProducts()

            elif sub == "2":
                try:
                    pId = self._account._productManager.getNextId(self._productsFilename)
                    pName = input("Enter Product Name: ").strip()
                    pPrice = float(input("Enter Product's Price: ").strip())
                    pQuantity = int(input("Enter Product's Quantity: ").strip())
                    pDescription = input("Enter Product's Description: ").strip()
                    self._account._productManager.registerProduct(pId, pName, pPrice, pQuantity, pDescription)
                except ValueError:
                    print("Invalid input. Price must be a number, Quantity must be an integer.\n")

            elif sub == "3":
                try:
                    self._catalogue.listProducts()
                    pId = int(input("Enter Product ID: ").strip())
                    newQty = int(input("Enter new quantity: ").strip())
                    self._account._productManager.updateQuantity(pId, newQty)
                except ValueError:
                    print("Invalid ID or Quantity. Must be integer.\n")

            elif sub == "4":
                try:
                    self._catalogue.listProducts()
                    pId = int(input("Enter Product ID: ").strip())
                    newPrice = float(input("Enter new price: ").strip())
                    self._account._productManager.updatePrice(pId, newPrice)
                except ValueError:
                    print("Invalid ID or Price. Must be numeric.\n")

            elif sub == "5":
                self._catalogue.listProducts()
                self.deleteProduct()

            elif sub == "6":
                print("Returning to Admin Menu.\n")
                break

            else:
                print("Invalid option. Please choose 1–6.\n")

    def generateStatistics(self):
        """
        Prompt for date range and call the admin's generate_sales_report.
        """
        try:
            startDate = input("Enter start date (YYYY-MM-DD): ").strip()
            endDate = input("Enter end date (YYYY-MM-DD): ").strip()
            self._account.generateSalesReport(startDate, endDate) #edit
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.\n")

    def manageShipmentStatus(self):
        """
        Prompt for an order ID, then update its status to Incomplete/Complete.
        """

        try:
            orders = OrderReader.readAllOrders()
            OrderReader.printOrders(orders)
            orderId = int(input("Enter order ID to edit status: ").strip())
        except ValueError:
            print("Order ID must be an integer.\n")
            return

        print("\n1. Update Status to 'Incomplete'")
        print("2. Update Status to 'Complete'")
        
        try:
            statusChoice = int(input("Choose option: ").strip())
        except ValueError:
            print("Invalid input: please enter 1 or 2.")
            return

        if statusChoice in [1, 2]:
            updated = self._account.updateOrderStatus(orderId, statusChoice)
            if updated:
                print(f"Order {orderId} status updated successfully.\n")
            else:
                print(f"Failed to update order {orderId} status.\n")
        else:
            print("Invalid choice. Must be 1 or 2.\n")
            return
        
    def deleteProduct(self):
        try:
            productId = int(input("Enter Product ID to delete: ").strip())
            self._account._productManager.deleteProduct(productId)
        except ValueError:
            print("[ERROR] Invalid Product ID. Must be a number.")
        



