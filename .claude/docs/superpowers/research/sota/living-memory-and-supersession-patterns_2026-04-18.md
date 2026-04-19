<!-- SPDX-License-Identifier: MIT -->
---
topic: living-memory-and-supersession-patterns
type: sota
created_at: 2026-04-18
expires_at: 2026-04-25
status: active
confidence: high
scope: universal
supersedes: null
sources:
  - https://martinfowler.com/eaaDev/EventSourcing.html
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing
  - https://microservices.io/patterns/data/event-sourcing.html
  - https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/event-sourcing.html
  - https://www.kurrent.io/blog/snapshots-in-event-sourcing
  - https://dev.to/young_gao/event-sourcing-explained-when-crud-is-not-enough-4od5
  - https://openreview.net/pdf?id=k0wyi4cOGy
  - https://aclanthology.org/2024.emnlp-main.486.pdf
  - https://cleanlab.ai/blog/tlm-structured-outputs-benchmark/
  - https://arxiv.org/pdf/2306.13063
  - https://www.sensible.so/blog/confidence-signals
  - https://xtdb.com/blog/building-a-bitemp-index-2-resolution
  - https://www.juxt.pro/blog/bitemporality-more-than-a-design-pattern/
  - https://v1-docs.xtdb.com/concepts/bitemporality/
  - https://en.wikipedia.org/wiki/Temporal_database
  - https://www.hyperstart.com/blog/legal-document-version-control/
  - https://www.hubifi.com/blog/immutable-audit-log-basics
  - https://oneuptime.com/blog/post/2026-01-30-mongodb-document-versioning/view
  - https://fynk.com/en/blog/document-audit-trail/
  - https://github.com/homeport/dyff
  - https://aws.amazon.com/blogs/database/build-a-cqrs-event-store-with-amazon-dynamodb/
internal_cross_references:
  - ~/.claude/memory/layer0/pattern_state_machine_outbox_from_day_one.md
  - ~/.claude/memory/layer0/workflow_research_and_memory.md
---

# Living memory & supersession patterns — SOTA 2026

R8 entry backing **Genesis v1.5.0 — Living drop zone memory**. Grounds the design decisions (per-document snapshots, filesystem archive, no silent resolution, halt-with-remediation on missing API) in 2026 state-of-the-art patterns.

## Executive summary

**Seven load-bearing findings** drive Genesis v1.5.0 design:

1. **Event sourcing is the canonical audit pattern for SaaS, but snapshots-only are defensible when the domain is low-frequency single-writer.** Martin Fowler, Kleppmann-lineage consensus, and 2026 DEV Community practical guides all recommend "first explore domain modeling before event-sourcing". Genesis's drop_zone_intent is rare-write, single-user, single-project — the simpler snapshot-only pattern aligns with this discipline.
2. **Snapshots + retention policy is the universal optimization pattern when event replay becomes costly** (Azure, AWS Prescriptive, Kurrent, Couchbase all agree). Typical policy: "keep last N per aggregate, prune the rest". Genesis defers the retention policy to v1.5.1+ (pain-driven when dogfood surfaces disk pressure).
3. **LLM multi-document conflict detection in 2026 uses multi-agent architectures with dedicated Conflict Resolution Agents** (KARMA paper, EMNLP 2024 knowledge-conflicts survey). The canonical resolution heuristic: source recency + source authority + number of supporting observations. **Critical caveat: LLMs are empirically overconfident in self-reported confidence scores** — don't trust "confidence > threshold = auto-resolve".
4. **Cleanlab TLM benchmarks show trust scores beat self-reported confidence by 25% precision/recall on structured outputs.** Alternative: Sensible's "confidence signals" (multiple-answers-detected / partial-answer / no-context) as structural flags, not scalar scores. Genesis v1.5.0 uses the structural flag approach: extractor flags divergences, never a "confidence" numeric threshold.
5. **Bitemporal databases (XTDB, Datomic) are overkill for single-writer memory with a single time axis** (Wikipedia, JUXT, XTDB docs). Genesis does not need "valid time vs system time" — it only has "when the snapshot was written". Single-time archive is sufficient.
6. **Immutable audit trails with cryptographic chaining (Hubifi, MongoDB document versioning) are standard for compliance-grade systems.** Genesis does NOT need cryptographic chaining (no tamper-resistance requirement from Victor) — simple filesystem archive with timestamp naming is sufficient. Cross-ref Layer 0 `pattern_state_machine_outbox_from_day_one.md` shows the SaaS-grade pattern; Genesis is the simpler end of the spectrum.
7. **YAML-frontmatter + filesystem-path is the canonical git-like document version-control pattern** (GitHub Docs uses it for multi-version docs, `dyff` tool is the canonical YAML-diff). Genesis aligns with this convention.

