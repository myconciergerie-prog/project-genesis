<!-- SPDX-License-Identifier: MIT -->
---
name: v1.6.2 Runtime dogfood — spec
description: Close the v1.5.0 paper-trace debt (deferred through v1.5.1 → v1.6.0 → v1.6.1) via runtime evidence captured from 5 fresh Claude Code sessions (4 v1.5.0 fixtures dispatch-only + 1 new "alexandre_windows" full happy-path). Real Anthropic Messages API subprocess calls on 4 fixtures ; EXIT_NO_KEY halt card runtime on 1. Ship retitled from v1.5.2 back-insert to v1.6.2 forward-increment after plan-reviewer surfaced plugin.json ≥ 1.6.1 semver reality. Hybrid blocker gate : privilege-violation → in-feat fix ; prose-ambigu → defer v1.6.3+. Evidence captured in dedicated runbook + evidence log under `tests/`, never in spec file (v1.6.1 runbook pattern). Streak ≥ 9.0 projected to advance to 4 consecutive.
type: spec
version: v1.6.2
ship_class: PATCH forward-increment from v1.6.1 (originally scoped as v1.5.2 back-insert ; retitled post plan-reviewer)
predecessor: v1.6.1 (2d634b9)
---

# v1.6.2 — Runtime dogfood — spec

## 1. Goal

Close the priced-in axis cap of **v1.5.0** (Pain-driven 8.1 — "zero runtime validation of Phase 0.4 / Phase 0.5 / archive / halt cards") that v1.5.1 only partially addressed via paper-trace dogfood. v1.5.1 correctly sequenced "dogfood before prose" but the dogfood itself was static-artefact analysis of 4 pre-populated fixtures — no actual Claude Code session was spawned, no actual skill dispatched.

This ship exercises the **runtime surface** : fresh Claude Code sessions in 5 fixture cwds, `/genesis-drop-zone` invoked naturally, cards rendered live, artefacts written by live subprocess extraction → Anthropic Messages API (Citations-enabled), halt card rendered on absent API key.

## 2. Non-goals

- **NG1** — not re-running the v1.5.1 paper-trace friction log. That analysis remains authoritative as a static review ; v1.6.2 augments with runtime and surfaces deltas only.
- **NG2** — not testing adversarial multi-artefact conflict (contradictory `catalogue_fr.md` vs `voice_memo.txt`). Reserved for v1.6.3+ under a dedicated "arbitration stress" spec.
- **NG3** — not refactoring the extraction subprocess, citation rendering, or halt card wording. Only evidence capture. Any blocker surfaced routes through the hybrid gate (§ 5) ; design changes stay out-of-scope.
- **NG4** — not exercising Friction #3 retirement-trigger semantics. Reserved for v1.6.3 as per v1.5.1 resume's v1.6.3 candidate.
- **NG5** — not formalizing CI scaffolding for dogfood. Runbook stays human-spawned for the v1.6.x line runtime-dogfood cadence ; CI harness is v1.7.x+ if pain surfaces.

## 3. Acceptance criteria

