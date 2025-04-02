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


# Technology categories and options for the selector
TECH_CATEGORIES = {
    "Languages": [
        "Python", "JavaScript", "TypeScript", "Java", "C#", "C++", 
        "Go", "Rust", "PHP", "Ruby", "Swift", "Kotlin"
    ],
    "Frontend": [
        "React", "Vue", "Angular", "HTML", "CSS", "Sass", 
        "TailwindCSS", "Bootstrap", "Material-UI", "Chakra-UI"
    ],
    "Backend": [
        "Node", "Django", "Flask", "Express", "FastAPI", "Spring Boot",
        "ASP.NET", "Laravel"
    ],
    "Database": [
        "MongoDB", "MySQL", "PostgreSQL", "Redis", "SQLite", "Oracle",
        "SQL Server", "Firestore"
    ],
    "DevOps": [
        "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Git", "GitHub", "GitLab",
        "Jenkins", "Travis CI", "CircleCI"
    ],
    "Mobile": [
        "React Native", "Flutter", "Android", "iOS", "Xamarin", "Ionic"
    ]
}


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


class TechnologySelector(CTkFrame):
    """A component for selecting technologies using a tag-based approach"""
    
    def __init__(self, master, callback, initial_items=None):
        super().__init__(master)
        self.callback = callback
        self.selected_techs = initial_items or []
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create tabs container for categories
        self.tabs_container = CTkScrollableFrame(self, height=250)
        self.tabs_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create tab buttons for each technology category
        tab_buttons_frame = CTkFrame(self.tabs_container)
        tab_buttons_frame.pack(fill="x", pady=10)
        
        self.current_category = tk.StringVar(value=next(iter(TECH_CATEGORIES)))
        
        # Create buttons for each category
        for i, category in enumerate(TECH_CATEGORIES.keys()):
            def make_category_func(cat):
                return lambda: self.show_category(cat)
                
            CTkButton(
                tab_buttons_frame,
                text=category,
                command=make_category_func(category),
                width=100,
                height=28,
                border_width=1,
                fg_color=("gray90", "gray20"),
                hover_color=("gray70", "gray30")
            ).grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            
        # Make columns expandable
        for i in range(len(TECH_CATEGORIES)):
            tab_buttons_frame.columnconfigure(i, weight=1)
        
        # Technology tags container
        self.tech_content = CTkFrame(self.tabs_container, fg_color="transparent")
        self.tech_content.pack(fill="both", expand=True, pady=10)
        
        # Selected technologies section
        selected_frame = CTkFrame(self)
        selected_frame.pack(fill="x", padx=10, pady=10)
        
        CTkLabel(selected_frame, text="Selected Technologies:", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 5))
        
        # Container for selected tech tags
        selected_tags_frame = CTkScrollableFrame(selected_frame, height=100)
        selected_tags_frame.pack(fill="x", pady=5)
        
        self.selected_container = CTkFrame(selected_tags_frame, fg_color="transparent")
        self.selected_container.pack(fill="both", expand=True)
        
        # Custom technology entry
        custom_frame = CTkFrame(selected_frame)
        custom_frame.pack(fill="x", pady=10)
        
        self.custom_tech_var = tk.StringVar()
        custom_tech_entry = CTkEntry(
            custom_frame, 
            textvariable=self.custom_tech_var, 
            width=200, 
            height=35, 
            placeholder_text="Enter custom technology"
        )
        custom_tech_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Add button for custom tech
        add_btn = CTkButton(
            custom_frame,
            text="Add Custom",
            command=self.add_custom_tech,
            height=35
        )
        add_btn.pack(side="right")
        
        # Bind Enter key to add custom tech
        custom_tech_entry.bind("<Return>", lambda e: self.add_custom_tech())
        
        # Initial display
        self.show_category(self.current_category.get())
        self.refresh_selected_techs()
        
    def show_category(self, category):
        """Display technologies for the selected category"""
        self.current_category.set(category)
        
        # Clear existing content
        for widget in self.tech_content.winfo_children():
            widget.destroy()
            
        # Create grid layout for technology buttons
        techs = TECH_CATEGORIES.get(category, [])
        columns = 4  # Number of columns in the grid
        
        for i, tech in enumerate(techs):
            row, col = divmod(i, columns)
            
            # Check if this tech is already selected
            is_selected = tech in self.selected_techs
            
            # Create button with appropriate styling based on selection state
            btn = CTkButton(
                self.tech_content,
                text=tech,
                command=lambda t=tech, s=is_selected: self.toggle_tech(t),
                width=80,
                height=30,
                fg_color="#3498db" if is_selected else "gray30",
                hover_color="#2980b9" if is_selected else "gray40",
                border_width=1
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            
        # Make columns expandable
        for col in range(columns):
            self.tech_content.columnconfigure(col, weight=1)
    
    def toggle_tech(self, tech):
        """Toggle a technology's selection state"""
        if tech in self.selected_techs:
            self.selected_techs.remove(tech)
        else:
            self.selected_techs.append(tech)
            
        # Refresh the current category view and selected tags
        self.show_category(self.current_category.get())
        self.refresh_selected_techs()
        self.callback(self.selected_techs)
    
    def add_custom_tech(self):
        """Add a custom technology not in the predefined list"""
        tech = self.custom_tech_var.get().strip()
        if tech and tech not in self.selected_techs:
            self.selected_techs.append(tech)
            self.custom_tech_var.set("")  # Clear input
            self.refresh_selected_techs()
            self.callback(self.selected_techs)
    
    def refresh_selected_techs(self):
        """Update the display of selected technologies"""
        # Clear existing tags
        for widget in self.selected_container.winfo_children():
            widget.destroy()
            
        # No technologies selected
        if not self.selected_techs:
            CTkLabel(
                self.selected_container, 
                text="No technologies selected yet", 
                text_color="gray60"
            ).pack(pady=10)
            return
            
        # Create a flex-wrap style layout for the tags
        current_frame = CTkFrame(self.selected_container, fg_color="transparent")
        current_frame.pack(fill="x", pady=2)
        
        max_width = self.selected_container.winfo_width() - 20  # Approximate padding
        current_width = 0
        
        for tech in self.selected_techs:
            # Create a frame for each tag
            tag_frame = CTkFrame(
                current_frame, 
                fg_color="#3498db",
                corner_radius=15
            )
            
            # Approximate width calculation
            estimated_width = len(tech) * 7 + 50  # Rough estimate: 7 pixels per character + padding
            
            # Start a new row if this tag would exceed the frame width
            if current_width > 0 and current_width + estimated_width > max_width:
                current_frame = CTkFrame(self.selected_container, fg_color="transparent")
                current_frame.pack(fill="x", pady=2)
                current_width = 0
            
            tag_frame.pack(side="left", padx=3, pady=3)
            
            # Tag label
            CTkLabel(
                tag_frame, 
                text=tech, 
                text_color="white",
                padx=8,
                pady=2
            ).pack(side="left")
            
            # Remove button
            def make_remove_func(t):
                return lambda: self.remove_tech(t)
                
            CTkButton(
                tag_frame,
                text="✕",
                width=20,
                height=20,
                command=make_remove_func(tech),
                fg_color="#3498db",
                hover_color="#2980b9",
                text_color="white",
                corner_radius=10
            ).pack(side="left")
            
            current_width += estimated_width
    
    def remove_tech(self, tech):
        """Remove a technology from the selected list"""
        if tech in self.selected_techs:
            self.selected_techs.remove(tech)
            self.show_category(self.current_category.get())
            self.refresh_selected_techs()
            self.callback(self.selected_techs)
    
    def set_items(self, items):
        """Set the list of selected technologies"""
        if items is None:
            self.selected_techs = []
        else:
            try:
                self.selected_techs = list(items)
            except (TypeError, ValueError):
                self.selected_techs = []
                
        self.show_category(self.current_category.get())
        self.refresh_selected_techs()
    
    def reset(self):
        """Clear all selections"""
        self.selected_techs = []
        self.show_category(self.current_category.get())
        self.refresh_selected_techs()


class ImageGallery(CTkFrame):
    """A component for managing project images with two specific screenshots"""
    
    def __init__(self, master, callback, initial_values=None):
        super().__init__(master)
        self.callback = callback
        
        self.initial_values = initial_values or {
            "DemoGif": "",
            "screenshot1": "",
            "screenshot2": ""
        }
        
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
        CTkLabel(screenshot_frame, text="Add exactly two screenshot URLs for your project").pack(anchor="w", pady=(0, 5))
        
        # Screenshot 1
        screenshot1_frame = CTkFrame(screenshot_frame, fg_color="transparent")
        screenshot1_frame.pack(fill="x", pady=10)
        
        CTkLabel(screenshot1_frame, text="Screenshot 1:").pack(side="left", padx=(0, 10))
        
        self.screenshot1_var = tk.StringVar(value=self.initial_values.get("screenshot1", ""))
        screenshot1_entry = CTkEntry(screenshot1_frame, textvariable=self.screenshot1_var, height=35)
        screenshot1_entry.pack(side="left", fill="x", expand=True)
        
        # Update screenshot1 when focus leaves the field
        screenshot1_entry.bind("<FocusOut>", lambda e: self.callback("screenshot1", self.screenshot1_var.get()))
        
        # Screenshot 2
        screenshot2_frame = CTkFrame(screenshot_frame, fg_color="transparent")
        screenshot2_frame.pack(fill="x", pady=10)
        
        CTkLabel(screenshot2_frame, text="Screenshot 2:").pack(side="left", padx=(0, 10))
        
        self.screenshot2_var = tk.StringVar(value=self.initial_values.get("screenshot2", ""))
        screenshot2_entry = CTkEntry(screenshot2_frame, textvariable=self.screenshot2_var, height=35)
        screenshot2_entry.pack(side="left", fill="x", expand=True)
        
        # Update screenshot2 when focus leaves the field
        screenshot2_entry.bind("<FocusOut>", lambda e: self.callback("screenshot2", self.screenshot2_var.get()))
        
    def set_values(self, values):
        """Set values for the image gallery"""
        if "DemoGif" in values:
            self.demo_var.set(values["DemoGif"])
            
        if "screenshot1" in values:
            self.screenshot1_var.set(values["screenshot1"])
            
        if "screenshot2" in values:
            self.screenshot2_var.set(values["screenshot2"])
    
    def reset(self):
        """Reset all fields"""
        self.demo_var.set("")
        self.screenshot1_var.set("")
        self.screenshot2_var.set("")


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