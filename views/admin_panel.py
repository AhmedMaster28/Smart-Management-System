import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
from utils.styles import AppStyles

class AdminPanel:
    def __init__(self, parent, data_manager, logout_callback):
        self.parent = parent
        self.data_manager = data_manager
        self.logout_callback = logout_callback
        
        # Initialize variables
        self.category_var = tk.StringVar()
        self.stock_product_var = tk.StringVar()
        self.stock_quantity_var = tk.StringVar()
        
        # Initialize UI components
        self.category_combo = None
        self.product_tree = None
        self.cashier_tree = None
        self.stock_product_combo = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create main container
        self.main_frame = ttk.Frame(self.parent, style="Card.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        title_label = AppStyles.create_section_label(header_frame, "Admin Panel 👨‍💼")
        title_label.pack(side=tk.LEFT)
        
        logout_btn = AppStyles.create_rounded_button(
            header_frame, "Logout", self.logout_callback, width=15
        )
        logout_btn.pack(side=tk.RIGHT)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create tabs
        self.create_products_tab()
        self.create_cashiers_tab()
        self.create_reports_tab()
        
    def create_products_tab(self):
        products_frame = ttk.Frame(self.notebook)
        self.notebook.add(products_frame, text="Products 📦")
        
        # Left side - Categories and products
        left_frame = ttk.LabelFrame(products_frame, text="Manage Products", style="Card.TLabelframe")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Category management
        category_frame = ttk.LabelFrame(left_frame, text="Categories", style="Card.TLabelframe")
        category_frame.pack(fill=tk.X, padx=5, pady=5)
        
        category_controls = ttk.Frame(category_frame)
        category_controls.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(category_controls, text="📁 Category:").pack(side=tk.LEFT)
        self.category_combo = ttk.Combobox(category_controls, textvariable=self.category_var)
        self.category_combo.pack(side=tk.LEFT, padx=5)
        self.category_combo.bind("<<ComboboxSelected>>", self.load_products)
        
        # Category buttons
        cat_btn_frame = ttk.Frame(category_frame)
        cat_btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        AppStyles.create_rounded_button(
            cat_btn_frame, "➕ Add Category", self.add_category, width=15
        ).pack(side=tk.LEFT, padx=2)
        
        AppStyles.create_rounded_button(
            cat_btn_frame, "🗑️ Delete Category", self.delete_category, width=15
        ).pack(side=tk.LEFT, padx=2)
        
        # Product list
        product_list_frame = ttk.LabelFrame(left_frame, text="Products in Category", style="Card.TLabelframe")
        product_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.product_tree = ttk.Treeview(
            product_list_frame, 
            columns=("Name", "Price", "Stock"),
            show="headings",
            style="Treeview"
        )
        self.product_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        for col in ("Name", "Price", "Stock"):
            self.product_tree.heading(col, text=col)
            self.product_tree.column(col, width=100)
            
        # Add scrollbar
        scrollbar = ttk.Scrollbar(product_list_frame, orient=tk.VERTICAL, command=self.product_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.product_tree.configure(yscrollcommand=scrollbar.set)
        
        # Right side - Product details
        right_frame = ttk.LabelFrame(products_frame, text="Product Details", style="Card.TLabelframe")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)
        
        # Product form
        form_frame = ttk.Frame(right_frame)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Product name
        ttk.Label(form_frame, text="📝 Name:").pack(fill=tk.X, pady=2)
        self.product_name_var = tk.StringVar()
        self.product_name_entry = ttk.Entry(form_frame, textvariable=self.product_name_var)
        self.product_name_entry.pack(fill=tk.X, pady=2)
        
        # Product price
        ttk.Label(form_frame, text="💲 Price:").pack(fill=tk.X, pady=2)
        self.product_price_var = tk.StringVar()
        self.product_price_entry = ttk.Entry(form_frame, textvariable=self.product_price_var)
        self.product_price_entry.pack(fill=tk.X, pady=2)
        
        # Product stock
        ttk.Label(form_frame, text="📦 Stock:").pack(fill=tk.X, pady=2)
        self.product_stock_var = tk.StringVar()
        self.product_stock_entry = ttk.Entry(form_frame, textvariable=self.product_stock_var)
        self.product_stock_entry.pack(fill=tk.X, pady=2)
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        AppStyles.create_rounded_button(
            button_frame, "➕ Add Product", self.add_product, width=15
        ).pack(side=tk.LEFT, padx=2)
        
        AppStyles.create_rounded_button(
            button_frame, "✏️ Update", self.update_product, width=15
        ).pack(side=tk.LEFT, padx=2)
        
        AppStyles.create_rounded_button(
            button_frame, "🗑️ Delete", self.delete_product, width=15
        ).pack(side=tk.LEFT, padx=2)
        
        # Load initial data
        self.load_categories()
        
    def create_cashiers_tab(self):
        cashiers_frame = ttk.Frame(self.notebook)
        self.notebook.add(cashiers_frame, text="Cashiers 👥")
        
        # Left side - Cashier list
        left_frame = ttk.LabelFrame(cashiers_frame, text="Cashier List")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Cashier list
        self.cashier_tree = ttk.Treeview(
            left_frame,
            columns=("ID", "Username"),
            show="headings",
            style="Treeview"
        )
        self.cashier_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        for col in ("ID", "Username"):
            self.cashier_tree.heading(col, text=col)
            
        # Add scrollbar
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.cashier_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.cashier_tree.configure(yscrollcommand=scrollbar.set)
        
        # Right side - Cashier details
        right_frame = ttk.LabelFrame(cashiers_frame, text="Cashier Details")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)
        
        # Cashier form
        form_frame = ttk.Frame(right_frame)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Cashier ID
        ttk.Label(form_frame, text="ID:").pack(fill=tk.X, pady=2)
        self.cashier_id_var = tk.StringVar()
        self.cashier_id_entry = ttk.Entry(form_frame, textvariable=self.cashier_id_var)
        self.cashier_id_entry.pack(fill=tk.X, pady=2)
        
        # Cashier username
        ttk.Label(form_frame, text="Username:").pack(fill=tk.X, pady=2)
        self.cashier_username_var = tk.StringVar()
        self.cashier_username_entry = ttk.Entry(form_frame, textvariable=self.cashier_username_var)
        self.cashier_username_entry.pack(fill=tk.X, pady=2)
        
        # Cashier password
        ttk.Label(form_frame, text="Password:").pack(fill=tk.X, pady=2)
        self.cashier_password_var = tk.StringVar()
        self.cashier_password_entry = ttk.Entry(form_frame, textvariable=self.cashier_password_var, show="●")
        self.cashier_password_entry.pack(fill=tk.X, pady=2)
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        AppStyles.create_rounded_button(
            button_frame, "Add Cashier", self.add_cashier, width=15
        ).pack(side=tk.LEFT, padx=2)
        
        AppStyles.create_rounded_button(
            button_frame, "Update", self.update_cashier, width=15
        ).pack(side=tk.LEFT, padx=2)
        
        AppStyles.create_rounded_button(
            button_frame, "Delete", self.delete_cashier, width=15
        ).pack(side=tk.LEFT, padx=2)
        
        # Load initial data
        self.load_cashiers()
        
    def create_reports_tab(self):
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="Reports 📊")
        
        # Sales report
        report_frame = ttk.LabelFrame(reports_frame, text="Sales Report")
        report_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Bills list
        self.bills_tree = ttk.Treeview(
            report_frame,
            columns=("Bill #", "Subtotal", "Discount", "Total", "Payment", "Cashier"),
            show="headings",
            style="Treeview"
        )
        self.bills_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        for col in ("Bill #", "Subtotal", "Discount", "Total", "Payment", "Cashier"):
            self.bills_tree.heading(col, text=col)
            
        # Add scrollbar
        scrollbar = ttk.Scrollbar(report_frame, orient=tk.VERTICAL, command=self.bills_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.bills_tree.configure(yscrollcommand=scrollbar.set)
        
        # Summary frame
        summary_frame = ttk.Frame(report_frame)
        summary_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Total sales
        self.total_sales_var = tk.StringVar(value="Total Sales: $0.00")
        total_sales_label = ttk.Label(
            summary_frame,
            textvariable=self.total_sales_var,
            font=("Helvetica", 12, "bold")
        )
        total_sales_label.pack(side=tk.LEFT, padx=10)
        
        # Total discounts
        self.total_discounts_var = tk.StringVar(value="Total Discounts: $0.00")
        total_discounts_label = ttk.Label(
            summary_frame,
            textvariable=self.total_discounts_var,
            font=("Helvetica", 12),
            foreground=AppStyles.ACCENT_COLOR
        )
        total_discounts_label.pack(side=tk.RIGHT, padx=10)
        
        # Load initial data
        self.load_bills()
        
    def load_categories(self):
        products = self.data_manager.load_data("products")
        categories = [category["name"] for category in products]
        self.category_combo["values"] = categories
        if categories:
            self.category_combo.set(categories[0])
            self.load_products()
            
    def load_products(self, event=None):
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
            
        products = self.data_manager.load_data("products")
        selected_category = self.category_var.get()
        
        for category in products:
            if category["name"] == selected_category:
                for product in category["products"]:
                    self.product_tree.insert("", tk.END, values=(
                        product["name"],
                        f"${product['price']:.2f}",
                        product["stock"]
                    ))
                break
                
    def add_product(self):
        try:
            name = self.product_name_var.get()
            price = float(self.product_price_var.get())
            stock = int(self.product_stock_var.get())
            
            if not name:
                raise ValueError("Product name is required")
            if price <= 0:
                raise ValueError("Price must be positive")
            if stock < 0:
                raise ValueError("Stock cannot be negative")
                
            products = self.data_manager.load_data("products")
            selected_category = self.category_var.get()
            
            for category in products:
                if category["name"] == selected_category:
                    # Check if product already exists
                    if any(p["name"] == name for p in category["products"]):
                        raise ValueError("Product already exists")
                        
                    category["products"].append({
                        "name": name,
                        "price": price,
                        "stock": stock
                    })
                    break
                    
            self.data_manager.save_data("products", products)
            self.load_products()
            
            # Clear form
            self.product_name_var.set("")
            self.product_price_var.set("")
            self.product_stock_var.set("")
            
            messagebox.showinfo("Success", "Product added successfully!")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            
    def update_product(self):
        selection = self.product_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a product to update")
            return
            
        try:
            name = self.product_name_var.get()
            price = float(self.product_price_var.get())
            stock = int(self.product_stock_var.get())
            
            if not name:
                raise ValueError("Product name is required")
            if price <= 0:
                raise ValueError("Price must be positive")
            if stock < 0:
                raise ValueError("Stock cannot be negative")
                
            products = self.data_manager.load_data("products")
            selected_category = self.category_var.get()
            old_name = self.product_tree.item(selection[0])["values"][0]
            
            for category in products:
                if category["name"] == selected_category:
                    for product in category["products"]:
                        if product["name"] == old_name:
                            product["name"] = name
                            product["price"] = price
                            product["stock"] = stock
                            break
                    break
                    
            self.data_manager.save_data("products", products)
            self.load_products()
            
            # Clear form
            self.product_name_var.set("")
            self.product_price_var.set("")
            self.product_stock_var.set("")
            
            messagebox.showinfo("Success", "Product updated successfully!")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            
    def delete_product(self):
        selection = self.product_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a product to delete")
            return
            
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this product?"):
            return
            
        product_name = self.product_tree.item(selection[0])["values"][0]
        products = self.data_manager.load_data("products")
        selected_category = self.category_var.get()
        
        for category in products:
            if category["name"] == selected_category:
                category["products"] = [p for p in category["products"] if p["name"] != product_name]
                break
                
        self.data_manager.save_data("products", products)
        self.load_products()
        
        # Clear form
        self.product_name_var.set("")
        self.product_price_var.set("")
        self.product_stock_var.set("")
        
        messagebox.showinfo("Success", "Product deleted successfully!")
        
    def load_cashiers(self):
        for item in self.cashier_tree.get_children():
            self.cashier_tree.delete(item)
            
        cashiers = self.data_manager.load_data("cashiers")
        for cashier in cashiers:
            self.cashier_tree.insert("", tk.END, values=(
                cashier["id"],
                cashier["username"]
            ))
            
    def add_cashier(self):
        try:
            cashier_id = int(self.cashier_id_var.get())
            username = self.cashier_username_var.get()
            password = self.cashier_password_var.get()
            
            if not username or not password:
                raise ValueError("Username and password are required")
                
            cashiers = self.data_manager.load_data("cashiers")
            
            # Check if ID or username already exists
            if any(c["id"] == cashier_id for c in cashiers):
                raise ValueError("Cashier ID already exists")
            if any(c["username"] == username for c in cashiers):
                raise ValueError("Username already exists")
                
            cashiers.append({
                "id": cashier_id,
                "username": username,
                "password": password
            })
            
            self.data_manager.save_data("cashiers", cashiers)
            self.load_cashiers()
            
            # Clear form
            self.cashier_id_var.set("")
            self.cashier_username_var.set("")
            self.cashier_password_var.set("")
            
            messagebox.showinfo("Success", "Cashier added successfully!")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            
    def update_cashier(self):
        selection = self.cashier_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a cashier to update")
            return
            
        try:
            cashier_id = int(self.cashier_id_var.get())
            username = self.cashier_username_var.get()
            password = self.cashier_password_var.get()
            
            if not username or not password:
                raise ValueError("Username and password are required")
                
            cashiers = self.data_manager.load_data("cashiers")
            old_id = int(self.cashier_tree.item(selection[0])["values"][0])
            
            # Update cashier
            for cashier in cashiers:
                if cashier["id"] == old_id:
                    cashier["id"] = cashier_id
                    cashier["username"] = username
                    cashier["password"] = password
                    break
                    
            self.data_manager.save_data("cashiers", cashiers)
            self.load_cashiers()
            
            # Clear form
            self.cashier_id_var.set("")
            self.cashier_username_var.set("")
            self.cashier_password_var.set("")
            
            messagebox.showinfo("Success", "Cashier updated successfully!")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            
    def delete_cashier(self):
        selection = self.cashier_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a cashier to delete")
            return
            
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this cashier?"):
            return
            
        cashier_id = int(self.cashier_tree.item(selection[0])["values"][0])
        cashiers = self.data_manager.load_data("cashiers")
        
        cashiers = [c for c in cashiers if c["id"] != cashier_id]
        self.data_manager.save_data("cashiers", cashiers)
        self.load_cashiers()
        
        # Clear form
        self.cashier_id_var.set("")
        self.cashier_username_var.set("")
        self.cashier_password_var.set("")
        
        messagebox.showinfo("Success", "Cashier deleted successfully!")
        
    def load_bills(self):
        for item in self.bills_tree.get_children():
            self.bills_tree.delete(item)
            
        bills = self.data_manager.load_data("bills")
        total_sales = 0
        total_discounts = 0
        
        for bill in bills:
            # Get cashier username
            cashiers = self.data_manager.load_data("cashiers")
            cashier_username = next(
                (c["username"] for c in cashiers if c["id"] == bill["cashier_id"]),
                "Unknown"
            )
            
            self.bills_tree.insert("", tk.END, values=(
                bill["bill_number"],
                f"${bill['subtotal']:.2f}",
                f"${bill['discount']:.2f}",
                f"${bill['total']:.2f}",
                bill["payment_method"].title(),
                cashier_username
            ))
            
            total_sales += bill["total"]
            total_discounts += bill["discount"]
            
        self.total_sales_var.set(f"Total Sales: ${total_sales:.2f}")
        self.total_discounts_var.set(f"Total Discounts: ${total_discounts:.2f}")
        
    def add_category(self):
        name = tk.simpledialog.askstring("Add Category", "Enter category name:")
        if name:
            if not name.strip():
                messagebox.showerror("Error", "Category name cannot be empty")
                return
                
            products = self.data_manager.load_data("products")
            
            # Check if category already exists
            if any(category["name"] == name for category in products):
                messagebox.showerror("Error", "Category already exists")
                return
                
            # Add new category
            products.append({
                "name": name,
                "products": []
            })
            
            self.data_manager.save_data("products", products)
            self.load_categories()
            messagebox.showinfo("Success", f"Category '{name}' added successfully!")
            
    def delete_category(self):
        if not self.category_var.get():
            messagebox.showerror("Error", "Please select a category to delete")
            return
            
        if not messagebox.askyesno("Confirm Delete", 
                                  f"Are you sure you want to delete the category '{self.category_var.get()}' and all its products?"):
            return
            
        products = self.data_manager.load_data("products")
        products = [cat for cat in products if cat["name"] != self.category_var.get()]
        
        self.data_manager.save_data("products", products)
        self.load_categories()
        messagebox.showinfo("Success", "Category deleted successfully!") 