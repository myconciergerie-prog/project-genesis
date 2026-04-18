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
| `drop_zone_intent.md` present | **Primary seed** — written by `genesis-drop-zone` v1.3.2+ at the user's drop-zone consent. Parse via YAML frontmatter in Step 0.2a. Overrides `config.txt` if also present (see precedence rule below). |
| Empty folder | User wants to start from zero — Phase 0.2 will offer to scaffold a `config.txt` interactively |
| `config.txt` only | Minimal seed — the standard happy path |
| `config.txt` + PDFs / images | Rich seed — extract text and OCR-able content via `Read` tool (supports PDF + image) |
| `config.txt` + a `seed/` or `inputs/` subfolder | Bundled seed — same as above but in a subdirectory |
| No `config.txt` but a `README.md`, `BRIEF.md`, or `PLAN.md` | Unusual — ask the user whether one of those should be read as the seed |
| Folder with existing code (`package.json`, `pyproject.toml`, `Cargo.toml`, `.git/`) | **Stop**. This is not a greenfield bootstrap. Surface the situation and ask whether the user meant `/phase-5-5-auth-preflight` or `/journal-system` instead |

Use `Glob` with `*` in the target folder to list top-level entries. Use `Read` on each text or PDF file, one by one, bounded by the security floor rules (never log full contents of files that look like they contain secrets — the same redaction rules from `session-post-processor` apply).

### Precedence rule (v1.3.2)

When Phase 0 Step 0.1 inspects the target folder, it checks for seeds in this order:

1. `drop_zone_intent.md` present → **primary seed**. Parse via YAML frontmatter in Step 0.2a.
2. No `drop_zone_intent.md`, `config.txt` present → **legacy seed**. Parse via free-form text in Step 0.2 (existing behaviour).
3. **Both present → `drop_zone_intent.md` wins.** Log a precedence note: `config.txt found but drop_zone_intent.md takes precedence — ignoring config.txt`. Never merge silently.
4. Neither present → interactive seed card offered (existing Step 0.2 fallback behaviour).

The rule exists because `drop_zone_intent.md` (written by Layer A after user consent) is the v2 canonical seed for bootstraps that begin in the conversational surface. `config.txt` remains supported for engineer-written or legacy bootstraps. Silently merging the two would create source-of-truth ambiguity — explicit precedence + log keeps provenance clear.

### Step 0.2a — Parse `drop_zone_intent.md` (when present)

**Added in v1.3.2.** Only fires when Step 0.1 detected a `drop_zone_intent.md` in the target folder.

Read the YAML frontmatter via `Read` on the file. Extract the 9 semantic keys + 4 metadata keys. Validate that `schema_version` equals `1` (the v1.3.2 format); if not, log a mismatch warning and fall through to Step 0.2 (`config.txt` parsing) with `drop_zone_intent.md` contents used as supplementary context only.

#### Field mapping (Layer A → Layer B)

| Layer A frontmatter | Layer B Phase 0 field | Transform |
|---|---|---|
| `idea_summary` | Vision (one-paragraph) | Verbatim. User can expand at Step 0.4 edit. If the 1-line synopsis is too short to serve as a paragraph Vision, the gap surfaces as an edit opportunity — Phase 0 does not synthesize a paragraph from Layer A atoms. |
| `nom` (source) | Project name | Direct if `nom` is a real value. If `nom` is null-class (`a trouver ensemble`), Step 0.4 card prompts the user for the name. |
| `nom` (same source, derived) | Project slug | Derive from the resolved Project name per the existing rule (lowercase, spaces → `-`, strip accents, alphanumeric + `-` only, < 50 chars). Slug is null until the name is set. |
| `type` | Is-a-plugin | Inferred: if the `type` value contains the substring `plugin` (case-insensitive), map to `yes`; otherwise `no`. User can edit at Step 0.4. |
| `hints_techniques` | Stack hints | Direct. If null-class, render as `[none]` on the card. |
| `attaches` | Mixed media | Descriptor. Step 0.3 still scans cwd via `Glob` for the source of truth; `attaches` describes what the user saw in their mirror. |

#### Layer-A-specific extras (preserved, not consumed by Phase 0 logic)

The following 4 fields are not consumed by Phase 0 mapping but are **preserved** for Step 0.4 card display (in the `Additional context from drop zone` block) and Step 0.5 write (in the `## Conversational context from drop zone` section):

- `pour_qui` — target audience.
- `langue_detectee` — detected user language (`FR` / `EN` / `mixte`).
- `budget_ou_contrainte` — budget / deadline / constraint mention.
- `prive_ou_public` — private / public / team visibility.

#### Citation preservation (v1.4.1)

**Added in v1.4.1.** `drop_zone_intent.md` frontmatter may carry optional `<field>_source_citation` nested dicts (written by `genesis-drop-zone` v1.4.0+ on the Citations API extraction path). Step 0.2a reads and **preserves** these keys alongside the 9 semantic + 4 metadata keys — the dict-based YAML parser already reads the entire frontmatter; no new parser branching is introduced.