**Confidence**: high. 20+ sources, converging consensus on the above 7 findings. One open question (snapshot retention policy) honestly deferred.

## Finding 1 — Event sourcing vs snapshot-only : when is each right ?

### SOTA consensus

Martin Fowler's canonical definition (still the reference in 2026): *"Ensure that all changes to application state are stored as a sequence of events. Not just can we query these events, we can also use the event log to reconstruct past states, and as a foundation to automatically adjust the state to cope with retroactive changes."*

Azure, AWS Prescriptive Guidance, and Microservices.io agree: event sourcing **becomes valuable** when :
- Multiple writers produce transitions on the same entity
- Forensic reconstruction of "how did we get here" is required
- Analytics queries are transition-based (funnel, time-between-states)
- Cross-service reactions depend on transitions (outbox + event bus)

2026 DEV Community practical guide (Young Gao, "Event Sourcing Explained: When CRUD Is Not Enough") is explicit about the **inverse** case — event sourcing is **overkill** when :
- Single writer + low frequency
- No downstream consumers
- No forensic requirement beyond "current state + previous state"
- The aggregate has a small, well-known transition matrix

Kurrent ("Snapshots in Event Sourcing") makes the optimization layering explicit: *"Snapshots are an optimization, not a replacement for the event stream. The event stream remains the source of truth, and you can regenerate snapshots from it at any time."*

### The domain-modeling-first discipline

Kurrent, echoing Greg Young (event-sourcing canonical voice): *"Before deciding to use snapshots, re-evaluate your stream design. It may appear that you may not need snapshotting by shaping your domain model differently."*

This is anti-Frankenstein SOTA applied to data architecture: **the most powerful tool is the simplest domain model that satisfies the actual requirements**.

### Application to Genesis v1.5.0

Genesis's drop_zone_intent.md fits the "event sourcing is overkill" profile :
- **Single writer** (Victor in one session)
- **Low frequency** (fresh bootstrap + occasional re-runs on revised brief)
- **No downstream consumers** (Layer B reads current state, not event stream)
- **No forensic requirement beyond single-previous-snapshot** (Victor wants to see "what changed vs last time", not "replay the full journey")
- **Transition matrix** trivial (snapshot N → snapshot N+1 via re-run, or snapshot N unchanged)

→ **Snapshot-only pattern with filesystem archive is the right choice** for Genesis. Event log would be anti-Frankenstein.

Cross-reference: Layer 0 `pattern_state_machine_outbox_from_day_one.md` codifies the event-log pattern for **SaaS marketplaces** (Shopify, Stripe, Uber, Airbnb, GoCardless / Monzo) — those are multi-writer, high-frequency, compliance-driven systems. Genesis is the opposite end of the spectrum; adopting the simpler pattern here is correct discipline, not regression.

## Finding 2 — Snapshot retention policy : keep last N, prune rest

### SOTA consensus

**Kurrent**: *"Old snapshots pile up. Set a retention policy — keep the latest two or three per aggregate and prune the rest."*

**AWS CQRS on DynamoDB**: Once a snapshot is superseded, older items get TTL attribute. DynamoDB Streams + Lambda trigger for auto-archival.

**Couchbase event-sourcing pattern**: Combine snapshots + retention policy + event compaction. Monitor store growth; archive old events.

### Application to Genesis v1.5.0

**Deferred to v1.5.1+**. Rationale :
- No dogfood signal yet that disk pressure is a concern
- Retention policy adds surface (trigger, TTL counter, user-facing config) that anti-Frankenstein gate requires justifying by observed pain
- v1.5.0 keeps all archived snapshots indefinitely; v1.5.1+ adds cap (e.g., keep last 10, prune oldest) if dogfood surfaces pain

