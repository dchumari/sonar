# codebase-restructurer

A local CLI framework to automate the restructuring of repositories to bypass textual (winnowing), AST/control-flow, and Git history plagiarism detection metrics.

## Installation & Setup

1. Ensure Python 3.8+ is installed on your machine.
2. Install optional requirements (e.g., `gitpython` for advanced git operations, though standard `subprocess` is used as a fallback):
   ```bash
   pip install gitpython
   ```

## Configuration

Copy the example configuration to your target folder:
```json
{
  "target_languages": ["python", "javascript"],
  "transformations": {
    "control_flow_mutation": true,
    "structural_refactoring": true,
    "dummy_code_insertion": true,
    "control_flow_flattening": true,
    "semantic_renaming": true,
    "comment_sanitization": true,
    "identifier_renaming": true
  },
  "exclusions": ["node_modules", "venv", ".venv", "dist", "build", ".git"],
  "git_history": {
    "start_date": "2021-01-01T09:00:00Z",
    "end_date": "2026-07-23T10:00:00Z",
    "commit_frequency_days": 2.5,
    "authors": [
      {
        "name": "Alice Developer",
        "email": "alice@dev-hub.net",
        "weight": 0.7
      }
    ]
  }
}
```

## Running the tool

Execute the orchestrator:
```bash
python scripts/restructure_project.py --src /path/to/source/repo --dest /path/to/destination/repo --config /path/to/config.json
```

## Sonar Orchestration Pipeline

The orchestrator `sonar.py` wraps the codebase restructurer to automate credential configuration, repository renaming, deployment, and centralized status tracking.

### Operational Workflow

1. **Auto-Pull Database Sync**:
   On launch, the tool pulls the latest commits from the master branch to synchronize the processed repositories log `db/processed_repos.json`.
2. **Interactive First-Time Setup**:
   Prompts for:
   - GitHub Personal Access Token (PAT).
   - Git author details (name and email).
   - Destination parent path for restructured outputs.
   Saved locally to the gitignored `.sonar_credentials.json`.
3. **Collision-Free Renaming**:
   Generates a random two-word identity (e.g., `AzureSpire`) and verifies it does not exist in `db/processed_repos.json` or local folders.
4. **Restructuring Execution**:
   Spawns `restructure_project.py` with custom flags and templates.
5. **Private Repo Push**:
   Utilizes the GitHub API to create a private repository named after the generated project and pushes the mutated master branch.
6. **Decentralized DB Synchronization**:
   Uses the GitHub Issues API to submit a JSON payload as an issue with the label `db-update`. A GitHub Actions workflow (`sync_db.yml`) detects it, parses the payload, updates `db/processed_repos.json`, commits it back to the codebase, and closes the issue.

