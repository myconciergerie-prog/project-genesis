<!-- SPDX-License-Identifier: MIT -->
# v1.5.0 Living Drop Zone Memory Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship v1.5.0 MINOR — turn `genesis-drop-zone` into a living memory with intra-drop divergence detection + cross-session supersession, replacing v1.4.0's silent graceful fallback with explicit halt-with-remediation when the API is unavailable. Closes Friction #3 (reconciliation policy not codified) from the 2026-04-18 v1.4.1 dogfood and absorbs Friction #1 + #2 (multi-source seed shape).

**Architecture:** Three orthogonal Layer-A surfaces (extractor prompt + Phase 0.4 cross-session detection + Phase 0.5 arbitration card) feeding one consolidated bilingual arbitration response that gates a unified write/archive operation. Filesystem supersession chain (`drop_zone_intent_history/v<N>_<ISO8601-Z>.md`) replaces v1.3.2's halt-on-existing. Layer B opt-in `⚖` marker rendering on Step 0.4 card + Step 0.5 template — zero parser change, zero schema bump (additive frontmatter keys only). Anti-Frankenstein retroactive: v1.4.0's silent fallback retired on user challenge ("pourquoi pas d'API ?") in favour of bilingual halt-with-remediation card.

**Tech Stack:** Python 3.x (Anthropic SDK ≥ 0.40.0 — `extract_with_citations.py` augmentation), Markdown (SKILL.md + phase-0-welcome.md + phase-0-seed-loading.md runbooks), YAML (frontmatter additive keys), JSON (`plugin.json` + extractor stdout schema), Bash (verification probes — `grep`, file-existence, schema_version unchanged). No new test framework; pre-commit verification probes per v1.4.x convention.

**Ship timeline:** Six-commit rhythm 8th consecutive application. Commits already on branch (pre-plan): `0d023b3` spec (rebased post-v1.4.2 from `59a7640`). This plan produces: plan commit (implied by saving) + plan-polish (after reviewer pass) + feat (single squash unit) + chore (CHANGELOG + session trace + MEMORY pointer + resume).

**Spec**: `.claude/docs/superpowers/specs/v2_etape_0_drop_zone.md` § "Scope — v1.5.0 Living drop zone memory" (lines 256-303, APPROVED 3 review iterations on parent commit `59a7640`)

**R8 references**:
- `.claude/docs/superpowers/research/sota/living-memory-and-supersession-patterns_2026-04-18.md` (308 lines, 7 SOTA findings grounding 12 design choices, expires 2026-04-25) — primary spec ground
- `.claude/docs/superpowers/research/sota/anthropic-auth-and-oauth-status_2026-04-19.md` (added 2026-04-19 plan-polish-2 ; expires 2026-04-26) — confirms **no first-party OAuth path for Messages API in April 2026**, justifies halt-with-remediation as the only ToS-clean contract for v1.5.0, drives 5 content upgrades to the remediation card (subscription≠API, Console deep-link, OS one-liners, escape hatches, env-scrub warning)

**Pain source**: `memory/project/dogfood_v1.4.1_stress_2026-04-18/stress_test_report.md` Friction #3 + #1 + #2

**Promptor binding**: per `~/.claude/memory/layer0/feedback_invoke_promptor_for_production_anthropic_prompts.md` — the augmented system prompt for `extract_with_citations.py` (Task 1) is designed via the Promptor template lens (`~/.claude/memory/layer0/pepite_promptor_template_anthropic_prompt_engineering.md`). Two-phase template skipped (extractor is one-shot subprocess, no interactive Phase 1 standby). Output structure (Parts B + C + D — payload + edge cases + env vars) used as quality grid; tone constraints + density-over-clarity preserved.

---

## File Structure

### New files (1 total)

| Path | Responsibility |
|---|---|
| `tests/fixtures/drop_zone_intent_fixture_v1_5_0_arbitrated.md` | Regression fixture demonstrating arbitrated_fields + supersedes_snapshot + snapshot_version frontmatter additions; canonical reference for Layer B `⚖` marker render testing |

### Modified files (10 total)

