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
- **README Untraceability**: Always completely rewrite README documentation files (e.g. `README.md`, `README.adoc`, `README.txt`, `README`) in the restructured destination folder with a clean, neutral template referencing only the new project name, and completely stripping original author/repo links to ensure maximum privacy and untraceability. When executing or preparing a repository in the chat session, the AI assistant must manually overwrite these files with a high-quality, customized, and unique description of the project features/build process to avoid generic duplication across multiple repositories.
- **ZIP Packaging**: Always automatically bundle the restructured target folder into a `.zip` archive alongside the output folder. Ensure that the generated `.git` repository folder is fully preserved inside the archive to allow manual pushes/restorations.




