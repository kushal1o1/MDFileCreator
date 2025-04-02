class MarkdownGenerator:
    """A class to generate markdown README files"""
    
    def __init__(self):
        """Initialize with default empty values"""
        self.data = {
            "project_name": "",
            "username": "",
            "concisedesc": "",
            "overview": "",
            "features": [],
            "logo": "",
            "DemoGif": "",
            "screenshots": [],  # Now an array of screenshot URLs
            "Prerequisites": [],
            "envvars": [],
            "tech": [],
            "license": "MIT",
            "contact": ""
        }
    
    def update_field(self, field, value):
        """Update a specific field"""
        if field in self.data:
            self.data[field] = value
    
    def get_field(self, field):
        """Get the value of a field"""
        return self.data.get(field, "")
    
    def get_data(self):
        """Get all data"""
        return self.data
    
    def set_data(self, data):
        """Set all data at once"""
        for key, value in data.items():
            if key in self.data:
                self.data[key] = value
    
    def reset(self):
        """Reset all fields to empty values"""
        self.__init__()
    
    def generate_markdown(self):
        """Generate markdown from data"""
        md = []
        
        # Add logo if available
        logo = self.data.get("logo", "").strip()
        if logo:
            md.append(f"<div align=\"center\">\n  <img src=\"{logo}\" alt=\"{self.data.get('project_name', 'Project')} Logo\" width=\"200\">\n</div>\n")
            
        # Title
        project_name = self.data.get("project_name", "").strip()
        if project_name:
            md.append(f"# {project_name}")
        else:
            md.append("# Project Title")
        
        # Add badges if we have username/project
        username = self.data.get("username", "").strip()
        if username and project_name:
            md.append("\n<div align=\"center\">")
            md.append(f"  <a href=\"https://github.com/{username}/{project_name}/stargazers\"><img src=\"https://img.shields.io/github/stars/{username}/{project_name}\" alt=\"Stars Badge\"/></a>")
            md.append(f"  <a href=\"https://github.com/{username}/{project_name}/network/members\"><img src=\"https://img.shields.io/github/forks/{username}/{project_name}\" alt=\"Forks Badge\"/></a>")
            md.append(f"  <a href=\"https://github.com/{username}/{project_name}/pulls\"><img src=\"https://img.shields.io/github/issues-pr/{username}/{project_name}\" alt=\"Pull Requests Badge\"/></a>")
            md.append(f"  <a href=\"https://github.com/{username}/{project_name}/issues\"><img src=\"https://img.shields.io/github/issues/{username}/{project_name}\" alt=\"Issues Badge\"/></a>")
            md.append(f"  <a href=\"https://github.com/{username}/{project_name}/blob/master/LICENSE\"><img src=\"https://img.shields.io/github/license/{username}/{project_name}\" alt=\"License Badge\"/></a>")
            md.append("</div>\n")
        
        # Concise description
        concisedesc = self.data.get("concisedesc", "").strip()
        if concisedesc:
            md.append(f"\n> {concisedesc}\n")
        
        # Demo GIF
        demo_gif = self.data.get("DemoGif", "").strip()
        if demo_gif:
            md.append("\n<div align=\"center\">")
            md.append(f"  <img src=\"{demo_gif}\" alt=\"{project_name} Demo\" width=\"600\">")
            md.append("</div>\n")
        
        # Overview
        overview = self.data.get("overview", "").strip()
        if overview:
            md.append("\n## Overview\n")
            md.append(overview)
        
        # Table of Contents
        md.append("\n## Table of Contents\n")
        sections = []
        
        if self.data.get("features", []):
            sections.append("- [Features](#features)")
        
        if self.data.get("screenshots", []):
            sections.append("- [Screenshots](#screenshots)")
            
        sections.append("- [Installation](#installation)")
        
        if self.data.get("Prerequisites", []):
            sections.append("- [Prerequisites](#prerequisites)")
            
        sections.append("- [Usage](#usage)")
        
        if self.data.get("envvars", []):
            sections.append("- [Environment Variables](#environment-variables)")
            
        if self.data.get("tech", []):
            sections.append("- [Technologies Used](#technologies-used)")
            
        sections.append("- [License](#license)")
        
        if self.data.get("contact", "").strip():
            sections.append("- [Contact](#contact)")
            
        md.append("\n".join(sections))
        
        # Features
        features = self.data.get("features", [])
        if features:
            md.append("\n## Features\n")
            for feature in features:
                md.append(f"- {feature}")
        
        # Screenshots section
        screenshots = self.data.get("screenshots", [])
        if screenshots:
            md.append("\n## Screenshots\n")
            for i, screenshot in enumerate(screenshots):
                if screenshot.strip():
                    md.append(f"\n<div align=\"center\">")
                    md.append(f"  <img src=\"{screenshot}\" alt=\"Screenshot {i+1}\" width=\"600\">")
                    md.append(f"  <p><em>Screenshot {i+1}</em></p>")
                    md.append("</div>")
        
        # Installation
        md.append("\n## Installation\n")
        
        if username and project_name:
            md.append("```bash")
            md.append(f"# Clone the repository")
            md.append(f"git clone https://github.com/{username}/{project_name}.git")
            md.append(f"cd {project_name}")
            md.append("")
            md.append(f"# Install dependencies")
            md.append(f"npm install  # or pip install -r requirements.txt for Python projects")
            md.append("```")
        else:
            md.append("```bash")
            md.append("# Clone the repository")
            md.append("git clone https://github.com/username/repo.git")
            md.append("cd repo")
            md.append("")
            md.append("# Install dependencies")
            md.append("npm install  # or pip install -r requirements.txt for Python projects")
            md.append("```")
        
        # Prerequisites
        prerequisites = self.data.get("Prerequisites", [])
        if prerequisites:
            md.append("\n## Prerequisites\n")
            for prerequisite in prerequisites:
                md.append(f"- {prerequisite}")
        
        # Usage
        md.append("\n## Usage\n")
        md.append("```bash")
        md.append("# Run the application")
        if project_name:
            md.append(f"npm start  # or python main.py for Python projects")
        else:
            md.append("npm start  # or python main.py for Python projects")
        md.append("```\n")
        md.append("Here's how to use the project after installation.")
        
        # Environment Variables
        env_vars = self.data.get("envvars", [])
        if env_vars:
            md.append("\n## Environment Variables\n")
            md.append("Create a `.env` file in the root directory and add the following variables:\n")
            md.append("```env")
            for var in env_vars:
                md.append(f"{var['name']}={var['value']}  # {var['desc']}")
            md.append("```")
        
        # Technologies
        tech = self.data.get("tech", [])
        if tech:
            md.append("\n## Technologies Used\n")
            for i, technology in enumerate(tech):
                if i > 0 and i % 3 == 0:
                    md.append("<br>")
                md.append(f"![{technology}](https://img.shields.io/badge/-{technology}-05122A?style=flat&logo={technology.lower()}) ")
        
        # License
        license_type = self.data.get("license", "MIT").strip()
        md.append(f"\n## License\n")
        md.append(f"This project is licensed under the {license_type} License - see the LICENSE file for details.")
        
        # Contact
        contact = self.data.get("contact", "").strip()
        if contact:
            md.append("\n## Contact\n")
            md.append(contact)
            
            if username:
                md.append(f"\nConnect with me on [GitHub](https://github.com/{username}).")
        
        return "\n".join(md) 