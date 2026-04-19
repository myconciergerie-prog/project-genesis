<!-- SPDX-License-Identifier: MIT -->
---
name: v1.5.1 dogfood + prose corrections on v1.5.0 living memory
description: PATCH spec closing the three gaps flagged in the 2026-04-19 v1.5.0 honesty correction (self-rating 8.62 vs 9.28 projected). The v1.5.1 discipline upgrade is **dogfood-first ordering** — Candidate 3 (first runtime dogfood of Phase 0.4 / Phase 0.5 / archive / halt) runs BEFORE Candidate 1 (Phase 0.5↔v1.3.2-consent clarification) and Candidate 2 (halt-card reduction, anti-Frankenstein retroactive part 2). This ordering IS the discipline upgrade, not a scheduling convenience — runtime evidence shapes prose edits, reversing the preemptive-prose mistake that drove v1.5.0's 0.66 self-rating drop.
type: spec
version: v1.5.1
target_ship: 2026-04-19
parent_ship: v1.5.0 (81f3c3f)
pain_source: memory/project/session_v1_5_0_living_memory.md § "Honesty correction"
---

# v1.5.1 — Dogfood + prose corrections on v1.5.0 living memory

## Problem statement — three gaps flagged on v1.5.0 ship

The v1.5.0 chore commit corrected the initial self-rating projection from **9.28 down to 8.62 honest**, breaking an 11-consecutive streak ≥ 9.0 (v1.2.1 → v1.4.2). Three substantive issues drove the correction:

1. **Zero runtime validation of new dispatch logic.** Phase 0.4 cross-session detection, Phase 0.5 arbitration card, archive write atomic sequence, and halt-with-remediation cards all ship as prose in `SKILL.md`. Verification probes (v1.5.0 Task 10) checked static structure only (grep patterns, JSON parse). The dispatch was never executed against a fixture. Per Layer 0 `discipline_periodic_dogfood_checkpoint.md`, this is a recognized gap — Genesis has not run an end-to-end dogfood since v1.4.1 (2026-04-18 colocs-tracker stress test), 10 ships ago.
2. **6 halt-with-remediation cards × 2 languages = 12 cards is enumeration-of-exit-codes Frankenstein-lite.** Only `EXIT_NO_KEY` and `EXIT_SDK_MISSING` address real user-facing pain (subscription≠API confusion and SDK install gap). The four others (`EXIT_BAD_INPUT`, `EXIT_API_ERROR`, `EXIT_RATE_LIMIT`, `EXIT_OUTPUT_INVALID`) hit ~0% of real users and carry high bilingual maintenance cost. v1.5.0 shipped them preemptively — the exact trap anti-Frankenstein discipline exists to prevent.
3. **Phase 0.5 arbitration card relationship to the v1.3.2 consent card is ambiguous in `SKILL.md`.** The `## Living memory dispatch (v1.5.0)` section documents the flow `welcome → mirror → 0.4 → 0.5 → write/archive` without stating whether Phase 0.5 subsumes the v1.3.2 consent card or renders in series. Bug latent at first runtime execution — an empty-divergences path may render zero consent prompts (silent write with no user acknowledgement) or two (Phase 0.5 empty card then v1.3.2 card).

These three map 1:1 to the three v1.5.1 candidates flagged in the 2026-04-19 resume. **Ordering matters**: Candidate 3 (dogfood) runs FIRST because its observations shape the exact prose edits in Candidates 1 and 2. Pre-designing the prose fixes before runtime evidence would repeat the v1.5.0 preemptive-halt-cards mistake at a different surface.

## Scope — v1.5.1

### In scope

