import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from utils.data_manager import DataManager
from utils.styles import AppStyles
from views.admin_panel import AdminPanel
from views.cashier_panel import CashierPanel
from scripts.init_data import main as init_data

class SmartMartSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Smart Mart Management System")
        self.root.geometry("1024x768")
        
        # Initialize data files if they don't exist
        if not os.path.exists("data") or not os.path.exists("data/admin.txt"):
            init_data()
        
        # Apply custom styles
        AppStyles.apply_styles(self.root)
        
        # Initialize data manager
        self.data_manager = DataManager()
        
        # Set up the main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create and show the login screen
        self.show_login_screen()
        
    def show_login_screen(self):
        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        # Create main container with padding
        container = ttk.Frame(self.main_frame, style="Card.TFrame")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create login frame
        login_frame = ttk.Frame(container, style="Card.TFrame")
        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Title with custom font
        title_label = AppStyles.create_section_label(login_frame, "Smart Mart Login")
        title_label.pack(pady=(20, 30))
        
        # Username frame with icon
        username_frame = ttk.Frame(login_frame)
        username_frame.pack(fill=tk.X, padx=30, pady=5)
        
        username_label = ttk.Label(username_frame, text="👤 Username:", font=("Helvetica", 12))
        username_label.pack(side=tk.LEFT)
        
        self.username_entry = ttk.Entry(username_frame, width=30, font=("Helvetica", 12))
        self.username_entry.pack(side=tk.LEFT, padx=10)
        
        # Password frame with icon
        password_frame = ttk.Frame(login_frame)
        password_frame.pack(fill=tk.X, padx=30, pady=5)
        
        password_label = ttk.Label(password_frame, text="🔒 Password:", font=("Helvetica", 12))
        password_label.pack(side=tk.LEFT)
        
        self.password_entry = ttk.Entry(password_frame, show="●", width=30, font=("Helvetica", 12))
        self.password_entry.pack(side=tk.LEFT, padx=10)
        
        # Login button with hover effect
        login_button = AppStyles.create_rounded_button(login_frame, "Login", self.handle_login)
        login_button.pack(pady=30)
        
        # Add some helpful text
        hint_text = "Default Admin Login:\nUsername: admin\nPassword: admin123"
        hint_label = ttk.Label(login_frame, text=hint_text, 
                             font=("Helvetica", 10), foreground=AppStyles.SECONDARY_COLOR)
        hint_label.pack(pady=(0, 20))
        
    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        # Check admin credentials
        admin_data = self.data_manager.load_data("admin")
        if username == admin_data["username"] and password == admin_data["password"]:
            self.show_admin_panel()
            return
            
        # Check cashier credentials
        cashiers = self.data_manager.load_data("cashiers")
        for cashier in cashiers:
            if username == cashier["username"] and password == cashier["password"]:
                self.show_cashier_panel(cashier)
                return
                
        messagebox.showerror("Error", "Invalid username or password")
        
    def show_admin_panel(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Create and show admin panel
        AdminPanel(self.main_frame, self.data_manager, self.show_login_screen)
        
    def show_cashier_panel(self, cashier_data):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        # Create and show cashier panel
        CashierPanel(self.main_frame, self.data_manager, cashier_data, self.show_login_screen)
        
    def run(self):
        # Center the window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        self.root.mainloop()

if __name__ == "__main__":
    app = SmartMartSystem()
    app.run() 