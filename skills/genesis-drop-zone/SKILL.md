<!-- SPDX-License-Identifier: MIT -->
---
name: genesis-drop-zone
description: Layer A conversational front door for Genesis v2 project bootstrap — print the unified drop-zone welcome box, reformulate what the user gave in a token-streamed acknowledgement, close with an honest bilingual bridge. Invoked by the slash command /genesis-drop-zone or by natural-language intent phrases ("je veux créer un projet", "nouveau projet", "démarre un projet", "dis-moi comment commencer", "I want to create a project", "start a new project", "new project"). Only fires in a fresh context (no existing project in cwd) — inside an active project the skill prints a bilingual redirect and exits.
---

# Genesis Drop Zone

## Purpose

Genesis v1 is an engineer's protocol that speaks to engineers. The v2 vision adds a conversational Layer A where a non-technical user can open Claude Code, drop an idea in any form (text, PDF, photo, link, audio), and be met by a warm conversational surface instead of a config file. `genesis-drop-zone` is the first Layer A skill. v1.3.0 shipped the welcome + token-streamed acknowledgement + bridge vertical slice; v1.3.1 upgraded the acknowledgement into a structured 9-field mirror screen (in-context extraction of user intent, rendered as an aligned-column table revealed row by row, no API call, no disk write).

**v1.3.2 adds the first Layer A concentrated privilege**: after the mirror renders, a bilingual consent card offers to save the extracted intent as `drop_zone_intent.md` at cwd root. On accept, the skill writes the file and the accept bridge instructs the user to type `/genesis-protocol` for the Layer B bootstrap. On decline, no write occurs and the decline bridge leaves the idea in-session. `genesis-protocol` Phase 0 is extended to detect, parse, and consume `drop_zone_intent.md` as the primary seed (precedence over legacy `config.txt`) — this is the first cross-layer wire in the Genesis plugin.

**Canonical spec**: `.claude/docs/superpowers/specs/v2_etape_0_drop_zone.md` — a living spec that evolves across versions. This `SKILL.md` is a 1:1 mirror across all `Mirrored` rows of the spec's mirror map. When either file changes, the other follows — drift is a merge-blocker per cross-skill-pattern #1.

## Scope

### In scope (v1.3.0)

1. New sibling skill package `skills/genesis-drop-zone/` with this `SKILL.md` + `phase-0-welcome.md`.
2. Welcome ASCII box template, FR primary and EN mirror — both coauthored day 1 per R9. FR printed by default in v1.3.0.
3. Token-streamed acknowledgement template — pattern (not verbatim), reformulates text / PDFs / images / URLs in progressive bullets.
4. Bilingual bridge message closing the interaction honestly.
5. Trigger evaluation gate — slash + bilingual natural-language triggers + context guard.
6. Concentrated privilege declaration: `none`.

### In scope (v1.3.1)

1. In-context extraction of user intent into a 9-field schema (see `phase-0-welcome.md § Mirror template — FR` for the labels).
2. Mirror screen replaces v1.3.0's `◐ ... ✓` bullet-list acknowledgement. Aligned-column table, token-streamed row reveal.
3. Null-visible convention — every row always renders. Missing core fields → `a trouver ensemble`; missing bonus fields → `non mentionne(e)`; ambiguity → `a affiner — X ou Y`.
4. Bridge update — "Création du projet (GitHub, fichiers, mémoire) arrive bientôt" replaces v1.3.0's extraction-is-coming claim.
5. Failure-mode extensions — zero-content re-prompt preserved; unreadable-attachment row inside `Depose`; very-thin-content mirror with mostly null labels.
6. Truncation rules — row values ≤ 60 chars, `Depose` caps at 3 items + `+ N autres`.
7. Concentrated privilege stays `none` (no API call, no disk write, no subprocess).

### In scope (v1.3.2)

1. **First Layer A concentrated privilege** — write `drop_zone_intent.md` to cwd after the user accepts the consent card. Narrow by design: one file, cwd root only (no `mkdir`, no path resolution), halt-on-existing (no overwrite).
2. **Bilingual consent card** — minimal accept/cancel, absolute path with arrow marker, natural-language response routing (affirmative / negative / modification).
3. **`drop_zone_intent.md` file format** — YAML frontmatter (9 semantic fields + 4 metadata keys: `schema_version`, `created_at`, `skill`, `skill_version`) + Markdown body with FR prose intro + mirror echo. UTF-8 no BOM, LF line endings.
4. **Halt-on-existing protection** — bilingual halt message with absolute path + remediation; printed in place of the consent card; no overwrite, no timestamp-suffix, no second consent.
5. **Two version-scoped bridges** — accept bridge (instructs `/genesis-protocol`) and decline bridge (non-pressurizing). Supersede the v1.3.1 bridge.
6. **Layer B integration** — `genesis-protocol` Phase 0 Step 0.1 detects `drop_zone_intent.md`, new Step 0.2a parses and maps its 9 fields to Layer B schema (Vision, Project name, Slug, Is-a-plugin, Stack hints, Mixed media), Step 0.4 card extended with origin tags + `Additional context from drop zone` block, Step 0.5 `memory/project/bootstrap_intent.md` template extended with `## Conversational context from drop zone` section preserving the 4 Layer-A-specific extras (`pour_qui`, `langue_detectee`, `budget_ou_contrainte`, `prive_ou_public`).
7. **Concentrated privilege map update** — `genesis-drop-zone` switches from `none` to the v1.3.2 declaration in `memory/master.md`'s privilege map.

### In scope (v1.3.3)

1. **Runtime locale detection + dispatch** across Layer A surfaces via two variables with distinct lifecycles:
   - `welcome_locale` — resolved at skill invocation. From the trigger phrase language on intent-match (FR phrase → `FR`; EN phrase → `EN`); defaults to `FR` on slash invocation `/genesis-drop-zone` (no language signal).
   - `content_locale` — resolved from extracted `langue_detectee` after the first user turn with content. Mapping: `FR` → FR, `EN` → EN, `mixte` → FR (tiebreaker = primary project language).
