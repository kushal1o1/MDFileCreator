"""
Enhanced AI Integration for MD Creator App
Integrates the fixed enhanced README generator into the existing GUI
"""

import threading
import time
import os
import json
from typing import Callable, Optional, Dict, Any
from dotenv import load_dotenv

try:
    from smart_ai_generator import SmartAIGenerator
    from github_collector import GitHubCollector
    AI_GENERATOR_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import AI modules: {e}")
    AI_GENERATOR_AVAILABLE = False

# Load environment variables
load_dotenv()

class AIIntegration:
    """
    Enhanced integration class for the MD Creator app using comprehensive GitHub data
    """
    
    def __init__(self, progress_callback: Optional[Callable] = None, result_callback: Optional[Callable] = None):
        self.progress_callback = progress_callback
        self.result_callback = result_callback
        self.is_running = False
        self._validate_setup()
        
    def _validate_setup(self) -> None:
        """Validate that all required components are available"""
        if not AI_GENERATOR_AVAILABLE:
            print("⚠️  Warning: AI modules not available")
            return
            
        # Check for required environment variables
        groq_key = os.getenv('GROQ_API_KEY')
        github_token = os.getenv('GITHUB_TOKEN')
        
        if not groq_key:
            print("⚠️  Warning: GROQ_API_KEY not found in environment")
        if not github_token:
            print("⚠️  Warning: GITHUB_TOKEN not found in environment (API rate limits will apply)")
        
    def generate_readme_async(self, github_url: str, style: str = "🤖 Let AI Choose Best Style") -> None:
        """
        Generate README asynchronously (for GUI integration)
        """
        if self.is_running:
            self._send_result({
                'success': False,
                'error': 'Generation already in progress',
                'logs': []
            })
            return
            
        def generate():
            self.is_running = True
            try:
                self._send_progress("Starting README generation...")
                
                if not AI_GENERATOR_AVAILABLE:
                    raise Exception("AI modules not available. Please install required dependencies.")
                
                if not github_url or not isinstance(github_url, str):
                    raise Exception("Invalid GitHub URL provided")
                
                # Create enhanced GitHub collector and AI generator
                self._send_progress("Initializing GitHub collector...")
                collector = GitHubCollector()
                
                self._send_progress("Initializing Smart AI generator...")
                generator = SmartAIGenerator()
                
                self._send_progress("Collecting comprehensive GitHub data...")
                
                # Collect comprehensive GitHub data
                github_data = collector.collect_comprehensive_data(github_url)
                
                if not isinstance(github_data, dict):
                    raise Exception("Invalid data returned from GitHub collector")
                
                if 'error' in github_data:
                    raise Exception(f"GitHub data collection failed: {github_data['error']}")
                
                self._send_progress("Generating professional README with AI...")
                
                # Save data temporarily
                temp_data_file = f"temp_github_data_{int(time.time())}.json"
                try:
                    with open(temp_data_file, 'w', encoding='utf-8') as f:
                        json.dump(github_data, f, indent=2, default=str)
                    
                    # Generate README using the comprehensive data with selected style
                    readme_content = generator.generate_smart_readme(
                        github_url=github_url,
                        data_file=temp_data_file,
                        style=style
                    )
                    
                    if not readme_content or not isinstance(readme_content, str):
                        raise Exception("AI generator returned empty or invalid content")
                    
                finally:
                    # Clean up temp file
                    if os.path.exists(temp_data_file):
                        try:
                            os.remove(temp_data_file)
                        except Exception as e:
                            print(f"Warning: Could not remove temp file: {e}")
                
                # Get debug logs from both collector and generator
                debug_logs = []
                try:
                    debug_logs.extend(collector.get_debug_logs())
                    debug_logs.extend(generator.get_debug_logs())
                except Exception as e:
                    debug_logs.append(f"Warning: Could not retrieve all debug logs: {e}")
                
                self._send_progress("README generation complete!")
                
                self._send_result({
                    'success': True,
                    'content': readme_content,
                    'logs': debug_logs,
                    'github_data': {
                        'owner': github_data.get('owner', 'Unknown'),
                        'repo': github_data.get('repo', 'Unknown'),
                        'stars': github_data.get('basic_info', {}).get('stars', 0),
                        'language': github_data.get('basic_info', {}).get('language', 'Unknown')
                    }
                })
                    
            except Exception as e:
                error_message = str(e)
                print(f"Error in generate_readme_async: {error_message}")
                
                self._send_result({
                    'success': False,
                    'error': error_message,
                    'logs': [f"Fatal error: {error_message}"]
                })
            finally:
                self.is_running = False
        
        # Run in background thread
        thread = threading.Thread(target=generate, name="README-Generator")
        thread.daemon = True
        thread.start()
    
    def generate_readme_sync(self, github_url: str, style: str = "🤖 Let AI Choose Best Style") -> Dict[str, Any]:
        """
        Generate README synchronously (for testing)
        """
        try:
            if not AI_GENERATOR_AVAILABLE:
                return {
                    'success': False,
                    'error': 'AI modules not available. Please install required dependencies.',
                    'logs': []
                }
            
            if not github_url or not isinstance(github_url, str):
                return {
                    'success': False,
                    'error': 'Invalid GitHub URL provided',
                    'logs': []
                }
            
            # Create enhanced GitHub collector and AI generator
            collector = GitHubCollector()
            generator = SmartAIGenerator()
            
            # Collect comprehensive GitHub data
            github_data = collector.collect_comprehensive_data(github_url)
            
            if not isinstance(github_data, dict):
                return {
                    'success': False,
                    'error': 'Invalid data returned from GitHub collector',
                    'logs': []
                }
            
            if 'error' in github_data:
                return {
                    'success': False,
                    'error': f"GitHub data collection failed: {github_data['error']}",
                    'logs': collector.get_debug_logs()
                }
            
            # Save data temporarily
            temp_data_file = f"temp_sync_github_data_{int(time.time())}.json"
            try:
                with open(temp_data_file, 'w', encoding='utf-8') as f:
                    json.dump(github_data, f, indent=2, default=str)
                
                # Generate README using the comprehensive data with selected style
                readme_content = generator.generate_smart_readme(
                    github_url=github_url,
                    data_file=temp_data_file,
                    style=style
                )
                
                if not readme_content or not isinstance(readme_content, str):
                    return {
                        'success': False,
                        'error': 'AI generator returned empty or invalid content',
                        'logs': generator.get_debug_logs()
                    }
                
            finally:
                # Clean up temp file
                if os.path.exists(temp_data_file):
                    try:
                        os.remove(temp_data_file)
                    except Exception as e:
                        print(f"Warning: Could not remove temp file: {e}")
            
            # Get debug logs from both collector and generator
            debug_logs = []
            try:
                debug_logs.extend(collector.get_debug_logs())
                debug_logs.extend(generator.get_debug_logs())
            except Exception as e:
                debug_logs.append(f"Warning: Could not retrieve all debug logs: {e}")
            
            return {
                'success': True,
                'content': readme_content,
                'logs': debug_logs,
                'github_data': {
                    'owner': github_data.get('owner', 'Unknown'),
                    'repo': github_data.get('repo', 'Unknown'),
                    'stars': github_data.get('basic_info', {}).get('stars', 0),
                    'language': github_data.get('basic_info', {}).get('language', 'Unknown')
                }
            }
            
        except Exception as e:
            error_message = str(e)
            print(f"Error in generate_readme_sync: {error_message}")
            
            return {
                'success': False,
                'error': error_message,
                'logs': [f"Fatal error: {error_message}"]
            }
    
    def _send_progress(self, message: str) -> None:
        """Send progress update to callback if available"""
        if self.progress_callback and callable(self.progress_callback):
            try:
                self.progress_callback(message)
            except Exception as e:
                print(f"Error in progress callback: {e}")
    
    def _send_result(self, result: Dict[str, Any]) -> None:
        """Send result to callback if available"""
        if self.result_callback and callable(self.result_callback):
            try:
                self.result_callback(result)
            except Exception as e:
                print(f"Error in result callback: {e}")
    
    def is_generation_running(self) -> bool:
        """Check if generation is currently running"""
        return self.is_running
    
    def get_setup_status(self) -> Dict[str, Any]:
        """Get status of setup requirements"""
        return {
            'ai_modules_available': AI_GENERATOR_AVAILABLE,
            'groq_api_key': bool(os.getenv('GROQ_API_KEY')),
            'github_token': bool(os.getenv('GITHUB_TOKEN')),
            'ready': AI_GENERATOR_AVAILABLE and bool(os.getenv('GROQ_API_KEY'))
        }

