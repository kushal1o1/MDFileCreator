import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import subprocess
import threading
import time

# Try to import required libraries, install if missing
try:
    from customtkinter import CTk, CTkFrame, CTkButton, CTkEntry, CTkLabel, CTkTextbox, CTkScrollableFrame
    from customtkinter import CTkTabview, CTkComboBox, CTkSwitch, CTkOptionMenu, set_appearance_mode, set_default_color_theme
    import markdown
    from tkhtmlview import HTMLScrolledText
except ImportError:
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter", "markdown", "tkhtmlview"])
    from customtkinter import CTk, CTkFrame, CTkButton, CTkEntry, CTkLabel, CTkTextbox, CTkScrollableFrame
    from customtkinter import CTkTabview, CTkComboBox, CTkSwitch, CTkOptionMenu, set_appearance_mode, set_default_color_theme
    import markdown
    from tkhtmlview import HTMLScrolledText

from md_generator import MarkdownGenerator
from ui_components import ListManager, EnvVarsManager, ImageGallery

# Common technology options
TECHNOLOGY_OPTIONS = [
    "Python", "JavaScript", "TypeScript", "React", "Vue", "Angular", "Node", 
    "Django", "Flask", "Express", "MongoDB", "MySQL", "PostgreSQL", "Redis",
    "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Git", "GitHub", "GitLab",
    "HTML", "CSS", "Sass", "TailwindCSS", "Bootstrap", "Material-UI", "Chakra-UI",
    "Java", "C#", "C++", "Go", "Rust", "PHP", "Ruby", "Swift", "Kotlin"
]

# Common license options
LICENSE_OPTIONS = [
    "MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause", "Unlicense", "MPL-2.0",
    "CC0-1.0", "LGPL-3.0", "AGPL-3.0", "BSL-1.0"
]

