<!-- SPDX-License-Identifier: MIT -->
---
name: pepite-flagging / pepite-format
description: Canonical file format for pépite entries stored in memory/pepites/. Frontmatter schema with mandatory fields, body section order, slug derivation rule, status transition table, idempotency rule. Mirrors the canonical spec v1_pepite_discovery_flagging.md.
---

# Pépite entry format

Every pépite entry is a single Markdown file at `memory/pepites/YYYY-MM-DD_<slug>.md`. The format mirrors the canonical spec at `.claude/docs/superpowers/specs/v1_pepite_discovery_flagging.md` section "The flag itself".

## File path

```
memory/pepites/<YYYY-MM-DD>_<slug>.md
```

- `<YYYY-MM-DD>` is the **discovery date** in local timezone, not the date of any status transition
- `<slug>` is derived from the frontmatter `name` field: lowercase, ASCII, non-alphanumerics → hyphens, trimmed, max 50 chars

If the target path already exists (rare — same discovery date + same slug), append `-2`, `-3`, etc. **Never overwrite silently**, same rule as the journal and session archive skills. Collisions indicate a duplicate detection and are worth flagging in the surfacing card.

## Frontmatter schema

```yaml
---
name: <short title — becomes the slug>
description: <one-line summary of the pépite, ≤ 120 chars>
type: pepite
discovered_at: YYYY-MM-DD
discovered_in_project: <project-identity — e.g. "project-genesis", "aurum-ai", "cyrano">
discovered_via: <research query, tool call, or source that surfaced it>
leverage: <short sentence explaining why it matters>
relevance:
  origin_project: high | medium | low | na
  transverse: high | medium | low | na
  specific_projects: [list of other project identities it applies to]
status: seed | extracted | actioned | archived | dismissed
criteria_matched: [list of criterion numbers from trigger-criteria.md]
tags: [comma-separated for retrieval]
sources:
  - <url>
  - <url>
---
```

### Field semantics

| Field | Type | Required | Notes |
|---|---|---|---|
| `name` | string | yes | Short title (≤ 60 chars), becomes the slug. Must be filesystem-safe after slugification |
| `description` | string | yes | One-line summary, ≤ 120 chars. Shown in INDEX entries |
| `type` | string | yes | Always `pepite` — the discriminator for the 7th memory type |
| `discovered_at` | date | yes | ISO-8601 YYYY-MM-DD, discovery date in local timezone |
| `discovered_in_project` | string | yes | The project identity where research happened. Not necessarily the same as `relevance.specific_projects` |
| `discovered_via` | string | yes | The research operation: `"WebSearch: duckdb vss"`, `"Agent(Explore): ..."`, `"R8 refresh: claude-code-hooks"`, etc. Provenance |
| `leverage` | string | yes | One sentence naming the specific advantage. "Why it matters" lives in the body; this is the one-liner for scanning |
| `relevance.origin_project` | enum | yes | Applicability to the project where discovered. `na` is valid if the pépite is purely transverse |
| `relevance.transverse` | enum | yes | Applicability to projects generally. `high` means every in-flight project benefits |
| `relevance.specific_projects` | list | yes | Concrete list of project identities it applies to. Empty list is valid if `transverse: high` or `origin_project: high` covers the use |
| `status` | enum | yes | `seed` at creation. Transitions via user decision in the surfacing step |
| `criteria_matched` | list | yes | Numbers 1–6 from `trigger-criteria.md`. Must have ≥ 2 elements unless manually force-flagged by the user |
| `tags` | list | yes | Retrieval tags. At least one tag — common examples: `emerging-tech`, `cross-project`, `tooling`, `pattern`, `research-correction` |
| `sources` | list | yes | URLs or local paths that surfaced the pépite. At least one source — unsourced pépites are not pépites, they are hunches |

### Fields deliberately NOT in the schema

- **priority** — pépites are not ranked at creation time. Prioritisation happens at extraction time, when the user decides to act on one
- **effort_estimate** — not meaningful at detection time; requires context the user has, not Claude
- **ttl** — seeds do not expire. A seed from last month is still a seed
- **related_pepites** — cross-pépite synthesis is a v2 target. Manual INDEX review is the v1 primitive
- **author** — always Claude + the user together. Redundant field

