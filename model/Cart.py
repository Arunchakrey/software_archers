from model.CartItem import CartItem
from typing import List

class Cart:
    def __init__(self):
        self._items: List[CartItem] = []
        
    def getTotal(self):
        return sum(item.getTotal() for item in self._items)