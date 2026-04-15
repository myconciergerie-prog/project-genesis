<!-- SPDX-License-Identifier: MIT -->
---
name: pepite-flagging / cross-project-routing
description: Pointer file mechanism for propagating pépite discoveries to sibling projects on the same machine. Each propagation requires explicit per-target user consent. Pointer files are short (< 30 lines), reference the canonical entry by absolute path, and live in the target project's auto-memory directory so they load at the target's next session open. Cold-read protocol for consumers. Zero duplication, full discoverability.
---

# Cross-project routing

When a pépite's `relevance.specific_projects` field lists other in-flight projects, the user may choose option **(c) propagate** during the surfacing card. This file describes how propagation works — how Claude finds the target projects, what the pointer file looks like, how the target project's next session discovers the pointer, and how consent is bounded per invocation.

This mechanism is the **first operational component of Meta-Memory Layer 3** (cross-project knowledge routing). It ships before the full Path B Meta-Memory session happens, as a minimum viable primitive. See the canonical spec `.claude/docs/superpowers/specs/v1_pepite_discovery_flagging.md` section "Cross-project propagation logic" and the Layer 0 rule "Cross-project research sharing — avoid redundant discoveries".

## The consent model — per target, never batched

Propagation is **always** gated on explicit user consent, and the consent is **per target project**. When the user says "propagate" (option c) during the surfacing card, Claude does NOT immediately write pointers to every project in `relevance.specific_projects`. Instead, it iterates:

```
For each target in relevance.specific_projects:
  Ask the user: "Write pointer for pépite '<title>' to <target>? (y/n)"
  If yes: write the pointer file, log the write in the pépite's status history
  If no or silence: skip, do not write, log the skip in the status history
```

Silence is **always** a skip, never an implicit yes. If the user wants to approve all in bulk, they say so explicitly ("propagate to all"). Even then, Claude echoes the target list one last time and waits for confirmation before writing.

**Why per-target consent**: the user runs ~20 projects. Some are active (in current development), some are dormant (on hold), some are archived (frozen). A pépite that fits three active projects may also technically apply to two archived ones — but propagating to archived projects adds noise at their next wake-up. Per-target consent lets the user exclude dormant/archived targets without editing the pépite's metadata.

## Target project discovery

When the user approves propagation to target `<project-name>`, Claude needs to find:

1. The target project's **auto-memory directory** at `~/.claude/projects/<target-slug>/`
2. Optionally, the target project's **repo directory** at `C:\Dev\Claude_cowork\<target-name>\` or `C:\Dev\AntiGravity\<target-name>\`

### Auto-memory directory — primary target

