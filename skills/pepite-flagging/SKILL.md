<!-- SPDX-License-Identifier: MIT -->
---
name: pepite-flagging
description: Watch for high-leverage discoveries during research operations (WebSearch, WebFetch, sub-agent exploration, reading external docs) and raise a red-light flag when at least two of the six trigger criteria are met. Create a pépite entry in `memory/pepites/`, surface a 🔴 card at the next natural boundary, wait for user choice (extract / seed / propagate / dismiss), and write pointer files to sibling projects only on explicit consent. Manual-invoke fallback: `/pepite-flag "<title>"` forces an entry when Claude missed the auto-detection.
---

# Pépite flagging

Gold-nugget discovery surfacing for Project Genesis and downstream projects. This skill is a **1:1 mirror of the canonical spec** at `.claude/docs/superpowers/specs/v1_pepite_discovery_flagging.md`. If the spec changes, this skill must be updated to match — never the other way around.

**Canonical reference**: `.claude/docs/superpowers/specs/v1_pepite_discovery_flagging.md` (2026-04-15, status: active).

## Why this skill exists

During any research operation — WebSearch, WebFetch, sub-agent exploration, reading external docs, even R8 cache refreshes — Claude frequently surfaces findings that are disproportionately valuable compared to the surrounding noise: a tool that solves a long-standing pain, a pattern that cross-cuts projects, a piece of emerging tech that will be standard in 6 months. Without a formal surfacing mechanism, these pépites get buried in the research report and the user skims past them.

The skill adds three things:

1. **A detection bar** — the six red-light criteria (`trigger-criteria.md`), with a "two or more" rule. Anything below the bar goes into the normal R8 cache. Anything above it becomes a pépite entry.
2. **A structured entry format** — `memory/pepites/YYYY-MM-DD_<slug>.md` with routing metadata (relevance.origin, relevance.transverse, specific_projects) so the entry is both searchable and propagable.
3. **A surfacing ritual** — the 🔴 Pépite card presented at the next natural conversation boundary, with four choices: extract now, keep as seed, propagate to other projects, dismiss. User is always the final filter.

The skill is speech-native and consent-bounded, mirroring the `journal-system` pattern: Claude detects and surfaces, the user decides and approves propagation.

## When to invoke

### Automatic (the primary mode)

During any research operation Claude runs, the skill's **trigger-criteria watcher** is always on. When Claude notices a finding that matches **at least two** of the six red-light criteria in `trigger-criteria.md`, it:

1. Silently creates the entry in `memory/pepites/<date>_<slug>.md` with `status: seed`
2. Does **not** interrupt the current tool batch
3. At the next natural boundary (end of tool batch, research synthesis, or turn close), surfaces the 🔴 card

"Research operation" means any of:

- `WebSearch` / `WebFetch` calls
- `Agent` sub-agent calls whose purpose is research / exploration
- Reading external documentation or GitHub repos
- Refreshing an R8 cache entry (the refresh itself may reveal a pépite)

Routine file reads for implementation work are **not** research operations — the skill does not watch those.

### Manual trigger phrases

The user may also invoke the skill directly at any time:

| Phrase | Action |
|---|---|
| **"Flag ceci comme pépite"** / "flag as pépite" / "this is a pépite" | Force-create an entry for the most recent finding. Use when Claude missed the auto-detection. |
| **"Tu as vu une pépite ?"** / "did you spot a pépite?" | Scan the current research session and list any findings that would qualify under the criteria but were not flagged yet. Claude explains why/why not. |
| **"Reprends la pépite sur X"** / "continue the pépite on X" | Load an existing entry, summarize current status, offer to change status (extract / actioned / archive / dismiss). |
| **"Propage la pépite sur X"** / "propagate X" | Write pointer files to the other projects listed in `relevance.specific_projects`. Requires explicit user confirmation per target project. |
| **"Dismiss la pépite sur X"** / "dismiss X" | Set `status: dismissed`. Entry stays on disk for audit trail but is skipped in future surfacing. |

## The flow — five steps

### Step 1 — Detect (automatic, during research)

While running any research operation, Claude evaluates each candidate finding against the six red-light criteria from `trigger-criteria.md`. **Two or more** criteria → raise the flag. **One** criterion → skip (goes into normal R8 cache instead).

The evaluation is a judgement call. The criteria are not a checklist to mechanically tick — they are shaped to give Claude permission to raise the flag when the finding "feels" meaningful. If in doubt, err toward creating the entry: a dismissed seed costs almost nothing, a missed pépite is compound pain.

### Step 2 — Create the entry silently

Write a new file at `memory/pepites/YYYY-MM-DD_<slug>.md` using the template from `pepite-format.md`. Frontmatter fields are mandatory (name, description, type, discovered_at, discovered_in_project, discovered_via, leverage, relevance, status, tags, sources). Body sections are mandatory (What it is, Why it matters, Who should know, Extraction plan, Status history).

The entry is created with `status: seed`. No user consent is needed for the file write itself — it is low-friction and auditable. **Only surfacing and propagation require consent** (Step 3 and Step 4).

### Step 3 — Surface at the next natural boundary

