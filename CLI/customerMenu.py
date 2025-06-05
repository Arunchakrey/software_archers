from model.CustomerAccount import CustomerAccount
from services.Catalogue import Catalogue
from manager.OrderManager import OrderManager

class CustomerMenu:
    """
    Handles the interactive loop for a CustomerAccount.
    """

    def __init__(self, account: CustomerAccount, catalogue: Catalogue):
        self.account = account
        self.catalogue = catalogue

    def run(self):
        """
        Runs the customer menu loop until the customer chooses to log out.
        """
        print(f"\nWelcome, {self.account.username}! (Customer Mode)\n")

        while True:
            print("--- Customer Menu ---")
            print("1. View Products")
            print("2. Add Product to Cart")
            print("3. View Cart")
            print("4. Remove Item from Cart")
            print("5. Checkout")
            print("6. View Orders")
            print("7. Log out")

            choice = input("Choose an option: ").strip()
            if choice == "1":
                self.catalogue.listProducts()

            elif choice == "2":
                self._addToCart()

            elif choice == "3":
                self.account._cartManager.viewCart()

            elif choice == "4":
                self._removeFromCart()

            elif choice == "5":
                self._checkout()

            elif choice == "6":
                self._viewOrders()

            elif choice == "7":
                print("Logging out of Customer Menu.\n")
                break

            else:
                print("Invalid option. Please choose 1–7.\n")

    def _addToCart(self):
        """
        Prompts for product ID & quantity, then adds to this customer's cart.
        """
        try:
            pid = int(input("Enter product ID: ").strip())
            qty = int(input("Enter quantity: ").strip())
        except ValueError:
            print("ID and quantity must be integers.\n")
            return

        product = self.catalogue.getProductById(pid)
        if not product:
            print("Product not found.\n")
            return

        msg = self.account._cartManager.addToCart(product, qty)
        print(msg + "\n")

    def _removeFromCart(self):
        """
        Prompts for product ID, then removes it from the cart if present.
        """
        try:
            pid = int(input("Enter product ID to remove: ").strip())
        except ValueError:
            print("Product ID must be an integer.\n")
            return

        self.account._cartManager.removeFromCart(pid)
        print("If that item was in your cart, it’s been removed.\n")

    def _checkout(self):
        """
        Prompts for address and attempts to checkout.
        """
        address = input("Enter your delivery address: ").strip()
        try:
            self.account._cartManager.checkout(self.account.username, address)
            print("")  # blank line after confirmation
        except Exception as e:
            print(f"Checkout failed: {e}\n")

    def _viewOrders(self):
        """
        Displays all past orders for this customer.
        """
        try:
            OrderManager.displayOrders(self.account)
            print("")  # blank line after listing
        except Exception as e:
            print(f"Failed to retrieve orders: {e}\n")
