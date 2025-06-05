from model.IAccount import IAccount
from manager.ProductManager import ProductManager
from services.Catalogue import Catalogue
from manager.StatisticsManager import StatisticsManager
from manager.OrderManager import OrderManager

class AdminAccount(IAccount):
    def __init__(self, username, password, catalogue):
        self._username = username
        self._password = password
        self.product_manager = ProductManager(catalogue)
        self.statistics_manager = StatisticsManager()

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
        print(f"Admin: {self._username}")
        
    """ Functions for handling products
    """
        
    def register_product(self, *args, **kwargs):
        self.product_manager.register_product(*args, **kwargs)

    def update_product_price(self, product_id, new_price):
        self.product_manager.update_price(product_id, new_price)

    def update_product_quantity(self, product_id, new_quantity):
        self.product_manager.update_quantity(product_id, new_quantity)

    def generate_sales_report(self, start_date: str, end_date: str, top_n: int = None):
        self.statistics_manager.generateStatistics(start_date, end_date, top_n)
        
    def updateOrderStatus(self, orderId: int, choice: int):
        if choice == 1:
            orderStatus = "Incomplete"
            OrderManager.updateOrderStatus(orderId, orderStatus)
        elif choice == 2:
            orderStatus = "Complete"
            OrderManager.updateOrderStatus(orderId, orderStatus)
        else:
            return "invalid choice"


    