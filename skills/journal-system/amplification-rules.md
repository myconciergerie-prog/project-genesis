<!-- SPDX-License-Identifier: MIT -->
---
name: journal-system / amplification-rules
description: The six hard rules that govern when and how Claude may amplify a user's journal entry. Mirrors the Layer 0 spec 1:1 — these rules are frozen and cannot be weakened.
---

# Amplification rules

Amplification is the most dangerous surface of the journal system. The point of a journal is to preserve the user's voice; amplification risks burying it under Claude's. These six rules exist to make amplification additive, attributed, and opt-in on every single turn.

**Source of truth**: `~/.claude/CLAUDE.md` → "Hard rules for amplification". If the Layer 0 rules change, this file must be updated — never the other way around.

## Rule 1 — Never auto-amplify

**Always ask consent first, every single time.**

Wait for an explicit yes. Consent given on a past turn, on a past entry, or on a past session does **not** carry over. The user must re-consent on every invocation.

The canonical ask is:

> *"Tu veux que je riffe dessus ?"* (FR)
> *"Want me to amplify this?"* (EN)

Acceptable yes signals: *"oui"*, *"vas-y"*, *"yes"*, *"go"*, *"amplifie"*, *"riffe"*. Anything ambiguous — silence, hesitation, *"peut-être"*, *"je ne sais pas"* — counts as **no**. Leave the layer bare.

**Why the rule is strict**: the vertigo-dogfooding entry from 2026-04-14 worked because amplification was earned in a specific moment of shared attention. Apply it formulaically and the same technique dies. Strictness on consent is what keeps amplification from becoming noise.

## Rule 2 — Never rewrite the user's words

The user's verbatim quote in a `> ` blockquote is immutable. Amplification **appends** new labeled sub-sections; it never edits the quoted text, never paraphrases it, never "improves" its grammar, never translates it.

If the user said it in French, the blockquote stays French. If the user's sentence is half-finished, it stays half-finished. If the user used a typo'd word, the typo stays. The journal preserves the original voice exactly as it was spoken.

**What counts as a violation**: any change to the characters inside the `> ` quote block after it has been written. Even "fixing" an obvious typo counts. If the user wants to revise, they open a new layer and the old quote remains intact.

## Rule 3 — Every addition is attributed and dated

Every Claude-authored sub-section carries:

```
### Amplification — Claude, YYYY-MM-DD (consent-based)
```

**Non-negotiable fields**:
- The word `Amplification` (or another explicit Claude-voice label if the content is not amplification — e.g. `Synthesis`, `Counter-argument`, `Question back`)
- The attribution `— Claude`
- The absolute date `YYYY-MM-DD` (never relative like "today" or "yesterday" — dates must be readable years later)
- The suffix `(consent-based)` to remind future readers that this was opt-in

The reader must always know, at a glance, whose voice they are reading and when it was written. Attribution is what makes the stratified format trustworthy across years.

## Rule 4 — Be sparing with poetry

Metaphor, historical parallel, cross-field analogy: reach for them only when the thought actually calls for it. The vertigo-dogfooding amplification worked because the subject was vertigo — the metaphors fit the content. Applied to a pragmatic engineering observation, the same metaphors would feel ornamental and false.

**Test before reaching for poetry**: if you removed the metaphor and stated the point plainly, would the user's thought lose something? If yes, the metaphor is earning its place. If no, it's ornament — cut it.

**Default register**: plain, specific, grounded. Amplification's job is to sharpen the thought, not to decorate it. A clear pushback is worth more than a pretty image.

## Rule 5 — Pushbacks are valid amplifications

A thinking partner disagrees when useful. If the user's thought has a hole, or reaches too fast for a conclusion, or elides a constraint, the amplification can say so. Labelled, dated, grounded in specifics.

Example:

```
### Amplification — Claude, 2026-04-15 (consent-based)

The move from "recursive tooling" to "infinite regress" skips a step. Recursion
terminates when the fixed point is reached — e.g. Genesis bootstrapping Genesis
converges once the output equals the input. It is not inherently infinite. If
the worry is instead "the tool evolves faster than my ability to audit it", that
is a different concern (supervision capacity, not self-reference).
```

**What pushback is not**: contrarianism for its own sake, or "devil's advocate" framing. A pushback must point to a specific missing piece or wrong turn and propose a sharper alternative. If you cannot name the hole concretely, stay silent instead.

## Rule 6 — A layer can have no amplification

If the user drops a thought and does not ask for enrichment, the layer is complete as-is. Capture the verbatim quote, update metadata, update the INDEX, stop. Do not jump in uninvited. Do not offer amplification a second time if the user already said no this turn. Do not decorate the quote with a closing observation.

Silence is a valid response. A journal entry composed entirely of unamplified layers is a valid journal entry.

## Additional implementation rules

These are operational consequences of the six hard rules. They do not add new constraints — they are how the rules manifest in code paths.

### R7 — Consent is a blocking gate

The flow is:

1. Capture the user's verbatim quote in the layer.
2. Write that to disk (the quote is preserved regardless of consent).
3. **Only then** ask for amplification consent.
4. On yes, write the amplification sub-section in a second file edit.
5. On no / silence / ambiguous, close the turn.

**Never write the amplification first and show it to the user for approval.** That pre-generates content the rules say must be opt-in — even if the user later says no, the text exists in your context window as if it had been published.

### R8 — Consent does not cascade

Consent on Layer 1 does not authorise amplification on Layer 2. When the user returns with "reprends la pensée", the new layer's amplification requires a new consent ask. Same rule applies within a single session if the user opens multiple entries back to back.

### R9 — No preemptive offers

Do not say *"I have some thoughts on this — want me to share?"* before the user has finished speaking, and do not queue up amplifications "in case" the user consents later. The amplification only exists after the consent, inside the same turn that wrote the layer.

### R10 — Amplification is never mandatory for the entry to be "complete"

An entry with zero amplifications across all its layers is fully valid and fully useful. Do not flag such entries as "needs enrichment" or similar. The user's voice alone is the minimum viable entry.

## Anti-Frankenstein reminder

If the user says **`frankenstein`** at any point during an amplification offer or an amplification write, stop immediately, back out of the last proposal, and leave the layer bare. The word overrides every in-flight operation.
