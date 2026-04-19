<!-- SPDX-License-Identifier: MIT -->
---
name: v1.5.1 implementation plan — dogfood + prose corrections
description: Step-by-step execution plan for v1.5.1 PATCH per `specs/v1_5_1_dogfood_and_prose.md`. Hard-ordered 3 → 1 → 2. Timeboxed dogfood at 2h with explicit fallback rules. Six-commit rhythm (spec / plan / plan-polish / dogfood-archive / feat / chore) matching v1.4.2 precedent.
type: plan
spec: specs/v1_5_1_dogfood_and_prose.md
target_ship: 2026-04-19
---

# v1.5.1 — Implementation plan

## Commit rhythm

Matches v1.4.2 / v1.5.0 precedent (six commits, possible plan polish):

1. `spec: v1.5.1 dogfood + prose corrections` (already in branch as `84048ef`)
2. `plan: v1.5.1 implementation plan` (this file)
3. `plan-polish: <if reviewer finds gaps>` (0-2 times)
4. `archive: dogfood v1.5.0 runtime — <ts>`
5. `feat: v1.5.1 — Phase 0.5 clarification + halt card collapse`
6. `chore(memory): v1.5.1 — CHANGELOG honesty + session trace + MEMORY + resume`

PR opens after commit 5 (feat). Chore commit post-merge on main per R2.4.

## Working directory

Worktree `C:/Dev/Claude_cowork/project-genesis/.claude/worktrees/v1.5.1-dogfood-and-prose/` branch `feat/v1.5.1-dogfood-and-prose` from main at `a0886bf`.

Fixture staging `C:/tmp/genesis-v1.5.0-dryrun/` — temporary, gitignored. Observed evidence is copied into `memory/project/dogfood_v1.5.0_<ts>/` under the worktree before the `archive:` commit.

## Step-by-step

### Step 1 — Plan review (now)

Invoke code-reviewer agent on this plan before execution. Land P0+P1 advisories via plan-polish commit. ≤ 2 polish passes per R10.

### Step 2 — Fixture preparation (~20 min)

Create `C:/tmp/genesis-v1.5.0-dryrun/` with four subdirectories per spec § Design:

- `scenario_retirement/` — `config.txt` + `brief.md` (intra-drop contradictions on budget + visibility) + pre-existing `drop_zone_intent.md` (budget=null-class for Completion, visibility=populated for Retirement, `snapshot_version: 1` for v1.4.x legacy compat test).
- `scenario_first_write/` — `config.txt` + `brief.md` (internally consistent, no pre-existing intent file).
- `scenario_halt_no_key/` — same shape as `first_write/`. Runtime: `ANTHROPIC_API_KEY` unset (already the default — verified 2026-04-19 in bash).
- `scenario_halt_no_sdk/` — same shape. Runtime: invoke via a throwaway venv at `C:/tmp/genesis-v1.5.0-dryrun/.venv-no-sdk/` that is created without installing `anthropic`. PYTHONPATH-mask on Windows is fragile due to site-packages precedence; venv is the canonical isolation. Document the venv creation command in the dogfood archive.

All seed file contents are hand-authored, ≤ 50 lines per file, deliberately simple so the dispatch logic is isolated as the test variable.

### Step 3 — Dogfood runtime execution (~90 min, hard cap 2h)

For each fixture scenario, execute the following protocol:

1. `cd C:/tmp/genesis-v1.5.0-dryrun/<scenario>/`.
2. Invoke `/genesis-drop-zone` from within Claude Code (current session suffices — the skill is loaded).
3. Observe each rendered surface: welcome box, mirror, Phase 0.4 stderr logs (if any), Phase 0.5 arbitration card (if any), v1.3.2 consent card (if any), write operation, halt card (if applicable).
4. Record per fixture in `memory/project/dogfood_v1.5.0_<YYYY-MM-DD>/fixture_<name>.md`:
   - Timestamp of invocation.
   - Which surfaces rendered, in which order.
   - Frontmatter of any file written (byte-level accurate — read with `cat` and paste).
   - stderr output verbatim.
   - Any ambiguity / friction / SKILL-prose-diverges-from-observed-behaviour.
5. If a surface's behaviour is ambiguous even after direct observation (e.g., "is this the v1.3.2 consent card or a Phase 0.5 card with zero-divergences-edge-case?"), mark it as a `structural` friction and annotate which hypothesis (H1-H4 from spec Appendix A) it bears on.

Aggregate findings into `memory/project/dogfood_v1.5.0_<YYYY-MM-DD>/friction_log.md` after all fixtures executed. Schema per § Design:

```markdown
## Friction N — <1-line summary>
severity: blocker | structural | polish
candidate_mapping: 1 | 2 | 3 | neither
fixture: <scenario name>
observation: <2-3 lines, direct quote or file path reference>
proposed_fix: <1-3 lines>
hypothesis_bearing: H1 | H2 | H3 | H4 | none
```

If the 2h timebox elapses with unexecuted fixtures, record them in `friction_log.md` as `## Fixture X — NOT EXECUTED (timebox exceeded)` and shape the corresponding Candidate-1/2 surface per spec's timebox-exceeded rule.

