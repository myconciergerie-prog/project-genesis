<!-- SPDX-License-Identifier: MIT -->
---
name: Phase 5.5.2 PAT walkthrough
description: Top-to-bottom walkthrough of the GitHub fine-grained PAT creation form in its actual UI order, with every copy-paste value isolated in its own fenced block, including the canonical scope list with Administration Read and write discovered missing during v1 bootstrap
type: template
stage: 5.5.2
expires_at: 2026-05-14
---

# Phase 5.5.2 — Fine-grained PAT walkthrough

This file walks the user through GitHub's fine-grained PAT creation form **in the exact order the fields appear on the page**, top to bottom, per `v1_phase_5_5_auth_preflight_learnings.md` Learning 2. Every value the user pastes into a field lives in its own isolated fenced code block (Learning 1). Any out-of-order instruction creates doubt and delays the user.

**Form snapshot date**: 2026-04-15 — re-verify when GitHub updates the form layout. See the `expires_at` field in the frontmatter; re-run a visual inspection after that date and bump the snapshot.

## Template variables

- `{{PROJECT_SLUG}}` — from the consent card
- `{{GITHUB_OWNER}}` — from the consent card (user login or org name)
- `{{REPO}}` — from the consent card
- `{{EXPIRATION_DAYS}}` — from the consent card (30 / 60 / 90)

## Step 1 — Open the form

**URL to open** *(paste exactly the content of the code block below, nothing else, in the Chrome profile chosen in the consent card):*

```
https://github.com/settings/personal-access-tokens/new
```

If GitHub asks the user to sudo-authenticate (re-enter password for the settings page), they do that first. The skill does not interfere.

## Step 2 — Fill the form top-to-bottom

The following fields appear in this order in GitHub's UI as of the snapshot date. Each one gets its own code block.

### Token name

GitHub label: **Token name**

**Value to paste** *(paste exactly the content of the code block below, nothing else):*

```
project-genesis-{{PROJECT_SLUG}}-{{EXPIRATION_DAYS}}d
```

Rationale (outside the block, not for pasting): a unique, searchable name makes later rotation easy. Includes project, slug, and expiration window so a future audit sees the full metadata at a glance.

### Description

GitHub label: **Description**

**Value to paste** *(paste exactly the content of the code block below, nothing else):*

```
Fine-grained PAT for {{GITHUB_OWNER}}/{{REPO}} — scopes: Contents RW, Metadata R, Pull requests RW, Workflows RW, Administration RW
```

### Resource owner

GitHub label: **Resource owner**

Click the dropdown and select:

**Value to select** *(exact string shown in the dropdown):*

```
{{GITHUB_OWNER}}
```

**Do not leave the default.** The default is usually the user's personal account, which is wrong for any org-owned or alternate-user-owned repo. If the target owner is not in the dropdown, the user needs to sign into the correct account first — stop and surface a recovery card.

### Expiration

GitHub label: **Expiration**

Select the radio button for **Custom**, then pick a date `{{EXPIRATION_DAYS}}` days from today. GitHub stores this date verbatim; the skill records it to `memory/reference/github_{{PROJECT_SLUG}}_account.md` for future rotation warnings.

Pre-set options (7/30/60/90 days) are fine; GitHub also accepts `No expiration` but the skill **never** recommends it — a non-expiring PAT is a security-floor violation.

### Repository access

GitHub label: **Repository access**

Select the radio button for:

**Option to select** *(exact label on the form):*

```
All repositories
```

**Do not select `Only select repositories`** at this step. The target repo does not exist yet — it is created in Step 5.5.3, after this PAT is created. Selecting `Only select` would either force a second pass or block the PAT entirely. `All repositories` is the only viable choice during bootstrap.

If the user already has the target repo created (rare — usually only in resume-from-midway scenarios), they can pick `Only select repositories` and choose the repo; the rest of the skill still works.

### Repository permissions

