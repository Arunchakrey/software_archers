from model.CustomerAccount import CustomerAccount
from model.AdminAccount import AdminAccount
from services.authenticator import Authenticator
from services.AccountReader import AccountReader


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
            else:
                print("Welcome")

    elif choice == "2":
        login_processor.signup()
    elif choice == "3":
        print("BYE")
        break
    else:
        print("Invalid Option")