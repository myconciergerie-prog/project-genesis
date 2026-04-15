<!-- SPDX-License-Identifier: MIT -->
---
name: journal-system
description: Stratified thought capture — recognise French/English trigger phrases ("ouvre une pensée", "reprends la pensée", "enregistre dans journal", "enrichis", "clôture"), create or extend dated journal entries under memory/journal/, and gate any amplification on explicit user consent per the Layer 0 journal system spec (6th memory type, not auto-loaded, re-read intentionally).
---

# Journal system

This skill implements the **6th memory type** defined in Layer 0 (`~/.claude/CLAUDE.md` → "Journal System — Universal Thought Capture"). It lets the user capture irreducibly-dialogic moments — reflections, turning points, aesthetic peaks — in a stratified format that grows across sessions and is never rewritten by Claude.

Journal entries are **not auto-loaded** at session open. They are browsed intentionally, the way one re-reads a personal notebook. This skill only runs when the user explicitly triggers it via one of the phrases below.

**Canonical spec**: `~/.claude/CLAUDE.md` — "Journal System — Universal Thought Capture" section. The content of this skill is a 1:1 implementation of that spec. If the Layer 0 spec changes, this skill must be updated to match — never the other way around.

## When to invoke

Recognise these phrases in the current turn and act on them **directly, without asking the user to type a slash command**. The journal system is speech-native: the user drops a phrase into conversation and Claude handles the rest.

| Phrase (FR or EN) | Action | State transition |
|---|---|---|
| **"Ouvre une pensée sur X"** / "open a thought on X" | Create `memory/journal/YYYY-MM-DD_<slug>.md`. Capture the user's initial words verbatim. Ask what triggered it. Offer amplification — **consent required**. | → `seed` |
| **"Reprends la pensée sur X"** / "continue the thought on X" | Load the existing entry by slug or keyword. Summarise its current state in one paragraph. Ask which angle to develop. Add a new dated `## Layer N — YYYY-MM-DD` section. | `seed` / `dormant` → `growing` |
| **"Enregistre dans journal"** / "save as journal" | One-shot snapshot. Static entry, does not grow. Used for moments complete in themselves. | → `captured` |
| **"Enrichis cette pensée"** / "amplifie" / "riffe sur X" | Append `### Amplification — Claude, YYYY-MM-DD (consent-based)` sub-section to the current layer. **Consent mandatory per invocation**. | no state change |
| **"Clôture la pensée sur X"** / "résous la pensée" | Set `state: resolved`. Entry stops growing but remains readable. | any → `resolved` |

**Do not invent new trigger phrases.** The list is fixed by the Layer 0 spec. If the user says something ambiguous, ask them explicitly which action they want.

## Prerequisites

- The current project has (or can have) a `memory/journal/` directory. The `install-manifest.yaml` step of this skill creates it and seeds `memory/journal/INDEX.md` if missing.
- The user has opted into journal capture for this project (implicit once they fire the first trigger phrase — no separate opt-in card needed, because the trigger *is* the consent).

## The flow — five steps

### Step 1 — Recognise the trigger

The user speaks one of the phrases above. Match FR or EN. If the phrase references a thought "sur X", extract `X` as the working title / slug seed.

If the match is ambiguous (for example the user said "j'ai une idée sur X" which is *not* a journal trigger), do **not** auto-create an entry. Ask: *"Veux-tu que j'ouvre une pensée formelle sur X dans le journal, ou c'est juste une remarque de passage ?"*

### Step 2 — Load or create

