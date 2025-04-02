import tkinter as tk
from tkinter import filedialog
import os

# Import required libraries, install if needed
try:
    from customtkinter import CTkFrame, CTkButton, CTkEntry, CTkLabel, CTkTextbox, CTkScrollableFrame
    from customtkinter import CTkComboBox, CTkSwitch, CTkOptionMenu
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter"])
    from customtkinter import CTkFrame, CTkButton, CTkEntry, CTkLabel, CTkTextbox, CTkScrollableFrame
    from customtkinter import CTkComboBox, CTkSwitch, CTkOptionMenu


class FeaturesList(CTkFrame):
    """A component for managing a list of features"""
    
    def __init__(self, master, callback, initial_items=None):
        super().__init__(master)
        self.callback = callback
        self.items = initial_items or []
        
        self.create_widgets()
        self.populate_list()
        
    def create_widgets(self):
        # Title
        CTkLabel(self, text="Project Features", font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=10, pady=(0, 10))
        
        # Features list frame
        list_frame = CTkScrollableFrame(self, height=200)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create listbox for features (using custom implementation since CTkListbox doesn't exist)
        self.items_frame = CTkFrame(list_frame)
        self.items_frame.pack(fill="both", expand=True)
        
        # Input area
        input_frame = CTkFrame(self)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        CTkLabel(input_frame, text="New Feature:").pack(side="left", padx=5)
        
        self.item_var = tk.StringVar()
        CTkEntry(input_frame, textvariable=self.item_var, width=250).pack(side="left", padx=5, fill="x", expand=True)
        
        CTkButton(input_frame, text="Add", command=self.add_item).pack(side="left", padx=5)
        
    def populate_list(self):
        """Fill the list with current items"""
        # Clear existing items
        for widget in self.items_frame.winfo_children():
            widget.destroy()
            
        # Add items
        for i, item in enumerate(self.items):
            item_frame = CTkFrame(self.items_frame)
            item_frame.pack(fill="x", padx=5, pady=2)
            
            CTkLabel(item_frame, text=f"• {item}", anchor="w").pack(side="left", fill="x", expand=True, padx=5)
            
            # Create a bound function to remove this specific item
            def make_remove_func(index):
                return lambda: self.remove_item(index)
            
            CTkButton(
                item_frame, 
                text="✕", 
                width=30, 
                command=make_remove_func(i)
            ).pack(side="right", padx=5)
    
    def add_item(self):
        """Add a new item to the list"""
        item_text = self.item_var.get().strip()
        if item_text:
            self.items.append(item_text)
            self.item_var.set("")
            self.populate_list()
            self.callback(self.items)
    
    def remove_item(self, index):
        """Remove an item from the list"""
        if 0 <= index < len(self.items):
            del self.items[index]
            self.populate_list()
            self.callback(self.items)
    
    def set_items(self, items):
        """Set the list of items"""
        if items is None:
            self.items = []
        else:
            try:
                self.items = list(items)
            except (TypeError, ValueError):
                self.items = []
        self.populate_list()
    
    def reset(self):
        """Clear all items"""
        self.items = []
        self.item_var.set("")
        self.populate_list()


class ImageGallery(CTkFrame):
    """A component for managing multiple images with URLs"""
    
    def __init__(self, master, callback, initial_values=None):
        super().__init__(master)
        self.callback = callback
        
        self.initial_values = initial_values or {
            "DemoGif": "",
            "screenshots": []
        }
        
        self.screenshots = self.initial_values["screenshots"].copy() if self.initial_values["screenshots"] else []
        self.create_widgets()
        
    def create_widgets(self):
        # Main container with padding
        main_frame = CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        CTkLabel(main_frame, text="Image Gallery", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 15))
        
        # Demo GIF section
        demo_frame = CTkFrame(main_frame, fg_color="transparent")
        demo_frame.pack(fill="x", pady=10)
        
        CTkLabel(demo_frame, text="Demo GIF URL:", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 5))
        CTkLabel(demo_frame, text="Add a URL to a GIF that demonstrates your project in action").pack(anchor="w", pady=(0, 5))
        
        self.demo_var = tk.StringVar(value=self.initial_values.get("DemoGif", ""))
        demo_entry = CTkEntry(demo_frame, textvariable=self.demo_var, height=35)
        demo_entry.pack(fill="x", pady=5)
        
        # Update DemoGif when focus leaves the field
        demo_entry.bind("<FocusOut>", lambda e: self.callback("DemoGif", self.demo_var.get()))
        
        # Screenshots section
        screenshot_frame = CTkFrame(main_frame, fg_color="transparent")
        screenshot_frame.pack(fill="both", expand=True, pady=15)
        
        CTkLabel(screenshot_frame, text="Screenshots:", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 5))
        CTkLabel(screenshot_frame, text="Add URLs to screenshots of your project (press Enter to add)").pack(anchor="w", pady=(0, 5))
        
        # Screenshots list frame
        scroll_frame = CTkScrollableFrame(screenshot_frame, height=200)
        scroll_frame.pack(fill="both", expand=True, pady=5)
        
        self.screenshots_container = CTkFrame(scroll_frame, fg_color="transparent")
        self.screenshots_container.pack(fill="both", expand=True)
        
        # Add screenshot input
        input_frame = CTkFrame(screenshot_frame, fg_color="transparent")
        input_frame.pack(fill="x", pady=10)
        
        self.screenshot_var = tk.StringVar()
        screenshot_entry = CTkEntry(
            input_frame, 
            textvariable=self.screenshot_var,
            placeholder_text="Enter image URL and press Enter",
            height=35
        )
        screenshot_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        add_btn = CTkButton(
            input_frame,
            text="Add Screenshot",
            command=self.add_screenshot,
            height=35
        )
        add_btn.pack(side="right")
        
        # Enter key binding
        screenshot_entry.bind("<Return>", lambda e: self.add_screenshot())
        
        # Refresh screenshot list
        self.refresh_screenshots()
        
    def add_screenshot(self):
        """Add a new screenshot URL"""
        url = self.screenshot_var.get().strip()
        if url:
            self.screenshots.append(url)
            self.screenshot_var.set("")  # Clear input
            self.refresh_screenshots()
            self.callback("screenshots", self.screenshots)
    
    def remove_screenshot(self, index):
        """Remove a screenshot at the specified index"""
        if 0 <= index < len(self.screenshots):
            del self.screenshots[index]
            self.refresh_screenshots()
            self.callback("screenshots", self.screenshots)
    
    def refresh_screenshots(self):
        """Refresh the screenshots list display"""
        # Clear existing items
        for widget in self.screenshots_container.winfo_children():
            widget.destroy()
            
        # Add each screenshot with delete button
        for i, url in enumerate(self.screenshots):
            item_frame = CTkFrame(self.screenshots_container)
            item_frame.pack(fill="x", padx=5, pady=3)
            
            # Display URL (truncated if needed)
            display_url = url
            if len(url) > 50:
                display_url = url[:47] + "..."
                
            CTkLabel(item_frame, text=display_url, anchor="w").pack(side="left", fill="x", expand=True, padx=5)
            
            # Create delete button
            def make_remove_func(idx):
                return lambda: self.remove_screenshot(idx)
                
            CTkButton(
                item_frame,
                text="✕",
                width=30,
                height=25,
                command=make_remove_func(i),
                fg_color="#e74c3c",
                hover_color="#c0392b"
            ).pack(side="right", padx=5)
    
    def set_values(self, values):
        """Set values for the image gallery"""
        if "DemoGif" in values:
            self.demo_var.set(values["DemoGif"])
            
        if "screenshots" in values:
            try:
                self.screenshots = list(values["screenshots"])
            except (TypeError, ValueError):
                self.screenshots = []
                
            self.refresh_screenshots()
    
    def reset(self):
        """Reset all fields"""
        self.demo_var.set("")
        self.screenshots = []
        self.screenshot_var.set("")
        self.refresh_screenshots()


