<!-- SPDX-License-Identifier: MIT -->
---
name: Phase 0 — Seed loading
description: Runbook for Phase 0 of the Genesis protocol — read the target project folder's `config.txt` seed and any accompanying mixed media, parse the project intent into a structured handoff, and populate the working context that downstream phases consume.
---

# Phase 0 — Seed loading

Phase 0 is the first phase after Phase -1 finishes and the dev stack is verified. Its job is to **turn the raw user input into a structured project intent** that the remaining phases can consume without re-parsing.

The user invokes the orchestrator from inside a folder that either already contains seed material (a `config.txt` file, optionally with PDFs / images / sketches / URL lists) or is about to. Phase 0 is the formal moment where the orchestrator inspects that material and asks the user to confirm the parsed intent before any write happens.

## Prerequisites

- Phase -1 has completed — `memory/reference/automation-stack.md` exists OR the user explicitly confirmed skipping Phase -1 at the top-level consent card.
- The target project folder is the current working directory of the Claude Code session.
- The top-level consent card from `SKILL.md` Step 0 has been confirmed by the user.

## The flow — five steps

### Step 0.1 — Inspect the input folder

List every non-hidden file in the target folder (the one Claude Code was opened in). Expected shapes, any of:

| Shape | What it means |
|---|---|
| Empty folder | User wants to start from zero — Phase 0.2 will offer to scaffold a `config.txt` interactively |
| `config.txt` only | Minimal seed — the standard happy path |
| `config.txt` + PDFs / images | Rich seed — extract text and OCR-able content via `Read` tool (supports PDF + image) |
| `config.txt` + a `seed/` or `inputs/` subfolder | Bundled seed — same as above but in a subdirectory |
| No `config.txt` but a `README.md`, `BRIEF.md`, or `PLAN.md` | Unusual — ask the user whether one of those should be read as the seed |
| Folder with existing code (`package.json`, `pyproject.toml`, `Cargo.toml`, `.git/`) | **Stop**. This is not a greenfield bootstrap. Surface the situation and ask whether the user meant `/phase-5-5-auth-preflight` or `/journal-system` instead |

Use `Glob` with `*` in the target folder to list top-level entries. Use `Read` on each text or PDF file, one by one, bounded by the security floor rules (never log full contents of files that look like they contain secrets — the same redaction rules from `session-post-processor` apply).

### Step 0.2 — Parse `config.txt` into a structured intent

`config.txt` is free-form but expected to cover:

- **Project name** — the one-line title
- **Project slug** — optional, derived from the name if absent (lowercase, spaces to `-`, strip accents, < 50 chars, alphanumeric + `-` only)
- **One-paragraph vision** — what the project is and why it exists
- **Stack preferences** — optional language / framework / hosting hints
- **License** — defaults to MIT per `memory/master.md`; Apache-2 as documented pivot path
- **Is-this-a-plugin flag** — optional; if true, the orchestrator lands skill stubs at Phase 4
- **Plan tier hint** — optional; affects multidevice branch in Phase -1 if re-run, otherwise consumed at Phase 5.5 consent card
- **Scope lock references** — optional; names other projects that must be respected as frozen during this bootstrap (like the Aurum freeze rule from this very Genesis project). Each entry in `config.txt` can be either a bare slug (`aurum-ai`) or a free-form phrase (`aurum-ai (frozen at 0b1de3d until Genesis v1 ships)`). Phase 0 stores the original verbatim string in `bootstrap_intent.md` under "Scope locks", **and also** derives a machine slug for each entry: take the first whitespace-terminated token, lowercase it, strip surrounding punctuation, and replace internal non-alphanumerics with `-`. Phase 4 Step 4.5 uses the derived slug as the filename (`memory/project/<slug>_frozen_scope_lock.md`) and the verbatim string as the "until when" context inside the file.

If `config.txt` is missing fields, **do not invent them**. Record the gap and surface it at Step 0.4.

If `config.txt` is missing entirely, Step 0.1 already detected an empty folder. Offer the user an **interactive seed creation card** that asks each field one at a time (in French or English per Layer 0 language policy), then write `config.txt` into the target folder. Ask consent before writing.

### Step 0.3 — Read the accompanying mixed media

For each non-`config.txt` file found in Step 0.1:

- **PDF** — use `Read` with `pages` parameter if > 10 pages, else full read. Extract the relevant sections into the working intent. Never copy the full PDF into memory; extract only the portions that inform the project vision.
- **Image** — use `Read`. Claude is multimodal; the image is interpreted in-context. Mention the image's content in the parsed intent so downstream phases know it exists.
- **Markdown / text** — use `Read`, parse as additional context. Treat as supplementary to `config.txt`, not a replacement.
- **URL lists** — files named `urls.txt`, `links.md`, `sources.md`, etc. Each line is treated as a candidate research source for Phase 2's research cache seed entries.
- **Unknown binary** — list it in the report but do not auto-process. Ask the user whether to include or skip.

Mixed media are a courtesy input, not a requirement. A `config.txt`-only bootstrap is the happy path.

### Step 0.4 — Surface the parsed intent card

Render a structured card showing everything Phase 0 parsed. Use the following template — every field listed explicitly so gaps are visible:

```
📋 Parsed intent — Phase 0

Target folder          : <absolute path>
Project name           : <parsed or [missing]>
Project slug           : <parsed or derived-from-name or [missing]>
Vision                 : <parsed paragraph or [missing]>
Stack hints            : <parsed list or [missing]>
License                : <parsed or MIT (default)>
Is-a-plugin            : <yes | no | [missing]>
Plan tier              : <Max | Pro | Team | Free | [missing]>
Scope locks            : <parsed list or [none]>
Mixed media            : <file list or [none]>

Gaps to fill before Phase 1:
  - <gap 1>
  - <gap 2>
  ...

Proceed with these values?  (yes / edit / abort)
```

The user responds with:

- **yes** → persist the intent into `memory/project/bootstrap_intent.md` (a new file — does not exist yet in Phase 0, gets written here) and proceed to Phase 1.
- **edit** → enter a targeted edit flow: the user picks a field, corrects the value, and the card is re-rendered. Loop until the user says yes or abort.
- **abort** → exit the orchestrator cleanly. No write happens outside the target folder. `config.txt` may have been written at Step 0.2 if it was missing — leave it in place as audit trail, do not delete.

### Step 0.5 — Persist the intent as `bootstrap_intent.md`

Once the user confirms, write `memory/project/bootstrap_intent.md` inside the target folder. This file is the **contract** between Phase 0 and every downstream phase. Later phases read it instead of re-parsing `config.txt`, which keeps the orchestrator flow deterministic.

Template:

```markdown
<!-- SPDX-License-Identifier: MIT -->
---
name: Bootstrap intent — <project slug>
description: Structured project intent parsed from config.txt and mixed media at Genesis Phase 0. Consumed by all downstream phases as the source of truth for project name, slug, vision, license, plugin flag, plan tier, and scope locks.
type: project
phase: 0
---

# Bootstrap intent — <project slug>

## Parsed at

<ISO date and time of Phase 0 run>

## Fields

| Field | Value | Source |
|---|---|---|
| Project name | <value> | config.txt / user edit |
| Slug | <value> | config.txt / derived |
| Vision | <one-paragraph> | config.txt |
| License | <value> | config.txt / default |
| Is-a-plugin | <yes|no> | config.txt / user edit |
| Plan tier | <value> | config.txt / user edit |
| Stack hints | <list> | config.txt |
| Scope locks | <list> | config.txt / user edit |
| Mixed media | <file list> | folder scan |

## Raw config.txt

<verbatim contents — trimmed if > 5 KB>

## Gaps noted at Phase 0

<list of gaps the user acknowledged — each either resolved by a user-provided value or marked "deferred to <phase>">
```

After the file is written, Phase 0 is complete. Control returns to the orchestrator which advances to Phase 1.

## Exit condition

Phase 0 is complete when:

- `memory/project/bootstrap_intent.md` exists in the target folder.
- All mandatory fields (name, slug, vision) are populated.
- The user has confirmed the intent card (user said "yes", not "edit" or "abort").
- Phase 1 can read `bootstrap_intent.md` and proceed without needing to re-prompt the user for any intent question.

## Common failures

- **`config.txt` is binary / unreadable** — stop, surface an error, ask whether to rename or replace.
- **Folder contains existing code** — stop, surface the situation, direct the user to the right skill (`phase-5-5-auth-preflight` for an existing project needing GitHub setup, `journal-system` for capturing reflections, etc.). Do not overwrite.
- **Vision paragraph is empty in `config.txt` and user does not provide one during edit** — cannot proceed. Phase 1 and Phase 4 need the vision. Abort cleanly.
- **Slug conflicts with an existing sibling project on this machine** — warn, suggest appending `-2` or editing `config.txt`. Do not auto-rename.
- **Slug equals the orchestrator's own slug** (`project-genesis` or whatever the current plugin's `.claude-plugin/plugin.json` reports as `name`) — **structural stop, not a warning**. This is Guard B from `SKILL.md` Step 0 re-confirmed at Phase 0.2 in case the slug was derived rather than explicit. Halt with the Guard B message template. The user must pick a differentiated slug (e.g. append `-selfdogfood`, `-test`, a date stamp, or rename the project) before the orchestrator can continue. Added in v1.2.1 after friction F27.
- **Mixed media file is too large to `Read` in one shot** — extract what fits, note the truncation in the intent card, ask the user whether to proceed or split.

## Anti-Frankenstein reminders

- **Do not parse `config.txt` into a DSL.** Free-form text with a light field-extraction pass. No schema validator, no JSON Schema, no Pydantic model.
- **Do not infer fields from mixed media when `config.txt` is silent.** If `config.txt` does not name the project, ask the user — do not guess from a PDF title.
- **Do not auto-create `config.txt` from scratch without explicit user typing.** The interactive seed card asks each field; the user provides every value; Claude writes only what the user confirms.
- **Do not write outside `memory/project/` during Phase 0.** The only file Phase 0 creates is `bootstrap_intent.md` (and optionally `config.txt` in the target folder if it was missing and the user opted into the interactive seed card).
- **If the user says `frankenstein`**, drop the parsing pass and fall back to a minimal three-question prompt (name, vision, license).
