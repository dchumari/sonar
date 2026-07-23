# Repository Restructuring Guidelines

When modifying or maintaining the restructuring CLI framework, ensure all components adhere to the following principles:

## Code Correctness & Safety
- **Tiered Verification**: Never commit changes to any target codebase without verifying syntax compilation.
- **Strict Exclusions**: Never process vendor folders (`node_modules`, `.venv`), build outputs (`dist`, `build`), or active git configurations (`.git`).
- **Readability vs. Uniqueness**: When applying global control flow flattening, preserve logic functionality by verifying execution graphs against expected inputs.

## Token Efficiency
- Keep the python scripts modular and self-contained so that execution on local targets requires no communication or API calls back to the LLM.

## Sonar CLI & Wrapper Guidelines

- **Orchestration Separation**: Maintain a strict separation between the orchestrator (`sonar.py`) and the restructurer scripts. Do not introduce credentials, API requests, or networking code into the `scripts/restructure_project.py` files.
- **Git Safety**: Never push credentials to any repository. Ensure `.sonar_credentials.json` remains strictly gitignored.
- **Database Consistency**: Any modification to `db/processed_repos.json` or sync logic must preserve compatibility with the GitHub Action workflow (`.github/workflows/sync_db.yml`).