## Body template

```markdown
# <Pépite title>

## What it is

<1–3 paragraphs capturing the essence of the finding. Concrete — name the tool, the pattern, the library, the rule. Include one primary source URL inline. This section is what a reader sees first; make it self-contained enough to evaluate without clicking through.>

## Why it matters

<Pain it solves, opportunity it unlocks, or asymmetric leverage it provides. Tie directly to the `criteria_matched` list — if criteria 3 and 5 matched, this section should explicitly say "emerging tech with strong signal" and "saves N minutes per recurring task". The reader should be able to reconstruct the flagging decision from this paragraph.>

## Who should know

<Which in-flight projects would benefit and why. For each project in `relevance.specific_projects`, one sentence explaining the match. This section informs the cross-project routing step if the user approves propagation.>

## Extraction plan

<Concrete next action candidates. Not a decision — a short menu of ways the pépite could be extracted. Examples:
- "Add to the `genesis-protocol/templates/` as an optional Phase 6 addition"
- "Prototype in a throwaway branch of `cyrano` to validate before deciding"
- "Pin as a watch-item for the 2026-Q3 review"
- "Convert directly into a skill under `skills/<name>/`"

Each candidate has a rough effort estimate. The user picks one (or none) during the surfacing card.>

## Status history

- YYYY-MM-DD — discovered, marked `seed`. Criteria matched: <list>. Source: <primary>.
- YYYY-MM-DD — surfaced to user in response to <research operation>. User said: "<verbatim if given>". Status: <new status>.
- YYYY-MM-DD — (further transitions if any)
```

## Status transition table

Status moves forward only, with one reversal path (`archived → seed` on rediscovery). Every transition adds a new line to the "Status history" section — transitions are append-only.

| From | To | Trigger | Notes |
|---|---|---|---|
| *(none)* | `seed` | Detection step creates entry | Initial state |
| `seed` | `extracted` | User says "extract now" (option a) | Content pulled into a spec, plan, or implementation target |
| `seed` | `seed` | User says "keep as seed" (option b) | No-op status-wise but adds a history line |
| `seed` | `actioned` | User says "propagate" (option c) and at least one pointer written | Cross-project routing happened |
| `seed` | `dismissed` | User says "dismiss" (option d) | Entry stays on disk for audit |
| `seed` | `archived` | Manual status change after long dormancy | User decided the entry is no longer current but wants to keep it referenceable |
| `extracted` | `actioned` | Extraction has produced concrete work (PR, skill, commit) | Second forward transition — extraction → action |
| `actioned` | `archived` | The work has shipped and the entry's job is done | Terminal-ish state |
| `archived` | `seed` | Rediscovery — user says "this is still relevant" | Only allowed reversal |
| `dismissed` | *(terminal)* | — | Dismissed pépites never transition. They stay for audit |

**Why no delete path**: audit trail. Dismissed and archived entries are cheap to keep and valuable as provenance. If the user wants to delete an entry, they use `rm` manually — the skill does not expose a delete operation.

## Slug derivation

Apply the same rule as `journal-system/entry-format.md`:

1. Take the `name` field
2. Normalise Unicode (NFKD)
3. Strip to ASCII (ignore non-ASCII combining marks)
4. Lowercase
5. Replace non-alphanumeric runs with a single `-`
6. Trim leading and trailing `-`
7. Truncate to 50 chars (break at word boundary if possible)
8. If empty or pure numeric, fall back to `pepite-<8-hex-chars>`

Example: `name: "DuckDB + VSS extension for embedded vector search"` → `duckdb-vss-extension-for-embedded-vector-search`.

## Idempotency rules

