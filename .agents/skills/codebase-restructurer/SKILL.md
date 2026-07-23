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
