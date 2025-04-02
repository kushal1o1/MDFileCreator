class MarkdownGenerator:
    """A class to generate markdown README files with multiple design templates"""
    
    # Define available templates
    TEMPLATES = ["Standard", "Minimalist", "Detailed", "Modern", "Corporate"]
    
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
            "screenshot1": "",
            "screenshot2": "",
            "Prerequisites": [],
            "envvars": [],
            "tech": [],
            "license": "MIT",
            "contact": "",
            "file_structure": "",
            "usage_code": "",
            "template": "Standard"
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
        """Generate markdown from data using the selected template"""
        template = self.data.get("template", "Standard")
        
        if template == "Minimalist":
            return self._generate_minimalist_template()
        elif template == "Detailed":
            return self._generate_detailed_template()
        elif template == "Modern":
            return self._generate_modern_template()
        elif template == "Corporate":
            return self._generate_corporate_template()
        else:
            # Default to Standard template
            return self._generate_standard_template()
    
    def _generate_standard_template(self):
        """Generate markdown with the standard template"""
        md = []
        
        # Project Title
        project_name = self.data.get("project_name", "").strip()
        if project_name:
            md.append(f"# {project_name}")
        else:
            md.append("# Project Title")
        
        # Logo
        logo = self.data.get("logo", "").strip()
        if not logo:
            logo = "path/to/logo.png"
        md.append("\n<p align=\"center\">")
        md.append(f"  <img src=\"{logo}\" alt=\"Project Logo\" width=\"200\" height=\"200\">")
        md.append("</p>")
        
        # Badges
        username = self.data.get("username", "").strip()
        if not username:
            username = "username"
        if project_name:
            md.append("\n<p align=\"center\">")
            md.append(f"  <a href=\"https://github.com/{username}/{project_name}/stargazers\"><img src=\"https://img.shields.io/github/stars/{username}/{project_name}\" alt=\"Stars Badge\"/></a>")
            md.append(f"  <a href=\"https://github.com/{username}/{project_name}/network/members\"><img src=\"https://img.shields.io/github/forks/{username}/{project_name}\" alt=\"Forks Badge\"/></a>")
            md.append(f"  <a href=\"https://github.com/{username}/{project_name}/pulls\"><img src=\"https://img.shields.io/github/issues-pr/{username}/{project_name}\" alt=\"Pull Requests Badge\"/></a>")
            md.append(f"  <a href=\"https://github.com/{username}/{project_name}/issues\"><img src=\"https://img.shields.io/github/issues/{username}/{project_name}\" alt=\"Issues Badge\"/></a>")
            md.append(f"  <a href=\"https://github.com/{username}/{project_name}/graphs/contributors\"><img alt=\"GitHub contributors\" src=\"https://img.shields.io/github/contributors/{username}/{project_name}?color=2b9348\"></a>")
            md.append("</p>")
        
        # Concise description
        concisedesc = self.data.get("concisedesc", "").strip()
        if concisedesc:
            md.append("\n<p align=\"center\">")
            md.append(f"  <b>{concisedesc}</b>")
            md.append("</p>")
        
        # Navigation links
        md.append("\n<p align=\"center\">")
        md.append("  <a href=\"#features\">Features</a> •")
        md.append("  <a href=\"#demo\">Demo</a> •")
        md.append("  <a href=\"#installation\">Installation</a> •")
        md.append("  <a href=\"#usage\">Usage</a> •")
        md.append("  <a href=\"#configuration\">Configuration</a> •")
        md.append("  <a href=\"#api-reference\">API Reference</a> •")
        md.append("  <a href=\"#documentation\">Documentation</a> •")
        md.append("  <a href=\"#roadmap\">Roadmap</a> •")
        md.append("  <a href=\"#contributing\">Contributing</a> •")
        md.append("  <a href=\"#license\">License</a> •")
        md.append("  <a href=\"#contact\">Contact</a> •")
        md.append("  <a href=\"#acknowledgments\">Acknowledgments</a>")
        md.append("</p>")
        
        # Overview
        overview = self.data.get("overview", "").strip()
        md.append("\n\n## Overview\n")
        if overview:
            md.append(overview)
        else:
            md.append("Add your project overview here...")
        
        # Features
        features = self.data.get("features", [])
        md.append("\n## Features\n")
        if features:
            for feature in features:
                md.append(f"- **{feature}**")
        else:
            md.append("- **Feature 1**: Description")
            md.append("- **Feature 2**: Description")
            md.append("- **Feature 3**: Description")
        
        # Demo
        demo_gif = self.data.get("DemoGif", "").strip()
        if not demo_gif:
            demo_gif = "path/to/demo.gif"
        md.append("\n\n## Demo\n")
        md.append("<p align=\"center\">")
        md.append(f"  <img src=\"{demo_gif}\" alt=\"Demo\" width=\"600\">")
        md.append("</p>")
        
        # Screenshots
        screenshot1 = self.data.get("screenshot1", "").strip()
        screenshot2 = self.data.get("screenshot2", "").strip()
        
        if not screenshot1:
            screenshot1 = "path/to/screenshot1.png"
        if not screenshot2:
            screenshot2 = "path/to/screenshot2.png"
        
        md.append("\n## Screenshot")
        md.append(f"![Screenshot 1]({screenshot1})")
        md.append(f"![Screenshot 2]({screenshot2})")
        
        # Installation
        md.append("\n## Installation")
        md.append("```bash")
        if username and project_name:
            md.append(f"# Clone the repository")
            md.append(f"git clone https://github.com/{username}/{project_name}.git")
            md.append(f"")
            md.append(f"# Navigate to the project directory")
            md.append(f"cd {project_name}")
        else:
            md.append("# Clone the repository")
            md.append("git clone https://github.com/username/project-name.git")
            md.append("")
            md.append("# Navigate to the project directory")
            md.append("cd project-name")
        
        md.append("")
        md.append("# Install dependencies")
        md.append("npm install")
        md.append("# or")
        md.append("yarn install")
        md.append("# or")
        md.append("pip install -r requirements.txt")
        md.append("```")
        
        # Prerequisites
        prerequisites = self.data.get("Prerequisites", [])
        md.append("\n### Prerequisites")
        if prerequisites:
            for prerequisite in prerequisites:
                md.append(f"- **{prerequisite}**")
        else:
            md.append("- **Node.js**: v14.0 or higher")
            md.append("- **npm/yarn**: Latest version recommended")
        
        # Usage
        md.append("\n## Usage\n")
        usage_code = self.data.get("usage_code", "").strip()
        if usage_code:
            md.append("```javascript")
            md.append(usage_code)
            md.append("```")
        else:
            md.append("```javascript")
            md.append("doSomething();")
            md.append("```")
        
        # Configuration
        md.append("\n## Configuration\n")
        md.append("### Configuration File\n")
        md.append("Create a `config.json` file in the root directory with the following structure:\n")
        md.append("```json")
        md.append("nth")
        md.append("```")
        
        # Environment Variables
        env_vars = self.data.get("envvars", [])
        md.append("\n### Environment Variables\n")
        md.append("| Variable | Description | Default |")
        md.append("|----------|-------------|---------|")
        
        if env_vars:
            for envvar in env_vars:
                md.append(f"| `{envvar['name']}` | {envvar['desc']} | `{envvar['value']}` |")
        else:
            md.append("| `API_KEY` | Your API key | `null` |")
            md.append("| `DEBUG` | Enable debug mode | `false` |")
        
        # Directory Structure
        md.append("\n## Directory Structure\n")
        file_structure = self.data.get("file_structure", "").strip()
        if file_structure:
            md.append("```")
            md.append(file_structure)
            md.append("```")
        else:
            md.append("```")
            md.append("project-name/")
            md.append("├── .github/           # GitHub specific files (workflows, templates)")
            md.append("├── docs/              # Documentation files")
            md.append("├── src/               # Source code")
            md.append("│   ├── components/    # UI components (for frontend projects)")
            md.append("│   ├── utils/         # Utility functions")
            md.append("│   └── index.js       # Entry point")
            md.append("├── tests/             # Test files")
            md.append("├── .gitignore         # Git ignore file")
            md.append("├── LICENSE            # License file")
            md.append("├── package.json       # Project dependencies and scripts")
            md.append("└── README.md          # Project documentation (this file)")
            md.append("```")
        
        # Technologies
        tech = self.data.get("tech", [])
        md.append("\n## Technologies Used\n")
        md.append("<p align=\"center\">")
        
        if tech:
            for technology in tech:
                md.append(f"<img src=\"https://img.shields.io/badge/{technology}-%23007ACC.svg?style=for-the-badge&logo={technology}&logoColor=white\" alt=\"{technology}\">")
        else:
            md.append("<img src=\"https://img.shields.io/badge/JavaScript-%23F7DF1E.svg?style=for-the-badge&logo=javascript&logoColor=black\" alt=\"JavaScript\">")
            md.append("<img src=\"https://img.shields.io/badge/TypeScript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white\" alt=\"TypeScript\">")
            md.append("<img src=\"https://img.shields.io/badge/React-%2361DAFB.svg?style=for-the-badge&logo=react&logoColor=black\" alt=\"React\">")
        
        md.append("</p>")
        
        # Contributing
        md.append("\n## Contributing\n")
        md.append("Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.\n")
        md.append("1. Fork the Project")
        md.append("2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)")
        md.append("3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)")
        md.append("4. Push to the Branch (`git push origin feature/AmazingFeature`)")
        md.append("5. Open a Pull Request\n")
        md.append("Please make sure to update tests as appropriate and adhere to the [code of conduct](CODE_OF_CONDUCT.md).")
        
        # License
        license_type = self.data.get("license", "MIT").strip()
        md.append("\n## License\n")
        md.append(f"This project is licensed under the {license_type} License.")
        
        # Contact
        contact = self.data.get("contact", "").strip()
        md.append("\n## Contact\n")
        if contact:
            md.append(contact)
        else:
            md.append("Your Name - [@your_twitter](https://twitter.com/your_twitter) - your_email@example.com")
        
        # Footer
        md.append("\n---\n")
        md.append("<p align=\"center\">")
        md.append("  Made with ❤️ by <a href=\"https://github.com/kushal1o1/MDFileCreator\">MdCreator</a>")
        md.append("</p>")
        
        return "\n".join(md)

    def _generate_minimalist_template(self):
        """Generate markdown with a minimalist template"""
        md = []
        
        # Project Title
        project_name = self.data.get("project_name", "").strip()
        if project_name:
            md.append(f"# {project_name}")
        else:
            md.append("# Project Title")
        
        # Concise description
        concisedesc = self.data.get("concisedesc", "").strip()
        if concisedesc:
            md.append(f"\n> {concisedesc}")
        
        # Overview
        overview = self.data.get("overview", "").strip()
        if overview:
            md.append(f"\n{overview}")
        
        # Demo
        demo_gif = self.data.get("DemoGif", "").strip()
        if demo_gif:
            md.append(f"\n![Demo]({demo_gif})")
        
        # Features
        features = self.data.get("features", [])
        if features:
            md.append("\n## Features")
            for feature in features:
                md.append(f"- {feature}")
        
        # Installation
        md.append("\n## Installation")
        username = self.data.get("username", "").strip() or "username"
        
        md.append("```bash")
        if project_name:
            md.append(f"git clone https://github.com/{username}/{project_name}.git")
            md.append(f"cd {project_name}")
        else:
            md.append("git clone https://github.com/username/project.git")
            md.append("cd project")
        md.append("```")
        
        # Usage
        md.append("\n## Usage")
        usage_code = self.data.get("usage_code", "").strip()
        if usage_code:
            md.append("\n```")
            md.append(usage_code)
            md.append("```")
        
        # License
        license_type = self.data.get("license", "MIT").strip()
        md.append(f"\n## License\n{license_type}")
        
        # Footer
        md.append("\n---\n")
        md.append("Made with ❤️ by [MdCreator](https://github.com/kushal1o1/MDFileCreator)")
        
        return "\n".join(md)
    
    def _generate_modern_template(self):
        """Generate markdown with a modern template"""
        md = []
        
        # Header with logo and title
        project_name = self.data.get("project_name", "").strip() or "Project Title"
        logo = self.data.get("logo", "").strip()
        
        md.append("<div align=\"center\">")
        
        if logo:
            md.append(f"\n  <img src=\"{logo}\" alt=\"logo\" width=\"200\" height=\"auto\" />")
        
        md.append(f"  <h1>{project_name}</h1>")
        
        # Badges
        username = self.data.get("username", "").strip() or "username"
        if project_name:
            md.append("  <p>")
            md.append(f"    <img src=\"https://img.shields.io/badge/version-1.0.0-blue?style=for-the-badge\" alt=\"version\" />")
            md.append(f"    <img src=\"https://img.shields.io/github/license/{username}/{project_name}?style=for-the-badge\" alt=\"license\" />")
            md.append("  </p>")
        
        # Concise description
        concisedesc = self.data.get("concisedesc", "").strip()
        if concisedesc:
            md.append(f"\n  <p><em>{concisedesc}</em></p>")
        
        md.append("\n</div>")
        
        # Demo GIF
        demo_gif = self.data.get("DemoGif", "").strip()
        if demo_gif:
            md.append("\n<div align=\"center\">")
            md.append(f"  <img src=\"{demo_gif}\" alt=\"demo\" />")
            md.append("</div>")
        
        # Overview
        overview = self.data.get("overview", "").strip()
        md.append("\n## 📋 Overview")
        if overview:
            md.append(f"\n{overview}")
        
        # Features
        features = self.data.get("features", [])
        md.append("\n## ✨ Features")
        if features:
            for feature in features:
                md.append(f"\n- 🔸 **{feature}**")
        
        # Screenshots
        screenshot1 = self.data.get("screenshot1", "").strip()
        screenshot2 = self.data.get("screenshot2", "").strip()
        
        if screenshot1 or screenshot2:
            md.append("\n## 📸 Screenshots")
            
            if screenshot1:
                md.append(f"\n<img src=\"{screenshot1}\" alt=\"Screenshot 1\" width=\"400\" />")
            
            if screenshot2:
                md.append(f"\n<img src=\"{screenshot2}\" alt=\"Screenshot 2\" width=\"400\" />")
        
        # Installation
        md.append("\n## 🚀 Getting Started")
        md.append("\n### Prerequisites")
        prerequisites = self.data.get("Prerequisites", [])
        if prerequisites:
            for prerequisite in prerequisites:
                md.append(f"- {prerequisite}")
        
        md.append("\n### Installation")
        md.append("\n```bash")
        if project_name:
            md.append(f"git clone https://github.com/{username}/{project_name}.git")
            md.append(f"cd {project_name}")
        else:
            md.append("git clone https://github.com/username/project.git")
            md.append("cd project")
        md.append("# Install dependencies")
        md.append("npm install  # or yarn install")
        md.append("```")
        
        # Usage
        md.append("\n## 📖 Usage")
        usage_code = self.data.get("usage_code", "").strip()
        if usage_code:
            md.append("\n```")
            md.append(usage_code)
            md.append("```")
        
        # Project Structure
        file_structure = self.data.get("file_structure", "").strip()
        if file_structure:
            md.append("\n## 📁 Project Structure")
            md.append("\n```")
            md.append(file_structure)
            md.append("```")
        
        # Environment Variables
        env_vars = self.data.get("envvars", [])
        if env_vars:
            md.append("\n## ⚙️ Configuration")
            md.append("\n### Environment Variables")
            md.append("\n| Variable | Description | Default |")
            md.append("|----------|-------------|---------|")
            for envvar in env_vars:
                md.append(f"| `{envvar['name']}` | {envvar['desc']} | `{envvar['value']}` |")
        
        # Technologies
        tech = self.data.get("tech", [])
        if tech:
            md.append("\n## 🛠️ Technologies")
            md.append("\n<div align=\"center\">")
            
            for technology in tech:
                md.append(f"\n<img src=\"https://img.shields.io/badge/{technology}-%23007ACC.svg?style=for-the-badge&logo={technology}&logoColor=white\" alt=\"{technology}\" />")
            
            md.append("\n</div>")
        
        # License
        license_type = self.data.get("license", "MIT").strip()
        md.append(f"\n## 📝 License")
        md.append(f"\nThis project is licensed under the {license_type} License.")
        
        # Contact
        contact = self.data.get("contact", "").strip()
        if contact:
            md.append("\n## 📬 Contact")
            md.append(f"\n{contact}")
        
        # Footer
        md.append("\n---\n")
        md.append("<div align=\"center\">")
        md.append("  <p>Made with ❤️ by <a href=\"https://github.com/kushal1o1/MDFileCreator\">MdCreator</a></p>")
        md.append("</div>")
        
        return "\n".join(md)
    
    def _generate_detailed_template(self):
        """Generate markdown with a detailed template"""
        md = []
        
        # Title and description
        project_name = self.data.get("project_name", "").strip() or "Project Title"
        md.append(f"# {project_name}")
        
        # Badges
        username = self.data.get("username", "").strip() or "username"
        if project_name:
            md.append("\n[![License](https://img.shields.io/github/license/" + username + "/" + project_name + ")](https://github.com/" + username + "/" + project_name + "/blob/main/LICENSE)")
            md.append("[![Issues](https://img.shields.io/github/issues/" + username + "/" + project_name + ")](https://github.com/" + username + "/" + project_name + "/issues)")
            md.append("[![Pull Requests](https://img.shields.io/github/issues-pr/" + username + "/" + project_name + ")](https://github.com/" + username + "/" + project_name + "/pulls)")
        
        # Table of contents
        md.append("\n## Table of Contents")
        md.append("\n- [About](#about)")
        md.append("- [Features](#features)")
        md.append("- [Screenshots](#screenshots)")
        md.append("- [Installation](#installation)")
        md.append("- [Usage](#usage)")
        md.append("- [Project Structure](#project-structure)")
        md.append("- [Configuration](#configuration)")
        md.append("- [Technologies](#technologies)")
        md.append("- [License](#license)")
        md.append("- [Contact](#contact)")
        
        # About section
        md.append("\n## About")
        concisedesc = self.data.get("concisedesc", "").strip()
        if concisedesc:
            md.append(f"\n**{concisedesc}**")
        
        overview = self.data.get("overview", "").strip()
        if overview:
            md.append(f"\n{overview}")
        
        # Demo
        demo_gif = self.data.get("DemoGif", "").strip()
        if demo_gif:
            md.append(f"\n### Demo")
            md.append(f"\n![Demo]({demo_gif})")
        
        # Features
        features = self.data.get("features", [])
        md.append("\n## Features")
        if features:
            for feature in features:
                md.append(f"\n### {feature}")
                md.append("\nDetailed description of this feature would go here.")
                
        # Screenshots
        screenshot1 = self.data.get("screenshot1", "").strip()
        screenshot2 = self.data.get("screenshot2", "").strip()
        
        if screenshot1 or screenshot2:
            md.append("\n## Screenshots")
            
            if screenshot1:
                md.append(f"\n### Screenshot 1")
                md.append(f"\n![Screenshot 1]({screenshot1})")
                md.append("\nDescription of what the screenshot shows.")
            
            if screenshot2:
                md.append(f"\n### Screenshot 2")
                md.append(f"\n![Screenshot 2]({screenshot2})")
                md.append("\nDescription of what the screenshot shows.")
        
        # Installation
        md.append("\n## Installation")
        
        md.append("\n### Prerequisites")
        prerequisites = self.data.get("Prerequisites", [])
        if prerequisites:
            for prerequisite in prerequisites:
                md.append(f"- {prerequisite}")
        else:
            md.append("- List prerequisite 1")
            md.append("- List prerequisite 2")
        
        md.append("\n### Step-by-step installation")
        md.append("\n```bash")
        if project_name:
            md.append(f"# Clone the repository")
            md.append(f"git clone https://github.com/{username}/{project_name}.git")
            md.append(f"")
            md.append(f"# Navigate to the project directory")
            md.append(f"cd {project_name}")
        else:
            md.append("# Clone the repository")
            md.append("git clone https://github.com/username/project.git")
            md.append("")
            md.append("# Navigate to the project directory")
            md.append("cd project")
        
        md.append("")
        md.append("# Install dependencies")
        md.append("npm install")
        md.append("# or")
        md.append("yarn install")
        md.append("```")
        
        # Usage
        md.append("\n## Usage")
        usage_code = self.data.get("usage_code", "").strip()
        if usage_code:
            md.append("\n```")
            md.append(usage_code)
            md.append("```")
        
        # Project structure
        file_structure = self.data.get("file_structure", "").strip()
        md.append("\n## Project Structure")
        if file_structure:
            md.append("\n```")
            md.append(file_structure)
            md.append("```")
        else:
            md.append("\nThe project structure would be described here.")
        
        # Configuration
        md.append("\n## Configuration")
        
        # Environment Variables
        env_vars = self.data.get("envvars", [])
        md.append("\n### Environment Variables")
        if env_vars:
            md.append("\n| Variable | Description | Default | Required |")
            md.append("|----------|-------------|---------|----------|")
            for envvar in env_vars:
                md.append(f"| `{envvar['name']}` | {envvar['desc']} | `{envvar['value']}` | Yes/No |")
        else:
            md.append("\nList of environment variables would go here.")
        
        # Technologies
        tech = self.data.get("tech", [])
        md.append("\n## Technologies")
        if tech:
            for technology in tech:
                md.append(f"\n- **{technology}**: Description of how {technology} is used in the project.")
        
        # License
        license_type = self.data.get("license", "MIT").strip()
        md.append(f"\n## License")
        md.append(f"\nThis project is licensed under the {license_type} License - see the [LICENSE](LICENSE) file for details.")
        
        # Contact
        contact = self.data.get("contact", "").strip()
        md.append("\n## Contact")
        if contact:
            md.append(f"\n{contact}")
        else:
            md.append("\nProvide your contact information here.")
        
        # Footer
        md.append("\n---\n")
        md.append("Made with ❤️ by [MdCreator](https://github.com/kushal1o1/MDFileCreator)")
        
        return "\n".join(md)
    
    def _generate_corporate_template(self):
        """Generate markdown with a corporate template"""
        md = []
        
        # Header
        project_name = self.data.get("project_name", "").strip() or "Project Title"
        md.append(f"# {project_name}")
        md.append("\n---")
        
        # Executive Summary
        concisedesc = self.data.get("concisedesc", "").strip()
        if concisedesc:
            md.append(f"\n## Executive Summary")
            md.append(f"\n{concisedesc}")
        
        # Overview
        overview = self.data.get("overview", "").strip()
        if overview:
            md.append(f"\n## Business Overview")
            md.append(f"\n{overview}")
        
        # Value Proposition / Features
        features = self.data.get("features", [])
        md.append("\n## Product Capabilities")
        if features:
            for i, feature in enumerate(features, 1):
                md.append(f"\n### {i}. {feature}")
        
        # Screenshots
        screenshot1 = self.data.get("screenshot1", "").strip()
        screenshot2 = self.data.get("screenshot2", "").strip()
        
        if screenshot1 or screenshot2:
            md.append("\n## Product Screenshots")
            
            if screenshot1:
                md.append(f"\n![{project_name} Interface]({screenshot1})")
            
            if screenshot2:
                md.append(f"\n![{project_name} Dashboard]({screenshot2})")
        
        # Technical Implementation
        md.append("\n## Technical Implementation")
        
        tech = self.data.get("tech", [])
        if tech:
            md.append("\n### Technologies Utilized")
            md.append("\n| Technology | Purpose |")
            md.append("|------------|---------|")
            for technology in tech:
                md.append(f"| {technology} | Primary functionality for {technology} |")
        
        # Project Structure
        file_structure = self.data.get("file_structure", "").strip()
        if file_structure:
            md.append("\n### Solution Architecture")
            md.append("\n```")
            md.append(file_structure)
            md.append("```")
        
        # Implementation
        md.append("\n## Implementation Guide")
        
        # Installation
        md.append("\n### Deployment Procedure")
        md.append("\n```bash")
        username = self.data.get("username", "").strip() or "organization"
        if project_name:
            md.append(f"git clone https://github.com/{username}/{project_name}.git")
            md.append(f"cd {project_name}")
        else:
            md.append("git clone https://github.com/organization/project.git")
            md.append("cd project")
        md.append("# Installation steps")
        md.append("```")
        
        # Usage
        md.append("\n### Operation Instructions")
        usage_code = self.data.get("usage_code", "").strip()
        if usage_code:
            md.append("\n```")
            md.append(usage_code)
            md.append("```")
        
        # Configuration
        env_vars = self.data.get("envvars", [])
        if env_vars:
            md.append("\n### Configuration Parameters")
            md.append("\n| Parameter | Description | Default Value |")
            md.append("|-----------|-------------|---------------|")
            for envvar in env_vars:
                md.append(f"| {envvar['name']} | {envvar['desc']} | {envvar['value']} |")
        
        # License
        license_type = self.data.get("license", "Commercial").strip()
        md.append(f"\n## Licensing Information")
        md.append(f"\nThis software is provided under {license_type} license agreement.")
        
        # Contact
        contact = self.data.get("contact", "").strip()
        md.append("\n## Support Contact")
        if contact:
            md.append(f"\n{contact}")
        else:
            md.append("\nFor technical support, please contact our support team.")
        
        # Footer
        md.append("\n---")
        md.append("\n*This document is confidential and proprietary.*")
        md.append("\nGenerated with [MdCreator](https://github.com/kushal1o1/MDFileCreator)")
        
        return "\n".join(md) 