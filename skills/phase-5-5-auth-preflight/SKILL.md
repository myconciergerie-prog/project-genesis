---
name: phase-5-5-auth-preflight
description: Auth Pre-flight for Genesis downstream projects — walks the user through dedicated SSH keygen + fine-grained GitHub PAT creation + empty-repo creation, then runs the canonical three-probe pre-flight (SSH, PAT user, repo existence) as the explicit exit condition before Phase 5 starts writing. Every copy-paste value lives in its own isolated fenced block. Reads Phase -1 stack state to decide automated vs paste-back branches.
---

# Phase 5.5 — Auth Pre-flight

This skill is the gate between "the dev machine is installed" (Phase -1) and "Genesis is about to write the first commit / push to GitHub" (Phase 5). It ensures the target GitHub identity is correctly wired before any write happens: dedicated SSH key, host alias, fine-grained PAT, empty target repo, and three green probes.

Full design rationale: `.claude/docs/superpowers/specs/v1_phase_5_5_auth_preflight_learnings.md` — each file in this skill addresses a specific learning from the 2026-04-14 v1 self-bootstrap session.

## When to invoke

- The user types `/phase-5-5-auth-preflight`.
- The user says any of:
  - "run phase 5.5"
  - "auth pre-flight"
  - "lance la pre-flight auth"
  - "set up github for this project"
  - "wire the github account for genesis"
- The Genesis protocol orchestrator invokes this skill as Phase 5.5, immediately before Phase 5 writes the first commit.
- At session open, if the current project folder contains no `memory/reference/ssh_*_identity.md` and no `.git/config` remote, surface `/phase-5-5-auth-preflight` as a one-line suggestion.

**Never auto-run without consent.** Phase 5.5 touches SSH keys, creates PATs, and binds the project to a real GitHub identity — always ask first via `consent-card.md`.

## Prerequisites

- Phase -1 has completed — `memory/reference/automation-stack.md` exists and reports `git`, `gh`, and a browser as healthy. If Phase -1 did not run, surface `/phase-minus-one` instead and exit.
- The user has a GitHub account (any tier) that owns — or will own — the target repository.
- The user is signed into the correct Chrome profile for this project (per Layer 0 Chrome profile mapping). If unknown, the consent card asks.

## The flow — six numbered steps (v1.1 — CLI-first auth)

Phase 5.5 is a six-step linear flow. v1.1 replaces the browser-heavy v1.0 path with a CLI-first approach proven during the 2026-04-16 self-dogfood. User intervention reduced from 4 browser steps to 1 OAuth click + 2FA.

| # | Step | Purpose | User intervention |
|---|---|---|---|
| 5.5.0 | Consent + scope card | Confirm which project, which GitHub owner, which Chrome profile | One prompt |
| 5.5.1 | OAuth login via `gh` | `gh auth login --web` with device flow, browser opened via `Start-Process` to correct Chrome profile | One click "Authorize" + 2FA code (true security floor) |
| 5.5.2 | SSH keygen + `gh ssh-key add` | Generate dedicated ed25519 key, write `~/.ssh/config` alias, upload public key via CLI | None (fully automated) |
| 5.5.3 | Repo create via `gh repo create` | Create private repo + set remote + push in one command | None (fully automated) |
| 5.5.4 | Three-probe test | Run `ssh -T`, `gh api user`, `gh api repos/<owner>/<repo>`, gated exit | None if green |
| 5.5.5 | Verification card | Render health card, write `memory/reference/github_<project>_account.md` + `memory/reference/ssh_<project>_identity.md` | Read the card |

**v1.1 auth path (proven 2026-04-16):**

```bash
# Step 5.5.1 — ONE user interaction (OAuth + 2FA)
gh auth login --hostname github.com --web --git-protocol https \
  --scopes "repo,workflow,read:org,admin:public_key" &
# Open device auth URL in correct Chrome profile
powershell -NoProfile -Command "Start-Process '<chrome-path>' \
  -ArgumentList '--profile-directory=\"<profile>\"','https://github.com/login/device'"
# Copy device code to clipboard
echo -n "<code>" | clip.exe

# Step 5.5.2 — zero interaction
gh auth setup-git
ssh-keygen -t ed25519 -f "$HOME/.ssh/id_ed25519_<slug>" -C "<slug>-genesis-bootstrap" -N ""
gh ssh-key add "$HOME/.ssh/id_ed25519_<slug>.pub" --title "<slug>" --type authentication

# Step 5.5.3 — zero interaction
gh repo create <owner>/<repo> --private --source=. --remote=origin --push
```

Steps 5.5.2–5.5.3 require zero user intervention — they use the OAuth token from Step 5.5.1. The three-probe test at 5.5.4 is unchanged. Browser paste-back (`pat-walkthrough.md`, `empty-repo-create.md`, `playwright-automation.md`) remains as legacy fallback for environments where `gh` CLI is unavailable.

## Files in this skill

- `SKILL.md` — this file; entry point and flow overview.
- `consent-card.md` — Step 5.5.0 template collecting project slug, GitHub owner, PAT scopes, Chrome profile, expiration window.
- `ssh-keygen.md` — Step 5.5.1 walkthrough: per-project ed25519 key, `~/.ssh/config` host alias with `IdentitiesOnly yes`, public key added to GitHub.
- `pat-walkthrough.md` — Step 5.5.2 walkthrough: fine-grained PAT creation checklist with the full canonical scope list.
- `empty-repo-create.md` — Step 5.5.3 walkthrough: web-UI paste-back for repo creation, every form field in its own fenced code block.
- `three-probe-test.md` — Step 5.5.4 runner: the canonical three probes, pass/fail gating, targeted recovery branches.
- `playwright-automation.md` — conditional branch: if Playwright MCP is present from Phase -1, drive the GitHub forms programmatically; else fall back to paste-back.
- `verification.md` — Step 5.5.5 health card + canonical schemas for the two reference memory files written at skill completion.

