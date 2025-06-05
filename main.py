from model.CustomerAccount import CustomerAccount
from model.AdminAccount import AdminAccount
from services.Authenticator import Authenticator
from reader.AccountReader import AccountReader
from services.Catalogue import Catalogue
from CLI.AdminMenu import AdminMenu
from CLI.CustomerMenu import CustomerMenu

ACCOUNTS_FILE = "data/accounts.json"
PRODUCTS_FILE = "data/products.json"

def main():
    # Load account data and initialize authenticator
    accountReader = AccountReader(ACCOUNTS_FILE)
    accounts = accountReader.readAccounts()
    authenticator = Authenticator(accounts, accountReader)

    while True:
        print("\n=== Welcome to AWE Electronics ===")
        print("1. Login")
        print("2. Sign Up")
        print("3. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            account = authenticator.authenticate(username, password)

            if not account:
                print("Login failed. Invalid credentials.\n")
                continue

            account.displayInfo()

            # Load the latest catalogue
            catalogue = Catalogue()
            catalogue.loadFromFile(PRODUCTS_FILE)

            if isinstance(account, AdminAccount):
                AdminMenu(account, catalogue, PRODUCTS_FILE).run()
            elif isinstance(account, CustomerAccount):
                CustomerMenu(account, catalogue).run()
            else:
                print("Unknown account type.\n")

        elif choice == "2":
            authenticator.signUp()

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1, 2, or 3.\n")

if __name__ == "__main__":
    main()
