from model.AdminAccount import AdminAccount
from services.Catalogue import Catalogue

class AdminMenu:
    """
    Handles the interactive loop for an AdminAccount.
    """

    def __init__(self, account: AdminAccount, catalogue: Catalogue, products_filename: str):
        self.account = account
        self.catalogue = catalogue
        self.products_filename = products_filename

    def run(self):
        """
        Runs the admin menu loop until the admin chooses to log out.
        """
        print(f"\nWelcome, {self.account.username}! (Admin Mode)\n")

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
                self.catalogue.listProducts()

            elif choice == "2":
                self._editProducts()

            elif choice == "3":
                self._generateStatistics()

            elif choice == "4":
                self._manageShipmentStatus()

            elif choice == "5":
                print("Logging out of Admin Menu.\n")
                break

            else:
                print("Invalid option. Please choose 1–5.\n")

    def _editProducts(self):
        """
        Sub‐menu for editing products (register new, update quantity, update price).
        """
        while True:
            print("\n--- Edit Products ---")
            print("1. View Products")
            print("2. Register New Product")
            print("3. Update Product Quantity")
            print("4. Update Product Price")
            print("5. Return to Admin Menu")

            sub = input("Choose an option: ").strip()
            if sub == "1":
                self.catalogue.listProducts()

            elif sub == "2":
                # Register new product
                try:
                    p_id = self.account.product_manager.get_next_id(self.products_filename)
                    p_name = input("Enter Product Name: ").strip()
                    p_price = float(input("Enter Product's Price: ").strip())
                    p_quantity = int(input("Enter Product's Quantity: ").strip())
                    p_description = input("Enter Product's Description: ").strip()
                    self.account.product_manager.registerProduct(
                        p_id, p_name, p_price, p_quantity, p_description
                    )
                    print("New product registered successfully.\n")
                except ValueError:
                    print("Invalid input. Price must be a number, Quantity must be an integer.\n")

            elif sub == "3":
                # Update quantity
                try:
                    self.catalogue.listProducts()
                    p_id = int(input("Enter Product ID: ").strip())
                    new_qty = int(input("Enter new quantity: ").strip())
                    self.account.product_manager.updateQuantity(p_id, new_qty)
                    print("Quantity updated.\n")
                except ValueError:
                    print("Invalid ID or Quantity. Must be integer.\n")

            elif sub == "4":
                # Update price
                try:
                    self.catalogue.listProducts()
                    p_id = int(input("Enter Product ID: ").strip())
                    new_price = float(input("Enter new price: ").strip())
                    self.account.product_manager.updatePrice(p_id, new_price)
                    print("Price updated.\n")
                except ValueError:
                    print("Invalid ID or Price. Must be numeric.\n")

            elif sub == "5":
                print("Returning to Admin Menu.\n")
                break

            else:
                print("Invalid option. Please choose 1–5.\n")

    def _generateStatistics(self):
        """
        Prompt for date range and call the admin's generate_sales_report.
        """
        try:
            start_date = input("Enter start date (YYYY-MM-DD): ").strip()
            end_date = input("Enter end date (YYYY-MM-DD): ").strip()
            self.account.generate_sales_report(start_date, end_date)
            print("")  # blank line after stats
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.\n")

    def _manageShipmentStatus(self):
        """
        Prompt for an order ID, then update its status to Incomplete/Complete.
        """
        try:
            order_id = int(input("Enter order ID to edit status: ").strip())
        except ValueError:
            print("Order ID must be an integer.\n")
            return

        print("\n1. Update Status to 'Incomplete'")
        print("2. Update Status to 'Complete'")
        try:
            status_choice = int(input("Choose option: ").strip())
            if status_choice == 1:
                updated = self.account.updateOrderStatus(order_id, status_choice)
            elif status_choice == 2:
                updated = self.account.updateOrderStatus(order_id, status_choice)
            else:
                print("Invalid choice. Must be 1 or 2.\n")
                return

            if updated:
                print(f"Order {order_id} status updated successfully.\n")
            else:
                print(f"Failed to update status for order {order_id}.\n")

        except ValueError:
            print("Invalid input. Must be 1 or 2.\n")