2. **Locale-switched rendering** on seven surfaces (previously hardcoded FR + always-bilingual mixtures): welcome box (via `welcome_locale`), zero-content re-prompt (via `welcome_locale`), mirror + 9-field labels (via `content_locale`), consent card (via `content_locale`), halt message (via `content_locale`), accept bridge (via `content_locale`), decline bridge (via `content_locale`), and the `drop_zone_intent.md` body prose intro + mirror echo (via `content_locale`).
3. **Frontmatter data contract preserved** — `drop_zone_intent.md` frontmatter null-class tokens stay FR canonical (`"a trouver ensemble"`, `"non mentionne"`, `"non mentionnee"`, `"a affiner — ..."`) regardless of `content_locale`. Layer B Step 0.2a parser unchanged.
4. **One new bilingual pair** — the EN zero-content re-prompt `I'm listening — drop or write whatever you want to share.` pairs the v1.3.0 FR re-prompt. All other EN variants already exist (v1.3.0 welcome, v1.3.1 mirror + labels, v1.3.2 consent + halt + bridges).
5. **Concentrated privilege unchanged** — still writes `drop_zone_intent.md` to cwd after consent, halt-on-existing, no `mkdir`. Runtime rendering layer only.
6. **New EN fixture** — `tests/fixtures/drop_zone_intent_fixture_v1_3_3_en.md` covers EN body + FR canonical null tokens asymmetry for Layer B parser regression + EN body inspection.

### In scope (v1.4.0)

1. **Second concentrated privilege class** — external Anthropic Messages API call via Python subprocess at `skills/genesis-drop-zone/scripts/extract_with_citations.py`. Orthogonal to v1.3.2's disk class. Cross-skill-pattern #2 refined to "at most one concentrated privilege per operation class, per skill".
2. **Citations-enabled extraction** — the subprocess calls the API with `citations: {enabled: true}` per document block and `cache_control: {type: "ephemeral", ttl: "1h"}`. Mandatory 1h TTL explicit per R8 § Stage 2 (guards against March 2026 Anthropic default TTL regression).
3. **Mirror annotation** — each field optionally carries a `[page N]` (PDF) or `[lines X-Y]` (plain-text) suffix when a citation is available. ASCII-safe, language-neutral. Image-only drops produce no citations (by design — Citations API does not cite images).
4. **Frontmatter schema extension** — `drop_zone_intent.md` gains optional nested keys `<field>_source_citation` with shape `{type, document_index, start, end, cited_text_preview}`. Key omitted (not written as `null`) when no citation applies. `schema_version` stays at `1` — additive and backward-compatible.
5. **Graceful fallback** — four triggers commit to the v1.3.3 in-context extraction path: (a) `ANTHROPIC_API_KEY` unset at skill entry; (b) Python runtime unresolvable; (c) subprocess exit code ≠ 0; (d) subprocess stdout fails shape validation. Fallback is silent — no user-facing note.
6. **Five mitigations** for the network privilege class — pre-flight env check at skill entry; subprocess isolation; explicit 1h cache TTL; token-budget logging to stderr (forensic only); silent graceful fallback.
7. **Typed-text wrapping** — non-empty inline `typed_text` is wrapped in a synthetic citations-enabled document block at index 0 of the `documents[]` array. Attachments follow at indices 1..N.
8. **Three new fixtures** — `tests/fixtures/drop_zone_intent_fixture_v1_4_0_fr_with_citations.md`, `drop_zone_intent_fixture_v1_4_0_en_with_citations.md`, and `drop_zone_intent_fixture_v1_4_0_fallback.md` (byte-identical to `drop_zone_intent_fixture_v1_3_3_en.md` modulo `skill_version`).
9. **MINOR semver bump** — v1.3.3 → v1.4.0. Second privilege class + first external dependency (`ANTHROPIC_API_KEY`, Anthropic Python SDK) + first subprocess invocation in `genesis-drop-zone` justify the tranche.
10. **R8 stack entry** — `stack/anthropic-python_2026-04-18.md` pins the SDK version at ship time (TTL 1 day per stack convention).

### Out of scope (deferred to v1.4.1+)

- **Layer B citation surfacing** — the `_source_citation` entries are persisted at Layer A in v1.4.0 but not displayed in Layer B's Step 0.4 card or Step 0.5 `bootstrap_intent.md` template. Additive v1.4.1 if pain emerges.
- **Files API (beta)** — v1.4.0 uses inline base64 document blocks. Files API beta (`anthropic-beta: files-api-2025-04-14`) deferred until dedup or large-file cases warrant it.
- **Image source citations** — Citations API does not cite images. No pseudo-citation synthesized; field renders without annotation.
- **Structured Outputs (Path B)** — mutually exclusive with Citations. Path A committed for v1.4.x; Path B is a v2 architectural pivot question, not a v1.4.x option.
- **Contradictions array** — cross-document conflict surfacing. v1.5+ if multi-document drops become common.
- **Chain-of-Verification (CoVe) second pass** — R8 recommends skipping unless evals demand. Skip.
- Programmatic handoff — auto-invoke `genesis-protocol` without user typing the slash command.
- `GH_BROWSER` profile routing.
- UX toolkit integration (@clack/prompts, Charm Gum, cli-spinners).
- Completion chime (cross-platform).
- Error handling refinements (permission-denied / disk-full / symlink edge cases on the filesystem side; API-side errors have their own fallback per § "Fallback triggers").
- **Bilingual Layer B null-class parsing** — v1.5+ target.
- **Three-locale-or-more expansion** — deferred until a real non-FR/EN user emerges.

The v1.3.3 ship closes R9 tier-3 rendering loop end-to-end. v1.4.1+ refines remaining polish items.

The v1.4.0 ship introduces the second concentrated privilege class (network) with graceful fallback to v1.3.3 in-context extraction. v1.4.1+ refines remaining polish items (Layer B citation surfacing, UX toolkit, chime, error-handling).

## Trigger

The skill is invoked in two ways.

