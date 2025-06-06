from model.CustomerAccount import CustomerAccount

class Authenticator:
    def __init__(self, accounts, accountReader):
        """
        accounts: list of IAccount instances (either customer's or admin's )
        """
        self._accounts = accounts
        self._accountReader = accountReader

    def authenticate(self, username, password):
        """
        Returns the account if credentials are correct, else None.
        """
        for acc in self._accounts:
            # For demo: directly accessing _username/_password (could use getters/setters or make a check_password method)
            if acc._username == username and acc._password == password:
                print(f"Login successful: {username}")
                return acc
        print("Login failed.")
        return None
    
    def registerAccount(self, account):
        """
        Adds a new account. You may add duplicate-checking logic.
        """
        self._accounts.append(account)
        print(f"Account registered: {account.username}")

    def usernameExists(self, username):
        return any(acc.username == username for acc in self._accounts)

    def signUp(self):
        print("=== Sign Up ===")
        username = input("Username: ").strip()
        if self.usernameExists(username):
            print("Username already exists, please choose another.")
            return
        
        password = input("Password: ").strip()
        email = input("Email: ").strip()
        account = CustomerAccount(username, password, email)

        self._accounts.append(account)
        self._accountReader.appendAccount(account)
        print(f"Signup successful! welcome, {username}")

