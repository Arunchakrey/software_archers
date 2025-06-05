from model.CustomerAccount import CustomerAccount
from model.AdminAccount import AdminAccount
from services.Authenticator import Authenticator
from reader.AccountReader import AccountReader
from services.Catalogue import Catalogue
from manager.ProductManager import ProductManager
from manager.OrderManager import OrderManager


FILENAME = "data/accounts.json"
PRODUCTS_FILENAME = "data/products.json"
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
            catalogue = Catalogue()
            catalogue.loadFromFile("data/products.json")
    
        # Admin Logic Loop
        if isinstance(account, AdminAccount):
            print("Welcome, Sir Admin!!!. It's been too long since we last saw you...")

            while True:
                print("\n--- Admin Menu---")
                print("1. View Products")
                print("2. Edit Products")
                print("3. Generate Statistics")
                print("4. Manage Shipment Status")
                print("5. log out")
                a_choice = input("Choose an option: ").strip()

                if a_choice == "1":
                    catalogue.listProducts()
                
                elif a_choice == "2":
                    print("")
                    print("1. View Products")
                    print("2. Register New Product")
                    print("3. Update Product Quantity")
                    print("4. Update Price")
                    print("5. Return")
                    e_choice = input("Choose and option: ").strip()

                    if e_choice == "1":
                        catalogue.listProducts()
                        pass
                    
                    elif e_choice == "2":
                        try:
                            p_id = account.product_manager.get_next_id(PRODUCTS_FILENAME)
                            p_name = input("Enter Product Name: ").strip()
                            p_price = int(input("Enter Product's Price: ").strip())
                            p_quantity = float(input("Enter Product's Quantity: ").strip())
                            p_description = input("Enter Product's description: ").strip()
                            account.product_manager.registerProduct(p_id, p_name, p_price, p_quantity, p_description)
                            catalogue.listProducts()
                        except ValueError:
                            print("Entry is empty")

                    elif e_choice == "3":
                        try:
                            catalogue.listProducts()
                            p_id = input("Enter Product ID: ").strip()
                            p_quantity = input("Enter Product's Quantity: ").strip()
                            account.product_manager.updateQuantity(p_id, p_quantity)
                        except ValueError:
                            print("Invalid quantity or ID")
                            
                    elif e_choice == "4":
                        try:
                            catalogue.listProducts()
                            p_id = input("Enter Product ID: ").strip()
                            p_price = float(input("Enter Product's Price: ").strip())
                            account.product_manager.updatePrice(p_id, p_price)
                        except ValueError:
                            print("Invalid Price or ID")

                    elif e_choice == "5":
                        continue

                    else:
                        print("Invalid Option, try again.")

                elif a_choice == "3":
                    try:
                        startDate = input('Enter the start date (format: YYYY-MM-DD):')
                        endDate = input('Enter the end date (format: YYYY-MM-DD):')
                        account.generate_sales_report(startDate, endDate)
                    except ValueError:
                        print("Wrong input")
                elif a_choice == "4":
                    # try:
                        orderId = int(input("Enter orderId to edit: ").strip())
                        print("")
                        print("1. Update Status to 'Incomplete'")
                        print("2. Update Status to 'Complete'")
                        choice = int(input("Choose option: "))
                        account.updateOrderStatus(orderId, choice)
                    # except Exception as e:
                    #     print("Fail to update with:" )
                
                elif a_choice == "5":
                    break

        elif isinstance(account, CustomerAccount):
            print(f"Welcome, {account.username}!")
            
            while True:
                print("\n--- Customer Menu ---")
                print("1. View Products")
                print("2. Add Product to Cart")
                print("3. View Cart")
                print("4. Remove Item from Cart")
                print("5. Checkout")
                print("6. View orders")
                print("7. Logout")
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
                    account._cartManager.viewCart()

                elif c_choice == "4":
                    try:
                        pid = int(input("Enter product ID to remove: "))
                        account._cartManager.removeFromCart(pid)
                    except ValueError:
                        print("Invalid product ID.")

                elif c_choice == "5":
                    address = str(input("Enter your address: ")).strip()
                    try:
                        account._cartManager.checkout(account.username, address)
                    except Exception as e:
                        print(f"Checkout failed: {e}")
                
                elif c_choice == "6":
                    try:
                        OrderManager.displayOrders(account)
                    except Exception as e:
                         print(f"Failed to retrieve orders: {e}")

                elif c_choice == "7":
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