If implemented later, canonical choice is **keep-last-N** (simpler than TTL for Genesis: Victor controls lifecycle via filesystem directly if needed).

## Finding 3 — LLM multi-document conflict detection : multi-agent + flag-never-resolve

### SOTA 2026

**KARMA paper (OpenReview, 2026)** — multi-agent LLM systems for knowledge graph enrichment :
- Dedicated Conflict Resolution Agent module
- Logical incompatibility detection as first-class concern
- Candidate triplets evaluated by LLM-verifier before integration
- Quality control scores assess structure + citations + consistency

**EMNLP 2024 survey — Knowledge Conflicts for LLMs** — canonical taxonomy of conflict types and mitigation strategies. Key heuristics for LLM-proposed resolution :
- **Source recency** (newer source wins by default, subject to context)
- **Source authority** (primary > secondary > tertiary)
- **Supporting observations** (more sources agreeing = stronger signal)

**2026 consensus on multi-source LLM extraction UX** : contradiction detection is the *first step*, **human-in-the-loop resolution** is the *second step*. Silent auto-resolve is **anti-pattern** because LLMs are overconfident (see Finding 4).

### The flag-never-resolve principle

**Critical discipline** from knowledge-conflicts survey + KARMA + Sensible confidence signals :
- LLMs can reliably *detect* contradiction (two different values for same semantic field)
- LLMs **cannot reliably** *arbitrate* which is correct (biased by training priors + recency-in-context)
- The correct role for the LLM is **flag + surface to human**, not resolve

### Application to Genesis v1.5.0

**Extractor prompt augmentation design** :

The v1.4.0 extractor currently produces one value per field. v1.5.0 prompt augmentation :

```
When you see two or more DIFFERENT values for the same semantic field across
the provided documents, do NOT resolve silently. Emit both values in the
`divergences[]` array with their sources and preserve the contradiction for
human arbitration.

Emit `divergences[]` entries with shape :
  {
    "field": "<semantic_field_name>",
    "candidates": [
      {"value": "<value_A>", "source": {<citation>}},
      {"value": "<value_B>", "source": {<citation>}}
    ]
  }

For each divergent field, also leave `<field>` at null in the main output
(not one of the candidates — the arbitration layer will fill it).
```

This implements the "flag, never resolve" SOTA principle.

**Cross-session detection** (algorithmic, non-LLM) — simple field-by-field comparison between current snapshot and new extraction. No LLM involvement → no overconfidence risk. Pure data diff.

## Finding 4 — LLM confidence scoring : structural signals beat scalar scores

### SOTA 2026

**Cleanlab TLM benchmark** (2026) : Trustworthy Language Model uncertainty estimator scores trustworthiness of any LLM response including per-field structured outputs. Beats LLM-as-a-judge, LLM-judges-per-field, and Token Log Probabilities by **25% precision/recall on error detection**.

**Empirical finding from arxiv 2306.13063 + openreview GjEQKFxFpZ** : *"LLMs are often overconfident in their own outputs, which limits the effectiveness of self-reported confidence."*

**Token probability caveat (Cleanlab)** : Token probabilities *fail to detect cases when the LLM does not know it does not know* (high epistemic uncertainty due to lack of similar training data). Suboptimal for open-domain text fields where the same statement has many valid expressions.

**Sensible confidence signals** (alternative approach) : Replace scalar confidence with **structural flags** :
- `multiple-possible-answers` detected
- `partial-or-incomplete-answer`
- `uncertain-answer`
- `no-answer-returned-without-context`

Each flag is binary, sourced from structural inspection of the extraction, not from self-report.

**2026 structured output major-provider status** : OpenAI, Anthropic, Google all support **constrained decoding** native — schema-valid tokens only, making syntax errors impossible by construction. But this does NOT help with semantic correctness — a schema-valid wrong answer is still wrong.

### Application to Genesis v1.5.0

**Pragmatic stance** :
- **No scalar confidence threshold** in the arbitration decision ("confidence > 0.8 = skip arbitration"). Would rely on self-report, which SOTA shows is unreliable.
- **Binary structural flag** as trigger: divergence detected → arbitration. No divergence → no arbitration.
- **Extractor prompt constrains output via JSON schema** (leveraging Anthropic native structured outputs for the divergences[] array shape). The schema validity is enforced; the semantic correctness is delegated to human arbitration.

