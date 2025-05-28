import pytest
from models.user import User, Admin, Cashier
from models.product import Product, Category

def test_user_creation():
    user = User("testuser", "password123")
    assert user.username == "testuser"
    assert user.password == "password123"

def test_admin_creation():
    admin = Admin("admin", "admin123")
    assert admin.username == "admin"
    assert admin.password == "admin123"

def test_cashier_creation():
    cashier = Cashier("john", "john123", 1)
    assert cashier.username == "john"
    assert cashier.password == "john123"
    assert cashier.cashier_id == 1

def test_category_creation():
    category = Category("Electronics", "Electronic items")
    assert category.name == "Electronics"
    assert category.description == "Electronic items"
    assert len(category.products) == 0

def test_product_creation():
    category = Category("Electronics")
    product = Product("Laptop", 999.99, category, 10)
    assert product.name == "Laptop"
    assert product.price == 999.99
    assert product.category == category
    assert product.stock == 10

def test_product_stock_update():
    product = Product("Laptop", 999.99, Category("Electronics"), 10)
    product.update_stock(5)
    assert product.stock == 15
    product.update_stock(-3)
    assert product.stock == 12

def test_negative_stock_error():
    product = Product("Laptop", 999.99, Category("Electronics"), 10)
    with pytest.raises(ValueError) as exc_info:
        product.update_stock(-15)
    assert str(exc_info.value) == "Stock cannot be negative" 