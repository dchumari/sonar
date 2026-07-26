# Sonar: Codebase Restructuring & Anonymization Pipeline

Sonar is a pipeline tool designed to import source codebases, flatten and anonymize their structure, clean hardcoded credentials, synthesize git histories with randomized timelines, rewrite untraceable documentation, and package/sync them to private repositories.

## Features

- **Structural Restructuring**: Deconstructs and flattens directory configurations to obscure original project hierarchies.
- **Anonymization & Hardcoded Secret Stripping**: Automatically scans for and strips potential API keys, passwords, and sensitive configurations from source code.
- **Synthetic Git History Generation**: Creates a realistic, fake git history with randomized commit timelines (spanning 3-6 years) and custom author designations to eliminate tracing back to the original source repository.
- **README Untraceability**: Sanitizes and rewrites project documentation, replacing it with unique, custom project descriptions containing no external links or original context.
- **ZIP Packaging**: Packages the fully restructured repository—including its `.git` folder—into a compressed `.zip` archive for easy distribution.
- **GitHub Sync Flow**: Automates private repository creation, pushes the restructured codebase, and submits database updates to synchronize the central registry.

---

## Project Structure

```
├── .agents/                    # Workspace configuration & customizations
│   └── skills/                 # Restructuring skills & helper scripts
│       └── codebase-restructurer/
│           ├── examples/       # Config templates
│           └── scripts/        # Restructurer core scripts (git generator, etc.)
├── db/                         # Database storage
│   └── processed_repos.json    # Sync log of all processed source repositories
├── scratch/                    # Default output parent folder (gitignored)
├── sonar.py                    # Main orchestrator CLI script
└── README.md                   # Project documentation
```

---

## Setup & Installation

### Prerequisites

- Python 3.8+
- Git CLI (configured and authenticated on the host)

### 1. Configuration & Credentials

On its first execution, Sonar will prompt you to set up your configuration. Alternatively, you can pre-configure the credentials file manually.

Create a file named `.sonar_credentials.json` (which is gitignored) in the root of the project:

```json
{
    "github_push_pat": "ghp_yourPushTokenHere",
    "github_sync_pat": "ghp_yourSyncTokenHere",
    "author_name": "Marc Barber",
    "author_email": "marcbarber@cc.cc",
    "dest_parent": "d:\\Projects\\AUTOMATIONS\\AFTERQUERY\\Sonar\\scratch"
}
```

* **github_push_pat**: The Personal Access Token (PAT) used to push prepared repositories to your private GitHub organization/account.
* **github_sync_pat**: The PAT used to authenticate database synchronization with the orchestrator repository (requires issue write access).
* **author_name & author_email**: The default git identity details used to author commits in the synthetic git history.

---

## Usage

### Restructuring a Single Codebase

Run the orchestrator command by pointing it to the path of your source repository:

```bash
python sonar.py --src "/path/to/source/repo" --name "UniqueProjectName"
```

#### Command Line Arguments:

- `--src` (Required): Path to the source directory to restructure.
- `--dest-parent` (Optional): Directory where the output folder and ZIP file will be saved. Defaults to the configured `scratch` folder.
- `--config` (Optional): Path to a custom restructuring JSON configuration. Defaults to the template config.
- `--name` (Optional): Force a specific unique name for the restructured codebase. If omitted, a name will be dynamically generated.

### Batch Execution

To process multiple repositories at once, you can run batch scripts located in the `scratch/` directory:

- **Search & Download**: `python scratch/search_codeberg.py` - Scans Codeberg for target Python codebases based on LOC limits, size, and commit counts.
- **Batch Pipeline**: `python scratch/prepare_largest_batch.py` - Sequences clones and runs the Sonar restructuring and push pipeline for batch results.

---

## Guidelines & Best Practices

1. **Git Preservation**: Ensure you retain the generated `.git` folder when moving or extracting the output ZIP archive to permit subsequent commits and pushes.
2. **README Verification**: Always review and update the README of newly generated codebases manually in chat sessions to avoid duplicate generic project templates.
