<!-- SPDX-License-Identifier: MIT -->

# Journal INDEX — Project Genesis

Chronological index of journal entries (6th memory type per Layer 0 journal system spec). One-liner per entry, newest first.

*(No entries yet — entries are created via user trigger phrases from Layer 0.)*

## How to create an entry

Use any of the trigger phrases from `~/.claude/CLAUDE.md` Journal System section. Works in French or English:

| Phrase | Action |
|---|---|
| **"Ouvre une pensée sur X"** / "open a thought on X" | New entry with `state: seed`. Claude asks what triggered it, captures verbatim, optionally offers amplification (consent required) |
| **"Reprends la pensée sur X"** / "continue the thought on X" | Load existing entry, summarize current state, add a new dated layer. Updates `state: growing` |
| **"Enregistre dans journal"** / "save as journal" | One-shot snapshot `state: captured` — static, doesn't grow |
| **"Enrichis cette pensée"** / "amplifie" / "riffe sur X" | Claude adds `### Amplification — Claude, YYYY-MM-DD (consent-based)` sub-section. **Consent required per invocation** |
| **"Clôture la pensée sur X"** / "résous la pensée" | `state: resolved` — entry stops growing but stays readable |

## Stratified dialogue format

Entries use the stratified format where each session's contribution lands as a new dated layer on top of the existing layers. See `~/.claude/CLAUDE.md` Journal System section for the full format specification.

## Hard rules for amplification

1. Never auto-amplify — consent required per invocation
2. Never rewrite the user's words — amplification appends, never modifies
3. Every addition is attributed and dated
4. Be sparing with poetry — only reach for metaphor when the thought calls for it
5. Pushbacks are valid amplifications
6. A layer can have no amplification — silence is valid

## Entries

*(none yet)*
