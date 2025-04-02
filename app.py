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
except ImportError:
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter"])
    from customtkinter import CTk, CTkFrame, CTkButton, CTkEntry, CTkLabel, CTkTextbox, CTkScrollableFrame
    from customtkinter import CTkTabview, CTkComboBox, CTkSwitch, CTkOptionMenu, set_appearance_mode, set_default_color_theme

from md_generator import MarkdownGenerator
from ui_components import ListManager, EnvVarsManager, ImageGallery, TechnologySelector
from ui_components import TemplateSelector, FileStructureEditor, UsageCodeEditor

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
        self.geometry("1100x800")
        self.minsize(1000, 600)
        
        # Set theme
        set_appearance_mode("dark")  # Default to dark mode
        set_default_color_theme("blue")
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Setup variables
        self.markdown_generator = MarkdownGenerator()
        
        # Create UI
        self.create_ui()
        
    def create_ui(self):
        # Main container
        self.main_frame = CTkFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Form frame (covers the entire area now)
        self.form_frame = CTkFrame(self.main_frame)
        self.form_frame.grid(row=0, column=0, sticky="nsew")
        
        # Setup tabs
        self.setup_tabs()
        
        # Add status bar
        self.setup_status_bar()
        
        # Add action buttons at the bottom
        self.setup_action_buttons()
        
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
            "File Structure",
            "Usage Code",
            "Environment", 
            "Technologies", 
            "Template",
            "Additional"
        ]
        
        for tab in tabs:
            self.tabview.add(tab)
            
        # Setup each tab
        self.setup_basic_tab()
        self.setup_features_tab()
        self.setup_images_tab()
        self.setup_prerequisites_tab()
        self.setup_file_structure_tab()
        self.setup_usage_code_tab()
        self.setup_environment_tab()
        self.setup_technologies_tab()
        self.setup_template_tab()
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
                "screenshot1": self.markdown_generator.get_field("screenshot1") or "",
                "screenshot2": self.markdown_generator.get_field("screenshot2") or ""
            }
        )
        self.image_gallery.pack(fill="both", expand=True, padx=20, pady=20)

    def update_images(self, image_type, value):
        """Update image fields in the markdown generator"""
        if image_type in ["DemoGif", "screenshot1", "screenshot2"]:
            self.update_field(image_type, value)
    
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
    
    def setup_file_structure_tab(self):
        tab = self.tabview.tab("File Structure")
        
        # Create file structure editor
        self.file_structure_editor = FileStructureEditor(
            tab,
            callback=lambda content: self.update_field("file_structure", content),
            initial_content=self.markdown_generator.get_field("file_structure")
        )
        self.file_structure_editor.pack(fill="both", expand=True)
        
    def setup_usage_code_tab(self):
        tab = self.tabview.tab("Usage Code")
        
        # Create usage code editor
        self.usage_code_editor = UsageCodeEditor(
            tab,
            callback=lambda content: self.update_field("usage_code", content),
            initial_content=self.markdown_generator.get_field("usage_code")
        )
        self.usage_code_editor.pack(fill="both", expand=True)
        
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
        CTkLabel(content_frame, text="Click on technologies to add them to your project. Add custom ones below.").pack(anchor="w", pady=(0, 10))
        
        # Create the technology selector
        self.tech_selector = TechnologySelector(
            content_frame,
            callback=lambda techs: self.update_field("tech", techs),
            initial_items=self.markdown_generator.get_field("tech") or []
        )
        self.tech_selector.pack(fill="both", expand=True)
    
    def setup_template_tab(self):
        tab = self.tabview.tab("Template")
        
        # Create template selector
        self.template_selector = TemplateSelector(
            tab,
            callback=lambda template: self.update_field("template", template),
            initial_template=self.markdown_generator.get_field("template") or "Standard"
        )
        self.template_selector.pack(fill="both", expand=True)
        
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
    
    def setup_status_bar(self):
        # Create a status bar at the bottom
        self.status_var = tk.StringVar(value="Ready")
        status_frame = CTkFrame(self)
        status_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 15))
        
        CTkLabel(status_frame, textvariable=self.status_var).pack(side="left", padx=15)
    
    def setup_action_buttons(self):
        """Add action buttons for global operations"""
        actions_frame = CTkFrame(self.main_frame)
        actions_frame.grid(row=1, column=0, sticky="ew", pady=(15, 0))
        
        # Left side buttons
        left_frame = CTkFrame(actions_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="y", padx=20, pady=10)
        
        CTkButton(
            left_frame, 
            text="New Project", 
            command=self.new_project,
            width=120,
            height=40,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        ).pack(side="left", padx=5)
        
        # Right side buttons
        right_frame = CTkFrame(actions_frame, fg_color="transparent")
        right_frame.pack(side="right", fill="y", padx=20, pady=10)
        
        CTkButton(
            right_frame, 
            text="Save README.md", 
            command=self.save_markdown,
            fg_color="#27ae60",
            hover_color="#219653",
            width=150,
            height=40
        ).pack(side="right", padx=5)
        
        CTkButton(
            right_frame, 
            text="Save Template", 
            command=self.save_template,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            width=120,
            height=40
        ).pack(side="right", padx=5)
        
        CTkButton(
            right_frame, 
            text="Load Template", 
            command=self.load_template,
            fg_color="#3498db",
            hover_color="#2980b9",
            width=120,
            height=40
        ).pack(side="right", padx=5)
        
        CTkButton(
            right_frame, 
            text="Copy to Clipboard", 
            command=self.copy_to_clipboard,
            width=150,
            height=40
        ).pack(side="right", padx=5)
        
    def update_field(self, field, value):
        """Update a field in the markdown generator"""
        try:
            self.status_var.set(f"Updated {field}")
            
            # Update data
            self.markdown_generator.update_field(field, value)
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
    
    def new_project(self):
        """Create a new project"""
        if messagebox.askyesno("New Project", "Are you sure you want to start a new project? All unsaved changes will be lost."):
            # Reset markdown generator
            self.markdown_generator.reset()
            
            # Reset form fields
            self.reset_form()
            
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
        self.tech_selector.reset()
        
        # Reset editors
        self.file_structure_editor.content_text.delete("0.0", "end")
        self.usage_code_editor.content_text.delete("0.0", "end")
        
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
            "screenshot1": data.get("screenshot1", ""),
            "screenshot2": data.get("screenshot2", "")
        })
        
        # Populate file structure and usage code
        self.file_structure_editor.content_text.delete("0.0", "end")
        self.file_structure_editor.content_text.insert("0.0", data.get("file_structure", ""))
        
        self.usage_code_editor.content_text.delete("0.0", "end")
        self.usage_code_editor.content_text.insert("0.0", data.get("usage_code", ""))
        
        # Populate additional info
        self.license_var.set(data.get("license", "MIT"))
        self.contact_var.set(data.get("contact", ""))
        
        # Populate managers
        self.prerequisites_manager.set_items(data.get("Prerequisites", []))
        self.env_vars_manager.set_items(data.get("envvars", []))
        
        # Populate technologies
        self.tech_selector.set_items(data.get("tech", []))
        
    def save_markdown(self):
        """Save markdown content to a file"""
        from tkinter import filedialog
        
        self.status_var.set("Generating markdown...")
        self.update_idletasks()
        
        try:
            # Generate markdown from current data
            markdown_content = self.markdown_generator.generate_markdown()
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".md",
                filetypes=[("Markdown Files", "*.md"), ("All Files", "*.*")],
                initialfile="README.md"
            )
            
            if file_path:
                try:
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(markdown_content)
                    messagebox.showinfo("Success", f"Markdown saved to {file_path}")
                    self.status_var.set(f"Markdown saved to {os.path.basename(file_path)}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save file: {str(e)}")
                    self.status_var.set(f"Error saving markdown: {str(e)}")
            else:
                self.status_var.set("Markdown save cancelled")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate markdown: {str(e)}")
            self.status_var.set(f"Error generating markdown: {str(e)}")
                
    def copy_to_clipboard(self):
        """Copy markdown content to clipboard"""
        try:
            # Generate markdown from current data
            markdown_content = self.markdown_generator.generate_markdown()
            
            self.clipboard_clear()
            self.clipboard_append(markdown_content)
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