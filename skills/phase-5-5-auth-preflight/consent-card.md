<!-- SPDX-License-Identifier: MIT -->
---
name: Phase 5.5.0 consent card
description: One-prompt consent collector that captures project slug, GitHub owner, PAT scope confirmation, PAT expiration window, Chrome profile choice, and Playwright opt-in before any Phase 5.5 side effect runs
type: template
stage: 5.5.0
---

# Phase 5.5.0 — Consent card

Rendered once, at the start of Phase 5.5, before any keygen / PAT / repo creation. Every field defaults to a safe null — the user must actively pick a value for the skill to proceed. Consent is logged to `memory/reference/consent-log.md` so a future session can audit who approved what and when.

## Template variables

- `{{PROJECT_SLUG}}` — derived from current directory name, e.g. `project-genesis`
- `{{GITHUB_OWNER_DEFAULT}}` — derived from Phase -1 state if `gh auth status` reported a login, else empty
- `{{CHROME_PROFILES}}` — the list of Chrome profiles discovered via Layer 0 mapping
- `{{PLAYWRIGHT_PRESENT}}` — boolean from `memory/reference/automation-stack.md`

## Card body

```
===== Phase 5.5.0 — Consent =====

Project about to be auth-wired:
  Slug:              {{PROJECT_SLUG}}
  Git working dir:   {{CWD}}

GitHub target
  [ ] Owner (user or org):   ___________________
       (type the exact login, e.g. myconciergerie-prog)
  [ ] Repository name:       ___________________
       (usually matches the project slug — default: {{PROJECT_SLUG}})
  [ ] Visibility:             private  /  public
       (default: private — R10 anti-Frankenstein suggests private until v1.0.0)

Dedicated SSH key (Phase 5.5.1)
  [ ] Key file name:          id_ed25519_{{PROJECT_SLUG}}
  [ ] Host alias:              github.com-{{PROJECT_SLUG}}
  [ ] Confirm this will NOT replace an existing key:  yes / no
       (additive auth rule — never overwrite)

Fine-grained PAT (Phase 5.5.2)
  [ ] I confirm the canonical scope list:
        - Contents:        Read and write
        - Metadata:        Read (auto)
        - Pull requests:   Read and write
        - Workflows:       Read and write
        - Administration:  Read and write
  [ ] Repository access:      All repositories
  [ ] Expiration window:      30 / 60 / 90 days   (default: 90)

Chrome profile for paste-back steps
  [ ] Profile chosen:          ___________________
       (known profiles on this machine: {{CHROME_PROFILES}})
       Never use `Default` for project work — belongs to another project.

Playwright automation (optional)
  [ ] Playwright MCP present:  {{PLAYWRIGHT_PRESENT}}
  [ ] Opt in to automate form pass-through?  y / N
       (default N — paste-back is always safe; opt in only if you want form clicks scripted)

=================================
```

## Rendering rules

1. Present every line on its own row — the user must be able to check or type into a single line without ambiguity.
2. The GitHub owner and repo name lines are copy-paste-safe — their values go straight into commands later, so they must not contain trailing whitespace or markdown decoration.
3. Default values are shown but never silently applied. The skill asks explicitly.
4. If the user rejects any row, the skill stops and asks what to change. No silent defaults.
5. If the user says "all yes" or "go" the skill treats the defaults as accepted for every null row.

## What to do with the answers

Write the full card answers to `memory/reference/consent-log.md` with an entry:

```markdown
## Phase 5.5.0 consent — YYYY-MM-DD — {{PROJECT_SLUG}}

- GitHub owner: {{OWNER}}
- Repository: {{OWNER}}/{{REPO}}
- Visibility: {{private|public}}
- SSH key: id_ed25519_{{PROJECT_SLUG}} (host alias github.com-{{PROJECT_SLUG}})
- PAT scopes: Contents RW, Metadata R, PR RW, Workflows RW, Administration RW
- PAT repository access: All repositories
- PAT expiration window: {{N}} days
- Chrome profile: {{PROFILE_LABEL}}
- Playwright automation opt-in: {{yes|no}}
- Approved by: user, {{DATETIME_ISO}}
```

If the consent log does not exist, create it with a one-line header. If it exists, append.

## Exit condition

- Every checkbox has a value or an explicit "skip".
- The consent log entry is written.
- Control passes to `ssh-keygen.md` for Step 5.5.1.

## Anti-Frankenstein

- Do not add fields to this card that the skill does not actually consume. Every field must feed a concrete later step.
- Do not collapse the canonical PAT scope list into "all scopes" for speed — the explicit list is the teaching surface.
- Do not auto-accept defaults silently — the user must see and confirm.