| # | Criterion | Method |
|---|---|---|
| AC1 | Worktree `feat_2026-04-19_v1_5_2_runtime_dogfood/` (directory name retained for local forensic continuity post-retitle ; branch renamed to `feat/v1.6.2-runtime-dogfood`) exists, created from `main` at `0b1b310` | `git worktree list` shows entry |
| AC2 | `skills/genesis-drop-zone/tests/runtime_dogfood_v1_6_2.md` runbook exists with sections "Pre-flight", "Per-fixture spawn + trigger + observe", "Redaction rules", "Re-run guidance" | `test -f` + `grep -c "^##"` ≥ 4 |
| AC3 | `skills/genesis-drop-zone/tests/runtime_dogfood_evidence_v1_6_2.md` evidence log exists with 5 per-fixture sections (4 v1.5.0 + 1 alexandre_windows), each with `Trigger phrase used`, `Invocation form observed`, `Cards rendered`, `Artefacts written`, `Frictions found` headers | `grep -c "^### Fixture"` = 5 |
| AC4 | New fixture at `C:/tmp/genesis-v1.6.2-alexandre/` contains 5 artefacts : `config.txt`, `catalogue_fenetres_fr.md`, `specs_usine_pl.md`, `voice_memo_alexandre.txt`, `photo_facade_client.jpg` | `ls` shows 5 files, sizes > 0 |
| AC5 | `plugin.json` version bumped `1.6.1` → `1.6.2` | `jq -r .version` |
| AC6 | Evidence log H1 table populated after runtime checkpoint : for each of 5 fixtures, one row with shape `\| fixture_<name> \| dispatch (confirmed\|failed\|deferred) \| <verbatim-invocation-form> \|` (3 pipe-separated cells per row) | `grep -cE "^\| fixture_[a-z_]+ \| dispatch (confirmed\|failed\|deferred) \|" evidence_log.md == 5` |
| AC7 | Evidence log H2 row populated : alexandre_windows Phase 0.4 arbitration card section captured, `arbitrated_fields` list verbatim | `grep -c "arbitrated_fields:" ≥ 1` |
| AC8 | Evidence log H3 row populated : Phase 0.5 Path 2a consent card confirmed rendered on at least 1 fixture with empty divergences | `grep -c "Path 2a.*:.*confirmed" ≥ 1` |
| AC9 | Evidence log H4 row populated : the 1 API-key-absent fixture shows EXIT_NO_KEY halt card rendered, redacted API error message OK | `grep -c "EXIT_NO_KEY.*rendered" ≥ 1` |
| AC10 | Evidence log H5 row : `git diff --name-only main...HEAD` in feat branch shows ZERO Layer B files modified (no `skills/genesis-protocol/`, no `skills/phase-5-5-auth-preflight/`, no `skills/phase-minus-one/`, no `skills/journal-system/`, no `skills/session-post-processor/`, no `skills/pepite-flagging/`, no `skills/promptor/`). Whitelist narrowed per path precision ; `skills/README.md` explicitly forbidden in § 4.5. | `test "$(git diff --name-only main...HEAD \| grep -v '^skills/genesis-drop-zone/' \| grep -v '^\.claude-plugin/plugin\.json$' \| grep -vE '^\.claude/docs/superpowers/(specs/v1_6_2_runtime_dogfood\.md\|resume/2026-04-19_v1_6_2.*\|plans/v1_6_2_runtime_dogfood\.md\|research/INDEX\.md)$' \| grep -vE '^memory/(project/session_v1_6_2.*\|MEMORY\.md\|master\.md)$' \| grep -v '^CHANGELOG\.md$' \| wc -l)" -eq 0` |
| AC11 | CHANGELOG entry v1.6.2 lists 5-axis self-rating with projected-vs-honest delta ≤ ±0.5 total | Manual rubric review post-feat |
| AC12 | `master.md` pattern #4 data-point updated : **depth update on the sixth data-point** (v1.5.1 Layer A-only sixth). v1.6.2 is structurally the same Layer A-only mode as v1.5.1 — the work (runtime evidence capture vs paper-trace analysis) differs but the ripple class is identical (zero Layer B diff). Per v1.6.1 depth-update precedent (pattern #1 fourth, no new ordinal) : ripple-class continuity → depth update, not new ordinal. Ninth data-point is reserved for a genuinely new ripple mode. | `grep -c "depth update on the sixth data-point" master.md ≥ 1` |
| AC13 | Phase D Layer 0 sync : IF runtime surfaces GH_TOKEN-env-override pattern again (3rd data-point), amplify `workflow_github_and_tooling.md` to encode prefix as mandatory ; otherwise NO Layer 0 touch | Conditional ; idempotency marker `_v1_6_2_layer0_sync_DONE_2026-04-19.md` iff applied |
| AC14 | Self-rating HONEST post-runtime : streak ≥ 9.0 advances to **4 consecutive** (v1.5.1 = 9.12, v1.6.0 = 9.02, v1.6.1 = 9.18, v1.6.2 projected 9.14) OR honest deduction breaks streak with explicit honesty note | Manual |

## 4. Design

### 4.1 Fixture set

**Reused from `C:/tmp/genesis-v1.5.0-dryrun/`** (4 fixtures, already paper-traced v1.5.1) :
- Fixture A : minimal text-only drop
- Fixture B : multi-file populated drop (paper-trace happy path)
- Fixture C : re-run / supersession scenario
- Fixture D : SDK-absent edge (now collapses into generic internal-error per v1.5.1)

