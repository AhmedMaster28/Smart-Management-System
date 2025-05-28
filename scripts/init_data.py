import os
import json

def ensure_data_directory():
    """Create data directory if it doesn't exist"""
    if not os.path.exists("data"):
        os.makedirs("data")

def init_admin():
    """Initialize admin credentials"""
    admin_data = {
        "username": "admin",
        "password": "admin123"
    }
    with open("data/admin.txt", "w") as f:
        json.dump(admin_data, f, indent=4)

def init_cashiers():
    """Initialize sample cashier accounts"""
    cashiers = [
        {"id": 1, "username": "john", "password": "john123"},
        {"id": 2, "username": "emma", "password": "emma123"},
        {"id": 3, "username": "mike", "password": "mike123"}
    ]
    with open("data/cashiers.txt", "w") as f:
        json.dump(cashiers, f, indent=4)

def init_products():
    """Initialize sample products in different categories"""
    categories = [
        {
            "name": "Electronics",
            "products": [
                {"name": "Laptop", "price": 999.99, "stock": 10},
                {"name": "Smartphone", "price": 599.99, "stock": 15},
                {"name": "Tablet", "price": 299.99, "stock": 8},
                {"name": "Headphones", "price": 79.99, "stock": 20},
                {"name": "Smart Watch", "price": 199.99, "stock": 12}
            ]
        },
        {
            "name": "Groceries",
            "products": [
                {"name": "Bread", "price": 2.99, "stock": 50},
                {"name": "Milk", "price": 3.99, "stock": 40},
                {"name": "Eggs", "price": 4.99, "stock": 30},
                {"name": "Cheese", "price": 5.99, "stock": 25},
                {"name": "Fruits Pack", "price": 9.99, "stock": 20}
            ]
        },
        {
            "name": "Clothing",
            "products": [
                {"name": "T-Shirt", "price": 19.99, "stock": 30},
                {"name": "Jeans", "price": 49.99, "stock": 25},
                {"name": "Jacket", "price": 79.99, "stock": 15},
                {"name": "Sneakers", "price": 89.99, "stock": 20},
                {"name": "Hat", "price": 24.99, "stock": 35}
            ]
        },
        {
            "name": "Home & Living",
            "products": [
                {"name": "Bed Sheet", "price": 29.99, "stock": 20},
                {"name": "Pillow", "price": 19.99, "stock": 30},
                {"name": "Towel Set", "price": 24.99, "stock": 25},
                {"name": "Lamp", "price": 39.99, "stock": 15},
                {"name": "Mirror", "price": 49.99, "stock": 10}
            ]
        },
        {
            "name": "Books",
            "products": [
                {"name": "Novel", "price": 14.99, "stock": 40},
                {"name": "Cookbook", "price": 24.99, "stock": 25},
                {"name": "Self-Help", "price": 19.99, "stock": 30},
                {"name": "Technical", "price": 49.99, "stock": 20},
                {"name": "Children's Book", "price": 9.99, "stock": 35}
            ]
        }
    ]
    with open("data/products.txt", "w") as f:
        json.dump(categories, f, indent=4)

def init_bills():
    """Initialize empty bills list"""
    with open("data/bills.txt", "w") as f:
        json.dump([], f, indent=4)

def main():
    """Initialize all data files"""
    print("Initializing Smart Mart Management System data...")
    
    # Create data directory
    ensure_data_directory()
    
    # Initialize all data files
    init_admin()
    init_cashiers()
    init_products()
    init_bills()
    
    print("Data initialization complete!")
    print("\nDefault login credentials:")
    print("Admin:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\nSample Cashiers:")
    print("1. john/john123")
    print("2. emma/emma123")
    print("3. mike/mike123")

if __name__ == "__main__":
    main() 