class MDCreatorApp(CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("MD File Creator")
        self.geometry("1280x720")
        self.minsize(1000, 600)
        
        # Set theme
        set_appearance_mode("dark")  # Default to dark mode
        set_default_color_theme("blue")
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Setup variables
        self.markdown_generator = MarkdownGenerator()
        self.update_pending = False
        
        # Create UI
        self.create_ui()
        
        # Initial update
        self.after(100, self.update_preview)
        
    def create_ui(self):
        # Main container
        self.main_frame = CTkFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Left side (form)
        self.form_frame = CTkFrame(self.main_frame)
        self.form_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Right side (preview)
        self.preview_frame = CTkFrame(self.main_frame)
        self.preview_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        self.preview_frame.grid_columnconfigure(0, weight=1)
        self.preview_frame.grid_rowconfigure(1, weight=1)
        
        # Setup tabs
        self.setup_tabs()
        
        # Setup preview
        self.setup_preview()
        
        # Add status bar
        self.setup_status_bar()
        
    def setup_tabs(self):
        # Create tabview
        self.tabview = CTkTabview(self.form_frame)
        self.tabview.pack(fill="both", expand=True)
        
        # Create tabs
        tabs = [
            "Basic Info", 
            "Features", 
            "Images", 
            "Prerequisites", 
            "Environment", 
            "Technologies", 
            "Additional"
        ]
        
        for tab in tabs:
            self.tabview.add(tab)
            
        # Setup each tab
        self.setup_basic_tab()
        self.setup_features_tab()
        self.setup_images_tab()
        self.setup_prerequisites_tab()
        self.setup_environment_tab()
        self.setup_technologies_tab()
        self.setup_additional_tab()
        
    def setup_basic_tab(self):
        tab = self.tabview.tab("Basic Info")
        
        # Create a frame with padding
        content_frame = CTkFrame(tab, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Section title
        CTkLabel(content_frame, text="Project Information", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 15))
        
        # Project name
        CTkLabel(content_frame, text="Project Name:").pack(anchor="w", pady=(5, 0))
        self.project_name_var = tk.StringVar()
        project_name_entry = CTkEntry(content_frame, textvariable=self.project_name_var, width=350, height=35)
        project_name_entry.pack(anchor="w", pady=(0, 10), fill="x")
        
        # GitHub username
        CTkLabel(content_frame, text="GitHub Username:").pack(anchor="w", pady=(5, 0))
        self.username_var = tk.StringVar()
        username_entry = CTkEntry(content_frame, textvariable=self.username_var, width=350, height=35)
        username_entry.pack(anchor="w", pady=(0, 10), fill="x")
        
        # Concise description
        CTkLabel(content_frame, text="Concise Description:").pack(anchor="w", pady=(5, 0))
        self.concisedesc_var = tk.StringVar()
        concisedesc_entry = CTkEntry(content_frame, textvariable=self.concisedesc_var, width=350, height=35)
        concisedesc_entry.pack(anchor="w", pady=(0, 10), fill="x")
        
        # Logo URL
        CTkLabel(content_frame, text="Logo URL:").pack(anchor="w", pady=(5, 0))
        self.logo_var = tk.StringVar()
        logo_entry = CTkEntry(content_frame, textvariable=self.logo_var, width=350, height=35)
        logo_entry.pack(anchor="w", pady=(0, 10), fill="x")
        
        # Overview
        CTkLabel(content_frame, text="Project Overview:").pack(anchor="w", pady=(5, 0))
        self.overview = CTkTextbox(content_frame, width=350, height=150)
        self.overview.pack(anchor="w", pady=(0, 10), fill="both", expand=True)
        
        # Focus out events to update data when leaving fields
        project_name_entry.bind("<FocusOut>", lambda e: self.update_field("project_name", self.project_name_var.get()))
        username_entry.bind("<FocusOut>", lambda e: self.update_field("username", self.username_var.get()))
        concisedesc_entry.bind("<FocusOut>", lambda e: self.update_field("concisedesc", self.concisedesc_var.get()))
        logo_entry.bind("<FocusOut>", lambda e: self.update_field("logo", self.logo_var.get()))
        
        # Update button for overview - since it doesn't have focus out event
        update_btn = CTkButton(
            content_frame,
            text="Update Overview",
            command=lambda: self.update_field("overview", self.overview.get("0.0", "end").strip()),
            height=35,
            fg_color="#3a7ebf",
            hover_color="#2a6da8"
        )
        update_btn.pack(anchor="e", pady=10)
        
    def setup_features_tab(self):
        tab = self.tabview.tab("Features")
        
        # Create container frame
        content_frame = CTkFrame(tab, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Section title
        CTkLabel(content_frame, text="Project Features", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 15))
        
        # Instructions
        CTkLabel(content_frame, text="Add key features of your project. Press Enter to add each feature.").pack(anchor="w", pady=(0, 10))
        
        # Features list frame
        list_frame = CTkScrollableFrame(content_frame, height=250)
        list_frame.pack(fill="both", expand=True, pady=10)
        
        # Container for feature items
        self.features_container = CTkFrame(list_frame, fg_color="transparent")
        self.features_container.pack(fill="both", expand=True)
        
        # Input for new feature
        input_frame = CTkFrame(content_frame, fg_color="transparent")
        input_frame.pack(fill="x", pady=10)
        
        self.feature_var = tk.StringVar()
        feature_entry = CTkEntry(input_frame, textvariable=self.feature_var, width=350, height=35, placeholder_text="Enter a new feature")
        feature_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        add_btn = CTkButton(
            input_frame, 
            text="Add Feature", 
            command=self.add_feature,
            height=35
        )
        add_btn.pack(side="right")
        
        # Enter key binding
        feature_entry.bind("<Return>", lambda e: self.add_feature())
        
        # Load existing features
        self.features = self.markdown_generator.get_field("features") or []
        self.refresh_features_list()
        
    def refresh_features_list(self):
        # Clear existing items
        for widget in self.features_container.winfo_children():
            widget.destroy()
            
        # Add each feature with delete button
        for i, feature in enumerate(self.features):
            item_frame = CTkFrame(self.features_container)
            item_frame.pack(fill="x", padx=5, pady=3)
            
            CTkLabel(item_frame, text=f"• {feature}", anchor="w").pack(side="left", fill="x", expand=True, padx=5)
            
            # Create delete button
            def make_remove_func(idx):
                return lambda: self.remove_feature(idx)
                
            CTkButton(
                item_frame,
                text="✕",
                width=30,
                height=25,
                command=make_remove_func(i),
                fg_color="#e74c3c",
                hover_color="#c0392b"
            ).pack(side="right", padx=5)
    
    def add_feature(self):
        feature = self.feature_var.get().strip()
        if feature:
            self.features.append(feature)
            self.feature_var.set("")  # Clear input
            self.refresh_features_list()
            self.update_field("features", self.features)
    
    def remove_feature(self, index):
        if 0 <= index < len(self.features):
            del self.features[index]
            self.refresh_features_list()
            self.update_field("features", self.features)
    
    def setup_images_tab(self):
        tab = self.tabview.tab("Images")
        
        # Create image gallery
        self.image_gallery = ImageGallery(
            tab,
            callback=self.update_images,
            initial_values={
                "DemoGif": self.markdown_generator.get_field("DemoGif") or "",
                "screenshots": self.markdown_generator.get_field("screenshots") or []
            }
        )
        self.image_gallery.pack(fill="both", expand=True, padx=20, pady=20)

    def update_images(self, image_type, value):
        """Update image fields in the markdown generator"""
        if image_type == "DemoGif":
            self.update_field("DemoGif", value)
        elif image_type == "screenshots":
            self.update_field("screenshots", value)
    
    def setup_prerequisites_tab(self):
        tab = self.tabview.tab("Prerequisites")
        
        # Create container frame
        content_frame = CTkFrame(tab, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Section title
        CTkLabel(content_frame, text="Prerequisites", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 15))
        
        # Instructions
        CTkLabel(content_frame, text="Add project prerequisites. Press Enter to add each item.").pack(anchor="w", pady=(0, 10))
        
        # List manager
        self.prerequisites_manager = ListManager(
            content_frame,
            item_name="prerequisite",
            callback=lambda items: self.update_field("Prerequisites", items),
            initial_items=self.markdown_generator.get_field("Prerequisites")
        )
        self.prerequisites_manager.pack(fill="both", expand=True)
        
    def setup_environment_tab(self):
        tab = self.tabview.tab("Environment")
        
        # Create container frame
        content_frame = CTkFrame(tab, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Section title
        CTkLabel(content_frame, text="Environment Variables", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 15))
        
        # Instructions
        CTkLabel(content_frame, text="Add environment variables for your project.").pack(anchor="w", pady=(0, 10))
        
        # Env vars manager
        self.env_vars_manager = EnvVarsManager(
            content_frame,
            callback=lambda env_vars: self.update_field("envvars", env_vars),
            initial_items=self.markdown_generator.get_field("envvars")
        )
        self.env_vars_manager.pack(fill="both", expand=True)
        
    def setup_technologies_tab(self):
        tab = self.tabview.tab("Technologies")
        
        # Create container frame
        content_frame = CTkFrame(tab, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Section title
        CTkLabel(content_frame, text="Technologies Used", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 15))
        
        # Instructions
        CTkLabel(content_frame, text="Select from common options or add your own technologies.").pack(anchor="w", pady=(0, 10))
        
        # Common technology options
        options_frame = CTkFrame(content_frame)
        options_frame.pack(fill="x", pady=10)
        
        # The combo box for tech selection
        CTkLabel(options_frame, text="Common Technologies:").pack(side="left", padx=(0, 10))
        
        self.tech_combo = CTkComboBox(
            options_frame, 
            values=TECHNOLOGY_OPTIONS,
            width=200,
            height=35
        )
        self.tech_combo.pack(side="left", padx=(0, 10))
        
        add_selected_btn = CTkButton(
            options_frame,
            text="Add Selected",
            command=self.add_selected_tech,
            height=35
        )
        add_selected_btn.pack(side="left")
        
        # Custom tech entry
        custom_frame = CTkFrame(content_frame)
        custom_frame.pack(fill="x", pady=10)
        
        CTkLabel(custom_frame, text="Custom Technology:").pack(side="left", padx=(0, 10))
        
        self.custom_tech_var = tk.StringVar()
        custom_tech_entry = CTkEntry(custom_frame, textvariable=self.custom_tech_var, width=200, height=35)
        custom_tech_entry.pack(side="left", padx=(0, 10))
        
        add_custom_btn = CTkButton(
            custom_frame,
            text="Add Custom",
            command=self.add_custom_tech,
            height=35
        )
        add_custom_btn.pack(side="left")
        
        # Enter key binding
        custom_tech_entry.bind("<Return>", lambda e: self.add_custom_tech())
        
        # List of added technologies
        CTkLabel(content_frame, text="Technologies (click to remove):").pack(anchor="w", pady=(10, 5))
        
        list_frame = CTkScrollableFrame(content_frame, height=200)
        list_frame.pack(fill="both", expand=True, pady=5)
        
        self.tech_container = CTkFrame(list_frame, fg_color="transparent")
        self.tech_container.pack(fill="both", expand=True)
        
        # Load existing technologies
        self.technologies = self.markdown_generator.get_field("tech") or []
        self.refresh_tech_list()
    
    def add_selected_tech(self):
        """Add the selected technology from the dropdown"""
        tech = self.tech_combo.get()
        if tech and tech not in self.technologies:
            self.technologies.append(tech)
            self.refresh_tech_list()
            self.update_field("tech", self.technologies)
    
    def add_custom_tech(self):
        """Add a custom technology"""
        tech = self.custom_tech_var.get().strip()
        if tech and tech not in self.technologies:
            self.technologies.append(tech)
            self.custom_tech_var.set("")  # Clear input
            self.refresh_tech_list()
            self.update_field("tech", self.technologies)
    
    def refresh_tech_list(self):
        """Refresh the list of technologies"""
        # Clear existing items
        for widget in self.tech_container.winfo_children():
            widget.destroy()
            
        # Create a grid of technology buttons
        columns = 3
        for i, tech in enumerate(self.technologies):
            row, col = divmod(i, columns)
            
            # Create a clickable button that removes the tech when clicked
            def make_remove_func(t):
                return lambda: self.remove_tech(t)
                
            btn = CTkButton(
                self.tech_container,
                text=tech,
                command=make_remove_func(tech),
                fg_color="#3498db",
                hover_color="#2980b9",
                height=30
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            
        # Make columns expandable
        for col in range(columns):
            self.tech_container.columnconfigure(col, weight=1)
    
    def remove_tech(self, tech):
        """Remove a technology from the list"""
        if tech in self.technologies:
            self.technologies.remove(tech)
            self.refresh_tech_list()
            self.update_field("tech", self.technologies)
        
    def setup_additional_tab(self):
        tab = self.tabview.tab("Additional")
        
        # Create container frame
        content_frame = CTkFrame(tab, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Section title
        CTkLabel(content_frame, text="Additional Information", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 15))
        
        # License selection
        license_frame = CTkFrame(content_frame, fg_color="transparent")
        license_frame.pack(fill="x", pady=10)
        
        CTkLabel(license_frame, text="License:").pack(side="left", padx=(0, 10))
        
        self.license_var = tk.StringVar()
        self.license_dropdown = CTkComboBox(
            license_frame,
            values=LICENSE_OPTIONS,
            variable=self.license_var,
            width=250,
            height=35
        )
        self.license_dropdown.pack(side="left")
        self.license_var.set(self.markdown_generator.get_field("license") or "MIT")
        
        # License focusout event
        self.license_dropdown.bind("<FocusOut>", lambda e: self.update_field("license", self.license_var.get()))
        
        # Contact information
        contact_frame = CTkFrame(content_frame, fg_color="transparent")
        contact_frame.pack(fill="x", pady=20)
        
        CTkLabel(contact_frame, text="Contact:").pack(side="left", padx=(0, 10))
        
        self.contact_var = tk.StringVar(value=self.markdown_generator.get_field("contact") or "")
        contact_entry = CTkEntry(contact_frame, textvariable=self.contact_var, width=350, height=35)
        contact_entry.pack(side="left", fill="x", expand=True)
        
        # Contact focusout event
        contact_entry.bind("<FocusOut>", lambda e: self.update_field("contact", self.contact_var.get()))
        
        # Theme selection
        theme_frame = CTkFrame(content_frame, fg_color="transparent")
        theme_frame.pack(fill="x", pady=20)
        
        CTkLabel(theme_frame, text="UI Theme:").pack(side="left", padx=(0, 10))
        
        CTkButton(
            theme_frame, 
            text="Light", 
            command=lambda: set_appearance_mode("light"),
            width=100,
            height=35
        ).pack(side="left", padx=5)
        
        CTkButton(
            theme_frame, 
            text="Dark", 
            command=lambda: set_appearance_mode("dark"),
            width=100,
            height=35
        ).pack(side="left", padx=5)
        
        # Actions section
        actions_frame = CTkFrame(content_frame)
        actions_frame.pack(fill="x", pady=20)
        
        CTkButton(
            actions_frame, 
            text="New Project", 
            command=self.new_project,
            width=120,
            height=40,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        ).pack(side="left", padx=5)
        
        CTkButton(
            actions_frame, 
            text="Save Template", 
            command=self.save_template,
            width=120,
            height=40,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        ).pack(side="left", padx=5)
        
        CTkButton(
            actions_frame, 
            text="Load Template", 
            command=self.load_template,
            width=120,
            height=40,
            fg_color="#3498db",
            hover_color="#2980b9"
        ).pack(side="left", padx=5)
        
    def setup_preview(self):
        # Title
        CTkLabel(
            self.preview_frame, 
            text="Markdown Preview", 
            font=("Segoe UI", 18, "bold")
        ).grid(row=0, column=0, sticky="w", padx=15, pady=(0, 10))
        
        # Preview tabs frame
        preview_tabs = CTkTabview(self.preview_frame)
        preview_tabs.grid(row=1, column=0, sticky="nsew", padx=15, pady=5)
        
        # Create tabs
        preview_tabs.add("HTML View")
        preview_tabs.add("Source")
        
        # HTML preview
        self.html_view = HTMLScrolledText(preview_tabs.tab("HTML View"), padx=10, pady=10)
        self.html_view.pack(fill="both", expand=True)
        
        # Source preview
        self.markdown_text = CTkTextbox(preview_tabs.tab("Source"), wrap="word")
        self.markdown_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Action buttons
        actions_frame = CTkFrame(self.preview_frame)
        actions_frame.grid(row=2, column=0, sticky="ew", padx=15, pady=15)
        
        CTkButton(
            actions_frame, 
            text="Save README.md", 
            command=self.save_markdown,
            fg_color="#28a745",
            hover_color="#218838",
            width=150,
            height=40
        ).pack(side="right", padx=5)
        
        CTkButton(
            actions_frame, 
            text="Copy to Clipboard", 
            command=self.copy_to_clipboard,
            width=150,
            height=40
        ).pack(side="right", padx=5)
    
    def setup_status_bar(self):
        # Create a status bar at the bottom
        self.status_var = tk.StringVar(value="Ready")
        status_frame = CTkFrame(self)
        status_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 15))
        
        CTkLabel(status_frame, textvariable=self.status_var).pack(side="left", padx=15)
        
    def update_field(self, field, value):
        """Update a field in the markdown generator and refresh the preview"""
        try:
            self.status_var.set(f"Updating {field}...")
            self.update_idletasks()
            
            # Update data
            self.markdown_generator.update_field(field, value)
            
            # Schedule preview update if not already pending
            if not self.update_pending:
                self.update_pending = True
                self.after(100, self.update_preview)
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
        
    def update_preview(self):
        """Generate and update the preview"""
        try:
            # Reset the pending flag
            self.update_pending = False
            
            # Update status
            self.status_var.set("Generating preview...")
            self.update_idletasks()
            
            # Generate markdown
            markdown_content = self.markdown_generator.generate_markdown()
            
            # Update markdown text view
            self.markdown_text.delete("0.0", "end")
            self.markdown_text.insert("0.0", markdown_content)
            
            # Update HTML view - use after to avoid blocking UI
            self.after(0, lambda: self.update_html_view(markdown_content))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update preview: {str(e)}")
            self.status_var.set(f"Error: {str(e)}")
    
    def update_html_view(self, content):
        """Update the HTML view separately to avoid blocking the UI"""
        try:
            # Convert to HTML
            html_content = markdown.markdown(content, extensions=['tables'])
            
            # Set HTML content
            self.html_view.set_html(html_content)
            
            # Update status
            self.status_var.set("Preview updated")
        except Exception as e:
            self.status_var.set(f"HTML render error: {str(e)}")
            
    def new_project(self):
        """Create a new project"""
        if messagebox.askyesno("New Project", "Are you sure you want to start a new project? All unsaved changes will be lost."):
            # Reset markdown generator
            self.markdown_generator.reset()
            
            # Reset form fields
            self.reset_form()
            
            # Update preview
            self.update_preview()
            self.status_var.set("New project created")
            
    def reset_form(self):
        """Reset all form fields"""
        # Reset basic info
        self.project_name_var.set("")
        self.username_var.set("")
        self.concisedesc_var.set("")
        self.logo_var.set("")
        self.overview.delete("0.0", "end")
        
        # Reset features
        self.features = []
        self.refresh_features_list()
        
        # Reset images
        self.image_gallery.reset()
        
        # Reset additional info
        self.license_var.set("MIT")
        self.contact_var.set("")
        
        # Reset managers
        self.prerequisites_manager.reset()
        self.env_vars_manager.reset()
        
        # Reset technologies
        self.technologies = []
        self.refresh_tech_list()
        
    def save_template(self):
        """Save the current project as a template"""
        from tkinter import filedialog
        import json
        
        self.status_var.set("Saving template...")
        self.update_idletasks()
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
            initialfile="template.json"
        )
        
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(self.markdown_generator.get_data(), file, indent=2)
                messagebox.showinfo("Success", f"Template saved to {file_path}")
                self.status_var.set(f"Template saved to {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save template: {str(e)}")
                self.status_var.set(f"Error saving template: {str(e)}")
        else:
            self.status_var.set("Template save cancelled")
                
    def load_template(self):
        """Load a project from a template"""
        from tkinter import filedialog
        import json
        
        self.status_var.set("Loading template...")
        self.update_idletasks()
        
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                
                # Update markdown generator
                self.markdown_generator.set_data(data)
                
                # Reset and populate form
                self.reset_form()
                self.populate_form()
                
                # Update preview
                self.update_preview()
                
                messagebox.showinfo("Success", f"Template loaded from {file_path}")
                self.status_var.set(f"Template loaded from {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load template: {str(e)}")
                self.status_var.set(f"Error loading template: {str(e)}")
        else:
            self.status_var.set("Template load cancelled")
                
    def populate_form(self):
        """Populate form fields from loaded data"""
        data = self.markdown_generator.get_data()
        
        # Populate basic info
        self.project_name_var.set(data.get("project_name", ""))
        self.username_var.set(data.get("username", ""))
        self.concisedesc_var.set(data.get("concisedesc", ""))
        self.logo_var.set(data.get("logo", ""))
        self.overview.delete("0.0", "end")
        self.overview.insert("0.0", data.get("overview", ""))
        
        # Populate features
        self.features = data.get("features", [])
        self.refresh_features_list()
        
        # Populate images
        self.image_gallery.set_values({
            "DemoGif": data.get("DemoGif", ""),
            "screenshots": data.get("screenshots", [])
        })
        
        # Populate additional info
        self.license_var.set(data.get("license", "MIT"))
        self.contact_var.set(data.get("contact", ""))
        
        # Populate managers
        self.prerequisites_manager.set_items(data.get("Prerequisites", []))
        self.env_vars_manager.set_items(data.get("envvars", []))
        
        # Populate technologies
        self.technologies = data.get("tech", [])
        self.refresh_tech_list()
        
    def save_markdown(self):
        """Save markdown content to a file"""
        from tkinter import filedialog
        
        self.status_var.set("Saving markdown...")
        self.update_idletasks()
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown Files", "*.md"), ("All Files", "*.*")],
            initialfile="README.md"
        )
        
        if file_path:
            try:
                markdown_content = self.markdown_text.get("0.0", "end")
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(markdown_content)
                messagebox.showinfo("Success", f"Markdown saved to {file_path}")
                self.status_var.set(f"Markdown saved to {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
                self.status_var.set(f"Error saving markdown: {str(e)}")
        else:
            self.status_var.set("Markdown save cancelled")
                
    def copy_to_clipboard(self):
        """Copy markdown content to clipboard"""
        try:
            self.clipboard_clear()
            self.clipboard_append(self.markdown_text.get("0.0", "end"))
            self.status_var.set("Markdown copied to clipboard")
            messagebox.showinfo("Success", "Markdown copied to clipboard")
        except Exception as e:
            self.status_var.set(f"Error copying to clipboard: {str(e)}")
            messagebox.showerror("Error", f"Failed to copy to clipboard: {str(e)}")
        
def main():
    app = MDCreatorApp()
    app.mainloop()
    
if __name__ == "__main__":
    main() 