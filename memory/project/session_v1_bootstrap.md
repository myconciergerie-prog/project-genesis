<!-- SPDX-License-Identifier: MIT -->
---
name: Session v1 bootstrap — 2026-04-14 / 2026-04-15
description: Origin session of Project Genesis v1 — applied the v0 template (committed in aurum-ai at 0b1de3d) recursively to bootstrap the v1 plugin repo, producing this scaffold plus all v1 design specs and research cache entries
type: project
session_date: 2026-04-14
session_continued: 2026-04-15
origin_template: C:\Dev\Claude_cowork\aurum_ai\.claude\docs\superpowers\templates\project-genesis-2026.md (at commit 0b1de3d)
---

# Session v1 bootstrap

## Context

Project Genesis v0 was born during the Aurum.ai v0_init session on 2026-04-14 as a 7-phase template markdown. It was committed in the Aurum.ai repo at `0b1de3d` as a historical artefact. But its natural home was always its own dedicated repo — a workflow tool has a different lifecycle, audience, and license than a product.

This session recursively applies the v0 template to bootstrap the v1 plugin repo. The pattern is **compiler bootstrapping**: the first C compiler was written in assembly, rewritten in C, and compiled by itself. Every C compiler since 1971 self-compiles. Genesis follows the same philosophical move.

The user framed the recursion as a "strange loop" (Hofstadter) — the template reflects itself as it processes itself. See the vertigo journal entry in Aurum's auto-memory:

```
C:\Users\conta\.claude\projects\C--Dev-Claude-cowork-aurum-ai\memory\journal_2026-04-14_vertigo-genesis-dogfooding.md
```

## Decisions frozen during this session

### Structure and distribution

- **Repo name**: `project-genesis` (evergreen — no year suffix; rejected `project-genesis-2026` as brittle)
- **License**: MIT + SPDX short-form headers on every source file (per best-at-date research 2026, matches `obra/superpowers` which is the direct comparable)
- **Distribution**: self-hosted Claude Code plugin marketplace — the git repo IS the marketplace. Official Anthropic marketplace (`claude-plugins-official`) submission deferred until at least one external project uses Genesis (aurum-v1 re-bootstrap will be the first field test)
- **Structure**: plugin convention — `.claude-plugin/plugin.json` manifest, `skills/`, `templates/`, `hooks/` at plugin root, dev-internal docs in `.claude/docs/superpowers/`

### Rules R1-R10

Per the Étape 2 scoreboard, adapted from Aurum v1:

- **KEEP intégral**: R2 (worktree & branch discipline) — the universal pattern, no adaptation
- **ADAPT**: R1 (session lifecycle — drop OVH Actions check), R3 (deploy = `plugin.json` version bump + git tag + marketplace manifest update, NOT OVH), R4 (memory — add `journal/` and `pepites/` as 6th and 7th memory types), R5 (dual-layer docs: plugin content at root, dev docs in `.claude/docs/superpowers/`), R6 (sub-agents + Messages API only, drop Managed Agents R6.3)
- **DROP**: R7 (multi-backend MCP BYO-AI — purely Aurum-runtime-specific)
- **INHERIT from Layer 0**: R8 (research cache with TTL), R9 (language policy) — cited by reference, not duplicated
- **NEW**: R10 (plugin conventions + SPDX headers + self-rating discipline + anti-Frankenstein gate + pépite discipline)

Full rules in `.claude/docs/superpowers/rules/v1_rules.md`.

### Phase -1 Dependencies Pre-flight

**Originally scoped as a v2 feature, promoted to v1 core during this session** after the user said *"il est temps de connecter les MCP"* and *"multidevice dès le début on a des beta testeurs"*.

- **3-mode ladder**: detailed pas-à-pas / semi-auto / auto (user picks at consent time)
- **Mode 3 (auto)** pauses only at the 5 security-floor categories: sign-ins, admin passwords, browser extension permissions, 2FA, device authorization
- **Baseline detection**, **gap report card**, **batched sign-in round**, **batched restart round**, **verification pass**, **optional advanced bonus offer**
- **Multidevice core**: Claude Code Remote Control for Max users, Codespaces fallback for Pro users — subscription-aware branching
- **Core stack**: Claude Code CLI (Phase -2 prereq via `irm https://claude.ai/install.ps1 | iex`), VS Code extension (doubles as `ide` MCP server), Playwright MCP, Claude in Chrome
- **Optional bonuses**: Google Antigravity (multi-model IDE with Claude 4.6 + Gemini 3 + GPT-OSS), Android Termux local Claude Code, voice mode `/voice`, connector presets