The 9 citation keys that may be preserved (one per semantic field):

- `idea_summary_source_citation`
- `nom_source_citation`
- `type_source_citation`
- `hints_techniques_source_citation`
- `attaches_source_citation`
- `pour_qui_source_citation`
- `langue_detectee_source_citation`
- `budget_ou_contrainte_source_citation`
- `prive_ou_public_source_citation`

Each preserved citation dict has five keys per the v1.4.0 contract: `type` (one of `pdf_page_range`, `text_char_range`), `document_index` (int), `start` (int), `end` (int), `cited_text_preview` (str ≤ 80 chars). Key omission (not explicit `null`) signals absence — a field without citation has no corresponding `_source_citation` key in the frontmatter. Step 0.4 + Step 0.5 render logic inspects each citation key independently per row; the `_source_citation` preservation is read-only passthrough to those render surfaces.

Parser mechanics are **unchanged** — this is a documentation-only note naming which keys are carried forward. Zero Layer A ripple: `genesis-drop-zone` is byte-identical across the v1.4.0 → v1.4.1 boundary.

#### Null-class handling

Null-class strings (`a trouver ensemble`, `non mentionne`, `non mentionnee`, `a affiner — X ou Y`) are preserved verbatim. They signal "user hasn't said yet", not a valid value. Step 0.4 card will prompt for any null-class field that is mandatory downstream (name, vision).

#### Origin tracking

Step 0.4 card tags each field with its origin: `(from drop zone)`, `(from config.txt)`, `(derived)`, `(default)`, `(inferred)`. Tag the 6 mapped fields with `(from drop zone)` or `(inferred)` (Is-a-plugin) as appropriate.

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
Project name           : <value or [missing]> (<origin>)<citation>
Project slug           : <derived or [pending name]><citation>
Vision                 : <value or [missing]> (<origin>)<citation>
Stack hints            : <value or [none]> (<origin>)<citation>
License                : <value or MIT (default)>
Is-a-plugin            : <yes | no | [missing]> (<origin>)<citation>
Plan tier              : <Max | Pro | Team | Free | [missing]>
Scope locks            : <list or [none]>
Mixed media            : <file list or [none]>

Additional context from drop zone:
  Target audience      : <pour_qui value><citation>
  Language detected    : <FR | EN | mixte><citation>
  Budget / constraint  : <value or non mentionne><citation>
  Visibility           : <value or non mentionnee><citation>

Gaps to fill before Phase 1:
  - <gap 1>
  - <gap 2>
  ...

