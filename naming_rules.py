import re
import requests
from github import Github

# Set the GitHub API endpoint and repository information
github_api = 'https://api.github.com'
owner = 'owner_name'  # Replace with the repository owner's username or organization name
repo_name = 'repo_name'  # Replace with the name of the repository
branch = 'main'  # Replace with the branch you want to check file and folder names in

# Set up the GitHub API headers with an access token
access_token = 'access_token'
headers = {'Authorization': f'token {access_token}'}

# Define the rules for file and folder names
name_regex = re.compile('^[a-z0-9]+(-[a-z0-9]+)*$')
max_length = 80
action_verbs = ['develop', 'buy', 'build', 'troubleshoot']
small_words = [' a ', ' an ', ' the ', ' and ', ' in ']
markdown_ext = '.md'
landing_pages = ['toc.yml', 'index.yml']
redundancy_segments = ['docs', 'documentation', 'doc']

# Get a list of all files and folders in the repository
url = f'{github_api}/repos/{owner}/{repo_name}/git/trees/{branch}?recursive=1'
response = requests.get(url, headers=headers)
tree = response.json()['tree']

# Check each file and folder name against the specified rules and flag any issues
for item in tree:
    if item['type'] == 'blob':
        # Check the file name against the specified rules
        name = item['path'].split('/')[-1]
        if not name_regex.match(name.split('.')[0]):
            print(f'Invalid file name: {name}')
        if len(name) > max_length:
            print(f'File name is too long: {name}')
        if name.endswith('.md') and name not in landing_pages:
            if ' ' in name:
                print(f'Invalid file name: {name}')
            if any(word in name for word in small_words):
                print(f'File name contains unnecessary small words: {name}')
            if any(verb in name for verb in action_verbs):
                print(f'File name contains "-ing" words: {name}')
        elif not name.endswith('.yml') and not name.endswith('.yaml'):
            if name.split('.')[0] not in redundancy_segments:
                if ' ' in name:
                    print(f'Invalid file name: {name}')
                if any(word in name for word in small_words):
                    print(f'File name contains unnecessary small words: {name}')
                if any(verb in name for verb in action_verbs):
                    print(f'File name contains "-ing" words: {name}')
    elif item['type'] == 'tree':
        # Check the folder name against the specified rules
        name = item['path'].split('/')[-1]
        if not name_regex.match(name):
            print(f'Invalid folder name: {name}')
        if len(name) > max_length:
            print(f'Folder name is too long: {name}')
        if ' ' in name:
            print(f'Invalid folder name: {name}')
        if any(word in name for word in small_words):
            print(f'Folder name contains unnecessary small words: {name}')
        if any(verb in name for verb in action_verbs):
            print(f'Folder name contains "-ing" words: {name}')
