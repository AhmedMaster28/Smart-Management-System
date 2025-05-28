import pytest
import os
import json
from pathlib import Path
from utils.data_manager import DataManager

@pytest.fixture
def data_manager():
    # Create a test data manager
    dm = DataManager()
    yield dm
    # Cleanup test files after tests
    for file_path in dm.files.values():
        if file_path.exists():
            file_path.unlink()
    if dm.base_path.exists():
        dm.base_path.rmdir()

def test_initialization(data_manager):
    """Test that DataManager initializes correctly with required files"""
    assert data_manager.base_path.exists()
    assert data_manager.files["admin"].exists()
    assert data_manager.files["products"].exists()
    assert data_manager.files["cashiers"].exists()
    assert data_manager.files["bills"].exists()

def test_admin_credentials(data_manager):
    """Test that default admin credentials are created correctly"""
    admin_data = data_manager.load_data("admin")
    assert admin_data["username"] == "admin"
    assert admin_data["password"] == "admin123"

def test_save_and_load_data(data_manager):
    """Test saving and loading data"""
    test_data = {"test": "data"}
    data_manager.save_data("products", test_data)
    loaded_data = data_manager.load_data("products")
    assert loaded_data == test_data

def test_append_bill(data_manager):
    """Test appending bills"""
    # Add two bills
    data_manager.append_bill(100.50)
    data_manager.append_bill(200.75)
    
    # Load bills and verify
    bills = data_manager.load_data("bills")
    assert len(bills) == 2
    assert bills[0]["bill_number"] == 1
    assert bills[0]["amount"] == 100.50
    assert bills[1]["bill_number"] == 2
    assert bills[1]["amount"] == 200.75

def test_load_nonexistent_file(data_manager):
    """Test loading data from a non-existent file returns empty list"""
    # Delete the products file
    data_manager.files["products"].unlink()
    assert data_manager.load_data("products") == []

def test_invalid_json_file(data_manager):
    """Test loading corrupted JSON file returns empty list"""
    # Write invalid JSON to file
    with open(data_manager.files["products"], 'w') as f:
        f.write("invalid json data")
    assert data_manager.load_data("products") == [] 