"""
🚀 Smart AI README Generator
Supports multiple README styles and uses minimal GitHub data
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

class SmartAIGenerator:
    """🚀 Smart AI README Generator with Multiple Styles"""
    
    def __init__(self):
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        self.default_model = os.getenv('DEFAULT_MODEL', 'llama-3.3-70b-versatile')
        self.fallback_model = os.getenv('FALLBACK_MODEL', 'llama-3.1-8b-instant')
        self.groq_client = None
        self.debug_log = []
        
        # README Style Templates
        self.style_prompts = {
            "🔥 Modern & Trendy": """
Create a MODERN and TRENDY README with:
- Cool emojis and visual elements
- Animated GIFs and badges
- Center-aligned sections
- Modern badges and shields
- Trending design patterns
- Social media style headers
""",
            "📊 Professional & Corporate": """
Create a PROFESSIONAL and CORPORATE README with:
- Clean, formal language
- Business-focused sections
- Professional badges
- Corporate structure
- Executive summary style
- Clear business value proposition
""",
            "🚀 Developer Focused": """
Create a DEVELOPER-FOCUSED README with:
- Technical details and architecture
- Code examples and snippets
- API documentation style
- Technical badges and stats
- Development workflow info
- Contribution guidelines focus
""",
            "📝 Simple & Clean": """
Create a SIMPLE and CLEAN README with:
- Minimal design
- Essential information only
- Clean formatting
- No excessive decorations
- Straightforward structure
- Easy to read and scan
""",
            "🎯 Detailed & Comprehensive": """
Create a DETAILED and COMPREHENSIVE README with:
- Complete documentation
- All possible sections
- Detailed explanations
- Multiple examples
- Troubleshooting guides
- FAQ sections
""",
            "🤖 Let AI Choose Best Style": """