**Slash**: `/genesis-drop-zone` — deterministic, scriptable, testable. Used by engineers, Genesis-dev sessions, integration tests.

**Natural-language intent match**: Claude auto-invokes the skill when the current user turn matches one of the phrases declared in this file's frontmatter `description:`. Matching is Claude's standard intent evaluation — the skill lists the phrases, Claude decides. Bilingual coverage per R9:

| Language | Phrases |
|---|---|
| FR | "je veux créer un projet", "nouveau projet", "démarre un projet", "dis-moi comment commencer" |
| EN | "I want to create a project", "start a new project", "new project" |

**Invoke only when the user is starting from nothing.** If the user is already mid-task, mid-feature, or troubleshooting an existing project and happens to utter a trigger phrase in passing, do not invoke. The context guard below is a second layer of protection but the primary filter is this intent evaluation — the skill is for fresh-start moments, not casual mentions.

## Context guard

Before printing the welcome box, evaluate `is_fresh_context`. It is `true` if **all three** of the following hold:

- cwd has no `CLAUDE.md` at its root, AND
- cwd has no populated `memory/` directory (directory absent, or present but with fewer than 2 non-template files), AND
- either cwd is not a git repository, or `git rev-list --count HEAD` returns fewer than 3.

All three are AND-conjoined — a single `false` disables the welcome. No disjunction, no precedence to parse.

If `is_fresh_context` is `false`, do not print the welcome. Print this redirect instead (both languages, always):

```
Tu es déjà dans un projet — la drop zone est réservée aux nouveaux projets.
Si tu veux en démarrer un autre, ouvre Claude Code dans un dossier vide.

You're already in a project — the drop zone is reserved for new projects.
To start another one, open Claude Code in an empty folder.
```

No halt, no error, no stack trace — just a graceful bilingual redirect and clean exit. The redirect stays always-bilingual by design: it fires before any `welcome_locale` resolution, so printing both languages covers any user who reaches it.

## Locale dispatch (v1.3.3)

v1.3.3 wires two locale variables governing Layer A rendering. Each has a distinct lifecycle, a distinct signal source, and a distinct set of render targets.

### `welcome_locale` — resolved at skill invocation

**Signal sources** (evaluated in order, first match wins):

1. **Intent-match trigger phrase**: if the skill was auto-invoked by a natural-language intent phrase, the phrase's language sets `welcome_locale`. FR phrases (`je veux créer un projet`, `nouveau projet`, `démarre un projet`, `dis-moi comment commencer`) → `FR`. EN phrases (`I want to create a project`, `start a new project`, `new project`) → `EN`.
2. **Slash command**: if the skill was invoked by `/genesis-drop-zone`, no language signal is available. `welcome_locale` defaults to `FR` (primary project language, matches trigger-list ordering).

**Render targets**:

- Welcome ASCII box (FR or EN variant from `phase-0-welcome.md`).
- Zero-content re-prompt (FR `Je t'écoute...` or EN `I'm listening...`).

### `content_locale` — resolved after first content turn

**Signal source**: the `langue_detectee` field extracted from the user's first content turn via the v1.3.1 9-field extraction mechanism. Three-value mapping:

| `langue_detectee` | `content_locale` |
|---|---|
| `FR` | `FR` |
| `EN` | `EN` |
| `mixte` | `FR` (tiebreaker) |

**Render targets**:

- Mirror template + 9-field labels (FR or EN variant).
- Consent card (FR or EN variant — v1.3.2 was always-bilingual; v1.3.3 prints one).
- Halt message (FR or EN variant).
- Accept bridge (FR or EN variant).
- Decline bridge (FR or EN variant).
- `drop_zone_intent.md` body — prose intro + mirror echo.

### Divergence between `welcome_locale` and `content_locale`

The two variables are deliberately independent. A user who auto-triggers with `je veux créer un projet` (FR welcome) and then drops an EN brief (`langue_detectee = EN`, `content_locale = EN`) sees an FR welcome, then mirror-onwards in EN. The inverse is equally possible. No forced consistency — each surface honours the best signal available when it renders.

### Frontmatter data contract unchanged

`drop_zone_intent.md` frontmatter null-class tokens stay **FR canonical** regardless of `content_locale`:

- `"a trouver ensemble"` (core missing)
- `"non mentionne"` (bonus missing, masculine)
- `"non mentionnee"` (bonus missing, feminine)
- `"a affiner — X ou Y"` (ambiguity)

Layer B's Step 0.2a parses these verbatim. The asymmetry (body = locale-detected human echo; frontmatter = FR canonical data contract) is intentional. Bilingual Layer B parser is a v1.4+ target.

### Zero-content branch

If the user's first response contains only the trigger phrase (no content), `content_locale` cannot be resolved. The skill stays in `welcome_locale` for the re-prompt and continues to wait. When content eventually arrives, `content_locale` is resolved at mirror time.

### Modification-loop branch (v1.3.2 consent card)

When the user replies to the consent card with a modification (`garde Type en boulangerie`), the skill re-runs the 9-field extraction with the correction, re-renders the mirror, and re-prints the consent card. `content_locale` is re-evaluated on each extraction; if the correction shifts `langue_detectee`, subsequent surfaces switch locale.

## Citations API dispatch (v1.4.0)

v1.4.0 layers an optional API-powered extraction path on top of the v1.3.1 in-context extraction. When `ANTHROPIC_API_KEY` is present at skill entry, the skill launches a Python subprocess that calls the Anthropic Messages API with `citations: {enabled: true}` per document block. Per-field source attribution (`[page N]` for PDF, `[lines X-Y]` for plain-text documents) is rendered inline in the mirror and persisted as optional `<field>_source_citation` nested keys in `drop_zone_intent.md`. When the key is absent or the subprocess fails for any reason, the skill routes through a silent graceful fallback to v1.3.3 in-context extraction.

### Dispatch lifecycle

Three gates are evaluated in order at skill entry (before the welcome box prints):

