<!-- SPDX-License-Identifier: MIT -->
---
name: Resume prompt — 2026-04-17 v1.2.0 selfdogfood → v1.2.1 structural fixes
description: Handoff from the second self-dogfood (conscious strange loop). 13 new frictions (F20–F33) captured, v2 spec amended with Étape 0 drop-zone + Promptor correction. v1.2.1 is the ship-fix cycle: close P0 structural issues before any further v2 work.
type: resume
previous_session: v1.2.0 selfdogfood (feat/v1.2.0-selfdogfood branch, PR #TBD)
next_action: Land P0 fixes (F29 rules path + F30 nested-repo check + F23/F27 paradox guards) in a separate v1.2.1 session
---

# Resume — 2026-04-17 v1.2.0-selfdogfood → v1.2.1

## What v1.2.0-selfdogfood did

- Closed the strange loop consciously (worktree target + config.txt describing Genesis).
- Captured **13 new frictions F20–F33** live: 5 STRUCTURAL, 6 DESIGN, 2 COSMETIC.
- Ran 3 research agents in parallel (drop-drop UX, doc extraction, conversational briefing) → consolidated SOTA entry at `research/sota/v2_promptor_fusion_landscape_2026-04-17.md` (TTL 2026-04-24).
- Amended `specs/v2_vision_promptor_fusion.md` with a new **Étape 0 — Le Dépôt** and a factual correction ("Promptor 4-part structure" is Genesis-native, not a published pattern).
- Self-rating v1.2.0-sd: **8.70/10**. Running average v0.1 → v1.2.0-sd: **8.51/10** (above 8.5 v1 target).

## Pépites flagged (cross-project alert)

1. **F29 — Genesis v1.1 plugin personal-scope install is broken.** Users who followed F18's `cp -r skills/ ~/.claude/skills/` cannot run the orchestrator end-to-end: Phase 1.3 rules resolution (three-levels-up heuristic) yields `~/.claude/` which has no `.claude/docs/superpowers/rules/`. **Priority: README warning in v1.1.0 release notes + P0 fix in v1.2.1.**

2. **"Promptor 4-part structure" is Genesis-native.** Credit Genesis for the synthesis in all external communication (v2 blog post, marketplace listing, community Q&A). The academic Promptor paper does not describe this structure.

Both pépites await pointer files in `memory/pepites/` and cross-project propagation per `specs/v1_pepite_discovery_flagging.md`. Route to `~/.claude/memory/project_claude_cowork_roadmap.md` (v1.2.1 task).

## v1.2.1 — what to ship

P0 structural blockers (must fix before any further v2 work):

| Friction | Fix |
|---|---|
| **F29** | Option A: ship `v1_rules.md` inside `skills/genesis-protocol/rules/` so the skill is self-contained. Option B: require `cp -r .claude/docs/superpowers/rules/` at install time with a loud README note. Recommend A. |
| **F30** | In `phase-3-git-init.md` Step 3.1, replace literal `.git/` check with `git rev-parse --show-toplevel 2>/dev/null`. If output is a path ≠ target, STOP with "target is inside existing git repo at X — nested repos unsupported". |
| **F23 + F27** | In `SKILL.md` Step 0, pre-flight check: if target path is inside the orchestrator's own repo tree (`git rev-parse --show-toplevel` from target resolves to a parent containing `skills/genesis-protocol/`), OR if derived slug equals the orchestrator's own slug, STOP. |

P1 features (after P0):

| Friction | Fix |
|---|---|
| F20 + F22 + F21 | `mode` argument with detailed / semi-auto / auto semantics; `## Arguments` section in SKILL.md |
| F32 | Plan a lightweight Python driver for v1.3 (`genesis_protocol/driver.py` treating Markdown runbooks as templates + `.genesis/state.json` for re-entrancy) |

P2 polish:

| Friction | Fix |
|---|---|
| F25 + F31 | `templates/config-minimal.txt.example` + `templates/config-complete.txt.example` + README Quick Start |
| F26 | Phase 0 passes non-canonical fields to `bootstrap_intent.md` under "Non-canonical fields (passed through)" |
| F28 | `genesis-cleanup` sibling skill OR `--cleanup` orchestrator flag |
| F33 | R8 scope disambiguation note in the cache convention |

## Current state

- Branch: `feat/v1.2.0-selfdogfood` at `31f960d` base + v1.2 deliverables (friction log, session memory, v2 spec amendments, R8 research entry, bootstrap_intent.md, config.txt in the target).
- Main: clean, at `31f960d` (F18/F19 commit).
- A PR opened at end of v1.2.0-sd session (**draft — do not merge until user approves v1.2.1 plan**).
- 3 research agents left running IDs available for follow-up: `a3a29e0f`, `af96288a`, `a0ea272e`.

## Open questions for v1.2.1 kickoff

1. Should v1.2.1 be a ship cycle (tag v1.2.1 after P0 fixes) or an interim (tag v1.2.0 with P0 fixed, treat v1.2.1 as the v2 prep cycle)?
2. Should the research entry `v2_promptor_fusion_landscape_2026-04-17.md` live in main's R8 cache or stay in the selfdogfood-target as a forensic artefact? (F33 raised this.)
3. Does the user want the pépite pointer files written NOW (v1.2.0-sd wrap-up) or at v1.2.1 open?

## Suggested first action at v1.2.1 open

1. Read this resume prompt.
2. Read `memory/project/selfdogfood_friction_log_v1_2_0_2026-04-17.md` (especially Meta-findings + "v1.2.1 priorities" table).
3. Read `memory/project/session_v1_2_0_selfdogfood.md` (context + self-rating).
4. Read `research/sota/v2_promptor_fusion_landscape_2026-04-17.md` (v2 landscape).
5. Ask user the 3 open questions above.
6. Open a NEW worktree `.claude/worktrees/fix_2026-04-1X_v1.2.1-structural-fixes/` and start with F29 (highest-leverage: fixing it unblocks every personal-scope install on the planet).

## Phrase to paste at v1.2.1 open

    Je reviens du selfdogfood v1.2.0. 13 frictions capturees (F20-F33).
    Pepites: F29 (plugin personal-scope install broken) + correction Promptor
    (Genesis-native, pas publie). Lis le friction log + session memory + research
    cache, puis on attaque v1.2.1 : P0 = F29 + F30 + F23/F27 paradox guards.
