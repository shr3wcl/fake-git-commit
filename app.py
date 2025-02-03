from git import Repo, Actor
import os
import random
import sys
import time
import faker
import requests
from art import text2art

GITHUB_USERNAME = "your_github_username"
GITHUB_TOKEN = "your_github_personal_access_token" 
REPO_NAME = "fake-commit-github"
REPO_URL = f'https://github.com/{GITHUB_USERNAME}/{REPO_NAME}.git'


def github_repo_exists(repo_name):
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}"
    response = requests.get(url, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
    return response.status_code == 200  

def create_github_repo(repo_name):
    url = "https://api.github.com/user/repos"
    data = {"name": repo_name, "private": False}
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    response = requests.post(url, json=data, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
    
    if response.status_code == 201:
        print(f"[+] Repository '{repo_name}' has been created on GitHub.")
        return True
    else:
        print(f"[-] Failed to create repository: {response.json()}")
        return False

def check_repo():
    repo_path = os.path.abspath(f"./{REPO_NAME}") 

    if not os.path.exists(repo_path):
        os.makedirs(repo_path)
        repo = Repo.init(repo_path)
        print(f"[+] Repository has been initialized locally at {repo_path}.")
    else:
        repo = Repo(repo_path)
        if repo.bare:
            print("[-] Directory exists but is not a Git repository. Initializing...")
            repo = Repo.init(repo_path)
            print(f"[+] Repository has been re-initialized at {repo_path}.")
        else:
            print(f"[+] Repository already exists at {repo_path}.")

    file_path = os.path.join(repo_path, "initial.txt")
    print(f"[+] Creating file at {file_path}.")
    with open(file_path, 'w') as file:
        file.write("This is an initial file to ensure there is something to commit.")
    
    repo.index.add([file_path])

    if repo.is_dirty(untracked_files=True):
        repo.index.commit("Initial commit")
        print("[+] Initial commit has been made.")
    else:
        print("[+] No changes to commit.")

    if not github_repo_exists(REPO_NAME):
        if create_github_repo(REPO_NAME):
            repo.create_remote("origin", f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git")
            repo.remotes.origin.push("refs/heads/master:refs/heads/master")          
            print(f"[+] Repository '{REPO_NAME}' has been pushed to GitHub.")
        else:
            print("[-] Could not create repository on GitHub.")
    else:
        print(f"[+] Repository '{REPO_NAME}' already exists on GitHub.")
        if "origin" not in repo.remotes:
            repo.create_remote("origin", f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git")

        if repo.active_branch.tracking_branch() is None:
            try:
                repo.git.push("--set-upstream", "origin", repo.active_branch.name)
                print("[+] Upstream branch set for current branch.")
            except Exception as e:
                print(f"[-] Failed to set upstream branch: {e}")

    return repo


def fake_commit(username, email, message="Fake commit",
                from_date="2021-01-01", to_date="2021-12-31",
                time_commit="12:00:00", is_random=False):
    global REPO_NAME, REPO_URL
    REPO_URL = f'https://github.com/{username}/{REPO_NAME}.git'

    repo = check_repo()
    fake = faker.Faker()

    fromdate = time.mktime(time.strptime(from_date, "%Y-%m-%d"))
    todate = time.mktime(time.strptime(to_date, "%Y-%m-%d"))
    
    while fromdate < todate:
        for _ in range(random.randint(1, 10) if is_random else 1): 
            file_name = f'{repo.working_dir}/fake_commit_file.txt'
            with open(file_name, 'w') as f:
                f.write(fake.text() + str(random.randint(0, 1000)) + fake.date() + fake.time() + fake.text())
            
            repo.index.add([file_name])
            author = Actor(username, email)
            date = time.strftime('%Y-%m-%d ', time.localtime(fromdate)) + time_commit

            os.environ['GIT_COMMITTER_DATE'] = date
            os.environ['GIT_AUTHOR_DATE'] = date

            repo.index.commit(message, author=author)

            del os.environ['GIT_COMMITTER_DATE']
            del os.environ['GIT_AUTHOR_DATE']

            print(f"[+] Date: {date}, Commit: {message}")
        
        fromdate += 86400

    if not repo.remotes:
        remote_url = input("[?] Enter the URL for the remote repository: ")
        repo.create_remote('origin', remote_url)
        try:
            repo.git.push("--set-upstream", "origin", repo.active_branch.name)
            print("[+] Upstream branch set for current branch.")
        except Exception as e:
            print(f"[-] Failed to set upstream branch: {e}")

    try:
        repo.remotes.origin.push()
        print("[+] Changes have been pushed to the remote repository.")
    except Exception as e:
        print(f"[-] Failed to push changes: {e}")

if __name__ == "__main__":
    print("""
          Welcome to Fake Commit GitHub - A tool to create fake commits on GitHub.
          ========================================================================
          =                         Author: shr3wd                               =
          =                 GitHub: https://github.com/shr3wcl                   =
          ========================================================================
          """)
    print(text2art("Fake Commit GitHub"))
    
    if len(sys.argv) < 2:
        GITHUB_USERNAME = input("[+] Enter your GitHub username: ")
        GITHUB_TOKEN = input("[+] Enter your GitHub personal access token: ")
        REPO_NAME = input("[+] Enter the repository name: ")
        username = input("[+] Enter your username: ")
        email = input("[+] Enter your email: ")
        message = input("[+] Enter your message: ")
        from_date = input("[+] Enter from date (YYYY-MM-DD): ")
        to_date = input("[+] Enter to date (YYYY-MM-DD): ")
        time_commit = input("[+] Enter time commit (HH:MM:SS): ")
        is_random = input("[+] Random commit (y/n): ")
        if is_random.lower() == "y":
            is_random = True
        else:
            is_random = False

        save_config = input("[+] Save configuration to .config file (y/n): ")
        if save_config.lower() == "y":
            with open(".config", "w") as f:
                f.write(f"{GITHUB_USERNAME}\n{GITHUB_TOKEN}\n{REPO_NAME}\n{username}\n{email}\n{message}\n{from_date}\n{to_date}\n{time_commit}\n{is_random}")
        fake_commit(username, email, message, from_date, to_date, time_commit, is_random)
    elif len(sys.argv) == 2 and sys.argv[1] == "config":
        try:
            with open(".config", "r") as f:
                data = f.read().splitlines()
                GITHUB_USERNAME = data[0]
                GITHUB_TOKEN = data[1]
                REPO_NAME = data[2]
                username = data[3]
                email = data[4]
                message = data[5]
                from_date = data[6]
                to_date = data[7]
                time_commit = data[8]
                is_random = data[9]
                # Nếu giá trị is_random là 'True' hoặc 'False' thì chuyển đổi:
                if str(is_random).lower() in ("true", "1", "y"):
                    is_random = True
                else:
                    is_random = False

                fake_commit(username, email, message, from_date, to_date, time_commit, is_random)
        except FileNotFoundError:
            print("[-] Could not find .config file.")
        sys.exit(1)
    elif len(sys.argv) == 2 and sys.argv[1] == "help":
        print("Usage: ")
        print("[1] Nếu muốn nhập tay: python app.py")
        print("[2] Dùng file cấu hình .config: python app.py config")
        print("[3] Xem help: python app.py help")
        print("[4] Dùng toàn bộ tham số dòng lệnh:")
        print("    python app.py <username> <email> <message> <from_date> <to_date> <time_commit> <is_random>")
        sys.exit(1)
    else:
        try:
            username = sys.argv[1]
            email = sys.argv[2]
            message = sys.argv[3]
            from_date = sys.argv[4]
            to_date = sys.argv[5]
            time_commit = sys.argv[6]
            is_random = sys.argv[7]
            if is_random.lower() == "y":
                is_random = True
            else:
                is_random = False

            save_config = input("[+] Save configuration to .config file (y/n): ")
            if save_config.lower() == "y":
                with open(".config", "w") as f:
                    f.write(f"{GITHUB_USERNAME}\n{GITHUB_TOKEN}\n{REPO_NAME}\n{username}\n{email}\n{message}\n{from_date}\n{to_date}\n{time_commit}\n{is_random}")
            fake_commit(username, email, message, from_date, to_date, time_commit, is_random)
        except IndexError:
            print("Usage: python app.py <username> <email> <message> <from_date> <to_date> <time_commit> <is_random>")
            sys.exit(1)
