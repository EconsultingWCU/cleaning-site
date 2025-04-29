import requests
import json
import git
import os
from git.exc import GitCommandError

# Grok API setup
GROK_API_KEY = 'xai-gZ0Q2lMAFNoRxWKQjnmsjI3Jjk57cGssKw1GciAYscETJFnKHiEl0Sjk5ulJn7VmndwdYaUTGrEvWa5d'
GROK_API_URL = 'https://api.x.ai/v1/chat/completions'

# GitHub repository setup
REPO_PATH = '/home/wouter/test_6'
REPO_URL = 'https://github.com/EconsultingWCU/cleaning-site.git'
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')  # Load token from environment variable

def generate_html_with_grok():
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {GROK_API_KEY}'
        }
        payload = {
            'model': 'grok-3-mini-beta',
            'messages': [
                {
                    'role': 'user',
                    'content': 'Generate HTML content for a simple cleaning services website homepage.'
                }
            ]
        }
        response = requests.post(GROK_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()
        html_content = response_data['choices'][0]['message']['content']
        return html_content
    except requests.RequestException as e:
        print(f"Error generating HTML: {e}")
        return None

def push_to_github():
    try:
        if not GITHUB_TOKEN:
            print("Error: GITHUB_TOKEN environment variable not set")
            return
        os.chdir(REPO_PATH)
        print(f"Working in directory: {REPO_PATH}")
        html_content = generate_html_with_grok()
        if not html_content:
            print("Failed to generate HTML content")
            return
        with open('index.html', 'w') as f:
            f.write(html_content)
        print("HTML generated successfully")
        repo = git.Repo(REPO_PATH)
        repo.git.add('index.html')
        repo.index.commit('Update index.html with new content')
        origin = repo.remote(name='origin')
        origin.push()
        print("Successfully pushed to GitHub")
    except GitCommandError as e:
        print(f"Error pushing to GitHub: {e}")
    except Exception as e:
        print(f"Main error: {e}")

if __name__ == '__main__':
    push_to_github()