1. `is_fresh_context` — unchanged from v1.3.0 (see `## Context guard`). Controls whether the welcome prints at all.
2. `welcome_locale` — unchanged from v1.3.3 (see `## Locale dispatch (v1.3.3)`). Controls welcome + zero-content re-prompt rendering.
3. `api_extraction_available` (new in v1.4.0) — a boolean resolved by checking `ANTHROPIC_API_KEY` in the environment. If unset or empty, `false`; if set, `true`. The flag is evaluated **once** at skill entry and is **immutable for the session** — mid-session env changes are out of scope.

### Python extractor — invocation contract

The extractor lives at `skills/genesis-drop-zone/scripts/extract_with_citations.py`. The SKILL.md dispatch launches it via `Bash` using the Python portability pattern established by `session-post-processor/run.py`:

```bash
PYTHON=$(command -v python || command -v python3 || command -v py)
```

If no Python is found on `$PATH`, fall back to the v1.3.3 in-context extraction path (same as if `api_extraction_available` had been `false` at skill entry).

**Input** (stdin, single JSON object): `cwd` (string, absolute), `attachments` (array of strings), `typed_text` (string), `content_locale_hint` (FR / EN / mixte), `model` (string, default `claude-opus-4-7`, overridable via env).

**Output (exit 0)**: single JSON object on stdout with `schema_version` (int, `1`), the 9 semantic fields, optional `<field>_source_citation` nested entries (key omitted when no citation applies), and `usage` mirroring the SDK response's token counts.

**Exit codes**:

| Exit | Meaning | SKILL.md response |
|---|---|---|
| `0` | Success — valid JSON on stdout | Parse, proceed with citation-annotated mirror |
| `2` | `ANTHROPIC_API_KEY` unset at subprocess runtime | Fallback |
| `3` | SDK import error (`anthropic` not installed) | Fallback |
| `4` | API error (4xx / 5xx not 429) | Fallback |
| `5` | Rate limit (429) — retries exhausted | Fallback |
| `6` | Bad input (malformed stdin JSON / missing key) | Fallback |
| `7` | Output JSON shape invalid | Fallback |
| other | Unknown error | Fallback |

All fallback paths are silent to the user. Subprocess stderr surfaces at the harness-visible stderr for developer inspection.

### Typed-text citation wrapping

The Anthropic Citations API produces `cited_text` only for content carried in a `document` block with `citations: {enabled: true}`. Inline user text arriving as `typed_text` is not citeable by default. v1.4.0 wraps non-empty `typed_text` as a synthetic document block at index 0 of the `documents[]` array sent to the API:

```python
{
    "type": "document",
    "source": {"type": "text", "media_type": "text/plain", "data": typed_text},
    "title": "User typed text",
    "context": "Inline conversational input from the drop-zone turn.",
    "citations": {"enabled": True},
    "cache_control": {"type": "ephemeral", "ttl": "1h"},
}
```

Document-array ordering: typed-text synthetic document at index 0 (if `typed_text` non-empty), followed by one document block per file in `attachments[]` (indices 1..N for PDFs and text files). Image blocks are a different content-block type and do NOT carry the `citations` flag — Citations API does not cite images. If `typed_text` is empty, attachment documents start at index 0. Citation output uses `document_index` referring to this assembled array.

### Fallback triggers

The dispatch commits to the v1.3.3 in-context extraction path under any of:

1. `api_extraction_available` is `false` at skill entry (pre-flight env check negative).
2. Python runtime unresolvable at subprocess launch.
3. Subprocess exit code ≠ 0.
4. Subprocess exit code `0` but stdout is not valid UTF-8 JSON, or is JSON but fails shape validation (missing required keys, wrong types).

Fallback is silent. The mirror renders v1.3.3-identical output (no `[page N]` / `[lines X-Y]` annotations). `drop_zone_intent.md` is written without any `<field>_source_citation` keys on the fallback path.

### Citation object shape

Per-field citation, when present in the extractor's output JSON:

```yaml
idea_summary_source_citation:
  type: pdf_page_range      # pdf_page_range | text_char_range
  document_index: 0          # zero-based index into the documents[] array
  start: 1                   # 1-indexed page (PDF) or 0-indexed char offset (text)
  end: 1                     # inclusive
  cited_text_preview: "..."  # <= 80 chars, truncated with ellipsis
```

Rendered in the mirror as `[page N]` (PDF) or `[lines X-Y]` (text, derived from char offsets via `\n` counting). Annotation is language-neutral ASCII — brackets, digits, dash, space. Image sources never produce citations (the Citations API does not cite images); the row renders without annotation.

**Truncation rule interaction**: the v1.3.1 mirror truncation rule (row value ≤ 60 chars, truncate at 57 + `...`) applies to the *value* before the annotation. The annotation appends after the ellipsis and may push the row over 60 chars — this is the single exception to the truncation rule. Annotated rows may reach 75 characters in the worst case; still fits within 80-col terminals.

### Environment variables

| Variable | Default | Effect |
|---|---|---|
| `ANTHROPIC_API_KEY` | unset → fallback | Presence unlocks the API extraction path |
| `GENESIS_DROP_ZONE_MODEL` | `claude-opus-4-7` | Override active model. Any Messages-API-compatible model ID. |
| `GENESIS_DROP_ZONE_CACHE_TTL` | `1h` | Override cache TTL. Accepts `5m` or `1h`. Never defaulted to `5m` by omission — R8 § Stage 2 mandate against silent Anthropic TTL regression. |
| `GENESIS_DROP_ZONE_VERBOSE` | unset | If `1`, detailed stderr tracing per phase. Default: one usage line per call. |

### Modification-loop interaction

When the user replies to the consent card with a modification, the skill re-invokes the extractor subprocess on each iteration. Citations are re-computed. The 1h cache TTL keeps the document block resident across iterations — typical modification-loop re-run cost is ~0.1× of the first call per R8 § Stage 2 cache economics.

If `ANTHROPIC_API_KEY` is revoked mid-session (user unsets externally — out-of-scope), `api_extraction_available` stays `true` (the gate is immutable). The subprocess launches on the next iteration, hits exit code `2` at its own env check, and the dispatch routes through the fallback path via the exit-code-≠-0 trigger. The re-printed consent card does not indicate the path change.