1. **Candidate 3 — First runtime dogfood of v1.5.0 dispatch.** Prepare a fixture at `C:/tmp/genesis-v1.5.0-dryrun/` containing (a) multi-source seed with intra-drop contradictions (triggers Phase 0.5 intra-drop arbitration), (b) a pre-existing `drop_zone_intent.md` snapshot with a populated field that the new extraction retires (triggers Phase 0.4 retirement), (c) a second scenario variant that exercises the empty-divergences + first-write paths. Invoke `/genesis-drop-zone` against the fixture. Observe the dispatch. Capture frictions (structural / behavioural / ambiguity-observed) in `memory/project/dogfood_v1.5.0_*.md`. Cover the halt card path by unsetting `ANTHROPIC_API_KEY` in one scenario. **Hard timebox 2 hours.**
2. **Candidate 1 — Phase 0.5 ↔ v1.3.2 consent card relationship clarification.** One-paragraph addition to `skills/genesis-drop-zone/SKILL.md` § `## Living memory dispatch (v1.5.0)`. The clarification names the canonical flow for the empty-divergences path, the non-empty-divergences path, and the halt path. Pre-registered hypothesis lives in § Appendix A (not inline here) — [A2] requires the shipped prose to cite a specific fixture scenario name and observed behavioural line, grep-able on disk.
3. **Candidate 2 — Halt-card taxonomy collapse.** Merge `EXIT_BAD_INPUT` + `EXIT_API_ERROR` + `EXIT_RATE_LIMIT` + `EXIT_OUTPUT_INVALID` into one generic "internal error" halt card with stderr-log + issue-template guidance. Keep `EXIT_NO_KEY` as a distinct card (get-an-API-key remediation is the highest-pain user-facing surface per v1.5.0 honesty correction). `EXIT_SDK_MISSING` status depends on dogfood Fixture D evidence (see § Design). Final distinct-card count: **≤ 3 × 2 languages = ≤ 6 variants** (down from 12), with an explicit two-way rule — **allowed to drop** to 4 variants (2 cards × 2 langs) if Fixture D shows `EXIT_SDK_MISSING` is unreachable post-v1.4.2 bundled stack refresh; **not allowed to raise** above 6 (no new cards introduced under this scope). Edit `skills/genesis-drop-zone/phase-0-welcome.md` bilingual templates AND `skills/genesis-drop-zone/SKILL.md` halt-table accordingly. The script `scripts/extract_with_citations.py` keeps its 6 distinct exit codes — collapse is at the render layer only. Diagnostic fidelity for Victor preserved via stderr.
4. **Session memory + CHANGELOG + resume + MEMORY index.** Standard chore commit materials following the v1.4.2 / v1.5.0 pattern.

### Out of scope (deferred)

- **v1.6.0 Promptor skill promotion** — queued for v1.6.0 (or later) per the 2026-04-19 resume. Independent of the v1.5.x line. Shipping it before closing the v1.5.0 dogfood gap would carry the honest-rating debt forward.
- **fsync-then-rename atomic archive write** — v1.5.0 accepted the small archive-written-then-new-write-fails window as a tradeoff. Deferring still. Would earn v1.5.2+ attention only if dogfood observes a real failure in that window.
- **Additional bilingual variants** — zero new bilingual pairs in scope. Net delta is **negative**: fewer variants after collapse.
- **Schema version bump** — `schema_version: 1` preserved. No frontmatter key added, none removed.
- **New privilege class** — disk class unchanged; network class unchanged. No extraction subprocess rewrite.
- **Layer B ripple** — zero Layer B (`genesis-protocol`) changes projected. Phase 0 Step 0.2a parser untouched. If dogfood surfaces a Layer B friction, it defers to v1.5.2.
- **New cross-skill pattern** — four patterns stable. v1.5.1 touches no pattern narrative.
- **Dogfood surfacing 4+ new frictions** — hard defer rule: anything beyond the three flagged candidates scopes out to v1.5.2 regardless of severity, except `blocker` (explicit halt taxonomy below). Non-blocker Layer A ↔ Layer B prose inconsistency defers. Non-blocker archive-path OS-specific bug (absolute vs relative, Windows path normalization) defers.
  - `blocker` = cannot ship v1.5.1 safely without fixing — data-destructive behaviour, silent no-op on consent card, Phase 0.5 renders zero surface when divergences present, Phase 0.4 writes to wrong filesystem location, Layer B parser crashes on v1.5.0 frontmatter keys. Halts ship; renegotiate scope explicitly with user.
  - `structural` = shipped-prose misrepresents runtime behaviour on a candidate-mapped surface (1 or 2). In scope for v1.5.1 because Candidate 1 / Candidate 2 edits address them.
  - `polish` = cosmetic or edge-case, not candidate-mapped. Defers to v1.5.2.

