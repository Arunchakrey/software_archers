from model.CustomerAccount import CustomerAccount
from services.Catalogue import Catalogue
from manager.OrderManager import OrderManager

class CustomerMenu:
    """
    Handles the interactive loop for a CustomerAccount.
    """

    def __init__(self, account: CustomerAccount, catalogue: Catalogue):
        self._account = account
        self._catalogue = catalogue

    def run(self):
        """
        Runs the customer menu loop until the customer chooses to log out.
        """
        print(f"\nWelcome, {self._account._username}! (Customer Mode)\n")

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
                self._catalogue.listProducts()
            elif choice == "2":
                self.addToCart()
            elif choice == "3":
                self._account._cartManager.viewCart()
            elif choice == "4":
                self.removeFromCart()
            elif choice == "5":
                self.checkout()
            elif choice == "6":
                self.viewOrders()
            elif choice == "7":
                print("Logging out of Customer Menu.\n")
                break
            else:
                print("Invalid option. Please choose 1–7.\n")

    def addToCart(self):
        """
        Prompts for product ID & quantity, then adds to this customer's cart.
        """
        try:
            productId = int(input("Enter product ID: ").strip())
            quantity = int(input("Enter quantity: ").strip())
        except ValueError:
            print("ID and quantity must be integers.\n")
            return

        product = self._catalogue.getProductById(productId)
        if not product:
            print("Product not found.\n")
            return

        msg = self._account._cartManager.addToCart(product, quantity)
        print(msg + "\n")

    def removeFromCart(self):
        """
        Prompts for product ID, then removes it from the cart if present.
        """
        try:
            productId = int(input("Enter product ID to remove: ").strip())
        except ValueError:
            print("Product ID must be an integer.\n")
            return

        self._account._cartManager.removeFromCart(productId)
        print("If that item was in your cart, it’s been removed.\n")

    def checkout(self):
        """
        Prompts for address and attempts to checkout.
        """
        address = input("Enter your delivery address: ").strip()
        try:
            self._account._cartManager.checkout(self._account._username, address)
            print("")
        except Exception as e:
            print(f"Checkout failed: {e}\n")

    def viewOrders(self):
        """
        Displays all past orders for this customer.
        """
        try:
            OrderManager.displayOrders(self._account)
            print("")
        except Exception as e:
            print(f"Failed to retrieve orders: {e}\n")