**Handling of api-key-required paths** (P1-b discipline branch):

1. **First pass** — invoke Fixtures A and B with `ANTHROPIC_API_KEY` unset (current session state). Observe what the skill does. This is the honest baseline of what Victor experiences without a key.
2. **If both A and B route to halt-no-key** (fallback retired per v1.5.0), the Phase 0.4 / Phase 0.5 / archive / v1.3.2-consent-card surfaces are unreachable without an API key — this IS itself a structural friction (candidate_mapping=1, bearing on H1) and gets logged.
3. **Branch point**: ask the user to provide `ANTHROPIC_API_KEY` for one re-run of Fixtures A + B so the non-halt flow can be observed at runtime. If the user declines or the key is unavailable, accept that [A2] will cite halt-path evidence only and **explicitly mark non-halt paths as "not dogfood-validated" in shipped prose** per spec timebox-exceeded rule. No silent assumption, no confirmation bias disguised as evidence.
4. **If the skill gracefully degrades to v1.3.3 in-context extraction** (hypothesis H0 — not pre-registered), log a structural friction since this contradicts the v1.5.0 retirement-of-fallback statement. Candidate-1 prose must surface this divergence.

This environmental constraint is a dogfood finding in its own right and gets logged regardless of which branch runs.

**H2 coverage (byte-identical re-run short-circuit)**: after Fixture B first-write completes (or first-write is verified non-halt), run Fixture B a **second time** in the same directory without altering the seed files. This exercises the re-run-no-change path — either H2 confirmed (dispatch short-circuits, no new archive entry) or refuted (overwrite happens anyway). If time pressure prevents the second pass, record H2 as `deferred — Fixture B re-run not executed within timebox` in friction_log.md per [A1].

### Step 4 — Dogfood archive commit (~10 min)

Stage all files under `memory/project/dogfood_v1.5.0_<YYYY-MM-DD>/`. Commit message template:

```
archive: dogfood v1.5.0 runtime — <N fixtures executed / M frictions>

Runtime dogfood of v1.5.0 Phase 0.4 + Phase 0.5 + archive write + halt
card paths per v1.5.1 spec Candidate 3. <N> fixtures executed within
2h timebox; <M> frictions logged. Severity breakdown: <X blocker, Y
structural, Z polish>. Candidate-1 hypothesis H1 <confirmed |
refuted | refined>; Candidate-2 hypothesis H3 <confirmed | refuted>;
H2 <confirmed | refuted | deferred>; H4 <confirmed | refuted>.
<any blocker callout>.
```

**Blocker halt rule**: if the severity breakdown contains `X ≥ 1` blocker (per spec § Scope blocker taxonomy — data-destructive behaviour, silent no-op on consent card, Phase 0.5 renders zero surface when divergences present, Phase 0.4 writes to wrong filesystem location, Layer B parser crashes), do NOT proceed to Step 5. Halt the ship, renegotiate scope explicitly with user. The `archive:` commit may still land (evidence is worth preserving) but the v1.5.1 line pauses until the blocker is triaged — possible outcomes: emergency patch ship of just that blocker; scope bump to v1.5.2 bundling the blocker fix with more work; outright revert of the v1.5.0 surface involved.

### Step 5 — Candidate 1 feat edit (~30 min)

Open `skills/genesis-drop-zone/SKILL.md`. Locate the end of `## Living memory dispatch (v1.5.0)` (line ~420). Insert new subsection `### Consent-card interaction with Phase 0.5 (v1.5.1 clarification)` BEFORE `## Phase 0 — welcome`.

Prose content shaped per spec discipline constraint:

- Must cite at least one fixture scenario name from `memory/project/dogfood_v1.5.0_<YYYY-MM-DD>/`.
- Must include at least one grep-able observed-behaviour line (stderr quote, rendered-card excerpt, frontmatter key presence).
- If H1 confirmed, prose says so and cites. If refuted, prose reflects the observed canonical flow.
- If zero friction observed, prose explicitly states "all three paths behaved per pre-registration; clarification added for future readers rather than to correct observed divergence".

### Step 6 — Candidate 2 feat edit (~30 min)

Open `skills/genesis-drop-zone/phase-0-welcome.md`. Delete the bilingual templates for the merged exit codes (exits 4, 5, 6, 7 by default — narrowed per Fixture D outcome). Add one new bilingual pair for the generic internal-error card with body content from spec § Design Candidate 2.

Open `skills/genesis-drop-zone/SKILL.md`. Collapse the 6-row halt table (lines ~406-413) to the new row count (3 rows default, 2 rows if Fixture D triggers the `EXIT_SDK_MISSING` collapse). Update the section-heading count in prose ("six halt cards" → "three halt cards" or similar).

Verify via grep that `scripts/extract_with_citations.py` is unchanged (zero-line diff per [A4]).

### Step 7 — Version bump + reviewer pass (~15 min)

Edit `.claude-plugin/plugin.json`: `"version": "1.5.0"` → `"version": "1.5.1"`.

