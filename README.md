<!-- SPDX-License-Identifier: MIT -->

# Project Genesis

> Recursive project bootstrap template, shipped as a Claude Code plugin.

**Version**: 0.1.0 (scaffold bootstrap)
**License**: MIT
**Status**: Pre-release. Functional content lands at Étape 5 of the bootstrap session, inside worktrees per R2.1.

---

## English

### What this is

Project Genesis is a Claude Code plugin that transforms a folder with a `config.txt` seed (plus optional mixed media) into a fully bootstrapped project — rules, memory architecture, research cache, git repo, and resume prompts — via a 7-phase protocol orchestrated by Claude Code itself.

The plugin ships:

- **Phase -1 Dependencies Pre-flight** — installs the required dev stack with minimal user intervention (3-mode ladder: detailed pas-à-pas / semi-auto / auto)
- **Phase 5.5 Auth Pre-flight** — exhaustive checklist that prevents auth setup pain (SSH keygen, PAT scopes, repo creation pattern, 3-probe pre-flight test)
- **Journal system** — stratified thought capture across sessions (6th memory type, trigger phrases like *"open a thought on X"*)
- **Session post-processor** — converts Claude Code's native JSONL transcripts into redacted Markdown archives
- **Pépite discovery flagging** — red-light system that surfaces high-leverage findings with cross-project routing metadata (7th memory type)
- **Canonical R1-R10 rule set** — adapted for any new project
- **Multidevice core** — Claude Code Remote Control pairing for Claude Max users, Codespaces fallback for Pro users

### The magical starting point

Open PowerShell on Windows and paste:

```powershell
irm https://claude.ai/install.ps1 | iex
```

On macOS / Linux:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Once Claude Code is installed, drop a `config.txt` in a fresh folder, run `claude` in that folder, and invoke Genesis via its plugin install command (published once v1.0.0 ships).

### Requirements

- Claude Code CLI 2.0.73+ (free plan NOT supported — Pro / Max / Team / Enterprise required)
- OS with a package manager: `winget` (Windows 10/11), `brew` (macOS), `apt` / `dnf` / `pacman` (Linux)
- Optional bonuses: VS Code, Chrome, Google Antigravity, a mobile device for Claude Code Remote Control

### Install

*(Self-hosted marketplace install command documented here at v1.0.0 release — pre-release currently.)*

---

## Français

### Ce que c'est

Project Genesis est un plugin Claude Code qui transforme un dossier contenant un seed `config.txt` (avec éventuellement des médias mixtes) en un projet entièrement bootstrapé — règles, architecture mémoire, cache de recherche, repo git, prompts de reprise — via un protocole 7-phases orchestré par Claude Code lui-même.

Le plugin livre :

- **Phase -1 Dependencies Pre-flight** — installe le stack dev requis avec intervention minimale du user (ladder 3 modes : détaillé / semi-auto / auto)
- **Phase 5.5 Auth Pre-flight** — checklist exhaustif qui prévient les douleurs d'auth setup (SSH keygen, scopes PAT, pattern de création de repo, pre-flight test 3 probes)
- **Système de journal** — capture stratifiée des pensées à travers les sessions (6ème type de mémoire, phrases trigger comme *"ouvre une pensée sur X"*)
- **Post-processor de session** — convertit les transcripts JSONL natifs de Claude Code en archives Markdown avec redaction des secrets
- **Pépite discovery flagging** — système red-light qui fait remonter les trouvailles à haut levier avec routing metadata cross-projets (7ème type de mémoire)
- **Rule set canonique R1-R10** — adapté pour tout nouveau projet
- **Multidevice core** — pairing Claude Code Remote Control pour les users Claude Max, fallback Codespaces pour les users Pro

### Le point de démarrage magique

Ouvre PowerShell sur Windows et colle :

```powershell
irm https://claude.ai/install.ps1 | iex
```

Sur macOS / Linux :

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Une fois Claude Code installé, dépose un `config.txt` dans un dossier vide, lance `claude` dans ce dossier, et invoque Genesis via sa commande d'install plugin (publiée quand v1.0.0 sort).

### Prérequis

- Claude Code CLI 2.0.73+ (plan gratuit PAS supporté — Pro / Max / Team / Enterprise requis)
- OS avec un package manager : `winget` (Windows 10/11), `brew` (macOS), `apt` / `dnf` / `pacman` (Linux)
- Bonus optionnels : VS Code, Chrome, Google Antigravity, un device mobile pour Claude Code Remote Control

### Installation

*(Commande d'install en self-hosted marketplace documentée ici quand v1.0.0 sort — pre-release actuellement.)*

---

## Status and self-rating history

| Version | Date | Rating | Notes |
|---|---|---|---|
| v0.1.0 | 2026-04-14 | 6.0/10 | Scaffold bootstrap only — no functional content yet |
| v1.0.0 | target | 8.5/10 | All v1 specs implemented as skills |

See `CHANGELOG.md` for the full 5-axis rating rubric and version history.

## License

MIT — see `LICENSE`. SPDX short-form identifiers (`SPDX-License-Identifier: MIT`) on every source file.

## Contributing

Pre-release. Contributions deferred until v1.0.0 ships.

## Acknowledgments

Born from the Aurum.ai v0_init session on 2026-04-14 as a 7-phase template committed at `0b1de3d`. This repo is the v1 self-bootstrap — the template applied recursively to itself. Compiler bootstrapping philosophy, Hofstadter strange-loop territory.
