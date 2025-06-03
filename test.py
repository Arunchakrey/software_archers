from model.CustomerAccount import CustomerAccount
from model.AdminAccount import AdminAccount
from services.authenticator import Authenticator
from services.AccountReader import AccountReader
from services.Catalogue import Catalogue
# from services.CartManager import CartManager


FILENAME = "data/accounts.json"
account_reader = AccountReader(FILENAME)
accounts = account_reader.read_accounts()
login_processor = Authenticator(accounts, account_reader)

while True:
    print("\n=== Welcome ===")
    print("1. Login")
    print("2. Sign Up")
    print("3. Exit")
    choice = input("Select an option: ").strip()

    if choice == "1":
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        account = login_processor.authenticate(username, password)
        if account:
            account.display_info()
    
        if isinstance(account, AdminAccount):
            print("Welcome, admin")
            # (insert admin menu here if needed)
        
        elif isinstance(account, CustomerAccount):
            print(f"Welcome, {account.username}!")
            catalogue = Catalogue()
            catalogue.loadFromFile("data/products.json")
            
            while True:
                print("\n--- Customer Menu ---")
                print("1. View Products")
                print("2. Add Product to Cart")
                print("3. View Cart")
                print("4. Remove Item from Cart")
                print("5. Checkout")
                print("6. Logout")
                c_choice = input("Choose an option: ").strip()

                if c_choice == "1":
                    catalogue.listProducts()

                elif c_choice == "2":
                    try:
                        pid = int(input("Enter product ID: "))
                        qty = int(input("Enter quantity: "))
                        product = catalogue.getProductById(pid)
                        if product:
                            account._cartManager.addToCart(product, qty)
                        else:
                            print("Product not found.")
                    except ValueError:
                        print("Invalid input.")

                elif c_choice == "3":
                    account._cart.displayCart()

                elif c_choice == "4":
                    try:
                        pid = int(input("Enter product ID to remove: "))
                        account._cart.removeItem(pid)
                    except ValueError:
                        print("Invalid product ID.")

                elif c_choice == "5":
                    address = input("Enter your address: ")
                    try:
                        account._cartManager.checkout(account.username, address)
                    except Exception as e:
                        print(f"Checkout failed: {e}")

                elif c_choice == "6":
                    print("Logged out.")
                    break

                else:
                    print("Invalid option. Try again.")

    elif choice == "2":
        login_processor.signup()
    elif choice == "3":
        print("BYE")
        break
    else:
        print("Invalid Option")