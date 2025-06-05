from model.IAccount import IAccount
from manager.ProductManager import ProductManager
from services.Catalogue import Catalogue
from manager.StatisticsManager import StatisticsManager
from manager.OrderManager import OrderManager

class AdminAccount(IAccount):
    def __init__(self, username: str, password: str, catalogue: Catalogue):
        self._username = username
        self._password = password
        self._productManager = ProductManager(catalogue)
        self._statisticsManager = StatisticsManager()

    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, value):
        self._username = value

    def changePassword(self, new_password):
        self._password = new_password

    @property
    def access_level(self):
        return self._access_level

    @access_level.setter
    def access_level(self, value):
        self._access_level = value

    def displayInfo(self):
        print(f"Admin: {self._username}")
        
    def updateOrderStatus(self, orderId: int, choice: int):
        if choice == 1:
            orderStatus = "Incomplete"
        elif choice == 2:
            orderStatus = "Complete"
        else:
            return False

        # Try to update, and return the actual result
        success = OrderManager.updateOrderStatus(orderId, orderStatus)
        return success



    