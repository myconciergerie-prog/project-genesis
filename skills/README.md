<!-- SPDX-License-Identifier: MIT -->

# skills/

This directory holds the skills that Project Genesis ships. Per Claude Code plugin convention (2026), `skills/` is at the plugin root level — **NOT** inside `.claude-plugin/`. Only `plugin.json` lives in `.claude-plugin/`.

## Planned skills for v1.0.0

The following skills land here at **Étape 5** of the v1 bootstrap session, implemented inside worktrees per R2.1 discipline (one skill per PR, squash-merged via `gh pr merge --squash`):

- **`genesis-protocol/`** — the 7-phase protocol orchestrator (Phase 0 sanity → Phase 1 multimodal pre-read → Phase 2 interactive discovery → Phase 3 rules alignment → Phase 4 research burst → Phase 5 bootstrap → Phase 5.5 auth pre-flight → Phase 6 resume → Phase 7 goodbye)
- **`phase-minus-one/`** — Dependencies Pre-flight. Detects OS, package manager, existing stack, gaps. Presents gap report card. Offers 3-mode ladder (detailed pas-à-pas / semi-auto / auto). Runs installs via `winget` / `brew` / `apt`. Handles the batched sign-in round and batched restart round. Multidevice core per `specs/v1_phase_minus_one_first_user_bootstrap_flow.md`.
- **`phase-5-5-auth-preflight/`** — Auth Pre-flight checklist implementation. SSH keygen + `~/.ssh/config` alias. Fine-grained PAT creation walkthrough with the full scope list (Contents RW, Metadata R, PR RW, Workflows RW, Administration RW). Empty repo creation pattern via web UI paste-back. Three-probe pre-flight test (SSH + `gh api user` + `gh api repos/.../.../`). Branches on Playwright MCP availability for automation vs paste-back.
- **`journal-system/`** — Stratified thought capture. Trigger phrases recognizer (`ouvre / reprends / enregistre / enrichis / clôture la pensée sur X`). Entry creator with YAML frontmatter and stratified dialogue format. Amplification-on-consent handler. State transition manager (`seed` → `growing` → `dormant` → `resolved` | `captured`). See Layer 0 for the full journal spec.
- **`session-post-processor/`** — Reads Claude Code's native JSONL transcripts from `~/.claude/projects/<slug>/<uuid>.jsonl`. Parses typed message records chained by `parentUuid`. Runs secret redaction pass (regex patterns for `github_pat_`, `ghp_`, `sbp_`, `sb_secret_`, `sk_`, JWT, AWS keys). Emits Markdown transcript with frontmatter to `.claude/docs/superpowers/sessions/YYYY-MM-DD_<slug>.md`. Updates `sessions/INDEX.md` with a one-line entry. Optional `SessionEnd` hook wiring deferred to v1.1.0.
- **`pepite-flagging/`** — Red-light detection during research. The 6 criteria with "two or more" rule. Pépite entry creator with routing metadata (`origin_project` / `transverse` / `specific_projects`). Cross-project pointer writer. Surfacing card generator for user prompts. Status transition handler (`seed` → `extracted` / `actioned` / `archived` / `dismissed`). Full spec in `.claude/docs/superpowers/specs/v1_pepite_discovery_flagging.md`.

## Claude Code skills convention (Q2 2026 reminder)

- Every skill gets a `/<skill-name>` slash-command interface automatically
- Skills are recommended over `.claude/commands/` for new plugins (commands still work for backward compatibility)
- Auto-discovery: Claude Code loads everything under `skills/` without manifest-level paths in `plugin.json` — keep standard directory names
- Each skill is a subdirectory with its own content (markdown prompts, Python / shell scripts, optional assets)

Refer to `.claude/docs/superpowers/research/stack/claude-code-plugin-structure_2026-04-14.md` for the full plugin layout spec.

## Anti-Frankenstein reminder

No skill ships without a documented pain point it addresses. Every skill above points to a specific `specs/` file or a specific feedback memory from the Aurum v0_init session. Speculative skills are rejected by default per R10.4.