At the end of the current tool batch or at research synthesis time, emit a short 🔴 Pépite card in the response:

```
🔴 Pépite detected during this research — <title>

Why: <one-line reason>
Relevance: origin=<X>, transverse=<Y>, also relevant to=<list of projects or "n/a">
Criteria matched: <which of the 6 criteria triggered>
Full entry: memory/pepites/<file>.md

What to do:
  (a) extract now — pull the content into a spec or implementation plan
  (b) keep as seed — leave for later review
  (c) propagate to other projects — write pointer files to sibling projects
  (d) dismiss — mark resolved, keep on disk for audit
```

Never auto-choose on behalf of the user. Wait for the response. If the user is silent across multiple turns, the entry stays at `status: seed` by default — silence is not consent to any of (a) (c) (d), but it is permission for (b).

### Step 4 — Act on the user's choice

Depending on the response:

- **(a) extract** → Ask the user where the extraction should go (new spec? existing plan? implementation task?). Write the content to the target location, update the entry's status to `extracted`, add a line to the "Status history" section with the date and the destination. Do not dismiss the original entry — it remains as the provenance record.
- **(b) seed** → Leave `status: seed`. Add a "Status history" line noting the user chose to keep as seed. No further action.
- **(c) propagate** → Follow `cross-project-routing.md`: for each project in `relevance.specific_projects`, ask for explicit per-target confirmation before writing a pointer file. Default **no** — silence or ambiguity means skip. Update status to `actioned` once at least one pointer is written.
- **(d) dismiss** → Set `status: dismissed`, add a "Status history" line with the dismissal reason if the user gave one. Entry stays on disk.

### Step 5 — Update the INDEX

`memory/pepites/INDEX.md` already exists with the red-light criteria, entry states, and surfacing protocol baked in (from the Genesis bootstrap). After any status change, append or update the entry line under the "## Entries" section. Never duplicate entries — always update in place.

## Files in this skill

| File | Purpose |
|---|---|
| `SKILL.md` | This entry point — trigger phrases, auto-detection mode, five-step flow, 1:1 mirror reference |
| `trigger-criteria.md` | The six red-light criteria with "two or more" rule, rationale per criterion, calibration examples, anti-noise guards |
| `pepite-format.md` | Frontmatter schema and body template. Mirrors the canonical spec. Slug derivation rule. Status transition table. |
| `cross-project-routing.md` | Pointer file template, per-target consent pattern, target project discovery (how to find sibling project memory dirs), cold-read protocol for pointer consumers |
| `install-manifest.yaml` | Idempotent creation of `memory/pepites/` + `INDEX.md` stub with create_if_missing_only guard, three verification checks |
| `verification.md` | Two-mode health card (post-install + post-action) with halt-on-RED on any missing required field or consent-bypass attempt |

## Hard rules

1. **Never auto-propagate to another project.** Cross-project pointer writes require explicit per-target user yes. Silence is not consent.
2. **Never surface without creating the entry first.** The file on disk is the source of truth; the surfacing card is a view. If the user dismisses the card, the entry is still on disk at `status: dismissed`.
3. **Never rewrite the user's spoken context.** If the user explains why they want to keep a pépite, record their words verbatim in the "Status history" line as a blockquote, not paraphrased.
4. **Be sparing with the red light.** Two-or-more rule is a floor, not an aspiration. Over-flagging burns the signal. If the 🔴 icon shows up every research session, either the criteria are too loose or the bar is too low — audit and tighten.
5. **A pépite can stay a seed indefinitely.** Seed is a valid terminal state. Not every detected pépite needs to become work; the surfacing itself is sometimes the value.
6. **If the user says `frankenstein`**, back out of the last proposal and do not create the entry. Even detection can be scope creep if the current session is supposed to be narrowly focused.

## What this skill does NOT do

- **Cross-pépite synthesis** — no clustering, no "you've detected three pépites on X in the last month" pattern matching. Manual review of the INDEX is the v1 primitive.
- **Auto-archive by TTL** — seeds do not expire. The user decides when to archive.
- **Automatic propagation** — even with `relevance.specific_projects` set, every propagation requires per-target consent. Auto-propagation is a v2 target.
- **Slash commands** — `/pepite` commands (list / propagate / status) are v2. The v1 interface is speech-native trigger phrases only.
- **Pépite ranking** — no priority field, no effort estimate, no ROI calculator. The entry is a capture; prioritisation happens in the extraction step when a pépite becomes work.
- **Detection on non-research operations** — the skill does not watch implementation reads, edits, or routine tool calls. Only research operations produce pépites.

## Anti-Frankenstein reminder

The skill's surface is six files mirroring a frozen spec. Every addition beyond that surface — a slash command, an auto-archiver, a similarity index, a ranking system — is deferred by default. Add only what points to a documented pain.

If a future session wants to add a feature to this skill, the first question is: **has a user invocation of the current skill been blocked by the absence of that feature?** If not, defer.

---

*The pépite system is the seventh memory type in the Genesis stack, after user/feedback/project/reference/themes/journal. It is the first memory type whose primary job is cross-project propagation — a stepping stone toward Meta-Memory Layer 3 before the full Path B session happens.*
