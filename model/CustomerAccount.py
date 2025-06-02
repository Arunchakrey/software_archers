from model.IAccount import IAccount
from model.Cart import Cart

class CustomerAccount(IAccount):
    def __init__(self, username, password, email):
        self._username = username
        self._password = password
        self._email = email
        self._cart = Cart()

    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, value):
        if not value:
            raise ValueError("Username can not be empty.")
        self._username = value

    def change_password(self, new_password):
        self._password = new_password
        print("Customer password updated")

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        self.email = value

    def display_info(self):
        print(f"Customer: {self._username}, Email: {self._email}")