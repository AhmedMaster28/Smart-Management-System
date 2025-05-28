# Smart Mart Management System

A Python-based retail management system with separate interfaces for administrators and cashiers.

## Features

### Admin Panel
- Manage product categories and products
- Add, update, and delete cashier accounts
- Monitor and update product stock levels
- View all registered cashiers

### Cashier Panel
- Browse products by category
- Add items to shopping cart
- Process payments (Cash/Card)
- Apply automatic 10% discount for card payments
- Generate and store bills

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/smart-mart-management.git
cd smart-mart-management
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python main.py
```

2. Login credentials:
   - Admin:
     - Username: admin
     - Password: admin123
   - Cashiers:
     - Created by admin

## Data Storage

The system uses text files to store data:
- `data/products.txt`: Product and category information
- `data/cashiers.txt`: Cashier account details
- `data/admin.txt`: Admin credentials
- `data/bills.txt`: Transaction records

## Development

### Project Structure
```
smart-mart-management/
├── main.py
├── requirements.txt
├── README.md
├── models/
│   ├── user.py
│   └── product.py
├── views/
│   ├── admin_panel.py
│   └── cashier_panel.py
└── utils/
    └── data_manager.py
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 