### Zero Layer B ripple preserved

v1.4.0 touches **zero Layer B files**. Layer B's `phase-0-seed-loading.md` Step 0.2a parser is dict-based YAML parsing — unknown `<field>_source_citation` keys are silently ignored. `schema_version` stays at `1`. Fallback-path files are byte-identical to v1.3.3 files modulo `skill_version`. API-path files carry the additional keys without removing or renaming any existing key, without bumping schema_version. Layer B v1.4.1+ may add card / template surfacing of the citations additively if real user pain emerges.

## Phase 0 — welcome

Print the welcome ASCII box from `phase-0-welcome.md`. Locale dispatch: use the FR variant when `welcome_locale = FR`, the EN variant when `welcome_locale = EN` (see `## Locale dispatch (v1.3.3)` above). Do not inline the template here — it lives in the phase body file so bilingual audit greps have a single target.

After printing the box, wait for the user's next conversational turn. Do not prompt, do not block, do not spin a loading indicator — the welcome box is itself the invitation. The user's next message (text, text + attached files, text + URL, or any combination) feeds the acknowledgement step below.

## Phase 0 — mirror

When the user's response arrives, extract the 9-field intent schema from the dropped content (text, PDFs, images, URLs — all read via multimodal). **v1.3.3**: resolve `content_locale` from the extracted `langue_detectee` value, then render the FR variant of the mirror template when `content_locale = FR` (from `phase-0-welcome.md § "Mirror template — FR"`) or the EN variant when `content_locale = EN` (from `phase-0-welcome.md § "Mirror template — EN"`). Reveal rows progressively (Ably token-streaming pattern).

**v1.4.0 extraction-source dispatch**: when `api_extraction_available` is `true`, the skill launches the Python subprocess at `skills/genesis-drop-zone/scripts/extract_with_citations.py` to produce the 9-field extraction with per-field citations (see `## Citations API dispatch (v1.4.0)` above). When the subprocess returns successfully (exit 0, valid JSON, shape check passes), each field with a citation receives a `[page N]` (PDF source) or `[lines X-Y]` (text source) annotation appended to its row value in the mirror. Rows without citations (image sources, fallback path, or fields the API did not cite) render without annotation — v1.3.3 parity. Annotations are language-neutral ASCII (brackets, digits, dash, space). On any fallback trigger, the mirror renders v1.3.3-identical output with no user-facing indication of the path difference.

**v1.4.0 mirror truncation exception**: the v1.3.1 truncation rule (row value ≤ 60 chars, truncate at 57 + `...`) applies to the value *before* the annotation. When an annotation is appended, the total row may exceed 60 chars (worst case ~75 chars, still within 80-col terminals). This is the single exception to the truncation rule — truncating the annotation would hide the audit-trail.

The schema:

| Field | Label FR | Label EN | Semantic |
|---|---|---|---|
| `idea_summary` | Idee | Idea | 1-line synopsis in user's words |
| `pour_qui` | Pour qui | Who for | Target users / audience |
| `type` | Type | Kind | Category (app / tool / site / plugin / doc / …) |
| `nom` | Nom | Name | Proposed project name (explicit, not auto-slugged) |
| `attaches` | Depose | Dropped | Dropped items with brief descriptor |
| `langue_detectee` | Langue | Language | FR / EN / mixte detected from text |
| `budget_ou_contrainte` | Budget | Budget | Budget / deadline / constraint mention |
| `prive_ou_public` | Visibilite | Visibility | Private / public / team-only mention |
| `hints_techniques` | Tech | Tech | Tech stack hints mentioned or inferred |

**Null-visible convention** — every row always prints. Three null classes:

- `a trouver ensemble` — core field missing (signals Étape 1 Q&A to come). Used for `pour_qui`, `type`, `nom`.
- `non mentionne(e)` — bonus field missing (not-blocking). Used for `budget_ou_contrainte`, `prive_ou_public`, `hints_techniques`.
- `a affiner — <two or more hypotheses>` — ambiguity needing user arbitrage.

**Zero-content branch**: if the user's response contains only the trigger phrase with no content, do NOT print the `◐` line or the table. Instead re-prompt in `welcome_locale` — **v1.3.3** dispatches: FR re-prompt `Je t'écoute — dépose ou écris ce que tu veux me partager.` when `welcome_locale = FR`; EN re-prompt `I'm listening — drop or write whatever you want to share.` when `welcome_locale = EN` (newly-authored in v1.3.3). Wait for the user's next turn. No `✓` closure in that branch.

**Unreadable-attachment branch**: if Claude cannot read an attached file (exotic binary, oversize PDF past the 32 MB × 600 pages Files API limits), the `Depose` / `Dropped` row lists it alongside readable items: `Depose        1 brief "X" + 1 fichier illisible : <filename>`. Extraction of the other 8 fields continues from readable content.

**Truncation**: each row value ≤ 60 chars after the label. Longer → truncate at 57 + `...`. `Depose` lists at most 3 items; beyond 3, append `+ N autres`.

**Schema persistence**: v1.3.1 holds the schema in Claude's conversational context only — no disk write, no JSON serialization, no external consumer. v1.3.2+ persists to `bootstrap_intent.md` for handoff to `genesis-protocol`.

## Phase 0 — bridge

v1.3.1 shipped a single bridge printed after every successful mirror. **v1.3.2 supersedes the v1.3.1 bridge** with two version-scoped variants — an accept bridge after a successful write, and a decline bridge after user refusal. Runtime selection is driven by the response to the v1.3.2 consent card (see `## Phase 0 — consent card (v1.3.2, v1.3.3 locale-switched)` below). **v1.3.3**: each bridge variant now dispatches on `content_locale`; only one language variant prints per surface instead of always-bilingual (see `## Phase 0 — bridges (v1.3.2, v1.3.3 locale-switched)` below).

