<!-- SPDX-License-Identifier: MIT -->
---
name: Session v1.2.3 — gh active-account pre-flight at Phase 6.0
description: v1.2.3 ship session. Single P1 friction F34 landed as a 3-commit PR (feat Step 6.0, feat SKILL.md sync, chore version+archive+prose). Phase 6 now opens with a gh api user --jq .login check against the resolved target owner, an auto-switch attempt, and a halt-with-remediation on switch-failure. P1 queue from v1.2.0 now closed.
type: project
date: 2026-04-17
session: v1.2.3
branch: feat/v1.2.3-f34-gh-preflight
parent-tag: v1.2.2
parent-commit: 0094696
---

# Session v1.2.3 — gh active-account pre-flight at Phase 6.0

Direct follow-up to v1.2.2 (merged as PR #25, tagged `v1.2.2` on `ea25068` with chore resume prompt on `0094696`). Scope: the last P1 friction from the v1.2.0 self-dogfood log — F34 (`gh` active-account mismatch at PR create time). Path A from the v1.2.1 → v1.2.2 and v1.2.2 → v1.2.3 resume prompts, picked by the user at session open with the explicit framing that *the self-rating score reflects user experience, not vanity discipline* — so the three consecutive ≥ 9.0 ships are worth extending rather than pivoting to v2 Étape 0.

## What shipped

Three commits on `feat/v1.2.3-f34-gh-preflight` off `0094696`:

| Commit | Fix | Files changed |
|---|---|---|
| `bbffe35` | **F34 (Step 6.0 itself)** — `### Step 6.0 — gh active-account pre-flight` inserted at the opening of `phase-6-commit-push.md` before Step 6.1 pre-commit review | 1 file (`skills/genesis-protocol/phase-6-commit-push.md`) |
| `ea5163e` | **F34 (SKILL.md sync)** — `## Mode dispatch` Category A "Structural stops" row now lists Step 6.0 as a new entry alongside paradox guards, nested-repo halts, halt-on-leak, and failed probes | 1 file (`skills/genesis-protocol/SKILL.md`) |
| (pending) | **chore** — version bump `1.2.2` → `1.2.3`, CHANGELOG entry with 5-axis self-rating, R8 archive of two expired stack entries, this session trace, resume prompt v1.2.3 → v1.2.4 | 7 files |

Net diff for the feat commits alone: `+64 / −1` across 2 distinct files (the big 63-line block is Step 6.0 with its branching halt UX + Layer 0 note; the 1-line diff is the Mode dispatch Category A catalogue sync). The chore commit adds CHANGELOG, version, archive, and session artefacts — pure bookkeeping + prose, no runbook change.

## Why the bundle is one PR with three commits

Same rationale as v1.2.2: one root cause per commit, bundle into one PR so the reader sees the complete scope change in one merge. F34 has two runbook touchpoints — the step itself in the phase-6 runbook, and the canonical Category A catalogue in SKILL.md — and shipping them in separate PRs would leave the Category A catalogue temporarily out of sync (a v1.2.3-alpha PR would ship Step 6.0 without listing it in SKILL.md, which breaks the 1:1 mirror discipline even for one revision cycle).

The chore commit is the third because it carries the CHANGELOG entry that references both feat commits by their hash and needs them to exist first. It also does the housekeeping that does not warrant its own PR: archiving the two expired R8 stack entries (both skill-internal, neither refreshed because F34 does not depend on plugin SDK or JSONL shape) and bumping `plugin.json`.

## Verification walk-throughs (scenario replays)

### F34 — multi-account mismatch caught before any remote call

Replay scenario: user runs the orchestrator on a machine with two logged-in gh accounts (the Layer 0 `reference_accounts_orgs_and_projects.md` scope split makes this the norm, not the edge case). The active account is `myconciergerieavelizy-cloud` (another project's identity). The target repo resolves to owner `myconciergerie-prog`.

With new code: Phase 6 opens with Step 6.0. `git -C <target> remote get-url origin` returns `git@github.com-<alias>:myconciergerie-prog/<repo>.git`; the owner parse yields `myconciergerie-prog`. `gh api user --jq .login` returns `myconciergerieavelizy-cloud`. Mismatch detected. The orchestrator runs `gh auth switch -h github.com -u myconciergerie-prog`, re-runs `gh api user --jq .login`, sees `myconciergerie-prog`, surfaces a one-line note `gh active account switched to myconciergerie-prog for this Phase 6 run`, and proceeds to Step 6.1.

If `myconciergerie-prog` had not been logged in on the machine at all, the switch would have failed, Step 6.0 would halt with the `Remediation: gh auth login --web` block and the full `gh auth status` output for context. The user authenticates and re-invokes — Phase 6 resumes from Step 6.0 at the next run because the orchestrator's resume logic reads the git state to figure out the right phase anyway.

### F34 — mismatch in the v0.2.0+ PR pattern (extrapolation beyond bootstrap)

Replay scenario: a post-bootstrap session on the same multi-account machine wants to run `gh pr create` from a feat branch. Phase 6 runbook is Genesis-bootstrap-specific and does not run in a v0.2.0+ session. However, the fix informs the pattern: any session that touches `gh` on a multi-account machine should front-load the `gh api user --jq .login` vs git-remote-owner check.

A v1.3 candidate (flagged in the session trace and the CHANGELOG): mirror Step 6.0 as a rule-level check in `skills/genesis-protocol/rules/v1_rules.md` so the discipline applies to v0.2.0+ PR sessions in any Genesis-bootstrapped downstream project, not only to Phase 6 of the bootstrap itself. Explicitly out of scope for v1.2.3 per the surgical-commit discipline.

### Category A catalogue sync — SKILL.md reflects the new structural stop

Replay scenario: a future session reads `SKILL.md` looking for the full list of Category A structural stops that halt in every mode. Without the v1.2.3 sync, the reader would have to cross-check every phase runbook to find Step 6.0 — the 1:1 mirror between SKILL.md's dispatch table and the phase runbooks would silently drift. With the v1.2.3 sync, the Category A row lists `gh active-account mismatch at Phase 6 Step 6.0 when auto-switch fails (added v1.2.3 for F34)` alongside paradox guards, nested-repo halts, halt-on-leak, and failed probes — the catalogue is complete.

## What v1.2.3 intentionally does NOT fix

Per the v1.2.2 session trace deferral list, still outstanding after v1.2.3:

- **F24 Phase 0.1 git-aware inspection** — P2 cosmetic, F30 already covers the Phase 3 blocker case.
- **F25 / F31 config.txt canonical examples** — P2 doc work, best shipped as a chore PR (`templates/config-minimal.txt.example` + `templates/config-complete.txt.example`).
- **F26 non-canonical fields audit UI** — still half-fixed. The passthrough convention is documented in SKILL.md `## Arguments`; the actual `## Non-canonical fields (passed through)` write into `bootstrap_intent.md` at Phase 0.5 is still not explicit in the template.
- **F28 `genesis-cleanup` sibling skill** — P3.
- **F32 Python driver** — v1.3 target. The Markdown ceiling was again above v1.2.3's scope.
- **F33 R8 scope disambiguation** — P3.
- **gh auth pre-switch restore** — v1.3 candidate. Surfaced in the v1.2.3 Step 6.0 prose but not implemented (the current active account is not recorded at Step 6.0 for later restoration at Phase 7).
- **v0.2.0+ PR-session equivalent of Step 6.0** — v1.3 candidate. Mirrors the Step 6.0 check in `rules/v1_rules.md` so post-bootstrap sessions benefit too.

## Self-rating — v1.2.3

See CHANGELOG for the 5-axis table. Summary:

- **Pain-driven**: Step 6.0 implements the v1.2.0 friction-log fix sketch verbatim. The live reproducer from v1.2.1's own PR creation is directly addressed. Zero speculative additions.
- **Anti-Frankenstein**: no Python driver, no retry loop, no hook wiring. Three commits, 64 + 1 + prose lines across 2 runbook files + CHANGELOG + version + archive + session trace + resume prompt. v0.2.0+ rule-level extension explicitly deferred to v1.3.
- **Self-contained**: SKILL.md remains the single source of truth for the Category A catalogue; the phase-6 runbook is the single source of truth for Step 6.0's behaviour. Owner resolution uses three existing-artefact sources without introducing a new contract.
- **Prose**: each feat commit has a 3-paragraph narrative body with root cause + mechanism + scope boundary; the chore commit body names the three scopes bundled in it (version, CHANGELOG, archive+prose).
- **Best-at-date**: `gh api user --jq .login` and `gh auth switch -h github.com -u <user>` are the established gh CLI primitives. Two expired stack entries archived as bookkeeping without refresh — same stance as v1.2.2 because F34 does not depend on plugin SDK or JSONL shape.

## Running average post-v1.2.3

v0.2 → v1.2.2 running average was 8.68/10. v1.2.3 self-rating is 9.18/10, bringing the running average to **8.71/10** (up from 8.68, well above the 8.5 v1 target, comfortably inside the anti-Frankenstein inflection-point budget). Three consecutive ships scoring ≥ 9.0 (v1.2.1 9.26, v1.2.2 9.14, v1.2.3 9.18) — the surgical one-root-cause-per-commit / bundle-in-one-PR discipline continues to hold.

## P1 queue status

**CLOSED after v1.2.3.** Every P1 friction from the v1.2.0 self-dogfood log has now landed:

- F23 + F27 + F29 + F30 (P0 paradox guards + self-contained rules + git-aware probe) → v1.2.1
- F20 + F21 + F22 (P1 mode-auto semantics + Arguments schema + Step 0 consent dispatch) → v1.2.2
- F34 (P1 gh active-account pre-flight) → v1.2.3

The next-severity band is P2 doc work (F25/F31 config.txt canonical examples) or the **v2 Étape 0 drop-zone pivot** — the research cache `v2_promptor_fusion_landscape_2026-04-17.md` is still fresh (expires 2026-04-24) and the mental mode switch from v1.2.x refinement to v2 feature work is now the natural next boundary.

## Next session entry point

`.claude/docs/superpowers/resume/2026-04-17_v1_2_3_to_v1_2_4_or_v2_etape_0.md` (written at the end of this session). Resume prompt frames the v1.2.4-or-v2 choice: v1.2.4 would be P2 doc work (config examples, `genesis-cleanup`) or a rule-level v0.2.0+ equivalent of Step 6.0; v2 Étape 0 would be the drag-and-drop drop-zone that surfaces as Étape 0 of the Promptor fusion. The research cache freshness gives runway for either path.