Proceed with these values?  (yes / edit / abort)
```

The `Additional context from drop zone` block renders **only when `drop_zone_intent.md` was the Phase 0 seed source** (v1.3.2+). For legacy `config.txt` bootstraps the block is omitted entirely (no blank section). Origin tags on each field: `(from drop zone)`, `(from config.txt)`, `(derived)`, `(default)`, `(inferred)`.

#### Citation suffix on card rows (v1.4.1)

**Added in v1.4.1.** The `<citation>` placeholder renders an inline `[page N]` / `[pages N-M]` / `[lines X-Y]` suffix when the row's Layer A source field carries a `<source>_source_citation` key in the `drop_zone_intent.md` frontmatter. When no citation is available for the row, `<citation>` expands to the empty string (no leading space, no placeholder text, no `[unknown]`).

Citation-source mapping per row (9 citation-eligible rows — 5 mapped + 4 extras):

| Card row | Citation source key | Propagation |
|---|---|---|
| Project name | `nom_source_citation` | Direct |
| Project slug | `nom_source_citation` | Propagated — slug is derived from `nom` |
| Vision | `idea_summary_source_citation` | Direct |
| Stack hints | `hints_techniques_source_citation` | Direct |
| Is-a-plugin | `type_source_citation` | Propagated — inferred from `type` |
| Target audience | `pour_qui_source_citation` | Direct |
| Language detected | `langue_detectee_source_citation` | Direct |
| Budget / constraint | `budget_ou_contrainte_source_citation` | Direct |
| Visibility | `prive_ou_public_source_citation` | Direct |

Propagated citations honour the principle that a deterministically-derived value (slug from `nom`, Is-a-plugin inferred from `type`) shares provenance with its source field. When the source citation is absent, both the source-derived row and the direct row render without suffix.

**Citation suffix format** reuses verbatim `skills/genesis-drop-zone/phase-0-welcome.md § "Citation annotation format (v1.4.0)"` as the single source of truth across both layers:

- `pdf_page_range` with `start == end` → ` [page N]` (N is 1-indexed page)
- `pdf_page_range` with `start != end` → ` [pages N-M]`
- `text_char_range` → ` [lines X-Y]` (1-indexed, inclusive; line-count via `\n` counting on source text)

Language-neutral ASCII. Identical rendering across FR / EN / mixte locales.

#### Rows explicitly NOT annotated

Six rows on the card carry no Layer A source, and therefore receive no citation suffix even when the seed source was `drop_zone_intent.md`:

- `Target folder` — computed from `Bash pwd`; no Layer A source.
- `License` — defaults to MIT or sourced from `config.txt`; no Layer A source.
- `Plan tier` — prompted at Step 0.4 or sourced from `config.txt`; no Layer A source.
- `Scope locks` — sourced from `config.txt`; no Layer A source.
- `Gaps to fill` — synthesized by Phase 0 logic; no single-source attribution.
- `Mixed media` — sourced from Step 0.3 disk `Glob`, **not** from Layer A's `attaches` frontmatter field. The two sources can legitimately diverge (Victor drops "logo.png" but the actual file on disk is `brand_logo.png`). Rendering `attaches_source_citation` on this row would cite the wrong provenance — claiming the row's value came from the user's drop-zone description when it actually came from disk. Honest stance: `attaches_source_citation` is **preserved by Step 0.2a** (dict parse reads everything) but **not rendered** on this row. Cross-check any rendered card: a grep for `[page N]` on the Mixed media line must return zero matches regardless of whether `attaches_source_citation` exists in the frontmatter.

The user responds with:

- **yes** → persist the intent into `memory/project/bootstrap_intent.md` (a new file — does not exist yet in Phase 0, gets written here) and proceed to Phase 1.
- **edit** → enter a targeted edit flow: the user picks a field, corrects the value, and the card is re-rendered. Loop until the user says yes or abort.
- **abort** → exit the orchestrator cleanly. No write happens outside the target folder. `config.txt` may have been written at Step 0.2 if it was missing — leave it in place as audit trail, do not delete.

**Mode dispatch** (see `SKILL.md § Mode dispatch`): this is a category C consent gate. In `detailed` and `semi-auto` modes the card blocks until the user responds. In `auto` mode the card is rendered as an informational log and the orchestrator proceeds to persist the intent and advance to Phase 1 — the user can still interject `pause` / `abort` / `edit` at any time. If `bootstrap_intent.md` is about to be written without a blocking confirmation (auto mode), the orchestrator logs the full card content immediately before the write so the action is fully auditable after the fact.

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
| Project name | <value><citation> | config.txt / drop_zone_intent.md / user edit |
| Slug | <value><citation> | config.txt / derived |
| Vision | <one-paragraph><citation> | config.txt / drop_zone_intent.md |
| License | <value> | config.txt / default |
| Is-a-plugin | <yes|no><citation> | config.txt / drop_zone_intent.md / user edit |
| Plan tier | <value> | config.txt / user edit |
| Stack hints | <list><citation> | config.txt / drop_zone_intent.md |
| Scope locks | <list> | config.txt / user edit |
| Mixed media | <file list> | folder scan |

## Raw config.txt

<verbatim contents — trimmed if > 5 KB; rendered as `n/a — seeded from drop_zone_intent.md` when the source was Layer A>

## Conversational context from drop zone

(Rendered only when `drop_zone_intent.md` was the Phase 0 seed source.)

| Field | Value |
|---|---|
| Target audience (pour qui) | <value or "a trouver ensemble"><citation> |
| Language detected | <FR / EN / mixte><citation> |
| Budget or constraint | <value or "non mentionne"><citation> |
| Visibility (private / public) | <value or "non mentionnee"><citation> |

Source: `drop_zone_intent.md` written by `genesis-drop-zone` v<version> at <ISO timestamp>.

## Gaps noted at Phase 0

<list of gaps the user acknowledged — each either resolved by a user-provided value or marked "deferred to <phase>">
```

When the seed source was `drop_zone_intent.md`, the `## Raw config.txt` section is retained in the template but rendered as `n/a — seeded from drop_zone_intent.md`. This preserves the file's section structure across both seed paths and makes the seed source explicit to any future reader.

**Citation suffix inside `Value` columns (v1.4.1)**: the `<citation>` placeholder in the `## Fields` and `## Conversational context from drop zone` tables renders the same inline `[page N]` / `[pages N-M]` / `[lines X-Y]` suffix as Step 0.4's card (citation-source mapping + annotation format documented in § "Step 0.4 / Citation suffix on card rows (v1.4.1)" above). When the seed source was `config.txt` (legacy bootstrap, no `drop_zone_intent.md`), no citation suffixes render — the `## Fields` table matches v1.3.2 layout verbatim, and the `## Conversational context from drop zone` section is omitted entirely (no Layer A seed → no section). The `Mixed media` row is deliberately unadorned even when `attaches_source_citation` is preserved, per the honest-provenance rule in § "Rows explicitly NOT annotated".

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