- **Re-detection on the same finding in a later session**: if a pépite with the same `name` slug already exists, do NOT create a new entry. Instead, append a "Status history" line to the existing entry noting the re-detection and the new source. This prevents duplicate seeds cluttering the INDEX
- **Same-day same-slug collision**: append `-2`, `-3`, etc. to the filename. This is rare but possible if two distinct findings happen to produce the same slug — never overwrite
- **Status transition on an already-terminal entry**: no-op with a warning. A `dismissed` entry cannot become `actioned` without first going back to `seed` via explicit manual edit

## SPDX header

Every pépite entry starts with:

```markdown
<!-- SPDX-License-Identifier: MIT -->
```

Before the frontmatter block. Consistent with all other Genesis memory types per R10.

## Example entry (illustrative)

```markdown
<!-- SPDX-License-Identifier: MIT -->
---
name: DuckDB + VSS for embedded analytics
description: DuckDB's VSS extension (stable March 2026) gives embedded vector-similarity search with zero ops, likely the best embedded analytics stack for new projects in 6 months
type: pepite
discovered_at: 2026-04-15
discovered_in_project: project-genesis
discovered_via: "R8 refresh: embedded-analytics-stack-2026"
leverage: "Embedded (no separate service), stable VSS extension, best-at-date ceiling in 6 months — one install per project unlocks vector search without Postgres+pgvector ops"
relevance:
  origin_project: medium
  transverse: high
  specific_projects: [aurum-ai, cyrano, myconciergerie-prog]
status: seed
criteria_matched: [2, 3, 6]
tags: [emerging-tech, embedded-db, vector-search, highest-potential]
sources:
  - https://duckdb.org/docs/extensions/vss
  - https://github.com/duckdb/duckdb-vss
---

# DuckDB + VSS for embedded analytics

## What it is

DuckDB is an in-process analytical database — like SQLite but columnar and optimised for OLAP queries. The VSS (vector similarity search) extension, released as stable in March 2026, adds HNSW-indexed vector search to DuckDB tables. Result: a single-file embedded database with SQL, columnar analytics, and vector search, all in one dependency.

## Why it matters

Three of the six pépite criteria match:

- **Criterion 2 (leverage)**: one install per project, ongoing benefit across every query. No separate Postgres process, no pgvector setup, no connection pooling
- **Criterion 3 (emerging)**: stable release was March 2026; the mainstream has not caught up yet. Early adoption positions projects to be reference implementations
- **Criterion 6 (highest potential)**: best-at-date-today for most projects is still Postgres + pgvector, but DuckDB+VSS's embedded-first posture is the better fit for projects that don't need multi-writer concurrency

## Who should know

- **aurum-ai**: wealth-app needs user-scoped semantic search over notes. Embedded fits the single-user-per-process model
- **cyrano**: local-first CLI with no DB dependency target. DuckDB is a perfect fit
- **myconciergerie-prog**: fleet of per-property databases. Embedded + single-file simplifies the per-property deployment

## Extraction plan

- **Option A**: add to `genesis-protocol/templates/` as an optional Phase 6 bonus block for projects that need embedded analytics. Low effort (< 2 hours), high benefit on new projects only
- **Option B**: prototype in a cyrano throwaway branch first to validate the developer experience and performance on a real query shape. Medium effort (1 day)
- **Option C**: pin as a watch-item for 2026-Q3 review. Zero effort now, re-evaluate in July

## Status history

- 2026-04-15 — discovered, marked `seed`. Criteria matched: 2, 3, 6. Source: https://duckdb.org/docs/extensions/vss
```

Note: this example is **illustrative only** for the format. It is not a real pépite detected in this session — no real pépite was detected in the v0.7.0 session yet. The skill ships without any pre-seeded pépite entries; the first real entry will be created during normal research operations in v0.7.0+ sessions.

## What this file does NOT define

- **The detection criteria** — those live in `trigger-criteria.md`
- **The cross-project routing mechanism** — lives in `cross-project-routing.md`
- **The INDEX.md format** — the INDEX is seeded by `install-manifest.yaml` and maintained by the skill's flow
- **The slash command interface** — deferred to v2
- **Validation / linting** — deferred. The user reviews entries manually; automated validation is a v2 candidate if the entry volume justifies it