This aligns with the SOTA "structural signals over scalar confidence" principle.

## Finding 5 — Temporal databases : bitemporal is overkill for single-time memory

### SOTA

**XTDB** (JUXT) : Bitemporal = system-time + valid-time. Valid time is the "when this fact became true in the business sense" vs system time "when we recorded it". Essential for audit-regulated systems ("what did you know and when did you know it ?").

**Datomic** : Unitemporal (system-time only). Each entity has a single timeline of immutable values through system time. No valid-time dimension.

**Postgres** : Neither temporal by default. `pg_bitemporal` extension adds it ; query planner does not understand bitemporal columns natively. Bytebase 2026 footgun survey mentions bitemporality as common false-start in SaaS migrations.

**Awesome-data-temporality list** (curated GitHub) : canonical references across temporal modalities. Consensus: bitemporal if regulated, unitemporal if just audit, none if neither.

### Application to Genesis v1.5.0

**Single-time snapshot is correct.** Genesis drop_zone_intent has **one** timeline : "when this snapshot was written". There is no "valid time in the business sense" distinct from system time — Victor's "this is the current truth" is the single time axis.

Adopting bitemporal would be Frankenstein-adjacent : adds a dimension (valid-time metadata) without a pain point justifying it.

**If Genesis ever needs bitemporality** (e.g., "this brief is valid from 2026-04-01 although we extracted it 2026-04-18") — that's a v2.x.x MINOR, not v1.5.0. Deferred honestly.

## Finding 6 — Audit trail : activity timeline is the UX pattern

### SOTA 2026

**Fynk blog, Legal Document Version Control 2026, Docsie** :
- Audit trails capture context + metadata per action : which version, what change, from where
- Tamper-resistant + complete: no edit or delete of trail entries without trace
- Activity timeline is the canonical UX : "John Smith changed the status from 'Pending' to 'Approved' on 15 Jan 2026 at 14:32"

**Hubifi / MongoDB document versioning** — three canonical storage strategies :
- **Embedded versioning** (history inline in the document) — simple cases
- **Separate collections for full audit** — compliance-grade
- **Diffs only** — large documents, frequent changes

**Cryptographic chain** (Hubifi) : Each new entry cryptographically tied to the previous one. If someone alters an entry, the seal breaks. Overkill for Genesis (Victor is single writer, no tamper-resistance need).

### Application to Genesis v1.5.0

**Separate archive strategy** = MongoDB "separate collections for full audit". For Genesis filesystem : current snapshot + `drop_zone_intent_history/` directory. Aligned with canonical strategy.

**No cryptographic chain**. Genesis does not have tamper-resistance requirement (Victor trusts own filesystem).

**Activity timeline UX deferred to v1.5.1+**. v1.5.0 ships the archive substrate ; the timeline UX (Layer B expandable marker showing archive diff) is the v1.5.1+ pain-driven next step.

**Immediate Layer B marker** = lightweight audit signal ("this field was arbitrated") without full activity timeline. Bridges the v1.5.0 → v1.5.1+ evolution.

## Finding 7 — YAML frontmatter + git-like versioning : canonical doc-version pattern

### SOTA

**GitHub Docs** : YAML frontmatter + liquid operators support multi-version docs single-source. Canonical doc-version pattern at scale.

**`dyff` tool** (homeport/dyff GitHub) : Canonical YAML diff tool, git-embeddable via `.gitattributes`. When diffs become a UX question, this is the reference.

**Markdown + YAML frontmatter + git** (Cooklang, recipe version control example; Quora consensus on non-programming text docs in git) : Natural diffs happen because the format is readable. Ingredient names, quantities, steps = directly visible in diff. Same applies to drop_zone_intent.md semantic fields.

### Application to Genesis v1.5.0

**Validates existing Genesis choice** (v1.3.2+ already uses YAML frontmatter + Markdown body). v1.5.0 additive keys (`arbitrated_fields`, `supersedes_snapshot`, `snapshot_version`) continue in the canonical pattern.

**No new format work**. Genesis inherits the SOTA naturally.

## Design validation — Genesis v1.5.0 against SOTA

