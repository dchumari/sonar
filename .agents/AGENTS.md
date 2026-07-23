# Repository Restructuring Guidelines

When modifying or maintaining the restructuring CLI framework, ensure all components adhere to the following principles:

## Code Correctness & Safety
- **Tiered Verification**: Never commit changes to any target codebase without verifying syntax compilation.
- **Strict Exclusions**: Never process vendor folders (`node_modules`, `.venv`), build outputs (`dist`, `build`), or active git configurations (`.git`).
- **Readability vs. Uniqueness**: When applying global control flow flattening, preserve logic functionality by verifying execution graphs against expected inputs.

## Token Efficiency
- Keep the python scripts modular and self-contained so that execution on local targets requires no communication or API calls back to the LLM.
