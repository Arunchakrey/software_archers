from CustomerAccount import CustomerAccount


class Authenticator:
    def __init__(self, accounts, account_reader):
        """
        accounts: list of IAccount instances (either customer's or admin's )
        """
        self._accounts = accounts
        self.account_reader = account_reader

    def authenticate(self, username, password):
        """
        Returns the account if credentials are correct, else None.
        """
        for acc in self._accounts:
            # For demo: directly accessing _username/_password (could use getters/setters or make a check_password method)
            if acc.username == username and acc._password == password:
                print(f"Login successful: {username}")
                return acc
        print("Login failed.")
        return None
    
    def register_account(self, account):
        """
        Adds a new account. You may add duplicate-checking logic.
        """
        self._accounts.append(account)
        print(f"Account registered: {account.username}")

    def username_exists(self, username):
        return any(acc.username == username for acc in self._accounts)

    def signup(self):
        print("=== Sign Up ===")
        user_type = "1"

        username = input("Username: ").strip()
        if self.username_exists(username):
            print("Username already exists, please choose another.")
            return
        
        password = input("Password: ").strip()
        email = input("Email: ").strip()
        account = CustomerAccount(username, password, email)

        self._accounts.append(account)
        self.account_reader.append_account(account)
        print(f"Signup successful! welcome, {username}")