class ListManager(CTkFrame):
    """Generic component for managing a list of items"""
    
    def __init__(self, master, item_name, callback, initial_items=None):
        super().__init__(master)
        self.item_name = item_name
        self.callback = callback
        self.items = initial_items or []
        
        self.create_widgets()
        self.populate_list()
        
    def create_widgets(self):
        # List frame
        list_frame = CTkScrollableFrame(self, height=200)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create frame for items
        self.items_frame = CTkFrame(list_frame, fg_color="transparent")
        self.items_frame.pack(fill="both", expand=True)
        
        # Input area
        input_frame = CTkFrame(self)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        CTkLabel(input_frame, text=f"New {self.item_name.capitalize()}:").pack(side="left", padx=5)
        
        self.item_var = tk.StringVar()
        entry = CTkEntry(input_frame, textvariable=self.item_var, width=250, height=35)
        entry.pack(side="left", padx=5, fill="x", expand=True)
        
        # Enter key binding
        entry.bind("<Return>", lambda e: self.add_item())
        
        CTkButton(input_frame, text="Add", command=self.add_item, height=35).pack(side="left", padx=5)
        
    def populate_list(self):
        """Fill the list with current items"""
        # Clear existing items
        for widget in self.items_frame.winfo_children():
            widget.destroy()
            
        # Add items
        for i, item in enumerate(self.items):
            item_frame = CTkFrame(self.items_frame)
            item_frame.pack(fill="x", padx=5, pady=2)
            
            CTkLabel(item_frame, text=f"• {item}", anchor="w").pack(side="left", fill="x", expand=True, padx=5)
            
            # Create a bound function to remove this specific item
            def make_remove_func(index):
                return lambda: self.remove_item(index)
            
            CTkButton(
                item_frame, 
                text="✕", 
                width=30,
                height=25,
                command=make_remove_func(i),
                fg_color="#e74c3c",
                hover_color="#c0392b"
            ).pack(side="right", padx=5)
    
    def add_item(self):
        """Add a new item to the list"""
        item_text = self.item_var.get().strip()
        if item_text:
            self.items.append(item_text)
            self.item_var.set("")
            self.populate_list()
            self.callback(self.items)
    
    def remove_item(self, index):
        """Remove an item from the list"""
        if 0 <= index < len(self.items):
            del self.items[index]
            self.populate_list()
            self.callback(self.items)
    
    def set_items(self, items):
        """Set the list of items"""
        if items is None:
            self.items = []
        else:
            try:
                self.items = list(items)
            except (TypeError, ValueError):
                self.items = []
        self.populate_list()
    
    def reset(self):
        """Clear all items"""
        self.items = []
        self.item_var.set("")
        self.populate_list()


