<!-- SPDX-License-Identifier: MIT -->
---
name: Phase 5.5 — Auth pre-flight (pointer to phase-5-5-auth-preflight skill)
description: Thin pointer file — Phase 5.5 of the Genesis protocol is handled entirely by the sibling skill `phase-5-5-auth-preflight`. This runbook documents the contract between the orchestrator and the sibling skill — slug passing, Chrome profile selection, Layer 0 references, and exit conditions — without duplicating the sibling's flow.
---

# Phase 5.5 — Auth pre-flight (thin pointer)

Phase 5.5 is **not implemented in this file**. It is implemented by the sibling skill at `skills/phase-5-5-auth-preflight/SKILL.md`, which owns the six numbered steps (5.5.0 consent card through 5.5.5 verification card) and the canonical PAT scope list.

This pointer file exists for one reason: **the 1:1 mirror discipline with `memory/master.md`'s 7-phase table requires every phase to have an explicit home**. Folding Phase 5.5 into another runbook would muddle the compositional story — it is cleaner to keep it as its own short pointer that documents the orchestrator↔sibling contract.

If you are reading this looking for the auth flow itself, go directly to `skills/phase-5-5-auth-preflight/SKILL.md`. Everything below is orchestrator-side wiring, not auth mechanics.

## What the orchestrator passes to the sibling skill

At Phase 5.5 entry, the orchestrator has:

| Field | Source | Reason |
|---|---|---|
| Project slug | `memory/project/bootstrap_intent.md` (Phase 0) | Identifies the SSH key name, host alias, and reference memory filenames |
| GitHub owner | Top-level consent card (`SKILL.md` Step 0) | Determines PAT resource owner + target repo owner — may differ from the default personal account |
| Target repo name | `bootstrap_intent.md` (defaults to slug) | The empty repo to create at Step 5.5.3 |
| Chrome profile | Top-level consent card, cross-referenced with Layer 0 `reference_chrome_profiles_machine.md` | Which Chrome profile is signed into the correct GitHub account for the paste-back steps |
| Playwright MCP opt-in | Top-level consent card | If user opted in, the sibling skill uses Playwright for form fills; otherwise paste-back |
| License | `bootstrap_intent.md` | Shown on the repo create form (paste-back) |
| PAT expiration window | `bootstrap_intent.md` OR Layer 0 default (90 days) | Recorded in `memory/reference/github_<slug>_account.md` at sibling exit |

The orchestrator does **not** hand the sibling skill a PAT, an SSH private key, or any secret material. Every secret is generated **by** the sibling skill inside its own flow — the orchestrator is the caller, not the producer of those values.

## What the orchestrator receives from the sibling skill

At Phase 5.5 exit, the orchestrator reads:

| Field | Location | How it is consumed |
|---|---|---|
| `memory/reference/ssh_<slug>_identity.md` | File written by sibling Step 5.5.5 | Proves the SSH identity is wired; Phase 6 uses the host alias from here |
| `memory/reference/github_<slug>_account.md` | File written by sibling Step 5.5.5 | Proves the GitHub account, PAT scopes, expiration, three-probe result |
| `.env.local` with `GH_TOKEN=<pat>` | File written by sibling Step 5.5.5 | Consumed by Phase 6 for `gh pr create` / `gh pr merge --squash` |
| Three-probe gate result | Health card at sibling Step 5.5.5 | Must be GREEN before Phase 6 can touch the remote |

If any of these is missing or the three-probe gate is RED, **the orchestrator stops**. Phase 6 cannot run until the sibling skill reports a fully green exit. There is no "partial auth" fallback — Genesis treats auth as binary.

## Why Phase 5.5 runs after Phase 4 and not before

Phase 5.5 cannot run before Phase 4 because:

1. The project slug comes from `bootstrap_intent.md` (Phase 0) but is also shown in the consent card as part of `<owner>/<repo>`, and the user may revise the repo name at Phase 4 review. The sibling skill reads the finalized value, not the Phase 0 draft.
2. `.gitignore` must exist before `.env.local` is written — otherwise a stray `git add -A` would stage the PAT. Phase 3.7 writes `.gitignore`; Phase 5.5's `.env.local` write happens after.
3. The sibling skill writes to `memory/reference/` — the directory must exist from Phase 1.2, and it does.
4. The sibling skill reads `memory/reference/automation-stack.md` to know whether Playwright MCP is available — that file was written during Phase -1 (or skipped, in which case the sibling falls back to paste-back).

Running Phase 5.5 earlier than Phase 4 would violate one or more of these invariants.

## Why Phase 5.5 runs before Phase 6 and not as part of it

