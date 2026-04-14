<!-- SPDX-License-Identifier: MIT -->

# Pépites INDEX — Project Genesis

Chronological index of pépite entries (7th memory type per `.claude/docs/superpowers/specs/v1_pepite_discovery_flagging.md`). One-liner per entry, newest first. Each entry has routing metadata for cross-project propagation.

*(No entries yet — pépites are flagged automatically during research when "two or more" red-light criteria are met, then surfaced to the user at the next natural boundary for extraction / keep / propagate / dismiss.)*

## Red-light trigger criteria (short form)

A finding is flagged as a pépite when **at least two** of the following are true:

1. Contradicts a previous assumption or past research cache entry
2. Has asymmetric leverage — one-time setup unlocks ongoing compound value
3. Emerging tech / early-adopter stage with strong cross-source signal
4. Cross-cuts projects — solves a known open question in a different in-flight project
5. Saves ≥ 5 minutes per recurring use case OR eliminates a recurring pain
6. "Most-potential" framing in best-practice-at-date analysis (not necessarily best today, but likely best in 3-12 months)

If only one criterion is met, the finding goes into the normal R8 research cache — not flagged as a pépite.

## Entry states

- `seed` — just flagged, not yet reviewed by user
- `extracted` — user said "extract" and content has been pulled into a spec or implementation plan
- `actioned` — extraction has resulted in concrete work (PR, skill implementation, etc.)
- `archived` — kept for reference but no longer active
- `dismissed` — user said "dismiss" — not every detected pépite warrants work

## Surfacing protocol

When a red light is raised during research, Claude:

1. Creates the entry silently with `status: seed`
2. At the next natural conversation boundary, surfaces a short 🔴 Pépite card:

```
🔴 Pépite detected — <title>
Why: <one-line reason>
Relevance: origin=<X>, transverse=<Y>, also relevant to=<list of projects>
Full entry: memory/pepites/<file>.md
Choose: (a) extract now  (b) keep as seed  (c) propagate to other projects  (d) dismiss
```

3. User responds with one of (a)(b)(c)(d)
4. Claude updates the entry's status and takes the requested action

## Cross-project propagation

Propagation to other projects requires **explicit user yes per invocation**. When approved, Claude writes pointer files (< 20 lines each) into the target projects' auto-memory with a canonical-location reference. Zero duplication.

See the full spec at `.claude/docs/superpowers/specs/v1_pepite_discovery_flagging.md`.

## Entries

*(none yet)*