- **Ouvre** → create new file per `entry-format.md` template. Generate slug from `X`: lowercase, spaces → `-`, strip accents, keep < 50 chars. Filename = `memory/journal/<YYYY-MM-DD>_<slug>.md`. If the file already exists (same date + slug), surface the existing path and ask the user if they meant "reprends" instead.
- **Reprends** → search `memory/journal/` for a file whose slug or frontmatter `name` matches `X`. If multiple matches, list them with `last_developed` dates and let the user pick. If zero matches, fall back to "ouvre" behaviour.
- **Enregistre** → create new file, state = `captured`, single `## Seed — YYYY-MM-DD` section with the user's verbatim message, no prompt for next layer, no amplification offered unless explicitly requested.
- **Enrichis** → the user must reference an existing open or growing thought. Find the most recently touched entry (or ask which one) and append the amplification sub-section under its current layer.
- **Clôture** → find the entry by slug, set `state: resolved`, touch `last_developed` to today, do not add any content.

### Step 3 — Capture the user's words verbatim

**Never paraphrase, summarise, or "improve" what the user said.** The entry preserves the user's voice. Paste their message inside a `> ` blockquote as the body of the `## Seed` or `## Layer N` section, then add a date stamp.

See `entry-format.md` for the exact template.

### Step 4 — Offer amplification (consent-gated)

After capturing the user's words, **always** ask:

> *"Tu veux que je riffe dessus ?"* / *"Want me to amplify this?"*

Wait for explicit yes. If yes, append a sub-section `### Amplification — Claude, <date> (consent-based)` under the current layer. Keep it grounded in the user's actual thought — don't free-associate. See `amplification-rules.md` for the six hard rules.

If no, or silence, leave the layer unamplified. A layer with no amplification is perfectly valid.

### Step 5 — Update metadata and INDEX

After any write:

- Update the entry's frontmatter `last_developed: <YYYY-MM-DD>` and `state: <current>`.
- Append a one-line entry to `memory/journal/INDEX.md`: `- [YYYY-MM-DD — <title>](YYYY-MM-DD_<slug>.md) — <state> — <one-line description>`.
- If the `INDEX.md` already has an entry for the same file, update it in place (don't duplicate).

## The six amplification hard rules — brief reminder

1. **Never auto-amplify.** Always ask consent first, wait for explicit yes.
2. **Never rewrite the user's words.** Amplification appends, never modifies.
3. **Every addition is attributed and dated** — `### Amplification — Claude, YYYY-MM-DD`.
4. **Be sparing with poetry.** Only reach for metaphor when the thought calls for it.
5. **Pushbacks are valid amplifications.** Disagree or reframe when useful.
6. **A layer can have no amplification.** Silence is a valid response.

Full rationale + examples in `amplification-rules.md`.

## Files in this skill

| File | Purpose |
|---|---|
| `SKILL.md` | This entry point — trigger recognition, flow map |
| `entry-format.md` | Frontmatter schema, stratified format, five states |
| `amplification-rules.md` | The six hard rules with rationale |
| `install-manifest.yaml` | Creates `memory/journal/` + `INDEX.md` in the target project |
| `verification.md` | Health card — confirms the skill wired correctly |

## Anti-Frankenstein reminders

- **Do not add new trigger phrases.** The five are fixed by Layer 0.
- **Do not auto-amplify.** Consent is mandatory on every invocation, even if a previous amplification was consented to.
- **Do not retroactively edit past layers.** Each layer is append-only. If the user wants to revise, they say so and a new layer captures the revision.
- **Do not collapse layers.** Stratification is the point — the entry's value is the chronological trace.
- **Do not auto-load entries at session open.** Journal is intentional, not ambient. If the user wants to re-read, they say so.
- **If the user says `frankenstein`**, back out of the last proposal immediately.

## What this skill does NOT do

- **Cross-project aggregation** — the `/journal timeline` view that walks every repo's `memory/journal/` on this machine. That is the Meta-Memory Path B session's job. This skill ships single-project capture only.
- **Auto-classification by keywords** — tags live in `keywords:` frontmatter, but no auto-tagger runs. The user adds keywords explicitly or Claude infers them with consent on entry creation.
- **Full-text search across entries** — use `grep` / `ripgrep` directly on `memory/journal/` when needed. This skill does not ship its own search.
- **Journal-driven behaviour change** — entries never direct Claude's future actions the way `feedback` or `project` memories do. They are read on demand, not at session open.
