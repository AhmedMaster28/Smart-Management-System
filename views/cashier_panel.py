import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from utils.styles import AppStyles

class CashierPanel:
    def __init__(self, parent, data_manager, cashier_data, logout_callback):
        self.parent = parent
        self.data_manager = data_manager
        self.cashier_data = cashier_data
        self.logout_callback = logout_callback
        self.cart = []
        
        # Initialize discount rates
        self.CARD_BASE_DISCOUNT = 0.10  # 10% base discount
        self.BULK_DISCOUNT_THRESHOLD = 1000  # Bulk purchase threshold
        self.BULK_DISCOUNT_RATE = 0.05  # Additional 5% for bulk purchases
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create main container
        self.main_frame = ttk.Frame(self.parent, style="Card.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header with gradient effect
        header_frame = ttk.Frame(self.main_frame, style="Card.TFrame")
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        title_label = AppStyles.create_section_label(
            header_frame, 
            f"Welcome, {self.cashier_data['username']}! 🛍️"
        )
        title_label.pack(side=tk.LEFT)
        
        logout_btn = AppStyles.create_rounded_button(
            header_frame, "🚪 Logout", self.logout_callback, width=15
        )
        logout_btn.pack(side=tk.RIGHT)
        
        # Create main content area
        content_frame = ttk.Frame(self.main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left side - Product selection
        left_frame = ttk.LabelFrame(content_frame, text="Browse Products", style="Card.TLabelframe")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Category selection with icon
        category_frame = ttk.Frame(left_frame)
        category_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(category_frame, text="📁 Category:").pack(side=tk.LEFT)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(category_frame, textvariable=self.category_var)
        self.category_combo.pack(side=tk.LEFT, padx=5)
        self.category_combo.bind("<<ComboboxSelected>>", self.load_products)
        
        # Product list with custom styling
        product_list_frame = ttk.LabelFrame(left_frame, text="Available Products", style="Card.TLabelframe")
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
            
        # Add to cart controls
        add_frame = ttk.LabelFrame(left_frame, text="Add to Cart", style="Card.TLabelframe")
        add_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(add_frame, text="🔢 Quantity:").pack(side=tk.LEFT, padx=5)
        self.quantity_var = tk.StringVar(value="1")
        quantity_entry = ttk.Entry(add_frame, textvariable=self.quantity_var, width=10)
        quantity_entry.pack(side=tk.LEFT, padx=5)
        
        add_btn = AppStyles.create_rounded_button(
            add_frame, "🛒 Add to Cart", self.add_to_cart, width=15
        )
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # Right side - Cart and payment
        right_frame = ttk.LabelFrame(content_frame, text="Shopping Cart 🛒", style="Card.TLabelframe")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Cart list
        cart_list_frame = ttk.Frame(right_frame)
        cart_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.cart_tree = ttk.Treeview(
            cart_list_frame, 
            columns=("Name", "Price", "Quantity", "Total"), 
            show="headings",
            style="Treeview"
        )
        self.cart_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        for col in ("Name", "Price", "Quantity", "Total"):
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=100)
            
        # Cart scrollbar
        cart_scrollbar = ttk.Scrollbar(cart_list_frame, orient=tk.VERTICAL, command=self.cart_tree.yview)
        cart_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.cart_tree.configure(yscrollcommand=cart_scrollbar.set)
            
        # Total and discount info
        total_frame = ttk.LabelFrame(right_frame, text="Order Summary", style="Card.TLabelframe")
        total_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.subtotal_var = tk.StringVar(value="Subtotal: $0.00")
        subtotal_label = ttk.Label(
            total_frame, 
            textvariable=self.subtotal_var,
            font=("Helvetica", 12)
        )
        subtotal_label.pack(fill=tk.X, padx=5, pady=2)
        
        self.discount_var = tk.StringVar(value="Discount: $0.00")
        discount_label = ttk.Label(
            total_frame, 
            textvariable=self.discount_var,
            font=("Helvetica", 12),
            foreground=AppStyles.ACCENT_COLOR
        )
        discount_label.pack(fill=tk.X, padx=5, pady=2)
        
        self.total_var = tk.StringVar(value="Total: $0.00")
        total_label = ttk.Label(
            total_frame, 
            textvariable=self.total_var,
            font=("Helvetica", 14, "bold"),
            foreground=AppStyles.PRIMARY_COLOR
        )
        total_label.pack(fill=tk.X, padx=5, pady=2)
        
        # Payment options
        payment_frame = ttk.LabelFrame(right_frame, text="Payment Method 💳", style="Card.TLabelframe")
        payment_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.payment_var = tk.StringVar(value="cash")
        ttk.Radiobutton(
            payment_frame, 
            text="💵 Cash Payment", 
            variable=self.payment_var,
            value="cash",
            command=self.update_cart_total
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Radiobutton(
            payment_frame, 
            text=f"💳 Card Payment (10% off + 5% bulk discount over ${self.BULK_DISCOUNT_THRESHOLD})", 
            variable=self.payment_var,
            value="card",
            command=self.update_cart_total
        ).pack(side=tk.LEFT, padx=10)
        
        # Action buttons
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        clear_btn = AppStyles.create_rounded_button(
            button_frame, "🗑️ Clear Cart", self.clear_cart, width=15
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        pay_btn = AppStyles.create_rounded_button(
            button_frame, "✅ Process Payment", self.process_payment, width=15
        )
        pay_btn.pack(side=tk.RIGHT, padx=5)
        
        # Load initial data
        self.load_categories()
        
    def calculate_discount(self, subtotal):
        """Calculate discount based on payment method and total amount"""
        if self.payment_var.get() == "card":
            # Base card discount
            discount = subtotal * self.CARD_BASE_DISCOUNT
            
            # Additional bulk purchase discount
            if subtotal >= self.BULK_DISCOUNT_THRESHOLD:
                discount += subtotal * self.BULK_DISCOUNT_RATE
                
            return discount
        return 0
        
    def update_cart_total(self):
        subtotal = 0
        for item in self.cart_tree.get_children():
            item_total = float(self.cart_tree.item(item)["values"][3].replace("$", ""))
            subtotal += item_total
            
        # Calculate discount
        discount = self.calculate_discount(subtotal)
        total = subtotal - discount
            
        # Update display
        self.subtotal_var.set(f"Subtotal: ${subtotal:.2f}")
        self.discount_var.set(f"Discount: -${discount:.2f}")
        self.total_var.set(f"Total: ${total:.2f}")
        
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
                
    def add_to_cart(self):
        selection = self.product_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a product")
            return
            
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
                
            product_values = self.product_tree.item(selection[0])["values"]
            product_name = product_values[0]
            product_price = float(product_values[1].replace("$", ""))
            available_stock = int(product_values[2])
            
            if quantity > available_stock:
                messagebox.showerror("Error", "Not enough stock available")
                return
                
            # Add to cart
            total = product_price * quantity
            self.cart_tree.insert("", tk.END, values=(
                product_name,
                f"${product_price:.2f}",
                quantity,
                f"${total:.2f}"
            ))
            
            # Update cart total
            self.update_cart_total()
            
            # Reset quantity
            self.quantity_var.set("1")
            
            # Show success message
            messagebox.showinfo("Success", f"Added {quantity} x {product_name} to cart")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            
    def clear_cart(self):
        if not self.cart_tree.get_children():
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to clear the cart?"):
            for item in self.cart_tree.get_children():
                self.cart_tree.delete(item)
            self.update_cart_total()
        
    def process_payment(self):
        if not self.cart_tree.get_children():
            messagebox.showerror("Error", "Cart is empty")
            return
            
        # Calculate final total
        total = float(self.total_var.get().replace("Total: $", ""))
        
        # Update product stock
        products = self.data_manager.load_data("products")
        for item in self.cart_tree.get_children():
            item_values = self.cart_tree.item(item)["values"]
            product_name = item_values[0]
            quantity = int(item_values[2])
            
            for category in products:
                for product in category["products"]:
                    if product["name"] == product_name:
                        product["stock"] -= quantity
                        break
                        
        self.data_manager.save_data("products", products)
        
        # Save bill
        bills = self.data_manager.load_data("bills")
        bill_number = len(bills) + 1
        
        # Get discount information
        subtotal = float(self.subtotal_var.get().replace("Subtotal: $", ""))
        discount = float(self.discount_var.get().replace("Discount: -$", ""))
        
        bills.append({
            "bill_number": bill_number,
            "subtotal": subtotal,
            "discount": discount,
            "total": total,
            "payment_method": self.payment_var.get(),
            "cashier_id": self.cashier_data["id"]
        })
        self.data_manager.save_data("bills", bills)
        
        # Show success message with discount details
        success_message = f"""Payment processed successfully!
        
Subtotal: ${subtotal:.2f}
Discount: -${discount:.2f}
Total Paid: ${total:.2f}

Payment Method: {self.payment_var.get().title()}
Bill Number: {bill_number}"""
        
        messagebox.showinfo("Success", success_message)
        
        # Clear cart
        self.clear_cart()
        
        # Reload products
        self.load_products() 