## Design

### Candidate 3 — Dogfood fixture design

Two fixtures at `C:/tmp/genesis-v1.5.0-dryrun/`:

**Fixture A — `scenario_retirement/`** — exercises Phase 0.4 retirement + Phase 0.5 cross-session arbitration + archive write.

- Seed files:
  - `config.txt` — minimal 3-line description of a small app idea.
  - `brief.md` — contradicts `config.txt` on the `budget` field ("gratuit / free tier only") and on `visibility` ("public OSS").
  - `drop_zone_intent.md` — pre-existing snapshot with `budget: "a trouver ensemble"` (null-class token). New extraction returns a real value → Completion (additive, no arbitration). Snapshot also has `visibility: "public"` (real value). New extraction returns `"non mentionnee"` (null-class) → Retirement (forces arbitration). Intra-drop contradiction on `budget` (new files disagree among themselves) also feeds intra-drop arbitration.
  - `drop_zone_intent.md` frontmatter has `snapshot_version: 1` (v1.4.x legacy compat path) to test the default-to-1 fallback.

**Fixture B — `scenario_first_write/`** — exercises first-write path (no existing snapshot) + empty divergences.

- Seed files:
  - `config.txt` — 3-line description, internally consistent.
  - `brief.md` — elaborates on the same description, no contradictions with `config.txt`.
  - No pre-existing `drop_zone_intent.md`.

Expected: Phase 0.4 skipped (no existing snapshot), Phase 0.5 skipped (no intra-drop divergences), direct write to `drop_zone_intent.md` with `snapshot_version: 1`, `arbitrated_fields: []`, no `supersedes_snapshot` key. **This is the path where the v1.3.2 consent card should render** if our hypothesis is correct.

**Fixture C — `scenario_halt_no_key/`** — exercises `EXIT_NO_KEY` path.

- Seed files: same minimal shape as Fixture B.
- Invocation-time: run with `ANTHROPIC_API_KEY` unset (or empty).
- Expected: extractor exits 2, dispatch renders `EXIT_NO_KEY` halt card, no file write.

**Fixture D — `scenario_halt_no_sdk/`** — exercises `EXIT_SDK_MISSING` path. Required because Candidate 2's "keep `EXIT_SDK_MISSING` as distinct card" decision otherwise ships on prose-only grounds — the exact mistake v1.5.1 exists to correct.

- Seed files: same minimal shape as Fixture B.
- Invocation-time: simulate SDK absence by invoking the extractor with a `PYTHONPATH` that excludes the `anthropic` package location (e.g., a throwaway venv without `anthropic`, or temporary rename of the installed package dir). Document the chosen method in the dogfood archive.
- Expected: extractor exits 3, dispatch renders `EXIT_SDK_MISSING` halt card, no file write.
- **If Fixture D is infeasible within the 2h timebox** (e.g., SDK is a core Python dependency that cannot be cleanly excluded): explicitly mark `EXIT_SDK_MISSING` as "prose-validated only" in the `dogfood archive` and drop the Candidate 2 floor to 4 variants (2 cards × 2 langs) — collapse `EXIT_SDK_MISSING` into the generic internal-error card. This converts an unverifiable decision into a simpler shippable one.

