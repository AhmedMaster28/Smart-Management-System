import json
import os
from pathlib import Path

class DataManager:
    def __init__(self):
        self.base_path = Path("data")
        self.base_path.mkdir(exist_ok=True)
        
        # Initialize files if they don't exist
        self.files = {
            "products": self.base_path / "products.txt",
            "cashiers": self.base_path / "cashiers.txt",
            "admin": self.base_path / "admin.txt",
            "bills": self.base_path / "bills.txt"
        }
        
        self._initialize_files()
        
    def _initialize_files(self):
        # Create default admin credentials if not exists
        if not self.files["admin"].exists():
            self.save_data("admin", {"username": "admin", "password": "admin123"})
            
        # Initialize other files if they don't exist
        for file_path in self.files.values():
            if not file_path.exists():
                self.save_data(file_path.stem, [])
    
    def load_data(self, file_type):
        try:
            with open(self.files[file_type], 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []
    
    def save_data(self, file_type, data):
        with open(self.files[file_type], 'w') as file:
            json.dump(data, file, indent=4)
    
    def append_bill(self, amount):
        bills = self.load_data("bills")
        bill_number = len(bills) + 1
        bills.append({"bill_number": bill_number, "amount": amount})
        self.save_data("bills", bills) 