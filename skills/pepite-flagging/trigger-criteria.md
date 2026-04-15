<!-- SPDX-License-Identifier: MIT -->
---
name: pepite-flagging / trigger-criteria
description: The six red-light criteria that gate whether a research finding becomes a pépite entry or a plain R8 cache row. A finding qualifies when at least two criteria are met. One criterion alone is not enough — goes into the normal cache. Each criterion has rationale, calibration example, and anti-noise guidance.
---

# Red-light trigger criteria

A research finding becomes a pépite when **at least two** of the six criteria below are met. One criterion alone is not enough — the finding goes into the normal R8 research cache without a red-light flag.

**Why a two-of-six bar**: a single criterion is a normal research observation. Two or more criteria indicate the finding is unusually high-leverage along at least two independent axes — the kind of discovery that would save compound future work if captured, and compound future pain if lost.

**Why not higher** (e.g. three-of-six): most real pépites satisfy 2–3 criteria cleanly. A three-of-six floor would miss the genuinely-valuable cross-cutting findings that are only exceptional on two axes. Empirical calibration will tell — if v1 over-flags, raise to three; if v1 under-flags, lower to one-of-six.

## The six criteria

### Criterion 1 — Contradicts a prior assumption or R8 cache entry

The finding proves a previously-held assumption wrong, or falsifies an active R8 research cache entry. Contradiction is asymmetric information — the correction is valuable regardless of whether the underlying topic is important, because preventing future decisions from depending on the wrong assumption has compound value.

**Why**: finding a single contradiction costs one session. Making ten future decisions on the wrong assumption costs ten sessions. The ratio is the pépite.

**Calibration example**:
> During a v0.6 dogfood run, `run.py` proved the slug rule in the `claude-code-session-jsonl-format` R8 entry was incomplete (underscore also maps to `-`). This contradicts a `confidence: high` R8 entry. **Criterion 1 met.**

**Anti-noise guard**: a minor wording difference in an R8 entry is not a contradiction. A character-class omission in a slug rule **is**, because code downstream actually depends on the missing character.

### Criterion 2 — Asymmetric leverage — one-time setup unlocks compound value

The finding describes a setup or pattern where the cost is paid once and the benefit accumulates across every future session, project, or user. Typical shapes: a new tool that automates a recurring task, a skill that a Claude Code plugin ships and every user of the plugin inherits, a research cache entry that hundreds of future decisions can reference.

**Why**: this is the definition of leverage. A one-hour investment that saves five minutes per week across twenty future projects is a 160-hour return on a one-hour cost, over a year.

