import os
import subprocess
import random
from datetime import datetime, timedelta

def run_git_cmd(args, cwd, env=None):
    """Executes a git command synchronously, cleaning parent git environment pollution."""
    clean_env = os.environ.copy()
    for key in list(clean_env.keys()):
        upper_key = key.upper()
        if upper_key.startswith("GIT_") and not upper_key.startswith("GIT_AUTHOR_") and not upper_key.startswith("GIT_COMMITTER_"):
            del clean_env[key]
    
    if env:
        clean_env.update(env)

    result = subprocess.run(["git"] + args, cwd=cwd, env=clean_env, capture_output=True, text=True)
    print(f"[Git Debug] cmd: git {' '.join(args)} | code: {result.returncode} | out: {result.stdout.strip()} | err: {result.stderr.strip()}")
    if result.returncode != 0:
        raise Exception(f"Git command failed: {' '.join(args)}\nError: {result.stderr}")
    return result.stdout

def generate_synthetic_git_history(target_dir, start_date_str, end_date_str, authors, commit_freq_days=2.5):
    """
    Builds a synthetic git repository with stochastically distributed commits
    over a designated timeline, complete with random developer profiles.
    """
    start_date = datetime.fromisoformat(start_date_str.replace("Z", "+00:00"))
    end_date = datetime.fromisoformat(end_date_str.replace("Z", "+00:00"))

    # Remove stale index.lock if present from a crashed run
    lock_file = os.path.join(target_dir, ".git", "index.lock")
    if os.path.exists(lock_file):
        try:
            os.remove(lock_file)
            print("[*] Removed stale index.lock file.")
        except Exception as e:
            print(f"[!] Warning: Could not remove stale index.lock: {e}")

    # Initialize a new git repository (running unconditionally is safe and repairs corrupt repos)
    run_git_cmd(["init"], cwd=target_dir)
    
    # Configure safety parameters
    run_git_cmd(["config", "user.name", "System Restructurer"], cwd=target_dir)
    run_git_cmd(["config", "user.email", "restructurer@sonar.internal"], cwd=target_dir)

    # Gather all file paths in target directory
    file_list = []
    for root, dirs, files in os.walk(target_dir):
        # Skip git metadata
        if ".git" in root.split(os.sep):
            continue
        for file in files:
            file_list.append(os.path.relpath(os.path.join(root, file), target_dir))

    if not file_list:
        print("No files found to commit.")
        return

    # Sort files to stage them in groups (initial setup -> features -> polish)
    file_list.sort()
    
    current_date = start_date
    commit_templates = [
        "feat({scope}): implement initial core structure",
        "refactor({scope}): optimize execution and control flow",
        "docs({scope}): clean layout structure and definitions",
        "fix({scope}): resolve initialization exceptions",
        "perf({scope}): reduce computation overhead",
        "style({scope}): format logic blocks and declarations"
    ]

    # Staging batches
    chunk_size = max(1, len(file_list) // 10)
    batches = [file_list[i:i + chunk_size] for i in range(0, len(file_list), chunk_size)]

    for idx, batch in enumerate(batches):
        if current_date >= end_date:
            break

        # Stage files in this batch all at once to avoid index.lock issues
        if batch:
            run_git_cmd(["add"] + batch, cwd=target_dir)

        # Select a random author based on weights
        author = random.choices(
            authors, 
            weights=[a.get("weight", 1.0) for a in authors], 
            k=1
        )[0]

        # Pick semantic template
        scope = "core"
        if batch:
            scope = os.path.splitext(os.path.basename(batch[0]))[0][:10]
        
        msg = random.choice(commit_templates).format(scope=scope)

        # Apply stochastic burstiness: randomize commits within office hours (9am to 6pm)
        # Avoid weekends
        while current_date.weekday() >= 5:
            current_date += timedelta(days=1)

        commit_hour = random.randint(9, 17)
        commit_minute = random.randint(0, 59)
        commit_second = random.randint(0, 59)
        current_date = current_date.replace(hour=commit_hour, minute=commit_minute, second=commit_second)

        # Create the commit with explicit timestamps
        date_str = current_date.isoformat()
        
        env = os.environ.copy()
        env["GIT_AUTHOR_NAME"] = author["name"]
        env["GIT_AUTHOR_EMAIL"] = author["email"]
        env["GIT_AUTHOR_DATE"] = date_str
        env["GIT_COMMITTER_NAME"] = author["name"]
        env["GIT_COMMITTER_EMAIL"] = author["email"]
        env["GIT_COMMITTER_DATE"] = date_str

        # Commit subprocess invocation using custom env
        run_git_cmd(["commit", "-m", msg], cwd=target_dir, env=env)

        # Increment date
        days_to_add = random.uniform(commit_freq_days * 0.5, commit_freq_days * 1.5)
        current_date += timedelta(days=days_to_add)

    print(f"Synthesized history from {start_date_str} to {current_date.isoformat()}")
