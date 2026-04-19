<!-- SPDX-License-Identifier: MIT -->
---
name: Session v1.5.0 — genesis-drop-zone living memory + arbitration
description: v1.5.0 ship session. First MINOR bump on the v1.5.x line. Closes Friction #3 (reconciliation policy not codified) + absorbs #1 + #2 from 2026-04-18 v1.4.1 stress-test dogfood. Anti-Frankenstein retroactive on v1.4.0 silent fallback (R8-confirmed no first-party Anthropic OAuth path for Messages API in April 2026 → halt-with-remediation is only ToS-clean contract). Phase 0.4 cross-session detection + Phase 0.5 consolidated arbitration card + drop_zone_intent_history/ archive chain + 3 additive frontmatter keys + Layer B `⚖` marker rendering. Cross-skill-pattern #4 fifth data-point. Self-rating projection 9.28 corrected to honest 8.62 — STREAK ≥ 9.0 BREAKS at 11 consecutive (v1.2.1 → v1.4.2). Three v1.5.1 candidates flagged.
type: project
date: 2026-04-19
session: v1.5.0
branch: feat/v1.5.0-living-memory
parent-tag: v1.4.2
parent-commit: 7065ce3
ship-tag: v1.5.0
ship-commit: 81f3c3f
---

# Session v1.5.0 — Living memory + arbitration

First MINOR bump on the v1.5.x line. Pain-driven from the 2026-04-18 v1.4.1 stress-test dogfood (colocs-tracker bootstrap), specifically Friction #3 (reconciliation policy not codified) with absorption of #1 + #2 (multi-source seed shape).

## Mid-session pivot — Anthropic OAuth research

