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

---

## Prepared Repositories Registry

<!-- START_PREPARED_REPOS_TABLE -->

| Original Repository Name | Unique Destination Name | Status | Size (MB) | Commits (Orig / Target) | Description | GitHub Target Repo |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| [ansible](https://codeberg.org/asaramet/ansible.git) | **DeployAutomation** | `pushed` | 102.2 | 62 / 190 | An automated server provisioning and application deployment orchestrator based on Ansible playboo... | [DeployAutomation](https://github.com/starnbluey-cell/DeployAutomation) |
| [PyPSA](https://codeberg.org/neunzehnachtneun/PyPSA.git) | **GridEnergy** | `pushed` | 29.2 | 62 / 716 | A power systems optimization framework and transmission network simulation engine. Designed to mo... | [GridEnergy](https://github.com/starnbluey-cell/GridEnergy) |
| [stack-harness](https://codeberg.org/myoungjin/stack-harness.git) | **HarnessStack** | `pushed` | 13.4 | 62 / 1031 | An automated testing harness and deployment orchestration pipeline for enterprise application sta... | [HarnessStack](https://github.com/starnbluey-cell/HarnessStack) |
| [karrot-backend](https://codeberg.org/karrot/karrot-backend.git) | **KarrotCore** | `pushed` | 11.7 | 62 / 1002 | The backend API platform for Karrot, a community sharing, food saving, and collective organizatio... | [KarrotCore](https://github.com/starnbluey-cell/KarrotCore) |
| [crochess](https://codeberg.org/mmlacak/crochess.git) | **TacticalChess** | `pushed` | 96.9 | 62 / 242 | A chess game engine, evaluation simulator, and graphical board analyzer. Features search optimiza... | [TacticalChess](https://github.com/starnbluey-cell/TacticalChess) |
| [mcp-memory-service](https://codeberg.org/doobidoo/mcp-memory-service.git) | **CogniMem** | `pushed` | 61.7 | 62 / 1161 | A Model Context Protocol (MCP) semantic memory service. Features automatic memory consolidation p... | [CogniMem](https://github.com/starnbluey-cell/CogniMem) |
| [AudioMuse-AI](https://codeberg.org/NeptuneHub/AudioMuse-AI.git) | **AudioMuse** | `pushed` | 69.8 | 62 / 525 | An AI-assisted audio production suite and generative music arranger. Integrates acoustic analysis... | [AudioMuse](https://github.com/starnbluey-cell/AudioMuse) |
| [PhoenixAdult](https://codeberg.org/PhoenixAdultProvider/PhoenixAdult.git) | **PhoenixPortal** | `pushed` | 4.5 | 62 / 434 | A comprehensive community portal and booking platform for independent adult service providers. Fe... | [PhoenixPortal](https://github.com/starnbluey-cell/PhoenixPortal) |
| [FoxDot-ce](https://codeberg.org/FoxDot-community/FoxDot-ce.git) | **SonicSynth** | `pushed` | 172.4 | 62 / 119 | A Python live coding engine and synthetic music performance environment. Integrates connection pi... | [SonicSynth](https://github.com/starnbluey-cell/SonicSynth) |
| [LSaO-visualizer](https://codeberg.org/aaronfbianchi/LSaO-visualizer.git) | **SpaceVisualizer** | `pushed` | 128.1 | 62 / 59 | An interactive visualizer and analytical toolkit for Low-frequency Solar Acoustic Oscillations (L... | [SpaceVisualizer](https://github.com/starnbluey-cell/SpaceVisualizer) |
| [created_with_eee](https://codeberg.org/EEE-project/created_with_eee.git) | **AuraCanvas** | `pushed` | 51.6 | 115 / 112 | A digital humanities workspace and rendering engine for analyzing ancient texts and visual resour... | [AuraCanvas](https://github.com/starnbluey-cell/AuraCanvas) |
| [pypsmcbor](https://codeberg.org/PAPPSO/pypsmcbor.git) | **ProteoMetric** | `pushed` | 81.0 | 261 / 72 | A specialized data parser and validator for high-resolution mass spectrometry and proteomics metr... | [ProteoMetric](https://github.com/starnbluey-cell/ProteoMetric) |
| [nge_2_re](https://codeberg.org/EVA-zh-Hans/nge_2_re.git) | **VividEngine** | `pushed` | 79.3 | 555 / 108 | A toolkit and GUI workflow client designed to parse, patch, and extract translation assets from g... | [VividEngine](https://github.com/starnbluey-cell/VividEngine) |
| [PySIDM](https://codeberg.org/RotemBarnea/PySIDM.git) | **MatterGravity** | `pushed` | 589.1 | 1493 / 122 | A scientific simulation package designed to model Self-Interacting Dark Matter (SIDM) and gravoth... | [MatterGravity](https://github.com/starnbluey-cell/MatterGravity) |
| [fayf_processor](https://codeberg.org/pluggpreagar/fayf_processor.git) | **DataWeave** | `pushed` | 9.4 | 603 / 114 | A modular pipeline processor for parsing, transformation, and stream compilation of large dataset... | [DataWeave](https://github.com/starnbluey-cell/DataWeave) |
| [ss](https://codeberg.org/angelogreco/ss.git) | **TunnelFlow** | `pushed` | 101.4 | 1395 / 128 | A secure network tunneling daemon and traffic proxy optimizer. Supports multiple traffic obfuscat... | [TunnelFlow](https://github.com/starnbluey-cell/TunnelFlow) |
| [seedsigner](https://codeberg.org/kdmukAI-bot/seedsigner.git) | **ColdSigner** | `pushed` | 133.4 | 2237 / 110 | An offline secure transaction signer designed to run in air-gapped environments. Offers support f... | [ColdSigner](https://github.com/starnbluey-cell/ColdSigner) |
| [Quant-Nanggroe-AI](https://codeberg.org/Dhaher-Labs/Quant-Nanggroe-AI.git) | **TradeCalculus** | `pushed` | 93.1 | 237 / 104 | An advanced quantitative trading and backtesting engine for multi-asset portfolios. Supports cryp... | [TradeCalculus](https://github.com/starnbluey-cell/TradeCalculus) |
| [cognee](https://codeberg.org/nopejs/cognee.git) | **SemanticMind** | `pushed` | 275.5 | 8909 / 104 | A semantic memory orchestration engine and lightweight graph database handler. Integrates with ve... | [SemanticMind](https://github.com/starnbluey-cell/SemanticMind) |
| [smol-k8s-lab](https://codeberg.org/open-engineering/smol-k8s-lab.git) | **NanoCluster** | `pushed` | 170.6 | 1386 / 120 | A terminal-based playground and laboratory environment for lightweight Kubernetes distributions (... | [NanoCluster](https://github.com/starnbluey-cell/NanoCluster) |
| [gpt4free](https://codeberg.org/gpt4free-mirror/gpt4free.git) | **FreeAiGateway** | `pushed` | 1.9 | 100 / 114 | A lightweight client API gateway designed to unify, manage, and proxy free access to multiple Lar... | [FreeAiGateway](https://github.com/starnbluey-cell/FreeAiGateway) |
| [gallery-dl](https://codeberg.org/mikf/gallery-dl.git) | **MediaGrabber** | `pushed` | 2.6 | 100 / 102 | A powerful, extensible command-line media downloader designed to extract and organize image galle... | [MediaGrabber](https://github.com/starnbluey-cell/MediaGrabber) |
| [RAT](https://codeberg.org/RandoOne/RAT.git) | **RatAdmin** | `pushed` | 6.8 | 100 / 107 | An automated download manager, content archiver, and synchronization suite designed for forum-bas... | [RatAdmin](https://github.com/starnbluey-cell/RatAdmin) |
| [endurain](https://codeberg.org/endurain-project/endurain.git) | **EnduranceTrack** | `pushed` | 47.6 | 100 / 105 | A self-hosted, privacy-focused fitness analytics platform and multi-sport activity tracker. | [EnduranceTrack](https://github.com/starnbluey-cell/EnduranceTrack) |
| [origin-axiom](https://codeberg.org/originaxiom/origin-axiom.git) | **AxiomEngine** | `pushed` | 57.4 | 100 / 102 | A modern Python library for algebraic topology, computational geometry, and mobius transformations. | [AxiomEngine](https://github.com/starnbluey-cell/AxiomEngine) |
| [gradlew.py](https://codeberg.org/IzzyOnDroid/gradlew.py.git) | **SilentDrift** | `processed` | 0.4 | 109 / 100 | Restructured python codebase | N/A |
| [scriptura](https://codeberg.org/andresmessina/scriptura.git) | **NebulaRift** | `pushed` | 44.4 | 406 / 118 | NebulaRift is a Python-based textual catalog and Bible rendering system designed to parse, refere... | [NebulaRift](https://github.com/starnbluey-cell/NebulaRift) |
| [LotansTomb](https://codeberg.org/mc776/LotansTomb) | **NebulaCrypt** | `pushed` | 80.3 | 1287 / 103 | Restructured python codebase | [NebulaCrypt](https://github.com/starnbluey-cell/NebulaCrypt) |
| [yadgar](https://codeberg.org/maxagahi/yadgar.git) | **AzureHorizon** | `pushed` | 53.3 | 1476 / 104 | AzureHorizon is a python library and parsing framework designed for multi-calendar calculations, ... | [AzureHorizon](https://github.com/starnbluey-cell/AzureHorizon) |
| [rope-language-server](https://codeberg.org/mcepl/rope-language-server.git) | **StormSummit** | `pushed` | 2.2 | 651 / 87 | StormSummit is a Python language server protocol (LSP) implementation focusing exclusively on aut... | [StormSummit](https://github.com/starnbluey-cell/StormSummit) |
| [Ralph-Workflow](https://codeberg.org/RalphWorkflow/Ralph-Workflow.git) | **SolarRift** | `pushed` | 84.8 | 4634 / 104 | SolarRift is a Python-based scriptable workflow orchestration engine and asset lifecycle manager.... | [SolarRift](https://github.com/starnbluey-cell/SolarRift) |
| [opendesk-edu](https://codeberg.org/opendesk-edu/opendesk-edu.git) | **EchoSaber** | `pushed` | 62.5 | 2335 / 102 | EchoSaber is a cloud deployment and orchestration framework designed for secure, sovereign educat... | [EchoSaber](https://github.com/starnbluey-cell/EchoSaber) |
| [matridge](https://codeberg.org/slidge/matridge.git) | **QuantumCanyon** | `pushed` | 2.8 | 381 / 46 | QuantumCanyon is an asynchronous, modular chat bridge and gateway engine written in Python. It en... | [QuantumCanyon](https://github.com/starnbluey-cell/QuantumCanyon) |
| [home-assistant-chart](https://codeberg.org/open-engineering/home-assistant-chart.git) | **SilentRift** | `processed` | 0.6 | 425 / 100 | Restructured python codebase | N/A |
| [siun](https://codeberg.org/lokimotive/siun.git) | **QuantumHaven** | `pushed` | 7.4 | 140 / 61 | QuantumHaven is a scriptable, CLI-based system update notifier and package manager assistant desi... | [QuantumHaven](https://github.com/starnbluey-cell/QuantumHaven) |
| [torii-hdl](https://codeberg.org/shrine-maiden-heavy-industries/torii-hdl.git) | **SpectralSaber** | `pushed` | 7.5 | 2767 / 138 | SpectralSaber is an open-source, Python-based Hardware Description Language (HDL) and synthesis f... | [SpectralSaber](https://github.com/starnbluey-cell/SpectralSaber) |
| [relysam](https://codeberg.org/0ai/relysam.git) | **QuantumSentinel** | `pushed` | 94.1 | 209 / 100 | Restructured python codebase | [QuantumSentinel](https://github.com/starnbluey-cell/QuantumSentinel) |
| [portage](https://codeberg.org/gentoo/portage.git) | **AzureNova** | `pushed` | 39.3 | 18785 / 12 | AzureNova is an advanced package compilation engine and software distribution manager designed fo... | [AzureNova](https://github.com/starnbluey-cell/AzureNova) |
| [hypergumbo](https://codeberg.org/iterabloom/hypergumbo.git) | **VoidSaber** | `pushed` | 84.8 | 6256 / 11 | VoidSaber is a modular compilation helper and grammar indexing framework designed to parse, valid... | [VoidSaber](https://github.com/starnbluey-cell/VoidSaber) |
| [phederation](https://codeberg.org/feldie/phederation.git) | **SolarHaven** | `pushed` | 5.0 | 1379 / 12 | Restructured python codebase | [SolarHaven](https://github.com/starnbluey-cell/SolarHaven) |
| [freeipa](https://codeberg.org/freeipa/freeipa.git) | **NebulaVortex** | `pushed` | 108.2 | 16658 / 12 | NebulaVortex is an enterprise-grade identity management, centralized authentication, and unified ... | [NebulaVortex](https://github.com/starnbluey-cell/NebulaVortex) |
| mock_src | **CyberHorizon** | `processed` | 10.0 | 100 / 100 | Restructured python codebase | N/A |
| [pushtunes](https://codeberg.org/psy-q/pushtunes.git) | **SilverDrift** | `pushed` | 2.8 | 169 / 100 | Restructured python codebase | [SilverDrift](https://github.com/starnbluey-cell/SilverDrift) |
| [Censor](https://codeberg.org/censor/Censor.git) | **SpectralHaven** | `processed` | 2.5 | 322 / 11 | Censor is a PDF document redaction tool. It permanently removes text and images | N/A |

<!-- END_PREPARED_REPOS_TABLE -->
