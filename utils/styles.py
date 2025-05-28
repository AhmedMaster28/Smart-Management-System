import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont

class AppStyles:
    # Modern Color scheme
    PRIMARY_COLOR = "#1a237e"  # Deep Blue
    SECONDARY_COLOR = "#0288d1"  # Light Blue
    ACCENT_COLOR = "#f50057"  # Pink
    SUCCESS_COLOR = "#00c853"  # Green
    WARNING_COLOR = "#ffd600"  # Yellow
    BACKGROUND_COLOR = "#f5f5f5"  # Light Gray
    CARD_BACKGROUND = "#ffffff"  # White
    TEXT_COLOR = "#263238"  # Dark Gray
    HEADER_COLOR = "#311b92"  # Deep Purple
    
    @staticmethod
    def apply_styles(root):
        # Configure the root window
        root.configure(bg=AppStyles.BACKGROUND_COLOR)
        
        # Create custom style
        style = ttk.Style()
        style.configure(".", 
                       background=AppStyles.BACKGROUND_COLOR,
                       foreground=AppStyles.TEXT_COLOR,
                       font=("Helvetica", 10))
        
        # Custom button style
        style.configure("Accent.TButton",
                       background=AppStyles.ACCENT_COLOR,
                       foreground="white",
                       padding=(10, 5),
                       font=("Helvetica", 10, "bold"))
        
        # Custom label style
        style.configure("Title.TLabel",
                       background=AppStyles.BACKGROUND_COLOR,
                       foreground=AppStyles.HEADER_COLOR,
                       font=("Helvetica", 24, "bold"),
                       padding=(0, 10))
        
        # Custom frame style
        style.configure("Card.TFrame",
                       background=AppStyles.CARD_BACKGROUND,
                       relief="raised",
                       borderwidth=1)
        
        # Custom labelframe style
        style.configure("Card.TLabelframe",
                       background=AppStyles.CARD_BACKGROUND,
                       foreground=AppStyles.PRIMARY_COLOR,
                       font=("Helvetica", 10, "bold"))
        
        style.configure("Card.TLabelframe.Label",
                       background=AppStyles.CARD_BACKGROUND,
                       foreground=AppStyles.PRIMARY_COLOR,
                       font=("Helvetica", 10, "bold"))
        
        # Custom treeview style
        style.configure("Treeview",
                       background=AppStyles.CARD_BACKGROUND,
                       foreground=AppStyles.TEXT_COLOR,
                       fieldbackground=AppStyles.CARD_BACKGROUND,
                       font=("Helvetica", 9))
        
        style.configure("Treeview.Heading",
                       background=AppStyles.PRIMARY_COLOR,
                       foreground="white",
                       font=("Helvetica", 10, "bold"))
        
        style.map("Treeview",
                 background=[("selected", AppStyles.SECONDARY_COLOR)],
                 foreground=[("selected", "white")])
        
        # Custom entry style
        style.configure("TEntry",
                       fieldbackground="white",
                       padding=(5, 2))
        
        # Custom combobox style
        style.configure("TCombobox",
                       fieldbackground="white",
                       padding=(5, 2))
        
        # Notebook style
        style.configure("TNotebook",
                       background=AppStyles.BACKGROUND_COLOR,
                       tabmargins=[2, 5, 2, 0])
        
        style.configure("TNotebook.Tab",
                       background=AppStyles.PRIMARY_COLOR,
                       foreground="white",
                       padding=[10, 2],
                       font=("Helvetica", 9, "bold"))
        
        # Configure selected tab
        style.map("TNotebook.Tab",
                 background=[("selected", AppStyles.SECONDARY_COLOR)],
                 foreground=[("selected", "white")])
        
    @staticmethod
    def create_rounded_button(parent, text, command, width=20):
        """Create a custom rounded button with hover effect"""
        button = tk.Button(parent, text=text, command=command,
                          bg=AppStyles.SECONDARY_COLOR,
                          fg="white",
                          font=("Helvetica", 10, "bold"),
                          relief="flat",
                          activebackground=AppStyles.PRIMARY_COLOR,
                          activeforeground="white",
                          width=width,
                          cursor="hand2")
        
        def on_enter(e):
            button['background'] = AppStyles.PRIMARY_COLOR
            
        def on_leave(e):
            button['background'] = AppStyles.SECONDARY_COLOR
            
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        return button
    
    @staticmethod
    def create_section_label(parent, text):
        """Create a section label with custom styling"""
        label = ttk.Label(parent, text=text,
                         style="Title.TLabel")
        return label 