These run **dispatch-only** at runtime : spawn Claude Code session in the fixture cwd → user invokes `/genesis-drop-zone` → observer captures (a) invocation form ("bare" / "project-genesis:genesis-drop-zone" / mixed) and (b) first card rendered (welcome). Further progression optional — goal is to confirm Skill engine dispatches cleanly cross-fixture.

**New fixture — `alexandre_windows/`** at `C:/tmp/genesis-v1.6.2-alexandre/` :
- `config.txt` (3-4 lines, FR) — vision one-liner
- `catalogue_fenetres_fr.md` (~30 lines FR, markdown) — fake catalogue
- `specs_usine_pl.md` (~15 lines PL/EN mix) — fake factory specs
- `voice_memo_alexandre.txt` (~10 lines FR informel) — transcript
- `photo_facade_client.jpg` — binary artefact. **Scope note :** per the v1.4.0 Citations API contract in `SKILL.md § v1.4.0 in scope item #3`, binary image artefacts do NOT carry the `citations` flag and are excluded from the extraction prompt's `documents[]` list. The JPG exists solely to validate that Phase 0.1 welcome card acknowledges non-parseable drops without crashing. It MUST be a valid JFIF-headered JPG (not a zero-byte stub) ≥ 5 KB, generated via a small Python Pillow one-liner in the fixture-prep step. H2 arbitration evidence draws from the 4 text artefacts only ; H2 refutation on binary presence would be out-of-scope and logged as P3 polish.

**API-key-absent designation** : Fixture A is chosen for the EXIT_NO_KEY test (minimal text-only drop = clearest halt-card evidence, no confound from multi-artefact parsing).

### 4.2 Observation protocol

Per fixture, the observer (user in fresh Claude Code session) captures :

1. **Trigger phrase verbatim** — whatever natural phrase surfaced `/genesis-drop-zone` (or failed to).
2. **Invocation form** — bare vs namespaced vs none.
3. **First 1-2 cards rendered** — verbatim or summarized depending on length.
4. **Artefacts written** — `ls -la` after session closes, note `drop_zone_intent.md` + archive if present.
5. **Frictions** — any deviation from v1.5.1 paper-trace expectation, any error, any ambiguity.
6. **Redaction rules** — the evidence log is committed to git. Before pasting ANY transcript excerpt into the log, strip :
   - ANTHROPIC_API_KEY values (regex `sk-ant-[a-zA-Z0-9-_]+` → `sk-ant-REDACTED`)
   - Other API tokens / bearer tokens (regex `(?i)(api[_-]?key|token|bearer)[=: ]+['"\s]*[a-zA-Z0-9-_\.]{20,}` → redacted)
   - Absolute user paths outside fixture (regex `C:/Users/[^/]+/` → `C:/Users/REDACTED/`)
   - Email addresses (regex `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}` → `<email-redacted>`)
   - Anthropic Console deep-link tokens if captured from any error message (regex `/sessions/[a-zA-Z0-9-_]+` → `/sessions/REDACTED`)
   - Anthropic request-id in stderr (regex `req_[a-zA-Z0-9]+` → `req_REDACTED`)
   - Any stderr token-count line containing a request-specific opaque identifier.

   If in doubt, redact rather than ship. The runbook at `tests/runtime_dogfood_v1_6_2.md` mirrors these rules verbatim in its "Redaction rules" section per AC2.

### 4.3 Hybrid blocker gate (scope-expansion policy)

When a friction is observed at runtime, it routes into one of three classes :

| Class | Definition | Action |
|---|---|---|
| **A. Privilege-violation** | Observed skill behaviour violates a concentrated-privilege mitigation (consent bypass, disk write outside scope, unauthorized network call, halt-on-existing bypass). | **In-feat fix** in v1.6.2. Spec expansion explicitly authorized here. |
| **B. Prose-ambigu** | Prose in SKILL.md / phase-*.md creates real user confusion at runtime, but skill **functionally** respects privilege + contract. | **Log + defer** to v1.6.3. Evidence log records the observation. |
| **C. Structural / polish** | Wording, typo, minor consistency, idempotency-marker polish. | **Log + defer** to v1.6.3. |

The objective test for class A : "Did the skill do something the privilege contract forbids, OR did it skip a consent gate that privilege contract requires?" Yes = A. No = B or C.

### 4.4 Evidence capture files

