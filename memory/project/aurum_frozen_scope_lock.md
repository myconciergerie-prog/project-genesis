<!-- SPDX-License-Identifier: MIT -->
---
name: Aurum frozen scope lock
description: LIFTED 2026-04-16 — aurum-ai repo was frozen at commit 0b1de3d from 2026-04-14 to 2026-04-16 (Genesis v1.0.0 ship). Lock is now lifted. Aurum v1 kickoff unblocked.
type: project
set_by: user instruction, 2026-04-14 (config.txt) and 2026-04-15 (reinforced mid-session)
---

# Aurum frozen scope lock

## The rule

**Aurum-ai repo is frozen at commit `0b1de3d` until Project Genesis v1.0.0 ships and is installed as a plugin.**

No work on aurum-ai code, no commits to aurum-ai, no PRs on aurum-ai, no branches pushed to aurum-ai. The repo stays exactly where it is.

## What IS allowed

- **Reading Aurum auto-memory** (`~/.claude/projects/C--Dev-Claude-cowork-aurum-ai/memory/`) for context
- **Writing pointer files** into Aurum auto-memory for cross-project research sharing — additive, hors-repo, never committed to Aurum's git history
- **Editing existing Aurum auto-memory files** to update the Meta-Memory architecture or add cross-references (e.g. the pépite addition 2026-04-15)
- **Reading the committed Aurum v0 template** at commit `0b1de3d` as a reference for the Genesis v1 work
- **Running Claude Code sessions** opened in other directories that happen to read Aurum auto-memory for context

## What is NOT allowed

- `git commit` on aurum-ai (any branch)
- `git push` to aurum-ai origin
- `gh pr create` / `gh pr merge` on aurum-ai
- **Editing any file** inside the `C:\Dev\Claude_cowork\aurum_ai\` repo directory (not the auto-memory — the actual repo filesystem)
- Running Aurum sessions with the intent to make progress on Aurum's product roadmap
- Using Genesis sessions to "warm up" on Aurum v1 work indirectly

## Why

User instruction, stated twice during the Genesis v1 bootstrap session:

1. **2026-04-14** via `config.txt`: *"WHAT THIS SESSION DOES NOT PRODUCE: ANY work on aurum-ai itself. Aurum-ai stays frozen at commit 0b1de3d until Genesis v1 is complete and installed at ~/.claude/templates/."*
2. **2026-04-15** reinforced mid-session: *"on est bien d'accord qu'à partir de maintenant on ne bosse plus qu'au perfectionnement de genesis plus de genesis dans aurum_ai"*

**Rationale**: the recursive bootstrap (applying the v0 template to itself to produce v1) requires complete focus. Splitting attention between Genesis v1 development and Aurum v1 kickoff would dilute both. Aurum v1 kickoff is **queued** for the session immediately after Genesis v1 ships.

## When this lock lifts

When Project Genesis v1.0.0 is:

1. Merged to `main` on the Genesis repo
2. Tagged with `v1.0.0`
3. Self-installable via `/plugin install project-genesis@myconciergerie-prog/project-genesis`
4. Verified working via a pre-flight test on a throwaway folder

Then — and only then — the Aurum v1 kickoff session can open with the Genesis v1 plugin active, and the scope lock on aurum-ai lifts for normal development work.

## How to apply

### In a Genesis session

If during Genesis work the temptation arises to "just quickly fix something in Aurum" (e.g. touch a rule file, update a memory entry, push a commit), STOP. Defer to the post-Genesis Aurum kickoff session. Any Aurum fix can wait.

### In an Aurum session opened before Genesis v1 ships

If a user opens a Claude Code session in `C:\Dev\Claude_cowork\aurum_ai\` before Genesis v1 ships (e.g. out of habit, or to look something up), the session should:

1. Read `memory/MEMORY.md` in Aurum's auto-memory as normal
2. Notice that Aurum v1 kickoff is queued and blocked by Genesis v1
3. Read this scope lock via the Genesis repo path if needed
4. Offer to open a Genesis session instead, OR restrict the Aurum session to read-only / research work
5. Refuse to commit or push to aurum-ai

### In the transition session (post-Genesis v1 ship)

The session immediately after Genesis v1.0.0 ships is the Aurum v1 kickoff. Its first action is to verify that:

- Genesis v1.0.0 is tagged and merged on the Genesis repo
- The Genesis plugin is installed (`/plugin install project-genesis@myconciergerie-prog/project-genesis` returns success)
- The aurum-ai repo is still at `0b1de3d` (no drift during the lock period)

Once verified, this scope lock lifts and Aurum v1 work can begin normally.

## **Why:** this matters

The Aurum v0_init session ended with a R2.1 violation under close-time pressure (squash-merged locally in the root directory because `gh pr merge` was blocked by PAT scope). The user's rule response was crystal clear: stress makes rule-following more important, not less. The scope lock is the same kind of hard rule, stated in advance during a calm moment — precisely so it can guide behavior under pressure when a half-finished Aurum change looks appealing.

## **How to apply:**

Any Claude Code session that could potentially touch Aurum must read this file at open (it's linked from Genesis `memory/MEMORY.md` which is always loaded at session open). If you find yourself about to commit or push to aurum-ai during the lock period, back out immediately. No exceptions.

---

## Lock lifted — 2026-04-16

**All four conditions met. The Aurum v1 kickoff is now unblocked.**

1. Genesis v1.0.0 merged to `main` on the Genesis repo
2. Tagged with `v1.0.0`
3. Self-installable via `/plugin install project-genesis@myconciergerie-prog/project-genesis`
4. Validated via v0.9.0 dry-run (10 findings, 5 fixed) + 3 dogfood runs (all GREEN)

The freeze was in effect from **2026-04-14** (Genesis session 1, Aurum v0_init freeze) to **2026-04-16** (Genesis v1.0.0 ship). Two calendar days, nine development sessions.

**Next**: the Aurum v1 kickoff session opens in `C:\Dev\Claude_cowork\aurum_ai\` with the Genesis v1 plugin active. Its first action is to verify that `aurum-ai` is still at `0b1de3d` (no drift during the lock period), then proceed with normal development.
