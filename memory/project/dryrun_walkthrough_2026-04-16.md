<!-- SPDX-License-Identifier: MIT -->
---
name: Dry-run walkthrough — v0.9.0 polish (2026-04-16)
description: Paper-walkthrough of the genesis-protocol orchestrator against a synthetic target folder (C:\tmp\genesis-dryrun\ with a minimal config.txt, slug=dryrun-demo, is-a-plugin=no). No real SSH keys, PATs, GitHub repos, or installers were executed. Surfaces 10 friction points; the v0.9.0 polish lands fixes for the 5 medium-severity ones. This is the first end-to-end trace of the orchestrator against a non-Genesis target and is the load-bearing evidence that v0.9.0 is polish-with-context, not a number-chase.
type: project
session_date: 2026-04-16
session_version: v0.9.0
target_folder: C:\tmp\genesis-dryrun\
---

# Dry-run walkthrough — genesis-protocol v0.8.0 → v0.9.0 polish

## Setup

- Target folder: `C:\tmp\genesis-dryrun\`
- Seed input: a single `config.txt` with YAML-style fields (name, slug `dryrun-demo`, vision, license MIT, is-a-plugin no, plan-tier Max, scope-locks project-genesis)
- No mixed media, no existing `.git/`, no existing code — clean greenfield
- Walkthrough traced in-session against `skills/genesis-protocol/phase-*.md`
- Zero real side effects: no `ssh-keygen`, no `gh auth`, no `gh api`, no `git init`, no `git push`, no installers, no PATs. Pure paper trace

## Findings

10 items surfaced. Severity reflects impact on a real downstream bootstrap.

| # | Phase / Step | Severity | Finding | Fix landed in v0.9.0? |
|---|---|---|---|---|
| 1 | Phase 0 Step 0.1 | low | No convention for ignoring orchestrator-internal scratch files accidentally left in the target folder | No — v1.1 candidate |
| 2 | Phase 0 Step 0.1 | low | No explicit dry-run / preview mode flag in the orchestrator itself | No — v1.1 candidate, already documented in SKILL.md's "What this skill does NOT do" |
| 3 | Phase 1 Step 1.2 | med | Ambiguous: "Use Write to create each file" wording vs parenthetical delegation claims — reader cannot tell whether INDEX.md files are created at Step 1.2 or at Step 1.5 by sibling install-manifests | **Yes** — clarified Step 1.2 language to split scaffold-creation from INDEX-delegation |
| 4 | Phase 1 Step 1.3 + Phase 2 Step 2.3 | med | Source-path resolution for the Genesis plugin root is described as "either under `~/.claude/plugins/project-genesis/...` OR the dev repo" — no concrete resolution recipe, no fallback order | **Yes** — added explicit resolution rule: walk 3 levels up from `skills/genesis-protocol/SKILL.md`, with fallback to the `~/.claude/plugins/` install path |
| 5 | Phase 2 Step 2.3 | low | Entries are copied unconditionally regardless of `is-a-plugin: yes/no` — for non-plugin projects the plugin-distribution + plugin-structure entries are lightly redundant (not harmful; R8 cache is reference material) | No — kept as-is. Cache entries are reference material, not load-bearing; pruning them adds branching complexity without clear benefit. Noted in polish walkthrough as acceptable |
| 6 | Phase 3 Step 3.1 | low | `git init -b main` requires git 2.28+ — no explicit version probe at the start of Phase 3 | No — Phase -1 is expected to verify git version via phase-minus-one; if it doesn't, that's a phase-minus-one gap not a genesis-protocol gap |
| 7 | Phase 3 Step 3.2 | med | `~/.ssh/id_ed25519_<slug>` uses tilde expansion which is shell-dependent on Windows (bash expands, cmd/powershell do not) | **Yes** — changed to `$HOME/.ssh/id_ed25519_<slug>` which works in bash, zsh, and PowerShell (automatic variable) |
| 8 | Phase 3 Step 3.3 | low | `chmod 0600` on `~/.ssh/config` is POSIX-only; Windows uses ACLs (OpenSSH on Windows auto-fixes perms, but the instruction doesn't note the caveat) | **Yes** — added a one-line Windows caveat |
| 9 | Phase 4 Step 4.5 | med | Scope lock entries from `config.txt` are free-form text (e.g. `project-genesis (frozen at v0.8.0 until v1.0.0 ships)`), but the runbook writes `memory/project/<lock_slug>_frozen_scope_lock.md` — no documented transformation from free-form to slug | **Yes** — added slug derivation rule in Phase 0 Step 0.2 (first whitespace-terminated token, lowercased, `-` cleanup) and referenced it in Phase 4 Step 4.5 |
| 10 | Phase 6 Step 6.2 | med | Multi-line `git commit -m "..."` with embedded newlines is bash-only; Windows cmd/powershell need either a HEREDOC (bash) or a file-backed message (`-F`) | **Yes** — rewrote Step 6.2 to use HEREDOC explicitly and added a fallback note for powershell |

## Also verified (no fix needed)

- `session-post-processor/install-manifest.yaml` uses `create_if_missing_only: true` + `idempotent: true` — safe to re-run and does not overwrite a pre-existing `INDEX.md`
- `journal-system/install-manifest.yaml` same discipline
- `pepite-flagging/install-manifest.yaml` same discipline (sampled; all three follow the idempotent pattern)
- `phase-minus-one/install-manifest.yaml` is a stack-install spec (per-OS package list), NOT a file-target manifest — Phase 1 Step 1.5's claim that phase-minus-one "creates `memory/reference/automation-stack.md` placeholder if missing" is technically inaccurate because the install-manifest has no `targets:` section. The actual `automation-stack.md` is written at runtime when `phase-minus-one` runs during Phase -1. Fixed in the Phase 1 Step 1.5 edit (item #3 above)

## What the walkthrough did NOT uncover

- No structural bug in the 7-phase ordering
- No contract mismatch between the orchestrator and sibling skills at input/output boundaries
- No missing consent gate
- No privilege escalation path outside the documented concentrated-privilege map
- No recursive loop risk
- No skill that would need to reimplement logic owned by another skill

## Conclusion

The orchestrator's 7-phase structure is sound. The 5 medium-severity fixes are all in the "runbook language precision" category — nothing structural, nothing that required a re-design. The trace confirms Option A pure Markdown was the right call: the fixes landed as prose edits, not code changes. v0.9.0 ships these fixes plus meta-memory visibility in `master.md` and the public-facing README rewrite.

Running the orchestrator for real against a downstream project remains a v1.1 candidate (paper trace validates structure; execution validates implementation under real network, disk, and Windows quirks).
