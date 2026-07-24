import os
import shutil
import json
import argparse
import ast
import re

from ast_transformer import ASTTransformer, sanitize_regex_comments, rename_semantic_identifiers
from git_generator import generate_synthetic_git_history

import stat

def handle_remove_readonly(func, path, exc_info):
    """Clears the read-only bit and retries file removal on Windows."""
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        pass

def copy_and_sanitize_tree(src, dest, exclusions):
    """Copies all source files to dest, skipping exclusions."""
    if os.path.exists(dest):
        shutil.rmtree(dest, onerror=handle_remove_readonly)
    os.makedirs(dest, exist_ok=True)

    for root, dirs, files in os.walk(src):
        # Filter directories in-place
        dirs[:] = [d for d in dirs if d not in exclusions and not d.startswith('.')]
        
        rel_path = os.path.relpath(root, src)
        dest_dir = os.path.join(dest, rel_path) if rel_path != '.' else dest
        
        os.makedirs(dest_dir, exist_ok=True)

        for file in files:
            if file in exclusions or file.startswith('.'):
                continue
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_dir, file)
            shutil.copy2(src_file, dest_file)

def anonymize_document(file_path):
    """Paraphrases content, strips external hyperlinks and metadata."""
    if not os.path.exists(file_path):
        return
    
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Strip external URLs/links but keep text
    content = re.sub(r'\[([^\]]+)\]\((https?://\S+)\)', r'\1', content)
    content = re.sub(r'https?://\S+', ' [Link Removed] ', content)
    
    # Simple semantic replacement of specific terms
    content = re.sub(r'(?i)afterquery', 'SonarRestructuredSystem', content)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def transform_python_file(file_path, flatten_all):
    """Parses Python code, modifies AST, compiles to verify syntax, writes back."""
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        parsed = ast.parse(source)
        transformer = ASTTransformer(flatten_all=flatten_all)
        transformed = transformer.visit(parsed)
        ast.fix_missing_locations(transformed)
        
        # Verify compilation correctness
        new_source = ast.unparse(transformed)
        compile(new_source, file_path, "exec")
        
        # Write back transformed code
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_source)
    except Exception as e:
        print(f"Skipping AST transformation for {file_path} due to error: {e}")

def check_qualification(src_dir, config):
    """
    Checks if the codebase qualifies based on LOC, commit count, and scans for secrets.
    """
    qual_config = config.get("qualification", {})
    min_loc = qual_config.get("min_loc", 10000)
    min_commits = qual_config.get("min_commits", 100)

    # 1. Check original commit count
    commit_count = 0
    if os.path.exists(os.path.join(src_dir, ".git")):
        try:
            import subprocess
            res = subprocess.run(
                ["git", "rev-list", "--count", "HEAD"], 
                cwd=src_dir, 
                capture_output=True, 
                text=True
            )
            if res.returncode == 0:
                commit_count = int(res.stdout.strip())
        except Exception:
            pass

    if commit_count < min_commits:
        print(f"[-] Rejected: Repository does not qualify. Original commits ({commit_count}) < required ({min_commits})")
        return False

    # 2. Check Lines of Code (LOC)
    total_loc = 0
    exclusions = config.get("exclusions", [])
    for root, dirs, files in os.walk(src_dir):
        dirs[:] = [d for d in dirs if d not in exclusions and not d.startswith('.')]
        for file in files:
            if file in exclusions or file.startswith('.'):
                continue
            # Scan only textual code files
            if file.endswith((".py", ".js", ".ts", ".go", ".cpp", ".h", ".java")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        total_loc += sum(1 for line in f if line.strip())
                except Exception:
                    pass

    if total_loc < min_loc:
        print(f"[-] Rejected: Repository does not qualify. Authored LOC ({total_loc}) < required ({min_loc})")
        return False

    print(f"[+] Repository qualified with {total_loc} LOC and {commit_count} commits.")
    return True

def auto_strip_secrets(content):
    """Scans and auto-strips credentials, replacing them with generic placeholders."""
    secret_patterns = [
        (r'(?i)api_key\s*=\s*["\'][a-zA-Z0-9_\-]{16,}["\']', 'api_key = "SANITIZED_GENERIC_KEY"'),
        (r'(?i)password\s*=\s*["\'][^"\']{6,}["\']', 'password = "SANITIZED_PASSWORD"'),
        (r'(?i)token\s*=\s*["\'][a-zA-Z0-9_\-\.]{16,}["\']', 'token = "SANITIZED_TOKEN"'),
        (r'(?i)client_secret\s*=\s*["\'][a-zA-Z0-9_\-]{16,}["\']', 'client_secret = "SANITIZED_CLIENT_SECRET"')
    ]
    modified = False
    for pattern, replacement in secret_patterns:
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            content = new_content
            modified = True
    return content, modified

def main():
    parser = argparse.ArgumentParser(description="Sonar Unique Codebase Restructuring CLI Tool")
    parser.add_argument("--src", required=True, help="Source repository path")
    parser.add_argument("--dest", required=True, help="Destination directory path")
    parser.add_argument("--config", required=True, help="JSON configuration filepath")
    args = parser.parse_args()

    # Load configuration
    with open(args.config, "r") as f:
        config = json.load(f)

    # Perform pre-qualification checks
    if not check_qualification(args.src, config):
        sys.exit(1)

    exclusions = config.get("exclusions", [])
    transformations = config.get("transformations", {})
    git_history_config = config.get("git_history", {})

    print(f"[*] Copying files to clean working destination: {args.dest}")
    copy_and_sanitize_tree(args.src, args.dest, exclusions)

    # Process all files recursively
    for root, dirs, files in os.walk(args.dest):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Anonymize and clean documents/READMEs
            if file.lower().endswith((".md", ".txt", ".json", ".xml", ".html")):
                anonymize_document(file_path)
                continue

            # Process code source files
            if file.endswith(".py"):
                if transformations.get("control_flow_flattening", False):
                    transform_python_file(file_path, flatten_all=True)

             # Apply regex comment sanitization & identifier renaming
            if file.endswith((".py", ".js", ".ts", ".go", ".cpp", ".h")):
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                
                if config.get("qualification", {}).get("scan_secrets", True):
                    content, stripped = auto_strip_secrets(content)
                    if stripped:
                        print(f"[!] Warning: Hardcoded secrets detected and stripped in {file_path}")

                if transformations.get("comment_sanitization", False):
                    content = sanitize_regex_comments(content)
                
                if transformations.get("identifier_renaming", False):
                    content = rename_semantic_identifiers(content)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)

    print("[*] Generating synthetic git history...")
    generate_synthetic_git_history(
        target_dir=args.dest,
        start_date_str=git_history_config.get("start_date", "2021-01-01T09:00:00Z"),
        end_date_str=git_history_config.get("end_date", "2026-07-23T10:00:00Z"),
        authors=git_history_config.get("authors", []),
        commit_freq_days=git_history_config.get("commit_frequency_days", 2.5),
        target_commits=git_history_config.get("target_commits", 100)
    )
    git_dir_path = os.path.join(args.dest, ".git")
    print(f"[*] Debug - Does .git exist at {git_dir_path}? {os.path.exists(git_dir_path)}")
    print("[+] Codebase restructuring completed successfully!")

if __name__ == "__main__":
    main()
