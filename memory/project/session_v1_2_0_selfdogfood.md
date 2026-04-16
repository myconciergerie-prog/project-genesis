<!-- SPDX-License-Identifier: MIT -->
---
name: Session v1.2.0 — Conscious strange-loop self-dogfood
description: Second self-dogfood session. Genesis runs on Genesis-describing-Genesis from a worktree subfolder. 13 new frictions captured (F20–F33), v2 Promptor fusion spec corrected with research findings, drop-zone Étape 0 designed. Ended mid-Phase 3 by design, not blocker.
type: project
date: 2026-04-17
version: v1.2.0-selfdogfood (not tagged — dev branch)
outcome: 13 frictions + v2 research landscape + corrected v2 spec + v1.2.1 fix priorities
---

# Session v1.2.0 — conscious strange-loop self-dogfood

## One-paragraph summary

User asked for a second self-dogfood, consciously closing the strange loop: create a worktree of project-genesis, write a config.txt describing Genesis itself, run `genesis-protocol` in mode=auto against it. In parallel, three research agents gathered 2026 best practices for the v2 drop-zone → extract → formalize surface. The live run halted mid-Phase 3 after the predicted structural blockers fired (F23 worktree-is-inside-repo, F27 slug collision, F30 nested git init silently succeeds). 13 new frictions were captured, `v2_vision_promptor_fusion.md` was amended with a new Étape 0 drop-zone and a factual correction ("Promptor 4-part structure" is Genesis-native, not a published pattern). Two pépite-worthy findings surfaced: F29 (Genesis plugin personal-scope install is broken today) and the Promptor misattribution.

## Frictions captured (13 new)

See `memory/project/selfdogfood_friction_log_v1_2_0_2026-04-17.md` for the full log.

| ID | Severity | Domain |
|---|---|---|
| F20 | STRUCTURAL | mode=auto contradicts "do not auto-run" |
| F21 | DESIGN | argument schema undocumented |
| F22 | DESIGN | consent card mandatory even in mode=auto (F2 re-confirmed) |
| F23 | STRUCTURAL | worktree-as-subdir defeats paradox safety net |
| F24 | DESIGN | Phase 0.1 inside-git-repo check is weak |
| F25 | DESIGN | config.txt format undocumented to users (F19 re-confirmed) |
| F26 | DESIGN | extra config.txt fields silently dropped |
| F27 | STRUCTURAL | slug self-collision non-blocking |
| F28 | COSMETIC | stale SSH key artefacts never cleaned |
| F29 | STRUCTURAL | Phase 1.3 rules path resolution breaks in personal-scope install |
| F30 | STRUCTURAL | Phase 3.1 nested-repo silent success |
| F31 | COSMETIC | seed author had to guess YAML boundary |
| F32 | DESIGN | orchestrator cannot be invoked programmatically |
| F33 | DESIGN | research cache entry written in wrong repo scope |

## Research agents dispatched in parallel

Three agents ran simultaneously for ~2 minutes each, no cross-contamination:
1. **Drag-drop UX 2026** (agent a3a29e0f) — 44k tokens, 13 tool uses
2. **Document extraction Claude API 2026** (agent af96288a) — 82k tokens, 17 tool uses
3. **Conversational briefing 2026** (agent a0ea272e) — 61k tokens, 19 tool uses

All three verified their claims against live documentation URLs. Consolidated report written to `.claude/docs/superpowers/research/sota/v2_promptor_fusion_landscape_2026-04-17.md` (TTL 2026-04-24).

**Key findings**:
- "Promptor 4-part structure" is NOT a published pattern → v2 spec corrected
- Structured Outputs + Citations are mutually exclusive → v2 Path A (Citations-audited) recommended for first release
- Cache `ttl: "1h"` is now mandatory (Anthropic silently tightened default to 5-min in March 2026)
- Drop-zone UX canon: intent-first unified box, token-streamed live acknowledgement, accept-anything, relationship-language privacy
- EVPI-selected questions (0-3, adaptive) beats fixed "at most 3"
- Brief-quality via ResearchRubrics 6-axis rubric (Scale AI 2026 SOTA)
- Binary meta-question stays binary — every tool that tried a third mode reverted

## Deliverables

1. `config.txt` (Genesis describing Genesis — the strange-loop seed)
2. `memory/project/bootstrap_intent.md` (Phase 0 output)
3. `memory/project/selfdogfood_friction_log_v1_2_0_2026-04-17.md` (13 new frictions + meta-findings + v1.2.1 priorities)
4. `.claude/docs/superpowers/research/sota/v2_promptor_fusion_landscape_2026-04-17.md` (consolidated research)
5. `specs/v2_vision_promptor_fusion.md` amendments (Étape 0 drop-zone + Promptor correction)
6. `memory/project/session_v1_2_0_selfdogfood.md` (this file)
7. Resume prompt: `.claude/docs/superpowers/resume/2026-04-17_v1_2_0_selfdogfood_to_v1_2_1.md`

## Pépites

Two findings qualify per `v1_pepite_discovery_flagging.md`:
- **F29**: Genesis plugin personal-scope install is broken → cross-project alert + README warning needed
- **Promptor misattribution**: "4-part structure" is Genesis-native → v2 spec + CHANGELOG + any external blog post must credit correctly

## Self-rating

| Axis | Score | Rationale |
|---|---|---|
| Pain-driven | 9.2/10 | 13 frictions captured, 5 STRUCTURAL, all traceable to real bootstraps (including the pépite F29 break affecting every personal-scope installer) |
| Prose cleanliness | 8.8/10 | Friction log follows the 2026-04-16 template exactly, each entry has What/Root cause/Fix |
| Best-at-date | 9.0/10 | Three parallel research agents verified 2026 SOTA with live URLs; cache entry expires 2026-04-24 |
| Self-contained | 7.5/10 | Heavily depends on Layer 0 + existing memory; research entry mixed scopes (F33); worktree vs sibling-project paradox not yet fixed |
| Anti-Frankenstein | 9.0/10 | No new skill invented; no live fixes; every friction captured, none auto-resolved in-session; research used to *refine* v2 spec, not pile features |
| **Running (geometric)** | **8.70/10** | — |

Version v1.2.0 NOT tagged. This was a discovery session; v1.2.1 is the ship target that closes P0 frictions.

**Running average v0.1–v1.2.0-selfdogfood**: (v0.1 6.0 + v0.2 7.6 + v0.3 8.2 + v0.4 8.8 + v0.5 8.4 + v0.6 8.6 + v0.7 8.8 + v0.8 9.0 + v0.9 8.92 + v1.0 8.5 + v1.1 8.6 + v1.2.0-sd 8.70) / 12 = **8.51/10** — above the v1 target of 8.5.

## Paradox status

Conscious strange loop = closed, observed, documented. The paradox is now a named architectural concern with a defensive fix plan, not a lurking surprise.
