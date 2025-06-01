from IAccount import IAccount   

class AdminAccount(IAccount):
    def __init__(self, username, password, access_level):
        self._username = username
        self._password = password
        self._access_level = access_level

    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, value):
        self._username = value

    def change_password(self, new_password):
        self._password = new_password

    @property
    def access_level(self):
        return self._access_level

    @access_level.setter
    def access_level(self, value):
        self._access_level = value

    def display_info(self):
        print(f"Admin: {self._username}, Access Level: {self._access_level}")

    