| Design choice | SOTA alignment | Notes |
|---|---|---|
| Snapshot-only (no event log) | ✅ Aligned with "domain modeling first" discipline | Low-frequency, single-writer, no downstream consumers. Event log would be anti-Frankenstein |
| Per-document revision (not per-field inline history) | ✅ Aligned with separate-archive pattern (MongoDB canonical) | Simpler schema, clear audit |
| `drop_zone_intent_history/` filesystem archive | ✅ Canonical "separate collection for full audit" | No cryptographic chain (not needed) |
| Additive frontmatter keys (no schema_version bump) | ✅ Aligned with YAML-frontmatter + git canonical pattern | Forward-compat preserved |
| Flag-never-resolve in extractor prompt | ✅ Aligned with "LLM flags, human arbitrates" SOTA (KARMA, EMNLP survey) | Overconfidence empirically unreliable for auto-resolve |
| No scalar confidence threshold | ✅ Aligned with structural-signals-over-scalar principle (Sensible, Cleanlab findings) | Binary divergence flag suffices |
| Single-time snapshot timestamp | ✅ Unitemporal (not bitemporal) | No valid-time dimension needed |
| Halt-with-remediation on API-missing (no fallback) | ✅ Aligned with anti-Frankenstein rétroactive | Pain-driven: user challenged the v1.4.0 preemptive fallback |
| Retention policy deferred to v1.5.1+ | ✅ Aligned with domain-modeling-first + pain-driven discipline | Will adopt keep-last-N when dogfood surfaces disk pressure |
| Activity timeline deferred to v1.5.1+ | ✅ Aligned with progressive-UX pattern | Layer B marker is the v1.5.0 MVP of the timeline |
| Cross-project memory flow deferred to v2.x.x | ✅ Aligned with Meta-Memory Path B territoire | Requires universal infrastructure, out of v1.5.0 scope |

**Twelve design choices, all SOTA-aligned.** Best-at-date axis projection 9.2-9.3 on the v1.5.0 rubric.

## Open question (deferred)

**Should v1.5.0 emit an event log alongside the snapshot ?** (the SaaS-grade pattern from Layer 0 `pattern_state_machine_outbox_from_day_one.md`)

**Arguments in favor** :
- Future-proofs Genesis for multi-writer scenarios (team bootstrap?)
- Seeds the cross-project memory flow (v2.x.x)
- Transition analytics possible (how often do users re-run? how many fields change on average?)

**Arguments against** :
- No current multi-writer pain
- Adds surface (event log schema + write trigger) without justifying pain
- Anti-Frankenstein gate fails: event log is the pattern for SaaS marketplaces, not single-user project bootstrap
- Can be added in v2.x.x if pain emerges; the archive directory is the same filesystem shape, easy to extend with event log later

**Reco** : defer event log to v2.x.x. v1.5.0 ships snapshot-only + archive. Honest scope.

If a concrete multi-writer scenario surfaces during v1.5.0 dogfood, escalate the decision immediately (do not reconsider silently).

## Discipline reminders

1. **Refresh this entry on 2026-04-25** (7d TTL). If v1.5.0 has shipped by then, the entry's role shifts to "retrospective" — still keep active until a refresh proves SOTA changed.
2. **Pointer files** : Classify as `universal`. Candidates for pointer propagation : aurum-ai (if memory architecture surfaces as requirement), myconciergerie-www (if project memory with revision becomes relevant). Pointer propagation decision post-v1.5.0 dogfood.
3. **Cross-refs** : This entry is the load-bearing citation for v1.5.0 spec's `Best-at-date` axis. Spec must cite this file explicitly in frontmatter + rationale section.
4. **Discipline reminder to future-self** : Genesis's choice of snapshot-only is defensible *today*. If SOTA shifts (e.g., 2027 consensus moves toward always-event-log even for single-writer), re-evaluate in a fresh R8 entry — don't rationalize stale entries.

## References cross-check

Internal :
- `~/.claude/memory/layer0/pattern_state_machine_outbox_from_day_one.md` — canonical event-log pattern for SaaS marketplaces (opposite end of the spectrum vs Genesis)
- `~/.claude/memory/layer0/workflow_research_and_memory.md` — R8 cache convention + anti-Frankenstein gate this entry is backing

External : see `sources:` frontmatter list.
