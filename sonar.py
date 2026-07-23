import os
import sys
import json
import argparse
import random
import datetime
import subprocess
import urllib.request
import urllib.parse

CREDENTIALS_FILE = ".sonar_credentials.json"
DB_FILE = os.path.join("db", "processed_repos.json")
DEFAULT_CONFIG_TEMPLATE = os.path.join(".agents", "skills", "codebase-restructurer", "examples", "config.example.json")

def setup_credentials():
    print("=== Sonar CLI Setup ===")
    print("Please enter the required credentials and configuration settings below.")
    print("These will be stored in .sonar_credentials.json (gitignored).")
    print("-" * 50)
    
    push_pat = input("GitHub Push Token (PAT for secondary/push account): ").strip()
    sync_pat = input("GitHub Sync Token (PAT with issue write access to dchumari/sonar): ").strip()
    author_name = input("Default Git Author Name (e.g., Marc Barber): ").strip()
    author_email = input("Default Git Author Email (e.g., marcbarber@cc.cc): ").strip()
    
    default_dest = os.path.join(os.getcwd(), "scratch")
    dest_parent = input(f"Default parent directory for restructured codebases [default: {default_dest}]: ").strip()
    if not dest_parent:
        dest_parent = default_dest

    config = {
        "github_push_pat": push_pat,
        "github_sync_pat": sync_pat,
        "author_name": author_name,
        "author_email": author_email,
        "dest_parent": dest_parent
    }
    
    # Create scratch folder if it doesn't exist
    os.makedirs(dest_parent, exist_ok=True)

    with open(CREDENTIALS_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
        
    print(f"\n[+] Configuration successfully saved to {CREDENTIALS_FILE}\n")
    return config

def load_credentials():
    if not os.path.exists(CREDENTIALS_FILE):
        return setup_credentials()
    with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def auto_pull_db():
    print("[*] Checking for database updates from central repository...")
    try:
        # Verify if current directory is a git repository
        if os.path.exists(".git"):
            # Run git pull quietly
            res = subprocess.run(["git", "pull", "origin", "master"], capture_output=True, text=True)
            if res.returncode == 0:
                print("[+] Local database successfully synced with remote master branch.")
            else:
                # Fallback to general git pull
                res_fallback = subprocess.run(["git", "pull"], capture_output=True, text=True)
                if res_fallback.returncode == 0:
                    print("[+] Local database successfully synced.")
                else:
                    print(f"[!] Warning: Could not run git pull: {res_fallback.stderr.strip()}")
    except Exception as e:
        print(f"[!] Warning: Auto-pull database failed: {e}")

def load_db():
    if not os.path.exists(DB_FILE):
        # Create empty db file if it does not exist
        os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def generate_unique_name(db, dest_parent):
    adjectives = ["Silver", "Nebula", "Golden", "Silent", "Copper", "Crimson", "Shadow", "Azure", "Quantum", "Echo", "Frost", "Solar", "Lunar", "Cyber", "Void", "Spectral", "Phantom", "Iron", "Storm", "Velocity"]
    nouns = ["Falcon", "Crypt", "Eclipse", "Horizon", "Vortex", "Saber", "Sentinel", "Rogue", "Matrix", "Beacon", "Pinnacle", "Summit", "Canyon", "Glacier", "Drift", "Haven", "Nova", "Pulse", "Rift", "Spire"]
    
    existing_names = {entry.get("restructured_name") for entry in db if entry.get("restructured_name")}
    
    while True:
        name = f"{random.choice(adjectives)}{random.choice(nouns)}"
        dest_path = os.path.join(dest_parent, name)
        if name not in existing_names and not os.path.exists(dest_path):
            return name

def get_github_username(pat):
    url = "https://api.github.com/user"
    headers = {
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Sonar-CLI-Agent"
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode())
            return res_data.get("login", "unknown")
    except Exception:
        return "unknown"

def create_and_push_github(local_path, project_name, pat):
    print(f"[*] Initiating GitHub push flow for {project_name}...")
    
    # 1. Create repository via REST API
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
        "User-Agent": "Sonar-CLI-Agent"
    }
    data = json.dumps({
        "name": project_name,
        "private": True,
        "description": "Unique restructured codebase generated by Sonar"
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode())
            html_url = res_data.get("html_url")
            print(f"[+] Private GitHub repository created successfully: {html_url}")
    except Exception as e:
        print(f"[-] Failed to create repository: {e}")
        return None

    # 2. Push repository
    parsed = urllib.parse.urlparse(html_url)
    auth_url = f"https://{pat}@{parsed.netloc}{parsed.path}"
    
    try:
        # Remove old remote and configure authenticated remote
        subprocess.run(["git", "remote", "remove", "origin"], cwd=local_path, capture_output=True)
        subprocess.run(["git", "remote", "add", "origin", auth_url], cwd=local_path, capture_output=True)
        subprocess.run(["git", "branch", "-M", "master"], cwd=local_path, capture_output=True)
        
        # Strip parent Git env variables to prevent contamination
        env = os.environ.copy()
        for key in list(env.keys()):
            if key.upper().startswith("GIT_"):
                del env[key]
                
        print("[*] Pushing commits to private remote...")
        res = subprocess.run(["git", "push", "-u", "origin", "master"], cwd=local_path, env=env, capture_output=True, text=True)
        if res.returncode == 0:
            print("[+] Push completed successfully!")
            return html_url
        else:
            print(f"[-] Push failed: {res.stderr.strip()}")
            return None
    except Exception as e:
        print(f"[-] Push error: {e}")
        return None

def submit_sync_issue(pat, codeberg_url, project_name, pushed_url, username):
    print("[*] Submitting database update via GitHub Issue...")
    url = "https://api.github.com/repos/dchumari/sonar/issues"
    headers = {
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
        "User-Agent": "Sonar-CLI-Agent"
    }
    
    payload = {
        "title": f"DB Update: {project_name}",
        "labels": ["db-update"],
        "body": json.dumps({
            "codeberg_url": codeberg_url,
            "restructured_name": project_name,
            "pushed_github_url": pushed_url,
            "status": "pushed" if pushed_url else "processed",
            "processed_by": username,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        }, indent=4)
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 201:
                print("[+] Sync issue submitted. Central database will update momentarily!")
            else:
                print(f"[!] Warning: Issue creation returned status {response.status}")
    except Exception as e:
        print(f"[-] Failed to submit sync issue: {e}")

def sanitize_and_rewrite_readmes(dest_dir, project_name):
    print("[*] Sanitizing and rewriting README documentation...")
    if not os.path.exists(dest_dir):
        return
        
    for item in os.listdir(dest_dir):
        if item.upper().startswith("README"):
            file_path = os.path.join(dest_dir, item)
            if not os.path.isfile(file_path):
                continue
                
            ext = os.path.splitext(item)[1].lower()
            
            # Write generic template according to format
            if ext in (".md", ".markdown"):
                content = f"""# {project_name}

Welcome to {project_name}. This repository contains a restructured and optimized codebase.

## Overview
This project has been restructured for deployment and development.

## Setup & Usage
Please check the build configurations (e.g., package files, build scripts, or meson configuration) in the root of the repository for setup instructions.
"""
            elif ext in (".adoc", ".asciidoc"):
                content = f"""= {project_name}

Welcome to {project_name}. This repository contains a restructured and optimized codebase.

== Overview
This project has been restructured for deployment and development.

== Setup & Usage
Please check the build configurations (e.g., package files, build scripts, or meson configuration) in the root of the repository for setup instructions.
"""
            else:
                # Text/Default template
                content = f"""=== {project_name} ===

Welcome to {project_name}. This repository contains a restructured and optimized codebase.

-- Overview --
This project has been restructured for deployment and development.

-- Setup & Usage --
Please check the build configurations (e.g., package files, build scripts, or meson configuration) in the root of the repository for setup instructions.
"""
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"[+] Successfully sanitized and rewrote README: {item}")
            except Exception as e:
                print(f"[!] Warning: Failed to rewrite README {item}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Sonar Unified Restructuring CLI Orchestrator")
    parser.add_argument("--src", required=True, help="Path to source codebase to restructure")
    parser.add_argument("--dest-parent", help="Parent directory where uniquely named outputs will be saved")
    parser.add_argument("--config", help="Path to restructuring JSON configuration")
    args = parser.parse_args()

    # 1. Sync database and load local settings
    auto_pull_db()
    creds = load_credentials()
    db = load_db()
    
    # 2. Check for duplicate repository in DB
    source_git_url = ""
    # Attempt to extract repo remote URL from source repo if it is a Git folder
    if os.path.exists(os.path.join(args.src, ".git")):
        try:
            res = subprocess.run(["git", "config", "--get", "remote.origin.url"], cwd=args.src, capture_output=True, text=True)
            if res.returncode == 0:
                source_git_url = res.stdout.strip()
        except Exception:
            pass

    # Normalize url check
    check_url = source_git_url or args.src
    print(f"[*] Checking DB for repository identifier: {check_url}")
    for entry in db:
        if entry.get("codeberg_url") == check_url:
            print(f"[-] Cancelled: Repository '{check_url}' has already been processed as '{entry.get('restructured_name')}' and pushed to {entry.get('pushed_github_url')}.")
            sys.exit(0)

    # 3. Resolve destination name & parent dir
    dest_parent = args.dest_parent or creds.get("dest_parent")
    project_name = generate_unique_name(db, dest_parent)
    dest_dir = os.path.join(dest_parent, project_name)
    
    print(f"[+] Unique name selected: {project_name}")
    print(f"[*] Target destination: {dest_dir}")
    
    # 4. Resolve config file
    config_file = args.config or DEFAULT_CONFIG_TEMPLATE
    if not os.path.exists(config_file):
        print(f"[-] Error: Configuration template {config_file} not found.")
        sys.exit(1)
        
    # Dynamically inject credentials into temporary config block or use script parameters
    # The restructuring script expects configuration parameters
    print("[*] Running restructuring process...")
    restructure_script = os.path.join(os.path.dirname(__file__), ".agents", "skills", "codebase-restructurer", "scripts", "restructure_project.py")
    
    # Construct subprocess call
    cmd = [
        sys.executable,
        restructure_script,
        "--src", args.src,
        "--dest", dest_dir,
        "--config", config_file
    ]
    
    res = subprocess.run(cmd)
    if res.returncode != 0:
        print("[-] Restructuring failed. Halting pipeline.")
        sys.exit(res.returncode)

    # 4.5 Sanitize and rewrite README documents
    sanitize_and_rewrite_readmes(dest_dir, project_name)

    # 5. Ask to push to private GitHub repo
    push_pat = creds.get("github_push_pat") or creds.get("github_pat")
    sync_pat = creds.get("github_sync_pat") or creds.get("github_pat")
    
    username = get_github_username(push_pat)
    pushed_url = None
    
    push_choice = input(f"\nDo you want to push '{project_name}' to a private GitHub repo? (y/n) [default: y]: ").strip().lower()
    if push_choice in ("y", "yes", ""):
        pushed_url = create_and_push_github(dest_dir, project_name, push_pat)
        if not pushed_url:
            print("[!] Warning: Repository could not be pushed to GitHub.")
    
    # 6. Submit issue update to synchronize the database
    submit_sync_issue(
        pat=sync_pat,
        codeberg_url=check_url,
        project_name=project_name,
        pushed_url=pushed_url,
        username=username
    )

if __name__ == "__main__":
    main()
