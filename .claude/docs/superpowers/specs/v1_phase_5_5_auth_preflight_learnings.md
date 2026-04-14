<!-- SPDX-License-Identifier: MIT -->
---
name: Phase 5.5 Auth Pre-flight — v1 learnings from live dogfooding
description: Concrete pain points discovered during Project Genesis v1 self-bootstrap on 2026-04-14 that must be fixed before the v1 template ships
type: spec
target_version: v1
created_at: 2026-04-14
originSessionId: project-genesis v1 bootstrap
status: active
---

# Phase 5.5 Auth Pre-flight — v1 learnings

## Context

During the v1 self-bootstrap session on 2026-04-14, applying the v0 protocol's vague "auth checkpoint" line revealed several concrete paste-back pattern frictions that Genesis v1 must address before ship. Each learning below came from a real friction observed during this session.

## Learning 1 — Copy-paste values must be isolated

### Pain observed

When instructing the user to create the empty GitHub repo, I presented the description value inside a table row whose cell contained both the text-to-paste and a contextual note:

> | **Description** | `Project Genesis 2026 — recursive project bootstrap template as a Claude Code plugin` *(EN-only par R9 — `myconciergerie-prog/project-genesis` will be polished later in README.md bilingue)* |

The user copy-pasted the **entire cell** into GitHub's description field, including my rendered table markup (`│   │ Description  │`) and my parenthetical note. Result: the repo description is garbled.

### Root cause

Mixing "value to paste" and "note about the value" in the same visual unit. The user's eye couldn't separate what was literal from what was commentary, especially when the rendered Markdown table adds visual borders.

### v1 rule

**Every single value the user must paste into an external system gets its own dedicated fenced code block, with nothing else inside it. Notes and context appear OUTSIDE the code block, before or after.**

Template snippet:

```markdown
**Description** *(paste exactly the content of the code block below, nothing else):*

```
Project Genesis 2026 — recursive project bootstrap template, shipped as a Claude Code plugin
```

*Rationale: short, English-only, states both what it is and how it ships. Will be elaborated later in the bilingual README.*
```

Never put the value to paste inside a table cell. Tables are for comparison matrices, not for instruction sheets.

## Learning 2 — Describe the form fields in their natural order

The v0 auth checkpoint is one vague line. v1 must walk the user top-to-bottom through the GitHub repo-creation form in the exact order the fields appear on the page. Any out-of-order instruction creates doubt ("did I miss something above?") and delays the user.

### v1 rule

The Phase 5.5 instructions follow the literal form order as it is rendered in the GitHub UI at the time the template ships. This means the v1 template contains a form-order snapshot that **must be re-verified** whenever GitHub changes the form. An `expires_at` field on the form snapshot is appropriate — same R8 TTL discipline applied to form specs.

## Learning 3 — Pre-flight test must run BEFORE any Claude write

The v0 bootstrap phase has no explicit pre-flight test. A well-designed Phase 5.5 runs three concrete probes immediately after the user reports done on the paste-back actions:

1. SSH test — `ssh -T -o StrictHostKeyChecking=accept-new git@github.com-<project>` — must print "Hi <user>! You've successfully authenticated"
2. PAT test — `GH_TOKEN='<token>' gh api user` — must return the target user/org
3. Repo existence test — `GH_TOKEN='<token>' gh api repos/<owner>/<repo>` — must return 200

If any one fails, the template does not proceed to the bootstrap writes. The user gets a targeted recovery instruction for the failing probe. This is the gate.

The v1 template codifies these three probes as the end of Phase 5.5 — they are Phase 5's entry condition.

## Learning 4 — PAT scope checklist with `Administration: Read and write`

The canonical PAT scope checklist from `feedback_project_genesis_auth_preflight.md` listed Contents RW, Metadata R, Pull requests RW, Workflows RW. **Missing**: Administration RW. Without it, the PAT cannot PATCH the repo's description, topics, visibility, or other metadata-level settings. Cosmetic for some projects, blocking for projects that want to lock down settings programmatically.

### v1 rule

Add **Administration: Read and write** to the canonical PAT scope checklist. Explain it is needed for setting repo description, topics, visibility toggles, and repo-level settings management. The scope is safe within the "All repositories" access mode — it does not create or delete repos.

Updated canonical PAT scope list for v1:

- Contents: Read and write
- Metadata: Read (auto)
- Pull requests: Read and write
- Workflows: Read and write
- **Administration: Read and write** *(NEW — learned 2026-04-14)*

## Learning 5 — Paste-back cost becomes the v2 roadmap justification

See `v2_phase_minus_one_dependencies_automation.md`. The paste-back cost observed during this session (three separate GitHub forms, one description error, one PAT scope gap, ~10 minutes total) is the concrete justification for introducing a Phase -1 Dependencies Pre-flight in v2 that requests browser automation MCPs up front.

## Application for v1 template

- Rewrite Phase 5.5 in the v1 template file with the learnings above baked in
- Every form-field value uses its own fenced code block
- Three-probe pre-flight test is the explicit exit condition for Phase 5.5
- PAT scope list includes Administration RW
- Form order matches GitHub's actual 2026 UI
- v2 pointer: "If browser automation MCPs are installed, see Phase -1 flow instead"
