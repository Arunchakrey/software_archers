from model.CustomerAccount import CustomerAccount
from model.AdminAccount import AdminAccount
from services.Authenticator import Authenticator
from reader.AccountReader import AccountReader
from services.Catalogue import Catalogue
from CLI.AdminMenu import AdminMenu
from CLI.CustomerMenu import CustomerMenu

FILENAME = "data/accounts.json"
PRODUCTS_FILENAME = "data/products.json"

def main():
    account_reader = AccountReader(FILENAME)
    accounts = account_reader.read_accounts()

    # Note: Authenticator’s constructor expects (list_of_accounts, account_reader)
    login_processor = Authenticator(accounts, account_reader)

    while True:
        print("\n=== Welcome to AWE Electronics ===")
        print("1. Login")
        print("2. Sign Up")
        print("3. Exit")

        choice = input("Select an option: ").strip()
        if choice == "1":
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            account = login_processor.authenticate(username, password)

            if not account:
                print("Login failed. Invalid credentials.\n")
                continue

            # Show basic “you’re logged in” info
            account.display_info()

            # Always load the latest catalogue
            catalogue = Catalogue()
            catalogue.loadFromFile(PRODUCTS_FILENAME)

            # Dispatch to the correct menu
            if isinstance(account, AdminAccount):
                AdminMenu(account, catalogue, PRODUCTS_FILENAME).run()

            elif isinstance(account, CustomerAccount):
                CustomerMenu(account, catalogue).run()

            else:
                print("Unknown account type.\n")

        elif choice == "2":
            login_processor.signup()

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1, 2, or 3.\n")

if __name__ == "__main__":
    main()
