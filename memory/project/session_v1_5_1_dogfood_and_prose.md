<!-- SPDX-License-Identifier: MIT -->
---
name: Session v1.5.1 dogfood + prose — 2026-04-19
description: First PATCH on v1.5.x line. Dogfood-first ordering (3→1→2) closes v1.5.0's three-gap honesty correction (8.62 broken-at-11-streak). Dogfood surfaced 2 blocker frictions + 3 structural + 1 polish + 1 deferred — driving Candidate 1 scope expansion in-feat (v1.4.0 retirement propagation across SKILL.md) and Candidate 2 floor drop to 4 halt-card variants. Code-reviewer pre-commit caught 3rd latent collision (v1.3.2 halt-on-existing vs v1.5.0 re-run archive). v1.5.1 tagged at 9.12/10 honest — new streak ≥ 9.0 starts at 1.
type: project
version: v1.5.1
pr: "#39"
merge_commit: eba3e46
tag: v1.5.1
predecessor: v1.5.0 (81f3c3f)
---

# Session v1.5.1 — Dogfood + prose corrections — 2026-04-19

## What shipped

**Tag v1.5.1** (PR #39 squash-merged as `eba3e46`). **PATCH** — first correction on the v1.5.x line after v1.5.0's 2026-04-19 honesty correction broke the 11-ship ≥ 9.0 streak at 8.62.

- **Feat commit `6dce8fa`** — 3 files, **+91 / −274 lines** (net negative = anti-Frankenstein):
  - `skills/genesis-drop-zone/SKILL.md` — new `### Consent-card interaction with Phase 0.5 (v1.5.1 clarification)` subsection with three-path contract (Path 1 non-empty divergences + Path 2a first-write empty + Path 2b re-run empty + Path 3 halt). Phase 0.5 empty-divergences wording bifurcates on write mechanism. v1.4.0 fallback retirement propagated (9 banner/footnote edits). Halt table 6 rows → 2 rows.
  - `skills/genesis-drop-zone/phase-0-welcome.md` — 10 bilingual halt-card variants deleted (EXIT_SDK_MISSING / API_ERROR / RATE_LIMIT / BAD_INPUT / OUTPUT_INVALID × FR + EN). 2 new variants added for generic internal-error card (FR + EN). Net final: 4 variants (2 cards × 2 langs).
  - `.claude-plugin/plugin.json` — version `1.5.0 → 1.5.1`.
- **Archive commit `5c68f20`** — 1 file, +194 lines. Dogfood friction log for 4 fixtures at `C:/tmp/genesis-v1.5.0-dryrun/` with 7 frictions + hypothesis-bearing analysis + blocker triage decision.
- **Plan commit `e2b7197`** — 1 file, +198 lines. Reviewer-landed P1s: R2.3.1 double pre-flight + api-key-absent branch logic + reviewer-P0 loopback rule + blocker-halt rule in archive template + H2 coverage protocol + Fixture D throwaway venv.
- **Spec commit `84048ef`** — 1 file, +184 lines. Reviewer-landed P1s: [A1] zero-friction branch explicit + Appendix A pre-registration + Candidate 2 floor two-way rule + Fixture D for EXIT_SDK_MISSING runtime coverage + timebox-exceeded rule + blocker/structural/polish taxonomy.
- **Chore commit** (this commit) — CHANGELOG honest v1.5.1 entry + MEMORY pointer + session trace + resume.

## Why — three-gap honesty correction from v1.5.0

v1.5.0 shipped 2026-04-19 as MINOR living-memory + arbitration. Post-feat honesty correction dropped self-rating from projected 9.28 to 8.62, breaking an 11-consecutive ≥ 9.0 streak (v1.2.1 → v1.4.2). The correction surfaced three substantive issues:

1. **Zero runtime validation** of Phase 0.4 / Phase 0.5 / archive write / halt cards. Verification was static-structure only (grep, JSON parse). No execution. Per Layer 0 `discipline_periodic_dogfood_checkpoint.md`, a known gap.
2. **12 halt-with-remediation cards** (6 distinct × 2 langs) = enumeration-of-exit-codes Frankenstein-lite. Only EXIT_NO_KEY + EXIT_SDK_MISSING address real user-facing pain. Exits 4-7 hit ~0% of real users.
3. **Phase 0.5 ↔ v1.3.2 consent card relationship ambiguous** in SKILL.md. Empty-divergences path silently bypasses consent — latent bug at first runtime execution.

These three mapped 1:1 to the three v1.5.1 candidates flagged in the 2026-04-19 resume.

## Discipline upgrade — dogfood-first ordering

The candidates were ordered 3 → 1 → 2 deliberately. Runtime evidence (Candidate 3) shapes the prose edits (Candidates 1 + 2) instead of the reverse. This reversed v1.5.0's preemptive-prose mistake at the process level.

Validation of the discipline by observed outcome:

- **If Candidates 1 + 2 had shipped before dogfood**: Friction #1 (v1.4.0 / v1.5.0 prose contradiction in the same file) would have been missed — Candidate 1 would have added the new subsection without propagating the v1.4.0 retirement banners, leaving SKILL.md still self-contradicting. Friction #6 (empty-divergences silent-skip of v1.3.2 consent card) would have been framed as a clarification-for-future-readers rather than a BLOCKER-severity bug actively violating the v1.3.2 privilege model. Candidate 2 would have preserved `EXIT_SDK_MISSING` as a distinct card on prose-only grounds (the pre-registered H3 hypothesis).
- **With Candidates 1 + 2 shaped by dogfood evidence**: scope expanded in-feat to propagate v1.4.0 retirement across 9 surfaces. Friction #6 prose commits Path 1/2a/2b/3 explicitly. `EXIT_SDK_MISSING` collapses into the generic internal-error card per Friction #4 (H3 refuted by evidence — runtime distinction operationally opaque within 2h timebox).

The dogfood-first ordering is now a named discipline for future PATCH work on recently-shipped skill surfaces. This session is the reference implementation.

## Code-reviewer caught a third latent bug pre-commit

After Candidate 1 edits landed but before feat commit, a code-reviewer agent pass surfaced a P0 collision that dogfood alone had missed: the new "fall through to v1.3.2 consent card + v1.3.2 write flow" wording inadvertently routed re-run empty-divergences paths into `## Phase 0 — write flow (v1.3.2)` whose Step 2 is a pre-write existence check that halts on existing `drop_zone_intent.md`. The v1.5.0 re-run contract requires archive + supersession, not halt.

Fix: Path 2 bifurcates into 2a (first-write, v1.3.2 write flow) and 2b (re-run, archive supersession chain). Both the Phase 0.5 empty-divergences paragraph (SKILL.md:348) and the Candidate 1 subsection Path 2 block (SKILL.md:~430) updated in the same feat commit.

This is the two-gate validation story: dogfood surfaces prose-level ambiguities; code-reviewer surfaces prose-level-contract collisions. Both needed — neither alone catches the other's class of bug.

## Scope expansion honesty

Candidate 1 grew from "add one subsection" (spec scope) to "subsection + v1.4.0 fallback retirement propagation + Modification-loop v1.4.0 paragraph rewrite + Path 2a/2b bifurcation" (feat scope). The spec explicitly permitted scope expansion for BLOCKER frictions via § Scope blocker taxonomy. Dogfood surfaced 2 blockers mapped to Candidate 1 — the expansion traces to evidence, not tidy-up.

Honest assessment of expansion honesty:
- Each individual edit is mechanical (grep-guided retirement banner + prose fix) — no new design decisions.
- Each edit directly addresses an observed friction (referenced in commit message + Candidate 1 subsection).
- No unrelated edits crept in (verified by grep: only `skills/genesis-drop-zone/` touched; Layer B zero-line diff; scripts zero-line diff).

Still counted as 0.2 deduction on Self-contained axis (9.3 vs 9.5 ceiling) because bundling scope-expansion in the same feat rather than separate PATCH stretched the PATCH tranche. An alternate framing (three separate PATCHes: v1.5.1 subsection + v1.5.2 retirement + v1.5.3 collapse) would have been more minimal-change, but would have deferred the blocker fixes that the v1.5.1 exists to close. The tradeoff was accepted with honesty.

## Hypothesis outcomes (spec Appendix A)

| Hypothesis | Pre-registered | Actual outcome | Evidence |
|---|---|---|---|
| H1 | Phase 0.5 SUBSUMES v1.3.2 consent on non-empty divergences; v1.3.2 consent renders on empty-divergences write; halt renders neither | **Confirmed in principle, BLOCKER in current prose** — Friction #6 showed v1.5.0 prose actively violated this. Candidate 1 fix: add three-path contract subsection + Path 2a/2b bifurcation after reviewer pass. |
| H2 | Byte-identical re-run may short-circuit overwrite | **Refined** — consent card ALWAYS renders on empty-divergences; short-circuit of overwrite is optional cosmetic optimization AFTER consent, deferred to v1.5.2+. |
| H3 | EXIT_SDK_MISSING stays distinct | **Refuted** — Friction #4 showed operational-opacity without runtime distinction; H3 collapsed to "EXIT_NO_KEY distinct, all other exits merged into generic internal-error". Final floor = 4 variants. |
| H4 | Extractor 6 distinct exit codes preserved | **Confirmed** — zero-line diff on `extract_with_citations.py`. Collapse is render-layer only. |

## Cross-skill-pattern data point

Cross-skill-pattern #4 (Layer A / Layer B stratification + zero-ripple principle) gains a **sixth data-point**: v1.5.1 Layer A-only correction with zero Layer B ripple. Previous data-points: v1.3.2 wire + v1.3.3 body-vs-frontmatter asymmetry + v1.4.0 additive keys + v1.4.1 additive rendering + v1.5.0 additive revision-state rendering + v1.5.1 Layer A-only corrections. The zero-ripple principle holds across Layer A growth, Layer A correction, AND Layer B opt-in rendering — three distinct extension modes, same invariant.

No narrative update to `master.md` needed — v1.5.1 touches no cross-skill pattern structurally. The data-point will be consolidated into master.md at the next minor/major bump if the pattern narrative needs refresh.

## Self-rating — honest post-feat (5-axis)

| Axis | Projected | Honest | Delta | Notes |
|---|---|---|---|---|
| Pain-driven | 9.5 | 9.4 | −0.1 | All candidates concrete; paper-trace method acknowledged explicitly in shipped prose. |
| Prose cleanliness | 9.3 | 9.0 | −0.3 | v1.4.0 retirement banners preserve history but increase SKILL.md cognitive load. Wholesale deletion would be cleaner; tradeoff accepted. |
| Best-at-date | 9.0 | 9.0 | 0.0 | Dogfood-first discipline SOTA-aligned per Layer 0. No new R8 research. |
| Self-contained | 9.3 | 9.3 | 0.0 | Zero ripple verified. Scope expansion contained to genesis-drop-zone. |
| Anti-Frankenstein | 9.0 | 9.0 | 0.0 | Net −10 bilingual variants. Third consecutive anti-Frankenstein retroactive. Bundling-scope-in-same-feat deduction already priced. |
| **Mean** | **9.22** | **9.12** | **−0.10** | **New streak ≥ 9.0 starts at 1.** |

Running average post-v1.5.1: ≈ **8.87/10** (+0.01 vs v1.5.0 running 8.86 — reverses the regression trend at the smallest possible increment, which matches PATCH tranche expectations).

## Follow-up candidates (for v1.5.2 or later)

- **Runtime (not paper-trace) dogfood** in a separate Claude Code session spawned per fixture cwd. Would validate H2 short-circuit + actually exercise dispatch against API-key-present paths. Requires user cooperation (spawn session in `C:/tmp/<fixture>/`) or CI scaffolding. v1.5.2+ candidate.
- **fsync-then-rename atomic archive write** — v1.5.0 accepted the small window. Still deferred. Would land in v1.5.2+ only if dogfood observes real failure.
- **Friction #3 retirement trigger semantics** — Phase 0.4 Retirement class triggers whenever a previously-populated field is not mentioned in new drop (null-visible default). Could flood the arbitration card on sparse drops. v1.5.2+ design work.
- **Friction #7 is_fresh_context dogfood method** — the paper-trace method worked but a README under `tests/` on "how to dogfood genesis-drop-zone at runtime" would help future sessions. v1.5.2+ polish.
- **v1.6.0 Promptor skill** — still queued per 2026-04-19 Option C decision. Independent of v1.5.x line.

## PR + tag state

- Branch `feat/v1.5.1-dogfood-and-prose` PR #39 squash-merged as `eba3e46`.
- Tag `v1.5.1` pushed.
- Worktree `C:/Dev/Claude_cowork/project-genesis/.claude/worktrees/v1.5.1-dogfood-and-prose/` retained per R2.5 forensic.
- Chore worktree `C:/Dev/Claude_cowork/project-genesis/.claude/worktrees/chore_2026-04-19_v1_5_1_session/` for this chore commit.
- Tag chain: … v1.4.2 → v1.5.0 → **v1.5.1**.
