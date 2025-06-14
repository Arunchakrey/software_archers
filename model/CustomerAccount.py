from model.IAccount import IAccount
from manager.CartManager import CartManager
from model.Cart import Cart

class CustomerAccount(IAccount):
    def __init__(self, username, password, email):
        self._username = username
        self._password = password
        self._email = email
        self._cart = Cart()
        self._cartManager = CartManager(self._cart)

    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, value):
        if not value:
            raise ValueError("Username can not be empty.")
        self._username = value

    def changePassword(self, new_password):
        self._password = new_password
        print("Customer password updated")

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        self.email = value

    def displayInfo(self):
        print(f"Customer: {self._username}, Email: {self._email}")