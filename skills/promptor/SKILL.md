<!-- SPDX-License-Identifier: MIT -->
---
name: promptor
description: 'Production-grade system-prompt template for the Anthropic ecosystem (Claude Opus 4.7 1M + MCP protocol). Two-phase operating mode (standby acquisition + creation), structured output (inference params + XML payload + edge cases + env vars), KV-cache optimized. Invoke when the user asks (verbatim binding-rule triggers) - "aide-moi à écrire / drafter / rédiger un prompt pour [Claude / opus / sonnet / haiku / claude api / anthropic]" - "architecture / architecte un prompt production-grade pour [use case]" - "optimise ce prompt pour KV cache / Context Caching / cache_control / prompt caching" - "reverse-engineere / reverse-engineer un prompt optimal pour [tâche stricte]" - or implicitly when about to write/modify any LLM prompt destined for an Anthropic-first project (extractor system prompts, agent personas, structured-output coercion). Audience: senior AI engineers, ML architects, researchers — peer-to-peer staff-engineer tone, density over clarity. Skip when audience is non-technical, prompt is trivial one-shot, or context is non-Anthropic.'
---

# Promptor — Anthropic prompt engineering template

This skill is a **1:1 mirror** of the Layer 0 pépite at
`~/.claude/memory/layer0/pepite_promptor_template_anthropic_prompt_engineering.md`.
This skill is the **canonical source of truth** ; the Layer 0 pépite is a synced
cache for sessions outside Genesis-bootstrapped projects (where this skill is not
installed). **Last sync: v1.6.0 @ 2026-04-19.** Drift between this skill and the
pépite is a merge-blocker — content edits land here first, then propagate to the
Layer 0 cache via the convention documented in the spec.

## When to invoke

**Explicit triggers** — any of these user phrases :

- "aide-moi à écrire / drafter / rédiger un prompt pour [Claude / opus / sonnet / haiku / claude api / anthropic]"
- "architecture / architecte un prompt production-grade pour [use case]"
- "optimise ce prompt pour KV cache / Context Caching / cache_control / prompt caching"
- "reverse-engineere / reverse-engineer un prompt optimal pour [tâche stricte]"

**Implicit triggers** — invoke even without explicit user request when :

- About to write or modify a runtime LLM prompt inside any Anthropic-first project
  (extractor system prompts, arbitration prompts, agent personas, structured-output
  coercion prompts)
- Reviewing or refactoring an existing Anthropic prompt where structure / KV-cache /
  failure modes / env-var discipline could be tightened

## When NOT to invoke

- **Non-technical / non-engineer user** — vulgarisation banned by template, incompatible
  with audience
- **Trivial one-shot prompt** — template assumes production context, surkill otherwise
- **Exploratory / brainstorm phase** before specs are clear — use `superpowers:brainstorming`
  skill first
- **Non-Anthropic context** (OpenAI / Gemini / local models) — calibrage MCP + KV-cache
  optimization is Anthropic-specific ; principles transfer conceptually but adapt the
  template

## Two-phase operating mode (high-level)

1. **Phase 1 standby** — acquire technical specs of the target. Render the standby
   card from `references/template.md` § "Phase 1 standby output", halt awaiting
   engineer specs. Generate NOTHING beyond the standby card.
2. **Phase 2 creation** — once specs in hand, render Parts A/B/C/D per the canonical
   XML in `references/template.md`. Observe global constraints (zero intro, zero
   outro, density over clarity, semantic XML + rigorous Markdown, peer-to-peer
   staff-engineer tone).

The full canonical XML lives in `references/template.md`. Read it in Phase 2 ;
this `SKILL.md` is the gate for Phase 1.

## Adaptation discipline

When adapting the template for a specific use case :

- **Adjust `<role>`** — replace "Promptor" + "Agent Expert" by domain-fit persona
  (e.g. "Data Engineer Expert SQL", "Security Researcher", "Legal Contract Drafter")
- **Keep the `<phase_*>` gates** — the discipline acquisition-before-creation is
  universal, do not dilute it
- **Adapt `<output_structure>`** — Parts A/B/C/D are modular ; replace by what makes
  sense for the domain (e.g. "Vectorisation strategy" instead of "MCP tools schemas"
  for a RAG pipeline)
- **Preserve `<global_constraints>` on tone + noise** — this is the heart of the
  audience-calibration

See `references/template.md` § "Adaptation points" for fuller guidance.

## Source of truth

This skill is canonical. The Layer 0 pépite at
`~/.claude/memory/layer0/pepite_promptor_template_anthropic_prompt_engineering.md`
is a synced cache, kept in lock-step via the manual sync convention documented in
the v1.6.0 spec. If you find drift between the two, the skill wins ; update the
pépite to match.
