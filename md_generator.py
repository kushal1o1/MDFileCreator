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
            "screenshot1": "",
            "screenshot2": "",
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
        """Generate markdown from data exactly matching the user's format"""
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
        md.append(f"  Made with ❤️ by <a href=\"https://github.com/{username}\">{username}</a>")
        md.append("</p>")
        
        return "\n".join(md) 