See `phase-0-welcome.md § "Accept bridge (v1.3.2, v1.3.3 locale-switched)"` and `phase-0-welcome.md § "Decline bridge (v1.3.2, v1.3.3 locale-switched)"` for exact text per locale variant.

The v1.3.1 bridge at `phase-0-welcome.md § "Bridge message (v1.3.1 ...)"` is preserved as regression context but is not reached in a v1.3.2 / v1.3.3 session.

## Phase 0 — consent card (v1.3.2, v1.3.3 locale-switched)

Printed between the mirror's `✓ Lu et compris.` / `✓ Read and understood.` closing line and the write. The absolute cwd path is resolved at prompt time — use `Bash` with `pwd` (POSIX) / `%CD%` (Windows PowerShell) / or read `$PWD` from the runtime environment. The path separator follows platform convention.

**v1.3.3 locale dispatch**: v1.3.2 printed both FR and EN blocks always. v1.3.3 prints only the FR variant when `content_locale = FR`, only the EN variant when `content_locale = EN`. See `phase-0-welcome.md § "Consent card (v1.3.2, v1.3.3 locale-switched)"` for the exact templates per locale variant. Response routing is natural-language per three equivalence classes:

- **Affirmative** (`oui`, `yes`, `y`, `ok`, `d'accord`, `go`, `garde`, `écris`, `save`, `keep`) → proceed to `## Phase 0 — write flow (v1.3.2)`.
- **Negative** (`non`, `no`, `n`, `cancel`, `annule`, `abort`, `stop`, `nope`) → proceed to decline bridge, no write.
- **Modification** (e.g. `garde Type en boulangerie`) → re-run the 9-field extraction with the correction applied, re-render the mirror with updated rows, re-print this consent card. `content_locale` is re-evaluated on each re-extraction; if the correction shifts `langue_detectee`, the re-printed consent card switches locale. Loop until convergence.

No iteration cap on modifications — the card is the only gate. The consent card is the single point of user intent before a concentrated privilege fires.

## Phase 0 — drop_zone_intent.md file (v1.3.2, v1.3.3 body locale-switched)

The file written to cwd on consent. YAML frontmatter + Markdown body. UTF-8 without BOM, LF line endings.

**v1.3.3 split**: the body prose intro + mirror echo now render in `content_locale` (FR when content is FR, EN when content is EN). **Frontmatter is unchanged** — keys stay snake_case English, null-class tokens stay FR canonical (`"a trouver ensemble"`, `"non mentionne"`, `"non mentionnee"`, `"a affiner — ..."`) regardless of `content_locale`. Deliberate Layer A / Layer B contract asymmetry: body = locale-detected human echo; frontmatter = FR canonical data contract parsed by Layer B's Step 0.2a.

### Schema

| Frontmatter key | Type | Purpose |
|---|---|---|
| `schema_version` | integer | `1` for v1.3.2+. Increment only if schema incompatibly changes (null-class token change would be one; v1.3.3 does NOT change schema). |
| `created_at` | string | ISO-8601 UTC timestamp at write time. |
| `skill` | string | Constant `genesis-drop-zone`. |
| `skill_version` | string | Read from `.claude-plugin/plugin.json` at write time (`1.4.0` for this ship). |
| `idea_summary` | string | 1-line synopsis of the user's idea. Null-class `"a trouver ensemble"` if content is zero (mirror guard ensures this only happens at degenerate fallback). |
| `pour_qui` | string | Target users / audience. Null-class `"a trouver ensemble"` if missing. |
| `type` | string | Kind of project (app, tool, site, plugin, etc.). Null-class `"a trouver ensemble"` if missing. |
| `nom` | string | Proposed project name. Null-class `"a trouver ensemble"` if missing. |
| `attaches` | string | Mirror `Depose` row verbatim — truncated display, may include `+ N autres`. `"texte seul"` if nothing attached. |
| `langue_detectee` | string | `FR` / `EN` / `mixte`. Always filled. |
| `budget_ou_contrainte` | string | Budget / constraint mention. Null-class `"non mentionne"` if missing (bonus). |
| `prive_ou_public` | string | Private / public / team-only mention. Null-class `"non mentionnee"` if missing (bonus, feminine agreement). |
| `hints_techniques` | string | Tech stack hints. Null-class `"non mentionne"` if missing (bonus). |

Three null classes serialized verbatim as strings: `"a trouver ensemble"`, `"non mentionne"`, `"non mentionnee"`, `"a affiner — X ou Y"`. Never `null`, never `~`, never empty string.

**v1.4.0 additive frontmatter extension**: when the API extraction path runs successfully and fields receive citations, the frontmatter gains optional nested entries `<field>_source_citation` (e.g. `idea_summary_source_citation`) with shape `{type, document_index, start, end, cited_text_preview}`. The keys are **omitted** (not written as `null`) for fields without citations — this keeps fallback-path files byte-identical to v1.3.3 files modulo `skill_version`. `schema_version` stays at `1` — the addition is purely additive and backward-compatible with Layer B's Step 0.2a parser (dict-based YAML parsers ignore unknown keys naturally).

See the canonical spec `.claude/docs/superpowers/specs/v2_etape_0_drop_zone.md § "drop_zone_intent.md — schema + body format (v1.3.2)"` for the full template and the concrete illustrative example. See `## Citations API dispatch (v1.4.0) § "Citation object shape"` above for the v1.4.0 citation entry shape.

## Phase 0 — write flow (v1.3.2)

State machine from mirror close through skill exit.

### Sequence

1. Mirror closes with `✓ Lu et compris.` (v1.3.1 path).
2. **Pre-write existence check** — use `Bash` with `test -e "$(pwd)/drop_zone_intent.md"`. If present → halt branch (see `## Phase 0 — halt branch (v1.3.2)`). If absent → proceed.
3. **Consent card prints** (see `## Phase 0 — consent card (v1.3.2)`).
4. **User response routes**:
   - Affirmative → write flow.
   - Negative → decline bridge, exit clean.
   - Modification → re-extract + re-render mirror + re-print consent card, loop.