## How the skill uses these files

1. Read `memory/reference/automation-stack.md` (written by Phase -1) to know which optional automations are available (Playwright MCP, `gh` CLI, Chrome profile presence).
2. Render `consent-card.md` — collect project slug, GitHub owner, PAT expiration, scopes confirmation, Chrome profile choice. Record the outcome in `memory/reference/consent-log.md`.
3. Branch into `ssh-keygen.md` for Step 5.5.1 — keygen is always local (no PAT needed); the public-key add is paste-back if Playwright is absent, automated otherwise.
4. Branch into `pat-walkthrough.md` for Step 5.5.2 — always paste-back for the token capture (the raw token only appears once in the GitHub UI and cannot be retrieved via API later).
5. Branch into `empty-repo-create.md` for Step 5.5.3 — paste-back by default (user-owned repos cannot be created via fine-grained PATs); Playwright drives the form if available.
6. Run `three-probe-test.md` as Step 5.5.4. Every probe must pass before handing control back.
7. Render `verification.md`, write the two reference memory files, hand control back to the Genesis protocol for Phase 5.

## Canonical PAT scope list — the v1 truth

Fine-grained PATs for Genesis-downstream projects need these exact scopes. The list was finalized during v1 self-bootstrap after the `Administration: Read and write` gap was discovered mid-session (`v1_phase_5_5_auth_preflight_learnings.md` Learning 4).

| Scope | Level | Why |
|---|---|---|
| Contents | **Read and write** | Push commits, create branches, update files via API |
| Metadata | **Read** *(auto-selected)* | Always required; cannot be deselected |
| Pull requests | **Read and write** | `gh pr create`, `gh pr merge`, review flows |
| Workflows | **Read and write** | Trigger / update GitHub Actions workflow files |
| Administration | **Read and write** | PATCH repo description, topics, visibility, settings — missing this is a **silent blocker** for any repo-metadata write |

**Repository access**: `All repositories` (not `Only select`) — the target repo does not exist yet at PAT creation time, so `Only select` would force a second pass. Resource owner: the target user/org, NOT the default personal account.

**Expiration**: default 90 days. The skill records the expiration date so a future session can warn before rotation is needed.

## Isolated copy-paste rule — the v1 law

Every single value the user must paste into an external system lives in **its own dedicated fenced code block**, with nothing else inside it. Notes and context appear outside the block, before or after. Tables are for comparison matrices, not for instruction sheets. This rule is non-negotiable and was learned the hard way — see `v1_phase_5_5_auth_preflight_learnings.md` Learning 1.

Every template file in this skill follows the rule. If you edit one of them, keep the rule.

## Security floor — what Phase 5.5 never automates

- **Private SSH key material**: always stays on the user's machine, never printed to the transcript, never copied elsewhere.
- **PAT token capture**: the raw token appears once in GitHub's UI. The skill never asks the user to paste it into an unencrypted channel other than `.env.local`. It never auto-commits `.env.local`.
- **Signing in to GitHub**: if the target Chrome profile is not signed into the right GitHub account, the skill hands control to the user to sign in manually.
- **2FA / hardware key prompts**: always user-driven.
- **Repo deletion or visibility downgrade**: never performed by this skill.

When the skill hits one of these, it stops and surfaces a paste-back micro-card; no "convenience wrapper" ever bundles a security-floor step.

## Playwright branch — opt-in automation

If `memory/reference/automation-stack.md` lists Playwright MCP as healthy, the skill offers a one-line opt-in during the consent card: *"Automate the GitHub form pass-through via Playwright? (y/N, default N — paste-back is the safe baseline)"*. The user must explicitly opt in. Paste-back is always the safe fallback and is the default path.

See `playwright-automation.md` for the exact branch logic and the short list of known form selectors (with a TTL — GitHub UI changes invalidate the selectors).

## Anti-Frankenstein reminders

- **Do not create more than one SSH key per project.** One ed25519 key, one host alias, one project. Never reuse an existing key "because it's easier".
- **Do not auto-select "All scopes" on the PAT form.** The canonical list is specific for a reason — each scope is a blast-radius increment.
- **Do not skip the three-probe test for speed.** Even if everything "looks green", the three probes are the gate. Mode 3 auto in Phase -1 runs them; Phase 5.5 runs them.
- **Do not create the target repo via `gh repo create`.** Fine-grained PATs cannot create user-owned repos — this was a hard lesson and is baked in.
- **Do not wire Administration scope silently.** The user must see the scope list and consent to each item.
- **If the user says `frankenstein`**, stop immediately and back out of the last proposal.

## Exit condition

Phase 5.5 is complete when:

- `memory/reference/ssh_<project>_identity.md` exists with the new key's fingerprint, alias, and SSH config entry.
- `memory/reference/github_<project>_account.md` exists with target owner, repo, PAT scopes, expiration date, and the three-probe test outcome.
- The three probes (SSH, PAT user, repo existence) all returned green on the last run.
- `.env.local` contains `GH_TOKEN=<pat>` and is gitignored.
- Control is handed back to the Genesis protocol for Phase 5.
<!-- SPDX-License-Identifier: MIT -->