Analyze the project and choose the BEST README style based on:
- Project type and purpose
- Target audience
- Technology stack
- Repository structure
- Existing README (if any)
Choose the most appropriate style automatically.
"""
        }
        
        if not GROQ_AVAILABLE:
            self.log("⚠️  Warning: Groq package not available")
            return
            
        if not self.groq_api_key:
            self.log("⚠️  Warning: No GROQ_API_KEY found in .env file")
            return
            
        try:
            self.groq_client = Groq(api_key=self.groq_api_key)
            self.log(f"🚀 Smart AI Generator initialized with model: {self.default_model}")
        except Exception as e:
            self.log(f"❌ Error initializing Groq client: {e}")
            self.groq_client = None
    
    def log(self, message: str) -> None:
        """📝 Enhanced logging"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        self.debug_log.append(log_entry)
        print(log_entry)
    
    def generate_smart_readme(self, github_url: str, data_file: str, style: str = "🤖 Let AI Choose Best Style") -> str:
        """🎯 Generate README with selected style"""
        
        if not self.groq_client:
            raise Exception("Groq client not initialized")
        
        self.log(f"🎨 Generating README with style: {style}")
        
        # Load GitHub data
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                github_data = json.load(f)
        except Exception as e:
            raise Exception(f"Failed to load GitHub data: {e}")
        
        # Get style prompt
        style_instruction = self.style_prompts.get(style, self.style_prompts["🤖 Let AI Choose Best Style"])
        
        # Build comprehensive prompt
        prompt = self._build_smart_prompt(github_data, style_instruction, github_url)
        
        try:
            self.log(f"🧠 Sending request to Groq AI using model: {self.default_model}...")
            
            response = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert README generator. Create professional, engaging, and comprehensive README files based on GitHub repository data."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                model=self.default_model,
                temperature=0.7,
                max_tokens=4000
            )
            
            readme_content = response.choices[0].message.content.strip()
            self.log("✅ README generated successfully!")
            
            return readme_content
            
        except Exception as e:
            # Try fallback model if default fails
            if "decommissioned" in str(e).lower() or "model" in str(e).lower():
                self.log(f"⚠️ Default model failed, trying fallback: {self.fallback_model}")
                try:
                    response = self.groq_client.chat.completions.create(
                        messages=[
                            {
                                "role": "system",
                                "content": "You are an expert README generator. Create professional, engaging, and comprehensive README files based on GitHub repository data."
                            },
                            {
                                "role": "user", 
                                "content": prompt
                            }
                        ],
                        model=self.fallback_model,
                        temperature=0.7,
                        max_tokens=4000
                    )
                    
                    readme_content = response.choices[0].message.content.strip()
                    self.log(f"✅ README generated successfully with fallback model: {self.fallback_model}")
                    
                    return readme_content
                    
                except Exception as fallback_error:
                    self.log(f"❌ Fallback model also failed: {fallback_error}")
                    raise Exception(f"Both models failed. Default: {e}, Fallback: {fallback_error}")
            else:
                self.log(f"❌ Error generating README: {e}")
                raise Exception(f"AI generation failed: {e}")
    
    def _build_smart_prompt(self, github_data: Dict, style_instruction: str, github_url: str) -> str:
        """🔨 Build intelligent prompt with all essential data"""
        
        # Extract key information
        basic_info = github_data.get('basic_info', {})
        file_structure = github_data.get('file_structure', {})
        languages = github_data.get('languages', {})
        existing_readme = github_data.get('existing_readme', {})
        package_files = github_data.get('package_files', {})
        key_files = github_data.get('key_files', {})
        
        # Build the enhanced prompt
        prompt = f"""
🎨 CREATE AN ABSOLUTELY STUNNING & EYE-CATCHING README 🎨

{style_instruction}

🔥 VISUAL REQUIREMENTS - MAKE IT SPECTACULAR:
✨ Use rich emojis throughout for visual appeal
🎯 Create eye-catching headers with ASCII art or fancy formatting
🌈 Add colorful badges from shields.io (build status, version, license, downloads, etc.)
🚀 Include animated GIFs from giphy.com or similar for demos (use placeholder URLs)
📊 Add dynamic badges showing stats, metrics, and achievements
🎭 Use HTML for advanced formatting (center alignment, colors, sizing)
💫 Create visually striking sections with borders, dividers, and spacing
🏆 Add contributor badges, tech stack visualization, and feature highlights
🎪 Make liberal use of tables, collapsible sections, and visual hierarchy
📸 Include placeholder screenshots, diagrams, and visual elements
🌟 Add "Star History" charts, download counters, and engagement metrics

🔥 MANDATORY VISUAL ELEMENTS TO INCLUDE:
- Hero banner with project logo and title
- Multiple colorful badges (build, version, license, downloads, stars, etc.)
- Table of contents with emoji navigation
- Feature showcase with icons and descriptions
- Screenshot/demo section with placeholder images
- Technology stack with logos/icons
- Quick start guide with copy-paste commands
- Contributor avatars and stats
- Star history graph
- Footer with social links and acknowledgments

REPOSITORY DATA TO WORK WITH:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 PROJECT INFORMATION:
• Repository: {github_url}
• Name: {basic_info.get('name', 'Awesome Project')}
• Description: {basic_info.get('description', 'An amazing project that will blow your mind!')}
• Primary Language: {basic_info.get('language', 'Multiple Languages')}
• ⭐ Stars: {basic_info.get('stars', 0)}
• 🍴 Forks: {basic_info.get('forks', 0)}
• 📜 License: {basic_info.get('license', 'MIT License')}
• 🌐 Homepage: {basic_info.get('homepage', 'Not specified')}

💻 PROGRAMMING LANGUAGES & TECH STACK:
{self._format_languages(languages)}

📁 PROJECT STRUCTURE ANALYSIS:
{self._format_file_structure(file_structure)}

📋 DEPENDENCY FILES DETECTED:
{self._format_package_files(package_files)}

🔑 KEY PROJECT FILES:
{self._format_key_files(key_files)}

📖 EXISTING README ANALYSIS:
{self._format_existing_readme(existing_readme)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 GENERATION INSTRUCTIONS - MAKE IT AMAZING:

1. 🎨 VISUAL IMPACT: Create a README that makes people go "WOW!" at first glance
2. 🏗️ STRUCTURE: Use the detected technologies to create smart installation/usage guides
3. 🔄 ENHANCEMENT: If existing README exists, keep good parts but make it 10x more visual
4. 🎪 BADGES GALORE: Generate at least 8-12 relevant badges for the project
5. 📊 TECH SHOWCASE: Create a beautiful tech stack section with descriptions
6. 🚀 DEMO READY: Include demo GIFs, screenshots, and interactive elements
7. 📝 COMPLETE DOCS: All essential sections (Features, Install, Usage, API, Contributing, etc.)
8. 🌟 ENGAGEMENT: Add elements that encourage stars, forks, and contributions
9. 🎭 FORMATTING: Use HTML, emojis, tables, and advanced markdown features
10. 💎 PREMIUM FEEL: Make it look like a premium, professional project

🎪 SPECIAL REQUIREMENTS:
- Start with an impressive hero section
- Use creative ASCII art or text formatting for the title
- Include at least 3 different types of badges
- Add a "Why Choose This Project?" section
- Create a visual roadmap or timeline
- Include a "Show Your Support" section
- Add contributor recognition
- End with an impressive footer

🔥 MAKE IT SO VISUALLY STUNNING THAT DEVELOPERS WILL WANT TO STAR IT IMMEDIATELY! 🔥

Generate the complete, spectacular README.md file:
"""
        
        return prompt
    
    def _format_languages(self, languages: Dict) -> str:
        """Format languages data"""
        if not languages or 'languages' not in languages:
            return "• 🔍 Language detection in progress..."
        
        lang_data = languages['languages']
        if not lang_data:
            return "• 🌐 Multi-language project detected"
        
        formatted = []
        lang_emojis = {
            'Python': '🐍', 'JavaScript': '💛', 'TypeScript': '💙', 'Java': '☕',
            'C++': '⚡', 'C': '🔧', 'Go': '🚀', 'Rust': '⚙️', 'PHP': '🐘',
            'Ruby': '💎', 'Swift': '🦉', 'Kotlin': '🎯', 'HTML': '🌐',
            'CSS': '🎨', 'Shell': '🐚', 'Dockerfile': '🐳'
        }
        
        for lang, info in lang_data.items():
            emoji = lang_emojis.get(lang, '📝')
            if isinstance(info, dict) and 'percentage' in info:
                formatted.append(f"• {emoji} {lang}: {info['percentage']}%")
            else:
                formatted.append(f"• {emoji} {lang}")
        
        return '\n'.join(formatted[:8])  # Top 8 languages with emojis
    
    def _format_file_structure(self, file_structure: Dict) -> str:
        """Format file structure"""
        if not file_structure:
            return "• 📂 Project structure analysis pending..."
        
        files = file_structure.get('files', [])
        directories = file_structure.get('directories', [])
        
        structure_info = []
        structure_info.append(f"• 📄 Total files: {len(files)}")
        structure_info.append(f"• 📁 Total directories: {len(directories)}")
        
        # Show key directories with emojis
        dir_emojis = {
            'src': '📦', 'lib': '📚', 'app': '🏗️', 'components': '🧩',
            'pages': '📄', 'api': '🔌', 'utils': '🛠️', 'config': '⚙️',
            'docs': '📖', 'tests': '🧪', '__pycache__': '🗂️', 'node_modules': '📦'
        }
        
        key_dirs = [d for d in directories if d in dir_emojis.keys()][:6]
        if key_dirs:
            formatted_dirs = [f"{dir_emojis.get(d, '📁')}{d}" for d in key_dirs]
            structure_info.append(f"• 🗂️ Key directories: {', '.join(formatted_dirs)}")
        
        # Show file extensions with counts
        extensions = file_structure.get('file_extensions', {})
        if extensions:
            top_ext = sorted(extensions.items(), key=lambda x: x[1], reverse=True)[:4]
            ext_str = ', '.join([f"{ext} ({count})" for ext, count in top_ext])
            structure_info.append(f"• 📊 Main file types: {ext_str}")
        
        return '\n'.join(structure_info)
    
    def _format_package_files(self, package_files: Dict) -> str:
        """Format package files information"""
        if not package_files:
            return "• 📦 No package files detected - custom project structure"
        
        found_files = []
        file_emojis = {
            'package.json': '📦', 'requirements.txt': '🐍', 'Gemfile': '💎',
            'Cargo.toml': '⚙️', 'go.mod': '🚀', 'composer.json': '🐘',
            'pom.xml': '☕', 'build.gradle': '🏗️', 'Pipfile': '🐍'
        }
        
        for filename, data in package_files.items():
            emoji = file_emojis.get(filename, '📄')
            if isinstance(data, dict) and 'content' in data:
                found_files.append(f"• {emoji} {filename} detected")
                
                # Add key dependencies for popular files
                if filename == 'package.json':
                    try:
                        content = json.loads(data['content'])
                        deps = content.get('dependencies', {})
                        if deps:
                            key_deps = list(deps.keys())[:4]
                            found_files.append(f"  🔗 Key deps: {', '.join(key_deps)}")
                    except:
                        pass
                elif filename == 'requirements.txt':
                    lines = data['content'].split('\n')[:6]
                    deps = [line.strip().split('==')[0].split('>=')[0] for line in lines 
                           if line.strip() and not line.startswith('#')]
                    if deps:
                        found_files.append(f"  🔗 Python packages: {', '.join(deps[:4])}")
        
        return '\n'.join(found_files) if found_files else "• 📦 Custom dependency management detected"
    
    def _format_key_files(self, key_files: Dict) -> str:
        """Format key files information"""
        if not key_files:
            return "• 🔍 Key files analysis in progress..."
        
        found_files = []
        key_emojis = {
            'README': '📖', 'LICENSE': '📜', 'CONTRIBUTING': '🤝',
            'CHANGELOG': '📝', 'docker': '🐳', 'config': '⚙️',
            'test': '🧪', 'docs': '📚', 'scripts': '📜'
        }
        
        for filename, data in key_files.items():
            # Find appropriate emoji
            emoji = '📄'
            for key, em in key_emojis.items():
                if key.lower() in filename.lower():
                    emoji = em
                    break
            
            if isinstance(data, dict) and 'description' in data:
                found_files.append(f"• {emoji} {filename}: {data['description']}")
        
        return '\n'.join(found_files[:10]) if found_files else "• 🗂️ Standard project files detected"
    
    def _format_existing_readme(self, existing_readme: Dict) -> str:
        """Format existing README information"""
        if not existing_readme or not existing_readme.get('exists'):
            return "• 🆕 No existing README - creating from scratch with maximum visual impact!"
        
        filename = existing_readme.get('filename', 'README.md')
        content = existing_readme.get('content', '')
        lines = existing_readme.get('lines', 0)
        
        info = [
            f"• 📖 Existing README found: {filename}",
            f"• 📏 Current lines: {lines}",
            f"• 🔄 Enhancement mode: Will preserve good content and make it spectacular",
            f"• 👀 Current content preview:"
        ]
        
        if content:
            preview = content[:200].replace('\n', ' ').strip()
            info.append(f"  💭 \"{preview}...\"")
            info.append("• 🎨 Will enhance with modern design, badges, and visual elements")
        
        return '\n'.join(info)
    
    def get_debug_logs(self) -> List[str]:
        """📋 Get all debug logs"""
        return self.debug_log.copy()

# Test the smart generator
if __name__ == "__main__":
    print("🧪 Testing Smart AI Generator...")
    generator = SmartAIGenerator()
    print("✅ Smart generator ready!")