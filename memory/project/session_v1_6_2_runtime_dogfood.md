<!-- SPDX-License-Identifier: MIT -->
---
name: Session v1.6.2 runtime dogfood — 2026-04-19
description: Ship originally scoped v1.5.2 back-insert on v1.5.x line, retitled v1.6.2 forward-increment after plan-reviewer surfaced plugin.json already at 1.6.1. Runtime dogfood automated via `claude -p --plugin-dir <worktree>` subprocess calls (~$3.19 / 7.6 min for 8 runs). H1-H4 formally unable-to-test due to 5-friction cluster ; F5 SPDX-comment-before-frontmatter is universal Genesis-owned load-failure affecting every new marketplace install. Honest 8.96/10 breaks streak ≥ 9.0 at 3 consecutive.
type: project
version: v1.6.2
pr: "#45"
merge_commit: 025ad1b
tag: v1.6.2
predecessor: v1.6.1 (2d634b9)
---

# Session v1.6.2 — Runtime dogfood — 2026-04-19

## What shipped

**Tag v1.6.2** (PR #45 squash-merged as `025ad1b`). **Second PATCH on v1.6.x line.** Originally scoped as v1.5.2 back-insert (close v1.5.0 paper-trace debt) ; retitled v1.6.2 forward-increment after plan-reviewer surfaced `plugin.json` already at 1.6.1 semver reality. WORK identical (runtime dogfood drop-zone surface + Alexandre multi-language fixture).

**8 commits in feat tranche** (squash-merged) :

1. **Spec commit `9644052`** — 157-line spec (14 ACs, 5 pre-registered hypotheses, hybrid blocker gate class A/B/C taxonomy).
2. **Spec-polish commit `891fdf7`** — 4 P1 + 5 P2 fixes from spec-reviewer pass.
3. **Plan commit `72fb565`** — 643-line plan (13 tasks Phase A + B + C + D + E).
4. **Retitle commit `968bd93`** — v1.5.2 → v1.6.2 rename post plan-reviewer P0 (plugin.json 1.6.1 ≠ 1.5.1).
5. **Plan-polish commit `3b9da4d`** — 2 P0 (Pillow precondition + retitle) + 6 P1 + 5 P2 + 3 P3 fixes from plan-reviewer.
6. **Feat-core commit `db0749f`** — 5-artefact Alexandre fixture + runbook + evidence stub + plugin.json 1.6.1 → 1.6.2 + master.md pattern #4 depth-update on sixth data-point + AC10 grep = 0 verified.
7. **Fixture-rename commit `95df7f0`** — reconcile fixture_A/B/C/D → scenario_halt_no_key / scenario_first_write / scenario_retirement / scenario_halt_no_sdk per actual v1.5.0 dryrun disk names.
8. **Runbook-polish commit `2d3fe7d`** — `--plugin-dir` pre-check added after discovery that user has stale v1.1.0 user-scope install.
9. **Feat-runtime commit `2677b65`** — initial evidence from 7 runs (5 fixtures + 2 controls).
10. **Feat-runtime-amend commit `cc00427`** — Path B additional findings F4 (user-scope shadow) + F5 (SPDX-frontmatter universal break).

## Why — runtime dogfood methodology

The ship's pain-driven target was to close v1.5.0's paper-trace dogfood debt with real runtime evidence. User's "automatise moi tout ça" pivot during Phase A turned the method from manual 5-session spawns to automated subprocess calls via `claude -p --plugin-dir <worktree> --output-format=json --dangerously-skip-permissions "<trigger>"`. This cut user involvement to brainstorm + reviewer Q&A gates only ; actual evidence capture ran autonomously.

## Architecture decisions (brainstorming resolved)

**Q1 — Fixture set** → Option B : 4 v1.5.0 dryrun + 1 new alexandre_windows full happy-path.
**Q2 — Evidence depth** → Option B : dispatch × 5 + full-happy-path on alexandre.
**Q3 — Blocker policy** → Option C : hybrid gate (class A privilege-violation in-feat / B prose-ambigu defer / C polish defer).
**Q4 — API key strategy** → Option B + real API calls : 4 happy with key + 1 unset for EXIT_NO_KEY test.
**Q5 — Alexandre composition** → Option B : 5-artefact messy realistic (config + catalogue FR + specs PL + voice-memo + JPG via Pillow).

## Spec + plan reviewer findings summary

- **Spec reviewer** : 4 P1 (AC10 whitelist incomplete + invalid bash, AC10 Layer-B-specs glob too broad, JPG placeholder incoherent, § 4.2 redaction under-specified) + 5 P2 + 3 P3. APPROVED-WITH-POLISH-BUNDLE. All P1+P2 landed in `891fdf7`.
- **Plan reviewer** : **2 P0** (plugin.json version reality = 1.6.1 NOT 1.5.1 ; Pillow not installed on host) + 6 P1 (fixture content literals needed ; TBD grep gate ; master.md Edit old_string literal ; NG3 boundary check ; placeholder-substitution discipline ; ship-gate partition) + 5 P2 + 3 P3. APPROVED-WITH-POLISH-BUNDLE. Retitle commit `968bd93` addressed P0.1. Plan-polish `3b9da4d` addressed P0.2 + all P1+P2+P3.

## Runtime evidence findings (Path A + Path B)

**Path A initial run** (5 fixture subprocess + 2 controls, $2.78, ~7 min) surfaced :
- **F1** (class B, methodology) — `--plugin-dir` doesn't shadow same-named stale install ; even `plugin disable` doesn't help.
- **F2** (class B, methodology) — `-p` single-shot can't multi-turn.
- **F3** (class C, insight) — freelance Claude matches arbitration quality.

**Path B isolation attempt** (3 additional runs + uninstall + rm cache + reinstall, $0.41, ~30 s) surfaced :
- **F4** (class B, structural — Claude Code CLI) — user has 6 Genesis skills at `~/.claude/skills/` personal-scope, shadowing plugin loads entirely.
- **F5** (class B, structural — **Genesis-owned UNIVERSAL**) — every SKILL.md (all 8) starts with `<!-- SPDX-License-Identifier: MIT -->` before `---` delimiter. `claude plugin validate` reports "No frontmatter block found" for ALL 8. Fresh marketplace installs would load zero Genesis skills. Latent since v1.3.0, masked by F4 shadow.

F5 is the most important finding of v1.6.2. Blast radius : every new marketplace user. Fix is mechanical (move SPDX to trailing HTML comment, OR scope-narrow R10.5 to exclude SKILL.md). Deferred to v1.6.3 P0.

## Hypothesis outcomes

| H | Outcome | Rationale |
|---|---|---|
| H1 dispatch | UNABLE-TO-TEST | F5 root cause + F4 shadow — 5/5 natural-phrase runs freelanced. |
| H2 arbitration | UNABLE-TO-TEST formally ; indirect evidence positive | Alexandre freelance extracted multi-source data cleanly (RAL 9005, MOQ 8, EN 14351-1, Uw range, 3 pricing tiers). |
| H3 Phase 0.5 consent | UNABLE-TO-TEST | No skill dispatch → no Phase 0.5 path. |
| H4 EXIT_NO_KEY halt | UNABLE-TO-TEST | Skill didn't dispatch on halt-no-key fixture. |
| H5 zero Layer B ripple | **CONFIRMED** | AC10 grep = 0 at all checkpoints. |

## Self-rating — honest post-feat (5-axis)

| Axis | Projected | Honest | Delta | Notes |
|---|---|---|---|---|
| Pain-driven | 9.4 | 8.8 | −0.6 | Formal H1-H4 deferred ; F5 discovery IS substantial load-bearing pain-reduction but doesn't match projected form. |
| Prose | 9.0 | 9.0 | 0.0 | No prose rewrites ; evidence + runbook cleanly structured. |
| Best-at-date | 9.0 | 9.0 | 0.0 | No new R8 ; existing still valid. |
| Self-contained | 9.2 | 8.9 | −0.3 | Scope expanded into evidence log for F4+F5 (not into feat commits — still zero Layer B ripple). |
| Anti-Frankenstein | 9.1 | 9.1 | 0.0 | 5 frictions classified cleanly. 1:1 evidence-to-hypothesis maintained. |
| **Mean** | **9.14** | **8.96** | **−0.18** | **Streak ≥ 9.0 at 3 consecutive BREAKS** (v1.5.1 9.12 / v1.6.0 9.02 / v1.6.1 9.18 → v1.6.2 8.96). |

**Running average** : (8.90 × 18 + 8.96) / 19 = 169.16 / 19 ≈ **8.90 (flat).** 19 tagged ratings total.

## Cross-skill-pattern data-points added

- **Pattern #4 (zero-ripple)** — **depth update on the sixth data-point**, no new ordinal. Layer A-only runtime-evidence capture session = same ripple class as v1.5.1 Layer A-only corrections. Per v1.6.1 depth-update precedent.
- **Pattern #1 (1:1 mirror)** — no touch this ship.
- **Pattern #2 (concentrated privilege)** — no touch (genesis-drop-zone privilege unchanged).
- **Pattern #3 (granular commits)** — reference implementation continues : 10 commits in feat tranche, each with clear rationale, squash merge preserves forensic worktree.

## Out-of-scope follow-ups (v1.6.3+)

- **v1.6.3 P0** : fix F5 (SPDX-comment-before-frontmatter universal break). Mechanical across 8 SKILL.md. Bundle F1 + F4 runbook hardening.
- **v1.6.3 / v1.6.4** : re-run runtime dogfood against F5-fixed plugin. True H1-H4 evidence expected.
- **v1.6.3+** : F2 multi-turn via `--input-format stream-json` scripted.
- **v1.6.x+** : promptor Skill-tool plugin-installed runtime (was v1.6.2 candidate in v1.6.1 resume — bumped since this ship took the slot).
- **v2 design conversation** : F3 product-positioning ("when does skill beat freelance?").

## PR + tag state

- Branch `feat/v1.6.2-runtime-dogfood` PR #45 squash-merged as `025ad1b`.
- Tag `v1.6.2` pushed.
- Worktree `C:/Dev/Claude_cowork/project-genesis/.claude/worktrees/feat_2026-04-19_v1_5_2_runtime_dogfood/` retained per R2.5 (directory name retained post-retitle for forensic continuity ; branch renamed to `feat/v1.6.2-runtime-dogfood`).
- Chore worktree `.claude/worktrees/chore_2026-04-19_v1_6_2_session/` for this chore commit.
- Tag chain : ... v1.5.1 → v1.6.0 → v1.6.1 → **v1.6.2**. 19 tagged versions total.

## R2.3.1 observation

Mid-session `gh auth switch -u myconciergerie-prog` + GH_TOKEN env-prefix applied **proactively** (not reactively) at Phase C for `git push` + `gh pr create` + `gh pr merge` + `git push tag`. Pattern is now habitual. If proactive application continues in v1.6.3+ sessions, no Layer 0 amplification needed. Phase D skipped this ship.

## User state preservation

- `claude plugin uninstall project-genesis@project-genesis-marketplace` performed during Path B — **restored via reinstall after evidence capture**.
- `rm -rf ~/.claude/plugins/cache/project-genesis-marketplace/` performed — will regenerate on next `plugin update`.
- `~/.claude/skills/<genesis-skills>/` stale personal-scope installs — NOT touched (would require user consent ; user's data).
- Runtime JSON outputs archived at `C:/tmp/v1.6.2-runs/` (7 runs, not repo-committed).
