"""
██████╗ ███████╗ █████╗ ██╗   ██╗████████╗██╗███████╗██╗   ██╗██╗         ██████╗ ███████╗███╗   ██╗
██╔══██╗██╔════╝██╔══██╗██║   ██║╚══██╔══╝██║██╔════╝██║   ██║██║        ██╔════╝ ██╔════╝████╗  ██║
██████╔╝█████╗  ███████║██║   ██║   ██║   ██║█████╗  ██║   ██║██║        ██║  ███╗█████╗  ██╔██╗ ██║
██╔══██╗██╔══╝  ██╔══██║██║   ██║   ██║   ██║██╔══╝  ██║   ██║██║        ██║   ██║██╔══╝  ██║╚██╗██║
██████╔╝███████╗██║  ██║╚██████╔╝   ██║   ██║██║     ╚██████╔╝███████╗   ╚██████╔╝███████╗██║ ╚████║
╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝╚═╝      ╚═════╝ ╚══════╝    ╚═════╝ ╚══════╝╚═╝  ╚═══╝

🎨 BEAUTIFUL AI README Generator - Creates STUNNING Animated READMEs  
✨ With Center Alignment, Cool Animations & Professional Design
🚀 Powered by Groq AI + Enhanced GitHub Data Collection
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, Any, List, Optional

try:
    from groq import Groq
    from dotenv import load_dotenv
    load_dotenv()
    GROQ_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Missing package: {e}")
    GROQ_AVAILABLE = False

class AIGenerator:
    """🎨 Beautiful AI README Generator with Stunning Animations"""
    
    def __init__(self):
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        self.groq_client = None
        self.debug_log = []
        
        if not GROQ_AVAILABLE:
            self.log("⚠️  Warning: Groq package not available")
            return
            
        if not self.groq_api_key:
            self.log("⚠️  Warning: No GROQ_API_KEY found in .env file")
            return
            
        try:
            self.groq_client = Groq(api_key=self.groq_api_key)
            self.log("🎨 Beautiful AI README Generator initialized!")
            self.log("✨ Ready to create STUNNING animated READMEs!")
        except Exception as e:
            self.log(f"❌ Error initializing Groq client: {e}")
            self.groq_client = None
    
    def log(self, message: str, data: Any = None):
        """📝 Beautiful logging with emojis"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        if data:
            log_entry += f" | Data: {str(data)[:100]}..."
        self.debug_log.append(log_entry)
        print(log_entry)

    def generate_professional_readme(self, github_url: str = None, data_file: str = None) -> str:
        """🚀 Generate STUNNING professional README with animations"""
        start_time = time.time()
        self.log("🎯 === STARTING BEAUTIFUL README GENERATION ===")
        
        try:
            github_data = {}
            
            if data_file and os.path.exists(data_file):
                self.log(f"📂 Loading data from file: {data_file}")
                with open(data_file, 'r', encoding='utf-8') as f:
                    github_data = json.load(f)
                self.log(f"📊 Loaded data for: {github_data.get('owner', 'Unknown')}/{github_data.get('repo', 'Unknown')}")
            else:
                self.log("❌ ERROR: No valid data file provided")
                return self._fallback_readme(github_url or "Unknown")
            
            # Generate README with AI
            self.log("🎨 Generating STUNNING README with AI...")
            readme_content = self._generate_with_ai(github_data)
            
            if not readme_content:
                self.log("❌ ERROR: AI generation failed, using fallback")
                return self._fallback_readme(github_url or github_data.get('url', 'Unknown'))
            
            total_time = time.time() - start_time
            self.log(f"✅ === BEAUTIFUL README GENERATION COMPLETE in {total_time:.2f}s ===")
            
            return readme_content
            
        except Exception as e:
            self.log(f"💥 FATAL ERROR: {e}")
            return self._fallback_readme(github_url or "Unknown")

    def _generate_with_ai(self, github_data: Dict) -> Optional[str]:
        """🤖 Generate README using AI with STUNNING design"""
        if not self.groq_client:
            self.log("❌ No Groq client available, using fallback")
            return None
            
        try:
            prompt = self._build_stunning_prompt(github_data)
            self.log(f"📤 Sending BEAUTIFUL prompt to AI ({len(prompt)} characters)")
            
            ai_start = time.time()
            
            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": """You are THE WORLD'S BEST README designer and technical writer! 🌟

