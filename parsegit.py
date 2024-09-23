import urllib.request
import json
import ssl
import os
import time


n = 5  # number of fetched READMEs
url = 'https://api.github.com/search/repositories?q=stars:%3E500&sort=stars'
request = urllib.request.urlopen(url)
page = request.read().decode()
api_json = json.loads(page)

def user_repos(username):
  user_repos = f"https://api.github.com/users/{username}/repos"
  request = urllib.request.urlopen(user_repos)
  page = request.read().decode()
  api_json = json.loads(page)
  return api_json

def get_repos_readmes(save_dir, repos):
  for repo in repos:
      full_name = repo['full_name']
      print('fetching readme from', full_name)

      # find readme url (case senitive)
      contents_url = repo['url'] + '/contents'
      print(contents_url)
      try:
        request = urllib.request.urlopen(contents_url)
      except Exception as e:
        print(e)
        continue
      page = request.read().decode()
      contents_json = contents_json = json.loads(page)
      try:
        readme_url = [file['download_url'] for file in contents_json if file['name'].lower() == 'readme.md'][0]
      except:
        continue

      # download readme contents
      try:
          context = ssl._create_unverified_context()  # prevent ssl problems
          request = urllib.request.urlopen(readme_url, context=context)
      except urllib.error.HTTPError as error:
          print(error)
          continue  # if the url can't be opened, there's no use to try to download anything
      readme = request.read().decode()

      # create folder named after repo's name and save readme.md there
      save_path = os.path.join(save_dir, repo['name'])
      try:
          os.mkdir(save_dir)
          os.mkdir(save_path)

      except OSError as error:
          print(error)
      f = open(os.path.join(save_path, "README.md"), 'w', encoding="utf-8")
      f.write(readme)
      print('ok')

      # only 10 requests per min for unauthenticated requests
      if n >= 9:  # n + 1 initial request
          time.sleep(6)

def save_user_repos(save_dir, username):
  repos = user_repos(username)
  get_repos_readmes(save_dir, repos)

# Example
# save_user_repos('goin2crazy')


import shutil

def move_readme_files(open_dir='repositories', save_dir='articles'):
  """Moves README files from subfolders to a new folder 'articles'."""
  if not os.path.exists(save_dir):
    os.makedirs(save_dir)

  for root, _, files in os.walk(open_dir):
    for file in files:
      if file.lower() == 'readme.md':
        source_path = os.path.join(root, file)
        parent_folder_name = os.path.basename(root)
        destination_filename = os.path.join(save_dir, parent_folder_name + '.md')
        shutil.copy(source_path, destination_filename)
        print(f"Moved {source_path} to {destination_filename}")
