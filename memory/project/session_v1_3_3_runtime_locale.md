<!-- SPDX-License-Identifier: MIT -->
---
name: Session v1.3.3 — genesis-drop-zone runtime locale rendering
description: v1.3.3 ship session. Runtime locale dispatch across seven Layer A user-facing surfaces via two variables (welcome_locale set at invocation from trigger phrase language; content_locale set after content from langue_detectee). Closes R9 tier-3 rendering loop end-to-end. Zero Layer B ripple by design — frontmatter null-class tokens stay FR canonical (documented Layer A / Layer B asymmetry). One PR, one skill touched. Six-commit rhythm held (spec + spec polish + plan + plan polish + feat + chore) for fourth consecutive time.
type: project
date: 2026-04-18
session: v1.3.3
branch: feat/v1.3.3-runtime-locale
parent-tag: v1.3.2
parent-commit: c2dc771
---

# Session v1.3.3 — runtime locale rendering

Follow-up to v1.3.2 (merged PR #30, tagged v1.3.2 on 06ccce9). Candidate B from the v1.3.2 → v1.3.3 resume prompt, picked after reviewing A (Citations API) / B (runtime locale) / C (UX toolkit) trade-offs: B was the cleanest next structural closer — small scope, closes a concrete R9 tier-3 gap end-to-end, all EN templates pre-authored across v1.3.0 / v1.3.1 / v1.3.2. A = v1.3.4 candidate (bigger, second privilege class). C = v1.3.5 (polish on surface that must render in detected locale first).

## What shipped

Six commits on `feat/v1.3.3-runtime-locale` off `c2dc771`:

| # | Commit | Purpose | Files |
|---|---|---|---|
| 1 | `7f85484` | **spec** — extend `v2_etape_0_drop_zone.md` with `## Scope — v1.3.3 runtime locale rendering` + new design section `## Runtime locale — signal + dispatch (v1.3.3)` (two-variable table + render targets + divergence rules + frontmatter-contract-unchanged note). Consent card / halt / accept bridge / decline bridge / drop_zone_intent.md sections updated inline with locale-switched subsections. 1:1 mirror map + R9 language policy table extended. Deferred renamed to v1.3.4+; runtime locale removed (closed). Verification scenarios #20-27 new. `## Rationale for v1.3.3 route` section added. +255/-45. | 1 |
| 2 | `8591914` | **spec polish** — 3 advisories from spec-document-reviewer: (1) frontmatter header stale (target_version / description / updated_at didn't reflect v1.3.3); (2) extraction schema `langue_detectee` row claimed "does not switch mirror rendering" — contradicted new v1.3.3 dispatch section; (3) v1.3.0/1.3.1 regression scenarios #5 / #9 / #10 expected-outcome text not updated while ship gate claimed they were. All three fixed. +7/-7. | 1 |
| 3 | `7dabae5` | **plan** — 12-task implementation plan. Design decisions + file change map + task-by-task breakdown with per-step verification probes. Mirrors v1.3.2 plan discipline (Python portability `$(command -v python \|\| command -v python3 \|\| command -v py)`, local-branch-name confirmation before push). 262 lines. | 1 |
| 4 | `4b2716a` | **plan polish** — 3 advisories from plan-document-reviewer: (1) Task 4 grep count probes under-specified (changed to exact-equal counts: welcome_locale = 4, content_locale = 10); (2) Task 5 Step 3 FR-canonical-null-token probe too loose (replaced with three exact-count probes including negative probe `"not mentioned" = 0`); (3) Task 9 missing welcome-box ASCII purity regression probe after header rewrites (added box frame intactness + non-ASCII leakage checks). +9/-3. | 1 |
| 5 | `f79b874` | **feat** — v1.3.3 ship. skills/genesis-drop-zone/SKILL.md adds `## Locale dispatch (v1.3.3)` top-level section, `### In scope (v1.3.3)` + `### Out of scope (deferred to v1.3.4+)` sub-blocks, inline v1.3.3 dispatch notes on Phase 0 sections, privilege map v1.3.3 qualifier, schema skill_version updated to 1.3.3. skills/genesis-drop-zone/phase-0-welcome.md rewrites section headers with render conditions (`welcome_locale` x4, `content_locale` x10), splits v1.3.2 always-bilingual consent card + halt + accept bridge + decline bridge into FR variant + EN variant sub-blocks, adds newly-authored EN zero-content re-prompt `I'm listening — drop or write whatever you want to share.`. New tests/fixtures/drop_zone_intent_fixture_v1_3_3_en.md (EN body + FR canonical null tokens). memory/master.md privilege map v1.3.3 line + cross-skill-pattern #4 zero-ripple discipline note. .claude-plugin/plugin.json 1.3.2 → 1.3.3. .claude/docs/superpowers/research/INDEX.md hygiene fix (missing v2_promptor_fusion row caught at R1.1). +200/-55 across 6 files. | 6 |
| 6 | (chore, pending) | **chore** — CHANGELOG v1.3.3 + this session trace + MEMORY.md pointer + resume prompt v1.3.3 → v1.3.4. | 4 |

## Why spec + plan written ahead (six-commit rhythm)

Fourth consecutive application of the v1.2.1 → v1.3.2 discipline — spec and plan are first-class artefacts with their own reviewer loops. Six-commit rhythm (spec + spec polish + plan + plan polish + feat + chore) now runs at full discipline for v1.3.0 / v1.3.1 / v1.3.2 / v1.3.3. Living-spec pattern continues with `v2_etape_0_drop_zone.md` — one canonical vein-of-truth across four version-scoped sections (v1.3.0 welcome + v1.3.1 extraction + v1.3.2 write + Layer B + v1.3.3 runtime locale).

## Verification walk-throughs

Ship gate declared #20 (FR intent + EN content), #21 (EN intent + FR content), #25 (EN body write), #26 (R9 audit new EN re-prompt), #27 (Layer B zero-ripple regression) mandatory, plus regressions on v1.3.2 #15 / #16 / #17 and v1.3.1 #9. Outcome:

### Scenario #20 + #21 + #22 + #23 + #24 — locale dispatch bidirectional divergence + tiebreaker + slash degradation + zero-content — PASS

`## Locale dispatch (v1.3.3)` section present in SKILL.md (grep count 1). Section documents both `welcome_locale` and `content_locale` signal sources, render targets, divergence behaviour, mixte → FR tiebreaker, slash → FR default, zero-content welcome_locale, modification-loop re-evaluation.

### Scenario #25 — EN body write (artefact-level) — PASS

Synthetic fixture `tests/fixtures/drop_zone_intent_fixture_v1_3_3_en.md` parses cleanly against the 13-key expected schema via Python `yaml.safe_load`. Frontmatter: `langue_detectee: "EN"`, `skill_version: "1.3.3"`. Body contains EN prose intro `Intent captured at the drop zone on 2026-04-18` + EN mirror echo inside code fence. Null-class tokens FR canonical: `"non mentionne"` x2 (budget + tech), `"non mentionnee"` x1 (visibility), `"a trouver ensemble"` x1 (nom). Negative probe `"not mentioned"` = 0 (no EN leakage into frontmatter).

### Scenario #26 — R9 audit newly-authored EN re-prompt — PASS

`grep "I'm listening — drop or write whatever you want to share\." phase-0-welcome.md` = 1. FR companion `Je t'écoute — dépose ou écris ce que tu veux me partager.` = 1. Both present exactly once.

### Scenario #27 — Layer B zero-ripple regression — PASS

`git diff main -- skills/genesis-protocol/` returns empty — Layer B files completely untouched by v1.3.3. Layer B parser at Step 0.2a reads FR canonical null-class tokens the same way it did in v1.3.2; the EN fixture from #25 parses identically to the FR fixture, confirming the asymmetry contract.

### Task 4 grep counts — PASS

`grep -c "rendered when welcome_locale" phase-0-welcome.md` = 4 (matches plan exact-count expectation — welcome box FR + welcome box EN + zero-content re-prompt FR + zero-content re-prompt EN).

`grep -c "rendered when content_locale" phase-0-welcome.md` = 10 (matches plan exact-count expectation — 5 surfaces × 2 variants: mirror, consent card, halt, accept bridge, decline bridge).

### Welcome-box ASCII purity regression (plan advisory #3) — PASS

Python-portable probe extracted lines between `┌` and `└` box frames, checked each character code point, allowed em-dash (U+2014) as the pre-existing v1.3.0 exception. Zero unexpected non-ASCII characters leaked into box content during Task 4 header rewrites.

### Regression #15 (halt branch) — PASS

Halt message split into FR variant + EN variant with render conditions in `phase-0-welcome.md`. SKILL.md halt section retitled `## Phase 0 — halt branch (v1.3.2, v1.3.3 locale-switched)` with dispatch note referencing the locale dispatch section.

### Regression #16 (modification loop) — PASS

SKILL.md `## Phase 0 — consent card (v1.3.2, v1.3.3 locale-switched)` notes `content_locale` re-evaluation on each modification re-extraction; if correction shifts `langue_detectee`, re-printed consent card switches locale.

### Regression #17 (R9 audit on written file) — PASS

FR canonical null tokens preserved in fixture frontmatter despite EN body (the key v1.3.3 asymmetry). Body mirror echo is ASCII-pure inside code fence (same accent discipline as v1.3.0).

### Regression #9 (zero-content branch) — PASS

Both FR and EN re-prompt variants present in `phase-0-welcome.md § "Zero-content branch (v1.3.0 preserved, v1.3.3 locale-switched)"`. Dispatch on `welcome_locale` documented (content extraction not yet run at this point).

### plugin.json sanity — PASS

Version `1.3.3` on plugin.json line 3.

### master.md freshness — PASS

Privilege map entry for `genesis-drop-zone` updated with v1.3.3 qualifier. Cross-skill-pattern #4 carries v1.3.3 zero-Layer-B-ripple discipline note with cross-reference for future Layer A rendering polish.

### INDEX.md hygiene — PASS

`v2_promptor_fusion_landscape_2026-04-17.md` row added to `## Active` table. Previously the entry existed on disk under `research/sota/` but the INDEX was not updated when the entry was created — caught during R1.1 open-ritual scan at session open, landed in this feat commit.

### Runtime replay note — deferred as before

Runtime replay of #20, #21, #23, #24 (all locale-dispatch scenarios) requires a fresh Claude Code process in an empty directory — not executable from inside this session. Artefact-level verification is the ship gate; runtime replay is observability-track, not merge-blocker. Consistent −0.2 Pain-driven deduction applies per replay-deferred scenario and rolls forward (same convention as v1.3.1 / v1.3.2).

## What v1.3.3 intentionally does NOT fix

Mirror of the spec § "Deferred to v1.3.4+" and SKILL.md § "Deferred scope":

1. **Path A Citations API upgrade** — second privilege class (network vs disk), `cited_text` + `document_index` audit-trail. Downstream reader now in place since v1.3.2. **v1.3.4 candidate.**
2. Programmatic handoff — auto-invoke `genesis-protocol` without the user typing the slash command.
3. `GH_BROWSER` profile routing wire-up.
4. UX toolkit integration (@clack/prompts, Charm Gum, cli-spinners).
5. Completion chime (cross-platform).
6. Error handling refinements (permission-denied / disk-full / symlink edge cases).
7. **Bilingual Layer B null-class parsing** — v1.4+ target if real pain emerges.
8. **Three-locale-or-more expansion** — deferred until non-FR/EN user emerges.

## Self-rating — v1.3.3

See CHANGELOG for the 5-axis table. Summary:

| Axis | Score |
|---|---|
| Pain-driven | 9.3 |
| Prose cleanliness | 9.2 |
| Best-at-date | 9.2 |
| Self-contained | 9.4 |
| Anti-Frankenstein | 9.4 |
| **Average** | **9.30** |

Target ≥9.3 per axis met on 4/5; floor ≥9.0 respected on every axis. **Eighth consecutive ship ≥ 9.0** (v1.2.1 9.26, v1.2.2 9.14, v1.2.3 9.18, v1.2.4 9.16, v1.3.0 9.34, v1.3.1 9.30, v1.3.2 9.28, v1.3.3 9.30). Best-at-date holds at 9.2 (Citations API still the structural lever; R8 entry `v2_promptor_fusion_landscape_2026-04-17.md` not stale — expires 2026-04-24).

## Running average post-v1.3.3

v0.2 → v1.3.2 running average was ~8.84 across 18 tagged ships. v1.3.3 at 9.30 brings the running average to **≈ 8.87/10** (+0.03). Above v1.0.0 target of 8.5 by 0.37. Plateau holds inside the anti-Frankenstein inflection-point budget (no single axis hits 9.5).

## P1 queue status

Closed at both bootstrap (v1.2.3) and downstream-rule (v1.2.4) levels. v1.3.x is a feature-line ship cycle. v1.3.0 opened it, v1.3.1 structured the mirror, v1.3.2 closed the write + Layer B wire, v1.3.3 closed the R9 tier-3 rendering loop. v1.3.4+ remains refinement (Citations, programmatic handoff, UX toolkit, chime, error-handling).

## Next session entry point

`.claude/docs/superpowers/resume/2026-04-18_v1_3_3_to_v1_3_4.md` (written as part of the chore commit). Resume prompt frames v1.3.4 with three candidate directions — A Citations API upgrade (now-unfrozen second privilege class), B UX toolkit polish, C error-handling refinements.

The `v2_promptor_fusion_landscape_2026-04-17.md` R8 entry remains fresh (expires 2026-04-24), ~6 days of runway after v1.3.3 ship.