You specialize in creating ABSOLUTELY STUNNING, BREATHTAKING README.md files that:
• Use cutting-edge GitHub markdown features and animations
• Have perfect center alignment and premium visual hierarchy  
• Include 3D effects, gradient text, and animated elements
• Are 100% accurate based on real repository data
• Follow modern design trends with glassmorphism effects
• Include interactive elements and hover animations
• Use advanced badge combinations and custom SVGs
• Have flawless typography and spacing
• Create "WOW factor" that makes developers stop scrolling

Your READMEs are so beautiful they get featured on GitHub trending and receive thousands of stars! 
You NEVER use placeholder content - everything is based on REAL DATA provided.
You create works of art that are both functional and absolutely gorgeous! ✨🚀"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.3-70b-versatile",
                max_tokens=4500,
                temperature=0.8,
                top_p=0.9
            )
            
            ai_duration = time.time() - ai_start
            content = chat_completion.choices[0].message.content
            
            self.log(f"🎉 AI generated STUNNING README: {len(content)} characters in {ai_duration:.2f}s")
            return content
                
        except Exception as e:
            self.log(f"❌ ERROR in AI generation: {e}")
            return None

    def _build_stunning_prompt(self, github_data: Dict) -> str:
        """🎨 Build STUNNING prompt for beautiful animated README"""
        basic_info = github_data.get('basic_info', {})
        contents = github_data.get('contents', {})
        languages = github_data.get('languages', {})
        commits = github_data.get('recent_commits', [])
        contributors = github_data.get('contributors', [])
        releases = github_data.get('releases', [])
        existing_readme = github_data.get('existing_readme', {})
        package_files = github_data.get('package_files', {})
        
        # Enhanced file analysis
        files_list = []
        dirs_list = []
        
        if isinstance(contents.get('files'), list):
            files_list = [f.get('name', '') for f in contents['files'] if isinstance(f, dict)]
        
        if isinstance(contents.get('directories'), list):
            dirs_list = contents['directories']
        
        # Detailed language analysis
        lang_breakdown = ""
        primary_lang = languages.get('primary_language', 'Unknown')
        if isinstance(languages.get('languages'), dict):
            for lang, data in languages['languages'].items():
                if isinstance(data, dict):
                    percentage = data.get('percentage', 0)
                    lang_breakdown += f"  • {lang}: {percentage:.1f}%\n"

        # Enhanced commit analysis
        commits_info = "No recent development activity"
        if commits and isinstance(commits, list) and len(commits) > 0:
            latest_commit = commits[0]
            if isinstance(latest_commit, dict):
                commits_info = f"Latest: '{latest_commit.get('message', '')}' by {latest_commit.get('author', '')} ({latest_commit.get('date', '')})"
                commits_info += f"\n  • Total analyzed commits: {len(commits)}"
        
        # Enhanced contributor analysis
        contributors_info = []
        if isinstance(contributors, list):
            for c in contributors[:5]:  # Top 5 contributors
                if isinstance(c, dict):
                    login = c.get('login', '')
                    contributions = c.get('contributions', 0)
                    contributors_info.append(f"{login} ({contributions} contributions)")
        
        # Advanced technology detection
        tech_stack = self._detect_advanced_tech_stack(files_list, package_files)
        project_type = self._determine_project_type(files_list, primary_lang, tech_stack)
        
        # Enhanced repository metrics
        repo_stats = {
            'stars': basic_info.get('stars', 0),
            'forks': basic_info.get('forks', 0),
            'watchers': basic_info.get('watchers', 0),
            'issues': basic_info.get('open_issues', 0),
            'size_kb': basic_info.get('size', 0),
            'files_count': contents.get('total_files', 0),
            'contributors_count': len(contributors) if isinstance(contributors, list) else 0,
            'releases_count': len(releases) if isinstance(releases, list) else 0
        }
        
        # Build comprehensive project analysis
        project_analysis = self._analyze_project_structure(files_list, dirs_list, tech_stack)
        
        prompt = f"""# 🎯 ULTIMATE MISSION:  BREATHTAKING README.md

You have been provided with COMPREHENSIVE, REAL DATA about this GitHub repository. Your mission is to create the most STUNNING, ACCURATE, and PROFESSIONAL README.md with beautiful animations!

## 📊 REPOSITORY INTELLIGENCE REPORT

### 🏷️ Basic Information
- **Repository**: `{github_data.get('owner', 'Unknown')}/{github_data.get('repo', 'Unknown')}`
- **Full Name**: {basic_info.get('full_name', 'Not specified')}
- **Description**: {basic_info.get('description', 'No description available')}
- **Homepage**: {basic_info.get('homepage', 'None specified')}
- **License**: {basic_info.get('license', 'License not specified')}
- **Created**: {basic_info.get('created_at', 'Unknown')}
- **Last Updated**: {basic_info.get('updated_at', 'Unknown')}
- **Topics**: {', '.join(basic_info.get('topics', [])) if isinstance(basic_info.get('topics'), list) else 'No topics specified'}

### 📈 Repository Metrics (USE THESE EXACT NUMBERS!)
- **⭐ Stars**: {repo_stats['stars']:,}
- **🍴 Forks**: {repo_stats['forks']:,}
- **👁️ Watchers**: {repo_stats['watchers']:,}
- **🐛 Open Issues**: {repo_stats['issues']:,}
- **📦 Repository Size**: {repo_stats['size_kb']:,} KB
- **📁 Total Files**: {repo_stats['files_count']:,}
- **👥 Contributors**: {repo_stats['contributors_count']:,}
- **🏷️ Releases**: {repo_stats['releases_count']:,}

### 💻 Technology Intelligence
- **Project Type**: {project_type}
- **Primary Language**: {primary_lang}
- **Language Distribution**:
{lang_breakdown if lang_breakdown else '  • No language data available'}

- **Technology Stack Detected**: {', '.join(tech_stack) if tech_stack else 'Basic project structure'}

### 📁 Project Structure Analysis
{project_analysis}

### 🔄 Development Activity
- **Recent Development**: {commits_info}
- **Key Contributors**: {', '.join(contributors_info) if contributors_info else 'No contributor data available'}
- **Has Releases**: {'✅ Yes' if repo_stats['releases_count'] > 0 else '❌ No releases yet'}

### 📦 Dependencies & Configuration
{self._format_dependencies(package_files)}



Follow such structure OR You can design in you own way OK and make it GORGEOUS with animations:

### 🌟 HEADER SECTION:
```markdown
# [Project Name]

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=35&pause=1000&color=FF6B6B&center=true&vCenter=true&width=800&lines=[Project+Name];✨+[Compelling+Description]+✨;🚀+Built+with+[Primary+Tech]+🚀" alt="Typing Animation" />
</p>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=180&section=header&text=[Project%20Name]&fontSize=42&fontColor=fff&animation=twinkling&fontAlignY=32" width="100%"/>
</p>

<p align="center">
  <a href="https://github.com/{github_data.get('owner', 'owner')}/{github_data.get('repo', 'repo')}/stargazers">
    <img src="https://img.shields.io/github/stars/{github_data.get('owner', 'owner')}/{github_data.get('repo', 'repo')}?style=for-the-badge&logo=github&color=yellow" alt="Stars"/>
  </a>
  <a href="https://github.com/{github_data.get('owner', 'owner')}/{github_data.get('repo', 'repo')}/network/members">
    <img src="https://img.shields.io/github/forks/{github_data.get('owner', 'owner')}/{github_data.get('repo', 'repo')}?style=for-the-badge&logo=github&color=blue" alt="Forks"/>
  </a>
  <a href="https://github.com/{github_data.get('owner', 'owner')}/{github_data.get('repo', 'repo')}/issues">
    <img src="https://img.shields.io/github/issues/{github_data.get('owner', 'owner')}/{github_data.get('repo', 'repo')}?style=for-the-badge&logo=github&color=red" alt="Issues"/>
  </a>
  <a href="https://github.com/{github_data.get('owner', 'owner')}/{github_data.get('repo', 'repo')}/pulls">
    <img src="https://img.shields.io/github/issues-pr/{github_data.get('owner', 'owner')}/{github_data.get('repo', 'repo')}?style=for-the-badge&logo=github&color=orange" alt="Pull Requests"/>
  </a>
  <a href="https://github.com/{github_data.get('owner', 'owner')}/{github_data.get('repo', 'repo')}/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/{github_data.get('owner', 'owner')}/{github_data.get('repo', 'repo')}?style=for-the-badge&logo=github&color=green" alt="Contributors"/>
  </a>
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="700">
</p>

<p align="center">
  <b>✨ [Write compelling description based on actual project data] ✨</b>
</p>

<p align="center">
  <a href="#overview">🌟 Overview</a> •
  <a href="#features">✨ Features</a> •
  <a href="#demo">🎥 Demo</a> •
  <a href="#installation">🚀 Installation</a> •
  <a href="#usage">💻 Usage</a> •
  <a href="#tech-stack">🛠️ Tech Stack</a> •
  <a href="#structure">📁 Structure</a> •
  <a href="#contributing">🤝 Contributing</a> •
  <a href="#license">📄 License</a> •
  <a href="#contact">📞 Contact</a>
</p>

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">
```

### 🎯 REQUIRED SECTIONS IN THIS ORDER:

## **1. Overview Section**
```markdown
## 🌟 Overview



[Write compelling overview based on actual project analysis]

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="100%">
</p>
```

## **2. Features Section**
```markdown
## ✨ Features



- 🚀 **[Feature based on detected tech]**
- ⚡ **[Feature based on detected files]**
- 🎨 **[Feature based on project type]**
- 📱 **[Feature based on detected frameworks]**
- 🔧 **[Feature based on configuration files]**
- 🛡️ **[Feature based on detected security/auth]**

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png" width="100%">
</p>
```

## **3. Demo/Screenshots Section**
```markdown
## 🎥 Demo

<div align="center">
 
  ### 🖼️ Screenshots
  [Only include if images detected in repository]
</div>

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/fire.png" width="100%">
</p>
```

## **4. Installation Section**
```markdown
## 🚀 Installation


### 📋 Prerequisites
[List actual prerequisites based on detected tech stack]

### ⚡ Quick Setup
```bash
# Clone the repository
git clone https://github.com/{github_data.get('owner', 'owner')}/{github_data.get('repo', 'repo')}.git

# Navigate to project directory
cd {github_data.get('repo', 'project')}

[Add actual installation commands based on detected package files]
```

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/grass.png" width="100%">
</p>
```

## **5. Usage Section**
```markdown
## 💻 Usage



[Provide actual usage examples based on detected main files and tech stack]

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png" width="100%">
</p>
```

## **6. Tech Stack Section**
```markdown
## 🛠️ Technologies Used

<div align="center">
 
  
  <p>
    [Create skillicons.dev badges for ONLY detected technologies]
  </p>
</div>

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/vintage.png" width="100%">
</p>
```

## **7. Directory Structure**
```markdown
## 📁 Project Structure

```bash
THe directory must be same ok as provided
.
├── app.py
├── requirements.txt
├── README.md
└── utils.py
```

[Create beautiful tree structure using actual detected files and directories]


```

## **8. Contributing Section**
```markdown
## 🤝 Contributing



Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png" width="100%">
</p>
```

## **9. Footer Section**
```markdown
## 📄 License

This project is licensed under the [Actual License] License.

## 📞 Contact

[Author Name] - [@username](https://twitter.com/username) - email@example.com

---

<div align="center">
  <img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">
  
  **Made with ❤️ by [MDCreator](https://github.com/kushal1o1/MDFileCreator)**
  
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=120&section=footer&animation=twinkling" width="100%"/>
</div>
```

## 🚨 CRITICAL REQUIREMENTS:

1. **🎨 VISUAL EXCELLENCE**: Use animated GIFs, colorful dividers, perfect center alignment
2. **🎯 100% ACCURACY**: Use ONLY detected technologies, files, and real repository data
3. **🌈 COLORFUL DESIGN**: Include rainbow dividers, gradient headers, animated elements
4. **📱 RESPONSIVE**: Beautiful on all screen sizes with proper markdown
5. **✨ ANIMATED TYPING**: Use readme-typing-svg with project-specific content
6. **🏆 PROFESSIONAL**: Clean, modern, impressive design that gets stars
7. **🔗 WORKING LINKS**: All badges and links must work with actual repository data
8. **📦 COMPREHENSIVE CONTENT**: Include all relevant sections and information You can add Anyother content if you found this must be here or you can remove any sections If you think it shouldnot be here 

**TARGET REPOSITORY**: {github_data.get('owner', 'Unknown')}/{github_data.get('repo', 'Unknown')}

Create a README so BEAUTIFUL and ANIMATED that it becomes the new standard! 🎨✨🚀
"""

        return prompt
    
    def _detect_advanced_tech_stack(self, files_list: List[str], package_files: Dict) -> List[str]:
        """🔍 Advanced technology stack detection"""
        tech_stack = []
        
        # Web frameworks
        if any('app.py' in f or 'main.py' in f for f in files_list):
            if 'requirements.txt' in files_list or any('flask' in str(package_files).lower() for _ in [1]):
                tech_stack.append('Flask')
            elif any('django' in str(package_files).lower() for _ in [1]):
                tech_stack.append('Django')
            elif any('fastapi' in str(package_files).lower() for _ in [1]):
                tech_stack.append('FastAPI')
        
        # Frontend frameworks
        if 'package.json' in files_list:
            tech_stack.append('Node.js')
            if any('react' in str(package_files).lower() for _ in [1]):
                tech_stack.append('React')
            elif any('vue' in str(package_files).lower() for _ in [1]):
                tech_stack.append('Vue.js')
            elif any('angular' in str(package_files).lower() for _ in [1]):
                tech_stack.append('Angular')
            elif any('next' in str(package_files).lower() for _ in [1]):
                tech_stack.append('Next.js')
        
        # Database and storage
        if any('database' in f.lower() or 'db' in f.lower() for f in files_list):
            tech_stack.append('Database')
        
        # DevOps and deployment
        if any('dockerfile' in f.lower() for f in files_list):
            tech_stack.append('Docker')
        if any('docker-compose' in f.lower() for f in files_list):
            tech_stack.append('Docker Compose')
        if any('.github' in f for f in files_list):
            tech_stack.append('GitHub Actions')
        
        # Development tools
        if 'requirements.txt' in files_list or 'setup.py' in files_list:
            tech_stack.append('Python')
        if 'Cargo.toml' in files_list:
            tech_stack.append('Rust')
        if 'go.mod' in files_list:
            tech_stack.append('Go')
        if 'pom.xml' in files_list or 'build.gradle' in files_list:
            tech_stack.append('Java')
        
        return tech_stack
    
    def _determine_project_type(self, files_list: List[str], primary_lang: str, tech_stack: List[str]) -> str:
        """🎯 Determine project type from analysis"""
        if 'React' in tech_stack or 'Vue.js' in tech_stack or 'Angular' in tech_stack:
            return 'Frontend Web Application'
        elif 'Flask' in tech_stack or 'Django' in tech_stack or 'FastAPI' in tech_stack:
            return 'Backend Web API'
        elif 'Next.js' in tech_stack:
            return 'Full-Stack Web Application'
        elif primary_lang == 'Python' and any('jupyter' in f.lower() or '.ipynb' in f for f in files_list):
            return 'Data Science/Machine Learning Project'
        elif primary_lang == 'JavaScript' and 'Node.js' in tech_stack:
            return 'Node.js Application'
        elif 'Docker' in tech_stack:
            return 'Containerized Application'
        elif primary_lang in ['Python', 'JavaScript', 'Java', 'Go', 'Rust']:
            return f'{primary_lang} Application'
        else:
            return 'Software Project'
    
    def _analyze_project_structure(self, files_list: List[str], dirs_list: List[str], tech_stack: List[str]) -> str:
        """📁 Analyze and format project structure"""
        structure_analysis = ""
        
        # Key directories
        important_dirs = [d for d in dirs_list if d.lower() in ['src', 'app', 'components', 'pages', 'api', 'models', 'views', 'static', 'assets', 'docs', 'tests', 'config']]
        if important_dirs:
            structure_analysis += f"**📂 Key Directories**: {', '.join(important_dirs[:8])}\n"
        
        # Key files
        important_files = [f for f in files_list if any(ext in f.lower() for ext in ['.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.md', '.json', '.yml', '.yaml'])][:15]
        if important_files:
            structure_analysis += f"**📄 Key Files**: {', '.join(important_files)}\n"
        
        # Configuration files
        config_files = [f for f in files_list if any(config in f.lower() for config in ['config', '.env', 'settings', 'package.json', 'requirements.txt', 'dockerfile'])]
        if config_files:
            structure_analysis += f"**⚙️ Configuration**: {', '.join(config_files)}\n"
        
        return structure_analysis if structure_analysis else "**📁 Structure**: Standard project layout detected"
    
    def _format_dependencies(self, package_files: Dict) -> str:
        """📦 Enhanced dependency formatting"""
        if not isinstance(package_files, dict) or not package_files:
            return "**📦 Dependencies**: No package files detected"
        
        formatted = "**📦 Dependency Files Detected**:\n"
        for filename, data in package_files.items():
            if isinstance(data, dict):
                if 'content' in data and data['content']:
                    formatted += f"  ✅ **{filename}**: Ready for installation\n"
                else:
                    formatted += f"  📄 **{filename}**: Detected\n"
            else:
                formatted += f"  📄 **{filename}**: Found\n"
        
        return formatted
    
    def _fallback_readme(self, github_url: str) -> str:
        """🚨 Generate PREMIUM fallback README with stunning design"""
        self.log("🚨 Using PREMIUM fallback README generation")
        
        # Extract repo info
        repo_name = "Awesome Project"
        owner_repo = ""
        
        if github_url and isinstance(github_url, str):
            if "github.com" in github_url:
                parts = github_url.replace('https://github.com/', '').replace('.git', '').split('/')
                if len(parts) >= 2:
                    owner_repo = f"{parts[0]}/{parts[1]}"
                    repo_name = parts[1].replace('-', ' ').replace('_', ' ').title()
            else:
                repo_name = github_url.split('/')[-1].replace('.git', '').replace('-', ' ').replace('_', ' ').title()
        
        return f"""<div align="center">

# 🚀 {repo_name}

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=28&pause=1000&color=2E9EF7&center=true&vCenter=true&width=600&lines=Welcome+to+{repo_name.replace(' ', '+')}!;Building+Something+Amazing!;Open+Source+❤️" alt="Typing SVG" />

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="100%" />

{f'''[![⭐ Stars](https://img.shields.io/github/stars/{owner_repo}?style=for-the-badge&logo=github&logoColor=white&color=yellow)](https://github.com/{owner_repo}/stargazers)
[![🍴 Forks](https://img.shields.io/github/forks/{owner_repo}?style=for-the-badge&logo=github&logoColor=white&color=blue)](https://github.com/{owner_repo}/network)
[![🐛 Issues](https://img.shields.io/github/issues/{owner_repo}?style=for-the-badge&logo=github&logoColor=white&color=red)](https://github.com/{owner_repo}/issues)
[![📝 License](https://img.shields.io/github/license/{owner_repo}?style=for-the-badge&color=green)](https://github.com/{owner_repo}/blob/main/LICENSE)''' if owner_repo else ''}

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png" width="100%" />

</div>

## 📖 About This Project

Welcome to **{repo_name}**! This repository contains an amazing project that's ready to be explored.

<div align="center">

### 🌟 Key Features

</div>

- 🚀 **Modern Technology Stack**
- ⚡ **High Performance**
- 🎨 **Beautiful Design**
- 📱 **Responsive Layout**
- 🔧 **Easy Configuration**
- 🛡️ **Secure & Reliable**

<div align="center">

## ⚡ Quick Start

</div>

### 📥 Installation

```bash
# Clone the repository
git clone {github_url}

# Navigate to project directory
cd {repo_name.lower().replace(' ', '-')}

# Install dependencies (adjust based on your project type)
npm install  # For Node.js projects
# or
pip install -r requirements.txt  # For Python projects
```

### 🚀 Usage

```bash
# Start the application
npm start  # For Node.js
# or  
python main.py  # For Python
```

<div align="center">

## 🛠️ Tech Stack

</div>

<div align="center">

![Tech Stack](https://skillicons.dev/icons?i=html,css,js,python,nodejs,react,git,github)

</div>

<div align="center">

## 📊 GitHub Stats

</div>

<div align="center">

{f'''![GitHub Stats](https://github-readme-stats.vercel.app/api?username={owner_repo.split('/')[0] if owner_repo else 'user'}&show_icons=true&theme=radical)''' if owner_repo else ''}

</div>

<div align="center">

## 🤝 Contributing

</div>

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<div align="center">

## ⚖️ License

</div>

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<div align="center">

## 💝 Support

</div>

Give a ⭐️ if this project helped you!

<div align="center">

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="100%" />

**Made with ❤️ by [MDCreator](https://github.com/kushal1o1/MDFileCreator)**

<img src="https://forthebadge.com/images/badges/built-with-love.svg" />
<img src="https://forthebadge.com/images/badges/powered-by-coffee.svg" />

</div>
"""
    
    def get_debug_logs(self) -> List[str]:
        """📋 Get all debug logs"""
        return self.debug_log

# 🧪 Test the beautiful generator
if __name__ == "__main__":
    print("🧪 Testing Beautiful AI Generator...")
    generator = AIGenerator()
    print("🎨 Beautiful generator created successfully!")