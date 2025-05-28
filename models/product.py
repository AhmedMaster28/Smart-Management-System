class Category:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self.products = []

class Product:
    def __init__(self, name, price, category, stock=0):
        self.name = name
        self.price = price
        self.category = category
        self.stock = stock

    def update_stock(self, quantity):
        self.stock += quantity
        if self.stock < 0:
            raise ValueError("Stock cannot be negative") 