The Claude Code auto-memory directory lives under `~/.claude/projects/<slug>/` where `<slug>` is the URL-encoded absolute cwd path. The slug rule (per the 2026-04-15 research entry, corrected in v0.6.0) replaces `\`, `/`, `:`, `_`, and space with `-`.

For a target project at `C:\Dev\Claude_cowork\aurum-ai`, the slug is `C--Dev-Claude-cowork-aurum-ai` and the target auto-memory directory is `~/.claude/projects/C--Dev-Claude-cowork-aurum-ai/memory/`.

Pointer files are written to `~/.claude/projects/<target-slug>/memory/pepite_<date>_<slug>.md`. The `pepite_` prefix distinguishes pointers from the target project's native memory files.

**Why auto-memory not repo memory**: the target project's repo may be frozen, archived, or on a different branch. Writing to the repo would require a worktree, a commit, and a PR — far too much friction for a pointer. The auto-memory directory is per-machine state, not committed, and loads at the target's next session open without any git operation. The pointer becomes visible to the target's next Claude Code session without touching git.

### Repo directory — deferred to v2

Writing a pointer to the target's repo memory (`<repo>/memory/references/pepite_<slug>.md`) would make the pointer version-controlled and visible to any collaborator on the target repo. This is a v2 target. In v1, pointers live in auto-memory only, which means they are per-machine. Multi-machine users may want a v2 option.

### Project slug lookup — current known machine state

The pépite skill needs a known mapping of project names to slugs. In v1 this is **hard-coded** in `SKILL.md` (or referenced there) — the Genesis user has ~20 projects, the mapping is small, and it changes slowly. When a new project is added to the machine, the user manually updates the mapping.

The v1 machine map for the Genesis user:

| Project name | Physical path | Slug |
|---|---|---|
| project-genesis | `C:\Dev\Claude_cowork\project-genesis` | `C--Dev-Claude-cowork-project-genesis` |
| aurum-ai | `C:\Dev\Claude_cowork\aurum-ai` | `C--Dev-Claude-cowork-aurum-ai` |
| cyrano | `C:\Dev\Claude_cowork\cyrano` or `C:\Dev\AntiGravity\cyrano-by-antigravity` | `C--Dev-Claude-cowork-cyrano` or `C--Dev-AntiGravity-cyrano-by-antigravity` |
| myconciergerie-prog | `C:\Dev\AntiGravity\Myconciergerie` | `C--Dev-AntiGravity-Myconciergerie` (pre-v0.6 slug rule — verify before writing) |

The v2 improvement is auto-discovery: walk `~/.claude/projects/*/` and `C:\Dev\Claude_cowork\*\` + `C:\Dev\AntiGravity\*\`, match slugs to projects, build the map on the fly. Deferred because the hard-coded map covers v1 use and automation can wait.

**Before writing**: always verify the target slug directory exists. If it does not (typo in the pépite metadata, or the target project has never been opened in Claude Code), surface a YELLOW warning and ask the user whether to create the directory (probably no) or abort the write for that target.

## Pointer file template

The pointer file is short (< 30 lines). Every pointer contains:

- Canonical path to the full pépite entry
- One-line summary
- Why this specific project should care
- The pépite's status at pointer-creation time
- Date the pointer was written

Template:

```markdown
<!-- SPDX-License-Identifier: MIT -->
---
name: Pépite pointer — <pépite title>
description: <one-line summary from the canonical entry>
type: reference
created_at: YYYY-MM-DD
canonical_location: <absolute path to the canonical pépite entry>
pepite_status_at_pointer_creation: seed | extracted | actioned | archived
source_project: <the project where the pépite was discovered>
relevance_to_this_project: <one-line reason this specific target project should care>
---

# Pépite pointer — <pépite title>

This is a pointer to a pépite discovered while working on `<source-project>` on `<YYYY-MM-DD>`.

**Canonical entry**: `<absolute path>`

## Why this project should care

<1–2 sentences tying the pépite to a specific unresolved question, pain point, or decision pending in THIS target project. Must be concrete — not "generally useful". The writer of the pointer must know enough about the target project to justify the write.>

## Full context

For the three framings, the sources, the extraction plan, and the status history, read the canonical entry above. This pointer intentionally does not duplicate — duplication drifts.

## If you (future AI session) want to act on this

Ask the user: *"There is a pépite pointer relevant to this project — `<title>`. Do you want to open the canonical entry and consider extracting it?"* If the user says yes, read the canonical, review the extraction plan, and propose a concrete action scoped to this project.

## Status of the source pépite at pointer creation

**`<status>`** — <one sentence on what status means in the transition table>

If you follow the canonical link and the status has changed since pointer creation, trust the canonical. The pointer is a snapshot; the canonical is current.
```

### Why the pointer is so explicit

Reading a pointer cold (no session memory of the original research) must give enough context to decide whether to click through. The pointer's job is **not** to re-explain the pépite — that would be duplication and it would drift. The pointer's job is to say: "there is something relevant to this project, here is where it lives, here is specifically why you should care". A lazy pointer ("see memory/pepites/foo.md on project-genesis") does not get read; a concrete pointer ("this solves the auth-token-rotation question we deferred in Cyrano v0 Phase 3") gets read.

## Cold-read protocol — for pointer consumers

When a target project's Claude Code session opens and reads its auto-memory, it sees the pointer file. The consumer protocol:

1. **At session open**, as part of R1.1, scan `~/.claude/projects/<current-slug>/memory/pepite_*.md` for any pointer files
2. For each pointer found, read the `canonical_location` and the `pepite_status_at_pointer_creation` fields
3. If the canonical still exists and has not been dismissed since pointer creation, surface a one-line note in the session's early context: *"Pépite pointer from `<source-project>`: `<title>`. Relevant because `<relevance_to_this_project>`. Full context at `<canonical>`."*
4. Do NOT auto-open the canonical. Wait for the user to ask.
5. If the user asks about the pointer, open the canonical and walk through the extraction plan.

The consumer protocol is **opt-in by the target project**. Genesis-bootstrapped projects inherit this protocol via the `pepite-flagging` skill install; non-Genesis projects may or may not pick it up. In v1, only Genesis projects consume pointers reliably. This is fine — the user runs predominantly Genesis-bootstrapped projects going forward.

## Pointer filename convention

```
pepite_YYYY-MM-DD_<slug>.md
```

Same date and slug as the canonical entry. The `pepite_` prefix distinguishes pointers from the target project's own files in the auto-memory directory. One pointer per canonical per target — never duplicate.

**Collisions**: if the same canonical has already been propagated to the same target, the pointer already exists. Do NOT overwrite. Instead, update the `pepite_status_at_pointer_creation` field in-place to reflect the current canonical status, and add a one-line append to the pointer noting the re-propagation date. This is the only case where in-place edit is allowed on a pointer.

## Status history sync

Every successful pointer write adds a line to the **canonical pépite's** "Status history" section:

```
- 2026-04-15 — propagated to aurum-ai via pointer at ~/.claude/projects/C--Dev-Claude-cowork-aurum-ai/memory/pepite_2026-04-15_<slug>.md
```

This way the canonical entry always knows which targets have seen it. If the user later asks "where has this pépite been propagated?", reading the canonical's Status history answers the question without needing a separate index.

## When propagation is NOT appropriate

- **Scope lock** — if the target project is under a scope lock (e.g. `aurum-frozen-scope-lock.md`), propagation is still allowed because a pointer file is additive auto-memory, not a code or commit change. Pointer writes never touch the target repo. But Claude should surface the lock in the per-target consent prompt so the user can decide whether the pépite warrants breaking the lock's spirit
- **Dormant target** — projects that have not been opened in Claude Code for > 90 days are dormant. Pointer writes to dormant targets are wasted until the target wakes up. Claude should surface dormancy in the consent prompt as a soft YELLOW warning, not a hard block
- **Unknown target slug** — the target's slug directory does not exist under `~/.claude/projects/`. Either the target has never been opened in Claude Code, or the slug rule differs. Abort the write for that target and log the skip in the canonical status history

## Consent examples

### Good — explicit per-target

```
Claude: Pépite detected — "DuckDB + VSS for embedded analytics".
         Relevance: origin=medium, transverse=high, also relevant to [aurum-ai, cyrano, myconciergerie-prog].
         Your call: (a) extract now (b) keep as seed (c) propagate (d) dismiss

User:    c

Claude: Propagating. Write pointer to aurum-ai? (y/n)
User:    y
Claude:  ✓ Pointer written to ~/.claude/projects/C--Dev-Claude-cowork-aurum-ai/memory/pepite_2026-04-15_duckdb-vss-...md

Claude:  Write pointer to cyrano? (y/n)
User:    y
Claude:  ✓ Pointer written to ~/.claude/projects/C--Dev-Claude-cowork-cyrano/memory/pepite_2026-04-15_duckdb-vss-...md

Claude:  Write pointer to myconciergerie-prog? (y/n)
User:    skip
Claude:  Skipped. Status history updated: "2026-04-15 — propagation to myconciergerie-prog skipped by user"
```

### Good — user batches with explicit all

```
Claude: Pépite detected — "DuckDB + VSS...". Propagation targets: [aurum-ai, cyrano, myconciergerie-prog]
User:    propage à tout

Claude:  Confirming: write pointers to aurum-ai, cyrano, and myconciergerie-prog? (y/n)
User:    y
Claude:  Writing 3 pointers...
         ✓ aurum-ai
         ✓ cyrano
         ✗ myconciergerie-prog — slug directory not found, skipped
         Status history updated with 2 writes and 1 skip.
```

### Bad — never auto-propagate without explicit consent

```
User:    c
Claude:  Writing pointers to all 3 targets automatically based on relevance.specific_projects...  ← WRONG
```

Even option (c) does not authorise batch writes. Consent must be explicit per target or via a user-initiated explicit all.

## v2 candidates (deferred)

- **Auto-discovery of sibling projects** via filesystem walk instead of hard-coded map
- **Multi-machine propagation** via a shared sync directory or a Git-backed central pépite index
- **Consent cascade** — "approve all future propagations for this pépite without asking each time" opt-in per pépite
- **Pointer linting** — ensure pointers are readable cold, flag pointers with vague `relevance_to_this_project`
- **Pointer TTL** — pointers that sit unread in target auto-memory for > 180 days get auto-archived

All deferred because v1 is explicitly about the minimum viable primitive. Expansion is scope creep until the v1 shape has been used enough to reveal which friction points matter.
