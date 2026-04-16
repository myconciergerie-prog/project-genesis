<!-- SPDX-License-Identifier: MIT -->
---
name: v2 Promptor fusion — 2026 landscape research
description: Three-agent parallel research on drag-drop UX, document extraction, and conversational briefing patterns. Gathered during v1.2.0 self-dogfood to inform the v2 drag-drop → extract → formalize surface.
type: research-sota
scope: project-specific
created_at: 2026-04-17
expires_at: 2026-04-24
sources_verified: true
---

# v2 Promptor fusion — 2026 landscape (three-agent research)

Collected 2026-04-17 during the v1.2.0 self-dogfood session. Three agents ran in parallel. Summary organized by the three pipeline stages of v2: **drop → extract → formalize**.

---

## STAGE 1 — Drop zone UX (boomer-friendly)

**Gold-standard 2026 pattern**: intent-first *unified* box. No "pick a file type" dialog. Prompt + files + URLs all land in the same zone. Verified across v0.app / Bolt.new / Lovable ([NxCode comparison](https://www.nxcode.io/resources/news/v0-vs-bolt-vs-lovable-ai-app-builder-comparison-2025)).

**Micro-interactions for Victor** (77-year-old, non-technical):
- Elevation signalling (shadow/tilt on grab, Trello-style)
- Magnetic snap (100 ms animation into final slot)
- Center-out reshuffling, not edge
- Drop zone scales 1.02× on hover, dotted → solid border
- **Dual-path rule**: drag-drop AND a visible "Browse files" button. Always. ([Filestack](https://blog.filestack.com/file-upload-ui-for-non-technical-users/))

**Accept-anything norm**: IBM Docling set the 2026 bar — PDF / DOCX / PPTX / XLSX / HTML / images / audio → unified DoclingDocument. Users should never pick a parser. Expected drop-zone inputs now include **paste-in URLs and Figma/Notion links** as first-class citizens.

**Three failure modes that alienate non-tech users**:
| Failure | Counter-pattern |
|---|---|
| Invisible focus states + icon-only buttons | Keyboard-reachable everything, text label beside every icon, `aria-live="polite"` status |
| Error codes / jargon ("Upload failed") | "Le fichier est trop gros. Max 2 Mo — essaie une image plus petite" |
| Silent processing | Real-time progress bar + filename echo + checkmark confirmation |

**The processing moment — anti-freeze pattern**: token-streamed *acknowledgement* is the 2026 norm. Surface partial extraction live — "Je vois un brief pour une boulangerie à Lyon, 3 photos produits, et une note de budget" — rather than a spinner ([Ably AI UX](https://ably.com/blog/token-streaming-for-ai-ux)).

**Privacy signal — relationship language, not compliance**: not "processed locally" but **"Tes fichiers restent avec toi pendant cette session"** ([MIT Tech Review, Apr 2026](https://www.technologyreview.com/2026/04/15/1135530/building-trust-in-the-ai-era-with-privacy-led-ux/)).

---

## STAGE 2 — Document extraction (Claude API, April 2026)

### Files API + PDF + Vision (the ingestion spine)

- **Files API** beta header `anthropic-beta: files-api-2025-04-14`. Create-once / use-many. 500 MB/file, 500 GB/org. File ops free, only tokens billed on use. ([docs](https://platform.claude.com/docs/en/build-with-claude/files))
- **PDF**: URL / base64 / `file_id`. 32 MB, 600 pages per request (100 on 200k-context models). Each page rendered as both text AND image → charts/tables/diagrams/handwriting seen via vision. ([docs](https://platform.claude.com/docs/en/build-with-claude/pdf-support))
- **Vision for sketches/handwriting**: built into every Claude 3+ model. Cited +15% vs traditional OCR on medical records.

### Structured Outputs (GA early 2026) — the extraction idiom

- `output_config.format` with `type: "json_schema"`. Guaranteed schema-valid JSON. Supported on Opus 4.7 / 4.6 / Sonnet 4.6 / Haiku 4.5. No beta header. First request compiles grammar (small latency hit), cached 24 h.
- SDK: Python `messages.parse()` with Pydantic, TS `parse()` with Zod. **Pydantic-as-schema is the native 2026 idiom**, not a wrapper pattern.
- Limits: 20 strict tools, 24 optional params, 16 union-type params.
- ([docs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs))

### Citations (GA, production-grade)

- `citations: {enabled: true}` per `document` block, all-or-none per request.
- Three doc types: plain text (char-index, 0-indexed), PDF (page-range, 1-indexed), custom content (block-index).
- Response interleaves `text` with `citations[]` carrying `cited_text` (not billed as output tokens) + `document_index` + location.
- Streams via `citations_delta` events. Works with caching, token counting, batch. ZDR-eligible.
- ([docs](https://platform.claude.com/docs/en/build-with-claude/citations))

### ⚠️ Load-bearing incompatibility

**Structured Outputs and Citations are mutually exclusive** — API returns 400 if both set. This forces a v2 architectural choice:

| Path | Use when |
|---|---|
| **A. Audit-first (Citations)** | Promptor needs to show "I got this from page 3 of your brief" |
| **B. Schema-first (Structured Outputs)** | Promptor outputs a clean JSON that the protocol engine consumes directly |

Both paths cache documents via prompt caching; choose one.

### Multi-file synthesis idiom

- Place `document` blocks **before** text prompt. Nest as `<documents><document index="1">…</document></documents>` or use Files-API content blocks with `title` + `context` metadata.
- Cross-reference prompt pattern: *"For each field in the target schema, prefer the source in priority order: transcript > brief > sketch. Flag conflicts in a `contradictions[]` array."*
- One call handles extraction + contradiction detection — no second pass.

### Prompt caching — Promptor-optimal

- TTLs: 5-min (default, 1.25× base write) OR 1h (2× base write). Reads 0.1× base either way. Up to 4 cache breakpoints per request.
- Promptor pattern: documents + extraction system prompt behind one `cache_control: {type: "ephemeral", ttl: "1h"}` breakpoint. Conversational follow-ups ("confirm extracted fields") fire multiple queries against that cached prefix.
- Break-even: ~5 queries on 5-min TTL, ~10 on 1h.
- ⚠️ **Cache TTL regression Apr 2026**: Anthropic silently tightened default from 1h → 5m around March 2026. **Explicit `ttl: "1h"` is now mandatory** — don't rely on defaults. ([issue #46829](https://github.com/anthropics/claude-code/issues/46829))

### Verification (three 2026 patterns, ranked)

1. **Citations as verification** — preferred when incompatibility allows. Add `source_citation` to each field in schema. Audit-trail by construction. Evaluated more reliable than prompt-based quote extraction.
2. **Chain-of-Verification (CoVe)** — second pass, *"For each field, quote the source. Flag fields with no direct support."* Rule: verification call must NOT see draft as conditioning or hallucinations copy through. ([explainer](https://moazharu.medium.com/chain-of-verification-the-prompting-pattern-that-makes-llm-answers-check-themselves-f9563ea9e960))
3. **Reflection / self-contrast** — Reasoner-Critic pair. Overkill for project-brief extraction.

### Recommended stack for v2 Promptor

Frankenstein-check: each layer earns its place.
- Files API for ingestion (dedup + billing hygiene)
- `claude-opus-4-7` for extraction (Sonnet 4.6 as cost fallback)
- **Choose Path A (Audit-first) for the first v2 release** — the "I see a brief for X, 3 photos, a budget note" live acknowledgement screen is Promptor's whole point. Schema-first Path B is v2.1 if a strict engine consumer emerges.
- 1h cache `ttl` on documents
- Haiku 4.5 verification call ONLY if evals show a specific failure class. Default: skip.

**Anti-patterns to avoid**:
- Structured Outputs + Citations on same call (API rejects)
- Tool-use extraction + `output_config.format` on same call (redundant, pick one)
- Stacking CoVe + reflection + multi-agent debate for project briefs (stakes don't justify)

---

## STAGE 3 — Conversational briefing / formalization

### The "Promptor" pattern — Genesis-native, not published

**Critical finding**: the 4-part structure (calibrage / prompt / auto-critique / questions) described in Genesis's v2 spec is **not documented in any public source**. "Promptor" has two distinct referents:

- **Academic Promptor** ([arXiv 2310.08101](https://arxiv.org/abs/2310.08101), Zhu et al., Oct 2023) — "conversational and autonomous prompt generation agent for intelligent text entry techniques." Abstract doesn't describe a 4-part structure.
- **Mr Promptor / FlowGPT Promptor** (French GPT Store / FlowGPT) — the likely direct inspiration. French-community GPTs that follow a calibrage-style conversational loop.

**Action**: stop citing this as "Promptor's published structure" in Genesis docs. Document it as **Genesis-native**, inspired by the FR-community pattern. This is a factual correction to the v2 spec.

### Minimum-viable-questions — EVPI is the 2026 SOTA

Moving away from fixed question counts toward **Expected Value of Perfect Information**:

- Confidence bands: >90% → answer, 60–90% → clarify with caveat, <60% → escalate ([Maven AGI](https://www.mavenagi.com/glossary/ai-confidence-score))
- Fixed thresholds **degrade perf 1–3 points** and ask 0.2–0.4 more questions than needed ([arXiv 2511.08798](https://arxiv.org/html/2511.08798v2), [arXiv 2603.26233](https://arxiv.org/html/2603.26233v1))
- Amazon Science: unnecessary clarification is the **#1 complaint driver** for voice agents

Tool landscape:
| Tool | Questions before build |
|---|---|
| Bolt.new, v0.app, Artifacts | 0 |
| Lovable | 0–1 |
| Replit Agent Plan Mode | 2–3 specific (DB? auth? what happens when X?) |
| Cursor/Claude Code Skills | As-needed, EVPI-style |

**Verdict**: Genesis's "at most 3" aligns with Replit, beats v0/Bolt by offering the power-user branch. **Don't add a 4th question** — degradation kicks in fast.

### Adaptive tone — system prompt, not framework

- Done via **in-context style mirroring**. Claude/GPT-5.2 natively match register from first message.
- @clack/prompts does NOT do tone adaptation — pure structural layer. Genesis correctly places tone adaptation in the LLM, not the CLI framework.
- SOTA prompt: *"Match the user's register: casual FR → warm + no jargon; technical EN → crisp + precise. Mirror sentence length within ±30%."*
- ⚠️ [PersonaMail (arXiv 2602.17340)](https://arxiv.org/html/2602.17340v1) warns AI writing flattens linguistic diversity unless a Factors Exploration Panel is used. One-line system-prompt directive suffices for v2.

### Brief-quality rubric — ResearchRubrics (2026 SOTA)

[Scale AI ResearchRubrics (arXiv 2511.07685)](https://arxiv.org/html/2511.07685v1) — 2,500+ expert rubrics, 6 axes:
1. Explicit requirements
2. Implicit requirements
3. Synthesis
4. References
5. Communication quality
6. Instruction following

Tasks annotated with (Breadth, Depth, **Ambiguity**) triplets — the Ambiguity axis maps to "is the brief ready?" Mandatory vs optional criteria split matches "missing fields" vs "over-specification".

**For Genesis**: a 6-axis mini-rubric checked silently before showing the mirror — slug derivable? vision unambiguous? plugin-flag implied? license default applicable? plan-tier detected? meta-question resolved? **Full 5-star loop is over-engineering** for a 3-question bootstrap. Single pass / iterate / stop trichotomy (already in spec) is enough.

### Iteration pattern — subtractive editing beats additive Q&A

[Jakob Nielsen: Intent by Discovery](https://jakobnielsenphd.substack.com/p/intent-ux) — "generate an overwhelming maximalist version, let user delete — infinitely easier than generating from a blank screen." This is Bolt/v0's model.

[Raisini](https://raisini.substack.com/p/why-most-people-struggle-to-articulate) grounds it in cognitive-load asymmetry: recognition > recall. **Genesis's Étape 2 mirror is correctly placed.**

### The meta-question — binary, not trinary

Close relatives in 2026 UX canon:
- Smart Defaults + Progressive Disclosure ([NN/g](https://www.nngroup.com/articles/the-power-of-defaults/))
- Predictive vs Reactive UX ([Groovyweb 2026](https://www.groovyweb.co/blog/ui-vs-ux-ai-apps-2026))
- Cursor: Agent / Ask / Manual selector
- Replit Agent: Plan Mode vs Agent Mode
- Claude Code itself: `/plan` vs direct execution

**Verdict**: Genesis's "Tu veux que je décide tout, ou tu préfères choisir ?" is the correct 2026 pattern. **Keep it binary.** Every tool that tried a hybrid third mode (Warp's early agent, v0 v3 beta) collapsed back to binary within a release.

---

## Over-engineering flags for v2 implementation

1. **5-star auto-critique loop** — ResearchRubrics 6-axis pass/fail is enough. Star rating adds ceremony without signal for 3-question bootstrap.
2. **"Promptor 4-part published structure"** — not published. Document as Genesis-native.
3. **Third mode in the meta-question** — every tool that tried it reverted. Keep binary.
4. **Tone adaptation as a separate module** — belongs in the system prompt.

---

## Synthesis for Genesis v2 roadmap

**The drop-zone architecture (NEW in this research)**:

```
┌────────────────────────────────────────────────────┐
│  [Box]  Dépose ici ton idée.                       │
│         Un texte, un PDF, une photo, un lien —     │
│         tout est bienvenu.                         │
│                                                    │
│         (ou: Parcourir les fichiers)               │
└────────────────────────────────────────────────────┘
           ↓ (token-streamed acknowledgement)
   "Je vois un brief pour X, une photo Y, une note Z"
           ↓ (Claude: Files API + Citations + 1h cache)
   Structured brief (Path A: Citations-audited)
           ↓ (ResearchRubrics 6-axis silent check)
   [Mirror] "Voilà ce que j'ai compris : …"
           ↓ (at most 3 EVPI-selected questions)
   [Genesis v1 engine: the 7 phases]
           ↓
   Projet sur GitHub, chime.
```

**What this changes in the v2 spec**:
1. Add a NEW Étape 0 — "Le Dépôt" (drop zone) — before Étape 1 "L'Étincelle".
2. Correct the "Promptor 4-part structure" section to say "Genesis-native, inspired by FR-community GPT patterns."
3. Replace fixed "at most 3 questions" with "EVPI-selected questions, typically 0–3."
4. Keep binary meta-question. Drop any mention of a third "hybrid" mode.
5. Document the Citations-vs-Structured-Outputs choice explicitly; recommend Path A for v2.0.
6. Mandate `ttl: "1h"` on prompt caching — explicit, not defaulted.

---

## Sources (all URLs verified by agents)

See individual stage sections above. Primary sources:
- [Anthropic Files API](https://platform.claude.com/docs/en/build-with-claude/files)
- [Anthropic Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- [Anthropic Citations](https://platform.claude.com/docs/en/build-with-claude/citations)
- [Anthropic Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [NxCode 2026 vibe-design comparison](https://www.nxcode.io/resources/news/v0-vs-bolt-vs-lovable-ai-app-builder-comparison-2025)
- [Smart Interface Design Patterns — drag-and-drop](https://smart-interface-design-patterns.com/articles/drag-and-drop-ux/)
- [Ably AI UX token streaming](https://ably.com/blog/token-streaming-for-ai-ux)
- [ResearchRubrics Scale AI](https://arxiv.org/html/2511.07685v1)
- [Structured Uncertainty guided Clarification (arXiv 2511.08798)](https://arxiv.org/html/2511.08798v2)
- [Jakob Nielsen — Intent by Discovery](https://jakobnielsenphd.substack.com/p/intent-ux)
- [MIT Tech Review — Privacy-led UX, Apr 2026](https://www.technologyreview.com/2026/04/15/1135530/building-trust-in-the-ai-era-with-privacy-led-ux/)