Full spec in `.claude/docs/superpowers/specs/v1_phase_minus_one_first_user_bootstrap_flow.md`.

### Pépite discovery flagging (new v1 feature)

- **Red-light flag** raised during research when a discovery matches **two or more** of 6 criteria (contradicts past, asymmetric leverage, emerging tech, cross-cuts projects, saves time, most-potential framing)
- **Surfacing at next natural boundary**, user chooses: extract now / keep as seed / propagate to other projects / dismiss
- **Cross-project propagation** via pointer files until Meta-Memory Path B session builds the full graph tooling
- **7th memory type** `pepite` with dedicated frontmatter for routing metadata

Full spec in `.claude/docs/superpowers/specs/v1_pepite_discovery_flagging.md`. First operational component of Meta-Memory Layer 3 before the full Path B session.

### Cross-project research sharing (Layer 0 rule)

Added to `~/.claude/CLAUDE.md` as a universal feedback rule: when research in one project reveals SOTA tools or patterns relevant beyond that project, create **pointer files** in other projects' auto-memory instead of duplicating. Until Meta-Memory Path B builds `~/.claude/memory/research/` as the canonical cross-project cache, canonical entries live in the project of origin and pointers reference them.

Pointer file written during this session: `~/.claude/projects/C--Dev-Claude-cowork-aurum-ai/memory/reference_genesis_research_cache_pointer_2026-04-15.md`.

### Phase 5.5 Auth Pre-flight learnings (v1 polish from live dogfooding)

Based on v0_init pain observed in real time during this session:

