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
- [Session v0.7.0 — 2026-04-15](project/session_v0_7_0_pepite_flagging.md) — Pepite flagging skill shipped (6 files, 1:1 spec mirror, consent floor on cross-project pointer writes), R8 slug rule amended in-place (first live-dogfood amend precedent), v0.7.0 tagged at 8.8/10 (ties highest single-version rating), running average 8.40/10, one stub remaining (genesis-protocol orchestrator = v1.0.0 candidate)
- [Session v0.8.0 — 2026-04-16](project/session_v0_8_0_genesis_protocol.md) — Genesis-protocol orchestrator shipped (8 files, ~1,400 lines, Option A pure Markdown, 1:1 mirror of master.md's 7-phase table, concentrated-privilege map with 6 data points, third 1:1 spec mirror), v0.8.0 tagged at **9.0/10** (new single-version high), **running average 8.49/10 — 0.01 below v1 target** → user picked **Path A (v0.9.0 polish → v1.0.0)** with explicit "leverage memory/meta-memory context" framing. Zero stubs remaining; full v1 skill surface complete
- [Session v0.9.0 — 2026-04-16](project/session_v0_9_0_polish.md) — Path A polish: dry-run walkthrough (10 findings, 5 fixed), meta-memory visibility in `master.md`, README rewrite, dogfood run 3 GREEN. v0.9.0 tagged at **8.92/10**, **running average 8.54/10 — 0.04 above v1 target**. Ship gate cleared. v1.0.0 next
- [Dry-run walkthrough — 2026-04-16](project/dryrun_walkthrough_2026-04-16.md) — paper trace of the genesis-protocol orchestrator against `C:\tmp\genesis-dryrun\` (10 findings, 5 med fixes landed in v0.9.0, 5 low deferred to v1.1)
- [Aurum frozen scope lock](project/aurum_frozen_scope_lock.md) — hard rule that aurum-ai repo stays at `0b1de3d` until Genesis v1 ships; no aurum-ai commits / PRs / edits allowed in any Genesis session
- [Session v1.1 selfdogfood — 2026-04-16](project/session_v1_1_selfdogfood.md) — first real genesis-protocol execution, hit auth wall at Phase 3.4, pivoted to analysis, produced v2 Promptor fusion vision (9.2/10)
- [Self-dogfood friction log — 2026-04-16](project/selfdogfood_friction_log_2026-04-16.md) — 18 frictions (5 STRUCTURAL in auth), Victor test birth, Promptor fusion discovery, v2 vision trigger
- [Session v1.2.0 self-dogfood — 2026-04-17](project/selfdogfood_friction_log_v1_2_0_2026-04-17.md) — conscious strange-loop self-dogfood, 14 new frictions (F20-F34), two pépite-worthy findings (F29 plugin-install broken + Promptor attribution correction), v2 Étape 0 drop-zone surfaced
- [Session v1.2.1 paradox guards — 2026-04-17](project/session_v1_2_1_paradox_guards.md) — three P0 fixes from v1.2.0 landed surgically: F29 skill-self-contained rules, F30 git-aware nested-repo probe, F23+F27 Step 0 paradox guards. One follow-up commit for git-bash path normalization. v1.2.1 tagged
- [Session v1.2.2 mode-auto args — 2026-04-17](project/session_v1_2_2_mode_auto_args.md) — P1 cluster bundled in one PR: F21 `## Arguments` section, F20 mode is first-class argument (detailed/semi-auto/auto), F22 Step 0 consent card dispatches per mode. Three phase runbooks reference the canonical `## Mode dispatch` table. v1.2.2 tagged at **9.14/10**, third consecutive ≥ 9.0 ship. F34 named as v1.2.3 target

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

- `skills/genesis-protocol/rules/v1_rules.md` — R1-R10 for this project (adapted from Aurum v1); relocated from `.claude/docs/superpowers/rules/` in v1.2.1 to make the `genesis-protocol` skill self-contained (friction F29)
- `.claude/docs/superpowers/research/INDEX.md` — R8 research cache with TTL, 7 active entries as of bootstrap
- `.claude/docs/superpowers/specs/` — design specs (4 v1 specs + 1 v2 spec captured during bootstrap)
- `.claude/docs/superpowers/plans/` — implementation plans
- `.claude/docs/superpowers/resume/` — session handoff prompts