GitHub label: **Repository permissions** — a list of toggles.

Click each row below and set it to the level shown. **Every row must be set explicitly** — defaults are usually `No access` and the PAT will fail silently later if any row is left unset.

| # | Permission | Level | Why |
|---|---|---|---|
| 1 | **Contents** | **Read and write** | Push commits, create branches, update files via API |
| 2 | **Metadata** | **Read** | Auto-selected when anything else is on; cannot deselect |
| 3 | **Pull requests** | **Read and write** | `gh pr create`, `gh pr merge`, review flows |
| 4 | **Workflows** | **Read and write** | Trigger / update GitHub Actions workflow files |
| 5 | **Administration** | **Read and write** | **CRITICAL** — PATCH repo description, topics, visibility, settings. Missing this is a **silent blocker** |

The Administration row is the one the v0 skill missed. Its absence is invisible until the first `gh api --method PATCH repos/{{GITHUB_OWNER}}/{{REPO}}` call returns HTTP 403 `Resource not accessible by personal access token`. The skill **never** skips it.

### Organization permissions (org-owned PATs only)

If `{{GITHUB_OWNER}}` is an org (not a user), GitHub also shows an **Organization permissions** section. For Genesis v1 defaults, leave every row at **No access** — none are needed for the baseline workflow. Users who want advanced flows (custom roles, org-level secrets, audit log reads) opt in manually.

### Account permissions

GitHub label: **Account permissions** — a list of toggles. Leave every row at **No access** for v1. These are user-account-level, not repo-level, and none are needed for the baseline workflow.

## Step 3 — Generate the token

Scroll to the bottom and click **Generate token**. GitHub may ask for sudo auth again.

GitHub renders the token **once** on a green banner. It looks like:

```
github_pat_11XXXXXXXXXXXXXXXXXXXX_YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
```

The user **must copy the full token now** — GitHub never shows it again. If they navigate away before copying, they have to delete the PAT and create a new one.

## Step 4 — Inject the token into `.env.local`

The user pastes the token back into the Claude Code conversation. The skill takes it and writes it to `.env.local`:

```bash
# From the worktree root, not the repo root
printf 'GH_TOKEN=%s\n' '<PASTED_TOKEN>' >> .env.local
```

**Safeguards** (the skill enforces these):

1. `.env.local` is already gitignored (verify via `git check-ignore .env.local` — must exit 0). If not, stop and add it to `.gitignore` first.
2. The token value is never echoed to stdout after this. The skill masks it in subsequent output with `github_pat_****`.
3. Never `git add .env.local`, never display its contents, never push it anywhere.

## Step 5 — Quick sanity test

```bash
GH_TOKEN="$(grep '^GH_TOKEN=' .env.local | cut -d= -f2-)" gh api user --jq .login
```

Expected output (a single line): `{{GITHUB_OWNER}}`.

If the output is a different login, the user created the PAT under the wrong resource owner — stop and re-create with the correct owner.

If the command returns `HTTP 401` or `Bad credentials`, the token was mis-copied (trailing whitespace, partial paste). Recovery: re-create the PAT from scratch — GitHub's one-time-view prevents re-reading.

This sanity test is not the full three-probe gate (that's Step 5.5.4) — it's a cheap early confirmation that the token itself is valid before we sink time into Step 5.5.3.

## Exit condition

- PAT is created with the full canonical scope list.
- Token is stored in `.env.local` (gitignored).
- `gh api user` returns `{{GITHUB_OWNER}}`.
- Control passes to `empty-repo-create.md` for Step 5.5.3.

## Anti-Frankenstein

- Do not collapse the scope list into "all permissions" — the explicit list is the teaching surface and the safety floor.
- Do not auto-paste the token anywhere except `.env.local`. Never log it, never `echo` it.
- Do not skip the sanity test to "save a round-trip" — it's a 200 ms call that catches 80% of typos.
- Do not create the PAT without an expiration. Always bounded.
