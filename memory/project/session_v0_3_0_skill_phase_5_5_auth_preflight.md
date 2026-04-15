<!-- SPDX-License-Identifier: MIT -->
---
name: Session v0.3.0 — Phase 5.5 Auth Pre-flight skill (2026-04-15)
description: Session that picked up the v0.2.0 → v0.3.0 handoff and shipped skills/phase-5-5-auth-preflight/ end-to-end in its own feat worktree, tagged v0.3.0 at self-rating 8.2/10
type: project
session_date: 2026-04-15
shipped_version: v0.3.0
self_rating: 8.2
---

# Session v0.3.0 — Phase 5.5 Auth Pre-flight skill

## Context

Second full skill-implementation session of Project Genesis. Picked up the v0.2.0 → v0.3.0 handoff prompt (`resume/2026-04-15_v0_2_0_to_v0_3_0.md`) and delivered the `phase-5-5-auth-preflight` skill as the next step in the plug-by-plug build of the Genesis 7-phase protocol.

## What shipped

**Commit** on main: `1f964e0` (squash of PR #4).

**Tag**: `v0.3.0` on `1f964e0`, pushed to origin.

**Branch**: `feat/2026-04-15_phase-5-5-auth-preflight-skill`, landed via squash merge, not deleted (per R2.3 retention).

### 8 new files under `skills/phase-5-5-auth-preflight/`

| File | Purpose | Lines |
|---|---|---|
| `SKILL.md` | Entry point + six-step flow map + canonical PAT scope list + isolated copy-paste rule | 124 |
| `consent-card.md` | Step 5.5.0 consent collector (project slug, owner, visibility, SSH alias, PAT scopes, expiration, Chrome profile, Playwright opt-in) | 105 |
| `ssh-keygen.md` | Step 5.5.1 per-project ed25519 keygen + `~/.ssh/config` alias append with `IdentitiesOnly yes` + paste-back public key + `ssh -T` confirmation with wrong-identity recovery | 167 |
| `pat-walkthrough.md` | Step 5.5.2 top-to-bottom fine-grained PAT form walkthrough with Administration RW in the canonical scope list, every paste value in its own fenced block, one-time token capture, `.env.local` sink with sanity test | 174 |
| `empty-repo-create.md` | Step 5.5.3 web-UI paste-back for empty repo creation (hard lesson: fine-grained PATs cannot create user-owned repos), every form field in isolated code blocks, `git remote set-url` to per-project SSH alias | 169 |
| `three-probe-test.md` | Step 5.5.4 canonical three-probe exit gate (SSH, `gh api user`, `gh api repos/owner/repo` with `.permissions.admin` check), per-probe failure-mode tables + targeted recovery, full-pass helper snippet with four exit codes | 119 |
| `playwright-automation.md` | Optional automation branch over 5.5.1-5.5.3 — opt-in via consent card only, known-selector map with `expires_at: 2026-05-14` TTL, hard fall-back to paste-back on any single selector miss, three-variant token capture + `browser_snapshot` safety net, screenshot-on-failure | 131 |
| `verification.md` | Step 5.5.5 final health card + canonical schemas for `memory/reference/ssh_<project>_identity.md` and `memory/reference/github_<project>_account.md`, three status outcomes, idempotency branches | 215 |

Total: **1,204 lines** across 8 files, every file SPDX-headered with `<!-- SPDX-License-Identifier: MIT -->`.

### Other changes

- `.claude-plugin/plugin.json` version bumped from `0.2.0` to `0.3.0`
- `CHANGELOG.md` entry for v0.3.0 prepended above v0.2.0, with the full Added list, notes, 5-axis self-rating averaging **8.2/10**, and known gaps for v0.4.0

## Self-rating v0.3.0 — 8.2/10

| Axis | Rating | Notes |
|---|---|---|
| Pain-driven coverage | 9/10 | Every file points to a specific learning in `specs/v1_phase_5_5_auth_preflight_learnings.md` |
| Prose cleanliness | 7/10 | Dense but readable; uniform failure-mode tables; intentional repetition across files |
| Best-at-date alignment | 9/10 | 2026 Q2 patterns: fine-grained PATs with Administration RW, per-project SSH alias with `IdentitiesOnly yes`, Playwright MCP with selector TTL, `GH_TOKEN` env override |
| Self-contained | 7/10 | Skill runs end-to-end within its directory; `three-probe-test.md` is deliberately extractable for Phase 5 and R1.1 reuse |
| Anti-Frankenstein | 9/10 | Zero speculative surfaces; one-miss Playwright fall-back with no retry loops; fixed scope list; fixed probe count; form-snapshot TTLs |
| **Average** | **8.2/10** | Clears 7.8 target by 0.4, below 8.5 v1 ceiling |

## Spec fidelity

All five stratified learnings from `specs/v1_phase_5_5_auth_preflight_learnings.md` are honoured:

1. **Learning 1 — Isolated copy-paste blocks**: every paste value in `ssh-keygen.md`, `pat-walkthrough.md`, `empty-repo-create.md` lives in its own fenced code block, never inside a table cell
2. **Learning 2 — Form-order instructions**: `pat-walkthrough.md` and `empty-repo-create.md` walk the GitHub UI top-to-bottom in the actual 2026-04-15 field order, with `expires_at` TTL for re-verification
3. **Learning 3 — Three-probe pre-flight**: `three-probe-test.md` is the canonical gate, extracted as standalone so Phase 5 and R1.1 can reuse without pulling in the rest of the skill
4. **Learning 4 — Administration: Read and write**: added to the canonical PAT scope list in `pat-walkthrough.md` and `SKILL.md`, with explicit explanation of the silent-blocker failure mode it prevents
5. **Learning 5 — Paste-back cost is the v2 justification**: honoured via the opt-in Playwright branch (`playwright-automation.md`), which is strictly opt-in, falls back to paste-back on any selector miss, and carries a 30-day TTL on its selector map

## Anti-Frankenstein discipline — held

- **One skill only**: `phase-5-5-auth-preflight` shipped; four other stubs (`genesis-protocol`, `journal-system`, `session-post-processor`, `pepite-flagging`) untouched
- **No refactor of `phase-minus-one`**: the v0.2.0 skill at 7.6/10 is stable and was not touched
- **No hook wiring, no templates/ population, no marketplace manifest**: still deferred
- **No speculative features**: every file in the PR points to a documented pain point or spec section

## Gaps logged for v0.4.0

From the CHANGELOG v0.3.0 known-gaps section:

1. No automated tests for `three-probe-test.md`'s full-pass helper — exit code contract documented but not exercised by a harness
2. Playwright selector map is a 2026-04-15 snapshot — no nightly probe to detect drift
3. `memory/reference/consent-log.md` schema documented but not shipped as a starter file
4. No `templates/phase-5-5-auth-preflight-*.md` ship — walkthrough templates are skill-local
5. Bash-only assumption — PowerShell-equivalent snippets deferred (consistent with `phase-minus-one` making `bash` a core requirement)
6. Idempotency on re-run is documented but the three-branch consent card runner is prose-only

None of these are blocking; all are v0.4.0+ candidates.

## R2.1 discipline — held

- All edits to the feat branch happened inside `.claude/worktrees/feat_2026-04-15_phase-5-5-auth-preflight-skill/`, never in the repo root
- All edits to the chore branch (session memory + v0.4.0 resume prompt) happened inside `.claude/worktrees/chore_2026-04-15_v0_3_0-session-memory-resume/`
- Neither worktree was deleted after merge (R2.5 forensic retention)
- PR #4 was opened via `GH_TOKEN="$GH_TOKEN" gh pr create` from the feat worktree
- Squash merge via `GH_TOKEN="$GH_TOKEN" gh pr merge 4 --squash` with no `--delete-branch`
- Tag `v0.3.0` created locally and pushed to origin
- No `--amend`, no `--force`, no rule bypass

## Cosmetic follow-up (still pending)

The GitHub repo description artefact from v1 bootstrap (Étape 4b) is still present. Both options unchanged:

1. Manual fix via web UI
2. PAT rotation with `Administration: Read and write` scope then PATCH via API — this is exactly the scope the new skill teaches, so the v0.4.0 session could dogfood its own recommendations and fix the description via the canonical probe

Non-blocking either way.

## Forward map — v0.4.0 and beyond

| Skill | Status | Notes |
|---|---|---|
| `phase-minus-one` | Shipped v0.2.0 at 7.6/10 | Stable, do not refactor |
| `phase-5-5-auth-preflight` | Shipped v0.3.0 at 8.2/10 | Stable, do not refactor |
| `journal-system` | Stub | Independent; reuses Layer 0 journal spec; candidate for v0.4.0 |
| `session-post-processor` | Stub | Independent; JSONL redaction + markdown archive; candidate for v0.4.0 |
| `pepite-flagging` | Stub | Independent; reuses pépite spec; candidate for v0.4.0 |
| `genesis-protocol` | Stub | Orchestrator — likely last, once every phase is implemented |

Pick whichever reuses the most existing state for v0.4.0. Target rating: **8.0/10**.

## References consumed during this session

- `resume/2026-04-15_v0_2_0_to_v0_3_0.md` — the handoff prompt from v0.2.0
- `specs/v1_phase_5_5_auth_preflight_learnings.md` — the canonical spec
- `memory/MEMORY.md`, `memory/master.md`, `memory/project/session_v0_2_0_skill_phase_minus_one.md` — R1.1 open ritual reads
- `memory/reference/ssh_genesis_identity.md`, `memory/reference/github_genesis_account.md` — model for the downstream skill's memory-writer schemas
- `skills/phase-minus-one/SKILL.md`, `skills/phase-minus-one/verification.md` — structural model for skill file layout
- `~/.claude/CLAUDE.md` Layer 0 — per-project SSH identity, GH_TOKEN env override, fine-grained PAT scope checklist
