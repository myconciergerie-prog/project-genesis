<!-- SPDX-License-Identifier: MIT -->
---
name: Session v1.2.4 — R2.3.1 gh active-account pre-flight (F34 rule-level mirror)
description: v1.2.4 ship session. Two-commit bundle in one PR landing the rule-level mirror of v1.2.3 Step 6.0. R2.3.1 added under R2.3 PR & merge in skills/genesis-protocol/rules/v1_rules.md so every v0.2.0+ post-bootstrap PR session in every Genesis-bootstrapped project inherits the same gh active-account pre-flight discipline that Step 6.0 introduced for the bootstrap run itself.
type: project
date: 2026-04-17
session: v1.2.4
branch: feat/v1.2.4-rule-gh-preflight
parent-tag: v1.2.3
parent-commit: 316937c
---

# Session v1.2.4 — R2.3.1 gh active-account pre-flight (F34 rule-level mirror)

Direct follow-up to v1.2.3 (merged as PR #26, tagged `v1.2.3` on `5b8179e` with chore resume pointer on `316937c`). Scope: the last P1-adjacent pain flagged in v1.2.3's own self-rating prose — the bootstrap-only coverage of F34 left every v0.2.0+ post-bootstrap PR session in every Genesis-bootstrapped project uncovered. Path A from the v1.2.3 → v1.2.4/v2-étape-0 resume prompt, picked by the user at session open after the two-path proposal with the "reco" shorthand accepted for Path A.

## What shipped

Two commits on `feat/v1.2.4-rule-gh-preflight` off `316937c`:

| Commit | Fix | Files changed |
|---|---|---|
| `c4464d5` | **F34 rule-level mirror** — new `### R2.3.1 gh active-account pre-flight (before any gh write — added v1.2.4)` under R2.3 in `skills/genesis-protocol/rules/v1_rules.md`. Two cross-ref parentheticals added to the R2.3 PR & merge bullets pointing at R2.3.1. | 1 file (`skills/genesis-protocol/rules/v1_rules.md`) |
| (pending) | **chore** — version bump `1.2.3` → `1.2.4`, CHANGELOG entry with 5-axis self-rating, this session trace, MEMORY.md pointer, resume prompt v1.2.4 → v1.2.5 or v2 Étape 0. | 5 files |

Net diff for the feat commit: `+61 / −2` on the single rules file — 2 bullet-line changes in R2.3 plus the ~60-line R2.3.1 section insert. The chore commit adds CHANGELOG, version, session artefacts + MEMORY.md index line + resume prompt — pure bookkeeping + prose, no rule or runbook change.

## Why one-fix / two-commits / one PR

Same discipline as v1.2.2 and v1.2.3: one root cause per commit, bundle into one PR so the reader sees the full scope change in one merge. Here the feat / chore split is the cleanest decomposition because:

- R2.3.1 is a single additive sub-rule — no second root cause to separate out. (No SKILL.md sync here as in v1.2.3 because R2.3.1 is not a structural stop of the `genesis-protocol` skill itself — it's a project-level rule that the skill's downstream-bootstrapped outputs inherit. SKILL.md's Mode dispatch Category A catalogue is scoped to the orchestrator skill, not to the rules a downstream project applies in its own sessions.)
- The chore commit carries the CHANGELOG entry that references the feat commit by hash and needs it to exist first. It also bundles version bump, session trace, MEMORY.md pointer update, and next resume prompt — all housekeeping that does not warrant its own PR.

## Verification walk-throughs (scenario replays)

### R2.3.1 — v0.2.0+ PR session on a multi-account machine

Replay scenario: a maintainer of a Genesis-bootstrapped downstream project (e.g. `atelier-playmobil`) runs `gh pr create` from a feat branch. Their machine has two logged-in gh accounts (personal + project-bound), and the active one is the personal account. The target repo owner (parsed from `git remote get-url origin`) is the project-bound account.

With R2.3.1 in the project's rules (inherited via the v1_rules.md template landed at Phase 1 of their bootstrap): the pre-flight runs before `gh pr create` is invoked. `target_owner` resolves from the git remote SSH form `git@github.com-<alias>:<owner>/<repo>.git`. `current_login` returns the personal account. Mismatch detected. `gh auth switch -h github.com -u <target_owner>` runs, re-verification returns `<target_owner>`, one-line note surfaces, `gh pr create` proceeds.

If the project-bound account had not been logged in on that machine at all, the switch would have failed. R2.3.1 halts with the `gh auth login --web` remediation block and the full `gh auth status` output — same halt surface as Step 6.0 from v1.2.3.

### R2.3.1 — identical to Step 6.0 in branches, simpler in owner resolution

The halt / auto-switch / re-verification branches in R2.3.1 are **byte-for-byte structurally identical** to Step 6.0 (same halt templates with `❌ R2.3.1 …` vs `❌ Step 6.0 …` as the only difference). The explicit "Relation to bootstrap Step 6.0" paragraph in R2.3.1 declares the 1:1 correspondence and commits future maintainers to reviewing both when either is touched. This is the 1:1 mirror discipline applied to a rule / runbook pair (not just within a SKILL.md / source-spec pair as it was for the three existing 1:1 mirror precedents).

Owner resolution is where the two diverge by design: Step 6.0 uses three fallbacks (git remote → `bootstrap_intent.md` → Step 0 consent card) to handle the pre-Phase-3.5 bootstrap ordering when no remote is configured yet; R2.3.1 uses only the git remote because v0.2.0+ sessions always have a remote (that's what makes them v0.2.0+). Collapsing the fallbacks in R2.3.1 is not a shortcut — it's the correct scoping.

### Scope and exemptions

Applies to every `gh` write op — `gh pr create`, `gh pr merge`, `gh release create`, `gh repo <write-verb>`, and any future `gh` command that mutates remote state. Read-only calls (`gh api user`, `gh auth status`, `gh repo view`) are exempt because they cannot surface the `must be a collaborator` error that motivates the rule. Explicitly naming the exemption in R2.3.1 prevents future over-application that would slow down every `gh api user` call.

## What v1.2.4 intentionally does NOT fix

Same deferral list as v1.2.3, now with F34 definitively closed at both bootstrap and v0.2.0+ levels:

- **F24 Phase 0.1 git-aware inspection** — P2 cosmetic, F30 already covers the Phase 3 blocker case.
- **F25 / F31 config.txt canonical examples** — P2 doc work, best shipped as a chore PR (`templates/config-minimal.txt.example` + `templates/config-complete.txt.example`).
- **F26 non-canonical fields audit UI** — still half-fixed since v1.2.2. The passthrough convention is documented in SKILL.md `## Arguments`; the actual `## Non-canonical fields (passed through)` write into `bootstrap_intent.md` at Phase 0.5 is still not explicit in the template.
- **F28 `genesis-cleanup` sibling skill** — P3.
- **F32 Python driver** — v1.3 target. The Markdown ceiling was again above v1.2.4's scope.
- **F33 R8 scope disambiguation** — P3.
- **gh auth pre-switch restore** — v1.3 candidate. The current active account is still not recorded at Step 6.0 / R2.3.1 for later restoration. Out of scope here to keep the surgical discipline intact.

## Self-rating — v1.2.4

See CHANGELOG for the 5-axis table. Summary:

- **Pain-driven**: R2.3.1 closes the exact downstream gap flagged in the v1.2.3 session trace — "the original failure surface (Genesis repo's own PR work) is still uncovered by anything but a verbal reminder". Small deduction because this is downstream prevention rather than an active live reproducer (the live reproducer on Genesis itself was during v1.2.1, which the v1.2.3 bootstrap fix partially-but-not-fully addressed).
- **Anti-Frankenstein**: one feat commit (61 insertions + 2 deletions in one file) plus one chore commit for bookkeeping. Explicit 1:1 mirror with Step 6.0 rather than inventing new semantics. No Python driver, no retry loop, no hook wiring. The 1:1 mirror declaration itself prevents future drift without adding machinery.
- **Self-contained**: R2.3.1 fits under R2.3 as a proper sub-rule. Owner resolution is a single `sed` pipe over `git remote get-url origin`. The "Relation to bootstrap Step 6.0" paragraph is the anti-drift hook that makes the rule maintain itself by reference.
- **Prose**: ~60 lines, proportionate to Step 6.0's 63 lines with structurally identical branches. Halt templates are copy-paste-ready. Mode dispatch paragraph is explicit.
- **Best-at-date**: `gh api user --jq .login` + `gh auth switch -h github.com -u <user>` are the established gh CLI primitives. No research refresh needed — primitives already validated in v1.2.3. The cache entry `gh-cli-single-click-auth_2026-04-16.md` is still fresh (expires 2026-04-23) and remains relevant as the prior art for the broader gh auth landscape.

## Running average post-v1.2.4

v0.2 → v1.2.3 running average was 8.71/10. v1.2.4 self-rating per the 5-axis table in CHANGELOG lands at **9.16/10**, bringing the running average to **8.74/10** (up from 8.71, well above the 8.5 v1 target, comfortably inside the anti-Frankenstein inflection-point budget). **Four consecutive ships scoring ≥ 9.0** (v1.2.1 9.26, v1.2.2 9.14, v1.2.3 9.18, v1.2.4 9.16) — the surgical one-root-cause-per-commit / bundle-in-one-PR discipline continues to hold, and the 1:1 mirror discipline extended cleanly from SKILL.md/spec pairs to rule/runbook pairs without changing the rhythm.

## P1 queue status — second closure

**CLOSED and reinforced.** v1.2.3 closed the P1 queue at the bootstrap level by shipping Step 6.0 for F34. v1.2.4 closes the same P1 at the v0.2.0+ rule level by shipping R2.3.1 as Step 6.0's rule-level mirror. The P1 pain surface is now covered at both levels — bootstrap runbook AND downstream-project rules. Any future F34-type recurrence would require a new pain point, not a missing coverage.

The next-severity band remains P2 doc work (F25/F31 config.txt canonical examples) or the **v2 Étape 0 drop-zone pivot** — the research cache `v2_promptor_fusion_landscape_2026-04-17.md` is still fresh (expires 2026-04-24, 6 days of runway after v1.2.4 ship). The resume prompt written at the end of this session frames the choice: v1.2.5 (P2 doc work, narrower than v1.2.4) OR v2 Étape 0 (mental mode switch, now with P1 coverage at both levels definitively closed).

## Next session entry point

`.claude/docs/superpowers/resume/2026-04-17_v1_2_4_to_v1_2_5_or_v2_etape_0.md` (written at the end of this session). Resume prompt frames the v1.2.5-or-v2 choice: v1.2.5 would be P2 doc work (config examples, `genesis-cleanup`) or R8 cache scope disambiguation; v2 Étape 0 would be the drag-and-drop drop-zone that surfaces as Étape 0 of the Promptor fusion. The research cache freshness gives runway for either path.
