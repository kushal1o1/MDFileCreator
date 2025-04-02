import json

def get_input(prompt, default=None):
    value = input(f"{prompt} ({'Press enter to skip' if default else 'Required'}): ")
    return value if value else default

def get_list_input(prompt):
    items = []
    print(f"Enter {prompt} (Type 'done' when finished):")
    while True:
        item = input("- ")
        if item.lower() == 'done':
            break
        items.append(item)
    return items

def generate_readme(details):
    readme_content = f"""# {details['project_name']}

<p align=\"center\">
  <img src=\"{details['logo']}\" alt=\"Project Logo\" width=\"200\" height=\"200\">
</p>

<p align=\"center\">
  <a href=\"https://github.com/{details['username']}/{details['project_name']}/stargazers\"><img src=\"https://img.shields.io/github/stars/{details['username']}/{details['project_name']}\" alt=\"Stars Badge\"/></a>
  <a href=\"https://github.com/{details['username']}/{details['project_name']}/network/members\"><img src=\"https://img.shields.io/github/forks/{details['username']}/{details['project_name']}\" alt=\"Forks Badge\"/></a>
  <a href=\"https://github.com/{details['username']}/{details['project_name']}/pulls\"><img src=\"https://img.shields.io/github/issues-pr/{details['username']}/{details['project_name']}\" alt=\"Pull Requests Badge\"/></a>
  <a href=\"https://github.com/{details['username']}/{details['project_name']}/issues\"><img src=\"https://img.shields.io/github/issues/{details['username']}/{details['project_name']}\" alt=\"Issues Badge\"/></a>
  <a href=\"https://github.com/{details['username']}/{details['project_name']}/graphs/contributors\"><img alt=\"GitHub contributors\" src=\"https://img.shields.io/github/contributors/{details['username']}/{details['project_name']}?color=2b9348\"></a>
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
  <img src=\"{details['DemoGif']}\" alt="Demo" width="600">
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
    for Prerequisite in details['Prerequisites']:
        readme_content += f"- **{Prerequisite}**\n"
    
    readme_content += f"""

## Usage

```javascript
doSomething();
```
## Configuration

### Configuration File

Create a `config.json` file in the root directory with the following structure:

```json
nth
```

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
        readme_content += f"<img src=\"https://img.shields.io/badge/{tech}-%23007ACC.svg?style=for-the-badge&logo={tech}&logoColor=white\"  alt=\"{tech}\">\n"
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

def get_list_input_for_env(prompt):
    print(prompt)
    env_vars = []
    
    while True:
        line = input().strip()
        if not line:  # Stop if empty line
            break
        parts = line.split(" ", 2)  # Split into three parts: name, desc, value
        if len(parts) < 3:
            print("Invalid format. Provide: NAME DESCRIPTION VALUE")
            continue
        
        name, desc, value = parts
        env_vars.append({"name": name, "desc": desc.strip('"'), "value": value})

    return env_vars
# Collect project details
details = {
    "project_name": get_input("Enter project name"),
    "username": get_input("Enter GitHub username"),
    "logo": get_input("Enter logo URL", "path/to/logo.png"),
    "concisedesc": get_input("Enter concise 1 liner  project description"),
    "overview": get_input("Enter project overview"),
    "features": get_list_input("features"),
    "DemoGif": get_input("Enter Demo Gif URL", "path/to/demo.gif"),
    "screenshot1": get_input("Enter screenshot 1 URL", "path/to/screenshot1.png"),
    "screenshot2": get_input("Enter screenshot 2 URL", "path/to/screenshot2.png"),
    "Prerequisites": get_list_input("Prerequisites"),
    "envvars" : get_list_input_for_env("Enter environment variables (name desc value), one per line. Press Enter on empty line to finish:"),
    "tech": get_list_input("Enter technologies used, one per line. Press Enter on empty line to finish:"),
    
    "license": get_input("Enter license type", "MIT"),
    "contact": get_input("Enter contact details", "your_email@example.com"),
}

# Generate README content
readme_content = generate_readme(details)

# Save to README.md
with open("README.md", "w", encoding="utf-8") as file:
    file.write(readme_content)

print("README.md file generated successfully!")
