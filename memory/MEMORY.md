<!-- SPDX-License-Identifier: MIT -->

# MEMORY — Project Genesis

Index of project-level memory for Project Genesis. **Always loaded at session open** per R1.1.

## Layer 0 inheritance

This project inherits all universal rules, user profile, hard rules, workflow patterns, and machine-specific reference from `~/.claude/CLAUDE.md` (Layer 0) **by reference**. See the project-level `CLAUDE.md` at the repo root for the pointer rules. This memory index does NOT duplicate Layer 0 content.

## Master

- [Master vision + stack + rules summary](master.md) — the stable project vision; read at every session open

## User

- [user/ README](user/README.md) — user profile is centralized in Layer 0; project-specific user notes would land here if they arise

## Feedback

- [feedback/ README](feedback/README.md) — universal feedback rules inherited from Layer 0; project-specific feedback would land here if it diverges

## Project

- [Session v1 bootstrap — 2026-04-14](project/session_v1_bootstrap.md) — origin session context, decisions frozen, self-ratings, forward map
- [Session v0.2.0 — 2026-04-15](project/session_v0_2_0_skill_phase_minus_one.md) — Phase -1 skill shipped end-to-end, v0.2.0 tagged at 7.6/10, gaps logged for v0.3.0
- [Session v0.3.0 — 2026-04-15](project/session_v0_3_0_skill_phase_5_5_auth_preflight.md) — Phase 5.5 Auth Pre-flight skill shipped end-to-end, v0.3.0 tagged at 8.2/10, gaps logged for v0.4.0
- [Session v0.4.0 — 2026-04-15](project/session_v0_4_0_skill_journal_system.md) — Journal system skill shipped end-to-end after recovery from lost PowerShell-window attempt, v0.4.0 tagged at 8.8/10, gaps logged for v0.5.0
- [Session v0.5.0 — 2026-04-15](project/session_v0_5_0_skill_session_post_processor.md) — Session post-processor skill shipped with halt-on-leak gate, R8 research refresh as prerequisite, first granular-commit discipline application (8 commits in feat branch), v0.5.0 tagged at 8.4/10, gaps logged for v0.6.0
- [Session v0.6.0 — 2026-04-15](project/session_v0_6_0_runpy.md) — Session post-processor run.py executable shipped (first runnable Python in Genesis), dogfood run 2/3 CLEAN, halt-on-leak gate proven live via `--inject-test-leak`, first live-dogfood correction of an R8 entry (slug underscore rule), v0.6.0 tagged at 8.6/10, gaps logged for v0.7.0
- [Aurum frozen scope lock](project/aurum_frozen_scope_lock.md) — hard rule that aurum-ai repo stays at `0b1de3d` until Genesis v1 ships; no aurum-ai commits / PRs / edits allowed in any Genesis session

## Reference

- [SSH identity — Project Genesis](reference/ssh_genesis_identity.md) — dedicated `~/.ssh/id_ed25519_genesis` + `github.com-genesis` alias in `~/.ssh/config`, fingerprint and git remote URL
- [GitHub account target — Project Genesis](reference/github_genesis_account.md) — `myconciergerie-prog/project-genesis`, PAT env pattern, SSH URL binding, Chrome Profile 2 for web UI

## Themes

- [themes/ README](themes/README.md) — empty; themes populated as the project grows and multi-entry patterns emerge

## Journal

- [Journal INDEX](journal/INDEX.md) — stratified thought capture (6th memory type per Layer 0 journal system spec). **First entry 2026-04-15** (seed): slug rule live-dogfood correction

## Pépites

- [Pépites INDEX](pepites/INDEX.md) — gold nugget discoveries with cross-project routing metadata (7th memory type per `specs/v1_pepite_discovery_flagging.md`); no entries yet, flagged automatically during research when red-light criteria match

## Pointers to dev-internal docs (not memory, but related)

- `.claude/docs/superpowers/rules/v1_rules.md` — R1-R10 for this project (adapted from Aurum v1)
- `.claude/docs/superpowers/research/INDEX.md` — R8 research cache with TTL, 7 active entries as of bootstrap
- `.claude/docs/superpowers/specs/` — design specs (4 v1 specs + 1 v2 spec captured during bootstrap)
- `.claude/docs/superpowers/plans/` — implementation plans
- `.claude/docs/superpowers/resume/` — session handoff prompts
