<!-- SPDX-License-Identifier: MIT -->
---
name: Phase 5.5.3 empty repo creation walkthrough
description: Create the empty target GitHub repo via web UI paste-back — fine-grained PATs cannot create user-owned repos via API, a hard lesson from Aurum v0_init and project-genesis v1 bootstrap — with every form field value in its own isolated fenced code block and in the actual UI field order
type: template
stage: 5.5.3
expires_at: 2026-05-14
---

# Phase 5.5.3 — Empty repo creation

Fine-grained PATs **cannot create user-owned repos via API**. The `gh repo create` CLI command silently fails with `HTTP 404 Not Found` or `HTTP 422 Unprocessable Entity` depending on the version. The only reliable method for Genesis-downstream projects is paste-back through the web UI.

This was learned the hard way during Aurum v0_init (2026-04-14) and re-confirmed during project-genesis v1 bootstrap (2026-04-14). It is baked in as a v1 invariant and is not revisited in this skill.

**Form snapshot date**: 2026-04-15 — re-verify when GitHub updates the form layout. See `expires_at` in the frontmatter.

## Template variables

- `{{PROJECT_SLUG}}` — from the consent card
- `{{GITHUB_OWNER}}` — from the consent card
- `{{REPO}}` — from the consent card (usually matches `{{PROJECT_SLUG}}`)
- `{{VISIBILITY}}` — `private` or `public` from the consent card

## Step 1 — Open the form

**URL to open** *(paste exactly the content of the code block below, nothing else):*

```
https://github.com/new
```

Open in the Chrome profile chosen in the consent card. If the user is not signed into `{{GITHUB_OWNER}}` in that profile, the form's Owner dropdown will not list the target — stop and surface a recovery card asking the user to sign in additively (never `sign out` — see additive auth rule in Layer 0).

## Step 2 — Fill the form top-to-bottom

The GitHub repo creation form has these fields in this order. Each paste value gets its own fenced code block — never inside a table cell.

### Owner (dropdown)

GitHub label: **Owner**

Click the dropdown and select:

**Value to select** *(exact string shown in the dropdown):*

```
{{GITHUB_OWNER}}
```

**Do not leave the default.** Default is usually the signed-in user's personal account, which may be wrong for org-owned repos. If the dropdown does not contain `{{GITHUB_OWNER}}`, the user is not signed into that account in the current Chrome profile — stop.

### Repository name

GitHub label: **Repository name**

**Value to paste** *(paste exactly the content of the code block below, nothing else):*

```
{{REPO}}
```

A green checkmark should appear next to the field ("is available"). If GitHub shows a red X and "already exists", surface a recovery card:

- Use the existing repo as-is (skip the create step, go straight to Step 5.5.4).
- Pick a new repo name and re-run the consent card.

### Description

GitHub label: **Description (optional)**

**Value to paste** *(paste exactly the content of the code block below, nothing else):*

```
Bootstrap target repo for {{GITHUB_OWNER}}/{{REPO}} — created by the Project Genesis Phase 5.5 Auth Pre-flight skill
```

This description is intentionally English-only and terse. A better description lives in the bilingual README that Phase 5 writes; this field is just a placeholder so the repo isn't blank on the GitHub About panel before the first push.

The description **must** go in its own code block. Learning 1 of `v1_phase_5_5_auth_preflight_learnings.md` was that a garbled table-cell paste is the single most expensive mistake in this phase.

### Visibility

GitHub label: **Public / Private** radio group

Click:

**Option to select** *(exact label on the form):*

```
{{VISIBILITY}}
```

Default for Genesis downstream is `Private` — locks down the blast radius until the project is ready. Flip to `Public` via the Settings tab later, once the README is polished.

### "Initialize this repository with" section

**Leave every box UNCHECKED.** Specifically:

- **Add a README file** — UNCHECK (the bilingual README will be written by Phase 5; a default README would conflict)
- **Add .gitignore** — UNCHECK (Phase 5 writes the .gitignore; GitHub's defaults don't know about `.env.local`)
- **Choose a license** — UNCHECK (Phase 5 writes `LICENSE` with the exact SPDX header; GitHub's license picker adds a file the skill doesn't expect)

The first push from Phase 5 will fail with `! [rejected] main -> main (fetch first)` if the repo is not empty. Empty means empty.

### Create the repo

Click **Create repository**. GitHub takes 1-2 seconds and redirects to the new repo's empty-state page, which shows three suggested setup blocks (we use none of them — Phase 5 writes the repo files locally and pushes).

Report `done` or `created` back to the skill.

## Step 3 — Verify the repo exists via API

Run the canonical repo existence probe:

```bash
GH_TOKEN="$(grep '^GH_TOKEN=' .env.local | cut -d= -f2-)" gh api repos/{{GITHUB_OWNER}}/{{REPO}} --jq .full_name
```

Expected output (a single line):

```
{{GITHUB_OWNER}}/{{REPO}}
```

If `HTTP 404`, the repo was not created (user navigated away before clicking), the name is wrong, or the PAT lacks Contents: Read. Recovery: re-open the form and re-create.

If `HTTP 403 Resource not accessible by personal access token`, the PAT lacks Contents: Read OR `Administration: Read and write`. Recovery: re-create the PAT with the full canonical scope list per `pat-walkthrough.md`.

This verification is a subset of the full three-probe test (Step 5.5.4) — it runs here because a missing repo blocks every downstream action.

## Step 4 — Configure git remote in the worktree

From the Genesis worktree root:

```bash
git remote set-url origin git@github.com-{{PROJECT_SLUG}}:{{GITHUB_OWNER}}/{{REPO}}.git
```

Note the host is `github.com-{{PROJECT_SLUG}}` (the alias from Step 5.5.1), not `github.com`. This binding is what gives each project its own SSH identity.

Verify:

```bash
git remote -v
```

Expected output (both origin lines end with the alias URL — NOT a plain `github.com:` URL):

```
origin  git@github.com-{{PROJECT_SLUG}}:{{GITHUB_OWNER}}/{{REPO}}.git (fetch)
origin  git@github.com-{{PROJECT_SLUG}}:{{GITHUB_OWNER}}/{{REPO}}.git (push)
```

If either line shows `github.com:` without the alias, re-run the `git remote set-url` command. Wrong-alias remotes are the most common source of "permission denied" failures at Phase 5's first push.

## Exit condition

- Target repo exists at `{{GITHUB_OWNER}}/{{REPO}}`.
- `gh api repos/{{GITHUB_OWNER}}/{{REPO}}` returns 200 with `full_name = "{{GITHUB_OWNER}}/{{REPO}}"`.
- Git remote origin is bound to `github.com-{{PROJECT_SLUG}}` alias.
- Control passes to `three-probe-test.md` for Step 5.5.4.

## Anti-Frankenstein

- Do not try to `gh repo create` as a shortcut. It does not work for fine-grained PATs on user-owned repos. Period.
- Do not check "Initialize with README". The empty state is a contract with Phase 5.
- Do not paste the description inside a table cell or a sentence — isolated code block only.
- Do not create the repo before the PAT is verified — a broken PAT plus a created repo is a worse state than no repo at all.
