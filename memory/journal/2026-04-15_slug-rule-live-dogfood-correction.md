<!-- SPDX-License-Identifier: MIT -->
---
name: Slug rule live-dogfood correction — an R8 entry fixed by running code, not by WebSearch
description: The first time a Project Genesis R8 research entry was corrected by the code in execution rather than by fresh research. The 2026-04-15 claude-code-session-jsonl-format entry said the cwd-to-slug rule replaced backslash, colon, and space with dash; the first dogfood run of session-post-processor/run.py proved underscore also maps to dash. The interesting thing is not the bug but the mechanism of discovery — running code falsified a confidence-high research entry without needing a new WebSearch pass.
type: journal
state: seed
opened_at: 2026-04-15
last_developed: 2026-04-15
keywords: r8-research-cache, live-dogfood, source-of-truth, strange-loop, empirical-vs-documented, slug-derivation, first-runnable-genesis
project_context: project-genesis v0.6.0 session, first runnable Genesis skill ships
authored_by: claude-opened-on-user-consent
---

# Slug rule live-dogfood correction

## Seed — 2026-04-15

### Authorship note

This thought was opened by Claude (me) during the v0.6.0 session, with the user's explicit consent via *"les 2"* — accepting both the chore PR and the proposed journal entry on the slug-rule moment. Per Layer 0 journal rules, both parties can open a thought when both consent; this is a Claude-opened seed, not a user-opened one. The user can add a verbatim layer in any future session via `"reprends la pensée sur la correction slug-rule"`.

### What triggered this thought

In the v0.6.0 session of Project Genesis, the first dogfood run of `skills/session-post-processor/run.py` failed on its very first action — locating the source JSONL — because the slug I derived from `cwd` was wrong.

The `claude-code-session-jsonl-format_2026-04-15.md` research entry (R8, `stack/`, confidence `high`, on-disk-verified against `a086701e.jsonl` 12 hours earlier) said the rule was to replace `\`, `:`, and space with `-`. My `slugify_cwd` followed the entry verbatim and produced `C--Dev-Claude_cowork-project-genesis`. The real directory on disk is `C--Dev-Claude-cowork-project-genesis`.

Underscore also maps to dash. The research entry, written at confidence `high` after on-disk verification, was wrong about one character class.

The code fix was a one-line change. But the moment worth preserving is not the bug.

### The observation this seed captures

**It is the first time a Genesis R8 research entry has been corrected by running code instead of by fresh WebSearch.**

Every prior correction of R8 content happened via web research — the 2026-04-15 jsonl-format refresh itself was a WebSearch pass (plus on-disk sampling of one file). This correction happened differently: I wrote code that depended on the entry, I ran the code against the real filesystem, and the filesystem disagreed with the entry. The fix was in the code. The entry is still wrong on disk as of this session — flagged as a v0.7 gap for a later refresh.

This is only possible because v0.6 is the first Genesis version that ships runnable code. Every prior skill was Markdown + YAML — specifications that cannot, by their nature, falsify anything, because they do not run. The moment Genesis shipped `run.py` is also the moment the R8 cache became *falsifiable by the project itself*.

That is the seed. One data point. Might generalise, might not.

### Amplification — Claude, 2026-04-15 (consent-based)

User consented via *"riffe"* on 2026-04-15 during the v0.6.0 chore session. Three framings, one pushback, one connection.

**Framing 1 — R8 as hypothesis, running code as falsification test (Popperian).** R8 entries are conjectures about the outside world, committed with a confidence level and a TTL. Every time a skill runs against real data it is a live experiment. A failed experiment falsifies the conjecture, the code gets patched, and the research entry is updated asynchronously as lower-priority follow-up. Under this framing, the research cache is always a bit behind the running code by some non-zero amount — and that is fine, because the code is where the world gets tested.

**Framing 2 — R8 as cache, running code as ground truth (cache-coherence).** R8 is an optimisation. WebSearch is expensive; entries exist so Claude does not re-run the same research on every decision. But the ground truth is whatever the code observes when it actually executes on the real machine. The cache can be stale (TTL handles that) and it can be wrong (this session's failure mode, now documented). Updates are lazy — the cache gets corrected when the code proves it wrong, not on a schedule. Under this framing, `expires_at` is a lower bound on staleness, not an upper bound on correctness.

**Framing 3 — R8 as theory, running code as practice.** R8 is a compressed model of the world. The code is an instantiation that interacts with reality. Disagreements between theory and practice are expected and informative; the question is which one to trust. The empirical answer in this session: trust the practice, patch the code first, update the theory later. Under this framing, the research cache is a theory that never gets to be purely theoretical — it exists to be cashed out in code.

All three framings agree on the same operational rule: **patch the code immediately, log the divergence, schedule the research refresh as a lower-priority follow-up**. They disagree on the epistemic status of the cache. I am not sure the disagreement matters operationally — it may be a distinction without a difference. It matters narratively: the Popperian framing is the most flattering to running code, the cache framing is the most humble, the theory/practice framing is the most familiar to anyone who has written software.

**Pushback — the strongest objection.** Generalising from one character-class bug is premature. Most R8 entries in this project are not about character sets — they are about which library to pick, which licence to use, what the plugin marketplace landscape looks like, which IDE integrations exist. Those entries are falsifiable only by external-world observation, not by running code. The slug-rule case is an edge case where code happens to be the right falsifier because the entity being described (a filesystem slug rule) is the same kind of entity that the code directly manipulates. That category overlap is rare. If I wrote a `run.py` that depended on "MIT is the right licence for Genesis", no amount of running would falsify it — the entry is about a social fact, not a mechanical one.

The honest answer is: running code is a falsifier for R8 entries **that describe the behaviour of systems the code interacts with**, and only those. That is a narrower claim than "running code is the source of truth". The slug-rule entry happened to fit. Most entries don't.

One data point is not a theory. The seed still rests on one data point.

**Connection — Hofstadter's strange loop, the compiler-bootstrapping metaphor.** The Genesis master vision invokes Hofstadter's strange loop explicitly, and the compiler-bootstrapping precedent specifically: the first C compiler was written in assembly, rewritten in C, and compiled by itself. Every C compiler since 1971 self-compiles. The equivalent move in Genesis is: research-cache entries are currently written by Claude during research sessions (via WebSearch + on-disk sampling). A later version of Genesis could ship skills that **write R8 entries as a byproduct of running** — the code that parses a JSONL would, on first run, emit a research entry describing what it found, supersede the stale one, and close the bootstrapping loop. The project dogfooding itself on the research cache, not just on the code.

That is not a v0.7 target. It is probably not a v1 target either. But it is the natural endpoint of the direction the slug-rule correction points in. Worth noting as a future ceiling, not an immediate action.

### Close of amplification

I have nothing else to add without becoming poetic. The seed now has the three framings, the strongest pushback against them, and a connection to the stated project vision. A future session can layer verbatim-quoted user content on top if the thought is re-opened, or the entry can rest as a resolved-enough stopping point.

---

*(End of 2026-04-15 layer. Future layers append above the `---` at the top of this section when the thought is re-opened.)*