class EnvVarsManager(CTkFrame):
    """Component for managing environment variables"""
    
    def __init__(self, master, callback, initial_items=None):
        super().__init__(master)
        self.callback = callback
        self.items = initial_items or []
        
        self.create_widgets()
        self.populate_list()
        
    def create_widgets(self):
        # Header
        header_frame = CTkFrame(self)
        header_frame.pack(fill="x", padx=10, pady=(0, 5))
        
        CTkLabel(header_frame, text="Name", width=100).pack(side="left", padx=5)
        CTkLabel(header_frame, text="Description", width=150).pack(side="left", padx=5)
        CTkLabel(header_frame, text="Default Value", width=100).pack(side="left", padx=5)
        CTkLabel(header_frame, text="", width=50).pack(side="left", padx=5)
        
        # List frame
        list_frame = CTkScrollableFrame(self, height=150)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create frame for items
        self.items_frame = CTkFrame(list_frame, fg_color="transparent")
        self.items_frame.pack(fill="both", expand=True)
        
        # Input area
        input_frame = CTkFrame(self)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        # Name input
        name_frame = CTkFrame(input_frame)
        name_frame.pack(side="left", padx=5)
        CTkLabel(name_frame, text="Name:").pack(anchor="w")
        self.name_var = tk.StringVar()
        name_entry = CTkEntry(name_frame, textvariable=self.name_var, width=100, height=35)
        name_entry.pack(fill="x")
        
        # Description input
        desc_frame = CTkFrame(input_frame)
        desc_frame.pack(side="left", padx=5, fill="x", expand=True)
        CTkLabel(desc_frame, text="Description:").pack(anchor="w")
        self.desc_var = tk.StringVar()
        CTkEntry(desc_frame, textvariable=self.desc_var, width=150, height=35).pack(fill="x")
        
        # Default value input
        value_frame = CTkFrame(input_frame)
        value_frame.pack(side="left", padx=5)
        CTkLabel(value_frame, text="Default:").pack(anchor="w")
        self.value_var = tk.StringVar()
        CTkEntry(value_frame, textvariable=self.value_var, width=100, height=35).pack(fill="x")
        
        # Add button
        add_frame = CTkFrame(input_frame)
        add_frame.pack(side="left", padx=5)
        CTkLabel(add_frame, text="").pack()  # Spacer for alignment
        CTkButton(add_frame, text="Add Variable", command=self.add_item, height=35).pack()
        
        # Enter key binding for the name field
        name_entry.bind("<Return>", lambda e: self.add_item())
        
    def populate_list(self):
        """Fill the list with current items"""
        # Clear existing items
        for widget in self.items_frame.winfo_children():
            widget.destroy()
            
        # Add items
        for i, item in enumerate(self.items):
            item_frame = CTkFrame(self.items_frame)
            item_frame.pack(fill="x", padx=5, pady=2)
            
            CTkLabel(item_frame, text=item["name"], width=100).pack(side="left", padx=5)
            CTkLabel(item_frame, text=item["desc"], width=150).pack(side="left", padx=5)
            CTkLabel(item_frame, text=item["value"], width=100).pack(side="left", padx=5)
            
            # Create a bound function to remove this specific item
            def make_remove_func(index):
                return lambda: self.remove_item(index)
            
            CTkButton(
                item_frame, 
                text="✕", 
                width=30,
                height=25,
                command=make_remove_func(i),
                fg_color="#e74c3c",
                hover_color="#c0392b"
            ).pack(side="left", padx=5)
    
    def add_item(self):
        """Add a new environment variable"""
        name = self.name_var.get().strip()
        desc = self.desc_var.get().strip()
        value = self.value_var.get().strip()
        
        if name and desc:
            self.items.append({
                "name": name,
                "desc": desc,
                "value": value
            })
            
            # Clear inputs
            self.name_var.set("")
            self.desc_var.set("")
            self.value_var.set("")
            
            # Update the list
            self.populate_list()
            self.callback(self.items)
    
    def remove_item(self, index):
        """Remove an environment variable"""
        if 0 <= index < len(self.items):
            del self.items[index]
            self.populate_list()
            self.callback(self.items)
    
    def set_items(self, items):
        """Set the list of environment variables"""
        if items is None:
            self.items = []
        else:
            try:
                # Make a deep copy of the items to avoid modifying the original
                self.items = [dict(item) for item in items]
            except (TypeError, ValueError):
                self.items = []
        self.populate_list()
    
    def reset(self):
        """Clear all environment variables"""
        self.items = []
        self.name_var.set("")
        self.desc_var.set("")
        self.value_var.set("")
        self.populate_list() 