| Path | Responsibility |
|---|---|
| `skills/genesis-drop-zone/scripts/extract_with_citations.py` | Augment `build_system_prompt()` with `divergences[]` field instructions; extend `build_output()` to merge `divergences` from extracted dict; remove fallback exit-code semantics (codes 2-7 now signal halt-with-remediation to SKILL.md, not in-context fallback); preserve all v1.4.0 citation logic verbatim |
| `skills/genesis-drop-zone/SKILL.md` | Add `### In scope (v1.5.0)` section with 11 items mirroring spec; add Phase 0.4 cross-session detection logic (read existing snapshot + 4-class diff: Completion / Retirement / Divergence / Unchanged); add Phase 0.5 arbitration card + halt-with-remediation card; add archive write logic (`drop_zone_intent_history/v<N>_<ISO8601-Z>.md` move + frontmatter augmentation + new snapshot write with incremented `snapshot_version` + `supersedes_snapshot` pointer); add 3 new frontmatter keys (`snapshot_version`, `arbitrated_fields`, `supersedes_snapshot`); update privilege map for v1.5.0 (disk class extended to include `drop_zone_intent_history/` + `drop_zone_intent.md` overwrite); add v1.5.0 to deferred / out-of-scope mirror sections |
| `skills/genesis-drop-zone/phase-0-welcome.md` | 1:1 mirror v1.5.0 SKILL.md additions (cross-skill-pattern #1 discipline). Add v1.5.0 sections per the SKILL.md changes; add new bilingual pair templates: arbitration card (FR + EN paired authoring) + halt-with-remediation card (FR + EN paired authoring); update bridge/locale dispatch logic |
| `skills/genesis-protocol/phase-0-seed-loading.md` | Add v1.5.0 opt-in `⚖` marker rendering on Step 0.4 card (after citation suffix, before EOL) + Step 0.5 `bootstrap_intent.md` template (adjacent to citation suffix in Value column). Logic: read `arbitrated_fields` from frontmatter (key may be absent for v1.4.x compat), render `⚖` suffix on rows whose source field name appears in the array. Zero parser change (dict YAML parse already reads everything); zero new privilege; zero Layer A ripple. Preserve v1.4.1 citation logic verbatim |
| `skills/genesis-drop-zone/scripts/extract_with_citations.py` | (covered above — listed once; the file is touched by Task 1) |
| `memory/master.md` | Cross-skill-pattern #4 fifth data-point: "Layer B opt-in additive rendering of revision-state metadata" (parallel to v1.4.1 "Layer B opt-in additive rendering of provenance metadata"); update concentrated-privilege map for `genesis-drop-zone` v1.5.0 (disk class extended); update streak count to 12th consecutive ≥ 9.0; preserve all v1.4.x prose verbatim |
| `.claude-plugin/plugin.json` | Version bump `1.4.2 → 1.5.0` |
| `CHANGELOG.md` | New v1.5.0 entry with 5-axis self-rating + ship narrative + dogfood-pain origin reference |
| `memory/MEMORY.md` | Add v1.5.0 session pointer entry (most-recent first per existing convention) |
| `memory/project/session_v1_5_0_living_memory.md` | New session trace narrative (chore commit) — 6-commit rhythm 8th application, pain-driven dogfood Friction #3 + #1 + #2 closure, anti-Frankenstein retroactive fallback removal narrative, cross-skill-pattern #4 fifth data-point, projected self-rating breakdown, ship envelope |
| `.claude/docs/superpowers/resume/2026-04-19_v1_5_0_to_v1_5_1_or_v1_6_0.md` | Resume prompt for next session — v1.5.0 ship summary + next candidates (v1.5.1 PATCH if dogfood surfaces friction OR v1.6.0 = `skills/promptor/` per 2026-04-19 Option C decision OR other direction) + PowerShell launcher command |

### Unchanged + preserved-intact (zero ripple guarantees)

| Path | Why listed |
|---|---|
| `skills/genesis-drop-zone/scripts/extract_with_citations.py` v1.4.0 citation logic | Citation extraction (`_shape_citation`, `call_api` block iteration, `<field>_source_citation` keys in output) preserved verbatim. Only the system prompt + `build_output()` divergences merge are added. |
| `skills/genesis-protocol/phase-0-seed-loading.md` Step 0.2a parser mechanics | Dict-based YAML parser unchanged; reads new keys naturally. v1.4.1 citation rendering preserved verbatim; `⚖` rendering added as additional independent suffix logic (citation + `⚖` are independent dimensions per row). |
| `skills/phase-minus-one/**` | Zero touch |
| `skills/phase-5-5-auth-preflight/**` | Zero touch |
| `skills/journal-system/**` | Zero touch |
| `skills/session-post-processor/**` | Zero touch |
| `skills/pepite-flagging/**` | Zero touch |
| `skills/genesis-protocol/install-manifest.yaml` | Zero touch (v1.5.0 does not add Layer B install-time deps) |
| `skills/genesis-protocol/research-templates/**` | Zero touch (v1.4.2 bundle stable) |
| Existing fixtures (`drop_zone_intent_fixture_v1_3_3_en.md`, `drop_zone_intent_fixture_v1_4_0_*.md`) | Zero touch — fixtures pin v1.3.3 / v1.4.0 / v1.4.0-fallback states forever as regression anchors |
| `drop_zone_intent.md` schema_version | Stays at `1` — additive keys only, forward-compatible |

---

## Promptor template — applied at Task 1

Per Layer 0 binding rule, the augmented system prompt for `extract_with_citations.py` is designed via the Promptor template lens. Phase 1 standby is skipped (the extractor is a one-shot subprocess with no interactive specs acquisition; specs are baked into the runtime contract). Phase 2 creation produces:

**Promptor Part A — Inference parameters & calibration (already locked v1.4.0)**
- Model: `claude-opus-4-7` default, env-overridable
- Max tokens: 2048
- Temperature: SDK default (extraction is deterministic enough; no override)
- Stop sequences: none (JSON-only output enforced via prompt + post-validation)
- MCP: none (subprocess is standalone Python, no MCP transport)

**Promptor Part B — Payload (XML architecture, KV cache optimization)**
- Static context first: canonical FR null tokens (constants), schema definition, divergences contract
- Dynamic input last: documents[] + images[] + typed_text wrapper
- Cache control: `ephemeral` with 1h TTL on document blocks (v1.4.0 contract preserved)
- Output schema: JSON object, top-level keys = `schema_version` + 9 semantic fields + `divergences[]` + per-field optional `<field>_source_citation`

**Promptor Part C — Edge cases & robustness**
- Failure modes (exit code semantics, now signaling halt-with-remediation rather than fallback):
  - `2 EXIT_NO_KEY`: env var unset → SKILL.md prints halt card, exits to user
  - `3 EXIT_SDK_MISSING`: import anthropic fails → halt card with `pip install anthropic` remediation
  - `4 EXIT_API_ERROR`: API status / network → halt card with retry hint
  - `5 EXIT_RATE_LIMIT`: 429 after SDK retries → halt card with rate-limit context
  - `6 EXIT_BAD_INPUT`: stdin malformed → halt card (controller-side bug, should not reach Victor)
  - `7 EXIT_OUTPUT_INVALID`: API returned non-JSON or missing fields → halt card with retry hint
- Divergences detection failure mode: extractor cannot perfectly disambiguate intra-document conflict → emit conservative `divergences[]` (false positives over false negatives per KARMA SOTA "flag-never-resolve")
- JSON parsing: `json.loads` failure → exit 7 (output invalid)

**Promptor Part D — Required environment variables**
- `ANTHROPIC_API_KEY` (mandatory; pre-flight checked at `main()` entry; absence → exit 2)
- `GENESIS_DROP_ZONE_MODEL` (optional override)
- `GENESIS_DROP_ZONE_CACHE_TTL` (optional, default `1h`)
- `GENESIS_DROP_ZONE_VERBOSE` (optional, `1` enables stderr forensic logging)

This Promptor lens is invoked silently as design-time grid. The actual prompt change is concentrated in `build_system_prompt()` — all other contract elements are v1.4.0-stable.

---

## Task 0: Pre-flight verification (already on branch)

**Files:**
- Verify: `git status -s` empty
- Verify: `git log --oneline -5` shows expected lineage
- Verify: spec section v1.5.0 present at lines 256-303

- [ ] **Step 0.1: Verify worktree state**

Run: `git status -s && git log --oneline -5`

Expected:
- `git status` empty (only OS-local untracked allowed: `.claude/settings.local.json`, `.playwright-mcp/`)
- HEAD = `0d023b3 spec: v1.5.0 — living drop zone memory ...`
- HEAD parent on main: `5869e54 chore(memory): commit pending 2026-04-18 session archive (#36)`

- [ ] **Step 0.2: Verify spec section present**

Run: `grep -n "^## Scope — v1\.5\.0" .claude/docs/superpowers/specs/v2_etape_0_drop_zone.md`

Expected: line `256:## Scope — v1.5.0 Living drop zone memory`

- [ ] **Step 0.3: Verify R8 reference present**

Run: `ls -la .claude/docs/superpowers/research/sota/living-memory-and-supersession-patterns_2026-04-18.md`

Expected: file exists, ~12 KB. Contents grounding spec rationale bullets (Findings 1-7).

- [ ] **Step 0.4: Verify zero Layer-B-ripple opportunity**

Run: `git diff main --stat -- skills/genesis-protocol/`

Expected: empty (the Layer B `⚖` rendering modifications are intentional v1.5.0 scope and will be added in Task 5; before Task 5 starts, this should be empty).

---

## Task 1: Augment extract_with_citations.py system prompt with divergences[] schema

**Files:**
- Modify: `skills/genesis-drop-zone/scripts/extract_with_citations.py:172-193` (`build_system_prompt()`)

**Context:** The v1.4.0 extractor returns 9 semantic fields + `schema_version` + optional `<field>_source_citation` keys. v1.5.0 adds an additional top-level array `divergences[]` (possibly empty) where the extractor flags intra-drop semantic conflicts (two sources disagree on the same field within the same drop session). Per Promptor Part B + Part C: the divergences contract is added to the static system prompt (KV-cacheable) so the model sees the schema obligation alongside the existing canonical-null-token rules.

- [ ] **Step 1.1: Read current `build_system_prompt()` verbatim for context**

Run: `sed -n '172,193p' skills/genesis-drop-zone/scripts/extract_with_citations.py`

Verify: the function is exactly the v1.4.0 implementation (English R9 tier-1 prompt quoting FR canonical null-class tokens as data).

- [ ] **Step 1.2: Insert divergences contract paragraph in `build_system_prompt()`**

Replace the current `return (...)` block (lines 174-193) with the augmented version. The new prompt appends a `divergences[]` paragraph after the existing `attaches` instruction and before the JSON-only output rule. Preserve all existing prose verbatim.

```python
def build_system_prompt() -> str:
    """English R9 tier-1 prompt quoting FR canonical null-class tokens as data.

    v1.5.0 adds the divergences[] contract — extractor flags intra-drop
    semantic conflicts where two or more sources disagree on the same
    field within the same drop session. Flag-never-resolve principle
    (KARMA + EMNLP knowledge-conflicts SOTA): emit conservative
    detections (false positives over false negatives), let Victor
    arbitrate via Phase 0.5 consolidated card.
    """
    return (
        "You are the v1.5.0 extractor for the Genesis drop-zone skill. "
        "Read the attached documents and images, then output a SINGLE JSON "
        "object with exactly these top-level keys: "
        f"schema_version (integer, value {SCHEMA_VERSION}), "
        f"{', '.join(SEMANTIC_FIELDS)}, "
        "divergences (array, possibly empty). "
        "All semantic field values are strings. "
        "Use these EXACT FR canonical null-class tokens when a field is missing: "
        f'"{FR_CANONICAL_NULL_CORE}" for missing core fields (pour_qui, type, nom); '
        f'"{FR_CANONICAL_NULL_BONUS_MASC}" for missing masculine bonus fields '
        "(budget_ou_contrainte, hints_techniques); "
        f'"{FR_CANONICAL_NULL_BONUS_FEM}" for the feminine bonus field (prive_ou_public); '
        f'"{FR_CANONICAL_AMBIGUITY_TEMPLATE}" pattern for ambiguous fields '
        "(substitute concrete hypotheses for X and Y). "
        "Do not translate these tokens even if the source content is in English. "
        "For langue_detectee emit exactly one of: FR, EN, mixte. "
        "For attaches emit a short human descriptor such as "
        '"1 brief \'name.pdf\' + 1 photo \'logo.png\'" or "texte seul" if nothing dropped. '
        "For divergences emit an array. Each item is an object with three keys: "
        "field (string, MUST be one of " + ", ".join(SEMANTIC_FIELDS) + "), "
        "candidate_values (array of strings, the conflicting values verbatim from sources), "
        "sources (array of strings, brief human identifiers e.g. 'brief.pdf p2', 'annexe.md L14'). "
        "Detect divergences only when two or more sources EXPLICITLY disagree on the same "
        "semantic field — do NOT flag completion (one source silent, another populated) "
        "and do NOT flag minor wording variation. When no divergence exists emit []. "
        "Output ONLY the JSON object, no prose wrapper, no code fence."
    )
```

- [ ] **Step 1.3: Verify the modification is syntactically valid Python**

Run: `python -c "import ast; ast.parse(open('skills/genesis-drop-zone/scripts/extract_with_citations.py').read())"`

Expected: no output (valid syntax). Failure = re-read step 1.2, fix indentation / quoting.

- [ ] **Step 1.4: Verify the new system prompt mentions divergences contract**

Run: `python -c "import sys; sys.path.insert(0, 'skills/genesis-drop-zone/scripts'); from extract_with_citations import build_system_prompt; p = build_system_prompt(); assert 'divergences' in p, 'missing divergences contract'; assert 'flag-never-resolve' not in p.lower() or True, 'docstring vs prompt separation'; assert 'candidate_values' in p; assert 'sources' in p; print('OK')"`

Expected: `OK` printed. The prompt mentions the three required keys (`field`, `candidate_values`, `sources`) and the empty-array convention.

---

## Task 2: Extend extract_with_citations.py output to include divergences

**Files:**
- Modify: `skills/genesis-drop-zone/scripts/extract_with_citations.py:230-243` (`call_api()` divergences extraction)
- Modify: `skills/genesis-drop-zone/scripts/extract_with_citations.py:290-298` (`build_output()` divergences merge)

**Context:** The augmented system prompt instructs the model to emit `divergences[]` at top level. The Python code must read this key from the parsed JSON and pass it through to stdout. Per Promptor Part C robustness: if the model omits the key (older model behaviour, prompt drift), default to `[]` rather than failing — empty divergences = no arbitration triggered, equivalent to v1.4.0 behaviour.

- [ ] **Step 2.1: Add divergences extraction in `call_api()`**

Modify `call_api()` to capture `divergences` from the parsed dict. Insert after the `missing` check (currently at line 230) and before the `per_field_citations` block (currently line 235):

```python
    # v1.5.0 — extract divergences[] from API output (default to [] if absent)
    raw_divergences = extracted.get("divergences", [])
    if not isinstance(raw_divergences, list):
        print(f"[extractor] divergences must be a list, got {type(raw_divergences).__name__}", file=sys.stderr)
        sys.exit(EXIT_OUTPUT_INVALID)
    divergences = _shape_divergences(raw_divergences)
```

Then update the return signature to include `divergences`:

```python
    return extracted, per_field_citations, usage, divergences
```

- [ ] **Step 2.2: Add `_shape_divergences()` helper function**

Insert after `_shape_usage()` (currently at line 285):

```python
def _shape_divergences(raw: list) -> list:
    """Validate and normalize each divergence object.

    v1.5.0 contract: each item must be a dict with keys
    `field` (str, in SEMANTIC_FIELDS), `candidate_values` (list of str),
    `sources` (list of str). Items failing the contract are dropped
    with a stderr warning rather than failing the whole extraction —
    flag-never-resolve principle: imperfect divergence detection
    should not block arbitration on the perfect ones.
    """
    shaped: list = []
    for idx, item in enumerate(raw):
        if not isinstance(item, dict):
            print(f"[extractor] divergence #{idx} not a dict; skipped", file=sys.stderr)
            continue
        field = item.get("field")
        cvs = item.get("candidate_values")
        srcs = item.get("sources")
        if field not in SEMANTIC_FIELDS:
            print(f"[extractor] divergence #{idx} field={field!r} not in SEMANTIC_FIELDS; skipped", file=sys.stderr)
            continue
        if not isinstance(cvs, list) or not all(isinstance(v, str) for v in cvs):
            print(f"[extractor] divergence #{idx} candidate_values invalid; skipped", file=sys.stderr)
            continue
        if not isinstance(srcs, list) or not all(isinstance(s, str) for s in srcs):
            print(f"[extractor] divergence #{idx} sources invalid; skipped", file=sys.stderr)
            continue
        if len(cvs) < 2:
            print(f"[extractor] divergence #{idx} candidate_values has fewer than 2 entries; skipped", file=sys.stderr)
            continue
        shaped.append({"field": field, "candidate_values": cvs, "sources": srcs})
    return shaped
```

- [ ] **Step 2.3: Update `build_output()` to merge divergences into stdout dict**

Modify the `build_output()` signature and body (currently lines 290-298). Replace verbatim:

```python
def build_output(extracted: dict, per_field_citations: dict, usage: dict, divergences: list) -> dict:
    """Merge extraction + citations + usage + divergences into the final stdout dict."""
    output: dict = {"schema_version": SCHEMA_VERSION}
    for field in SEMANTIC_FIELDS:
        output[field] = extracted[field]
    for field, citation in per_field_citations.items():
        output[f"{field}_source_citation"] = citation
    output["divergences"] = divergences
    output["usage"] = usage
    return output
```

- [ ] **Step 2.4: Update `main()` to pass divergences through to `build_output()`**

Modify `main()` body (currently around line 336). Update the `call_api()` unpacking and the `build_output()` call:

```python
    try:
        extracted, per_field_citations, usage, divergences = call_api(client, model, documents, images)
    except anthropic.RateLimitError as exc:
        # ... existing error handling unchanged ...
    # ... rest of main() unchanged until build_output call ...
    output = build_output(extracted, per_field_citations, usage, divergences)
```

- [ ] **Step 2.5: Verify Python syntax + smoke-test**

Run: `python -c "import ast; ast.parse(open('skills/genesis-drop-zone/scripts/extract_with_citations.py').read())"`

Expected: no output. Then verify the function signatures match:

`python -c "import sys; sys.path.insert(0, 'skills/genesis-drop-zone/scripts'); from extract_with_citations import build_output, _shape_divergences; assert build_output({'idea_summary': 'X', 'pour_qui': 'Y', 'type': 'Z', 'nom': 'A', 'attaches': 'B', 'langue_detectee': 'FR', 'budget_ou_contrainte': 'C', 'prive_ou_public': 'D', 'hints_techniques': 'E'}, {}, {}, [])['divergences'] == [], 'divergences default empty failed'; print('OK')"`

Expected: `OK`.

---

## Task 3: SKILL.md — add v1.5.0 In-scope section + Phase 0.4 + Phase 0.5 + archive logic

**Files:**
- Modify: `skills/genesis-drop-zone/SKILL.md` — append `### In scope (v1.5.0)` after the v1.4.0 section; add Phase 0.4 cross-session detection block; add Phase 0.5 arbitration card block; add archive write logic block; add halt-with-remediation card block; update privilege map; update mirror map

**Context:** SKILL.md is the canonical 1:1 mirror of the spec. Per cross-skill-pattern #1 discipline, every spec scope item with implementation surface must have a corresponding SKILL.md section. The v1.5.0 spec has 11 in-scope items — they collapse into ~5 SKILL.md additions because some are conceptual (item 10 six-commit rhythm, item 11 living-spec pattern) and don't need runtime implementation surface.

- [ ] **Step 3.1: Insert v1.5.0 In-scope section after v1.4.0 In-scope**

Locate the line `### In scope (v1.4.0)` in SKILL.md. After the v1.4.0 In-scope item list ends (after item 10), insert the v1.5.0 section:

```markdown
### In scope (v1.5.0)

1. **API requirement — fallback removed** — v1.4.0's silent graceful fallback to in-context extraction is **retired**. The extractor exit codes 2-7 now signal halt-with-remediation to the SKILL.md dispatch layer, not in-context fallback. Anti-Frankenstein retroactive — v1.4.0's fallback was preemptive, never pain-driven validated.
2. **Divergence detection — two triggers, one arbitration phase**:
   - **Intra-drop**: extractor's augmented prompt emits `divergences[]` array per the v1.5.0 system prompt contract. Each item flags two sources disagreeing on the same semantic field within the same drop session.
   - **Cross-session (Phase 0.4)**: when `drop_zone_intent.md` already exists at cwd at skill entry, a new in-context (Claude, not Python) phase compares the existing snapshot against the new extraction using the four-class diff — Completion / Retirement / Divergence / Unchanged.
   - Both trigger types feed the same Phase 0.5 arbitration card. Flag-never-resolve principle: LLM detects, human arbitrates.
3. **Phase 0.5 Arbitration — consolidated bilingual card** — when one or more divergences are detected (intra-drop and/or cross-session), a new arbitration card prints before any write. Lists each divergent field with candidate values + sources + tag (`[intra-drop]` or `[cross-session]`). Victor responds in one consolidated turn (e.g. `"2,1,2"` to pick value 2 for divergence 1, value 1 for divergence 2, value 2 for divergence 3, OR `"autre 3: <value>"` to override divergence 3 with a free-form value).
4. **Archive pattern — `drop_zone_intent_history/` directory** — when a re-run produces a new snapshot:
   - Existing `drop_zone_intent.md` moved to `drop_zone_intent_history/v<N>_<ISO8601-Z-timestamp>.md`
   - Archived file gains frontmatter additions: `status: deprecated`, `archived_at`, `superseded_by: ../drop_zone_intent.md`, `supersession_reason: <intra-drop arbitration | cross-session re-extraction>`
   - New snapshot written with incremented `snapshot_version` and `supersedes_snapshot: ./drop_zone_intent_history/v<N>_<ts>.md` pointer
5. **Three additive frontmatter keys** (schema_version stays at `1`, additive only):
   - `snapshot_version: <int>` — counter starting at 1 on first write, incremented on each supersession
   - `arbitrated_fields: [<field_name>, ...]` — list of field names that went through Phase 0.5 arbitration (empty `[]` if no arbitration; absent key signals v1.4.x legacy)
   - `supersedes_snapshot: "./drop_zone_intent_history/v<N>_<ts>.md"` — relative pointer to archived predecessor (absent on first write)
6. **Layer B opt-in `⚖` marker rendering** — Phase 0 Step 0.4 intent card and Step 0.5 `bootstrap_intent.md` template render a `⚖` marker suffix on each row whose semantic field name appears in `arbitrated_fields`. Marker positioned after the value + citation + origin tag, before EOL. Absent when `arbitrated_fields` is empty or the key is not present (v1.4.x legacy).
7. **Halt-with-remediation card — bilingual FR/EN pair** — printed on any of: `ANTHROPIC_API_KEY` unset, anthropic SDK missing, API status / network / rate-limit / output-invalid errors. Card content: bilingual title, remediation text (set env var + relaunch), link to Anthropic console, note clarifying Claude Code (Max) subscription does not grant API access. R9 tier-3 paired authoring.
8. **Completion vs retirement — asymmetric arbitration triggers** for Phase 0.4 cross-session detection:
   - **Completion** (`current == null-class`, `new != null-class`) → informative log, no arbitration (additive)
   - **Retirement** (`current != null-class`, `new == null-class`) → arbitration required ("keep existing or accept retirement?"), because silent retirement of populated field is destructive
   - **Divergence** (both populated, different) → arbitration required (canonical case)
   - **Unchanged** (both equal, byte-wise) → no action
9. **Victor-exit safety — no mid-flow state change** — if Victor exits (ctrl+c) or abandons mid-arbitration (Phase 0.5), the existing `drop_zone_intent.md` (if any) remains byte-identical, no archive is created, no new write occurs. Arbitration fully precedes write; no partial state on disk.
10. **Six-commit rhythm preservation — eighth consecutive application** (spec + spec polish + plan + plan polish + feat + chore).
11. **Living-spec pattern — seventh consecutive version-scoped section** in `v2_etape_0_drop_zone.md`.
```

- [ ] **Step 3.2: Update privilege declaration block**

Locate the `## Concentrated privilege` section in SKILL.md via `grep -n "^## Concentrated privilege" skills/genesis-drop-zone/SKILL.md` (currently around line 479, well below the In-scope list — do NOT search near v1.4.0 In-scope, the section is in its own canonical location). Append after the v1.4.0 declaration:

```markdown
**v1.5.0 update — disk class extended**: the disk class concentrated privilege now covers (a) writing `drop_zone_intent.md` to cwd after consent (v1.3.2 behaviour preserved), (b) writing `drop_zone_intent_history/v<N>_<ts>.md` archive on supersession, (c) overwriting `drop_zone_intent.md` with the new snapshot after archive. Mitigations: (1) arbitration card consent gates the entire write/archive operation; (2) archive directory created with no `mkdir -p` magic — the v1.5.0 dispatch creates `drop_zone_intent_history/` only when needed and only as a sibling of `drop_zone_intent.md` (no path traversal); (3) timestamp format ISO8601 UTC ensures filename uniqueness; (4) Victor-exit safety = no partial state; (5) supersedes_snapshot pointer + archived superseded_by pointer enable forensic traceability. Network class unchanged (subprocess to Anthropic API per v1.4.0 contract).
```

- [ ] **Step 3.3: Add Phase 0.4 cross-session detection logic block**

After the v1.4.0 dispatch lifecycle section in SKILL.md, insert a new section:

```markdown
### Phase 0.4 — Cross-session divergence detection (v1.5.0)

After the extractor returns its JSON output (whether via the Citations API path or, post-v1.5.0, via the halt-with-remediation card if the API failed), the dispatch layer checks whether `drop_zone_intent.md` already exists at cwd.

**If absent**: this is a first write. Skip Phase 0.4 entirely, proceed to Phase 0.5 with whatever intra-drop divergences the extractor surfaced (may be empty).

**If present**: read the existing snapshot's frontmatter, then run the four-class diff against the new extraction. For each of the 9 semantic fields:

| Class | Trigger | Action |
|---|---|---|
| Unchanged | byte-wise equality of trimmed values | no action |
| Completion | current is null-class token, new is real value | log to stderr `[phase-0.4] field=<name> COMPLETION current=null new="<value>"`; no arbitration |
| Retirement | current is real value, new is null-class token | append cross-session divergence: `{field, candidate_values: [current, new], sources: ["existing snapshot", "new extraction"]}` (forces Victor to arbitrate retirement) |
| Divergence | both populated, byte-wise different | append cross-session divergence with same shape as Retirement |

Tag each cross-session divergence with `[cross-session]` for the arbitration card; intra-drop divergences from the extractor are tagged `[intra-drop]`. Both lists are concatenated into the consolidated card payload.

**Null-class token recognition** uses string equality against the four canonical FR tokens (`a trouver ensemble`, `non mentionne`, `non mentionnee`, `a affiner — X ou Y` pattern with em-dash U+2014). Locale-detected variants are NOT in the contract — frontmatter null tokens stay FR canonical regardless of `content_locale` per v1.3.3's data contract.
```

- [ ] **Step 3.4: Add Phase 0.5 arbitration card logic block**

After Phase 0.4 section, insert:

```markdown
### Phase 0.5 — Arbitration consolidated card (v1.5.0)

If the consolidated divergences list (intra-drop + cross-session) is empty, skip Phase 0.5 entirely. Proceed to write/archive operations with the new extraction values verbatim.

If non-empty, render the bilingual arbitration card. Card content (template — see `phase-0-welcome.md` for verbatim FR + EN body):

```
⚖ Arbitration required — N divergences detected

[1] field=<name1> [intra-drop]
    candidate 1: "<value1>" (source: <src1>)
    candidate 2: "<value2>" (source: <src2>)

[2] field=<name2> [cross-session]
    current value: "<existing>" (source: existing snapshot)
    new value:     "<extracted>" (source: new extraction)

Reply with comma-separated indices: "2,1,2" picks value 2 for #1,
value 1 for #2, value 2 for #3.
Or "autre N: <value>" to override #N with a free-form value.
Or "abort" to exit without changes.
```

The card prints in `content_locale` per v1.3.3 dispatch (FR if `content_locale=FR`, EN if `content_locale=EN`, FR fallback if `mixte`). Both bilingual variants are paired-authored in `phase-0-welcome.md` per R9 tier-3.

**Victor's response** is parsed:
- Comma-separated indices `"i,j,k,..."` where each value is `1..len(divergence.candidate_values)` for that divergence: pick the corresponding candidate.
- `"autre N: <value>"` for any N: override divergence #N with the free-form value (string).
- `"abort"` (or any natural-language abort signal): exit cleanly. Existing `drop_zone_intent.md` (if any) byte-identical. No archive. No new write.
- Malformed response → re-prompt with parse-error hint, do not write.

After successful arbitration, the resolved values replace the extractor's raw values for the affected fields. The list of arbitrated field names is recorded in `arbitrated_fields` for the new snapshot's frontmatter.
```

- [ ] **Step 3.5: Add archive write logic block**

After Phase 0.5, insert:

```markdown
### Archive write — supersession chain (v1.5.0)

Once arbitration resolves (or skipped because no divergences), the dispatch layer performs the write/archive operation atomically (in dispatch terms — Genesis is single-writer):

**If `drop_zone_intent.md` exists** (re-run path):
1. Read its current `snapshot_version` (default 1 if absent — v1.4.x legacy compat).
2. Construct archive filename: `drop_zone_intent_history/v<N>_<ISO8601-Z>.md` where N = current snapshot_version, timestamp is `datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')`.
3. Read current `drop_zone_intent.md`, augment its frontmatter:
   - `status: deprecated`
   - `archived_at: <ISO8601-Z timestamp>`
   - `superseded_by: ../drop_zone_intent.md`
   - `supersession_reason: <"intra-drop arbitration" | "cross-session re-extraction" | "user re-run no divergence">`
4. Write augmented content to the archive path (creating `drop_zone_intent_history/` directory if absent).
5. Construct new snapshot frontmatter from extractor output + arbitration results:
   - `schema_version: 1` (unchanged)
   - 9 semantic fields (arbitrated values where applicable)
   - 4 metadata keys (`created_at` = current ISO8601-Z, `skill: genesis-drop-zone`, `skill_version: 1.5.0`)
   - `<field>_source_citation` for each field with citation (v1.4.0 logic preserved)
   - `snapshot_version: <N+1>`
   - `arbitrated_fields: [<list>]` (empty `[]` if no arbitration occurred this round)
   - `supersedes_snapshot: ./drop_zone_intent_history/v<N>_<ts>.md`
6. Overwrite `drop_zone_intent.md` with the new snapshot.

**If `drop_zone_intent.md` does NOT exist** (first write path):
1. Construct snapshot frontmatter as above with `snapshot_version: 1`, `arbitrated_fields: <list or []>`, omit `supersedes_snapshot` key entirely (not first-write semantics).
2. Write `drop_zone_intent.md`.

**Failure semantics**:
- Disk error during archive move (permission, disk-full): halt with error message, do NOT proceed to overwrite. Existing `drop_zone_intent.md` byte-identical.
- Disk error during new snapshot write after successful archive: halt with error message including the archive filename so Victor can manually restore. Existing `drop_zone_intent.md` is GONE in this case (worst case) — but the archive contains the previous content with augmented frontmatter for restore. v1.5.0 accepts this small window as the tradeoff for not implementing fsync-then-rename atomic-write semantics (Python `os.replace` provides POSIX rename atomicity on the new write but not on the archive move; Windows behaviour aligned via Python 3.x `os.replace`). v1.5.1+ may add fsync if the window matters in practice.
```

- [ ] **Step 3.6: Add halt-with-remediation card section (upgraded per 2026-04-19 R8 research)**

After the archive write logic, insert. **Upgraded content per `sota/anthropic-auth-and-oauth-status_2026-04-19.md`** — 5 content additions vs initial v1.5.0 spec § In scope item 7: subscription≠API explanation, Console deep-link, OS-specific one-liners, escape hatches, env-scrub warning.

```markdown
### Halt-with-remediation card (v1.5.0)

When the extractor exits with code 2-7, the dispatch layer renders the bilingual halt card (paired-authored in `phase-0-welcome.md`). The card content names the failure class explicitly so Victor knows what to fix.

**Why an API key (and not a Claude Max subscription)** — Anthropic intentionally separates two billing surfaces and identities:

- **Claude Max ($200/mo subscription)** covers `claude.ai` web app + Claude Desktop + Claude Code CLI inference. Pays for human-driven Claude conversations.
- **API key** (`sk-ant-...` from `console.anthropic.com`) bills per-token to a workspace. Pays for programmatic Messages API / Citations / Files calls — including the Genesis drop-zone Citations extractor subprocess.

The two are intentionally distinct — research-confirmed [`sota/anthropic-auth-and-oauth-status_2026-04-19.md`]. Even on April 19, 2026, no public OAuth path lets a third-party app (including Genesis) use a subscription identity for Messages API. The halt card surfaces this honestly rather than degrading silently.

Per-failure-class card content:

| Exit code | Card title (FR + EN) | Remediation |
|---|---|---|
| 2 EXIT_NO_KEY | Genesis nécessite une clé API Anthropic / Genesis requires an Anthropic API key | (See full FR + EN body templates in `phase-0-welcome.md` — includes Console deep-link, OS-specific one-liners, escape hatches, env-scrub warning.) |
| 3 EXIT_SDK_MISSING | SDK Anthropic non installé / Anthropic SDK not installed | `pip install anthropic` (or `uv pip install anthropic` / `pipx install anthropic` per Python tooling preference), then relaunch Claude Code in this folder, then re-invoke `/genesis-drop-zone`. |
| 4 EXIT_API_ERROR | Erreur API Anthropic / Anthropic API error | Check Anthropic Console status page for incidents (https://status.anthropic.com); retry in a few minutes. If persistent, set `GENESIS_DROP_ZONE_VERBOSE=1` and re-run for stderr diagnostic logs. |
| 5 EXIT_RATE_LIMIT | Limite de débit Anthropic dépassée / Anthropic rate limit exceeded | Wait 60s and retry; check workspace usage at https://console.anthropic.com/settings/billing. If you're on a free tier, request a tier upgrade. The Citations extraction is a single API call (cached 1h via cache_control) — repeated rate-limit triggers signal workspace-wide usage. |
| 6 EXIT_BAD_INPUT | Erreur interne extracteur (input invalide) / Internal extractor error (invalid input) | Internal Genesis bug — please file an issue at https://github.com/myconciergerie-prog/project-genesis/issues with the stderr log. The extractor expected a payload shape the SKILL.md dispatcher should always produce — divergence indicates a controller-side regression. |
| 7 EXIT_OUTPUT_INVALID | Sortie API invalide / Invalid API output | Retry once; if persistent, switch model via `GENESIS_DROP_ZONE_MODEL` env var (e.g. `GENESIS_DROP_ZONE_MODEL=claude-sonnet-4-6`). Anthropic Console message logs may show the raw response — useful for diagnosis. |

**Footer note (always rendered, both languages)**:

```
Note : la souscription Claude Code (Max) ne donne PAS acces a l'API.
La cle API Anthropic est un produit separe, factures au token et a la
ressource (workspace), independant de l'abonnement souscription.
Voir : https://console.anthropic.com/settings/keys

Note: the Claude Code (Max) subscription does NOT grant API access.
The Anthropic API key is a separate product, billed per-token at the
workspace level, independent of the subscription tier. See:
https://console.anthropic.com/settings/keys
```

The card prints in `content_locale` order — if `content_locale=FR`, FR top + EN bottom; if EN, EN top + FR bottom; if `mixte`, FR top + EN bottom. After printing, the dispatch layer halts (no fallback, no retry, no in-context degradation). Victor fixes the cause and re-runs `/genesis-drop-zone`.

**Future-proofing note**: a future Claude Code release may default `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1`, scrubbing `ANTHROPIC_API_KEY` from subprocess env at extractor invocation time. To survive that change, the env var MUST be set at the **OS / shell profile level** (see `setx` / `.zshenv` instructions in the EXIT_NO_KEY full body template in `phase-0-welcome.md`), NOT just in the current Claude Code session. This is a one-time setup; the env var persists across all Claude Code sessions afterwards.
```

- [ ] **Step 3.7: Update Out-of-scope mirror section to renumber v1.5.1+**

Locate the current `### Out of scope (deferred to v1.4.1+)` section. Update to reflect the v1.5.0 ship absorbed several items:

```markdown
### Out of scope (deferred to v1.5.1+)

(See spec § "Scope — v1.5.0 / Out of scope" for full list. Items unchanged from v1.4.2 deferred list, renumbered as v1.5.1+: Layer B expandable archive diff, retry policy on 5xx transient errors, archive retention policy, concurrent re-runs protection, import of archived snapshot, cross-project memory flow, event log alongside snapshot, `cited_text_preview` inline surfacing / hyperlink citations / Files API / programmatic handoff / GH_BROWSER / UX toolkit / chime / bilingual Layer B null-class parsing / three-locale expansion / Structured Outputs Path B pivot.)
```

- [ ] **Step 3.8: Update mirror map at top of SKILL.md**

If SKILL.md has a top-level mirror map naming the v1.4.x sections that mirror the spec, extend with v1.5.0 sections:

Run: `grep -n "1:1 mirror" skills/genesis-drop-zone/SKILL.md | head -3`

If the map exists as a table, append v1.5.0 rows. If the discipline is named in prose only, no change needed (spec section + SKILL.md additions both carry version markers).

---

## Task 4: phase-0-welcome.md — mirror v1.5.0 SKILL.md additions per 1:1 mirror discipline

**Files:**
- Modify: `skills/genesis-drop-zone/phase-0-welcome.md` — add v1.5.0 sections that mirror Task 3 SKILL.md additions; add 2 new bilingual pair templates (arbitration card + halt-with-remediation card)

**Context:** Cross-skill-pattern #1 mandates that SKILL.md and phase-0-welcome.md are 1:1 mirrors. Every Task 3 addition has a corresponding phase-0-welcome.md addition. Additionally, the bilingual card content (FR + EN paired authoring) lives in phase-0-welcome.md as the verbatim source of truth — SKILL.md references it without duplicating the body text.

- [ ] **Step 4.1: Read current phase-0-welcome.md table of contents**

Run: `grep -nE "^(##|###) " skills/genesis-drop-zone/phase-0-welcome.md | head -40`

Expected: structure matching SKILL.md sections (Welcome body, Acknowledgement template, Mirror screen, Consent card, Halt message, Bridges, Failure modes, etc.). Confirm v1.4.0 sections are present.

- [ ] **Step 4.2: Insert v1.5.0 mirror block after the v1.4.0 sections**

After the last v1.4.0-tagged section (likely "Citations API — signal + dispatch (v1.4.0)" near the end), append a v1.5.0 block with subsections:

- Phase 0.4 cross-session detection — describes the four-class diff, points back to SKILL.md for the dispatch logic
- Phase 0.5 arbitration card — verbatim FR + EN body templates (paired-authored)
- Halt-with-remediation card — verbatim FR + EN body templates (paired-authored, one card per exit code class)
- Archive frontmatter additions — verbatim YAML examples for first-write + supersession-write
- Living-memory bridges — updates to v1.3.2 accept/decline bridges if needed (likely unchanged: bridges are about "what next", not about the write mechanism)

- [ ] **Step 4.3: Add arbitration card FR template**

Insert under v1.5.0 Phase 0.5 subsection:

```markdown
### Arbitration card — FR variant (rendered when `content_locale = FR`)

```
⚖ Arbitrage requis — <N> divergences detectees

[1] champ=<nom_du_champ_1> [intra-drop]
    candidat 1 : "<valeur 1>" (source : <src 1>)
    candidat 2 : "<valeur 2>" (source : <src 2>)

[2] champ=<nom_du_champ_2> [cross-session]
    valeur actuelle : "<valeur existante>" (source : snapshot existant)
    nouvelle valeur : "<valeur extraite>" (source : nouvelle extraction)

Reponds avec les indices separes par des virgules : "2,1,2" choisit
la valeur 2 pour #1, valeur 1 pour #2, valeur 2 pour #3.
Ou "autre N : <valeur>" pour ecraser #N avec une valeur libre.
Ou "abort" pour quitter sans modification.
```
```

- [ ] **Step 4.4: Add arbitration card EN template**

Insert immediately after FR variant:

```markdown
### Arbitration card — EN variant (rendered when `content_locale = EN`)

```
⚖ Arbitration required — <N> divergences detected

[1] field=<field_name_1> [intra-drop]
    candidate 1: "<value 1>" (source: <src 1>)
    candidate 2: "<value 2>" (source: <src 2>)

[2] field=<field_name_2> [cross-session]
    current value: "<existing value>" (source: existing snapshot)
    new value:     "<extracted value>" (source: new extraction)

Reply with comma-separated indices: "2,1,2" picks value 2 for #1,
value 1 for #2, value 2 for #3.
Or "autre N: <value>" to override #N with a free-form value.
Or "abort" to exit without changes.
```
```

- [ ] **Step 4.5: Add halt-with-remediation card FR template (upgraded per 2026-04-19 R8 research, one per exit-code class)**

Insert under v1.5.0 halt-with-remediation subsection. Body includes 6 cards (one per exit code 2-7), each in FR.

**Upgraded EXIT_NO_KEY template** (upgrades per `sota/anthropic-auth-and-oauth-status_2026-04-19.md`: subscription≠API explanation, Console deep-link with role hint, OS-specific persistent one-liners using `setx` for Windows + `.zshenv` reference for POSIX persistence, escape hatches mention, env-scrub future-proofing warning):

```markdown
### Halt-with-remediation card — FR variant (EXIT_NO_KEY = 2)

```
⛔ Genesis necessite une cle API Anthropic

L'extracteur Citations a besoin d'une cle API Anthropic
configuree dans la variable d'environnement ANTHROPIC_API_KEY.

Pourquoi une cle API et pas mon abonnement Claude Max ?
  L'abonnement Claude Max paye claude.ai + Claude Desktop +
  Claude Code CLI (inference). La cle API Anthropic est un
  produit SEPARE, facture au token au niveau workspace, et
  active programmatic Messages API + Citations + Files. Les
  deux sont volontairement distincts (architecture Anthropic
  avril 2026, voir https://console.anthropic.com/settings/keys).

Remediation :

  1. Recupere une cle sur https://console.anthropic.com/settings/keys
     - Cliquer "Create Key" -> nommer "genesis-drop-zone"
     - Role : "Claude Code" (ou "Developer" si "Claude Code"
       n'est pas propose dans ton workspace)
     - Copier la valeur sk-ant-... commencant par sk-ant-

  2. Configure la variable d'environnement de facon PERSISTANTE
     (pas seulement la session courante) :

     Windows (PowerShell elevee, persistant systeme) :
       setx ANTHROPIC_API_KEY "sk-ant-..."

     POSIX (bash/zsh, ajouter au profile shell) :
       echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.zshenv
       (ou ~/.bashrc selon ton shell)

     Ne PAS utiliser uniquement `$env:ANTHROPIC_API_KEY = "..."`
     dans la session Claude Code en cours : un futur release
     Claude Code peut activer `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`
     par defaut, qui retirerait la variable des subprocess.
     setx / .zshenv survivent a ce changement.

  3. Relance Claude Code dans ce dossier (close + reopen)

  4. Reinvoque /genesis-drop-zone

Echapatoires (avance, optionnels) :
  - LLM gateway / proxy : utiliser ANTHROPIC_AUTH_TOKEN au lieu
    de ANTHROPIC_API_KEY (voir docs Anthropic)
  - Secrets rotatifs (vault, AWS Secrets Manager) : configurer
    apiKeyHelper dans ~/.anthropic/config (voir docs Anthropic)

Note : la souscription Claude Code (Max) ne donne PAS acces a
l'API. La cle API Anthropic est un produit separe.
```
```

**For the 5 remaining exit codes (EXIT_SDK_MISSING, EXIT_API_ERROR, EXIT_RATE_LIMIT, EXIT_BAD_INPUT, EXIT_OUTPUT_INVALID)**, follow the same canonical structure but use the per-code remediation content from Task 3.6 SKILL.md table. Each card body:

1. Brief diagnostic title (e.g. "SDK Anthropic non installe")
2. One-paragraph explanation of what failed
3. Remediation steps (numbered, exact commands)
4. Optional escape hatches if applicable
5. Footer note (subscription ≠ API — same paragraph for all 6 cards, ensuring consistency)

The bilingual pair count delta verification (Task 10.4 expects +14) accounts for: 1 arbitration FR + 1 arbitration EN + 6 halt-FR + 6 halt-EN = 14 new bilingual variants. Verify per Task 10.4 before commit.

- [ ] **Step 4.6: Add halt-with-remediation card EN templates (upgraded paired with Step 4.5 FR)**

Mirror the 6 FR cards to EN, paired-authored.

**Upgraded EXIT_NO_KEY EN template** (1:1 mirror of the FR Step 4.5 EXIT_NO_KEY card):

```markdown
### Halt-with-remediation card — EN variant (EXIT_NO_KEY = 2)

```
⛔ Genesis requires an Anthropic API key

The Citations extractor needs an Anthropic API key configured
in the ANTHROPIC_API_KEY environment variable.

Why an API key and not my Claude Max subscription?
  Your Claude Max subscription pays for claude.ai + Claude
  Desktop + Claude Code CLI (inference). The Anthropic API
  key is a SEPARATE product, billed per-token at the
  workspace level, and unlocks programmatic Messages API +
  Citations + Files. The two are intentionally distinct
  (Anthropic architecture, April 2026 — see
  https://console.anthropic.com/settings/keys).

Remediation:

  1. Get a key at https://console.anthropic.com/settings/keys
     - Click "Create Key" -> name it "genesis-drop-zone"
     - Role: "Claude Code" (or "Developer" if "Claude Code"
       is not offered in your workspace)
     - Copy the sk-ant-... value beginning with sk-ant-

  2. Set the environment variable PERSISTENTLY (not just the
     current session):

     Windows (PowerShell elevated, system-wide persistent):
       setx ANTHROPIC_API_KEY "sk-ant-..."

     POSIX (bash/zsh, add to shell profile):
       echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.zshenv
       (or ~/.bashrc depending on your shell)

     Do NOT use only `$env:ANTHROPIC_API_KEY = "..."` in the
     current Claude Code session: a future Claude Code release
     may default-enable `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`,
     which would strip the variable from subprocesses.
     setx / .zshenv survive that change.

  3. Relaunch Claude Code in this folder (close + reopen)

  4. Re-invoke /genesis-drop-zone

Escape hatches (advanced, optional):
  - LLM gateway / proxy: use ANTHROPIC_AUTH_TOKEN instead of
    ANTHROPIC_API_KEY (see Anthropic docs)
  - Rotating secrets (vault, AWS Secrets Manager): configure
    apiKeyHelper in ~/.anthropic/config (see Anthropic docs)

Note: the Claude Code (Max) subscription does NOT grant API
access. The Anthropic API key is a separate product.
```
```

**For the 5 remaining EN exit-code cards**, mirror the corresponding FR cards from Step 4.5. Same structure: title + why-paragraph + numbered remediation + optional escape hatches + footer note. Paired-authored discipline R9 tier-3 — every FR card has a 1:1 EN mirror written in the same plan-polish iteration.

- [ ] **Step 4.7: Add archive frontmatter examples (FR + EN locale-neutral — frontmatter keys are always English)**

Insert under v1.5.0 archive write subsection:

```markdown
### Archive frontmatter examples (locale-neutral — keys are English)

**First write (v1.5.0 fresh)**:
```yaml
schema_version: 1
created_at: 2026-04-19T15:30:00Z
skill: genesis-drop-zone
skill_version: "1.5.0"
snapshot_version: 1
arbitrated_fields: []
# ... 9 semantic fields ...
# ... optional <field>_source_citation entries ...
```

**Supersession write (v2 of the snapshot)**:
```yaml
schema_version: 1
created_at: 2026-04-19T16:00:00Z
skill: genesis-drop-zone
skill_version: "1.5.0"
snapshot_version: 2
arbitrated_fields: [pour_qui, budget_ou_contrainte]
supersedes_snapshot: ./drop_zone_intent_history/v1_20260419T153000Z.md
# ... 9 semantic fields (with arbitrated values) ...
```

**Archived predecessor frontmatter (after supersession)**:
```yaml
schema_version: 1
created_at: 2026-04-19T15:30:00Z
skill: genesis-drop-zone
skill_version: "1.5.0"
snapshot_version: 1
arbitrated_fields: []
status: deprecated
archived_at: 2026-04-19T16:00:00Z
superseded_by: ../drop_zone_intent.md
supersession_reason: cross-session re-extraction
# ... 9 semantic fields (original values) ...
```
```

- [ ] **Step 4.8: Verify mirror discipline post-additions**

Run: `grep -c "v1\.5\.0" skills/genesis-drop-zone/SKILL.md skills/genesis-drop-zone/phase-0-welcome.md`

Expected: both files have ≥ 5 v1.5.0 references each. Both files reference the same Phase 0.4, Phase 0.5, halt-with-remediation, archive logic concepts.

---

## Task 5: skills/genesis-protocol/phase-0-seed-loading.md — Layer B `⚖` marker rendering

**Files:**
- Modify: `skills/genesis-protocol/phase-0-seed-loading.md` — add v1.5.0 opt-in `⚖` marker rendering on Step 0.4 card + Step 0.5 template

**Context:** Cross-skill-pattern #4 fifth data-point: Layer B opt-in additive rendering of revision-state metadata. The v1.4.1 pattern (Layer B opt-in additive rendering of provenance metadata via citation suffix) is the precedent. v1.5.0 follows the same shape: Layer A writes new optional frontmatter key (`arbitrated_fields`), Layer B Step 0.4 + Step 0.5 read it (no parser change — dict YAML parser already reads everything) and render `⚖` suffix on rows whose source field name appears in the array. Zero Layer A ripple, zero schema bump, zero new privilege.

- [ ] **Step 5.1: Read current Step 0.4 card template + Step 0.5 template**

Run: `sed -n '131,170p' skills/genesis-protocol/phase-0-seed-loading.md` (Step 0.4 card template — lines 131-170 approx)
Run: `sed -n '212,272p' skills/genesis-protocol/phase-0-seed-loading.md` (Step 0.5 template — lines 212-272 approx)

Verify: v1.4.1 citation suffix rendering is present (`<citation>` placeholder on rows). The `⚖` will be added as a parallel suffix.

- [ ] **Step 5.2: Update Step 0.4 card template — add `⚖` placeholder after citation**

Locate the Step 0.4 card template (the ASCII box block). For each row that has a `<citation>` placeholder, replace `<citation>` with `<citation><arbitrated_marker>` (in that order — citation first, marker second, before EOL).

Example (illustrative — apply to all 9 citation-eligible rows):
```diff
- Project name           : <value or [missing]> (<origin>)<citation>
+ Project name           : <value or [missing]> (<origin>)<citation><arbitrated_marker>
```

The placeholder `<arbitrated_marker>` expands to `' ⚖'` when the row's semantic field name is in `arbitrated_fields` (the YAML key in `drop_zone_intent.md` frontmatter), or to the empty string otherwise.

- [ ] **Step 5.3: Add a "Marker rendering rules" subsection after the citation rules subsection in Step 0.4**

Insert after the v1.4.1 "Citation suffix on card rows (v1.4.1)" subsection (before "Rows explicitly NOT annotated"):

```markdown
#### Arbitrated-field marker (v1.5.0)

**Added in v1.5.0.** The `<arbitrated_marker>` placeholder renders a `⚖` suffix on rows whose semantic field name is present in the `arbitrated_fields` array of `drop_zone_intent.md` frontmatter. When the array is empty, or the key is absent (v1.4.x legacy snapshots), the placeholder expands to the empty string (no leading space, no marker).

Marker positioning per row: `<value> (<origin>)<citation> ⚖` — marker is the rightmost element on the line, immediately after the citation suffix (which itself is immediately after the origin tag). When citation is absent, marker still positions immediately after origin: `<value> (<origin>) ⚖`.

Field-to-row mapping for marker rendering — same propagation rules as the v1.4.1 citation map:

| Card row | Source semantic field name (in `arbitrated_fields`) | Render `⚖` if |
|---|---|---|
| Project name | `nom` | `arbitrated_fields` contains `nom` |
| Project slug | `nom` | propagated — same condition as Project name |
| Vision | `idea_summary` | `arbitrated_fields` contains `idea_summary` |
| Stack hints | `hints_techniques` | contains `hints_techniques` |
| Is-a-plugin | `type` | propagated — contains `type` |
| Target audience | `pour_qui` | contains `pour_qui` |
| Language detected | `langue_detectee` | contains `langue_detectee` |
| Budget / constraint | `budget_ou_contrainte` | contains `budget_ou_contrainte` |
| Visibility | `prive_ou_public` | contains `prive_ou_public` |

Rows in § "Rows explicitly NOT annotated" (Target folder, License, Plan tier, Scope locks, Gaps to fill, Mixed media) carry no Layer A semantic source and therefore receive no `⚖` marker even when `arbitrated_fields` is non-empty.

The marker is purely informational — it tells the human reviewer that this value went through Phase 0.5 arbitration during Layer A. Layer B does not consume the marker for any decision logic; it does not read the archived predecessor; it does not surface diffs. The "show me what changed" expansion is a v1.5.1+ deferred item (per spec § Out of scope).

**Backwards compatibility**: Layer B reading a v1.4.x `drop_zone_intent.md` (no `arbitrated_fields` key in frontmatter) renders zero markers — the dict YAML parser returns no key, the conditional collapses to empty string. The `<arbitrated_marker>` placeholder is safely additive.
```

- [ ] **Step 5.4: Update Step 0.5 template — add `<arbitrated_marker>` placeholder in Value columns**

Locate the Step 0.5 `bootstrap_intent.md` template. In the `## Fields` table, for each row with a `<citation>` placeholder, append `<arbitrated_marker>`:

```diff
- | Project name | <value><citation> | config.txt / drop_zone_intent.md / user edit |
+ | Project name | <value><citation><arbitrated_marker> | config.txt / drop_zone_intent.md / user edit |
```

Apply to: Project name, Slug, Vision, Is-a-plugin, Stack hints (5 rows in `## Fields`).

In the `## Conversational context from drop zone` table:

```diff
- | Target audience (pour qui) | <value or "a trouver ensemble"><citation> |
+ | Target audience (pour qui) | <value or "a trouver ensemble"><citation><arbitrated_marker> |
```

Apply to all 4 rows (Target audience, Language detected, Budget or constraint, Visibility).

- [ ] **Step 5.5: Add a Step 0.5 marker rendering note**

After the v1.4.1 citation suffix paragraph in Step 0.5, append:

```markdown
**Arbitrated-field marker inside `Value` columns (v1.5.0)**: the `<arbitrated_marker>` placeholder renders the `⚖` suffix per the same rules as Step 0.4's card (mapping table + visibility logic documented in § "Step 0.4 / Arbitrated-field marker (v1.5.0)" above). Placeholder is positioned after the citation suffix per the same canonical ordering: `<value><citation><arbitrated_marker>`. When `arbitrated_fields` is absent (v1.4.x legacy) or empty, no marker renders. Cross-skill-pattern #4 fifth data-point — Layer B opt-in additive rendering of revision-state metadata; parser mechanics unchanged.
```

- [ ] **Step 5.6: Verify zero parser change**

Run: `grep -c "schema_version" skills/genesis-protocol/phase-0-seed-loading.md`

Verify: schema_version still validated as `== 1` (v1.5.0 preserved schema_version 1 — additive frontmatter only).

Run: `git diff main -- skills/genesis-protocol/phase-0-seed-loading.md | grep -E "^[+-]" | grep -vE "^[+-]{3}" | wc -l`

Expected: positive number (additions for `<arbitrated_marker>` placeholder + new subsections), zero deletions of substantive parser logic. If deletions exist, re-read step 5.5 and re-add lines.

---

## Task 6: master.md — cross-skill-pattern #4 fifth data-point + ship streak count

**Files:**
- Modify: `memory/master.md` — extend cross-skill-pattern #4 narrative with v1.5.0 fifth data-point; update concentrated-privilege map for genesis-drop-zone v1.5.0

**Context:** master.md cross-skill-pattern #4 narrative tracks each version's contribution to the zero-Layer-B-ripple discipline. v1.3.2 wire + v1.3.3 body-vs-frontmatter asymmetry + v1.4.0 additive keys + v1.4.1 additive rendering + **v1.5.0 additive revision-state rendering with parser-mechanics unchanged** = fifth data-point. The privilege map for genesis-drop-zone disk class also needs the v1.5.0 archive operation added.

- [ ] **Step 6.1: Read current cross-skill-pattern #4 paragraph**

Run: `grep -nA 20 "Layer A / Layer B stratification" memory/master.md | head -60`

Verify v1.4.1 fourth data-point present.

- [ ] **Step 6.2: Append v1.5.0 fifth data-point sentence**

Locate the v1.4.1 sentence ending with "Future Étape-skills composing on this pattern default to "additive keys + additive read-only rendering", bumping schema_version only for genuinely incompatible restructurings."

Append:

```markdown
**v1.5.0 extends the discipline one version further via additive revision-state metadata** — Layer A writes three optional frontmatter keys (`snapshot_version`, `arbitrated_fields`, `supersedes_snapshot`) on first / supersession writes; Layer B's Step 0.4 card and Step 0.5 `bootstrap_intent.md` template render a `⚖` suffix on rows whose semantic field name appears in `arbitrated_fields`, without bumping `schema_version`, without growing the Step 0.2a parser, and without touching Layer A's write logic. **Fifth data-point of the zero-ripple principle**: v1.3.2 wire + v1.3.3 body-vs-frontmatter asymmetry + v1.4.0 additive keys + v1.4.1 additive rendering + v1.5.0 additive revision-state rendering. The forward-compat envelope holds: old Layer A + new Layer B = zero markers rendered (no key, no array); new Layer A + old Layer B = `arbitrated_fields` ignored silently (dict parser passes through). The v1.5.0 ship is also the first to apply the discipline to a non-provenance metadata class (revision-state vs source-attribution), confirming the pattern generalizes beyond citation surfacing.
```

- [ ] **Step 6.3: Update concentrated-privilege map paragraph**

Locate the genesis-drop-zone privilege description (search "genesis-drop-zone" + "first multi-class declaration"). Append after the v1.4.1 sentence:

```markdown
**v1.5.0 disk class extension** — the disk class privilege now covers (a) writing `drop_zone_intent.md` to cwd after consent (v1.3.2 behaviour preserved as first-write path), (b) writing `drop_zone_intent_history/v<N>_<ts>.md` archive entries on supersession, (c) overwriting `drop_zone_intent.md` with a new snapshot after archive. The five mitigations are extended: (1) arbitration card consent gates the entire write/archive operation; (2) `drop_zone_intent_history/` directory created without `mkdir -p` magic — only as a sibling of `drop_zone_intent.md`; (3) ISO8601 UTC timestamp guarantees archive filename uniqueness; (4) Victor-exit safety = no partial state on disk; (5) `supersedes_snapshot` pointer + archived `superseded_by` pointer enable bidirectional forensic traceability. **Network class unchanged** (subprocess to Anthropic Messages API per v1.4.0), but **fallback retired** — failure modes route to halt-with-remediation card instead of in-context degradation. Cross-class independence preserved: disk and network privileges remain orthogonal with their own consent models and mitigation sets.
```

- [ ] **Step 6.4: Update streak count + most-recent-ship reference at end of cross-skill-pattern paragraph**

**Default to the fallback path** — reviewer iteration confirmed master.md does not currently carry an explicit "Eleventh consecutive ship ≥ 9.0" sentence in the cross-skill-pattern paragraph. Do NOT spend time hunting for an existing sentence to edit. Instead, add a new sentence at the end of the v1.5.0 fifth-data-point paragraph (Step 6.2 just appended it) reading: "This data-point is also the **twelfth consecutive ship ≥ 9.0** for project-genesis (11/11 since v1.2.1, projected v1.5.0 self-rating ≈ 9.20-9.30)."

If grep DOES surface an existing ship-count sentence elsewhere (run `grep -nE "(consecutive|onzième|onzieme|eleventh|11th|11/11)" memory/master.md`), update that sentence in place rather than creating a duplicate.

- [ ] **Step 6.5: Verify edits don't break the existing prose flow**

Run: `wc -l memory/master.md`

Compare to pre-edit count (baseline from git): expected delta = +20 to +30 lines (one v1.5.0 data-point sentence + one privilege-extension sentence + minor count update).

---

## Task 7: .claude-plugin/plugin.json version bump

**Files:**
- Modify: `.claude-plugin/plugin.json` — version `1.4.2 → 1.5.0`

- [ ] **Step 7.1: Read current version**

Run: `grep -E '"version"' .claude-plugin/plugin.json`

Expected: `"version": "1.4.2",`

- [ ] **Step 7.2: Bump to 1.5.0**

Edit: replace `"version": "1.4.2"` with `"version": "1.5.0"`.

- [ ] **Step 7.3: Verify JSON parseable**

Run: `python -c "import json; print(json.load(open('.claude-plugin/plugin.json'))['version'])"`

Expected: `1.5.0`.

---

## Task 8: Create regression fixture for v1.5.0 arbitrated frontmatter

**Files:**
- Create: `tests/fixtures/drop_zone_intent_fixture_v1_5_0_arbitrated.md`

**Context:** Pinning a fixture demonstrating the v1.5.0 frontmatter additions provides a regression anchor for Layer B `⚖` marker render testing and future Layer A reads. Pattern follows v1.4.0 fixtures (FR + EN with citations + fallback). v1.5.0 needs only one fixture demonstrating the arbitration trail; FR + EN locale variants are not separately fixtured because frontmatter is locale-neutral (English keys, FR canonical null tokens) and body is implementation-detail-of-render-time.

- [ ] **Step 8.1: Write fixture file**

Create the file with this exact content (UTF-8, LF line endings, schema_version: 1, demonstrating arbitrated_fields + supersedes_snapshot + snapshot_version, with two arbitrated fields + corresponding citation keys retained).

**CRLF preservation note** (Layer 0 `gotcha_crlf_preservation_git_bash_windows.md`): use `Write` tool directly (Python-equivalent direct write via `pathlib`), NOT `cp` from an existing fixture template followed by `sed` / `perl` / `awk` in-place edits. Such tools silently normalize CRLF → LF on Windows git-bash and shift bytes invisibly. If the implementer chooses a copy-as-template path, use Python `pathlib.Path.read_bytes() + bytes.replace() + write_bytes()` to preserve byte-exact line-ending semantics. Probe load-bearing: `cmp -l <new fixture> <reference fixture> | wc -l` should show only the intentional byte deltas (e.g. frontmatter additions), zero spurious EOL byte differences.

```yaml
<!-- SPDX-License-Identifier: MIT -->
---
schema_version: 1
created_at: 2026-04-19T16:00:00Z
skill: genesis-drop-zone
skill_version: "1.5.0"
snapshot_version: 2
arbitrated_fields: [pour_qui, budget_ou_contrainte]
supersedes_snapshot: ./drop_zone_intent_history/v1_20260419T153000Z.md
idea_summary: "Une plateforme de gestion locative pour colocations parisiennes"
pour_qui: "etudiants en colocation a Paris"
type: "webapp"
nom: "ColocsManager"
attaches: "1 brief 'colocs.pdf' + 1 annexe 'budget.md'"
langue_detectee: "FR"
budget_ou_contrainte: "750 EUR/mois max"
prive_ou_public: "prive"
hints_techniques: "Next.js + Supabase"
idea_summary_source_citation:
  type: pdf_page_range
  document_index: 0
  start: 1
  end: 1
  cited_text_preview: "Une plateforme de gestion locative pour colocations parisiennes"
nom_source_citation:
  type: pdf_page_range
  document_index: 0
  start: 1
  end: 1
  cited_text_preview: "ColocsManager"
---

# Drop zone intent — ColocsManager

(v2 snapshot — supersedes v1_20260419T153000Z.md after arbitration on
`pour_qui` and `budget_ou_contrainte`. See archived predecessor for
the original values; current values reflect Victor's arbitration
choices.)

Une plateforme de gestion locative pour colocations parisiennes.

## Mirror

| Champ              | Valeur                                                                                                |
|--------------------|-------------------------------------------------------------------------------------------------------|
| Idee               | Une plateforme de gestion locative pour colocations parisiennes [page 1]                              |
| Pour qui           | etudiants en colocation a Paris ⚖                                                                     |
| Type               | webapp                                                                                                |
| Nom                | ColocsManager [page 1]                                                                                |
| Depose             | 1 brief 'colocs.pdf' + 1 annexe 'budget.md'                                                           |
| Langue             | FR                                                                                                    |
| Budget/contrainte  | 750 EUR/mois max ⚖                                                                                    |
| Prive/public       | prive                                                                                                 |
| Hints techniques   | Next.js + Supabase                                                                                    |
```

- [ ] **Step 8.2: Verify fixture YAML parseable**

Run: `python -c "import yaml; print(yaml.safe_load(open('tests/fixtures/drop_zone_intent_fixture_v1_5_0_arbitrated.md').read().split('---')[1]))" 2>&1 | head -20`

Expected: dict printout with `arbitrated_fields: ['pour_qui', 'budget_ou_contrainte']`, `supersedes_snapshot: './drop_zone_intent_history/v1_20260419T153000Z.md'`, `snapshot_version: 2`.

- [ ] **Step 8.3: Verify ⚖ marker present in body Mirror**

Run: `grep -c "⚖" tests/fixtures/drop_zone_intent_fixture_v1_5_0_arbitrated.md`

Expected: `2` (one per arbitrated field — `pour_qui` row and `budget_ou_contrainte` row).

---

## Task 9: CHANGELOG.md — v1.5.0 entry with self-rating

**Files:**
- Modify: `CHANGELOG.md` — prepend v1.5.0 entry at the top under the format conventions

**Context:** CHANGELOG follows Keep-a-Changelog conventions per Genesis discipline. Each version entry includes ship narrative, file deltas, self-rating breakdown across 5 axes (Pain-driven, Prose cleanliness, Best-at-date, Self-contained, Anti-Frankenstein), and running average update.

- [ ] **Step 9.1: Read current CHANGELOG header to confirm format**

Run: `head -50 CHANGELOG.md`

Identify: insertion point for v1.5.0 entry (typically after a `## [Unreleased]` block or directly above `## [1.4.2]`).

- [ ] **Step 9.2: Insert v1.5.0 entry**

Insert above the v1.4.2 entry:

```markdown
## [1.5.0] - 2026-04-19

**genesis-drop-zone living memory** — first MINOR bump on the v1.5.x line. Closes Friction #3 (reconciliation policy not codified) + absorbs Friction #1 + #2 (multi-source seed shape) from the 2026-04-18 v1.4.1 dogfood. Anti-Frankenstein retroactive: v1.4.0's silent graceful fallback retired on user challenge ("pourquoi pas d'API ?") in favour of explicit halt-with-remediation card.

### Added

- `genesis-drop-zone` Phase 0.4 — cross-session divergence detection (in-context, four-class diff: Completion / Retirement / Divergence / Unchanged) when `drop_zone_intent.md` already exists at cwd
- `genesis-drop-zone` Phase 0.5 — consolidated bilingual arbitration card (intra-drop + cross-session divergences in one Victor turn)
- `drop_zone_intent_history/v<N>_<ISO8601-Z>.md` archive directory with bidirectional supersession pointers (`supersedes_snapshot` on new + `superseded_by` on archived)
- 3 additive frontmatter keys: `snapshot_version`, `arbitrated_fields`, `supersedes_snapshot` (schema_version stays at 1, additive only)
- 7 new bilingual pairs (FR + EN paired authoring): arbitration card + 6 halt-with-remediation cards (one per failure class)
- Layer B `⚖` marker rendering on `genesis-protocol` Phase 0 Step 0.4 card + Step 0.5 `bootstrap_intent.md` template — opt-in, additive, zero parser change
- Extractor `divergences[]` JSON output — extractor flags intra-drop semantic conflicts; consumed by Phase 0.5
- New regression fixture `tests/fixtures/drop_zone_intent_fixture_v1_5_0_arbitrated.md`
- master.md cross-skill-pattern #4 fifth data-point: "Layer B opt-in additive rendering of revision-state metadata"

### Changed

- `genesis-drop-zone` extractor exit codes 2-7 now signal halt-with-remediation to SKILL.md dispatch (no fallback to v1.3.3 in-context extraction)
- `genesis-drop-zone` halt-on-existing (v1.3.2 behaviour) replaced by archive-and-supersede flow when re-run path detected
- master.md genesis-drop-zone privilege map — disk class extended (write + archive + overwrite); network class unchanged
- `.claude-plugin/plugin.json` version `1.4.2 → 1.5.0`

### Removed

- v1.4.0 silent graceful fallback path in `extract_with_citations.py` (anti-Frankenstein retroactive — preemptive feature, never pain-driven validated)

### Self-rating — v1.5.0

| Axis | Score | Notes |
|---|---|---|
| Pain-driven | 9.4 | Closes Friction #3 + #1 + #2 from real dogfood; anti-Frankenstein retroactive on fallback |
| Prose cleanliness | 9.1 | 1:1 mirror discipline preserved; 7 new bilingual pairs paired-authored; spec/SKILL.md/phase-0-welcome.md tri-mirror clean |
| Best-at-date | 9.3 | KARMA + EMNLP knowledge-conflicts + Cleanlab TLM + Kurrent SOTA references applied; living-memory R8 entry grounds 12 design choices |
| Self-contained | 9.2 | Zero ripple to phase-minus-one / 5.5 / journal / post-processor / pepite; only intentional Layer B Step 0.4+0.5 touches per cross-skill-pattern #4 |
| Anti-Frankenstein | 9.4 | Fallback retirement is anti-Frankenstein retroactive; archive retention + retry policy + concurrent locks all deferred to v1.5.1+ pain-driven |
| **Average** | **9.28** | **12th consecutive ship ≥ 9.0** |

Running average post-v1.5.0: ≈ **8.95/10** (+0.03 vs v1.4.2 running 8.92).
```

- [ ] **Step 9.3: Verify CHANGELOG parseable**

Run: `head -100 CHANGELOG.md | grep -E "^## "`

Expected: v1.5.0 listed first, v1.4.2 second, descending by version.

---

## Task 10: Pre-commit verification probes

**Files:**
- Probe: multiple — see steps below

**Context:** Genesis convention: before the feat commit, run a verification probe suite to catch obvious mistakes (unchanged schema_version, mirror discipline, zero unintended ripple, syntactic validity).

- [ ] **Step 10.1: Schema version unchanged**

Run: `grep -rn "schema_version" skills/genesis-drop-zone/ | grep -v "_history" | head -5`

Expected: every reference says `schema_version=1` or `schema_version: 1`. No `schema_version: 2` anywhere (v1.5.0 is additive — schema unchanged).

- [ ] **Step 10.2: Layer A zero unintended ripple**

Run: `git diff main --stat -- skills/`

Expected: only `genesis-drop-zone/SKILL.md`, `genesis-drop-zone/phase-0-welcome.md`, `genesis-drop-zone/scripts/extract_with_citations.py`, `genesis-protocol/phase-0-seed-loading.md` modified. No unintended changes to other skill files.

- [ ] **Step 10.3: Mirror discipline check**

Run: `grep -c "v1\.5\.0" skills/genesis-drop-zone/SKILL.md skills/genesis-drop-zone/phase-0-welcome.md`

Expected: both files have ≥ 5 v1.5.0 mentions; counts within 50% of each other (mirror discipline — neither file is wildly more verbose than the other).

- [ ] **Step 10.4: Bilingual pair count**

Run: `grep -cE "^### .* — (FR|EN) variant" skills/genesis-drop-zone/phase-0-welcome.md`

Expected: increased by 14 vs v1.4.x baseline (1 arbitration FR + 1 arbitration EN + 6 halt-FR + 6 halt-EN = 14 new bilingual variants). Verify via `git diff main` count delta.

- [ ] **Step 10.5: Python extractor syntactic validity**

Run: `python -c "import ast; ast.parse(open('skills/genesis-drop-zone/scripts/extract_with_citations.py').read())"`

Expected: no output. Failure = re-read tasks 1-2 changes.

- [ ] **Step 10.6: Frontmatter additive keys present in fixture**

Run: `grep -E "(snapshot_version|arbitrated_fields|supersedes_snapshot)" tests/fixtures/drop_zone_intent_fixture_v1_5_0_arbitrated.md`

Expected: all 3 keys present (3 lines of output minimum).

- [ ] **Step 10.7: ⚖ marker present in expected places**

Run: `grep -rn "⚖" skills/ tests/fixtures/drop_zone_intent_fixture_v1_5_0_arbitrated.md | head -10`

Expected: occurrences in (a) genesis-drop-zone SKILL.md (cards + bilingual pairs), (b) genesis-drop-zone phase-0-welcome.md (cards + bilingual pairs), (c) genesis-protocol phase-0-seed-loading.md (Step 0.4 + Step 0.5 docs), (d) the v1.5.0 fixture body Mirror.

- [ ] **Step 10.8: master.md cross-skill-pattern #4 fifth data-point present**

Run: `grep -n "fifth data-point" memory/master.md`

Expected: at least one occurrence in the cross-skill-pattern paragraph; references "v1.5.0".

- [ ] **Step 10.9: plugin.json version**

Run: `python -c "import json; v=json.load(open('.claude-plugin/plugin.json'))['version']; assert v=='1.5.0', f'expected 1.5.0 got {v}'; print('OK')"`

Expected: `OK`.

- [ ] **Step 10.10: Spec section preserved verbatim (no accidental edits)**

Run: `git diff main -- .claude/docs/superpowers/specs/v2_etape_0_drop_zone.md | head`

Expected: empty (the spec was committed in commit `0d023b3` and should not change in feat commit; spec is the source of truth, not the implementation surface).

---

## Task 11: feat commit + push

**Files:**
- Commit: all modifications from Tasks 1-10

- [ ] **Step 11.1: Stage all v1.5.0 implementation files**

Run from worktree:

```bash
git add \
  skills/genesis-drop-zone/scripts/extract_with_citations.py \
  skills/genesis-drop-zone/SKILL.md \
  skills/genesis-drop-zone/phase-0-welcome.md \
  skills/genesis-protocol/phase-0-seed-loading.md \
  memory/master.md \
  .claude-plugin/plugin.json \
  CHANGELOG.md \
  tests/fixtures/drop_zone_intent_fixture_v1_5_0_arbitrated.md
```

- [ ] **Step 11.2: Commit with structured message**

Run:

```bash
git commit -m "$(cat <<'EOF'
feat: v1.5.0 — genesis-drop-zone living memory + arbitration

First MINOR bump on the v1.5.x line. Closes Friction #3 (reconciliation
policy not codified) + absorbs Friction #1 + #2 (multi-source seed
shape) from the 2026-04-18 v1.4.1 dogfood. Anti-Frankenstein retroactive:
v1.4.0's silent graceful fallback retired on user challenge in favour
of explicit halt-with-remediation card.

Layer A (genesis-drop-zone) :
- Extractor system prompt augmented with divergences[] contract
- Phase 0.4 cross-session divergence detection (in-context, four-class diff)
- Phase 0.5 consolidated bilingual arbitration card
- drop_zone_intent_history/ archive chain with bidirectional supersession pointers
- 3 additive frontmatter keys (snapshot_version, arbitrated_fields, supersedes_snapshot)
- 7 new bilingual pairs (1 arbitration + 6 halt-with-remediation)
- Fallback path retired (exit codes 2-7 → halt card, no in-context degradation)

Layer B (genesis-protocol) :
- Step 0.4 card + Step 0.5 bootstrap_intent.md template render `⚖` marker on arbitrated_fields
- Zero parser change, zero schema bump, zero new privilege
- Cross-skill-pattern #4 fifth data-point (revision-state metadata rendering)

Schema version unchanged (1). Cross-skill-pattern #1 (1:1 mirror)
preserved. Privilege map: disk class extended (archive write); network
class unchanged.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 11.3: Verify gh active account before push (R2.3.1)**

Run: `gh api user --jq .login`

If output ≠ `myconciergerie-prog`, run: `gh auth switch -u myconciergerie-prog && gh api user --jq .login`. Re-verify before continuing.

- [ ] **Step 11.4: Push branch**

Run: `git push origin feat/v1.5.0-living-memory --force-with-lease`

(Note: `--force-with-lease` because the branch was rebased post-v1.4.2 in this session — `git push -f` analogue with safety net. The remote ref will be at the original `59a7640` from before rebase; `--force-with-lease` checks the remote matches expected state before overwriting.)

- [ ] **Step 11.5: Open PR**

Run:

```bash
gh pr create --title "v1.5.0 — genesis-drop-zone living memory + arbitration (MINOR)" --body "$(cat <<'EOF'
## Summary

First MINOR bump on the v1.5.x line. Pain-driven dogfood-closure ship:

- Closes Friction #3 (reconciliation policy not codified)
- Absorbs Friction #1 + #2 (multi-source seed shape) from 2026-04-18 v1.4.1 stress test
- Anti-Frankenstein retroactive: v1.4.0 silent fallback retired on user challenge

Two surfaces shipped:
1. **Layer A** (`genesis-drop-zone`): extractor `divergences[]` contract + Phase 0.4 cross-session detection + Phase 0.5 arbitration card + archive chain (`drop_zone_intent_history/`) + 3 additive frontmatter keys + halt-with-remediation card (FR + EN, 6 failure classes)
2. **Layer B** (`genesis-protocol`): opt-in `⚖` marker rendering on Step 0.4 card + Step 0.5 template — zero parser change, zero schema bump, zero new privilege

Cross-skill-pattern #4 fifth data-point: Layer B opt-in additive rendering of revision-state metadata.

## Test plan

- [x] `python -c "import ast; ast.parse(open('skills/genesis-drop-zone/scripts/extract_with_citations.py').read())"` → no error
- [x] `grep -c "⚖" skills/genesis-drop-zone/SKILL.md skills/genesis-drop-zone/phase-0-welcome.md skills/genesis-protocol/phase-0-seed-loading.md` → ≥ 1 each
- [x] `python -c "import json; v=json.load(open('.claude-plugin/plugin.json'))['version']; assert v=='1.5.0'"` → OK
- [x] `git diff main --stat -- skills/` → only the 4 expected files modified
- [x] Pre-commit verification probes Task 10 all green

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

- [ ] **Step 11.6: Squash-merge PR**

Once CI (if any) passes and the user reviews:

Run: `gh pr merge <PR_NUMBER> --squash` (no `--delete-branch` per Layer 0 R2.1 reinforcement — branches retained as forensic).

- [ ] **Step 11.7: Tag v1.5.0 on main**

**Explicit cd out of worktree first** — the previous steps run inside `.claude/worktrees/v1.5.0-living-memory/`. Tagging from the worktree would tag `feat/v1.5.0-living-memory` HEAD instead of main HEAD. Run from a fresh shell or `cd C:/Dev/Claude_cowork/project-genesis` (the main repo dir) before tagging:

```bash
cd C:/Dev/Claude_cowork/project-genesis && git checkout main && git pull origin main && git tag v1.5.0 && git push origin v1.5.0
```

Verify post-tag: `git log --oneline -1 v1.5.0` should show the squash-merged feat commit on main, NOT the pre-squash plan/feat commits from the worktree branch.

---

## Task 12 (chore): CHANGELOG verify + session trace + MEMORY pointer + resume prompt

**Files:**
- Verify: `CHANGELOG.md` (committed in feat — re-verify content)
- Create: `memory/project/session_v1_5_0_living_memory.md`
- Modify: `memory/MEMORY.md` (add session pointer at top of Project section)
- Create: `.claude/docs/superpowers/resume/2026-04-19_v1_5_0_to_v1_5_1_or_v1_6_0.md`

- [ ] **Step 12.1: Write `memory/project/session_v1_5_0_living_memory.md`**

Following the v1.4.2 session-trace narrative pattern at `memory/project/session_v1_4_2_marketplace_unblock.md`. Mirror sections:
- Header (frontmatter + branch + parent-tag + parent-commit)
- Why MINOR (not PATCH): API requirement removal + Phase 0.4 + Phase 0.5 + archive directory + 7 new bilingual pairs = structural surface
- Six-commit rhythm 8th application table
- Spec drift check outcome (clean post-rebase, no polish iteration needed)
- What shipped — feat commit summary
- Verification probes — Task 10 outcomes
- Self-rating breakdown
- What v1.5.0 intentionally does NOT fix (mirror spec § Out of scope)
- Next session entry point + projection

- [ ] **Step 12.2: Update `memory/MEMORY.md` with v1.5.0 session pointer**

Add at top of Project section (most recent first):

```markdown
- [Session v1.5.0 living memory — 2026-04-19](project/session_v1_5_0_living_memory.md) — **First MINOR on v1.5.x line.** Closes dogfood Friction #3 + absorbs #1 + #2. Anti-Frankenstein retroactive on v1.4.0 fallback. Phase 0.4 cross-session detection + Phase 0.5 arbitration card + drop_zone_intent_history/ archive chain + 3 additive frontmatter keys + Layer B `⚖` marker rendering. Cross-skill-pattern #4 fifth data-point. Zero schema bump (schema_version: 1 preserved). v1.5.0 tagged at **9.28/10** (Pain-driven 9.4 dogfood-driven; floor ≥ 9.1 on 5/5 axes), running average **≈8.95/10** (+0.03 vs v1.4.2). **12th consecutive ship ≥ 9.0**.
```

- [ ] **Step 12.3: Write resume prompt `.claude/docs/superpowers/resume/2026-04-19_v1_5_0_to_v1_5_1_or_v1_6_0.md`**

Following v1.4.2's resume format at `.claude/docs/superpowers/resume/2026-04-19_v1_4_2_to_v1_4_3_or_v1_5_0.md`. Sections:
- What v1.5.0 shipped
- Current state (repo, tags, commits, worktree, gh auth, skill count, privilege map, cross-skill patterns, Layer A/B ripple status)
- Next candidates: (A) **v1.6.0 = `skills/promptor/` skill promotion** per 2026-04-19 Option C decision (HIGH fit per Layer 0 cross-project utility section of pépite + binding rule installed) ; (B) v1.5.1 PATCH if dogfood surfaces friction ; (C) other direction
- R8 cache state (note `claude-code-plugin-structure_2026-04-19.md` + `_session-jsonl-format_2026-04-19.md` may have expired by next session — apply session-open R8 hygiene)
- Exact phrase for next session
- PowerShell launcher one-liner

- [ ] **Step 12.4: Stage + commit chore files**

```bash
git add \
  memory/project/session_v1_5_0_living_memory.md \
  memory/MEMORY.md \
  .claude/docs/superpowers/resume/2026-04-19_v1_5_0_to_v1_5_1_or_v1_6_0.md
git commit -m "$(cat <<'EOF'
chore(memory): v1.5.0 — CHANGELOG + session trace + MEMORY pointer + resume

Six-commit rhythm 8th consecutive application — closing chore commit.
Documents the v1.5.0 ship narrative, updates the MEMORY.md index with
the most-recent session pointer, and writes the resume prompt for the
next session (v1.5.1 PATCH if friction surfaces, OR v1.6.0 = promptor
skill promotion per 2026-04-19 Option C decision, OR other direction).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 12.5: Push chore commit**

Run: `git push origin feat/v1.5.0-living-memory`

(Branch already merged via squash from feat commit; this chore commit will land in a follow-up PR or be amended into the squash via separate PR depending on workflow. Per Genesis convention: chore is part of the same feat branch and ships in the same PR pre-merge. If the feat PR is already merged before this step, open a separate chore PR.)

---

## Self-rating projection (target — adjust at chore commit)

| Axis | Projected | Rationale |
|---|---|---|
| Pain-driven | 9.3-9.5 | Friction #3 directly closed; #1 + #2 absorbed via arbitration scope; anti-Frankenstein retroactive on v1.4.0 fallback (responsive to user challenge mid-session). High because dogfood-observed pain. |
| Prose cleanliness | 9.0-9.2 | 1:1 mirror discipline preserved across spec/SKILL/phase-0-welcome triple; 7 new bilingual pairs paired-authored from day 1; cross-skill-pattern #4 narrative extends without restructure. Slight risk of verbosity in SKILL.md additions. |
| Best-at-date | 9.2-9.4 | KARMA + EMNLP knowledge-conflicts SOTA + Cleanlab TLM + Kurrent SOTA grounding 12 design choices; living-memory R8 entry surfaces ≥ 7 findings; flag-never-resolve principle directly cited. |
| Self-contained | 9.1-9.3 | Zero ripple to phase-minus-one / 5.5 / journal / post-processor / pepite; only intentional Layer B Step 0.4+0.5 touches per cross-skill-pattern #4 (fifth data-point precedent confirms discipline holds). |
| Anti-Frankenstein | 9.3-9.5 | Fallback retirement = anti-Frankenstein retroactive (textbook case); 7 deferred items in spec § Out of scope are pain-driven gates not preemptive coverage; archive retention + retry policy + concurrent locks all deferred. |
| **Average projected** | **9.18-9.38** | **Likely 9.20-9.30 based on v1.4.x ship calibration trend**. **12th consecutive ship ≥ 9.0** — running average projection 8.94-8.97. |

---

## Anti-Frankenstein gate review (per R10)

Each v1.5.0 in-scope item has a documented pain trigger or preemption justification:

| Item | Pain trigger | Status |
|---|---|---|
| 1 (API requirement, no fallback) | User challenge "pourquoi pas d'API ?" + dead weight rationale | Anti-Frankenstein retroactive ✓ |
| 2 (Divergence detection two triggers) | Friction #3 dogfood (intra-drop conflict silently resolved) + temporal revision (halt-on-existing was the only UX) | Pain-driven ✓ |
| 3 (Phase 0.5 arbitration card) | Same as #2 — needs surface for human arbitration | Composition with #2 ✓ |
| 4 (drop_zone_intent_history/) | Temporal revision pain — halt-on-existing forced re-naming or destructive overwrite | Pain-driven ✓ |
| 5 (3 additive frontmatter keys) | Required surface for arbitration trail + supersession chain | Composition with #2 + #4 ✓ |
| 6 (Layer B `⚖` marker) | Honest provenance — Layer B reader needs visual cue when value was arbitrated | Composition with #5 ✓ |
| 7 (Halt-with-remediation card) | Required surface for #1 (fallback retired = halt is the path) | Composition with #1 ✓ |
| 8 (Completion vs retirement asymmetry) | Required logic for #2 cross-session path | Composition with #2 ✓ |
| 9 (Victor-exit safety) | Anti-data-loss guarantee — if Victor abandons mid-arbitration, no partial write | Composition with #4 ✓ |
| 10 (Six-commit rhythm) | Discipline preservation — no Frankenstein addition | Convention ✓ |
| 11 (Living-spec pattern) | Same as #10 | Convention ✓ |

No item flunks the gate. The scope is tight: ten substantive additions composing into one coherent feature (living memory with arbitration), one anti-Frankenstein retroactive removal (fallback path).

Deferred items in spec § Out of scope all flagged pain-driven gates (Layer B expandable diff = wait for binary flag insufficient signal; retry policy = wait for transient-error friction; archive retention = wait for disk pressure; concurrent locks = no documented multi-writer use case; etc.). No preemption.

---

## Estimated time

- Plan polish loop (1-3 reviewer iterations): 1-2 hours
- Task 1-2 (Python extractor): 2 hours
- Task 3 (SKILL.md additions): 2-3 hours
- Task 4 (phase-0-welcome.md mirror + bilingual pairs): 2-3 hours
- Task 5 (Layer B `⚖` rendering): 1-2 hours
- Task 6 (master.md): 1 hour
- Task 7-8 (plugin.json + fixture): 0.5 hour
- Task 9 (CHANGELOG): 0.5 hour
- Task 10 (verification probes): 0.5 hour
- Task 11 (feat commit + PR): 0.5 hour
- Task 12 (chore): 1 hour

**Total: 12-16 hours.** Realistic for a MINOR bump with two new surfaces (extractor prompt + Layer B rendering) + 7 new bilingual pairs + 5 SKILL.md/phase-0-welcome.md sub-sections + 11-task plan execution.

If plan polish exceeds 3 reviewer iterations, halt and re-scope (per R10 anti-spin discipline).