# Test function for the integration
def test_integration():
    """Test the AI integration"""
    
    def progress_update(message: str):
        print(f"Progress: {message}")
    
    def result_handler(result: Dict[str, Any]):
        print("\n=== RESULT ===")
        if result.get('success'):
            print("✅ Success!")
            content = result.get('content', '')
            print(f"README content length: {len(content)} characters")
            
            github_data = result.get('github_data', {})
            print(f"Repository: {github_data.get('owner')}/{github_data.get('repo')}")
            print(f"Stars: {github_data.get('stars')}")
            print(f"Language: {github_data.get('language')}")
            
            print(f"\nFirst 500 characters of README:")
            print(content[:500] + "..." if len(content) > 500 else content)
        else:
            print("❌ Failed!")
            print(f"Error: {result.get('error')}")
        
        print(f"\n=== DEBUG LOGS ({len(result.get('logs', []))}) ===")
        for log in result.get('logs', [])[-10:]:  # Show last 10 logs
            print(log)
    
    # Test with a simple repository
    integration = AIIntegration(progress_update, result_handler)
    
    # Check setup status
    status = integration.get_setup_status()
    print("=== SETUP STATUS ===")
    for key, value in status.items():
        print(f"{key}: {value}")
    
    if not status['ready']:
        print("❌ Setup not ready. Please check environment variables.")
        return
    
    test_repo = "https://github.com/kushal1o1/MDFileCreator"  
    print(f"\nTesting with repository: {test_repo}")
    
    # Test sync version first
    print("\n=== TESTING SYNC VERSION ===")
    result = integration.generate_readme_sync(test_repo)
    result_handler(result)
    
    # Test async version
    print("\n=== TESTING ASYNC VERSION ===")
    integration.generate_readme_async(test_repo)
    
    # Wait for completion (in real GUI this wouldn't be needed)
    max_wait = 30  # 30 seconds max
    waited = 0
    while integration.is_generation_running() and waited < max_wait:
        time.sleep(1)
        waited += 1
        if waited % 5 == 0:
            print(f"Still waiting... ({waited}/{max_wait}s)")
    
    if integration.is_generation_running():
        print("⚠️  Async test timed out")
    else:
        print("✅ Async test completed")

if __name__ == "__main__":
    test_integration()