<!-- SPDX-License-Identifier: MIT -->
---
name: Pépite discovery flagging — red-light surfacing of high-leverage findings
description: When research reveals a non-obviously valuable finding (gold nugget, emerging tech, pattern with high leverage), raise a red-light flag that triggers explicit surfacing to the user, with routing metadata so cross-project propagation happens without human intervention
type: spec
target_version: v1
created_at: 2026-04-15
originSessionId: project-genesis v1 bootstrap
status: active
---

# Pépite discovery flagging system

## Problem

During research sessions, Claude frequently surfaces findings that fall into one of these categories:

- **Pépite** (gold nugget) — a non-obviously valuable discovery, often surprising, that would save future work or unlock a new capability
- **Tech en devenir** (emerging tech) — a tool, pattern, or library in early maturity that is likely to become important in 3–12 months
- **Cross-reference opportunity** — a pattern discovered in Project A that happens to solve an unresolved problem in Project B

Without a formal surfacing mechanism:

- Pépites get buried in the research report alongside ordinary findings and the user may skim past them
- Emerging tech observations are lost after the session ends unless the user happens to ask about them again
- Cross-reference opportunities are never followed through because the researcher forgets which other projects would benefit

The user articulated this problem on 2026-04-15 during the Genesis bootstrap session:

> "il faut aussi probablement [...] ajouter une fonctionnalité lorsque l'on découvre une pépite ou une tech en devenir de mettre un red light et de faire remonter pour extraire la quintessence de l'idée. Ce serait valable de manière générale (ou transverse) ou spécifique à un projet d'où la recherche est lancée."

## Design — red light flag + routing metadata

### The flag itself

During any research operation (WebSearch, WebFetch, sub-agent research, reading external docs), Claude watches for findings matching the red-light criteria (below). When a finding qualifies, Claude creates a **pépite entry** with routing metadata and surfaces it at the next natural conversation boundary.

A pépite entry is a file in `memory/pepites/` (new 7th memory directory, alongside `journal/`). Format:

```yaml
---
name: <short title>
description: <one-line summary of the pépite>
type: pepite
discovered_at: YYYY-MM-DD
discovered_in_project: <project-identity>
discovered_via: <research query or source that surfaced it>
leverage: <short sentence explaining why it matters>
relevance:
  origin_project: high | medium | low | na
  transverse: high | medium | low | na
  specific_projects: [list of other project identities it applies to]
status: seed | extracted | actioned | archived | dismissed
tags: [comma-separated for retrieval]
sources:
  - <url>
---

# <Pépite title>

## What it is

<1–3 paragraphs capturing the essence>

## Why it matters

<Pain it solves, opportunity it unlocks, or asymmetric leverage it provides>

## Who should know

<Which in-flight projects would benefit and why>

## Extraction plan

<Concrete next action: e.g. "add to Aurum's Phase 5 options", "prototype in a throwaway branch", "defer to post-v1", "pin as watch-item for 2026-Q3 review">

## Status history

- YYYY-MM-DD — discovered, marked seed
- YYYY-MM-DD — presented to user, user said X
- YYYY-MM-DD — extracted to <destination> / actioned / archived / dismissed
```

### Red-light trigger criteria

Not every finding is a pépite. The bar is high on purpose — noise kills the signal. Claude raises the red light when **at least two** of the following conditions are true:

1. The finding contradicts a previous assumption or past research cache entry
2. The finding has asymmetric leverage — one-time setup unlocks ongoing compound value
3. The finding is emerging / early-adopter — not yet in mainstream adoption but strongly signaled by multiple independent sources
4. The finding cross-cuts projects — solves a known open question in a different in-flight project
5. The finding saves ≥ 5 minutes per recurring use case OR eliminates a recurring pain point
6. The finding has "most-potential" framing in best-practice-at-date analysis (not necessarily best today, but likely best in 3–12 months)

If only one criterion is met, the finding goes into the normal R8 research cache — not flagged as a pépite. Two or more criteria → red light raised.

### Surfacing protocol

When a red light is raised during research, Claude does **not** interrupt the current operation. Instead:

1. Silently creates the pépite entry in `memory/pepites/<date>_<slug>.md` with `status: seed`
2. At the **next natural conversation boundary** (end of current tool batch, or when presenting research synthesis), adds a short **🔴 Pépite flag** section to the response:

```
🔴 Pépite detected during this research — <title>

Why: <one line>
Relevance: origin=<X>, transverse=<Y>, also relevant to=<list>
Full entry: memory/pepites/<file>.md

What to do: (a) extract now, (b) keep as seed for later, (c) propagate to other projects, (d) dismiss
```

3. User responds with one of (a)(b)(c)(d). Claude updates the entry's status and takes the requested action.

### Consent model — mirrors journal amplification rule

Analogous to the journal amplification pattern in Layer 0:

- **Automatic flag creation** is allowed (low-friction cost, just a file write)
- **Surfacing to user** is always explicit ("I detected a pépite — what do you want to do with it?")
- **Propagation to other projects** requires explicit user yes — never auto-writes to another project's memory
- **Extraction** (turning the pépite into an actionable spec or implementation plan) requires explicit yes
- **Dismissal** is a valid outcome — not every detected pépite needs to become work

The user is always the final filter. Claude's job is to **detect and surface** — not to decide.

## Cross-project propagation logic

When a pépite is marked `relevance.transverse: high` or has `specific_projects` listed, and the user approves propagation, Claude writes **pointer files** into each target project's auto-memory:

```
~/.claude/projects/<target-project-slug>/memory/pepite_<date>_<slug>.md
```

The pointer file is short (< 20 lines) and contains:

```yaml
---
name: Pépite pointer — <title>
description: <one line>
type: reference
created_at: YYYY-MM-DD
canonical_location: <absolute path to the canonical entry>
pepite_status_at_pointer_creation: <status>
---

This is a pointer to a pépite discovered while working on <origin-project> on <date>.

The full entry lives at: <canonical path>

Why this project should care: <one-line relevance reason>

If you (the AI reading this in a future session) want the full context, read the canonical entry.
```

When the target project's next session opens and reads `MEMORY.md`, the pointer is visible and the session knows the pépite exists and where to look for details. Zero duplication, minimal friction, full discoverability.

## Integration with the Meta-Memory architecture

This feature is the **first operational component** of Meta-Memory Layer 3 (cross-project knowledge routing) that can ship before the full Path B Meta-Memory session happens.

- Layer 0 universal holds the pépite routing **rule** (added to `~/.claude/CLAUDE.md` as a feedback entry)
- Genesis v1 template ships the pépite **skill** (`skills/pepite-flagging/`) that implements the trigger detection, entry creation, surfacing, and propagation
- Per-project `memory/pepites/` directories hold the local entries and pointer files
- The future Meta-Memory Path B session will unify these into a graph view with `/pepite timeline`, `/pepite status`, `/pepite propagate`, etc.

## v1 deliverables

The Genesis v1 plugin ships with:

- `skills/pepite-flagging/` skill containing:
  - Red-light detection logic (the 6 criteria, "two or more" rule)
  - Pépite entry generator (frontmatter + body templates)
  - Surfacing prompt generator (the 🔴 card format)
  - Cross-project pointer writer
  - Status transition handlers (seed → extracted / actioned / archived / dismissed)
- `memory/pepites/` directory created in every Genesis-bootstrapped project
- `memory/pepites/INDEX.md` — chronological index, same pattern as `journal/INDEX.md`
- Documentation in `README.md` explaining the feature to users
- Reference in `v1_rules.md` under a new R11 — "Pépite discovery discipline"

## v2 deliverables (deferred)

- `/pepite` slash commands for manual flagging / review / status transitions
- Auto-propagation to all in-flight projects that match `specific_projects` without per-target confirmation (when the user has built trust in the system)
- Pépite TTL — entries that sit in `seed` status for > 90 days auto-archive
- Cross-pépite synthesis — pattern detection when multiple pépites cluster on the same topic

## Self-rating

- Pain-driven: 10/10 (user explicitly asked for this exact feature)
- Prose cleanliness: 7/10 (comprehensive, could be tighter)
- Best-at-date: 9/10 (novel design, no prior art directly equivalent, inspired by Zettelkasten routing)
- Self-contained: 9/10 (references Meta-Memory architecture but stands alone)
- Anti-Frankenstein: 9/10 (v1 deliverables tightly scoped, v2 deferred appropriately)
- Average: **8.8/10**
