<!-- SPDX-License-Identifier: MIT -->

# Project Genesis

> A Claude Code plugin that bootstraps a fresh project folder into a fully wired codebase — rules, memory architecture, research cache, git repo on GitHub, SSH identity, and a resume prompt for the next session — via a 7-phase orchestrated protocol.

**Version**: 0.9.0 (Path A polish toward v1.0.0) · **License**: MIT · **Status**: approaching v1.0.0 ship candidate

---

## English

### What Genesis does

Drop a `config.txt` (name, vision, license, plan tier) in an empty folder, open Claude Code in that folder, say `/genesis-protocol`, and Genesis runs 7 phases end-to-end: dependencies pre-flight, seed parsing, rules + memory scaffold, research cache, git init with a per-project SSH identity, GitHub auth pre-flight (SSH key + fine-grained PAT + empty repo + 3-probe gate), first commit + tag `v0.1.0`, resume prompt for the next session, and a redacted archive of the bootstrap transcript. Every privileged step has an explicit consent gate — nothing runs silently. The result is a project ready for real work at `v0.2.0`.

### The 7-phase protocol

| # | Phase | What it does |
|---|---|---|
| **-1** | Dependencies pre-flight | Detect dev stack, install gaps via a 3-mode ladder (detailed / semi-auto / auto), batch sign-ins, verify |
| **0** | Seed loading | Parse `config.txt` + mixed media into `memory/project/bootstrap_intent.md` |
| **1+2** | Rules + memory + research cache | Copy R1–R10 rules, scaffold `memory/`, invoke sibling install-manifests, seed the R8 research cache |
| **3+4** | Git init + project seeds | `git init -b main`, per-project ed25519 SSH key, `github.com-<slug>` host alias, `master.md`, `README.md`, `CHANGELOG.md`, optional `.claude-plugin/plugin.json` if plugin |
| **5.5** | Auth pre-flight | SSH keygen cross-check, fine-grained PAT creation, empty repo creation on GitHub, 3-probe test — all behind a consent gate |
| **6+7** | Commit + tag + resume + archive | First commit on `main`, tag `v0.1.0`, write the next session's resume prompt, invoke `session-post-processor` with halt-on-leak gate |

See `memory/master.md` for the canonical description and `skills/genesis-protocol/SKILL.md` for the full master table with per-phase runbook pointers.

### The six shipped skills

| Skill | What it does |
|---|---|
| `phase-minus-one` | 7-sub-phase dev stack pre-flight with a 3-mode ladder and multidevice baseline (Max Remote Control / Pro Codespaces) |
| `phase-5-5-auth-preflight` | SSH + PAT + empty repo creation + 3-probe gate; paste-back default, isolated copy-paste rule |
| `journal-system` | Stratified thought capture (6th memory type); speech-native triggers like *"open a thought on X"* / *"ouvre une pensée sur X"* |
| `session-post-processor` | Parse Claude Code's JSONL transcripts, redact secrets, emit Markdown archives to `memory/project/sessions/` with a halt-on-leak gate |
| `pepite-flagging` | Red-light discovery system with cross-project routing (7th memory type); per-target consent for sibling-project writes |
| `genesis-protocol` | The conductor — orchestrates the other five skills through the 7 phases with a top-level consent card |

Each skill has exactly one concentrated privilege and follows the 1:1 spec mirror discipline where applicable. See `memory/master.md` → "Cross-skill patterns" for the three emergent patterns that compose them.

### Quick-start (five steps)

