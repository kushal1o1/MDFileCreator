"""
ENHANCED GitHub API Collector
Uses GitHub token to get comprehensive repository data for AI README generation
"""

import requests
import json
import time
import os
import base64
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GitHubCollector:
    """
    Enhanced GitHub API collector that uses authentication token
    to get comprehensive repository information
    """
    
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.base_url = "https://api.github.com"
        self.session = requests.Session()
        self.debug_log = []
        
        # Set up session with proper headers
        self.session.headers.update({
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'MDFileCreator-GitHub-Collector/1.0'
        })
        
        if self.github_token:
            self.session.headers.update({
                'Authorization': f'token {self.github_token}'
            })
            self.log("✅ GitHub API authenticated with token")
        else:
            self.log("⚠️  No GitHub token found - using unauthenticated requests (rate limited)")
        
        # Set timeout for all requests
        self.session.timeout = 15
    
    def log(self, message: str, data: Any = None) -> None:
        """Enhanced logging with better formatting"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        
        if data is not None:
            # Safely convert data to string with length limit
            data_str = str(data)
            if len(data_str) > 100:
                data_str = data_str[:100] + "..."
            log_entry += f" | Data: {data_str}"
            
        self.debug_log.append(log_entry)
        print(log_entry)
    
    def collect_comprehensive_data(self, github_url: str) -> Dict[str, Any]:
        """
        Collect comprehensive repository data using GitHub API
        """
        start_time = time.time()
        self.log("=== STARTING COMPREHENSIVE GITHUB DATA COLLECTION ===")
        self.log(f"Repository: {github_url}")
        
        try:
            # Parse and validate GitHub URL
            owner, repo = self._parse_github_url(github_url)
            if not owner or not repo:
                return {'error': 'Invalid GitHub URL format'}
            
            self.log(f"Parsed: {owner}/{repo}")
            
            # Initialize data structure
            data = {
                'owner': owner,
                'repo': repo,
                'url': github_url,
                'collection_timestamp': datetime.now().isoformat()
            }
            
            # Collect all data sections with error handling
            data_sections = [
                ('basic_info', self._get_basic_info),
                ('contents', self._get_repository_contents),
                ('languages', self._get_languages),
                ('recent_commits', self._get_recent_commits),
                ('issues', self._get_issues),
                ('pull_requests', self._get_pull_requests),
                ('contributors', self._get_contributors),
                ('releases', self._get_releases),
                ('topics', self._get_topics),
                ('existing_readme', self._get_existing_readme),
                ('package_files', self._get_package_files)
            ]
            
            for section_name, section_func in data_sections:
                try:
                    self.log(f"Collecting {section_name}...")
                    section_data = section_func(owner, repo)
                    data[section_name] = section_data if section_data is not None else {}
                    self.log(f"✅ {section_name} collected successfully")
                except Exception as e:
                    self.log(f"❌ Error collecting {section_name}: {e}")
                    data[section_name] = {'error': str(e)}
            
            duration = time.time() - start_time
            self.log(f"=== COMPREHENSIVE DATA COLLECTION COMPLETE in {duration:.2f}s ===")
            
            return data
            
        except Exception as e:
            self.log(f"💥 FATAL ERROR: {e}")
            return {'error': f'Fatal collection error: {str(e)}'}
    
    def _parse_github_url(self, github_url: str) -> tuple[Optional[str], Optional[str]]:
        """Parse GitHub URL to extract owner and repo"""
        if not github_url or not isinstance(github_url, str):
            self.log("ERROR: Invalid GitHub URL provided")
            return None, None
        
        # Clean up the URL
        github_url = github_url.strip()
        
        # Handle different GitHub URL formats
        patterns = [
            r'github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?/?$',
            r'github\.com/([^/]+)/([^/]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, github_url)
            if match:
                owner, repo = match.groups()
                # Clean repo name
                repo = repo.replace('.git', '').strip()
                return owner.strip(), repo
        
        self.log(f"ERROR: Could not parse GitHub URL: {github_url}")
        return None, None
    
    def _make_api_request(self, url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> Optional[Dict]:
        """Make API request with error handling and rate limiting"""
        try:
            request_headers = self.session.headers.copy()
            if headers:
                request_headers.update(headers)
            
            response = self.session.get(url, params=params, headers=request_headers)
            
            # Check rate limiting
            if response.status_code == 403:
                rate_limit_remaining = response.headers.get('X-RateLimit-Remaining', '0')
                if rate_limit_remaining == '0':
                    self.log("⚠️  GitHub API rate limit exceeded")
                    return {'error': 'Rate limit exceeded'}
            
            if response.status_code == 404:
                self.log(f"⚠️  Resource not found: {url}")
                return {}
            
            if response.status_code != 200:
                self.log(f"⚠️  API request failed: {response.status_code} for {url}")
                return {'error': f'HTTP {response.status_code}'}
            
            return response.json()
            
        except requests.exceptions.Timeout:
            self.log(f"⚠️  Timeout for request: {url}")
            return {'error': 'Request timeout'}
        except requests.exceptions.RequestException as e:
            self.log(f"⚠️  Request error for {url}: {e}")
            return {'error': f'Request error: {str(e)}'}
        except json.JSONDecodeError as e:
            self.log(f"⚠️  JSON decode error for {url}: {e}")
            return {'error': 'Invalid JSON response'}
        except Exception as e:
            self.log(f"⚠️  Unexpected error for {url}: {e}")
            return {'error': f'Unexpected error: {str(e)}'}
    
    def _get_basic_info(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get comprehensive basic repository information"""
        url = f"{self.base_url}/repos/{owner}/{repo}"
        response_data = self._make_api_request(url)
        
        if not response_data or 'error' in response_data:
            return response_data or {}
        
        # Extract and clean the data
        return {
            'name': response_data.get('name', ''),
            'full_name': response_data.get('full_name', ''),
            'description': response_data.get('description') or 'No description provided',
            'language': response_data.get('language') or 'Multiple',
            'size': response_data.get('size', 0),
            'stars': response_data.get('stargazers_count', 0),
            'forks': response_data.get('forks_count', 0),
            'watchers': response_data.get('watchers_count', 0),
            'open_issues': response_data.get('open_issues_count', 0),
            'license': response_data.get('license', {}).get('name') if response_data.get('license') else 'Not specified',
            'homepage': response_data.get('homepage') or 'None',
            'clone_url': response_data.get('clone_url', ''),
            'ssh_url': response_data.get('ssh_url', ''),
            'created_at': response_data.get('created_at', ''),
            'updated_at': response_data.get('updated_at', ''),
            'pushed_at': response_data.get('pushed_at', ''),
            'default_branch': response_data.get('default_branch', 'main'),
            'topics': response_data.get('topics', []),
            'archived': response_data.get('archived', False),
            'disabled': response_data.get('disabled', False),
            'visibility': response_data.get('visibility', 'public'),
            'has_wiki': response_data.get('has_wiki', False),
            'has_pages': response_data.get('has_pages', False),
            'has_projects': response_data.get('has_projects', False)
        }
    
    def _get_repository_contents(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get ALL repository files recursively and important files"""
        try:
            # Try recursive tree API first (most efficient)
            tree_data = self._get_git_tree(owner, repo)
            if tree_data and 'error' not in tree_data:
                return tree_data
            
            # Fallback to root contents only
            self.log("Tree API failed, falling back to root contents")
            return self._get_root_contents_only(owner, repo)
            
        except Exception as e:
            self.log(f"Error in _get_repository_contents: {e}")
            return {'error': str(e)}

    def _get_git_tree(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get complete repository structure using Git Trees API"""
        url = f"{self.base_url}/repos/{owner}/{repo}/git/trees/HEAD"
        params = {'recursive': '1'}
        response_data = self._make_api_request(url, params=params)
        
        if not response_data or 'error' in response_data:
            return response_data or {}
        
        all_files = []
        all_directories = set()
        important_files = {}
        
        tree_items = response_data.get('tree', [])
        if not isinstance(tree_items, list):
            return {'error': 'Invalid tree data'}
        
        for item in tree_items:
            if not isinstance(item, dict):
                continue
                
            path = item.get('path', '')
            if not path:
                continue
            
            if item.get('type') == 'blob':  # File
                file_info = {
                    'name': os.path.basename(path),
                    'path': path,
                    'size': item.get('size', 0),
                    'sha': item.get('sha', '')
                }
                all_files.append(file_info)
                
                # Add parent directories
                dir_path = os.path.dirname(path)
                while dir_path and dir_path != '.':
                    all_directories.add(dir_path)
                    dir_path = os.path.dirname(dir_path)
                
                # Check for important files
                self._categorize_important_file(file_info, important_files)
                
            elif item.get('type') == 'tree':  # Directory
                all_directories.add(path)
        
        return {
            'files': all_files,
            'directories': sorted(list(all_directories)),
            'important_files': important_files,
            'total_files': len(all_files),
            'total_directories': len(all_directories),
            'file_extensions': self._analyze_file_extensions(all_files),
            'directory_structure': self._build_directory_structure(all_files, all_directories)
        }

    def _categorize_important_file(self, file_info: Dict, important_files: Dict) -> None:
        """Categorize important files"""
        filename = file_info['name'].lower()
        path = file_info['path'].lower()
        
        # Important file patterns
        important_patterns = {
            'readme': ['readme.md', 'readme.txt', 'readme.rst', 'readme'],
            'package.json': ['package.json'],
            'requirements.txt': ['requirements.txt'],
            'setup.py': ['setup.py'],
            'cargo.toml': ['cargo.toml'],
            'go.mod': ['go.mod'],
            'dockerfile': ['dockerfile'],
            'docker-compose.yml': ['docker-compose.yml', 'docker-compose.yaml'],
            '.env.example': ['.env.example'],
            '.gitignore': ['.gitignore'],
            'license': ['license', 'license.txt', 'license.md', 'mit-license.txt'],
            'contributing': ['contributing.md', 'contributing.txt'],
            'changelog': ['changelog.md', 'changelog.txt', 'history.md']
        }
        
        # Main application files
        main_files = ['app.py', 'main.py', 'index.js', 'server.js', 'manage.py', 'index.html']
        
        for category, patterns in important_patterns.items():
            if filename in patterns:
                important_files[category] = file_info
                break
        
        if filename in main_files:
            important_files[f'main_{filename}'] = file_info

    def _analyze_file_extensions(self, files: List[Dict]) -> Dict[str, int]:
        """Analyze file extensions to understand project structure"""
        extensions = {}
        for file in files:
            if not isinstance(file, dict):
                continue
            name = file.get('name', '')
            if '.' in name:
                ext = name.split('.')[-1].lower()
                extensions[ext] = extensions.get(ext, 0) + 1
        return extensions

    def _build_directory_structure(self, files: List[Dict], directories: set) -> Dict[str, Any]:
        """Build a simplified directory structure"""
        structure = {}
        
        # Count files in each directory
        dir_file_counts = {}
        for file in files:
            if not isinstance(file, dict):
                continue
            path = file.get('path', '')
            dir_path = os.path.dirname(path)
            if dir_path and dir_path != '.':
                dir_file_counts[dir_path] = dir_file_counts.get(dir_path, 0) + 1
        
        # Build simplified structure
        for directory in sorted(directories):
            if isinstance(directory, str):
                structure[directory] = {
                    'type': 'directory',
                    'file_count': dir_file_counts.get(directory, 0)
                }
        
        return structure

    def _get_root_contents_only(self, owner: str, repo: str) -> Dict[str, Any]:
        """Fallback method to get only root directory contents"""
        url = f"{self.base_url}/repos/{owner}/{repo}/contents"
        response_data = self._make_api_request(url)
        
        if not response_data or 'error' in response_data:
            return response_data or {}
        
        if not isinstance(response_data, list):
            return {'error': 'Invalid contents data'}
        
        files = []
        directories = []
        important_files = {}
        
        for item in response_data:
            if not isinstance(item, dict):
                continue
                
            if item.get('type') == 'file':
                file_info = {
                    'name': item.get('name', ''),
                    'path': item.get('name', ''),
                    'size': item.get('size', 0),
                    'download_url': item.get('download_url', '')
                }
                files.append(file_info)
                self._categorize_important_file(file_info, important_files)
                
            elif item.get('type') == 'dir':
                directories.append(item.get('name', ''))
        
        return {
            'files': files,
            'directories': directories,
            'important_files': important_files,
            'total_files': len(files),
            'total_directories': len(directories),
            'file_extensions': self._analyze_file_extensions(files),
            'directory_structure': {}
        }
    
    def _get_languages(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get programming languages used with percentages"""
        url = f"{self.base_url}/repos/{owner}/{repo}/languages"
        response_data = self._make_api_request(url)
        
        if not response_data or 'error' in response_data:
            return response_data or {}
        
        if not isinstance(response_data, dict):
            return {'error': 'Invalid languages data'}
        
        # Calculate percentages
        total_bytes = sum(response_data.values()) if response_data else 0
        language_percentages = {}
        
        for lang, bytes_count in response_data.items():
            if isinstance(bytes_count, (int, float)) and total_bytes > 0:
                percentage = (bytes_count / total_bytes * 100)
                language_percentages[lang] = {
                    'bytes': bytes_count,
                    'percentage': round(percentage, 2)
                }
        
        primary_language = max(response_data, key=response_data.get) if response_data else None
        
        return {
            'languages': language_percentages,
            'primary_language': primary_language,
            'total_bytes': total_bytes
        }
    
    def _get_recent_commits(self, owner: str, repo: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent commits"""
        url = f"{self.base_url}/repos/{owner}/{repo}/commits"
        params = {'per_page': min(limit, 100)}  # GitHub max is 100
        response_data = self._make_api_request(url, params=params)
        
        if not response_data or 'error' in response_data:
            return []
        
        if not isinstance(response_data, list):
            return []
        
        commits = []
        for commit in response_data:
            if not isinstance(commit, dict):
                continue
                
            commit_data = commit.get('commit', {})
            if not isinstance(commit_data, dict):
                continue
            
            author_data = commit_data.get('author', {})
            if not isinstance(author_data, dict):
                continue
            
            commit_info = {
                'sha': (commit.get('sha', ''))[:7],
                'message': (commit_data.get('message', '')).split('\n')[0][:100],  # First line, max 100 chars
                'author': author_data.get('name', 'Unknown'),
                'date': author_data.get('date', ''),
                'url': commit.get('html_url', '')
            }
            commits.append(commit_info)
        
        return commits
    
    def _get_issues(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get issues information"""
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        params = {'state': 'open', 'per_page': 5}
        response_data = self._make_api_request(url, params=params)
        
        if not response_data or 'error' in response_data:
            return {'open_issues': [], 'open_count': 0}
        
        if not isinstance(response_data, list):
            return {'open_issues': [], 'open_count': 0}
        
        open_issues = []
        for issue in response_data:
            if not isinstance(issue, dict):
                continue
            # Exclude pull requests (they appear in issues API)
            if 'pull_request' in issue:
                continue
                
            labels = issue.get('labels', [])
            label_names = []
            if isinstance(labels, list):
                label_names = [label.get('name', '') for label in labels if isinstance(label, dict)]
            
            issue_info = {
                'title': issue.get('title', '')[:100],  # Limit title length
                'number': issue.get('number', 0),
                'labels': label_names,
                'created_at': issue.get('created_at', ''),
                'url': issue.get('html_url', '')
            }
            open_issues.append(issue_info)
        
        return {
            'open_issues': open_issues,
            'open_count': len(open_issues)
        }
    
    def _get_pull_requests(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get pull requests information"""
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls"
        params = {'state': 'open', 'per_page': 5}
        response_data = self._make_api_request(url, params=params)
        
        if not response_data or 'error' in response_data:
            return {'open_pull_requests': [], 'open_count': 0}
        
        if not isinstance(response_data, list):
            return {'open_pull_requests': [], 'open_count': 0}
        
        open_prs = []
        for pr in response_data:
            if not isinstance(pr, dict):
                continue
                
            user_data = pr.get('user', {})
            author = user_data.get('login', 'Unknown') if isinstance(user_data, dict) else 'Unknown'
            
            pr_info = {
                'title': pr.get('title', '')[:100],  # Limit title length
                'number': pr.get('number', 0),
                'author': author,
                'created_at': pr.get('created_at', ''),
                'url': pr.get('html_url', '')
            }
            open_prs.append(pr_info)
        
        return {
            'open_pull_requests': open_prs,
            'open_count': len(open_prs)
        }
    
    def _get_contributors(self, owner: str, repo: str) -> List[Dict[str, Any]]:
        """Get repository contributors"""
        url = f"{self.base_url}/repos/{owner}/{repo}/contributors"
        params = {'per_page': 10}
        response_data = self._make_api_request(url, params=params)
        
        if not response_data or 'error' in response_data:
            return []
        
        if not isinstance(response_data, list):
            return []
        
        contributors = []
        for contributor in response_data:
            if not isinstance(contributor, dict):
                continue
                
            contributor_info = {
                'login': contributor.get('login', ''),
                'contributions': contributor.get('contributions', 0),
                'avatar_url': contributor.get('avatar_url', ''),
                'url': contributor.get('html_url', '')
            }
            contributors.append(contributor_info)
        
        return contributors
    
    def _get_releases(self, owner: str, repo: str) -> List[Dict[str, Any]]:
        """Get repository releases"""
        url = f"{self.base_url}/repos/{owner}/{repo}/releases"
        params = {'per_page': 5}
        response_data = self._make_api_request(url, params=params)
        
        if not response_data or 'error' in response_data:
            return []
        
        if not isinstance(response_data, list):
            return []
        
        releases = []
        for release in response_data:
            if not isinstance(release, dict):
                continue
                
            release_info = {
                'tag_name': release.get('tag_name', ''),
                'name': release.get('name', ''),
                'published_at': release.get('published_at', ''),
                'prerelease': release.get('prerelease', False),
                'draft': release.get('draft', False),
                'url': release.get('html_url', '')
            }
            releases.append(release_info)
        
        return releases
    
    def _get_topics(self, owner: str, repo: str) -> List[str]:
        """Get repository topics"""
        url = f"{self.base_url}/repos/{owner}/{repo}/topics"
        headers = {'Accept': 'application/vnd.github.mercy-preview+json'}
        response_data = self._make_api_request(url, headers=headers)
        
        if not response_data or 'error' in response_data:
            return []
        
        names = response_data.get('names', [])
        return names if isinstance(names, list) else []
    
    def _get_existing_readme(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get existing README content if available"""
        readme_files = ['README.md', 'README.txt', 'README.rst', 'README', 'readme.md']
        
        for readme_file in readme_files:
            url = f"{self.base_url}/repos/{owner}/{repo}/contents/{readme_file}"
            response_data = self._make_api_request(url)
            
            if response_data and 'error' not in response_data and isinstance(response_data, dict):
                content_b64 = response_data.get('content', '')
                if content_b64:
                    try:
                        # Decode base64 content
                        content = base64.b64decode(content_b64).decode('utf-8')
                        
                        return {
                            'exists': True,
                            'filename': readme_file,
                            'content': content[:1000],  # First 1000 chars
                            'size': response_data.get('size', 0),
                            'full_content_available': len(content) > 1000
                        }
                    except Exception as e:
                        self.log(f"Error decoding README content: {e}")
                        continue
        
        return {'exists': False}
    
    def _get_package_files(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get content of important package/dependency files"""
        package_files = {}
        important_files = [
            'package.json', 'requirements.txt', 'setup.py', 
            'Cargo.toml', 'go.mod', 'composer.json', 
            'Gemfile', 'pom.xml', 'build.gradle'
        ]
        
        for filename in important_files:
            url = f"{self.base_url}/repos/{owner}/{repo}/contents/{filename}"
            response_data = self._make_api_request(url)
            
            if response_data and 'error' not in response_data and isinstance(response_data, dict):
                content_b64 = response_data.get('content', '')
                if content_b64:
                    try:
                        content = base64.b64decode(content_b64).decode('utf-8')
                        package_files[filename] = {
                            'content': content[:2000],  # First 2000 chars
                            'size': response_data.get('size', 0),
                            'truncated': len(content) > 2000
                        }
                    except Exception as e:
                        package_files[filename] = {'error': f'Could not decode: {str(e)}'}
        
        return package_files
    
    def get_debug_logs(self) -> List[str]:
        """Get all debug logs"""
        return self.debug_log.copy()
    
    def clear_debug_logs(self) -> None:
        """Clear debug logs"""
        self.debug_log.clear()


