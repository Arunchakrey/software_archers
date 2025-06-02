from model.Cart import Cart
from model.Product import Product

# initialise products (self, id, name, price, quantity, description):
computer= Product(1, "Computer 1", 100, 5, "Black, Fast, Mobile")
phone = Product(2, "Iphone 10", 200, 10, "Silver, Sleek, Heavy")
chair = Product(3, "Gaming Chair", 50, 3, "Comfortable")

#Cart
cart_1 = Cart()

cart_1.addItem(computer, 1)
cart_1.addItem(phone, 1)
cart_1.addItem(chair, 1)

cart_1.removeItem(1)

cart_1.displayCart()

cart_1.checkOut(2)