5. **Write flow (on affirmative)**:
   - Resolve absolute target path: `<cwd>/drop_zone_intent.md`.
   - Compose full file content per `## Phase 0 — drop_zone_intent.md file (v1.3.2)`.
   - Use the `Write` tool to create the file at the target path. The Write tool is harness-atomic for small files (< 10 KB typical); no temp+rename needed at runtime.
   - **Post-write verification** — use `Bash` with `test -s <target>` to confirm the file exists and has non-zero size. If verification fails, print a bilingual failure message ("la sauvegarde a échoué, rien n'a été écrit / save failed, nothing written") and exit without printing the accept bridge. Let any `OSError`-class exceptions bubble up for harness visibility.
   - Print the accept bridge (see `## Phase 0 — bridges (v1.3.2)`).
   - Exit clean.

### Error handling scope — what v1.3.2 does NOT custom-handle

Per narrow-privilege anti-Frankenstein discipline:

- Permission denied on cwd (user opened Claude Code in a read-only folder) — `OSError` propagates via the harness, no custom halt.
- Disk full — same.
- `drop_zone_intent.md` is a symlink or directory — the `test -e` check at step 2 catches both as "file exists" and routes to the halt branch (safe default).
- Cwd deleted mid-flight — `OSError` at write time.

Real pain in any of these is a v1.3.3+ refinement target.

## Phase 0 — halt branch (v1.3.2, v1.3.3 locale-switched)

Fires when the pre-write existence check at step 2 of the write flow finds an existing `drop_zone_intent.md` in cwd. The mirror has already rendered at this point — Victor sees what was extracted from his content, then learns the write cannot proceed.

**v1.3.3 locale dispatch**: render the FR variant of the halt message when `content_locale = FR`, the EN variant when `content_locale = EN`. See `phase-0-welcome.md § "Halt message (v1.3.2, v1.3.3 locale-switched)"` for the exact templates per variant.

Behaviour:

- Printed **in place of** the consent card — the user never sees an accept/cancel prompt when the halt fires.
- Exit clean immediately after. No stack trace, no error code, no retry loop.
- No overwrite, no timestamp-suffix fallback, no second consent prompt for a destructive overwrite.

The context guard has already asserted a fresh cwd at skill entry — an existing `drop_zone_intent.md` is unexpected state that the user should reconcile manually (delete the file or change cwd). Halt + remediation is the honest signal.

## Phase 0 — bridges (v1.3.2, v1.3.3 locale-switched)

Two version-scoped bridges replace the v1.3.1 single bridge at runtime. Selection is determined by the consent card response. **v1.3.3** dispatches each bridge on `content_locale` — one variant printed, not both.

- **Accept bridge** — printed after a successful write. See `phase-0-welcome.md § "Accept bridge (v1.3.2, v1.3.3 locale-switched)"` for exact text per locale variant. Instructs the user to type `/genesis-protocol`. Path not repeated (consent card just showed it).
- **Decline bridge** — printed after a negative response. See `phase-0-welcome.md § "Decline bridge (v1.3.2, v1.3.3 locale-switched)"`. Warm, non-pressurizing — invites the user to return.

Accent discipline: plain-prose, accents preserved, UTF-8-stable stream path. Per-locale variants preserve the accent discipline unchanged from v1.3.2.

## Phase 0 — handoff to genesis-protocol (v1.3.2)

The user-visible handoff is the accept bridge's instruction (`tape /genesis-protocol`). When the user subsequently invokes `genesis-protocol` in the same cwd, Phase 0 detects and consumes `drop_zone_intent.md` per the cross-layer contract below.

### Precedence rule

Phase 0 Step 0.1 checks for seeds in this order:

1. `drop_zone_intent.md` present → **primary seed**. Parsed via YAML frontmatter in Step 0.2a.
2. No `drop_zone_intent.md`, `config.txt` present → **legacy seed**. Parsed via free-form text (existing Step 0.2).
3. Both present → **drop_zone_intent.md wins**. Phase 0 logs: `config.txt found but drop_zone_intent.md takes precedence — ignoring config.txt`. Never silent merge.
4. Neither present → interactive seed card (existing Step 0.2 fallback).

### Field mapping

| Layer A frontmatter | Layer B field | Transform |
|---|---|---|
| `idea_summary` | Vision | Verbatim. User can expand at Step 0.4 edit. |
| `nom` (source) | Project name | Direct; null-class → Step 0.4 prompts user. |
| `nom` (same source, derived) | Project slug | Derive from resolved Project name per existing rule. |
| `type` | Is-a-plugin | Inferred: contains "plugin" (case-insensitive) → `yes`; else `no`. |
| `hints_techniques` | Stack hints | Direct; null-class → `[none]`. |
| `attaches` | Mixed media | Informational; Step 0.3 still scans cwd via `Glob` for canonical list. |
| `pour_qui`, `langue_detectee`, `budget_ou_contrainte`, `prive_ou_public` | (no Layer B field) | Archived in `## Conversational context from drop zone` section of `memory/project/bootstrap_intent.md` at Step 0.5. |
| (absent) | License | Default MIT. |
| (absent) | Plan tier | Step 0.4 prompts user. |
| (absent) | Scope locks | Step 0.4 default `[none]`. |

### Cross-layer pattern

