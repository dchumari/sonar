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

| Original Repository Name | Unique Destination Name | Status | Timestamp | GitHub Target Repo |
| :--- | :--- | :--- | :--- | :--- |
| [blended-strawberry](https://codeberg.org/unwanted9855/blended-strawberry.git) | **BerrySynth** | `pushed` | 2026-07-27 | [BerrySynth](https://github.com/starnbluey-cell/BerrySynth) |
| [openwrt](https://codeberg.org/openwrt/openwrt.git) | **GatewayFirmware** | `pushed` | 2026-07-27 | [GatewayFirmware](https://github.com/starnbluey-cell/GatewayFirmware) |
| [curv](https://codeberg.org/doug-moen/curv.git) | **CurvModeler** | `pushed` | 2026-07-27 | [CurvModeler](https://github.com/starnbluey-cell/CurvModeler) |
| [OpenRGB](https://codeberg.org/OpenRGB/OpenRGB.git) | **SpectrumLight** | `pushed` | 2026-07-27 | [SpectrumLight](https://github.com/starnbluey-cell/SpectrumLight) |
| [blankart](https://codeberg.org/NepDisk/blankart.git) | **VividRender** | `pushed` | 2026-07-27 | [VividRender](https://github.com/starnbluey-cell/VividRender) |
| [C-Menu](https://codeberg.org/BillWaller/C-Menu.git) | **MenuConsole** | `pushed` | 2026-07-27 | [MenuConsole](https://github.com/starnbluey-cell/MenuConsole) |
| [mkshot](https://codeberg.org/u16/mkshot.git) | **SnapCapture** | `pushed` | 2026-07-27 | [SnapCapture](https://github.com/starnbluey-cell/SnapCapture) |
| [curl-mirror](https://codeberg.org/curl/curl-mirror.git) | **NetTransfer** | `pushed` | 2026-07-27 | [NetTransfer](https://github.com/starnbluey-cell/NetTransfer) |
| [noctalia](https://codeberg.org/noctalia-dev/noctalia.git) | **NoctaliaCore** | `pushed` | 2026-07-27 | [NoctaliaCore](https://github.com/starnbluey-cell/NoctaliaCore) |
| [eden](https://codeberg.org/eden-emu/eden.git) | **EdenEmu** | `pushed` | 2026-07-27 | [EdenEmu](https://github.com/starnbluey-cell/EdenEmu) |
| [xenia_canary_experimental](https://codeberg.org/thunksuck3r/xenia_canary_experimental.git) | **CoreEmulator** | `pushed` | 2026-07-27 | [CoreEmulator](https://github.com/starnbluey-cell/CoreEmulator) |
| [SaveManager](https://codeberg.org/marco007/SaveManager.git) | **VaultKeeper** | `pushed` | 2026-07-27 | [VaultKeeper](https://github.com/starnbluey-cell/VaultKeeper) |
| [ansible](https://codeberg.org/asaramet/ansible.git) | **DeployAutomation** | `pushed` | 2026-07-26 | [DeployAutomation](https://github.com/starnbluey-cell/DeployAutomation) |
| [PyPSA](https://codeberg.org/neunzehnachtneun/PyPSA.git) | **GridEnergy** | `pushed` | 2026-07-26 | [GridEnergy](https://github.com/starnbluey-cell/GridEnergy) |
| [stack-harness](https://codeberg.org/myoungjin/stack-harness.git) | **HarnessStack** | `pushed` | 2026-07-26 | [HarnessStack](https://github.com/starnbluey-cell/HarnessStack) |
| [karrot-backend](https://codeberg.org/karrot/karrot-backend.git) | **KarrotCore** | `pushed` | 2026-07-26 | [KarrotCore](https://github.com/starnbluey-cell/KarrotCore) |
| [crochess](https://codeberg.org/mmlacak/crochess.git) | **TacticalChess** | `pushed` | 2026-07-26 | [TacticalChess](https://github.com/starnbluey-cell/TacticalChess) |
| [mcp-memory-service](https://codeberg.org/doobidoo/mcp-memory-service.git) | **CogniMem** | `pushed` | 2026-07-26 | [CogniMem](https://github.com/starnbluey-cell/CogniMem) |
| [AudioMuse-AI](https://codeberg.org/NeptuneHub/AudioMuse-AI.git) | **AudioMuse** | `pushed` | 2026-07-26 | [AudioMuse](https://github.com/starnbluey-cell/AudioMuse) |
| [PhoenixAdult](https://codeberg.org/PhoenixAdultProvider/PhoenixAdult.git) | **PhoenixPortal** | `pushed` | 2026-07-26 | [PhoenixPortal](https://github.com/starnbluey-cell/PhoenixPortal) |
| [FoxDot-ce](https://codeberg.org/FoxDot-community/FoxDot-ce.git) | **SonicSynth** | `pushed` | 2026-07-26 | [SonicSynth](https://github.com/starnbluey-cell/SonicSynth) |
| [LSaO-visualizer](https://codeberg.org/aaronfbianchi/LSaO-visualizer.git) | **SpaceVisualizer** | `pushed` | 2026-07-26 | [SpaceVisualizer](https://github.com/starnbluey-cell/SpaceVisualizer) |
| [created_with_eee](https://codeberg.org/EEE-project/created_with_eee.git) | **AuraCanvas** | `pushed` | 2026-07-26 | [AuraCanvas](https://github.com/starnbluey-cell/AuraCanvas) |
| [pypsmcbor](https://codeberg.org/PAPPSO/pypsmcbor.git) | **ProteoMetric** | `pushed` | 2026-07-26 | [ProteoMetric](https://github.com/starnbluey-cell/ProteoMetric) |
| [nge_2_re](https://codeberg.org/EVA-zh-Hans/nge_2_re.git) | **VividEngine** | `pushed` | 2026-07-26 | [VividEngine](https://github.com/starnbluey-cell/VividEngine) |
| [PySIDM](https://codeberg.org/RotemBarnea/PySIDM.git) | **MatterGravity** | `pushed` | 2026-07-26 | [MatterGravity](https://github.com/starnbluey-cell/MatterGravity) |
| [fayf_processor](https://codeberg.org/pluggpreagar/fayf_processor.git) | **DataWeave** | `pushed` | 2026-07-26 | [DataWeave](https://github.com/starnbluey-cell/DataWeave) |
| [ss](https://codeberg.org/angelogreco/ss.git) | **TunnelFlow** | `pushed` | 2026-07-26 | [TunnelFlow](https://github.com/starnbluey-cell/TunnelFlow) |
| [seedsigner](https://codeberg.org/kdmukAI-bot/seedsigner.git) | **ColdSigner** | `pushed` | 2026-07-26 | [ColdSigner](https://github.com/starnbluey-cell/ColdSigner) |
| [Quant-Nanggroe-AI](https://codeberg.org/Dhaher-Labs/Quant-Nanggroe-AI.git) | **TradeCalculus** | `pushed` | 2026-07-26 | [TradeCalculus](https://github.com/starnbluey-cell/TradeCalculus) |
| [cognee](https://codeberg.org/nopejs/cognee.git) | **SemanticMind** | `pushed` | 2026-07-26 | [SemanticMind](https://github.com/starnbluey-cell/SemanticMind) |
| [smol-k8s-lab](https://codeberg.org/open-engineering/smol-k8s-lab.git) | **NanoCluster** | `pushed` | 2026-07-26 | [NanoCluster](https://github.com/starnbluey-cell/NanoCluster) |
| [gpt4free](https://codeberg.org/gpt4free-mirror/gpt4free.git) | **FreeAiGateway** | `pushed` | 2026-07-24 | [FreeAiGateway](https://github.com/starnbluey-cell/FreeAiGateway) |
| [gallery-dl](https://codeberg.org/mikf/gallery-dl.git) | **MediaGrabber** | `pushed` | 2026-07-24 | [MediaGrabber](https://github.com/starnbluey-cell/MediaGrabber) |
| [RAT](https://codeberg.org/RandoOne/RAT.git) | **RatAdmin** | `pushed` | 2026-07-24 | [RatAdmin](https://github.com/starnbluey-cell/RatAdmin) |
| [endurain](https://codeberg.org/endurain-project/endurain.git) | **EnduranceTrack** | `pushed` | 2026-07-24 | [EnduranceTrack](https://github.com/starnbluey-cell/EnduranceTrack) |
| [origin-axiom](https://codeberg.org/originaxiom/origin-axiom.git) | **AxiomEngine** | `pushed` | 2026-07-24 | [AxiomEngine](https://github.com/starnbluey-cell/AxiomEngine) |
| [gradlew.py](https://codeberg.org/IzzyOnDroid/gradlew.py.git) | **SilentDrift** | `processed` | 2026-07-24 | N/A |
| [scriptura](https://codeberg.org/andresmessina/scriptura.git) | **NebulaRift** | `pushed` | 2026-07-24 | [NebulaRift](https://github.com/starnbluey-cell/NebulaRift) |
| [LotansTomb](https://codeberg.org/mc776/LotansTomb) | **NebulaCrypt** | `pushed` | 2026-07-24 | [NebulaCrypt](https://github.com/starnbluey-cell/NebulaCrypt) |
| [yadgar](https://codeberg.org/maxagahi/yadgar.git) | **AzureHorizon** | `pushed` | 2026-07-24 | [AzureHorizon](https://github.com/starnbluey-cell/AzureHorizon) |
| [rope-language-server](https://codeberg.org/mcepl/rope-language-server.git) | **StormSummit** | `pushed` | 2026-07-24 | [StormSummit](https://github.com/starnbluey-cell/StormSummit) |
| [Ralph-Workflow](https://codeberg.org/RalphWorkflow/Ralph-Workflow.git) | **SolarRift** | `pushed` | 2026-07-24 | [SolarRift](https://github.com/starnbluey-cell/SolarRift) |
| [opendesk-edu](https://codeberg.org/opendesk-edu/opendesk-edu.git) | **EchoSaber** | `pushed` | 2026-07-24 | [EchoSaber](https://github.com/starnbluey-cell/EchoSaber) |
| [matridge](https://codeberg.org/slidge/matridge.git) | **QuantumCanyon** | `pushed` | 2026-07-24 | [QuantumCanyon](https://github.com/starnbluey-cell/QuantumCanyon) |
| [home-assistant-chart](https://codeberg.org/open-engineering/home-assistant-chart.git) | **SilentRift** | `processed` | 2026-07-24 | N/A |
| [siun](https://codeberg.org/lokimotive/siun.git) | **QuantumHaven** | `pushed` | 2026-07-24 | [QuantumHaven](https://github.com/starnbluey-cell/QuantumHaven) |
| [torii-hdl](https://codeberg.org/shrine-maiden-heavy-industries/torii-hdl.git) | **SpectralSaber** | `pushed` | 2026-07-24 | [SpectralSaber](https://github.com/starnbluey-cell/SpectralSaber) |
| [relysam](https://codeberg.org/0ai/relysam.git) | **QuantumSentinel** | `pushed` | 2026-07-24 | [QuantumSentinel](https://github.com/starnbluey-cell/QuantumSentinel) |
| [portage](https://codeberg.org/gentoo/portage.git) | **AzureNova** | `pushed` | 2026-07-24 | [AzureNova](https://github.com/starnbluey-cell/AzureNova) |
| [hypergumbo](https://codeberg.org/iterabloom/hypergumbo.git) | **VoidSaber** | `pushed` | 2026-07-24 | [VoidSaber](https://github.com/starnbluey-cell/VoidSaber) |
| [phederation](https://codeberg.org/feldie/phederation.git) | **SolarHaven** | `pushed` | 2026-07-24 | [SolarHaven](https://github.com/starnbluey-cell/SolarHaven) |
| [freeipa](https://codeberg.org/freeipa/freeipa.git) | **NebulaVortex** | `pushed` | 2026-07-23 | [NebulaVortex](https://github.com/starnbluey-cell/NebulaVortex) |
| mock_src | **CyberHorizon** | `processed` | 2026-07-23 | N/A |
| [pushtunes](https://codeberg.org/psy-q/pushtunes.git) | **SilverDrift** | `pushed` | 2026-07-23 | [SilverDrift](https://github.com/starnbluey-cell/SilverDrift) |
| [Censor](https://codeberg.org/censor/Censor.git) | **SpectralHaven** | `processed` | 2026-07-23 | N/A |

<!-- END_PREPARED_REPOS_TABLE -->
