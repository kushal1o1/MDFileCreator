import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import json
import os
from tkinter.font import Font
import markdown
import tkhtmlview

class MDCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MD File Creator")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Set theme and style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Data storage
        self.project_data = {
            "project_name": "",
            "username": "",
            "logo": "",
            "concisedesc": "",
            "overview": "",
            "features": [],
            "DemoGif": "",
            "screenshot1": "",
            "screenshot2": "",
            "Prerequisites": [],
            "envvars": [],
            "tech": [],
            "license": "MIT",
            "contact": ""
        }
        
        # Create main container
        self.main_container = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create form frame
        self.form_frame = ttk.Notebook(self.main_container)
        self.main_container.add(self.form_frame, weight=1)
        
        # Create preview frame
        self.preview_frame = ttk.Frame(self.main_container)
        self.main_container.add(self.preview_frame, weight=1)
        
        # Setup tabs
        self.setup_tabs()
        
        # Setup preview
        self.setup_preview()
        
        # Setup menu
        self.setup_menu()
        
        # Initial preview update
        self.update_preview()

    def configure_styles(self):
        # Configure ttk styles
        self.style.configure('TLabel', font=('Segoe UI', 10))
        self.style.configure('Header.TLabel', font=('Segoe UI', 12, 'bold'))
        self.style.configure('TButton', font=('Segoe UI', 10))
        self.style.configure('TEntry', font=('Segoe UI', 10))
        self.style.configure('TNotebook.Tab', font=('Segoe UI', 10))

    def setup_tabs(self):
        # Basic Info tab
        self.basic_tab = ttk.Frame(self.form_frame, padding=10)
        self.form_frame.add(self.basic_tab, text="Basic Info")
        self.setup_basic_tab()
        
        # Features tab
        self.features_tab = ttk.Frame(self.form_frame, padding=10)
        self.form_frame.add(self.features_tab, text="Features")
        self.setup_features_tab()
        
        # Media tab
        self.media_tab = ttk.Frame(self.form_frame, padding=10)
        self.form_frame.add(self.media_tab, text="Media")
        self.setup_media_tab()
        
        # Prerequisites tab
        self.prereq_tab = ttk.Frame(self.form_frame, padding=10)
        self.form_frame.add(self.prereq_tab, text="Prerequisites")
        self.setup_prereq_tab()
        
        # Environment Variables tab
        self.env_tab = ttk.Frame(self.form_frame, padding=10)
        self.form_frame.add(self.env_tab, text="Environment Vars")
        self.setup_env_tab()
        
        # Technologies tab
        self.tech_tab = ttk.Frame(self.form_frame, padding=10)
        self.form_frame.add(self.tech_tab, text="Technologies")
        self.setup_tech_tab()
        
        # Additional Info tab
        self.additional_tab = ttk.Frame(self.form_frame, padding=10)
        self.form_frame.add(self.additional_tab, text="Additional Info")
        self.setup_additional_tab()

    def setup_basic_tab(self):
        # Create form fields for basic project information
        ttk.Label(self.basic_tab, text="Project Information", style='Header.TLabel').grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        fields = [
            ("Project Name:", "project_name"),
            ("GitHub Username:", "username"),
            ("Concise Description:", "concisedesc"),
            ("Project Overview:", "overview")
        ]
        
        for i, (label_text, field_name) in enumerate(fields):
            ttk.Label(self.basic_tab, text=label_text).grid(row=i+1, column=0, sticky=tk.W, pady=5)
            
            if field_name == "overview":
                # Multiline text input for overview
                text_widget = scrolledtext.ScrolledText(self.basic_tab, wrap=tk.WORD, width=40, height=5)
                text_widget.grid(row=i+1, column=1, sticky=tk.W+tk.E, pady=5)
                text_widget.insert(tk.END, self.project_data[field_name])
                
                # Update data when text changes
                def on_text_change(event, field=field_name, widget=text_widget):
                    self.project_data[field] = widget.get("1.0", tk.END).strip()
                    self.update_preview()
                
                text_widget.bind("<KeyRelease>", on_text_change)
            else:
                # Single line text input
                var = tk.StringVar(value=self.project_data[field_name])
                entry = ttk.Entry(self.basic_tab, textvariable=var, width=40)
                entry.grid(row=i+1, column=1, sticky=tk.W+tk.E, pady=5)
                
                # Update data when entry changes
                def on_var_change(*args, field=field_name, variable=var):
                    self.project_data[field] = variable.get()
                    self.update_preview()
                
                var.trace_add("write", on_var_change)
        
        # Configure grid to expand
        self.basic_tab.columnconfigure(1, weight=1)

    def setup_features_tab(self):
        ttk.Label(self.features_tab, text="Project Features", style='Header.TLabel').grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
        
        # Features list frame
        list_frame = ttk.Frame(self.features_tab)
        list_frame.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW)
        
        # Features list
        self.features_listbox = tk.Listbox(list_frame, height=10, width=50)
        self.features_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar for features list
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.features_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.features_listbox.config(yscrollcommand=scrollbar.set)
        
        # Load existing features
        for feature in self.project_data["features"]:
            self.features_listbox.insert(tk.END, feature)
        
        # Add feature frame
        add_frame = ttk.Frame(self.features_tab)
        add_frame.grid(row=2, column=0, columnspan=3, sticky=tk.EW, pady=10)
        
        ttk.Label(add_frame, text="Feature:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.new_feature_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.new_feature_var, width=40).pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
        
        ttk.Button(add_frame, text="Add", command=self.add_feature).pack(side=tk.LEFT, padx=5)
        ttk.Button(add_frame, text="Remove Selected", command=self.remove_feature).pack(side=tk.LEFT)
        
        # Configure grid to expand
        self.features_tab.rowconfigure(1, weight=1)
        self.features_tab.columnconfigure(0, weight=1)

    def add_feature(self):
        feature = self.new_feature_var.get().strip()
        if feature:
            self.features_listbox.insert(tk.END, feature)
            self.project_data["features"] = list(self.features_listbox.get(0, tk.END))
            self.new_feature_var.set("")
            self.update_preview()

    def remove_feature(self):
        try:
            selection = self.features_listbox.curselection()[0]
            self.features_listbox.delete(selection)
            self.project_data["features"] = list(self.features_listbox.get(0, tk.END))
            self.update_preview()
        except IndexError:
            messagebox.showinfo("Info", "Please select a feature to remove.")

    def setup_media_tab(self):
        ttk.Label(self.media_tab, text="Media & Screenshots", style='Header.TLabel').grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
        
        fields = [
            ("Logo URL:", "logo", "Browse"),
            ("Demo GIF URL:", "DemoGif", "Browse"),
            ("Screenshot 1 URL:", "screenshot1", "Browse"),
            ("Screenshot 2 URL:", "screenshot2", "Browse")
        ]
        
        for i, (label_text, field_name, button_text) in enumerate(fields):
            ttk.Label(self.media_tab, text=label_text).grid(row=i+1, column=0, sticky=tk.W, pady=5)
            
            var = tk.StringVar(value=self.project_data[field_name])
            entry = ttk.Entry(self.media_tab, textvariable=var, width=40)
            entry.grid(row=i+1, column=1, sticky=tk.W+tk.E, pady=5)
            
            # Update data when entry changes
            def on_var_change(*args, field=field_name, variable=var):
                self.project_data[field] = variable.get()
                self.update_preview()
            
            var.trace_add("write", on_var_change)
            
            # Browse button
            def browse_file(field=field_name, variable=var):
                filename = filedialog.askopenfilename(
                    title=f"Select {field.capitalize()} File",
                    filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif"), ("All Files", "*.*")]
                )
                if filename:
                    # Use relative path if possible
                    try:
                        rel_path = os.path.relpath(filename)
                        variable.set(rel_path)
                    except ValueError:
                        variable.set(filename)
            
            ttk.Button(self.media_tab, text=button_text, command=browse_file).grid(row=i+1, column=2, padx=5, pady=5)
        
        # Configure grid to expand
        self.media_tab.columnconfigure(1, weight=1)

    def setup_prereq_tab(self):
        self.setup_list_tab(
            self.prereq_tab, 
            "Prerequisites", 
            "prerequisite", 
            "Prerequisites",
            self.project_data["Prerequisites"]
        )

    def setup_tech_tab(self):
        self.setup_list_tab(
            self.tech_tab, 
            "Technologies Used", 
            "technology", 
            "tech",
            self.project_data["tech"]
        )

    def setup_list_tab(self, tab, title, item_name, data_key, initial_items):
        ttk.Label(tab, text=title, style='Header.TLabel').grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
        
        # List frame
        list_frame = ttk.Frame(tab)
        list_frame.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW)
        
        # Create listbox
        listbox = tk.Listbox(list_frame, height=10, width=50)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar for list
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.config(yscrollcommand=scrollbar.set)
        
        # Load existing items
        for item in initial_items:
            listbox.insert(tk.END, item)
        
        # Add item frame
        add_frame = ttk.Frame(tab)
        add_frame.grid(row=2, column=0, columnspan=3, sticky=tk.EW, pady=10)
        
        ttk.Label(add_frame, text=f"{item_name.capitalize()}:").pack(side=tk.LEFT, padx=(0, 5))
        
        new_item_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=new_item_var, width=40).pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
        
        # Add function
        def add_item():
            item = new_item_var.get().strip()
            if item:
                listbox.insert(tk.END, item)
                self.project_data[data_key] = list(listbox.get(0, tk.END))
                new_item_var.set("")
                self.update_preview()
        
        # Remove function
        def remove_item():
            try:
                selection = listbox.curselection()[0]
                listbox.delete(selection)
                self.project_data[data_key] = list(listbox.get(0, tk.END))
                self.update_preview()
            except IndexError:
                messagebox.showinfo("Info", f"Please select a {item_name} to remove.")
        
        ttk.Button(add_frame, text="Add", command=add_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(add_frame, text="Remove Selected", command=remove_item).pack(side=tk.LEFT)
        
        # Configure grid to expand
        tab.rowconfigure(1, weight=1)
        tab.columnconfigure(0, weight=1)

    def setup_env_tab(self):
        ttk.Label(self.env_tab, text="Environment Variables", style='Header.TLabel').grid(row=0, column=0, columnspan=5, sticky=tk.W, pady=(0, 10))
        
        # Env vars frame with table-like structure
        table_frame = ttk.Frame(self.env_tab)
        table_frame.grid(row=1, column=0, columnspan=5, sticky=tk.NSEW)
        
        # Create table headers
        headers = ["Variable Name", "Description", "Default Value", ""]
        for i, header in enumerate(headers):
            ttk.Label(table_frame, text=header, font=('Segoe UI', 10, 'bold')).grid(row=0, column=i, padx=5, pady=5, sticky=tk.W)
        
        # Create scrollable frame for env vars
        canvas = tk.Canvas(table_frame)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
        self.env_vars_frame = ttk.Frame(canvas)
        
        # Configure scrolling
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.grid(row=1, column=0, columnspan=4, sticky=tk.NSEW)
        scrollbar.grid(row=1, column=4, sticky=tk.NS)
        canvas.create_window((0, 0), window=self.env_vars_frame, anchor=tk.NW)
        
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        self.env_vars_frame.bind("<Configure>", configure_scroll_region)
        
        # Load existing env vars
        self.refresh_env_vars_display()
        
        # Add env var frame
        add_frame = ttk.Frame(self.env_tab)
        add_frame.grid(row=2, column=0, columnspan=5, sticky=tk.EW, pady=10)
        
        # Entry fields for new env var
        ttk.Label(add_frame, text="Name:").grid(row=0, column=0, padx=5)
        self.new_env_name = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.new_env_name, width=15).grid(row=0, column=1, padx=5)
        
        ttk.Label(add_frame, text="Description:").grid(row=0, column=2, padx=5)
        self.new_env_desc = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.new_env_desc, width=25).grid(row=0, column=3, padx=5)
        
        ttk.Label(add_frame, text="Default:").grid(row=0, column=4, padx=5)
        self.new_env_value = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.new_env_value, width=15).grid(row=0, column=5, padx=5)
        
        ttk.Button(add_frame, text="Add Variable", command=self.add_env_var).grid(row=0, column=6, padx=5)
        
        # Configure grid to expand
        self.env_tab.rowconfigure(1, weight=1)
        self.env_tab.columnconfigure(0, weight=1)
        table_frame.rowconfigure(1, weight=1)
        table_frame.columnconfigure(0, weight=1)
        table_frame.columnconfigure(1, weight=2)
        table_frame.columnconfigure(2, weight=1)

    def refresh_env_vars_display(self):
        # Clear existing widgets
        for widget in self.env_vars_frame.winfo_children():
            widget.destroy()
        
        # Add env vars to the frame
        for i, env_var in enumerate(self.project_data["envvars"]):
            ttk.Label(self.env_vars_frame, text=env_var["name"]).grid(row=i, column=0, padx=5, pady=2, sticky=tk.W)
            ttk.Label(self.env_vars_frame, text=env_var["desc"]).grid(row=i, column=1, padx=5, pady=2, sticky=tk.W)
            ttk.Label(self.env_vars_frame, text=env_var["value"]).grid(row=i, column=2, padx=5, pady=2, sticky=tk.W)
            
            # Delete button
            def make_remove_func(index):
                return lambda: self.remove_env_var(index)
            
            ttk.Button(
                self.env_vars_frame, 
                text="Remove", 
                command=make_remove_func(i)
            ).grid(row=i, column=3, padx=5, pady=2)

    def add_env_var(self):
        name = self.new_env_name.get().strip()
        desc = self.new_env_desc.get().strip()
        value = self.new_env_value.get().strip()
        
        if name and desc:
            self.project_data["envvars"].append({
                "name": name,
                "desc": desc,
                "value": value
            })
            
            # Clear inputs
            self.new_env_name.set("")
            self.new_env_desc.set("")
            self.new_env_value.set("")
            
            # Refresh display
            self.refresh_env_vars_display()
            self.update_preview()

    def remove_env_var(self, index):
        if 0 <= index < len(self.project_data["envvars"]):
            del self.project_data["envvars"][index]
            self.refresh_env_vars_display()
            self.update_preview()

    def setup_additional_tab(self):
        ttk.Label(self.additional_tab, text="Additional Information", style='Header.TLabel').grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        fields = [
            ("License:", "license"),
            ("Contact Information:", "contact")
        ]
        
        for i, (label_text, field_name) in enumerate(fields):
            ttk.Label(self.additional_tab, text=label_text).grid(row=i+1, column=0, sticky=tk.W, pady=5)
            
            var = tk.StringVar(value=self.project_data[field_name])
            entry = ttk.Entry(self.additional_tab, textvariable=var, width=40)
            entry.grid(row=i+1, column=1, sticky=tk.W+tk.E, pady=5)
            
            # Update data when entry changes
            def on_var_change(*args, field=field_name, variable=var):
                self.project_data[field] = variable.get()
                self.update_preview()
            
            var.trace_add("write", on_var_change)
        
        # Configure grid to expand
        self.additional_tab.columnconfigure(1, weight=1)

    def setup_preview(self):
        ttk.Label(self.preview_frame, text="Markdown Preview", style='Header.TLabel').pack(anchor=tk.W, pady=(0, 10))
        
        # Create tabbed interface for preview
        preview_notebook = ttk.Notebook(self.preview_frame)
        preview_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Markdown source tab
        self.markdown_frame = ttk.Frame(preview_notebook)
        preview_notebook.add(self.markdown_frame, text="Markdown Source")
        
        # HTML preview tab
        self.html_frame = ttk.Frame(preview_notebook)
        preview_notebook.add(self.html_frame, text="HTML Preview")
        
        # Markdown source text widget
        self.markdown_text = scrolledtext.ScrolledText(self.markdown_frame, wrap=tk.WORD, font=("Courier New", 10))
        self.markdown_text.pack(fill=tk.BOTH, expand=True)
        
        # HTML preview widget (using tkhtmlview)
        self.html_view = tkhtmlview.HTMLScrolledText(self.html_frame, width=1, height=1)
        self.html_view.pack(fill=tk.BOTH, expand=True)
        
        # Buttons frame
        buttons_frame = ttk.Frame(self.preview_frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(buttons_frame, text="Save README.md", command=self.save_markdown).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons_frame, text="Copy to Clipboard", command=self.copy_to_clipboard).pack(side=tk.RIGHT, padx=5)

    def setup_menu(self):
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_project)
        file_menu.add_command(label="Save Template", command=self.save_template)
        file_menu.add_command(label="Load Template", command=self.load_template)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)

    def update_preview(self):
        """Generate and display markdown preview"""
        try:
            markdown_content = self.generate_readme(self.project_data)
            
            # Update markdown source view
            self.markdown_text.delete(1.0, tk.END)
            self.markdown_text.insert(tk.END, markdown_content)
            
            # Update HTML preview
            html_content = markdown.markdown(markdown_content, extensions=['tables'])
            self.html_view.set_html(html_content)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate preview: {str(e)}")

    def generate_readme(self, details):
        """Generate README.md content from project details"""
        readme_content = f"""# {details['project_name']}

<p align="center">
  <img src="{details['logo']}" alt="Project Logo" width="200" height="200">
</p>

<p align="center">
  <a href="https://github.com/{details['username']}/{details['project_name']}/stargazers"><img src="https://img.shields.io/github/stars/{details['username']}/{details['project_name']}" alt="Stars Badge"/></a>
  <a href="https://github.com/{details['username']}/{details['project_name']}/network/members"><img src="https://img.shields.io/github/forks/{details['username']}/{details['project_name']}" alt="Forks Badge"/></a>
  <a href="https://github.com/{details['username']}/{details['project_name']}/pulls"><img src="https://img.shields.io/github/issues-pr/{details['username']}/{details['project_name']}" alt="Pull Requests Badge"/></a>
  <a href="https://github.com/{details['username']}/{details['project_name']}/issues"><img src="https://img.shields.io/github/issues/{details['username']}/{details['project_name']}" alt="Issues Badge"/></a>
  <a href="https://github.com/{details['username']}/{details['project_name']}/graphs/contributors"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/{details['username']}/{details['project_name']}?color=2b9348"></a>
</p>

<p align="center">
  <b>{details["concisedesc"]}</b>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#demo">Demo</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#configuration">Configuration</a> •
  <a href="#api-reference">API Reference</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#roadmap">Roadmap</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a> •
  <a href="#contact">Contact</a> •
  <a href="#acknowledgments">Acknowledgments</a>
</p>


## Overview

{details['overview']}

## Features

"""
        for feature in details['features']:
            readme_content += f"- **{feature}**\n"
        
        readme_content += f"""

## Demo

<p align="center">
  <img src="{details['DemoGif']}" alt="Demo" width="600">
</p>

## Screenshot
![Screenshot 1]({details['screenshot1']})
![Screenshot 2]({details['screenshot2']})

## Installation
```bash
# Clone the repository
git clone https://github.com/{details['username']}/{details['project_name']}.git

# Navigate to the project directory
cd {details['project_name']}

# Install dependencies
npm install
# or
yarn install
# or
pip install -r requirements.txt
```

### Prerequisites
"""
        for prerequisite in details['Prerequisites']:
            readme_content += f"- **{prerequisite}**\n"
        
        readme_content += f"""

## Usage

```javascript
doSomething();
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
"""
        for envvar in details['envvars']:
                readme_content += f"| `{envvar['name']}` | {envvar['desc']} | `{envvar['value']}` |\n"
        
        readme_content += f"""

## Directory Structure

```
project-name/
├── .github/           # GitHub specific files (workflows, templates)
├── docs/              # Documentation files
├── src/               # Source code
│   ├── components/    # UI components (for frontend projects)
│   ├── utils/         # Utility functions
│   └── index.js       # Entry point
├── tests/             # Test files
├── .gitignore         # Git ignore file
├── LICENSE            # License file
├── package.json       # Project dependencies and scripts
└── README.md          # Project documentation (this file)
```

## Technologies Used

<p align="center">
"""
        for tech in details['tech']:
            readme_content += f'<img src="https://img.shields.io/badge/{tech}-%23007ACC.svg?style=for-the-badge&logo={tech}&logoColor=white"  alt="{tech}">\n'
        
        readme_content += f"""
</p>

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please make sure to update tests as appropriate and adhere to the [code of conduct](CODE_OF_CONDUCT.md).

## License

This project is licensed under the {details['license']} License.

## Contact

{details['contact']}

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/{details['username']}">{details['username']}</a>
</p>
"""
        return readme_content

    def save_markdown(self):
        """Save markdown content to a file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown Files", "*.md"), ("All Files", "*.*")],
            initialfile="README.md"
        )
        
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.markdown_text.get(1.0, tk.END))
                messagebox.showinfo("Success", f"Markdown saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")

    def copy_to_clipboard(self):
        """Copy markdown content to clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(self.markdown_text.get(1.0, tk.END))
        messagebox.showinfo("Success", "Markdown copied to clipboard")

    def new_project(self):
        """Reset all form fields for a new project"""
        if messagebox.askyesno("New Project", "Are you sure you want to start a new project? All unsaved changes will be lost."):
            self.project_data = {
                "project_name": "",
                "username": "",
                "logo": "",
                "concisedesc": "",
                "overview": "",
                "features": [],
                "DemoGif": "",
                "screenshot1": "",
                "screenshot2": "",
                "Prerequisites": [],
                "envvars": [],
                "tech": [],
                "license": "MIT",
                "contact": ""
            }
            
            # Reset to first tab
            self.form_frame.select(0)
            
            # Recreate all tabs to reset fields
            for widget in self.form_frame.winfo_children():
                widget.destroy()
            
            self.setup_tabs()
            self.update_preview()

    def save_template(self):
        """Save current project data as a template"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
            initialfile="template.json"
        )
        
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(self.project_data, file, indent=2)
                messagebox.showinfo("Success", f"Template saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save template: {str(e)}")

    def load_template(self):
        """Load project data from a template file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    self.project_data = json.load(file)
                
                # Recreate all tabs to update fields
                for widget in self.form_frame.winfo_children():
                    widget.destroy()
                
                self.setup_tabs()
                self.update_preview()
                messagebox.showinfo("Success", f"Template loaded from {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load template: {str(e)}")

    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About MD File Creator",
            "MD File Creator v1.0\n\n"
            "A professional desktop application for creating beautiful Markdown files.\n\n"
            "© 2023 MD File Creator"
        )

def main():
    # Check for required packages and install if missing
    try:
        import markdown
        import tkhtmlview
    except ImportError:
        import subprocess
        import sys
        
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown", "tkhtmlview"])
        
        # Import again after installation
        import markdown
        import tkhtmlview
    
    root = tk.Tk()
    app = MDCreatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 