**Timebox exceeded rule**: if 2 hours elapse and one or more fixtures are not fully executed, halt the dogfood. Whatever has been executed becomes the evidence base for Candidates 1 and 2. Unexecuted fixtures are explicitly recorded as "not reached within timebox" in the dogfood archive — the corresponding Candidate 1/2 surface falls back to pre-registered hypothesis with explicit "not dogfood-validated" marker in shipped prose. This is stricter than v1.5.0: absence of evidence is labelled, not hidden.

**Dogfood observation protocol** — for each fixture, record:
- Which cards rendered (welcome, mirror, Phase 0.5 arbitration, v1.3.2 consent, halt — tick per visible surface).
- Which frontmatter keys appear in any written file (`drop_zone_intent.md` + any `drop_zone_intent_history/v<N>_*.md`).
- Any stderr lines logged by the extractor or dispatch.
- Any divergence between observed behaviour and what `SKILL.md` § `## Living memory dispatch (v1.5.0)` documents.
- Any friction (unclear prompt, missing instruction, ambiguous response format, unrendered locale, broken archive path, etc.).

**Friction log format**: one `## Friction N — <1-line summary>` per finding in `memory/project/dogfood_v1.5.0_YYYY-MM-DD/friction_log.md`. Each entry carries `severity ∈ {blocker, structural, polish}`, `candidate_mapping ∈ {1, 2, neither}`, and `proposed_fix` (1-3 lines).

### Candidate 1 — Phase 0.5 ↔ v1.3.2 consent card clarification

**Current (v1.5.0, `SKILL.md` lines ~323-420)** — section `## Living memory dispatch (v1.5.0)` documents Phase 0.4 + Phase 0.5 + archive write + halt card in order, but never reconciles Phase 0.5 with the v1.3.2 consent card. The v1.3.2 consent card is defined upstream in a v1.3.2-era section and is orthogonal to the v1.5.0 dispatch prose.

**v1.5.1 rewrite** — add a new subsection `### Consent-card interaction with Phase 0.5 (v1.5.1 clarification)` at the end of `## Living memory dispatch (v1.5.0)`, before `## Phase 0 — welcome`.

**Discipline constraint — shipped prose cites dogfood**. The final subsection text MUST reference at least one Fixture scenario name (e.g., "as observed in Fixture A retirement scenario, ...") AND one grep-able observed-behaviour line (e.g., "the dispatch printed `[phase-0.4] field=visibility RETIREMENT ...` before rendering the arbitration card"). If the dogfood observation confirms the pre-registered hypothesis in § Appendix A, the prose still cites — "confirmed by Fixture A" is acceptable prose, "hypothesis assumed" is not. If dogfood refutes or refines the hypothesis, prose follows evidence. If dogfood surfaces zero friction on Candidate 1's target surfaces, shipped prose explicitly states that (e.g., "All three paths behaved per pre-registration; clarification added for future readers rather than to correct observed divergence") — silence on this point is the v1.5.0 mistake recurring.

### Candidate 2 — Halt card taxonomy collapse

**Current (v1.5.0, `skills/genesis-drop-zone/phase-0-welcome.md`)** — 12 bilingual templates (6 distinct cards × FR + EN):

| Exit code | Current card title | Collapse target |
|---|---|---|
| 2 `EXIT_NO_KEY` | Genesis nécessite une clé API Anthropic / ... requires an Anthropic API key | **KEEP** (distinct remediation: get a key) |
| 3 `EXIT_SDK_MISSING` | SDK Anthropic non installé / ... not installed | **KEEP** (distinct remediation: install SDK) — or COLLAPSE if dogfood shows it's rare post-v1.4.2 |
| 4 `EXIT_API_ERROR` | Erreur API / ... error | **MERGE** → generic internal error |
| 5 `EXIT_RATE_LIMIT` | Limite de débit / rate limit | **MERGE** → generic internal error |
| 6 `EXIT_BAD_INPUT` | Erreur interne extracteur / internal extractor error | **MERGE** → generic internal error |
| 7 `EXIT_OUTPUT_INVALID` | Sortie API invalide / invalid API output | **MERGE** → generic internal error |