1. **Install Claude Code** if you don't already have it: PowerShell `irm https://claude.ai/install.ps1 | iex` on Windows, or `curl -fsSL https://claude.ai/install.sh | bash` on macOS / Linux. Pro / Max / Team / Enterprise plan required.
2. **Create a fresh empty folder** for your new project and drop a `config.txt` inside it. Minimum fields: `name`, `slug` (optional, derived from name), `vision`, `license`, `is-a-plugin`, `plan-tier`. See `skills/genesis-protocol/phase-0-seed-loading.md` for the full field reference.
3. **Open Claude Code** in that folder: `cd path/to/new-folder && claude`.
4. **Say** `/genesis-protocol` (or any natural-language trigger like *"bootstrap this project"* / *"lance genesis"*). Genesis renders a top-level consent card showing the full plan — confirm it, then each phase runs with its own confirmation.
5. **The bootstrap session ends** with a genesis report, a `v0.1.0` tag on GitHub, and a resume prompt in `.claude/docs/superpowers/resume/<date>_bootstrap_to_v0_2.md`. Open Claude Code again in the same folder and start `v0.2.0` — the first real session.

### Where to go next

- **`memory/master.md`** — stable vision, stack, rules summary, Layer 0 inheritance explanation, the three cross-skill patterns
- **`CHANGELOG.md`** — full version history with the 5-axis self-rating rubric (pain-driven / prose cleanliness / best-at-date / self-contained / anti-Frankenstein)
- **`CLAUDE.md`** — project-level Claude Code pointer file; inherits universal rules from `~/.claude/CLAUDE.md` (Layer 0)
- **`skills/*/SKILL.md`** — entry point for each skill

### Requirements

- Claude Code CLI 2.0.73+ (free plan **not** supported — Pro / Max / Team / Enterprise required)
- OS with a package manager: `winget` (Windows 10/11), `brew` (macOS), `apt` / `dnf` / `pacman` (Linux)
- Git 2.28+ for `git init -b main` support
- Optional bonuses: VS Code, Chrome, Google Antigravity, a mobile device for Claude Code Remote Control

---

## Français

### Ce que fait Genesis

Dépose un `config.txt` (nom, vision, licence, plan tier) dans un dossier vide, ouvre Claude Code dans ce dossier, dis `/genesis-protocol`, et Genesis exécute 7 phases de bout en bout : pre-flight des dépendances, parsing du seed, scaffold règles + mémoire, cache de recherche, init git avec identité SSH dédiée au projet, pre-flight d'auth GitHub (clé SSH + PAT fine-grained + repo vide + gate 3-probes), premier commit + tag `v0.1.0`, prompt de reprise pour la session suivante, et archive rédactée du transcript de bootstrap. Chaque étape privilégiée a un gate de consentement explicite — rien ne tourne en silence. Le résultat est un projet prêt pour le vrai travail à `v0.2.0`.

### Le protocole 7-phases

| # | Phase | Ce qu'elle fait |
|---|---|---|
| **-1** | Dependencies pre-flight | Détecte le stack dev, installe les gaps via un ladder 3 modes (détaillé / semi-auto / auto), batch sign-ins, vérification |
| **0** | Seed loading | Parse `config.txt` + médias mixtes vers `memory/project/bootstrap_intent.md` |
| **1+2** | Règles + mémoire + cache recherche | Copie des règles R1–R10, scaffold `memory/`, invocation des install-manifests siblings, seed du cache R8 |
| **3+4** | Git init + seeds projet | `git init -b main`, clé SSH ed25519 dédiée, alias hôte `github.com-<slug>`, `master.md`, `README.md`, `CHANGELOG.md`, `.claude-plugin/plugin.json` conditionnel |
| **5.5** | Auth pre-flight | Cross-check SSH keygen, création PAT fine-grained, création repo vide GitHub, test 3-probes — tout derrière un gate de consentement |
| **6+7** | Commit + tag + resume + archive | Premier commit sur `main`, tag `v0.1.0`, écriture du prompt de reprise de la prochaine session, invocation `session-post-processor` avec gate halt-on-leak |

Voir `memory/master.md` pour la description canonique et `skills/genesis-protocol/SKILL.md` pour la master table complète avec les pointeurs runbook par phase.

### Les six skills livrés

