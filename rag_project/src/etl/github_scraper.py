import requests
import base64
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi
import re
from src.rag import get_task


class GitHubScraper:
    def __init__(self):
        self.task = get_task()
        self.token = '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'
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'RAG-Project'
        }

    def get_default_branch(self, owner, repo):
        try:
            url = f'https://api.github.com/repos/{owner}/{repo}'
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()['default_branch']
        except Exception as e:
            print(f"Error getting default branch: {str(e)}")
            return 'main'  

    def get_file_content(self, owner, repo, path, ref='main'):
        """Get content of a specific file"""
        try:
            url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
            response = requests.get(url, headers=self.headers, params={'ref': ref})
            response.raise_for_status()
            
            content = response.json()
            if 'content' in content:
                try:
                    decoded_content = base64.b64decode(content['content']).decode('utf-8')
                    return {
                        'path': path,
                        'content': decoded_content,
                        'sha': content['sha'],
                        'size': content['size'],
                        'timestamp': datetime.now()
                    }
                except UnicodeDecodeError:
                    # Skip binary files
                    return None
            return None
        except Exception as e:
            print(f"Error getting file content for {path}: {str(e)}")
            return None

    def get_tree_recursive(self, owner, repo, branch=None):
        try:
            if branch is None:
                branch = self.get_default_branch(owner, repo)
            
            url = f'https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}'
            response = requests.get(url, headers=self.headers, params={'recursive': 1})
            response.raise_for_status()
            return response.json()['tree']
        except Exception as e:
            print(f"Error getting repository tree: {str(e)}")
            return None

    def scrape_repo(self, repo_url):
        """Scrape entire repository"""
        self.task.get_logger().report_text(f"Scraping repository: {repo_url}")
        try:
            # Parse repo URL
            parts = repo_url.rstrip('/').split('/')
            owner = parts[-2]
            repo = parts[-1]
            
            # Get default branch
            branch = self.get_default_branch(owner, repo)
            
            # Get all files in the repository
            files = self.get_tree_recursive(owner, repo, branch)
            if not files:
                return None
            
            repository_content = []
            for file in files:
                if file['type'] == 'blob':  # Only process files, not directories
                    # Skip binary and large files
                    if file['size'] > 10000000:  # Skip files larger than 10MB
                        continue
                    
                    content = self.get_file_content(owner, repo, file['path'], branch)
                    if content:
                        repository_content.append(content)
            
            return {
                'url': repo_url,
                'files': repository_content,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            print(f"Error scraping {repo_url}: {str(e)}")
            return None
        

class ContentScraper:
    def __init__(self):
        super().__init__()
        
    def extract_video_id(self, youtube_url):
        """Extract video ID from YouTube URL"""
        pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
        match = re.search(pattern, youtube_url)
        return match.group(1) if match else None

    def get_youtube_transcript(self, url):
        try:
            video_id = self.extract_video_id(url)
            if not video_id:
                return None
                
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            
            # Combine transcript entries
            full_text = ' '.join([entry['text'] for entry in transcript])
            
            return {
                'url': url,
                'content': full_text,
                'type': 'youtube',
                'timestamp': datetime.now()
            }
        except Exception as e:
            print(f"Error getting transcript for {url}: {str(e)}")
            return None