- **PAT scope checklist updated** to include `Administration: Read and write` — learned 2026-04-14 when `gh api --method PATCH repos/.../...` failed with 403 on description update
- **Form-value copy-paste discipline**: each value in its own dedicated code block, never mixed with notes (learned when the user copy-pasted an instruction table cell including the parenthetical note into GitHub's description field)
- **Three-probe pre-flight test** (SSH + `gh api user` + `gh api repos/.../...`) as explicit Phase 5.5 exit condition before any Phase 5 writes

Full learnings in `.claude/docs/superpowers/specs/v1_phase_5_5_auth_preflight_learnings.md`.

### Anti-Frankenstein discipline (Layer 0 rule + R10.4)

- **Every feature must point to a documented pain point** (Aurum v0_init feedback memory, user request in this session, or live dogfooding friction)
- **Speculative features rejected by default**
- **Self-rating target intentionally sub-10** (8.5/10 for v1) — inflection point protection
- **Escape word**: if the user says `frankenstein`, current proposal is dropped immediately

### Multidevice as beta-tester feature

Promoted from Phase -1.7 optional to core during the 2026-04-15 refinement after the user said *"multidevice dès le début on a des beta testeurs"*. Beta testers will observe multidevice behavior from day one; shipping without it in the default flow would signal afterthought-grade design.

## Self-ratings by deliverable

| Deliverable | Self-rating | Axis details |
|---|---|---|
| **v0.1.0 scaffold (this commit)** | **6.0/10** | pain=2 / clean=6 / SOTA=8 / self-contained=5 / anti-Frankenstein=9 |
| v1 Phase -1 spec (stratified, 2 refinement layers) | 9.0/10 | Target-busting; load-bearing for v1 |
| v1 Phase 5.5 learnings spec | 7/10 | Needs more elaboration at Étape 5 |
| v1 Pépite spec | 8.8/10 | Above target; novel design |
| v2 Phase -1 dependencies (original) | 8.2/10 | Will merge/rename to v1 target at Étape 5 |
| R8 `claude-ecosystem-cross-os_2026-04-15` | 8.6/10 | Comprehensive per-OS matrix + 7 wow combos |
| R8 `claude-in-ide-tools_2026-04-15` | 8.7/10 | VS Code `ide` MCP discovery + Antigravity deep dive |
| R8 `claude-code-plugin-structure_2026-04-14` | 8/10 | Canonical spec reference |
| R8 `claude-code-session-jsonl-format_2026-04-14` | 7/10 | medium confidence — layout varies across versions |
| R8 `open-source-license-for-dev-tooling_2026-04-14` | 8/10 | Clean MIT decision + Apache-2 pivot |
| R8 `claude-code-plugin-distribution_2026-04-14` | 8/10 | Marketplace landscape well covered |
| R8 `spdx-headers_2026-04-14` | 8/10 | Straightforward but complete |

**Target v1.0.0 global rating: 8.5/10** (inflection point ceiling).

## Chronology of the session

- **2026-04-14** early: Aurum v0_init ends; user commits v0 template at `0b1de3d`; decides to separate into its own repo
- **2026-04-14** mid: Session opens in `C:\Dev\Claude_cowork\project-genesis-2026\` with `config.txt` seed
- **2026-04-14** progression: Path A (Layer 0 universal) finalization → Phase 1-2 discovery (5 questions → evergreen name, MIT, multi-file, plugin distribution, self-rating+anti-Frankenstein) → Phase 3 rules alignment scoreboard → Phase 4 research burst (5 initial R8 entries)
- **2026-04-14** late: SSH keygen + PAT creation + repo creation + pre-flight tests all pass; description garbled due to paste-back table-cell confusion (learning captured)
- **2026-04-14 → 15 transition**: Phase -1 design refinement — magical one-liner discovered, VS Code extension MCP server discovery, Antigravity deep dive, 7 wow combos identified, Phase -1 promoted from v2 to v1, pépite feature designed
- **2026-04-15**: Multidevice promoted to v1 core after beta-tester framing; cross-project research sharing rule added to Layer 0; aurum auto-memory pointer + Meta-Memory doc updated with pépite integration
- **2026-04-15** this commit: Étape 4d scaffold — the one-time R2.1 exception bootstrap commit that this file is part of

## Scope of what was built in this session

### Scaffold (Étape 4d — this commit)

Full directory structure and stub files for the v0.1.0 plugin scaffold.

### Design specs (4 v1 + 1 v2)

Each spec has its own self-rating ≥ 7/10. Captured during live research and design work.

### Research cache (7 R8 entries)

All SPDX-headered, all TTL-tagged. Cover license, plugin distribution, SPDX, plugin structure, JSONL format, Claude in IDE tools, cross-OS Claude ecosystem.

### Layer 0 additions

4 new Layer 0 rules: best-practice-at-date default, anti-Frankenstein, cross-project research sharing, pépite rule (this session added all four).

### Cross-project additive writes to Aurum auto-memory

Pointer file + Meta-Memory architecture addition + MEMORY.md index line. All additive, hors-repo, zero violation of the Aurum scope lock.

## What comes next

- **Étape 4e**: `git init` + first commit (the R2.1 exception bootstrap) + set remote via SSH alias + push to origin. This commit is named `bootstrap: project-genesis v0.1.0 scaffold` and is the **only** edit-in-root permitted for the lifetime of this repo. Everything after 4e happens in worktrees.
- **Étape 5**: v1 content work inside `.claude/worktrees/feat_2026-04-15_v1-content/` — implement skills one at a time, each in its own PR via `gh pr create` + `gh pr merge --squash`. Target: at least one skill (likely `phase-minus-one/` or `journal-system/`) reaches end-to-end in the first worktree PR → v0.2.0.
- **Étape 6**: Write session resume prompt to `.claude/docs/superpowers/resume/2026-04-15_v1_bootstrap_followup.md` for the next session to pick up at Étape 5.
- **Étape 7**: Goodbye card with updated self-ratings and the exact phrase the user should say to resume next session.

## References

- Aurum v0_init session origin: `~/.claude/projects/C--Dev-Claude-cowork-aurum-ai/memory/session_v0_init_summary.html`
- v0 template at birth: `C:\Dev\Claude_cowork\aurum_ai\.claude\docs\superpowers\templates\project-genesis-2026.md` @ commit `0b1de3d`
- Bootstrap config (seed): `.claude/docs/superpowers/plans/bootstrap_config_2026-04-14.md` (archived from repo root at Étape 4d)
- Aurum frozen scope lock: `memory/project/aurum_frozen_scope_lock.md`
- v1 rules: `.claude/docs/superpowers/rules/v1_rules.md`
- All specs: `.claude/docs/superpowers/specs/`
- All research: `.claude/docs/superpowers/research/`