| Skill | Ce qu'il fait |
|---|---|
| `phase-minus-one` | Pre-flight dev stack en 7 sous-phases, ladder 3 modes, baseline multidevice (Max Remote Control / Pro Codespaces) |
| `phase-5-5-auth-preflight` | SSH + PAT + création repo vide + gate 3-probes ; paste-back par défaut, règle de copy-paste isolé |
| `journal-system` | Capture stratifiée des pensées (6ème type de mémoire) ; triggers speech-native comme *"ouvre une pensée sur X"* |
| `session-post-processor` | Parse les transcripts JSONL Claude Code, rédige les secrets, émet des archives Markdown dans `memory/project/sessions/` avec gate halt-on-leak |
| `pepite-flagging` | Système de découverte red-light avec routing cross-projet (7ème type de mémoire) ; consentement per-target pour les écritures dans les projets voisins |
| `genesis-protocol` | Le conducteur — orchestre les cinq autres skills à travers les 7 phases avec un consent card de haut niveau |

Chaque skill a exactement un privilège concentré et suit la discipline 1:1 spec mirror quand applicable. Voir `memory/master.md` → "Cross-skill patterns" pour les trois patterns émergents qui les composent.

### Quick-start (cinq étapes)

1. **Installe Claude Code** si ce n'est pas déjà fait : PowerShell `irm https://claude.ai/install.ps1 | iex` sur Windows, ou `curl -fsSL https://claude.ai/install.sh | bash` sur macOS / Linux. Plan Pro / Max / Team / Enterprise requis.
2. **Crée un dossier vide** pour ton nouveau projet et dépose un `config.txt` dedans. Champs minimaux : `name`, `slug` (optionnel, dérivé du nom), `vision`, `license`, `is-a-plugin`, `plan-tier`. Voir `skills/genesis-protocol/phase-0-seed-loading.md` pour la référence complète.
3. **Ouvre Claude Code** dans ce dossier : `cd chemin/vers/nouveau-dossier && claude`.
4. **Dis** `/genesis-protocol` (ou n'importe quel trigger naturel comme *"bootstrap this project"* / *"lance genesis"*). Genesis rend un consent card de haut niveau avec le plan complet — confirme-le, puis chaque phase tourne avec sa propre confirmation.
5. **La session de bootstrap se termine** avec un rapport genesis, un tag `v0.1.0` sur GitHub, et un prompt de reprise dans `.claude/docs/superpowers/resume/<date>_bootstrap_to_v0_2.md`. Réouvre Claude Code dans le même dossier et démarre `v0.2.0` — la première vraie session.

### Pour aller plus loin

- **`memory/master.md`** — vision stable, stack, résumé des règles, explication de l'héritage Layer 0, les trois cross-skill patterns
- **`CHANGELOG.md`** — historique complet avec la rubrique de self-rating 5 axes (pain-driven / prose cleanliness / best-at-date / self-contained / anti-Frankenstein)
- **`CLAUDE.md`** — fichier pointeur Claude Code au niveau projet ; hérite des règles universelles depuis `~/.claude/CLAUDE.md` (Layer 0)
- **`skills/*/SKILL.md`** — point d'entrée de chaque skill

### Prérequis

- Claude Code CLI 2.0.73+ (plan gratuit **non** supporté — Pro / Max / Team / Enterprise requis)
- OS avec un package manager : `winget` (Windows 10/11), `brew` (macOS), `apt` / `dnf` / `pacman` (Linux)
- Git 2.28+ pour le support de `git init -b main`
- Bonus optionnels : VS Code, Chrome, Google Antigravity, un device mobile pour Claude Code Remote Control

---

## License

MIT — see `LICENSE`. SPDX short-form identifiers (`SPDX-License-Identifier: MIT`) on every source file, enforced by R10.

## Acknowledgments

Born from the Aurum.ai `v0_init` session on 2026-04-14 as a 7-phase template committed at `0b1de3d`. This repo is the v1 self-bootstrap — the template applied recursively to itself. Compiler bootstrapping philosophy, Hofstadter strange-loop territory. Every friction that surfaced during the self-application informed the v1 design, all the way through v0.2 → v0.9.