- `skills/genesis-drop-zone/tests/runtime_dogfood_v1_6_2.md` — **runbook** (reusable for v1.6.3+ re-runs). Sections :
  - Pre-flight (API key check, Claude Code version check, git status clean in fixture cwd)
  - Per-fixture spawn + trigger + observe procedure (step-by-step, copy-pasteable)
  - Redaction rules (what to strip)
  - Re-run guidance (how to re-run post-friction-fix)
- `skills/genesis-drop-zone/tests/runtime_dogfood_evidence_v1_6_2.md` — **evidence log** (this session only ; future runs create `_v1_5_3.md` etc. per v1.6.1 pattern). Sections :
  - Per-fixture section × 5 : Trigger phrase used / Invocation form observed / Cards rendered / Artefacts written / Frictions found
  - Global H1-H5 confirmation table
  - Friction triage table (class A / B / C per § 4.3)
  - Deferred-friction queue (class B + C entries with proposed v1.6.3+ ship assignments)

### 4.5 Autonomous checkpoint shape

**Phase A (autonomous)** — before runtime :
- Spec + spec-reviewer polish
- Plan + plan-reviewer polish
- Fixture prep : create `alexandre_windows/` 5 artefacts
- Runbook stub written
- Evidence log stub written with all 5 fixture headers + H1-H5 table with empty cells
- `plugin.json` bump 1.6.1 → 1.6.2
- `master.md` pattern #4 depth-update on sixth data-point (per AC12)
- feat-core commit

**Phase A is explicitly forbidden from touching** : any `skills/<other-than-genesis-drop-zone>/` subtree, `skills/README.md`, `templates/`, `hooks/`, any Layer 0 file (Layer 0 sync is Phase D conditional per AC13). AC10 enforces at diff time.

**HALT at runtime gate** — user notified : "Phase A complete. Please spawn 5 fresh Claude Code sessions per runbook instructions and paste back evidence."

**Phase B (autonomous after evidence pasted)** — :
- Evidence log filled per pasted transcript data
- Hybrid gate triage (§ 4.3)
- If class A → fix edits + separate feat commit (not amend, per v1.5.1 precedent)
- If class B / C → deferred-queue populated
- feat-runtime commit (evidence log)
- PR + tag + chore

### 4.5.1 Partial-evidence branch (bounded user-failure mode)

If the user spawns fewer than 5 sessions and pastes back partial evidence :

1. **Evidence integrity gate** — Phase B does NOT commit feat-runtime if any of H1-H5 has zero evidence. Every hypothesis must have at least one observation (confirmed, failed, or explicitly-deferred with reason).
2. **Branch parking** — `plugin.json` bump and `master.md` depth-update stay on the feat branch unmerged. Tag `v1.6.2` NOT pushed. Branch remains forensic per R2.5.
3. **Fallback shipping** — if Phase B cannot complete within a reasonable timebox (user availability dependent), v1.6.2 defers to v1.6.3+ as a "v1.6.2-partial" with an explicit honesty note in CHANGELOG recording : (a) which fixtures completed, (b) which H rows remain empty, (c) why the partial ship is acceptable given what was learned.
4. **Re-run guidance** — the runbook already documents re-run protocol ; partial-to-complete re-continuation follows the same flow with the evidence log appended, not overwritten.

This branch handles the "user availability dependent" axis honestly — v1.6.2 is NOT ship-ready until H1-H5 have at minimum one observation each.

## 5. Scope expansion policy (§ 3 blocker taxonomy detail)

Per § 4.3 the in-feat scope can expand **only** for class A privilege-violation findings. The following ceiling applies :
- Max 2 class-A fixes bundled per v1.6.2 ship before the fix-PATCH itself becomes scope-unbounded. If 3+ class-A findings surface, ship v1.6.2 with the first 2 fixed + log remaining for **immediate** v1.6.3 PATCH chain.
- **Common-root-cause abort** — if the 3rd-or-later class-A finding shares a root cause with the first 2 (e.g., all 3 cluster on the same Phase 0.4 code path or consent gate), abort v1.6.2 and re-scope as a v1.6.3 unified fix instead of a chain ; the chain would ship a known-broken v1.6.2 for 1-2 days between PATCHes, whereas a deferred unified fix keeps the prior ship (v1.5.1) as the known-good head.
- Class-A fix commits stay separate from feat-runtime evidence commit (code reviewer + evidence reviewer stay cleanly-partitioned). Class-A fixes MAY touch `SKILL.md` prose, halt-card wording, or consent-gate logic, but MUST NOT touch `extract_with_citations.py` (out-of-scope per NG3 — extraction refactor is a separate spec class).
- CHANGELOG entry explicitly names each class-A fix + links to evidence log line(s).

