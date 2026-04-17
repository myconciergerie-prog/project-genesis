<!-- SPDX-License-Identifier: MIT -->
---
name: Session v1.2.2 — mode is a first-class argument
description: v1.2.2 ship session. P1 cluster (F20 mode-auto semantics + F22 consent card mode-aware + F21 argument schema) landed as a 2-commit bundle in one PR. SKILL.md gains a canonical Arguments section and a Mode dispatch table; three phase runbooks reference the table at their consent-gate paragraphs.
type: project
date: 2026-04-17
session: v1.2.2
branch: feat/v1.2.2-mode-auto-args
parent-tag: v1.2.1
parent-commit: 0a1d138
---

# Session v1.2.2 — mode is a first-class argument

Direct follow-up to v1.2.1 (merged as PR #24, tagged `v1.2.1` on `0a1d138`). Scope: the three P1 frictions that converge on the same root cause — the 3-mode ladder was Phase-minus-one-only and the orchestrator inherited consent-gate wording without mode-awareness. Path A from the v1.2.1 → v1.2.2 resume prompt, picked by the user at session open on the grounds that the discipline scoring 9.26 at v1.2.1 (one-root-cause-per-PR, surgical diffs) is taillored for this cluster, and because F34 (gh active-account pre-flight) was live-reproduced during v1.2.1's own PR creation — a fresh signal that deserves its own focused cycle at v1.2.3.

## What shipped

Two commits on `feat/v1.2.2-mode-auto-args` off `afada47`:

| Commit | Fix | Files changed |
|---|---|---|
| `72ef17a` | **F21 + F20 + F22 (canonical spec)** — `## Arguments` + `## Mode dispatch` sections in SKILL.md; Step 0 dispatches per mode; anti-Frankenstein clause reworded | 1 file (`SKILL.md`) |
| `a086749` | **F20 + F22 (per-phase pointers)** — mode-dispatch paragraphs at the three consent-gate locations in Phase 0.4, Phase 3.2/3.3/3.5, Phase 6.1 | 3 files (`phase-0-seed-loading.md`, `phase-3-git-init.md`, `phase-6-commit-push.md`) |

Net diff: `+60 / −3` across 4 distinct files. Reading signal: the SKILL.md addition is ~54 lines (one new Arguments section + one new Mode dispatch section); the three phase pointers are 2 lines each (6 lines total). One source of truth + three pointers = the 1:1 mirror discipline restated for mode dispatch.

## Why the bundle is one PR instead of three

The v1.2.1 → v1.2.2 resume prompt flagged this cluster as Path A's v1.2.2 scope: "Bundle F20/F22/F21 into a single v1.2.2 PR: add mode-auto as a proper orchestrator argument with documented semantics, along with the `## Arguments` section." The three frictions share the same plumbing:

- F21 defines the argument (`mode`) that needs to exist.
- F20 asks for the mode argument to actually drive behaviour.
- F22 is the specific consent-gate instance of F20 at Step 0.

Shipping them in separate PRs would mean the per-phase pointers (second PR) would reference `mode` before it was defined, or the `mode` definition (first PR) would ship without any consumer. The one-PR-two-commits structure preserves the "one root cause per commit" discipline that scored 9.5 anti-Frankenstein in v1.2.1 while honouring the "each PR makes sense on its own" constraint.

## Verification walk-throughs (scenario replays)

### F21 — Arguments section reachable from invocation guess

Replay scenario: a future user or session invokes `/genesis-protocol mode=semi-auto target=/tmp/newproj seed=seed.md context="bootstrap a test project"` and needs to know what those arguments do.

With new code: SKILL.md has a `## Arguments` section immediately after `## When to invoke`. The user (or a reading Claude session) lands on it, sees the three-row table, and immediately knows: `mode=semi-auto` → block on concentrated-privilege gates, summary-and-proceed elsewhere; `target=/tmp/newproj` → destination folder, will be checked by Paradox Guard A; `seed=seed.md` → filename inside target read at Phase 0.2; `context=...` → passthrough, captured in `bootstrap_intent.md` under non-canonical fields, no runtime effect.

Mental replay confirms the v1.2.0 friction F21 ("Any caller — human or v2 Promptor — guessing at argument names will miss") is now structurally impossible. The schema is one `Cmd+F` away.

### F20 + F22 — mode dispatch at Step 0 consent card

Replay scenario: the v1.2.0 exact invocation — `/genesis-protocol mode=auto target=<worktree-path> seed=config.txt context="..." strange-loop="true" friction-log="..."`.

With new code: Paradox Guard A halts immediately because the target is inside the orchestrator plugin tree (the v1.2.1 defence). If the user deliberately picks a target OUTSIDE the plugin tree and sets mode=auto, Step 0 renders the top-level consent card as an informational log (full plan visible, every field listed), logs it to the session transcript, and proceeds to Phase -1. The user can still interject `pause` / `abort` / `frankenstein` at any point.

In `detailed` or `semi-auto` mode with the same invocation (same target, different mode), Step 0 blocks until the user confirms. Step 0 is the canonical gate that F22 specifically flagged as "the user must confirm the full card before Phase 0 starts. No silent bootstraps" — the wording is preserved for detailed/semi-auto, and the auto path is defined as "render the card, log it, proceed unless the user interjects" which is semantically different from "silent bootstrap".

Mental replay confirms F20 ("mode=auto degrades to 'render the consent card and assume yes' which is NOT what the user intended") is resolved — auto is now a fully-specified mode with its own dispatch.

### Per-phase mode dispatch — the 1:1 mirror

Replay scenario: a future session reads one of the phase runbooks (`phase-0-seed-loading.md`, `phase-3-git-init.md`, `phase-6-commit-push.md`) looking for the mode behaviour at a specific gate.

With new code: each of the three phase runbooks has a "**Mode dispatch**" paragraph at the consent-gate location with a pointer to `SKILL.md § Mode dispatch` plus the phase-specific twist. The reader never has to guess — either the SKILL.md table answers it, or the phase paragraph adds the one-off (Phase 3.2/3.3 security floor; Phase 6.1 blocking even in semi-auto).

Mental replay confirms F22's per-phase manifestation is covered — every consent-gate location now has an explicit mode-dispatch sentence, so no phase silently interprets "auto" differently from another.

## What v1.2.2 intentionally does NOT fix

Per the v1.2.1 session trace deferral list:

- **F26 passthrough non-canonical fields audit UI** — *half-fixed*. The passthrough **convention** is now documented in SKILL.md `## Arguments` (accepted, captured, no runtime effect). The actual write of `## Non-canonical fields (passed through)` into `bootstrap_intent.md` at Phase 0.5 is still not wired in the template. A v1.2.3 or v1.3 touch-up can complete it; deliberately deferred to keep v1.2.2 surgical.
- **F24 Phase 0.1 git-aware inspection** — P2, F30 already covers the Phase 3 blocker case; Phase 0.1 is cosmetic improvement only.
- **F25 / F31 config.txt canonical examples** — P2, ship `templates/config-minimal.txt.example` + `templates/config-complete.txt.example` in a future chore PR.
- **F28 `genesis-cleanup` sibling skill** — P3.
- **F32 Python driver** — v1.3 target. The v1.2.0 meta-finding #5 named this as the Markdown ceiling; v1.2.2 deliberately stays on the Markdown side to validate mode dispatch before adding a driver that would need to parse args.
- **F33 R8 scope disambiguation** — P3.
- **F34 gh active-account pre-flight** — **v1.2.3 target**. Live-reproduced during v1.2.1's PR creation, documented in the v1.2.1 → v1.2.2 resume prompt as the focused next PR.

## Self-rating — v1.2.2

See CHANGELOG for the 5-axis table. Summary:

- **Pain-driven**: every change maps 1:1 to a v1.2.0 friction (F21 → Arguments, F20/F22 → mode dispatch). Zero speculative additions. F26 deliberately half-fixed.
- **Anti-Frankenstein**: no Python driver, no hooks, no test harness. Two surgical commits, 60 + 3 lines across 4 files. F32 still deferred to v1.3 despite v1.2.0 meta-finding #5 calling it the Markdown ceiling — the mode dispatch added here lands on top of pure Markdown, proving the ceiling was above the v1.2.2 scope.
- **Self-contained**: SKILL.md is the single source of truth for mode dispatch. Phase runbooks reference the table rather than restate the rules. Drift is a merge-blocker.
- **Prose**: each commit has a 3-paragraph narrative body. The Arguments + Mode dispatch tables are copy-paste-ready for anyone reading the SKILL.md front-to-back.
- **Best-at-date**: the `mode` vocabulary matches `phase-minus-one`'s existing 3-mode ladder by design — no new conceptual territory, no external research cache refresh needed.

## Running average post-v1.2.2

v0.2 → v1.2.1 average was 8.65/10. v1.2.2 self-rating is 9.14/10, bringing the running average to **8.68/10** (comfortably above the 8.5 v1 target, well within the anti-Frankenstein inflection-point discipline — every version since v1.2.0 has been ≥ 8.88, three in a row scoring 9.0+).

## Next session entry point

`.claude/docs/superpowers/resume/2026-04-17_v1_2_2_to_v1_2_3.md` (written at the end of this session). Resume prompt names F34 as the v1.2.3 target, with the Phase 6.0 pre-flight (`gh api user --jq .login` compared to resolved owner, `gh auth switch -u <owner>` attempt before halt) as the fix sketch. A single-commit PR is the expected shape — no per-phase propagation, just a Phase 6 addition.
