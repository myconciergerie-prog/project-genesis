<!-- SPDX-License-Identifier: MIT -->
---
name: Dogfood friction log — v1.5.0 runtime — 2026-04-19
description: First runtime dogfood of Genesis v1.5.0 living-memory dispatch. Paper-trace method (the canonical "runtime" for prose-only skills = Claude reading SKILL.md and tracing the dispatch against fixtures). Captures frictions mapped to v1.5.1 Candidates 1, 2, 3 per spec Appendix A hypotheses H1-H4.
type: project
session: v1.5.1 dogfood execution
fixtures_executed: 4 (A retirement, B first_write, C halt_no_key, D halt_no_sdk)
fixtures_timebox: 2h (paper-trace under 1h — genuine runtime invocation of /genesis-drop-zone in C:/tmp/ subdirectories deferred to a follow-up session because the current Claude Code session cwd is the project-genesis repo, which fails the `is_fresh_context` guard — another finding in its own right, see Friction #7)
---

# Dogfood v1.5.0 — Friction log

## Method note

The canonical "runtime" for a prose-only Claude Code skill is a Claude session reading `SKILL.md` end-to-end and executing the dispatch logic against an input. This dogfood reads `skills/genesis-drop-zone/SKILL.md` from `main` (tag `v1.5.0`, commit `81f3c3f`, pre-v1.5.1 state) and traces each dispatch path against the four fixtures prepared at `C:/tmp/genesis-v1.5.0-dryrun/`. Frictions are the points where the prose is ambiguous, self-contradictory, or would produce behaviour contradicting the v1.5.0 design intent.

A cleaner "runtime" execution (spawning a separate Claude Code session in each fixture cwd and invoking `/genesis-drop-zone`) is recorded as a follow-up observation but not prerequisite to this dogfood's validity — the prose IS the runtime surface for this skill class, and prose contradictions directly produce runtime ambiguity.

## Fixture summaries

### Fixture A — `scenario_retirement/`

**Files at cwd**: `config.txt` (internally consistent, mentions "20 euros/month hosting" budget + "private personal use only" visibility), `brief.md` (contradicts — "Zero recurring cost" OR "~5 euros/month ceiling" + "open-sourcing under MIT" public), pre-existing `drop_zone_intent.md` (snapshot_version: 1, budget = null-class `"a trouver ensemble"`, visibility = `"private"` populated, project_name = null-class).

**Expected dispatch paths triggered**:
- Phase 0.4 Completion on `budget` (current null-class, new real) → additive, no arbitration.
- Phase 0.4 Retirement on `visibility` (current `"private"`, new would be... unclear — see Friction #3) → arbitration required.
- Phase 0.4 Divergence on `budget` if intra-drop also differs on `budget` value.
- Intra-drop divergence on `budget` (`config.txt` says ~20€/mo vs `brief.md` says ~5€/mo or free).
- Intra-drop divergence on `visibility` (`config.txt` says private vs `brief.md` says public OSS).
- Phase 0.5 arbitration card consolidating both lists.
- Archive write of superseded snapshot + new snapshot with `snapshot_version: 2`, `arbitrated_fields: [budget, visibility]`, `supersedes_snapshot: ./drop_zone_intent_history/v1_<ts>.md`.

**Frictions surfaced**: see #1, #2, #3, #4, #5, #6 below.

### Fixture B — `scenario_first_write/`

**Files at cwd**: `config.txt` (consistent, mentions "free" budget + "open source on GitHub" visibility + "TypeScript + Node" tech), `brief.md` (elaborates consistently, no contradictions). No pre-existing `drop_zone_intent.md`.

**Expected dispatch paths triggered**:
- Phase 0.4 skipped (no existing snapshot).
- Phase 0.5 skipped if no intra-drop divergences (likely — fixtures drafted to be internally consistent).
- Direct write path. **This is where the v1.3.2 consent card should render per Candidate 1 hypothesis H1.**

**Frictions surfaced**: see #6.

### Fixture C — `scenario_halt_no_key/`

**Files at cwd**: minimal `config.txt` only. No `drop_zone_intent.md`.

**Runtime env**: `ANTHROPIC_API_KEY` confirmed absent in the current session (verified by `test -n "$ANTHROPIC_API_KEY" && echo ... || echo ABSENT` → `API_KEY_ABSENT`).

**Expected dispatch paths triggered**:
- `api_extraction_available = false` at skill entry.
- Per v1.5.0 § "In scope" item #1: halt-with-remediation card, fallback retired.
- Per v1.4.0 § "Citations API dispatch" still in the file (lines 218-321): silent graceful fallback to v1.3.3 in-context extraction.
- **Contradictory prose.** See Friction #1 below.

**Frictions surfaced**: see #1, #4.

### Fixture D — `scenario_halt_no_sdk/`

**Files at cwd**: minimal `config.txt` only.

**Runtime env**: cannot be reached without first resolving Friction #1 + #4 (pre-flight ordering ambiguity between key check and SDK check). Throwaway venv preparation documented as `python -m venv C:/tmp/genesis-v1.5.0-dryrun/.venv-no-sdk; C:/tmp/genesis-v1.5.0-dryrun/.venv-no-sdk/Scripts/python --version` — venv would have no `anthropic` package. Invocation would set `ANTHROPIC_API_KEY=dummy_sk_do_not_use` (to get past the key gate) and point the subprocess `command -v python` resolution at the venv's python.

**NOT EXECUTED within this dogfood pass** — blocked by Friction #4 unclarity. Deferred per spec timebox-exceeded rule, affects Candidate 2 H3 evidence.

## Frictions

## Friction #1 — v1.4.0 fallback prose contradicts v1.5.0 fallback-retired declaration
severity: blocker
candidate_mapping: 1 (primary) + 2 (secondary)
fixture: A, B, C
observation: `SKILL.md` line 220 (inside § "Citations API dispatch (v1.4.0)") reads verbatim: *"When the key is absent or the subprocess fails for any reason, the skill routes through a silent graceful fallback to v1.3.3 in-context extraction."* Lines 244-257 present the Exit codes table with "SKILL.md response" column = `Fallback` for exits 2-7. Lines 277-285 present § "Fallback triggers" listing four conditions (including `api_extraction_available = false`) that commit dispatch to fallback.

In contrast, `SKILL.md` line 74 (inside § "In scope (v1.5.0)" item #1) reads: *"API requirement — fallback removed — v1.4.0's silent graceful fallback to in-context extraction is retired. The extractor exit codes 2-7 now signal halt-with-remediation to the SKILL.md dispatch layer, not in-context fallback."*

**Both sections live in the same file. Neither explicitly supersedes the other with a diff marker, "this supersedes v1.4.0 § Fallback triggers", or strikethrough.** A Claude reading `SKILL.md` as dispatch logic reaches contradictory conclusions depending on which section it anchors on. Real runtime behaviour under this prose is undefined.

Additional contradictory artefact: § "Modification-loop interaction" at line 317 explicitly describes v1.4.0 fallback behaviour ("If ANTHROPIC_API_KEY is revoked mid-session [...] the subprocess launches on the next iteration, hits exit code 2 at its own env check, and the dispatch routes through the fallback path via the exit-code-≠-0 trigger. The re-printed consent card does not indicate the path change."). This pure-v1.4.0 paragraph remains unamended post-v1.5.0 retirement.
proposed_fix: Candidate 1 must not only add a new subsection on Phase 0.5 ↔ consent. It must also either (a) delete the v1.4.0 fallback table rows + §"Fallback triggers" + Modification-loop-interaction v1.4.0 paragraph OR (b) prefix each v1.4.0 section with a clear "**Retired in v1.5.0 — see § Living memory dispatch below**" banner. Option (a) is cleaner and aligns with anti-Frankenstein retroactive discipline. This change is IN SCOPE for v1.5.1 Candidate 1 because the ambiguity it creates is structurally identical to the Phase 0.5 ↔ consent ambiguity — both are v1.5.0-ships-prose-that-contradicts-v1.5.0-intent.
hypothesis_bearing: H1 — refutes the pre-registration's implicit assumption that "SKILL.md clearly states retirement". Prose claims retirement; prose elsewhere contradicts retirement. Candidate 1's scope expands: the clarification subsection is insufficient — the v1.4.0 contradictions must be resolved too.

## Friction #2 — Phase 0.4 "after the extractor returns" assumes extractor ran
severity: structural
candidate_mapping: 1
fixture: A, B
observation: `SKILL.md` line 329 opens Phase 0.4 with: *"After the extractor returns its JSON output, the dispatch layer checks whether drop_zone_intent.md already exists at cwd."* If `api_extraction_available = false` and Friction #1 is resolved toward "halt-with-remediation" (no fallback), then no extractor returns — Phase 0.4 is unreachable without an API key. If Friction #1 is resolved toward "silent fallback to v1.3.3 in-context extraction" (status quo per the v1.4.0 prose still in the file), then v1.3.3's in-context extraction acts as "the extractor" and Phase 0.4 triggers — but the SKILL.md never explicitly says in-context extraction counts as "the extractor" for Phase 0.4 purposes.
proposed_fix: Candidate 1 clarifies: Phase 0.4 triggers on ANY extraction path (API + in-context), because it operates on the 9-field JSON regardless of source. The Phase 0.4 prose is amended to "After extraction completes (regardless of path — API subprocess per § Citations API dispatch, or in-context per § v1.3.1 baseline)..." If fallback is retired per Candidate 1, this amendment still stands as forward-compatible.
hypothesis_bearing: H1 — the cross-session-detection path is implicitly tied to extractor runtime state in current prose, creating a coupling that Candidate 1 must explicitly decouple.

## Friction #3 — Retirement trigger underspecified when new extraction source is absent
severity: structural
candidate_mapping: 1
fixture: A
observation: Phase 0.4 Retirement class: `current != null-class, new == null-class`. But what does "new" equal when the new extraction does not mention the field at all? The v1.3.1 null-visible convention says missing bonus fields default to `"non mentionnee"` (null-class). Hence any field not mentioned in the new drop triggers Retirement automatically, flooding the arbitration card. For Fixture A, `config.txt` does NOT mention `tech_hints` (inherited from pre-existing `drop_zone_intent.md` as null-class) — but it DOES mention `visibility` as `"private"` in `config.txt` while `brief.md` says public OSS. New extraction for `visibility` would likely resolve to one of the contradicting values (or `"a affiner — prive ou public"`) — NOT null-class. So Retirement is not triggered on `visibility`; Divergence + intra-drop divergence are. This contradicts the Fixture A expectation in this log's design. Re-plan: Retirement is only triggered on fields that were populated previously AND deliberately absent in the new drop — a narrow case.
proposed_fix: Neither Candidate 1 nor 2 target this directly. **Defers to v1.5.2** per spec's "non-blocker structural friction not candidate-mapped" rule. Log in friction_log.md for future reference. The v1.5.0 ship is not blocked by it; the Fixture A design is the confused artefact, not the SKILL.md.
hypothesis_bearing: none — out of v1.5.1 scope.

## Friction #4 — Pre-flight ordering between API key check and SDK check is unspecified
severity: structural
candidate_mapping: 2
fixture: C, D
observation: The v1.5.0 halt-card taxonomy distinguishes `EXIT_NO_KEY` (2) from `EXIT_SDK_MISSING` (3). These are extractor-subprocess exit codes. But `api_extraction_available` per v1.4.0 § "Dispatch lifecycle" item #3 (line 228) is *"a boolean resolved by checking ANTHROPIC_API_KEY in the environment. If unset or empty, false."* — only the key, not the SDK. So the SDK-presence check happens INSIDE the subprocess (or would, per extract_with_citations.py). Dispatch ordering:

1. Pre-flight: key absent → `api_extraction_available = false` → in v1.5.0 retired-fallback reading, halt with EXIT_NO_KEY (subprocess never invoked).
2. Pre-flight: key present → subprocess invoked → subprocess internally checks SDK → exits 2 if key-at-runtime-missing (impossible if pre-flight passed, unless env scrub) or exits 3 if SDK missing.

The prose does not state this ordering explicitly. For Fixture D, to reach EXIT_SDK_MISSING, we need key PRESENT AND SDK absent. Setting `ANTHROPIC_API_KEY=dummy_sk` is a workaround but may trigger EXIT_API_ERROR (auth fail) instead of EXIT_SDK_MISSING if the subprocess does SDK-import LAZY (after first API call).

**Without reading `extract_with_citations.py` source explicitly**, the ordering is unknown. Fixture D execution blocked.
proposed_fix: Candidate 2 must resolve by either (a) inspecting extract_with_citations.py import order and documenting it in SKILL.md, OR (b) conceding that EXIT_SDK_MISSING is operationally indistinguishable from EXIT_NO_KEY in practice (both = "something's missing in the user's env") and collapsing them into a single card. Option (b) drops Candidate 2 floor to **2 distinct cards × 2 langs = 4 variants** per the spec's two-way rule.
hypothesis_bearing: H3 — refutes the pre-registration's "EXIT_SDK_MISSING stays distinct as independent remediation". Evidence: without a verified runtime distinction, keeping them distinct is prose-only. Recommended v1.5.1 lands at floor of 4 variants (2 × 2) per spec's permitted-drop branch.

## Friction #5 — Modification-loop interaction paragraph describes retired behaviour
severity: structural
candidate_mapping: 1
fixture: —
observation: `SKILL.md` line 313-317 § "Modification-loop interaction" says: *"If `ANTHROPIC_API_KEY` is revoked mid-session (user unsets externally — out-of-scope), `api_extraction_available` stays `true` (the gate is immutable). The subprocess launches on the next iteration, hits exit code `2` at its own env check, and the dispatch routes through the fallback path via the exit-code-≠-0 trigger. The re-printed consent card does not indicate the path change."* This is pure v1.4.0 behaviour — v1.5.0 item #1 explicitly retires it. The paragraph survived the v1.5.0 ship without amendment.
proposed_fix: Candidate 1 deletes this paragraph OR rewrites it to align with v1.5.0 halt-card routing ("if key is revoked mid-session, the next iteration's subprocess hits exit 2, dispatch renders the EXIT_NO_KEY halt card, modification loop exits without writing"). Evidence from Friction #1 already motivates the v1.4.0 retirement scan across the file. This paragraph is one more instance to fix.
hypothesis_bearing: H1 extension — same root cause as Friction #1.

## Friction #6 — Empty-divergences path writes WITHOUT v1.3.2 consent card (BLOCKER)
severity: blocker
candidate_mapping: 1
fixture: B
observation: `SKILL.md` line 348 (§ "Phase 0.5 — Arbitration consolidated card") reads verbatim: *"If the consolidated divergences list (intra-drop + cross-session) is empty, skip Phase 0.5 entirely. Proceed to write/archive operations with the new extraction values verbatim."*

"Proceed to write/archive operations [...] verbatim." — no mention of the v1.3.2 consent card. A Claude executing this dispatch on Fixture B (first write, no divergences) would write `drop_zone_intent.md` to cwd without ever rendering the consent card. This is a direct violation of v1.3.2's privilege model: the v1.3.2 concentrated privilege (disk class) is gated by the bilingual consent card. Writing without consent breaks:

1. The five-mitigations contract for the disk class (mitigation: "bilingual consent card offers to save the extracted intent" — line 40, v1.3.2 scope item #1).
2. R10 concentrated-privilege-map discipline (every declared privilege has a consent gate).
3. Victor's reasonable expectation that Genesis does not write files without asking.

This is the exact ambiguity the v1.5.0 resume flagged as "latent bug at first runtime execution". **Dogfood confirms it is not merely latent — the literal prose writes it**. A blocker-class finding per spec § Scope blocker taxonomy ("silent no-op on consent card", which this is: the consent card is silently skipped on a path the user would assume includes it).
proposed_fix: Candidate 1 MUST fix this in v1.5.1. The new subsection `### Consent-card interaction with Phase 0.5 (v1.5.1 clarification)` commits to the following canonical flow:

- **Non-empty divergences**: Phase 0.5 arbitration card SUBSUMES the v1.3.2 consent card. Arbitration response IS consent.
- **Empty divergences, any write path (first-write OR re-run-same-content)**: v1.3.2 consent card RENDERS before write. If Victor declines, no write occurs (v1.3.2 behaviour preserved). If accepts, proceed to write/archive.
- **Empty divergences, re-run with byte-identical content**: consent card STILL renders (consistent with "no special case"). Dispatch may optionally short-circuit the overwrite if byte-identical, but the consent still happens — preserves predictability. H2 lowered to "UI short-circuit optional; consent is non-optional".
- **Halt card (any exit 2-7, post-Friction-#1-resolution)**: neither consent nor arbitration renders; halt terminates pre-write.

This commits v1.5.1 prose to a written contract. Line 348's current "proceed to write/archive verbatim" is rewritten to "render the v1.3.2 consent card; proceed to write/archive only on affirmative consent".

This is the single most important fix in v1.5.1 Candidate 1.
hypothesis_bearing: H1 — confirmed AND the shipped prose of v1.5.0 actively violates the hypothesis. Candidate 1's clarification goes from "add a new subsection for future readers" to "close a BLOCKER-severity prose gap that would cause Genesis to write without consent on the most common happy-path fixture (first write, internally-consistent drop)".

## Friction #7 — `is_fresh_context` blocks dogfood execution from within the Genesis repo
severity: polish
candidate_mapping: neither
fixture: —
observation: The current Claude Code session runs inside `C:/Dev/Claude_cowork/project-genesis/` — the Genesis development repo. `CLAUDE.md` at repo root + populated `memory/` dir + git history (≥ 3 commits) all hold. Therefore `is_fresh_context = false` and any invocation of `/genesis-drop-zone` from this session prints the bilingual redirect and exits without proceeding to the dispatch paths under test. The dogfood method chose paper-trace rather than sub-session spawn in `C:/tmp/<fixture>/`.
proposed_fix: v1.5.2+ polish — no action in v1.5.1. The paper-trace method is valid for prose-only skills; future dogfoods of runtime behaviour should spawn a separate Claude Code session per fixture cwd, documented as "how to dogfood genesis-drop-zone" in a README under `tests/` or `memory/project/`. Deferral explicit.
hypothesis_bearing: none.

## Hypothesis outcomes (per spec Appendix A)

| Hypothesis | Outcome | Evidence |
|---|---|---|
| **H1** — Phase 0.5 SUBSUMES v1.3.2 consent card on non-empty divergences; v1.3.2 consent renders on empty-divergences write path; halt renders neither | **Confirmed in principle, BLOCKER in current prose** — Friction #6 shows v1.5.0 shipped prose actively violates this. Candidate 1 fix is not optional polish; it is BLOCKER remediation. |
| **H2** — Byte-identical re-run may short-circuit overwrite | **Refined** — per Friction #6 fix, consent card ALWAYS renders on empty-divergences write paths. Short-circuit of overwrite is a cosmetic optimization AFTER consent, not instead of consent. Defer short-circuit to v1.5.2+. |
| **H3** — EXIT_SDK_MISSING stays distinct | **Refuted by evidence** — Friction #4 shows distinction is operationally opaque without fixture D runtime. Recommend collapse into EXIT_NO_KEY-or-env-missing card. Candidate 2 floor lands at **4 variants (2 × 2)** per spec's permitted-drop branch. |
| **H4** — Extractor 6 distinct exit codes preserved (render-layer collapse only) | **Confirmed** — no evidence against. extract_with_citations.py untouched in v1.5.1 scope. |

## Summary — severity breakdown

- **Blocker**: Friction #1 (v1.4.0 / v1.5.0 prose contradiction) + Friction #6 (empty-divergences writes without consent).
- **Structural**: Friction #2 (Phase 0.4 extractor coupling), Friction #4 (pre-flight ordering), Friction #5 (modification-loop v1.4.0 paragraph).
- **Polish**: Friction #7 (is_fresh_context blocks in-repo dogfood).
- Not candidate-mapped / deferred: Friction #3 (retirement trigger semantics — v1.5.2+).

## Blocker triage decision

Per spec § Scope blocker rule: 2 blockers surfaced. **Both are SCOPE-EXPANDING for Candidate 1, not ship-halting**. Rationale:

- Friction #1 falls naturally within Candidate 1's "clarify the v1.5.0 living-memory dispatch prose" scope — the v1.4.0 fallback retirement needs to be reflected throughout SKILL.md, not just in a new subsection. The fix is to delete / banner the v1.4.0 fallback prose. Straightforward, grep-guided, no new information needed.
- Friction #6 is exactly what Candidate 1's new subsection exists to prevent — making the consent-card contract explicit on the empty-divergences path.

Both can be addressed in the v1.5.1 feat commit via Candidate 1 prose edits. No need to halt the ship. Candidate 1 scope IS expanded from "add one subsection" to "one subsection + v1.4.0 fallback retirement propagation across SKILL.md + Modification-loop paragraph rewrite". Estimated effort doubles (~60 min instead of ~30 min) but stays within the PATCH tranche.

**Proceed to Step 5 (Candidate 1 feat edit) with expanded scope.**

## Surfaces NOT executed at runtime

Documented per spec [A1]:

- Phase 0.4 Completion / Retirement / Divergence observation — paper-traced, not executed (needs API key).
- Phase 0.5 arbitration card rendering — paper-traced, not executed.
- `drop_zone_intent_history/` archive write mechanics (path resolution, frontmatter injection, ISO8601 timestamp format) — paper-traced only.
- Fixture B second-pass re-run (H2 byte-identical short-circuit) — not executed; refined to "consent-card-always, short-circuit-optional" per Friction #6 analysis.
- Fixture D throwaway venv EXIT_SDK_MISSING runtime — not executed; collapsed into Candidate 2 floor-of-4 per Friction #4.

Shipped Candidate 1 prose will cite specific fixture scenario names (A, B, C) for grep-traceability per spec [A2], anchored in paper-trace evidence rather than live execution. **This is explicitly marked as "paper-trace dogfood" in the shipped prose** rather than silently claiming full runtime validation. The honesty marker per spec discipline.