## 6. Appendix A — Pre-registered hypotheses

| H | Pre-registered prediction | Refutation test |
|---|---|---|
| H1 | Claude Code skill engine dispatches `/genesis-drop-zone` on verbatim trigger phrase in each of the 5 fixture cwds (plugin installed) | Any fixture where dispatch fails → H1 refuted for that fixture, friction logged |
| H2 | Phase 0.4 arbitration card on `alexandre_windows` renders with `arbitrated_fields` list non-empty (multi-source drop) | Empty list → H2 refuted, arbitration logic paper-contract broken at runtime |
| H3 | Phase 0.5 Path 2a (first-write empty-divergences) renders the v1.3.2 consent card on at least 1 fixture | Zero consent cards observed → H3 refuted, v1.5.1 SKILL.md subsection lied |
| H4 | Fixture A with `ANTHROPIC_API_KEY` unset renders EXIT_NO_KEY halt card (FR or EN depending on locale) | No halt card OR wrong exit code → H4 refuted |
| H5 | `git diff --name-only main...feat/v1.6.2` shows zero Layer B files modified | AC10 machine check (§ 3). Any Layer B file diff line → H5 refuted, pattern #4 depth-update on sixth data-point fails |

**H5 is the structural hypothesis.** Its refutation test IS AC10 ; this symmetry is intentional. If H5 fails, the v1.6.2 ship self-discloses the failure in CHANGELOG and pattern #4 depth update does **not** land.

## 7. Running-average + streak context

- Running average post v1.6.1 honest : **8.90 / 10** (18 tagged ratings).
- Last 3 ships : v1.5.1 = 9.12, v1.6.0 = 9.02, v1.6.1 = 9.18 — streak ≥ 9.0 = 3 consecutive.
- v1.6.2 projected mean 9.14 — if honest, streak advances to 4. If honest deduction drops below 9.0, streak breaks but running average still advances (19th rating).
- Per v1.5.0 honest-correction precedent (Layer 0 `feedback_honest_self_rating_post_feat`), willingness to break streak if honest deduction warrants ≥ 0.2.

### 7.1 Axis projection (5-axis breakdown)

| Axis | Projected | Rationale |
|---|---|---|
| Pain-driven | 9.4 | Runtime evidence closes v1.5.0 paper-trace debt fully ; 2-cycle deferred gap fermé. Cap at 9.4 (not 9.5) — 1 of 5 fixtures uses synthetic Alexandre data rather than real-world drop. |
| Prose cleanliness | 9.0 | No large prose rewrites unless class-A blocker surfaces. Evidence log introduces new runtime-prose convention but bounded to `tests/` subtree. |
| Best-at-date | 9.0 | No new R8 commissioned ; existing R8 `living-memory-and-supersession-patterns_2026-04-18.md` still canonical for v1.5.x line arbitration design. Cap at 9.0 — runtime evidence does not move external SOTA frontier. |
| Self-contained | 9.2 | Layer A-only session, H5 enforces zero Layer B ripple. Cap at 9.2 (not 9.5) because the partial-evidence branch § 4.5.1 is a documented user-dependency that limits pure self-containedness. |
| Anti-Frankenstein | 9.1 | 5 fixtures ∝ 5 evidence classes (dispatch × 5 + full-path × 1 + EXIT_NO_KEY × 1, overlapping cleanly). No surplus artefacts. |
| **Mean** | **9.14** | Sum / 5 = 45.70 / 5 = 9.14. |

## 8. Out-of-scope follow-ups (candidate v1.6.3+)

- **Friction #3 retirement-trigger semantics** — v1.6.3 primary.
- **Adversarial arbitration stress fixture** — v1.6.3 or later.
- **fsync-then-rename atomic archive write** — v1.5.x or v1.6.x based on observed failure.
- **CI dogfood harness** — v1.6.x+ if manual runbook creates recurring friction.
- **Skill-tool plugin-installed runtime evidence (promptor)** — was originally named v1.6.2 in the v1.6.1 resume ; bumped to **v1.6.3** now that this ship takes the v1.6.2 slot. Remains a standalone candidate orthogonal to v1.5.x / v1.6.x runtime-dogfood work.