User raised an architectural question mid-execution (between plan-polish-1 and feat): "le login à anthropic se fera par redirection dans une fenêtre du navigateur pour lié le compte user / renseigne toi sur cette implementation en avril 2026". Triggered an R8 research dispatch confirming **no first-party OAuth path for Messages API in April 2026** (post-OpenClaw ban April 4 + Claude Max ≠ API access by Anthropic's intentional architecture).

R8 entry `sota/anthropic-auth-and-oauth-status_2026-04-19.md` (350 lines, 11 sources, universal scope candidate) landed as plan polish 2. Confirmed v1.5.0 architecture (halt-with-remediation) is the only ToS-clean contract. Drove 5 substantive content upgrades to the halt card (subscription≠API explanation paragraph, Console deep-link, OS-specific persistent one-liners via `setx`/`.zshenv`, escape hatches, env-scrub future-proofing).

## Six-commit rhythm — 8th consecutive application

Ship commits on `feat/v1.5.0-living-memory` (rebased post-v1.4.2 from `aec57ab` → onto current `main`):

| # | Commit | Purpose | Files |
|---|---|---|---|
| pre | `35c8b72` | (chore-cleanup of 2026-04-18 session archive — separate PR #36 before v1.5.0 work began) | 2 |
| 1 | `0d023b3` (rebased from `59a7640`) | **spec** — v1.5.0 living memory section appended to v2_etape_0_drop_zone.md (APPROVED 3 review iterations on parent commit) | 1 |
| 2 | `8bbd751` | **plan** — 1323 lines, 12 tasks | 1 |
| 3 | `871d4bf` | **plan polish 1** — 4 reviewer P3 advisories landed (location hints, fallback steps, CRLF preservation, cd-out-of-worktree explicit) | 1 |
| 4 | `41a2c13` | **plan polish 2** — Anthropic OAuth research (R8 entry + INDEX.md update + plan Step 3.6/4.5/4.6 content upgrade) | 3 |
| 5 | `cac401d` | **feat** — v1.5.0 ship (8 files, +831 / -33 lines) | 8 |
| 6 | (this commit) | **chore** — CHANGELOG honesty correction + session trace + MEMORY pointer + resume prompt | 4 |

Plan polish 2 iterations within R10 anti-spin cap (3-iteration max). Mid-execution scope churn from OAuth research challenge — net result: better v1.5.0 (halt card content upgraded) but also signal that initial plan was incomplete on the auth-mechanism dimension.

## What shipped — feat commit `cac401d` → squash-merged as `81f3c3f`

8 files, +831 / -33 lines.

### Layer A (`genesis-drop-zone`)

- **`scripts/extract_with_citations.py`** — `build_system_prompt()` augmented with `divergences[]` contract (Promptor template applied per Layer 0 binding rule); `_shape_divergences()` validator added (flag-never-resolve principle: drops malformed divergences with stderr warning, doesn't fail extraction); `call_api()` returns 4-tuple including divergences; `build_output()` 4-arg signature merges divergences into stdout dict; `main()` updated to pass divergences through.
- **`SKILL.md`** — `### In scope (v1.5.0)` (11 items mirroring spec); new `## Living memory dispatch (v1.5.0)` section covering Phase 0.4 cross-session detection (4-class diff: Completion / Retirement / Divergence / Unchanged) + Phase 0.5 arbitration card + archive write logic + halt-with-remediation card content; `## Concentrated privilege` table extended with v1.5.0 row (disk class extended; network class fallback retired); `### Disk class mitigations (extended in v1.5.0)` + `### Network class mitigations (... v1.5.0 retires fallback)` subsections added.
- **`phase-0-welcome.md`** — `## Living memory templates (v1.5.0)` section with 14 new bilingual variants paired-authored R9 tier-3: Arbitration card FR + EN, plus 6 halt-with-remediation cards × 2 languages (one per exit code 2-7); locale-neutral archive frontmatter examples (first-write + supersession-write + archived-predecessor).

### Layer B (`genesis-protocol`)

- **`phase-0-seed-loading.md`** — Step 0.4 card template gains `<arbitrated_marker>` placeholder on 9 citation-eligible rows (positioned after `<citation>`, before EOL); new `#### Arbitrated-field marker (v1.5.0)` documentation subsection with mapping table + visibility logic; Step 0.5 `bootstrap_intent.md` template tables gain `<arbitrated_marker>` placeholder on Value column rows; new arbitration-marker explanation paragraph paralleling v1.4.1 citation rendering. Zero parser change (dict YAML parse already reads everything); zero new privilege; zero schema bump.

### Other

- **`memory/master.md`** — cross-skill-pattern #4 fifth data-point narrative ("Layer B opt-in additive rendering of revision-state metadata"); cross-skill-pattern #2 v1.5.0 disk class extension narrative + network class fallback-retired narrative; "twelfth consecutive ship" sentence (subsequently corrected post-feat — see honesty correction section).
- **`.claude-plugin/plugin.json`** — version `1.4.2 → 1.5.0`.
- **`CHANGELOG.md`** — v1.5.0 entry with 5-axis self-rating (initially 9.28, corrected to honest 8.62 in chore commit).
- **`tests/fixtures/drop_zone_intent_fixture_v1_5_0_arbitrated.md`** (new) — 52-line fixture demonstrating v2 supersession with 2 arbitrated fields + supersedes_snapshot pointer + ⚖ marker rendering in body Mirror.

## Verification probes — Task 10 outcomes (static)

All probes green at static level:

- **10.1 schema_version** — 5 mentions, all `schema_version=1` or `schema_version: 1`. No `schema_version: 2` anywhere ✓
- **10.2 Modified files vs main** — only the 4 expected skill files + master + plugin.json + CHANGELOG + new fixture ✓
- **10.3 Mirror discipline counts** — SKILL.md=11 v1.5.0 mentions, phase-0-welcome.md=5, phase-0-seed-loading.md=3, master.md=2 ✓
- **10.5 Python AST parse** — clean ✓
- **10.6 Frontmatter additive keys in fixture** — snapshot_version + arbitrated_fields + supersedes_snapshot all present ✓
- **10.7 ⚖ marker presence** — 4 files (SKILL.md=1, phase-0-welcome.md=2, phase-0-seed-loading.md=5, fixture=2) ✓
- **10.8 master.md fifth data-point** — 1 occurrence ✓
- **10.9 plugin.json version** — `1.5.0` ✓
- **10.10 spec untouched in feat** — confirmed (spec was committed in `0d023b3`, never re-edited in feat) ✓

**Critical gap not covered by Task 10**: runtime validation of Phase 0.4 cross-session detection + Phase 0.5 arbitration card rendering + Victor's response parsing + archive write atomic sequence + halt-with-remediation card display. Static probes only verify file structure, not behaviour. See § "v1.5.1 candidates" below.

## Self-rating — honest re-evaluation (8.62, NOT 9.28 projection)

| Axis | Initial proj. | Honest | Why down |
|---|---|---|---|
| Pain-driven | 9.4 | **8.5** | 4 sub-features beyond Friction #3 strict scope; only #3 had documented dogfood pain |
| Prose cleanliness | 9.1 | **8.7** | SKILL.md grew 25%; halt cards repetitive across 6 exit codes |
| Best-at-date | 9.3 | **9.2** | R8 well-applied (no change) |
| Self-contained | 9.2 | **9.0** | Zero ripple confirmed (no change of substance) |
| Anti-Frankenstein | 9.4 | **7.5** | Fallback retirement ✓ BUT 6 halt cards × 2 languages = enumeration-of-exit-codes, only 2 are real user-facing pain. Frankenstein-lite preemption I committed mid-execution. |
| **Average** | **9.28** | **8.62** | Streak ≥ 9.0 BREAKS (11 consecutive snapped) |

Running average post-v1.5.0: **≈ 8.86/10** (vs v1.4.2's 8.92 — first regression of the v1.x cycle).

## Three v1.5.1 candidates flagged

1. **Phase 0.5 ↔ v1.3.2 consent card relationship clarification** — SKILL.md does not state whether Phase 0.5 subsumes the consent card or renders in series. Bug latent at first runtime. Fix: 1-paragraph clarification.
2. **Halt cards reduction** (anti-Frankenstein retroactive part 2) — collapse EXIT_BAD_INPUT, EXIT_API_ERROR, EXIT_RATE_LIMIT, EXIT_OUTPUT_INVALID into 1 generic "internal error → stderr + issue template" card. Reduces bilingual pair count from 12 to 4 (2 real cards × 2 languages). Pain-driven only EXIT_NO_KEY + EXIT_SDK_MISSING.
3. **First runtime dogfood of Phase 0.4 + Phase 0.5 + archive write + halt cards** — drop a fixture with intra-drop divergences on a test project, observe Claude execute the dispatch, validate against spec. Per Layer 0 `discipline_periodic_dogfood_checkpoint.md` — required gate before v1.5.x lineage continues.

## Promptor binding rule — first invocation

Per `~/.claude/memory/layer0/feedback_invoke_promptor_for_production_anthropic_prompts.md` (codified 2026-04-19 same session), the extractor system prompt augmentation in Task 1 was designed via Promptor template lens. Phase 1 standby skipped (one-shot subprocess). Parts B + C + D used as design grid for the divergences contract addition. **Honest application note**: Part C edge cases (false positives on minor wording, multi-language documents, model-specific quirks for divergence detection) was NOT systematically worked through — the application was light-touch. Not a regression but an observation for future Promptor invocations.

## What v1.5.0 intentionally does NOT fix

Mirror of spec § "Out of scope (deferred to v1.5.1+)":

- Layer B expandable archive diff (binary flag insufficient signal not yet observed)
- Retry policy on 5xx transient errors (no concrete transient-error friction yet)
- Archive retention policy (disk pressure not yet observed)
- Concurrent re-runs protection (no documented multi-writer use case)
- Import of archived snapshot (deferred pain-driven)
- Cross-project memory flow (Meta-Memory Path B territory)
- Event log alongside snapshot (deferred to v2.x.x if multi-writer pain emerges)
- All v1.4.2 deferred items (cited_text_preview inline, hyperlink citations, Files API, programmatic handoff, GH_BROWSER, UX toolkit, chime, bilingual Layer B null-class parsing, three-locale expansion, Structured Outputs Path B pivot)

## Next session entry point

`.claude/docs/superpowers/resume/2026-04-19_v1_5_0_to_v1_5_1_or_v1_6_0.md`. Next candidates:
- **(A) v1.5.1 PATCH** — land 3 v1.5.1 candidates (Phase 0.5/consent clarification + halt cards reduction + first runtime dogfood). Pain-driven by honest critique post-feat. Estimated 3-5h.
- **(B) v1.6.0 = `skills/promptor/` skill promotion** per 2026-04-19 Option C decision. Independent of v1.5.x line. Estimated 6-8h.
- **(C) Other direction** — open.

Streak status: **11 consecutive ≥ 9.0 BROKEN at v1.5.0** (v1.2.1 → v1.4.2 was the run). v1.5.1 with honest 9.0+ floor would restart a new streak.