Invoke code-reviewer agent on the feat diff before commit. Land P0+P1 advisories in-commit (rewrite before commit) rather than via second commit, matching v1.4.2/v1.5.0 discipline.

**Reviewer-P0 loopback rule** (P1-c):
- If reviewer finds a P0 that is PROSE-LEVEL (wording, missing cite, structural inconsistency with spec), rewrite prose in-place and re-invoke reviewer. No fixture re-observation needed.
- If reviewer finds a P0 that requires RE-OBSERVING a fixture (e.g., "Candidate 1 prose cites Fixture A but the fixture logs show Fixture A was never executed beyond welcome"), loop back to Step 3 for that single fixture IF residual timebox allows (budget = 2h − time already consumed in Step 3). If residual ≤ 15 min, the prose for the affected surface gets rewritten to "not dogfood-validated" with explicit honesty marker, and the ship proceeds with the reduced-evidence claim. No silent re-observation, no dogfood-without-timebox.

### Step 8 — Feat commit + push + PR (~20 min)

Commit template:

```
feat: v1.5.1 — Phase 0.5 clarification + halt card collapse

Closes v1.5.0 three-gap honesty correction (Candidates 1 + 2 from
2026-04-19 resume; Candidate 3 = dogfood runtime evidence committed
as `archive:` preceding this commit).

[Candidate 1] SKILL.md Living memory dispatch section gains
subsection "Consent-card interaction with Phase 0.5 (v1.5.1
clarification)" citing <fixture scenario name> runtime observation.
H1 <confirmed | refuted | refined>.

[Candidate 2] Halt-card taxonomy collapsed from 12 variants (6
cards × 2 langs) to <N> variants (<N/2> cards × 2 langs).
EXIT_NO_KEY retained; EXIT_SDK_MISSING <retained | collapsed>;
exits 4-7 merged into generic internal-error card. Extractor
script unchanged (6 exit codes preserved, collapse at render layer
only). stderr diagnostic fidelity preserved for Victor.

plugin.json 1.5.0 → 1.5.1. Zero Layer B ripple (genesis-protocol
byte-identical). Zero schema bump. Zero privilege change.

Acceptance per spec: [A1] <N> frictions logged, [A2] prose cites
<fixture>, [A3] halt variants <N>, [A4]-[A7] pass.
```

R2.3.1 pre-flight: `gh api user --jq .login` must return `myconciergerie-prog` before `gh pr create`.

PR title: `v1.5.1 — dogfood + Phase 0.5 clarification + halt card collapse (PATCH)`.

### Step 9 — PR merge + tag (~10 min)

Squash merge on GitHub. Tag `v1.5.1` on main after merge. Push tag.

### Step 10 — Chore commit (~20 min)

On main (checkout worktree back to main or new branch per R2.4):

- `CHANGELOG.md` — v1.5.1 entry with HONEST post-feat self-rating per [A8]. Axis breakdown + deduction cause if projection diverged ≥ 0.2.
- `memory/MEMORY.md` — add pointer to session trace.
- `memory/project/session_v1_5_1_<slug>.md` — session narrative.
- `.claude/docs/superpowers/resume/2026-04-19_v1_5_1_to_v1_5_2_or_v1_6_0.md` — handoff resume.
- Open PR for chore (separate from feat PR), squash merge.

**R2.3.1 pre-flight BEFORE chore PR open** (P1-a): re-run `gh api user --jq .login` and verify it returns `myconciergerie-prog`. Session-open flip-back to `avelizy-cloud` happens per resume; cannot assume the Step 8 switch persisted to Step 10. If the check fails, `gh auth switch --user myconciergerie-prog` and re-verify. Without this, [A10] ships silently to the wrong owner's namespace.

## Risk register

- **Environmental risk**: `ANTHROPIC_API_KEY` absent means happy-path fixtures (A, B) cannot reach real extraction runtime. Mitigated by treating this as the first dogfood finding (documented, not worked around) — drives the Candidate 1 prose if Phase 0.4 / 0.5 are unreachable without API key.
- **Timebox risk**: dogfood exceeds 2h. Mitigated by spec's timebox-exceeded rule — unexecuted fixtures labelled, shipped prose gains "not dogfood-validated" marker on affected surfaces.
- **Scope drift risk**: dogfood surfaces a Layer B friction. Mitigated by spec's explicit defer-to-v1.5.2 rule (unless blocker).
- **gh auth drift**: session-open `gh` active flips to `avelizy-cloud`. Mitigated by R2.3.1 re-verification at Step 8.
- **Hypothesis confirmation bias**: I wrote the pre-registration; I might interpret ambiguous fixture observations as "confirmed" when they're ambiguous. Mitigated by requiring grep-able evidence line in shipped prose — if I can't point to a specific stderr output or frontmatter line, the hypothesis stays "unconfirmed" regardless of my reading.

## Out of plan

- Layer B edits. If Layer B bug surfaces, defer unless blocker.
- New bilingual pairs. Net delta is negative.
- Cross-skill pattern edits. Four patterns stable.
- v1.6.0 Promptor scaffolding. Next ship, not this one.
