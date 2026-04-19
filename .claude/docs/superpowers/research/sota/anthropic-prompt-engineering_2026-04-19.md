<!-- SPDX-License-Identifier: MIT -->
---
name: Anthropic prompt-engineering SOTA — April 2026
description: Canonical sources for prompt-engineering Claude Opus 4.7 1M — XML structuring, prompt caching with 5m/1h TTL, MCP tool description craft, long-context placement, SKILL.md discovery. Grounds Project Genesis v1.6.0 Promptor skill against current Anthropic guidance.
type: sota
created: 2026-04-19
expires: 2026-04-26
confidence: high
---

# Anthropic prompt-engineering SOTA — April 2026

**Commissioned by:** Project Genesis v1.6.1 to close the 8.7/10 best-at-date cap on the v1.6.0 Promptor skill self-rating (no R8 entry backed the template choices).

**Method:** WebSearch breadth (6 queries, April 2026) → WebFetch depth on 4 load-bearing canonical pages (`platform.claude.com` prompt-engineering, prompt-caching, XML-tags, agent-skills best-practices) + 2 community sources (Simon Willison 2026-04-18, claudefa.st). All claims cited inline.

---

## TL;DR

- **Opus 4.7 interprets prompts more literally than 4.6** — state scope explicitly ("every section, not just the first"), do not rely on implicit generalization. ([Anthropic, prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices))
- **Prefill responses are deprecated** starting with 4.6 models and return 400 on Mythos Preview — migrate to structured outputs, direct system-prompt instructions, or tool calling. (ibid.)
- **Adaptive thinking (`thinking: {type: "adaptive"}`) replaces extended thinking with `budget_tokens`** on 4.6/4.7 — use the `effort` parameter (`low | medium | high | xhigh | max`) as the new budget knob. `xhigh` is the new recommended default for coding and agentic work. (ibid.)
- **Sampling parameters removed on 4.7** — `temperature`, `top_p`, `top_k` set to any non-default value return 400 errors ; safest migration is to omit them entirely. ([Anthropic migration guide, canonical](https://platform.claude.com/docs/en/about-claude/models/migrating-to-claude-4) — "Setting `temperature`, `top_p`, or `top_k` to any non-default value on Claude Opus 4.7 returns a 400 error")
- **Cache breakpoint placement rule**: put `cache_control` on the *last block that stays identical across requests*, never on per-request dynamic content (e.g., timestamped queries). Max 4 breakpoints per request. ([Anthropic, prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching))
- **Opus 4.7 minimum cacheable prefix = 4,096 tokens** (up from 1,024 on Opus 4 / Sonnet 4.5). Below that, cache silently no-ops — check `usage.cache_creation_input_tokens`. (ibid.)
- **Canonical cache order is `tools → system → messages`** — any change at a level invalidates that level and all following levels. (ibid.)
- **XML tags > Markdown** when prompts mix instructions, context, examples, and variable inputs. Tags Claude is effectively trained on: `<example>`, `<examples>`, `<document>`, `<document_content>`, `<source>`, `<instructions>`, `<context>`, `<input>`, `<thinking>`, `<answer>`. Nest when there is natural hierarchy. (ibid., [XML tags doc](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags))
- **Long-context placement rule**: put long-form data *at the top*, query/instructions *at the bottom* — improves response quality up to 30% on complex multi-document inputs. Critical info in the middle degrades. ([Anthropic, context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows); [Anthropic research](https://www.anthropic.com/research/prompting-long-context))

---

## Findings

### 1. Anthropic guidance for Claude Opus 4.7 (April 2026)

**Literal instruction following (the biggest 4.7 behavioral shift).**
> "Claude Opus 4.7 interprets prompts more literally and explicitly than Claude Opus 4.6, particularly at lower effort levels. It will not silently generalize an instruction from one item to another, and it will not infer requests you didn't make."
> ([Anthropic prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices))

Consequence: state scope (`"Apply this formatting to every section, not just the first one"`), success criteria, and constraints upfront in the *first* user turn. Progressive reveal across turns degrades token efficiency and sometimes performance. (ibid.)

**Effort parameter is the new primary lever.**
- `max` — diminishing returns, prone to overthinking, test before using
- `xhigh` (new in 4.7) — recommended default for coding and agentic use cases
- `high` — minimum for intelligence-sensitive work
- `medium` / `low` — cost-sensitive, latency-critical; 4.7 respects these strictly ("at low and medium, the model scopes its work to what was asked rather than going above and beyond")
  (ibid.)

> "We expect effort to be more important for this model than for any prior Opus."
  (ibid.)

**Adaptive thinking replaces extended thinking.** `thinking: {type: "adaptive"}` + `output_config: {"effort": "high"}` is the current canonical form. `budget_tokens` is deprecated but still functional on 4.6/4.7. Thinking is off by default when `thinking` is omitted. (ibid.)

**Tool-use triggering is more conservative.**
> "Claude Opus 4.7 has a tendency to use tools less often than Claude Opus 4.6 and to use reasoning more."
  (ibid.)

If more tool use is desired, raise effort or prompt explicitly. Anti-pattern: aggressive "CRITICAL: You MUST use this tool" language — 4.6+ is more responsive to system prompts so this now *overtriggers*. Dial down to "Use this tool when…". (ibid.)

**Subagent spawning reduced by default.** Opus 4.7 spawns fewer subagents than 4.6. Give explicit guidance around when subagents are desirable. (ibid.)

**Tone shift.**
> "Claude Opus 4.7 is more direct and opinionated, with less validation-forward phrasing and fewer emoji than Claude Opus 4.6's warmer style."
  (ibid.)

If product voice is warmer, state it explicitly.

**Verbosity is task-calibrated.** 4.7 calibrates response length to judged task complexity — no fixed default verbosity. To reduce: "Provide concise, focused responses. Skip non-essential context, and keep examples minimal." **Positive examples beat negative instructions** for style control. (ibid.)

**Prefill is deprecated.** On Mythos Preview, prefilled assistant-last-turn messages return 400. Migration path: structured outputs feature, direct system-prompt instruction, tools with enum, or post-processing strip. (ibid.)

**Sampling parameter removal on 4.7.** `temperature`, `top_p`, `top_k` set to any non-default value return 400 errors. Migration path = omit entirely from request payloads ; use prompting to guide behavior. ([Anthropic migration guide, canonical](https://platform.claude.com/docs/en/about-claude/models/migrating-to-claude-4))

**Extended thinking removed on 4.7.** `thinking: {type: "enabled", budget_tokens: N}` returns 400. Replacement : `thinking: {type: "adaptive"}` + `output_config: {"effort": "high|xhigh|max|medium|low"}`. Adaptive thinking is **off by default** on Opus 4.7 — omitting the `thinking` field runs without thinking (matching Opus 4.6 behavior). (ibid.)

**Thinking content omitted by default on 4.7.** Thinking blocks appear in response stream but `thinking` field is empty unless explicitly opted in. To restore summarized thinking : `thinking: {type: "adaptive", display: "summarized"}`. Default `display` = `"omitted"`. (ibid.)

**Tokenizer change on 4.7.** New tokenizer uses ~1x-1.35x more tokens for same text vs Opus 4.6. `/v1/messages/count_tokens` returns different numbers. Re-tune `max_tokens` and re-baseline costs. (ibid.)

**Task budgets (beta) new in 4.7.** Beta header `task-budgets-2026-03-13` + `output_config.task_budget = {type: "tokens", total: N}` (min 20k). Advisory cap the model sees across full agentic loop (thinking + tool calls + output) ; different from `max_tokens` which is a hard per-request ceiling not passed to model. Use `task_budget` when wanting model self-moderation ; reserve omission for open-ended agentic tasks where quality > speed. (ibid.)

**System prompt changes 4.6 → 4.7** (community reverse-engineered): new `<acting_vs_clarifying>` block encouraging proactive action, new `tool_search` capability for deferred tools, expanded `<critical_child_safety_instructions>`. Tone shift toward less pushy language ("Claude does not request that the user stay"). ([Simon Willison, 2026-04-18](https://simonwillison.net/2026/Apr/18/opus-system-prompt/), community-derived)

---

### 2. Prompt caching — cache_control, ephemeral, TTL

**Canonical syntax** ([Anthropic prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)):

```json
{"cache_control": {"type": "ephemeral", "ttl": "1h"}}
```

`"ephemeral"` is the only supported type. `ttl` defaults to `"5m"`.

**Pricing multipliers on base input:**
- 5m cache write: **1.25×**
- 1h cache write: **2×**
- Cache read: **0.1×** (10 % — significant)

**TTL decision rule:**
- **5m** — prompts reused more often than every 5 min; auto-refresh is *free* on hit within window.
- **1h** — agentic side-agents >5 min, long chat sessions where user turns exceed 5 min, latency-critical infrequent queries. Cache hits *do not count against rate limits*.

**Cache breakpoint placement (load-bearing rule):**
> "Place `cache_control` on the last block that stays identical across requests."
  (ibid.)

Anti-pattern: putting the breakpoint on a block containing a per-request timestamp or user input — hash never matches, miss every request.

**Lookback window: 20 positions per breakpoint.** If conversation grows beyond 20 blocks since last cache write, add a second breakpoint closer to current tail to prevent window gap.

**Ordering is strict:** `tools → system → messages`. Changes at level N invalidate level N and all following. Matrix (selected): tool def change invalidates all; tool_choice change invalidates system+messages; images add/remove invalidates messages; thinking params change invalidates messages.

**Minimum cacheable prefix by model** (critical for Opus 4.7):

| Model | Min tokens |
|---|---|
| **Claude Opus 4.7, 4.6, 4.5** | **4,096** |
| Claude Sonnet 4.6 | 2,048 |
| Claude Sonnet 4.5 / 4 / 3.7 | 1,024 |
| Claude Opus 4.1 / 4 | 1,024 |
| Claude Haiku 4.5 | 4,096 |

Below minimum → cache silently no-ops. Verify via `usage.cache_creation_input_tokens` and `cache_read_input_tokens`.

**Max 4 cache breakpoints per request.** Common layout: tools breakpoint + system stable-prefix breakpoint + system dynamic-context breakpoint + last-user-message breakpoint.

**Thinking blocks + cache composition:**
> "Thinking blocks cannot be directly marked with `cache_control`, but they are cached alongside other content in subsequent requests with tool results […] When non-tool-result user content is added, all previous thinking blocks are removed from the cache."
  (ibid.)

Consequence: thinking blocks survive across turns *only* while the conversation continues through tool-result user turns. A plain user text turn evicts all prior thinking from the cache.

**Mixed TTL rule:** 1h entries must precede 5m entries in block order. Billing proceeds in three positions: last hit → highest 1h after hit → last breakpoint. (ibid.)

**Hit-rate optimization (ordered priority):**
1. Automatic caching (set `cache_control` at top level) for multi-turn conversations
2. Cache stable content first: tool defs → system instructions → static context
3. Structure prompts so static prefix ≥ 4,096 tokens on Opus
4. Avoid cache invalidators (tool_choice toggles, image add/remove, web-search toggle)
5. Monitor `cache_read_input_tokens / (cache_read + cache_creation)` ratio

---

### 3. MCP server integration patterns

**Tool naming convention.** Canonical pattern: `mcp__<server-name>__<tool-name>` at runtime. Survey of first 100 MCP servers: >90 % snake_case, ~95 % multi-word, <1 % camelCase. ([zazencodes.com, MCP naming](https://zazencodes.com/blog/mcp-server-naming-conventions), community-derived; [Anthropic MCP docs](https://platform.claude.com/docs/en/agent-sdk/mcp))

**Fully qualified tool references in skills.** Skill authoring docs mandate: in SKILL.md, reference MCP tools with `ServerName:tool_name` form (e.g. `BigQuery:bigquery_schema`, `GitHub:create_issue`). Without server prefix, Claude may fail to locate the tool when multiple MCP servers are loaded. ([Anthropic skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices))

**Tool description density matters more than tool count.**
> "Claude reads tool descriptions and uses them to decide which tool to call for a given task, which is why tool descriptions in MCP servers matter so much." […] "If Claude is connected to the server but not using its tools, the issue is usually that the tool descriptions don't clearly signal when they should be used."
  ([builder.io MCP guide](https://www.builder.io/blog/claude-code-mcp-servers), community-derived)

**Narrow responsibility rule.**
> "Design clear tool definitions with explicit names, narrow responsibilities, and predictable schemas. If one tool does five things, Claude infers too much. Good integrations are boring — each tool does one thing cleanly."
  (ibid., community-derived)

**MCP resources vs tool results.** Tools = executable verbs (side effects / compute), resources = addressable read-only content. Prefer MCP resources for static / frequently-reused large context (they integrate with cache more naturally than tool-result messages which invalidate thinking blocks). ([Anthropic MCP docs](https://platform.claude.com/docs/en/agent-sdk/mcp))

**Server instructions field** becomes more useful with Tool Search enabled — helps Claude know when to search for the server's tools, analogous to skill descriptions. (ibid.)

---

### 4. KV-cache / long-context patterns for Opus 1M

**Models with 1M context (April 2026):** Claude Opus 4.7, Opus 4.6, Sonnet 4.6, Mythos Preview. ([Anthropic context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows))

**Retrieval accuracy at 1M:** Opus 4.6 scored 78.3 % on MRCR v2 at full 1M token context. ([Anthropic context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows))

**Context rot is real.** As tokens grow, accuracy and recall degrade; critical info in the *middle* suffers most. (ibid.)

**Placement rule (load-bearing):**
> "Put longform data at the top: place your long documents and inputs near the top of your prompt, above your query, instructions, and examples. […] Queries at the end can improve response quality by up to 30% in tests, especially with complex, multi-document inputs."
  ([Anthropic prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices))

**Document-tagging pattern for multi-document inputs** (canonical form):

```xml
<documents>
  <document index="1">
    <source>annual_report_2023.pdf</source>
    <document_content>
      {{ANNUAL_REPORT}}
    </document_content>
  </document>
</documents>
```

**Grounding-in-quotes pattern.** Ask Claude to emit `<quotes>` from the documents *before* reasoning, then produce final answer. Cuts through noise in long context. (ibid.)

**Context awareness (4.5+, including 4.7).** The model tracks its own token budget. In agent harnesses with compaction, inject explicit guidance ("context window will be automatically compacted […] do not stop tasks early due to token budget concerns") or the model may wrap up prematurely. (ibid.)

**Historical benchmark** (Claude 2.1, still instructive): adding `"Here is the most relevant sentence in the context:"` to response start raised score 27 % → 98 % on a single-needle eval. ([Anthropic long-context research](https://www.anthropic.com/research/prompting-long-context)) — Illustrates that *prompting can matter more than raw model capability* for long-context retrieval.

---

### 5. Skill discovery, SKILL.md frontmatter, pinning conventions

**Required frontmatter fields** ([Anthropic skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)):
- `name` — max 64 chars, lowercase letters/numbers/hyphens only, no XML tags, **forbidden reserved words: `anthropic`, `claude`**
- `description` — max 1024 chars, non-empty, no XML tags

**Description is the primary discovery signal.**
> "The system loads only the minimal metadata (skill names and descriptions from frontmatter) into Claude's initial context […] The full skill prompt loads only after Claude makes that selection."
  (ibid.)

Rule: description must contain both *what* the skill does and *when* to use it (explicit trigger contexts + key terms).

**Third person mandatory.**
> "Always write in third person. The description is injected into the system prompt, and inconsistent point-of-view can cause discovery problems."
> ✓ `"Processes Excel files and generates reports"`
> ✗ `"I can help you process Excel files"`
> ✗ `"You can use this to process Excel files"`
  (ibid.)

**Under-triggering is the dominant failure mode.**
> "Currently Claude has a tendency to 'undertrigger' skills — to not use them when they'd be useful. To combat this, please make the skill descriptions a little bit 'pushy'."
  ([claude-code-best-practice, community](https://github.com/shanraisshan/claude-code-best-practice/blob/main/best-practice/claude-skills.md), community-derived)

Corollary: redundant trigger phrasing (multiple phrasings of the same trigger condition, plus both imperative and contextual forms) increases recall. Paraphrased triggers help cover variance in user phrasing; verbatim triggers anchor specific slash-command-like invocations.

**Naming convention: gerund form preferred.** Good: `processing-pdfs`, `analyzing-spreadsheets`, `writing-documentation`. Acceptable alt: `pdf-processing`, `process-pdfs`. Bad: `helper`, `utils`, `tools`, `anthropic-helper`. ([Anthropic best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices))

**Size budget.** SKILL.md body < 500 lines for optimal performance. Beyond that: progressive disclosure (move detail to `references/*.md`, keep refs *one level deep* from SKILL.md — Claude uses `head -100` on nested refs and may miss content). (ibid.)

**Pinning syntax for plugin skills** (plugin:skill form):
- Plugin-namespaced slash-command form: `plugin-name:skill-name` ([Anthropic skills docs](https://code.claude.com/docs/en/skills))
- Known friction: plugin skills defined in `skills/*/SKILL.md` load as Agent Skills (Skill-tool invocation works), but may not register as user-invocable slash commands — `/plugin-name:skill-name` can return "Unknown skill" depending on Claude Code version. ([anthropics/claude-code#34144](https://github.com/anthropics/claude-code/issues/34144), community/issue tracker)
- Workaround: `disable-model-invocation: true` in frontmatter for strictly manual slash-command skills. ([DevelopersIO, community](https://dev.classmethod.jp/en/articles/disable-model-invocation-claude-code/))

**Progressive disclosure patterns:**
1. SKILL.md as index pointing to `reference/*.md` by domain
2. Bundled scripts *executed via bash* (zero context penalty until output consumed)
3. TOC at top of any reference file > 100 lines (Claude may partial-read with `head -100`)

**Reserved-word trap.** Frontmatter `name` cannot contain `anthropic` or `claude` — silent validation failure on some loaders. ([Anthropic best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices))

**Skill discovery bug surface** (as of April 2026): frontmatter parsing is sensitive to formatting — trailing whitespace, wrong `---` markers, or BOM can cause silent discovery failure. ([anthropics/claude-code#9817](https://github.com/anthropics/claude-code/issues/9817), community/issue tracker)

---

## What this validates in the v1.6.0 Promptor template

Cross-checking the current template at `skills/promptor/references/template.md` against the findings above:

| Template choice | SOTA validation |
|---|---|
| **XML outer structure (`<system_prompt>`, `<role>`, `<operating_mode>`)** | ✅ Validated — Anthropic explicitly recommends XML when prompts mix instructions, context, examples, inputs. Tags Claude is trained on include the family the template uses. |
| **Two-phase `<phase_1_standby>` / `<phase_2_creation>` gate** | ✅ Architecturally sound — matches "specify task, intent, and constraints upfront in the first human turn" guidance for 4.7. Phase 1's explicit question-acquisition matches the "literal interpretation" shift (don't let the model infer missing specs). |
| **KV-cache static-before-dynamic ordering** (`<static_context>` + `<mcp_tools_schemas>` before `<dynamic_input>`) | ✅ Validated — matches canonical `tools → system → messages` ordering and the cache-breakpoint placement rule ("last block that stays identical"). |
| **Strict ban on vulgarisation / staff-engineer density** | ✅ Validated — Opus 4.7 is more direct by default; density matches the new tone. Positive examples > negative instructions for style control also aligns with docs. |
| **Edge-cases section (Part C)** + downstream Pydantic/Zod validation | ✅ Validated — "Report every issue you find […] your goal is coverage" recommendation and "Don't punt to Claude" pattern from skill best practices both reinforce explicit failure-mode enumeration. |
| **`{{VAR}}` placeholder discipline (Part D)** | ✅ Validated — matches Anthropic's `{{ANNUAL_REPORT}}` document-content placeholder convention in long-context examples. |
| **`stop_sequences` + explicit temperature/top_p recommendation** | ⚠ Partially validated — useful for pre-4.7 models, but **sampling parameters are removed on Claude Opus 4.7** and return 400. Template should flag that Part A parameters are model-dependent and migrate 4.7 use cases to `output_config.effort`. |
| **`Claude Opus 4.7 1M` model anchor** | ✅ Current — matches Anthropic's model identity guidance (`claude-opus-4-7`). |

**Net: 6 of 8 core architectural choices are directly validated by current Anthropic canon. 1 is architecturally sound but needs a 4.7 note, 1 is partially outdated.**

---

## What this challenges (anti-Frankenstein candidates)

Five places where SOTA evidence weakens or contradicts the template as-is. Each is a candidate for v1.6.1 template patch — but per anti-Frankenstein, we log first, surgical-patch second.

### 1. `Température, Top_P, Top_K, stop_sequences` in Part A (PARAMÈTRES D'INFERENCE & CALIBRAGE) — **broken on Opus 4.7**

Opus 4.7 removes temperature/top_p/top_k (400 error). Template currently lists them as general recommendation without model gating. ([claudefa.st](https://claudefa.st/blog/guide/development/opus-4-7-best-practices), community-derived; corroborate on Anthropic migration guide before edit)

**Suggested patch:** replace with `effort: "xhigh" | "high" | "medium" | "low"` + `thinking: {type: "adaptive"}` + `max_tokens ≥ 64k` recommendation for 4.7. Keep legacy sampling doc as a "pre-4.7 models" subsection.

### 2. Phase 1 output mentions "Claude Opus 4.7 1M" as *example* model but doesn't prompt for effort level

Given effort is "more important for this model than for any prior Opus" (Anthropic direct quote), Phase 1 question 2 should explicitly acquire effort-level preference, not just model string + temperature. Current template prompts for "température, configuration MCP/Outils" — temperature is meaningless on 4.7.

**Suggested patch:** change Q2 to acquire `(modèle cible, effort level, thinking mode, max_tokens budget, MCP tools configuration)`.

### 3. No explicit cache-breakpoint placement guidance in `<static_context>` / `<mcp_tools_schemas>`

The template encodes the ordering principle but doesn't tell the engineer where to *put* the `cache_control` marker. With Opus 4.7 min cacheable = 4,096 tokens, many smaller prompts will silently no-op.

**Suggested patch:** add a sub-directive in Part A: "If the prompt prefix (role + static_context + mcp_tools_schemas) is ≥ 4,096 tokens on Opus 4.7 (or 2,048 on Sonnet 4.6), place `cache_control: {type: ephemeral, ttl: 5m | 1h}` on the last static block. Verify with `usage.cache_creation_input_tokens ≠ 0` on first call."

### 4. Template says `<mcp_tools_schemas>` but does not prescribe the `ServerName:tool_name` reference form

Anthropic skill best-practices explicitly mandate fully qualified `ServerName:tool_name` references in authored-prompt text to avoid tool-not-found errors when multiple MCP servers load. Template does not surface this.

**Suggested patch:** add a constraint in Part A: "Tool references within `<mcp_tools_schemas>` and any prompt text MUST use fully qualified `ServerName:tool_name` form (e.g. `Supabase:execute_sql`, not bare `execute_sql`)."

### 5. Phase 1 question 1 asks for "Precision/Recall, Latence" metrics unconditionally

For non-classification / non-retrieval tasks (e.g. content generation, agentic coding), Precision/Recall is not the right axis. Template's current phrasing can anchor engineers toward the wrong metric. Minor but real.

**Suggested patch:** soften to "métriques de succès adaptées à la tâche (e.g. Precision/Recall pour classification/RAG, taux de réussite end-to-end pour agentique, latence, coût/1k tokens)".

---

## Open questions

1. **Thinking + cache composition in practice** — documented rule is "non-tool-result user content strips all prior thinking from cache". For Promptor-generated prompts that run in *pure* single-shot structured-extraction flows (no tool use, no thinking), does caching the thinking block even apply? Needs a test prompt measurement before we assert anything in the template.

2. **4.7 system-prompt dogfooding evidence** — Simon Willison's reverse-engineered observations are community-derived. No canonical Anthropic publication confirms the `<acting_vs_clarifying>` / `tool_search` blocks. Template should not encode patterns from unpublished system prompts — but they're useful for understanding 4.7's defaults.

3. **`plugin:skill` slash-command pinning status** — issue #34144 (April 2026) shows intermittent breakage. Before documenting `plugin:skill` as a reliable invocation form in the template or the genesis-protocol skill, re-check latest Claude Code release notes.

4. **1M context vs 4.7 effort interaction** — no published evidence on whether `effort: xhigh` with 1M context behaves qualitatively differently from 200k context. Could matter for Aurum-scale multi-LLM prompts.

5. **Structured outputs as prefill replacement** — canonical migration path, but template currently doesn't mention structured outputs at all. Should the "strict_output_schema" section of the template recommend `response_format: json_schema` over free-form XML schema description for production? Probably yes for data-extraction use cases; probably no for agentic system prompts where flexibility matters.

---

## Sources (canonical first, community second)

**Canonical Anthropic (load-bearing):**
- [Prompting best practices (platform.claude.com)](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Prompt caching (platform.claude.com)](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Use XML tags (platform.claude.com)](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags)
- [Agent Skills best practices (platform.claude.com)](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Context windows (platform.claude.com)](https://platform.claude.com/docs/en/build-with-claude/context-windows)
- [Connect to external tools with MCP (platform.claude.com)](https://platform.claude.com/docs/en/agent-sdk/mcp)
- [Long-context prompting (anthropic.com/research)](https://www.anthropic.com/research/prompting-long-context)
- [Extend Claude with skills (code.claude.com)](https://code.claude.com/docs/en/skills)

**Community-derived (cross-check only, marked inline):**
- [Simon Willison — Opus 4.7 system prompt changes (2026-04-18)](https://simonwillison.net/2026/Apr/18/opus-system-prompt/)
- [claudefa.st — Opus 4.7 best practices](https://claudefa.st/blog/guide/development/opus-4-7-best-practices)
- [zazencodes — MCP naming conventions](https://zazencodes.com/blog/mcp-server-naming-conventions)
- [builder.io — Claude Code MCP servers](https://www.builder.io/blog/claude-code-mcp-servers)
- [shanraisshan/claude-code-best-practice — skills guide](https://github.com/shanraisshan/claude-code-best-practice/blob/main/best-practice/claude-skills.md)
- [anthropics/claude-code#34144 — plugin slash-command issue](https://github.com/anthropics/claude-code/issues/34144)
- [anthropics/claude-code#9817 — skill frontmatter formatting sensitivity](https://github.com/anthropics/claude-code/issues/9817)
- [DevelopersIO — disable-model-invocation](https://dev.classmethod.jp/en/articles/disable-model-invocation-claude-code/)
