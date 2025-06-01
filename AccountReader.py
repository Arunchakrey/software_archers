import json 
import os
from CustomerAccount import CustomerAccount
from AdminAccount import AdminAccount

class AccountReader:
    def __init__(self, filename):
        self._filename = filename

    def read_accounts(self):
        accounts = []
        if not os.path.exists(self._filename):
            return accounts
        with open(self._filename, "r") as file:
            data = json.load(file)
            for entry in data:
                if entry["type"] == "customer":
                    accounts.append(CustomerAccount(entry["username"], entry["password"], entry["email"]))
                elif entry["type"] == "admin":
                    accounts.append(AdminAccount(entry["username"], entry["password"], entry["access_level"]))

        return accounts
    
    def append_account(self, account):
        data = []
        if os.path.exists(self._filename):
            with open(self._filename, "r") as file:
                data = json.load(file)

        if isinstance(account, CustomerAccount):
            entry = {
                "type": "customer",
                "username": account.username,
                "password": account._password,
                "email": account.email
            }

        elif isinstance(account, AdminAccount):
            entry = {
                "type": "admin",
                "username": account.username,
                "password": account._password,
                "access_level": account.access_level
            }

        data.append(entry)

        with open(self._filename, "w") as file:
            json.dump(data, file, indent=2)