**Calibration example**:
> A new MCP server that exposes GitHub API operations via JSON-RPC with no auth setup (uses the host's existing `gh` auth). One install per machine, ongoing benefit across every project. **Criterion 2 met.**

**Anti-noise guard**: a feature that only benefits the current project does not meet this criterion, no matter how useful. Project-local value is not leverage — it is just value.

### Criterion 3 — Emerging tech / early-adopter stage

The finding describes a tool, pattern, or library that is in early maturity (beta, v0.x, < 1000 GitHub stars but growing fast, mentioned by multiple independent credible sources in the last 30 days) and has a plausible path to being mainstream in 3–12 months. Early adoption gives asymmetric positioning: the team that adopts first accumulates proficiency and becomes the reference implementation before the mainstream arrives.

**Why**: mainstream tools are priced-in — everyone knows about them and they do not give an edge. Early-adopter tools give an edge proportional to the adoption gap.

**Calibration example**:
> Google Antigravity shipped in March 2026 as a multi-model agent IDE (Gemini 3.1 Pro + Claude 4.6 + GPT-OSS). Free for individuals, Manager Surface for multi-agent orchestration. Signals: official Google launch, documented as "agent-first IDE" in TechCrunch and Anthropic docs. **Criterion 3 met.**

**Anti-noise guard**: a repo with 100 stars that has not been updated in a year is not emerging — it is either dormant or dead. "Emerging" requires a credible growth signal, not just novelty.

### Criterion 4 — Cross-cuts projects — solves an open question in another in-flight project

The finding directly applies to an unresolved problem or pain point in a different in-flight project on the user's machine. The pépite is not just "interesting in general" — it is **the answer** to something the user was stuck on elsewhere.

**Why**: cross-cut findings compound across projects linearly with the number of projects that benefit. The user runs ~20 projects; a cross-cut finding that applies to three of them has triple the value of a single-project finding.

**Calibration example**:
> While researching Claude Code hooks for Genesis, Claude reads that `SessionStart` hooks can inject environment variables into the first user turn. This directly solves the "how do we auto-inject project identity into the Cyrano CLI at session open" question the user flagged two weeks ago during the Cyrano v0 session. **Criterion 4 met.**

**Anti-noise guard**: a general-purpose tool that "could probably" apply to other projects is not cross-cut — it is just generic. Cross-cut requires a specific, named, documented open question in another specific project.

### Criterion 5 — Saves ≥ 5 min per recurring use case OR eliminates a recurring pain

The finding measurably reduces friction on a recurring operation. "Recurring" means the operation happens more than once a week, across one or more projects. Five minutes is the minimum threshold — below that, the cost of the pépite entry exceeds the saved time over a reasonable horizon.

**Why**: recurring friction is where the most compound pain hides. A 5-minute task done 200 times a year is 16 hours. Eliminating it is a pépite regardless of whether any other criterion applies — but usually at least one other does (leverage, cross-cut, emerging).

**Calibration example**:
> A shell alias that combines `git fetch origin && git status -b -s && git log --oneline origin/main..HEAD` into a single `gst` command, saving ~45 seconds per session-open ritual across every project. 45s × 30 sessions/week × 52 weeks = 19.5 hours/year. **Criterion 5 met.** (Also criterion 2 — asymmetric leverage.)

**Anti-noise guard**: one-off speedups ("this script runs 2x faster if you use uvloop") are not recurring-pain pépites. They are optimisations — log them in the R8 cache without a red light unless they also meet another criterion.

### Criterion 6 — Most-potential framing in best-practice-at-date analysis

The finding is NOT the best choice today but has the strongest signal for becoming the best choice in 3–12 months. This criterion is specifically for capturing the "upside" candidate in a decision where the "safe" choice is already obvious. See the Layer 0 `best-practice-at-date default` rule for the two-axis framing ("best at date" vs "highest potential").

**Why**: safe choices are known. Upside choices need deliberate capture because they are discounted by default (they are not the best today, so the normal decision process drops them). The pépite system is where upside candidates live until they are ready.

**Calibration example**:
> Best at date for a new Genesis project's local DB: PostgreSQL + `pgvector`. Highest potential: DuckDB + `vss` (vector-similarity extension) — DuckDB is embedded (zero ops) and `vss` released in March 2026 as a stable extension. Not the best today because the ecosystem is smaller, but likely the best for embedded analytics workloads in 6 months. **Criterion 6 met on DuckDB+vss.** (The PostgreSQL choice goes into the normal R8 cache; DuckDB becomes a pépite.)

**Anti-noise guard**: "this could be big" speculation without a specific signal is not highest-potential framing. Require at least one concrete indicator: a recent stable release, a funded startup built on it, a major vendor adopting it, or multiple credible independent sources citing it as "the one to watch".

## The "two or more" rule — applied

For every candidate finding during research, Claude walks the six criteria mentally and counts hits. Scoring examples:

| Finding | C1 | C2 | C3 | C4 | C5 | C6 | Hits | Action |
|---|---|---|---|---|---|---|---|---|
| Slug-rule underscore correction (v0.6 dogfood) | ✓ | — | — | — | — | — | 1 | R8 cache row only |
| DuckDB+vss for embedded analytics | — | ✓ | ✓ | — | — | ✓ | 3 | **Pépite** |
| Google Antigravity multi-model agent IDE | — | — | ✓ | ✓ | — | ✓ | 3 | **Pépite** |
| A shell alias saving 45s/session | — | ✓ | — | — | ✓ | — | 2 | **Pépite** |
| `pgvector` as Postgres vector extension | — | ✓ | — | — | — | — | 1 | R8 cache row only |

Note the slug-rule correction scored only 1 (contradicts a prior R8 entry). It is a valuable correction but it does not cross the two-of-six bar, so it is a plain R8 fix — which is what actually happened in the v0.6 session. The journal entry captures the epistemic observation; there is no pépite entry for it.

## Anti-over-flagging discipline

The red light should feel **slightly rare**. If the 🔴 card shows up in every research session, the criteria are too loose or the bar is too low. Signals that over-flagging is happening:

- More than one pépite per week on average
- Pépites with `status: dismissed` outnumber pépites with `status: extracted` or `actioned`
- User starts saying "another one?" with mild frustration

Remedies:

- Tighten the "two or more" bar to "three or more" for a trial period
- Audit the last five pépites and identify which criterion was the weakest — add an explicit anti-noise guard to that criterion
- Temporarily require manual-only flagging (speech-native) and disable the auto-detect watcher until the noise subsides

## Anti-under-flagging discipline

The red light should also not be **so rare that pépites are lost**. If the user says "you should have flagged that" about a past finding, the criteria are too strict or the bar is too high. Signals:

- Fewer than one pépite per month despite active research sessions
- User manually flags findings that Claude should have auto-detected
- Retrospective reviews surface findings that were in the R8 cache but would have been pépites

Remedies:

- Loosen the "two or more" bar to "one or more" for a trial period
- Audit the last five manual flags and calibrate Claude's detection against them
- Add a new criterion if a recurring pattern of missed pépites reveals a trigger not covered by the existing six

## When in doubt — err on the side of creating the entry

A dismissed seed costs a file write and a brief card on screen. A missed pépite costs compound pain over months. The asymmetry favours creating entries; the user is the filter. This is the same reasoning as the redaction patterns in `session-post-processor`: over-redact is cheap, under-redact is an incident.

Exception: if the user has said `frankenstein` in the current session, back off. Even detection can be scope creep in a narrowly-focused session.
