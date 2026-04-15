<!-- SPDX-License-Identifier: MIT -->
---
name: journal-system / entry-format
description: Canonical frontmatter schema and stratified dialogue format for journal entries. Mirrors the Layer 0 spec in ~/.claude/CLAUDE.md 1:1 — never diverge silently.
---

# Entry format

Every journal entry is a single Markdown file under `memory/journal/<YYYY-MM-DD>_<slug>.md`. The file has frontmatter, a title, and one or more dated layers. Each layer quotes the user verbatim and optionally contains a consent-based amplification sub-section and the user's response.

## Frontmatter schema

```yaml
---
name: <thought title>
description: <one-line summary — used for index lines and cross-project search>
type: journal
state: seed | growing | dormant | resolved | captured
opened_at: YYYY-MM-DD
last_developed: YYYY-MM-DD
keywords: <comma-separated tags, lowercase, accents stripped>
project_context: <slug of the project where the thought was opened — used by future cross-project aggregation>
---
```

Every field is required. If the user has not given enough information to fill `description` or `keywords`, fill them with a best-effort placeholder and flag them as `(draft)` in a trailing comment. Do not block on missing metadata — the user's words come first.

## The five states

| State | Meaning | Transitions |
|---|---|---|
| `captured` | One-shot snapshot. Complete in itself. Does not grow. Created by "enregistre dans journal". | Terminal (stays captured). |
| `seed` | Just opened by "ouvre une pensée". Barely developed. Waiting for the next session. | → `growing` on first "reprends", or → `dormant` after a long idle. |
| `growing` | Active. Being developed across multiple sessions via "reprends la pensée". | → `dormant` after a long idle, → `resolved` on "clôture". |
| `dormant` | Paused. Can resume at any time — days or months later. No time limit. | → `growing` on "reprends", → `resolved` on "clôture". |
| `resolved` | Crystallised. Stopped growing. Kept for reference. | Terminal (stays resolved). |

**When to flip to `dormant`**: do not auto-expire. The state only changes when the user triggers an action. If you notice an entry hasn't been touched in months during a "reprends" search, you can *suggest* marking it dormant, but never flip without asking.

**`captured` vs `seed`**: `captured` is a snapshot the user considers complete. `seed` is an opening they intend to develop. The trigger phrase decides: "enregistre" → captured, "ouvre" → seed.

## Stratified dialogue format — the canonical template

```markdown
<!-- SPDX-License-Identifier: MIT -->
---
name: <thought title>
description: <one-line summary>
type: journal
state: seed
opened_at: 2026-04-15
last_developed: 2026-04-15
keywords: example, placeholder
project_context: project-genesis
---

# <Title of the thought>

## Seed — 2026-04-15
> <the user's initial verbatim words, inside a blockquote, exactly as said>

### Amplification — Claude, 2026-04-15 (consent-based)
<richer articulation: metaphors, historical parallels, structural clarifications, pushbacks,
questions that sharpen the thought. Only present if the user consented to amplification.
Keep it grounded in the user's actual words — do not free-associate.>

### Response — user, 2026-04-15
<what the user added back in response to the amplification, verbatim. Optional.>

---

## Layer 2 — 2026-05-02
> <the user returning with a new angle, verbatim>

### Amplification — Claude, 2026-05-02 (consent-based)
<continued development, separately consented to on this turn>

### Response — user, 2026-05-02
<...>

---

## Layer 3 — 2026-06-14
> <next return, verbatim>
```

## Rules enforced by this format

1. **Every section starts with the user's verbatim words in a blockquote.** No paraphrase. No "the user said X" framing. The raw text.
2. **Every Claude addition is explicitly labelled and dated** — `### Amplification — Claude, <date> (consent-based)`. The reader must always know whose voice they are reading.
3. **Horizontal rules (`---`) separate layers.** They make the chronology scannable.
4. **Layers are append-only.** Adding `Layer N` does not touch `Layer 1`. If the user wants to revise a past thought, they say so and a new layer captures the revision.
5. **Sub-sections inside a layer stay in order**: `## Seed|Layer N` → `> <user>` → `### Amplification — Claude` (optional) → `### Response — user` (optional).
6. **The `# Title` never changes** once the entry is created. If the user reframes the thought entirely, they open a new entry — journal entries are not tickets to be renamed.

## Slug generation — how to build the filename

Given a trigger phrase like "ouvre une pensée sur la vertige du dogfooding récursif":

1. Extract the topic: `la vertige du dogfooding récursif`.
2. Lowercase: `la vertige du dogfooding récursif`.
3. Strip accents: `la vertige du dogfooding recursif`.
4. Replace spaces and non-alphanumerics with `-`: `la-vertige-du-dogfooding-recursif`.
5. Trim leading / trailing hyphens.
6. Truncate to < 50 characters from the right: `la-vertige-du-dogfooding-recursif` (already < 50).
7. Prepend the date: `2026-04-15_la-vertige-du-dogfooding-recursif.md`.

If the slug collides with an existing file (same date, same slug), append `-2`, `-3`, etc. This is rare but possible if the user opens two thoughts on the same topic in the same day.

## Where entries live

- **Primary**: `memory/journal/` inside the project repo. Version-controlled. Reviewed via PR like any other memory entry.
- **Auto-memory fallback**: `~/.claude/projects/<slug>/memory/journal_*.md` — used only when the session is pre-worktree or pre-repo. Migrate into the repo at the next worktree opportunity.
- **Cross-project view**: deferred to the Meta-Memory Path B session. Until then, cross-project journal navigation is manual, but entries are written consistently so the future aggregator has clean input.

## Index file — `memory/journal/INDEX.md`

Every journal entry is listed in `memory/journal/INDEX.md` under one of the five state sections. Format:

```markdown
<!-- SPDX-License-Identifier: MIT -->

# Journal INDEX — <project name>

Stratified thought capture per the Layer 0 journal system spec. Entries are not auto-loaded at session open — they are read intentionally.

## Growing
- [2026-04-15 — the vertigo of recursive dogfooding](2026-04-15_la-vertige-du-dogfooding-recursif.md) — the feeling of writing a tool that will be used to write itself

## Seed
- [2026-04-15 — on the shape of attention](2026-04-15_on-the-shape-of-attention.md) — first pass, awaiting next layer

## Captured
- [2026-04-14 — the commit hash moment](2026-04-14_the-commit-hash-moment.md) — snapshot, complete

## Dormant
*(none)*

## Resolved
*(none)*
```

Update this file every time an entry is created, transitioned, or last-developed. Never let it drift out of sync — the INDEX is the only cheap way to browse without walking every file.