**v1.5.1 target — 3 distinct cards × 2 languages = 6 variants**:

1. `EXIT_NO_KEY` — title, body, Console deep-link, persistent env-var one-liners, escape hatches, env-scrub warning (preserved from v1.5.0).
2. `EXIT_SDK_MISSING` — title, `pip install anthropic` (plus `uv pip install`, `pipx`), relaunch guidance (preserved).
3. Generic internal error — title "Erreur interne Genesis / Genesis internal error", body references the specific exit-code class printed to stderr by the extractor, directs to issue template at `https://github.com/myconciergerie-prog/project-genesis/issues`, one-line stderr-excerpt capture guidance, and `GENESIS_DROP_ZONE_VERBOSE=1` diagnostic env var.

**Script changes**: zero. `scripts/extract_with_citations.py` still exits with the distinct code (2-7). Dispatch layer in `SKILL.md` maps exit 2 → card A, exit 3 → card B (or card C if collapsed), exits 4-7 → card C.

**SKILL.md halt table rewrite**: replace the 6-row table (lines ~406-413) with a 3-row table. Keep the footer note about subscription ≠ API.

**Anti-Frankenstein rationale**: cards 4-7 enumerate exit codes the user never learns to distinguish (all map to "something broke internally, file an issue"). Preserving them costs bilingual maintenance on every future locale touch for zero user benefit. The dogfood Fixture C will verify card 1 (`EXIT_NO_KEY`) renders correctly; card 2 and card 3 can be verified by injecting forced exits in a follow-up run if dogfood timebox allows, else deferred to v1.5.2 probe.

### Acceptance criteria

Ship gate — all must hold:

- **[A1]** `memory/project/dogfood_v1.5.0_YYYY-MM-DD/friction_log.md` exists and contains a per-candidate entry for Candidates 1 + 2 + 3, where each entry is either (a) one or more frictions with severity ∈ {blocker, structural, polish}, OR (b) an explicit "zero friction observed" entry naming which fixture(s) exercised the surface and which pre-registered hypothesis was confirmed. Zero frictions is a valid outcome and must be recorded as such — unrecorded silence is not.
- **[A2]** `SKILL.md` contains the new subsection `### Consent-card interaction with Phase 0.5 (v1.5.1 clarification)` with wording grounded in dogfood evidence (cite fixture scenario names inside the prose).
- **[A3]** `phase-0-welcome.md` halt-card variant count drops from 12 to ≤ 6. `SKILL.md` halt table row count drops from 6 to ≤ 3.
- **[A4]** `scripts/extract_with_citations.py` unchanged (zero-line diff).
- **[A5]** Layer B diff empty: `git diff main -- skills/genesis-protocol/` shows no changes.
- **[A6]** `schema_version: 1` still present in `genesis-drop-zone` frontmatter examples; no additive / subtractive frontmatter keys.
- **[A7]** `.claude-plugin/plugin.json` version `1.5.0 → 1.5.1`.
- **[A8]** Between feat-commit and chore-commit, perform the honest self-rating re-evaluation ritual REGARDLESS of whether the projection was ≥ 9.0 (per Layer 0 `feedback_honest_self_rating_post_feat.md`). The chore commit's CHANGELOG entry records the post-feat honest rating. If it diverges ≥ 0.2 from the initial projection, state the axis-level deduction and its cause. If it confirms the projection, state that too. Silence is not acceptable.
- **[A9]** `gh api user --jq .login` returns `myconciergerie-prog` before any `gh pr create` invocation (R2.3.1 pre-flight).
- **[A10]** All commits pushed, PR squash-merged, tag `v1.5.1` pushed, post-merge chore committed on main.