Phase 5.5 is a gate, not a preamble. Splitting Phase 6 to do "auth + commit + push" would bundle two concentrated privileges into one phase — exactly the anti-Frankenstein trap Layer 0 warns about ("each skill has at most one concentrated privilege"). Phase 5.5 concentrates the auth privilege; Phase 6 concentrates the write-to-remote privilege. Separation keeps the consent gates distinct and the blast radius contained.

If Phase 5.5 fails, Phase 6 never starts and no commit gets created. If Phase 6 fails after Phase 5.5 succeeded, the user has a complete auth setup they can reuse in a manual recovery (the SSH key, the PAT, and the empty repo all still exist — they just never received the first push).

## Layer 0 references the sibling skill consults

The sibling `phase-5-5-auth-preflight` skill reads these Layer 0 files during its flow. The orchestrator does not interfere — it just ensures they are accessible:

| Layer 0 file | Consulted by | Why |
|---|---|---|
| `~/.claude/CLAUDE.md` → workflow patterns | Sibling Step 5.5.0 | Per-project SSH identity + GH_TOKEN env override + fine-grained PAT scope checklist |
| `~/.claude/memory/layer0/workflow_github_and_tooling.md` | Sibling Step 5.5.2 | Full canonical PAT scope list, fine-grained PAT limitation (cannot create user repos) |
| `~/.claude/memory/layer0/reference_chrome_profiles_machine.md` | Sibling Step 5.5.0 | Chrome profile → Google account → GitHub account mapping |
| `~/.claude/memory/layer0/reference_accounts_orgs_and_projects.md` | Sibling Step 5.5.0 | Universal cross-project registry — ensures the right identity scope is picked |
| `~/.claude/memory/layer0/rules_hard_discipline.md` | Sibling throughout | Additive auth, no new windows, isolated copy-paste rule |

If any Layer 0 file is missing from `~/.claude/memory/layer0/`, the sibling skill surfaces the gap but falls back to pure Layer 0 `CLAUDE.md` references. The orchestrator does not attempt to restore the Layer 0 files — they are outside Genesis's scope.

## How the orchestrator invokes the sibling

Conceptually:

```
phase_5_5_result = invoke_skill(
  "phase-5-5-auth-preflight",
  project_slug = intent.slug,
  github_owner = consent_card.github_owner,
  target_repo  = consent_card.target_repo,
  chrome_profile = consent_card.chrome_profile,
  playwright_opt_in = consent_card.playwright_opt_in,
  license = intent.license,
  pat_expiration = consent_card.pat_expiration or "90d",
)

if phase_5_5_result.three_probe_gate != GREEN:
  halt_with_error(phase_5_5_result.failure_reason)
  exit
```

In practice, v0.8.0 is pure Markdown — the "invocation" is Claude reading `skills/phase-5-5-auth-preflight/SKILL.md`, running the six numbered steps, and writing the output files. The orchestrator does not call Python or shell — it follows the Markdown and respects the contract above.

A v1.1 candidate is to replace the conceptual pseudocode with a real Python driver. Not in v0.8.0.

## Exit condition

Phase 5.5 is complete when:

- `memory/reference/ssh_<slug>_identity.md` exists in the target folder with the ed25519 key fingerprint, host alias, SSH config entry
- `memory/reference/github_<slug>_account.md` exists in the target folder with owner, repo, PAT scopes, expiration date, three-probe result
- `.env.local` exists at target folder root with `GH_TOKEN=<pat>` (and is gitignored from Phase 3.7)
- Empty target repo `<owner>/<repo>` exists on GitHub
- All three probes (SSH, PAT user, repo existence) returned GREEN on the last run
- Verification card at sibling Step 5.5.5 showed GREEN across all fields
- Control has returned to the orchestrator

## Anti-Frankenstein reminders

- **Do not duplicate the sibling skill's six-step flow here.** This file is a contract + pointer, not a runbook. The sibling owns its implementation
- **Do not add fallback auth mechanisms** (e.g. SSH passphrase recovery, PAT regeneration from scratch, alternate auth providers) — if the sibling's gate is red, the orchestrator halts and the user owns the recovery
- **Do not cache the PAT anywhere outside `.env.local` in the target folder** — not in memory files, not in Genesis's repo, not in an environment variable during the orchestrator run. The sibling writes it once to `.env.local` and subsequent phases read from there
- **Do not bypass the three-probe gate for speed.** The gate is the gate. If it fails, fix the cause, don't bypass the check
- **If the user says `frankenstein`**, halt the orchestrator at Phase 5.5 — the sibling skill does its own anti-Frankenstein handling, but the orchestrator-level halt is belt and braces
