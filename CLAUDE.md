<!-- SPDX-License-Identifier: MIT -->

# Project Genesis — CLAUDE.md

This is the project-level `CLAUDE.md` for the Project Genesis plugin repo. It is auto-loaded by Claude Code in every session opened inside this directory.

## Inherits from Layer 0

All universal rules, user profile, hard rules, workflow patterns, and machine-specific reference are **inherited by reference** from `~/.claude/CLAUDE.md` (Layer 0 universal). This file does NOT duplicate them — see Layer 0 directly for:

- **User profile** — identity, language, working style, AI stack
- **Hard rules** — additive auth, no new windows, R2.1 worktree discipline, R9 language policy, async mid-flow questions
- **Workflow patterns** — per-project SSH identity, GH_TOKEN env override, fine-grained PAT scope checklist, R8 research cache, best-practice-at-date default, anti-Frankenstein, cross-project research sharing
- **Journal system** — 6th memory type, trigger phrases, stratified dialogue format, amplification-on-consent
- **Machine-specific reference** — Chrome profiles mapping (Profile 2 = myconciergerie@gmail.com for Genesis work)

## Project-specific pointers

### Rules

Project-specific rules R1–R10 adapted for Genesis live at:

```
.claude/docs/superpowers/rules/v1_rules.md
```

These inherit R8 and R9 from Layer 0 by reference, drop R7 (multi-backend MCP BYO-AI — Aurum-runtime-specific), and add R10 (plugin conventions + self-rating discipline + SPDX headers + anti-Frankenstein gate + pépite discipline).

### Memory architecture

```
memory/
├── MEMORY.md           ← index, always loaded at session open per R1.1
├── master.md           ← stable vision + stack + rules summary
├── user/               ← project-scoped user notes (most profile in Layer 0)
├── feedback/           ← project-scoped collaboration rules (most rules in Layer 0)
├── project/            ← ongoing state, decisions, incidents, session history
├── reference/          ← external systems & accounts for this project
├── themes/             ← per-topic memory, populated as the project grows
├── journal/            ← stratified thought capture (6th memory type, Layer 0 spec)
└── pepites/            ← gold nugget discoveries with cross-project routing (7th memory type, specs/v1_pepite_discovery_flagging.md)
```

### Research cache

R8 research cache with TTL at:

```
.claude/docs/superpowers/research/
├── INDEX.md            ← auto-maintained index with expires_at dates
├── sota/               ← state of the art — TTL 7 days
├── stack/              ← package / MCP / version snapshots — TTL 1 day
└── archive/            ← deprecated reports, kept forensic
```

**Read `INDEX.md` before launching any new web research.** Active entries as of bootstrap cover:
- `open-source-license-for-dev-tooling` (MIT for Genesis, Apache-2 as pivot path)
- `claude-code-plugin-distribution` (self-hosted marketplace + official Anthropic marketplace)
- `spdx-headers` (canonical format per file type)
- `claude-code-plugin-structure` (`.claude-plugin/plugin.json` + root-level directories)
- `claude-code-session-jsonl-format` (transcript schema + redaction patterns)
- `claude-in-ide-tools` (VS Code extension = `ide` MCP server; Antigravity multi-model)
- `claude-ecosystem-cross-os` (per-OS matrix; Claude Code Remote Control; 280 connectors)

### Specs

Design specs at `.claude/docs/superpowers/specs/`:

- `v1_phase_5_5_auth_preflight_learnings.md` — live-dogfooding learnings from v1 bootstrap that inform the Phase 5.5 template content
- `v1_phase_minus_one_first_user_bootstrap_flow.md` — Phase -1 design with 3-mode ladder and multidevice core (stratified with 2 refinement layers)
- `v1_pepite_discovery_flagging.md` — red-light pépite system with cross-project routing metadata
- `v2_phase_minus_one_dependencies_automation.md` — original v2 target (will be renamed / merged at Étape 5 since the user promoted it to v1 target mid-session)

### Plans / Resume / Templates (dev-internal)

- `.claude/docs/superpowers/plans/` — multi-step implementation plans (including the archived `bootstrap_config_2026-04-14.md` seed)
- `.claude/docs/superpowers/resume/` — session resume prompts; read the most recent at session open
- `.claude/docs/superpowers/templates/` — dev-internal templates, separate from the shipped `templates/` at plugin root

## Scope lock — Aurum frozen

**Project aurum-ai is frozen at commit `0b1de3d`** until Genesis v1.0.0 ships. No work on aurum-ai code / commits / PRs is allowed in any Genesis session. Only additive auto-memory writes (pointer files) are permitted.

Full rule in `memory/project/aurum_frozen_scope_lock.md`. When the lock lifts, Aurum v1 kickoff opens as the immediately-next session.

## R1.1 Open ritual reminder

Every session opened in this directory must run R1.1 from `rules/v1_rules.md` before any Edit / Write:

1. Absolute date check
2. Read `memory/MEMORY.md` + `memory/master.md` + any theme memory relevant to planned work
3. `git status -s` must be empty — investigate if not
4. Read latest resume prompt from `.claude/docs/superpowers/resume/`
5. Scan `research/INDEX.md` for expired entries → archive + update index
6. Stack check — R8 TTL on `stack/` entries
7. Create the session worktree per R2.1 **before any Edit/Write**

## Quick-start for a returning session

If you're coming back to this repo after a break, read in order:

1. `memory/MEMORY.md` (this index)
2. `memory/master.md` (stable vision)
3. `memory/project/session_v1_bootstrap.md` (origin session context)
4. The most recent file in `.claude/docs/superpowers/resume/` (handoff from last session)
5. `CHANGELOG.md` (current version + self-rating history)

Then create your worktree and start.