### Rationale for v1.5.1 route — decision log

- PATCH honest: no privilege / schema / bilingual / cross-skill-pattern / Layer-B delta; net-negative variant count.
- Pain-driven: 3/3 candidates trace to the 2026-04-19 honesty correction, not speculation.
- Dogfood-first ordering: reverses the preemptive-prose cause of v1.5.0's Anti-Frankenstein 7.5 deduction at the process level.
- Streak discipline: first ship of a new ≥ 9.0 streak after the 11-ship streak broke at v1.5.0.

## Self-rating axes — projection (to be corrected post-feat per honesty discipline)

- Pain-driven — 9.3 (three concrete 2026-04-19-flagged pains, no speculation).
- Prose cleanliness — 9.2 (one new subsection, one table collapse, net-simpler prose than v1.5.0).
- Best-at-date — 9.0 (dogfood discipline is SOTA-aligned per Layer 0; halt-card collapse is anti-Frankenstein canon).
- Self-contained — 9.2 (no new dependencies, no schema changes, no cross-skill ripple, Layer B untouched).
- Anti-Frankenstein — 9.5 (reversing Frankenstein-lite from v1.5.0; three ships of retroactive discipline in a row: v1.4.2 fallback drop, v1.5.0 fallback drop, v1.5.1 halt cards drop).

**Projected mean**: 9.24. **Honest post-feat mean** to be evaluated after dogfood — specifically, if dogfood surfaces > 3 frictions and we defer them, Pain-driven drops; if halt-card collapse lands at 6 variants (not 4), Anti-Frankenstein drops to 9.2. Honest rating is mandatory per v1.5.0 precedent.

## Ship sequence

1. Spec review (spec-reviewer agent) — land P0+P1 advisories.
2. Plan draft + review.
3. Commit spec, commit plan (plan polish 1-2 passes allowed per R10).
4. Fixture prep at `C:/tmp/`.
5. Dogfood run (timebox 2h).
6. Commit dogfood archive under `memory/project/dogfood_v1.5.0_YYYY-MM-DD/`.
7. Feat commit — SKILL.md clarification + halt card reductions + phase-0-welcome.md edits + plugin.json version bump.
8. Reviewer pass on feat.
9. Push, open PR, R2.3.1 gh pre-flight, merge, tag.
10. Chore commit — CHANGELOG honest + MEMORY + session trace + resume for v1.5.1 → v1.5.2 or v1.6.0.

## Appendix A — Pre-registered hypotheses (NOT shipped prose)

These hypotheses are recorded BEFORE dogfood so the review trail is auditable. They are explicitly NOT the final prose for Candidates 1 and 2. The feat commit's final prose must cite dogfood fixture observations per [A2] and the Candidate 1 discipline constraint.

**Candidate 1 hypothesis H1** — Phase 0.5 arbitration card SUBSUMES the v1.3.2 consent card when divergences are non-empty. Victor's arbitration response IS the consent; `abort` is the refuse path. When divergences are empty, v1.3.2 consent card renders before write (preserves v1.4.x parity). When halt card renders, neither consent nor Phase 0.5 renders.

**Candidate 1 hypothesis H2** — on empty-divergences re-run with byte-identical content, dispatch may short-circuit to skip overwrite entirely (TBD from dogfood).

**Candidate 2 hypothesis H3** — `EXIT_NO_KEY` stays distinct; `EXIT_SDK_MISSING` stays distinct IF Fixture D validates it at runtime, else collapses into generic internal-error card; exits 4-7 collapse into the generic card.

**Candidate 2 hypothesis H4** — extraction script's 6 distinct exit codes are preserved; collapse is render-layer only.

If dogfood refutes H1 or H3, the Design section text shipped in SKILL.md / phase-0-welcome.md is rewritten from evidence. If dogfood confirms, shipped prose still cites the fixture scenario name.