v1.3.2 is the first cross-layer wire in Genesis. The pattern (per master.md cross-skill-pattern #4):

1. Layer A captures user intent in a dedicated file at cwd root with origin-tagged naming.
2. Layer B's corresponding phase detects + parses + maps + archives the Layer A file.
3. Precedence always favours the Layer A file over legacy seeds; never silent merge.
4. Layer A field names in frontmatter are English snake_case; user-facing labels live only in `phase-X-*.md` runtime templates.
5. Layer B card shows origin tags (`from drop zone`, `from config.txt`, `derived`, `default`, `inferred`) to make provenance explicit.

Future Étape 1 → Phase 1, Étape 2 → Phase 2, Étape 3 → Phase 3 wires will follow the same shape.

## Concentrated privilege

v1.4.0 refines cross-skill-pattern #2 from *"at most one concentrated privilege per skill"* to *"at most one concentrated privilege per operation class, per skill"*. `genesis-drop-zone` now declares two orthogonal privilege classes — disk (v1.3.2) and network (v1.4.0) — each with its own consent model and five mitigations.

### Privilege class table

| Version | Disk class | Network class |
|---|---|---|
| v1.3.0 | `none` | `none` |
| v1.3.1 | `none` | `none` |
| v1.3.2 | writes `drop_zone_intent.md` to cwd after consent, halt-on-existing, no `mkdir` | `none` |
| v1.3.3 | unchanged from v1.3.2 (runtime locale dispatch only) | `none` |
| **v1.4.0** | **unchanged from v1.3.2** (additive frontmatter keys only — same write, same halt, same path) | **subprocess → Anthropic Messages API for Citations extraction, pre-flight env check, silent graceful fallback, 1h cache TTL explicit** |

### Disk class mitigations (unchanged since v1.3.2)

v1.3.2 broke the `none` streak with the minimum viable concentrated privilege — one file, one path, one operation. The five mitigations remain canonical:

- **Bilingual consent card** (single gate; absolute path with arrow marker; natural-language response; modifications route back through mirror re-render). **v1.3.3**: consent card renders in the detected `content_locale` instead of always-bilingual.
- **Halt-on-existing** (pre-write check; no overwrite; no timestamp-suffix fallback; no second destructive-consent prompt; matches `session-post-processor` halt-on-leak precedent).
- **Narrow path resolution** — cwd only. No `mkdir`, no subdir, no arbitrary path. Context guard already asserted cwd fresh on entry.
- **Post-write verification** — `test -s` confirms the file exists and has non-zero size before the accept bridge prints.
- **Per-target consent floor match with `pepite-flagging`** — the precedent for Layer A privileges.

### Network class mitigations (new in v1.4.0)

v1.4.0 adds the second class with its own orthogonal consent model and five mitigations:

- **Pre-flight env check at skill entry** — `ANTHROPIC_API_KEY` unset → skill commits to the v1.3.3 in-context path before the welcome box prints. `api_extraction_available = false` for the session. No subprocess launch, no network call, no privilege actually exercised.
- **Subprocess isolation** — the extractor runs as a separate Python process. It cannot mutate the session filesystem beyond its own stdout/stderr streams. The SKILL.md dispatch is the only place where subprocess output is read, validated, and consumed.
- **Explicit 1h cache TTL always** — the extractor hardcodes `cache_control: {type: "ephemeral", ttl: "1h"}` on document blocks per R8 § Stage 2 mandate. The env override `GENESIS_DROP_ZONE_CACHE_TTL` accepts `5m` or `1h`; the SDK default (5-minute) is never reached by omission.
- **Token-budget logging to stderr** — every successful extraction logs `input_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens`, `output_tokens` as a single stderr line (verbose mode via `GENESIS_DROP_ZONE_VERBOSE=1` adds per-phase tracing). Forensic only — invisible to the Victor-facing UX.
- **Silent graceful fallback** — any fallback trigger (env unset, Python unresolvable, subprocess exit ≠ 0, stdout not valid JSON, schema check fails) commits to the v1.3.3 in-context extraction path. The mirror renders v1.3.3-identical output. No user-facing informational note prints. The privilege never escalates on failure — fallback inherits zero new privileges beyond v1.3.3.

### Precedent for future multi-class privileges

A skill can legitimately need operations from different classes. Each class must ship with its own consent model, its own five mitigations, be independently disableable (the user can opt out of one class without losing the other — v1.4.0 users without `ANTHROPIC_API_KEY` still get v1.3.2 disk writes intact), and have its own failure mode that never escalates privilege on the other class.

A skill that accretes a third class should trigger a hard anti-Frankenstein review — at that point the skill probably needs splitting.

## Deferred scope

Ordered by rough priority, non-binding, revisit at each session boundary:

1. **Layer B citation surfacing** — the `_source_citation` entries written to `drop_zone_intent.md` are persisted by Layer A in v1.4.0 but not surfaced in Layer B's Step 0.4 intent card or Step 0.5 `bootstrap_intent.md` template. v1.4.1 candidate if user pain emerges.
2. **Files API (beta) adoption** — v1.4.0 uses inline base64 document blocks. Files API beta (`anthropic-beta: files-api-2025-04-14`) enables dedup across sessions and larger file limits. Ship when a concrete user hits the limit.
3. Programmatic handoff — auto-invoke `genesis-protocol` without the user typing the slash command. Requires harness-level skill-to-skill invocation not 2026-04 ready.
4. `GH_BROWSER` profile routing wire-up.
5. UX toolkit integration — @clack/prompts, Charm Gum, cli-spinners. Surface is complete now (R9 closed in v1.3.3, citations shipped in v1.4.0); polish can land without re-fragmenting it.
6. Completion chime (cross-platform).
7. Error handling refinements — filesystem-side permission-denied / disk-full / symlink edge cases currently let `OSError` bubble up; API-side errors have their own silent fallback per § "Citations API dispatch (v1.4.0) / Fallback triggers". v1.4.1+ adds filesystem halt + remediation if real pain emerges.
8. **Contradictions surfacing** — cross-document conflict detection when multiple documents dropped. v1.5+ if multi-document drops become common.
9. **Chain-of-Verification (CoVe) second pass** — Haiku 4.5 verification of Citations output. R8 recommends skipping unless evals demand.
10. **Bilingual Layer B null-class parsing** — if `drop_zone_intent.md` frontmatter null-class tokens ever carry EN canonical variants alongside FR canonical, Layer B's Step 0.2a parser grows a bilingual branch. v1.5+ target.
11. **Three-locale-or-more expansion** — if Genesis ships beyond FR + EN (e.g. ES, DE), `welcome_locale` and `content_locale` become n-way enums. Deferred until a real non-FR/EN user emerges.
12. **Structured Outputs (Path B) alternative** — v2 architectural pivot question. Would require dropping Citations (API incompatibility). Not considered until Path A evals expose a concrete shortfall.
