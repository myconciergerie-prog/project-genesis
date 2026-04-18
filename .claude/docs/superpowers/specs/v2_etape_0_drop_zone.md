<!-- SPDX-License-Identifier: MIT -->
---
name: v2 Étape 0 — drop zone welcome + mirror + write + Layer B handoff + Citations (genesis-drop-zone skill)
description: Implementation-grade spec for the LAYER A conversational front door of Genesis v2. Living spec across versions. v1.3.0 shipped welcome + token-streamed acknowledgement + bridge; v1.3.1 upgraded the acknowledgement into a 9-field structured mirror screen (in-context extraction, zero disk write, no API call); v1.3.2 added first Layer A write privilege (drop_zone_intent.md to cwd after consent) + Layer B handoff wire into genesis-protocol Phase 0; v1.3.3 wires runtime locale detection (welcome + mirror + consent card + halt + bridges + body echo switch between FR and EN via welcome_locale / content_locale variables); v1.4.0 introduces the second concentrated privilege class for genesis-drop-zone — an Anthropic API extraction call via Python subprocess with Citations enabled, producing per-field source attribution (`[page N]` / `[lines X-Y]`) rendered inline in the mirror and persisted as optional `source_citation` frontmatter entries in drop_zone_intent.md, with graceful fallback to v1.3.3 in-context extraction when ANTHROPIC_API_KEY is absent or the extractor fails. Programmatic handoff, UX toolkit polish, and completion chime deferred to v1.4.1+.
type: spec
target_version: v1.3.0 (welcome vertical slice) + v1.3.1 (extraction mirror) + v1.3.2 (write + Layer B handoff) + v1.3.3 (runtime locale rendering) + v1.4.0 (Citations API extraction with fallback) → v1.4.1+ (programmatic handoff + UX polish + chime)
created_at: 2026-04-17
updated_at: 2026-04-18 (v1.4.0 brainstorming — Citations API + second privilege class + MINOR bump)
originSessionId: project-genesis v1.3.0 brainstorming
status: active
mirrors: skills/genesis-drop-zone/SKILL.md (1:1 section-for-section across versions)
also_touches: skills/genesis-protocol/phase-0-seed-loading.md + skills/genesis-protocol/SKILL.md + skills/genesis-protocol/verification.md (v1.3.2 cross-layer integration)
inherits_from: .claude/docs/superpowers/specs/v2_vision_promptor_fusion.md § "Étape 0 — Le Dépôt"
---

# v2 Étape 0 — Drop zone welcome (implementation spec)

## Position in the v2 architecture

Genesis v2 stratifies into two layered protocols with distinct numbering:

- **LAYER A — the conversation**: Étape 0 (drop zone) → Étape 1 (Étincelle) → Étape 2 (Creation) → Étape 3 (Miroir). What Victor sees.
- **LAYER B — the engine**: Phase -1 (deps) → Phase 0 (seed) → … → Phase 7 (resume/archive). What Genesis does. Implemented today by the `genesis-protocol` skill.

This spec owns LAYER A Étape 0. A new sibling skill `genesis-drop-zone` incarnates it. `genesis-protocol` (LAYER B) stays strictly untouched — the separation mirrors the architectural split the vision doc `v2_vision_promptor_fusion.md` takes care to draw.

## Problem statement

Genesis v1 is an engineer's protocol that speaks to engineers. Bootstrapping requires a written `config.txt`, an understanding of fine-grained PAT scopes, a willingness to paste public SSH keys. The v1.2.0 self-dogfood session catalogued this gap: Victor (77, non-technical, magnificent idea) cannot use Genesis v1. The vision doc names the target — "Dis-moi ton idée. Je m'occupe du reste." — but the surface that would deliver that promise does not exist yet.

The Étape 0 drop zone is the front door that closes this gap. It is the intent-first unified box where prompt + files + URLs land together, matching the 2026 canon established by v0.app / Bolt.new / Lovable / Perplexity / Notion AI [v2_promptor_fusion_landscape_2026-04-17.md § Stage 1]. A user who has never heard of `config.txt`, SSH, or PATs can open Claude Code, type "je veux créer un projet", drop a PDF brief, and be met by a conversational welcome rather than a dev-tooling prompt.

## Scope — v1.3.0 vertical slice

### In scope

1. **Skill package**: new sibling skill `skills/genesis-drop-zone/` with `SKILL.md` + `phase-0-welcome.md`.
2. **Welcome body**: the ASCII box template "Depose ici ton idee. / Un texte, un PDF, une photo, un lien, un audio — / tout est bienvenu. / (Parcourir les fichiers) / Tes fichiers restent avec toi pendant cette session." — authored in FR primary and EN mirror (both coauthored from day 1 per R9, FR printed by default in v1.3.0).
3. **Token-streamed acknowledgement template**: a pattern (not verbatim) that reformulates in progressive bullets what the user has given — text, PDFs, images, URLs. Ends with "✓ J'ai tout lu."
4. **Bridge message (bilingual)**: 2 paired lines closing the interaction honestly — "Extraction et création du projet arrivent bientôt… / Extraction and project creation are coming soon…"
5. **Trigger evaluation gate**: dual invocation (slash `/genesis-drop-zone` + bilingual natural-language triggers in `description:` frontmatter), with a guard that refuses invocation inside an existing project.
6. **Concentrated privilege declaration**: `none` (welcome + acknowledgement only).
7. **1:1 mirror map** with SKILL.md: section-for-section, drift = merge-blocker.

### Out of scope (deferred at v1.3.0 ship — partially closed in v1.3.1; see next section for the updated deferred list)

- Structured extraction of user intent into a target schema (Path A Citations or Path B Structured Outputs per vision doc).
- Writing `bootstrap_intent.md` into any directory.
- Handoff to `genesis-protocol` Phase 0.
- Runtime locale detection (FR vs EN selection).
- `GH_BROWSER` profile routing.
- Any UX toolkit integration (@clack/prompts, Charm Gum, cli-spinners).
- Any R9-related cleanup of `genesis-protocol` or other existing skills.

The slice was intentionally surface-only so the first MINOR bump of the v1.3.x cycle demonstrated the surface without accruing plumbing that would have to be migrated again when extraction lands. v1.3.1 then closes the in-context extraction piece of that deferred list; see § "Scope — v1.3.1 extraction" below.

## Scope — v1.3.1 extraction

### In scope

1. **In-context extraction of user intent** into a 9-field schema (see § "Extraction schema — 9 fields" below). The skill instructs Claude, at acknowledgement time, to extract the schema from the dropped content via its native multimodal understanding — no Anthropic API call, no subagent dispatch, no Python, no external dependency.
2. **Mirror screen** replaces the v1.3.0 `◐ ... ✓` bullet-list acknowledgement. Aligned-column table matching the Étape 2 canon of `v2_vision_promptor_fusion.md`, token-streamed reveal one row at a time. FR rendered by default (v1.3.0 pattern preserved), EN mirror coauthored day 1.
3. **Null-visible convention**: every one of the 9 fields always renders. Missing core fields → `a trouver ensemble` (signals the gap will be closed in Étape 1). Missing bonus fields → `non mentionne` / `non mentionnee` (signals not-blocking).
4. **Bridge update**: v1.3.0's "Extraction et création… arrivent bientôt" becomes false once extraction has run. Bridge is rewritten to reflect that extraction is done and only the write / creation of the actual project remains deferred. See § "Bridge message — bilingual (v1.3.1 update)" below for the exact text.
5. **Failure-mode extensions**: zero-content re-prompt (v1.3.0 branch preserved unchanged); unreadable-attachment fallback as a line inside the `Depose` / `Dropped` field; very-thin-content mirror with mostly null labels (honest disclosure).
6. **Truncation rules**: each row value ≤ 60 chars after the label (80-col terminal). `Depose` caps at 3 items + `+ N autres` beyond. Prose truncation = 57 chars + `...`.
7. **Concentrated privilege declaration**: still `none` (v1.3.0 precedent preserved; in-context extraction writes nothing to disk, spawns no process, makes no network call).
8. **1:1 mirror map** extended to cover the new sections; drift between spec and SKILL.md remains a merge-blocker.

### Out of scope (deferred to v1.3.2+)

- API-powered Path A Citations extraction (audit-trail via `cited_text` + `document_index`). In-context extraction of v1.3.1 is honest prose attribution only ("vu page 1 de ton brief") without API-hard traceability. Upgrade in v1.3.2 or later once the write + handoff is in place.
- Writing `bootstrap_intent.md` into any directory.
- Handoff to `genesis-protocol` Phase 0 (invocation with `bootstrap_intent.md` as the Layer B seed).
- Runtime locale detection (the mirror renders in FR even when `langue_detectee` = EN in v1.3.1; coupled fix v1.3.2).
- `GH_BROWSER` profile routing.
- UX toolkit integration (`@clack/prompts`, Charm Gum, cli-spinners).
- Completion chime.
- Any R9-related cleanup of `genesis-protocol` or other existing skills.

### Rationale for v1.3.1 route

- **Extract in-context, don't call API**: upgrading the existing acknowledgement into real extraction is the smallest meaningful increment. Adding an external API call — even with ANTHROPIC_API_KEY available in user profile — would introduce a first concentrated privilege of Layer A for code that has no downstream consumer yet (no `bootstrap_intent.md` write, no handoff). Anti-Frankenstein gate: declare privileges when the code that carries them ships, not speculatively.
- **Mirror replaces ack, not augments**: a two-screen "I saw items / I understood fields" pattern would feel duplicative to Victor. Single screen with structured fields delivers both "I'm paying attention" and "I understood" in one surface.
- **9 fields, not 5**: user picked extended schema at brainstorming. Additional 4 fields (`langue_detectee`, `budget_ou_contrainte`, `prive_ou_public`, `hints_techniques`) are Victor-legible (not dev dump) and surface naturally from conversation / attached content — no extra cost to extract, non-trivial information for Étape 1 / Étape 2.
- **Single spec, version-scoped sections**: v1.3.0 spec is 1 day old; extending it with a new `## Scope — v1.3.1 extraction` section keeps a single canonical vein of truth for the skill. The 1:1 mirror discipline extends naturally — each version's scope has its own section-for-section pair in SKILL.md.

## Scope — v1.3.2 write + Layer B handoff

### In scope

1. **First Layer A concentrated privilege**: write `drop_zone_intent.md` to the current working directory after the user accepts a bilingual consent card. The privilege is narrow by design — one file, one path (cwd root, no subdirectory, no `mkdir`), one operation (create new file, never overwrite).
2. **Consent card** — minimal bilingual accept/cancel card printed immediately after the `✓ Lu et compris.` line of the v1.3.1 mirror. Shows the absolute target path, one warm prose sentence per language, natural-language response. Modifications ("garde Type en boulangerie", "le nom c'est VelyzyBake") trigger re-extraction + re-render of the mirror + re-print of the consent card.
3. **`drop_zone_intent.md` file format** — YAML frontmatter carrying the 9-field extraction schema (internal snake_case names) + 4 metadata keys (`schema_version`, `created_at`, `skill`, `skill_version`) + Markdown body that echoes the FR mirror Victor saw. UTF-8 without BOM, LF line endings, atomic write via temp + rename.
4. **Halt-on-existing protection** — if `drop_zone_intent.md` already exists in cwd at skill entry (after mirror, before consent card), print a bilingual halt message with the absolute path + remediation ("delete it or open Claude Code in another folder") and exit clean. No overwrite, no timestamp suffix, no second consent prompt. Matches the halt-on-leak gate precedent of `session-post-processor`.
5. **Two bridge variants** — the v1.3.1 bridge message is superseded by two version-scoped messages:
   - **Accept bridge** — printed after a successful write. "Saved — type `/genesis-protocol` when you're ready to create the project (GitHub, files, memory) from this file." / FR mirror.
   - **Decline bridge** — printed after the user refuses the consent card. "OK, nothing written. Your idea stays in our exchange for now. Come back whenever you want to save it to disk." / FR mirror.
6. **Layer B integration** — `genesis-protocol` Phase 0 Seed runbook extended to detect, parse, and consume `drop_zone_intent.md` as an alternative seed (priority over legacy `config.txt`). Step 0.1 detection, new Step 0.2a parsing, Step 0.4 intent card carries origin tags per field + a `Additional context from drop zone` block, Step 0.5 `memory/project/bootstrap_intent.md` template extended with a `## Conversational context from drop zone` section that preserves the 4 Layer-A-specific extras (`pour_qui`, `langue_detectee`, `budget_ou_contrainte`, `prive_ou_public`). `skills/genesis-protocol/SKILL.md` and `skills/genesis-protocol/verification.md` updated accordingly.
7. **master.md privilege map update** — the `genesis-drop-zone` entry of cross-skill-pattern #2 switches from `none` to `writes drop_zone_intent.md to cwd after consent card, halt-on-existing, no mkdir` (first Layer A privilege ship). Cross-skill-pattern #4 (Layer A / Layer B stratification) gains an explicit note that v1.3.2 is the first cross-layer wire live.
8. **1:1 mirror map** extended to cover the new consent card + write flow + halt + bridges + schema sections; drift between spec and SKILL.md remains a merge-blocker.

### Out of scope (deferred to v1.3.3+)

- API-powered Path A Citations extraction (audit-trail via `cited_text` + `document_index`). First "external API call" privilege for `genesis-drop-zone`; can ship v1.3.3 or later now that the write + handoff exists as downstream reader.
- Runtime locale detection. v1.3.2 still hardcodes FR rendering for welcome + mirror + consent card. The `langue_detectee` field is extracted and preserved in `drop_zone_intent.md` + propagated into Layer B's `## Conversational context from drop zone`, but no rendering switches on it yet.
- Programmatic handoff — auto-invoke `genesis-protocol` without the user typing `/genesis-protocol`. v1.3.2 uses human-in-the-loop dispatch via the accept bridge's instruction. A harness-level skill-to-skill invocation mechanism is not 2026-04 ready.
- `GH_BROWSER` profile routing wire-up.
- UX toolkit integration (`@clack/prompts`, Charm Gum, cli-spinners).
- Completion chime (cross-platform).
- Error handling refinements for permission-denied / disk-full / symlink edge cases. v1.3.2 lets `OSError` bubble up naturally; v1.3.3+ adds halt + remediation if a real pain point surfaces.

### Rationale for v1.3.2 route

- **Write + consent + Layer B in one ship** — the write privilege has no downstream reader if Layer B is not updated; shipping Layer A write without Layer B integration would leave `drop_zone_intent.md` floating on disk with nothing that reads it. Anti-Frankenstein says declare privileges for code that ships with its downstream; we honour that by bundling.
- **Narrow privilege discipline** — the first Layer A privilege is the precedent every Étape 1 / Étape 2 / Étape 3 privilege will inherit from. Writing one file to cwd (no `mkdir`, no path resolution, no overwrite) is the minimum viable concentrated privilege. Later versions can widen if a real pain point emerges — the precedent should start tight.
- **Rename to avoid collision** — `genesis-protocol` already owns `memory/project/bootstrap_intent.md` as its Phase 0 write target. Layer A using the same filename at cwd root would be a faux ami: same name, different schema, different path, different audience. Renaming Layer A's file to `drop_zone_intent.md` is origin-tagged, collision-free with Victor-written files, and makes the Phase 0 detection logic unambiguous.
- **Human-in-the-loop handoff** — forcing Victor to type `/genesis-protocol` after the accept bridge costs one extra keystroke but preserves his control (pause, inspect the file, come back later) and sidesteps the absence of a programmatic skill-invocation API. The accept bridge is explicit about what to do next; the decline bridge is warm and non-pressurizing.
- **Halt-on-existing, never overwrite** — the context guard precondition ("fresh cwd") means an existing `drop_zone_intent.md` is a genuine anomaly, not a normal case. Halt + remediation is the right signal: let the user reconcile manually. Overwriting (C variant) or timestamping (B variant) would mask the anomaly and create ambiguity downstream.
- **Preserve the 4 Layer-A-specific extras at Layer B** — `pour_qui`, `langue_detectee`, `budget_ou_contrainte`, `prive_ou_public` are extracted at the cost of Victor's conversation turn. Dropping them at Layer B would be silent information loss. Archiving them in a `## Conversational context from drop zone` section of `memory/project/bootstrap_intent.md` keeps the end-to-end Layer A → Layer B flow informationally complete for Phases 1-7 that may want to consume them (e.g. Phase 1 R9 locale, Phase 4 memory scaffolding, Phase 5.5 auth scope).
- **Single spec, version-scoped sections** — extending the living spec with a `## Scope — v1.3.2 write + Layer B handoff` section (and the per-surface sections below) keeps one canonical vein of truth. The 1:1 mirror discipline extends naturally into `genesis-drop-zone/SKILL.md`. The Layer B changes are bundled in the same ship and documented in the same spec since the cross-layer wire is one coherent unit.

## Scope — v1.3.3 runtime locale rendering

### In scope

1. **Runtime locale detection + dispatch** across the Layer A user-facing surfaces. Two locale variables with distinct lifecycles:
   - `welcome_locale` — resolved at skill invocation. From the trigger phrase language on intent-match (`je veux créer un projet` → `FR`; `I want to create a project` → `EN`); defaults to `FR` on slash invocation `/genesis-drop-zone` (no language signal).
   - `content_locale` — resolved from the extracted `langue_detectee` field after the first user turn with content. Mapping: `FR` → FR variant; `EN` → EN variant; `mixte` → FR (tiebreaker = primary project language).
2. **Locale-switched rendering** on the following surfaces (previously hardcoded FR + bilingual-always mixtures):
   - Welcome box — uses `welcome_locale` (FR or EN variant printed, not both).
   - Zero-content re-prompt — uses `welcome_locale`. Newly-authored EN mirror `I'm listening — drop or write whatever you want to share.` pairs the v1.3.0 FR re-prompt `Je t'écoute — dépose ou écris ce que tu veux me partager.`.
   - Mirror template + 9-field labels — uses `content_locale`.
   - Consent card (v1.3.2) — uses `content_locale` (FR or EN variant printed, not both — v1.3.2 shipped as always-bilingual).
   - Halt message (v1.3.2) — uses `content_locale`.
   - Accept + decline bridges (v1.3.2) — uses `content_locale`.
   - `drop_zone_intent.md` body prose intro + mirror echo — uses `content_locale`.
3. **Frontmatter data contract preserved** — `drop_zone_intent.md` frontmatter null-class tokens stay FR canonical (`"a trouver ensemble"`, `"non mentionne"`, `"non mentionnee"`, `"a affiner — ..."`) regardless of `content_locale`. Layer B Step 0.2a parser reads FR canonical — unchanged. Intentional Layer A / Layer B asymmetry: **body = locale-detected human echo; frontmatter = FR canonical data contract.** Bilingual Layer B null-class parsing deferred to v1.4+ if a real pain point emerges.
4. **No new runtime string content beyond one pair** — v1.3.3 ships **one new bilingual pair** (the EN zero-content re-prompt). All other EN variants already exist: EN welcome (v1.3.0), EN mirror + 9-field labels (v1.3.1), EN consent card + EN halt + EN accept bridge + EN decline bridge (v1.3.2). v1.3.3 wires the dispatch variable; it does not author templates from scratch.
5. **Concentrated privilege map unchanged** — v1.3.3 introduces no new privilege class. `genesis-drop-zone` declaration stays at "writes `drop_zone_intent.md` to cwd after consent card, halt-on-existing, no `mkdir`, no path resolution beyond cwd". The privilege map entry in `memory/master.md` gains only a v1.3.3 qualifier noting that rendering is now locale-detected; mitigations list unchanged.
6. **Single new fixture** — `tests/fixtures/drop_zone_intent_fixture_v1_3_3_en.md` is the EN-content counterpart to v1.3.2's fixture. Frontmatter `langue_detectee: EN`, body echoes the EN mirror. Used at artefact-level for body-rendering inspection and as a Layer B regression probe (parser unchanged — the same FR canonical null tokens appear regardless of body locale).

### Out of scope (deferred to v1.3.4+)

- API-powered Path A Citations extraction (audit-trail via `cited_text` + `document_index`). First "external API call" privilege; downstream reader already in place as of v1.3.2.
- Programmatic handoff — auto-invoke `genesis-protocol` without the user typing the slash command.
- `GH_BROWSER` profile routing wire-up.
- UX toolkit integration (`@clack/prompts`, Charm Gum, cli-spinners).
- Completion chime (cross-platform).
- Error handling refinements for permission-denied / disk-full / symlink edge cases.
- **Bilingual Layer B null-class parsing** — if `drop_zone_intent.md` frontmatter null-class tokens ever carry EN canonical variants (`"to be found together"`, `"not mentioned"`), Layer B's Step 0.2a parser grows a bilingual branch. v1.4+ target, not v1.3.x.
- **Three-locale-or-more expansion** — if Genesis ships beyond FR + EN (e.g. ES, DE), `welcome_locale` and `content_locale` become enums. Minor, deferred until a real non-FR/EN user emerges.

### Rationale for v1.3.3 route

- **R9 tier-3 closure end-to-end** — v1.3.0 authored both FR and EN welcome. v1.3.1 authored both FR and EN mirror + 9-field labels. v1.3.2 authored both FR and EN consent card + halt + bridges. Every runtime string was bilingual-from-day-1 per R9 tier 3 — but rendering hardcoded FR across welcome and always-bilingual across v1.3.2 surfaces. v1.3.3 closes the loop with a single dispatch variable per stage. No template retrofit: all EN variants exist; the ship wires the variable.
- **Two variables, not one** — `welcome_locale` and `content_locale` are distinct signals with non-overlapping lifecycles. Welcome precedes any content; content-driven extraction cannot inform the welcome render. Using one variable forces either (a) always-FR welcome (wastes the easy signal of an EN trigger phrase) or (b) blocking the welcome behind content (bad UX, loses the "welcome box IS the invitation" principle of v1.3.0). Two variables with clear lifecycles is the minimum viable wiring.
- **Frontmatter FR canonical preserved** — Layer B's Step 0.2a parser detects null classes by exact string match on `"a trouver ensemble"` / `"non mentionne"` / `"non mentionnee"` / `"a affiner — ..."`. Changing the canonical ripples into a Layer B parser branch. v1.3.3 is a pure Layer-A-rendering-layer change; Layer B contract untouched. The asymmetry (body = locale-detected human echo; frontmatter = FR canonical data contract) is intentional and spec-documented. Bilingual Layer B parser is a v1.4+ target if real pain emerges — v1.3.3 does not speculate.
- **`mixte` → FR tiebreaker** — `langue_detectee` admits three values: `FR`, `EN`, `mixte`. Display needs a tiebreaker. FR is the primary project language (French-speaking machine, Layer 0 user profile, trigger lists start with FR phrases). Picking FR keeps the default stable and readable. Picking "always bilingual for mixte" would re-fragment the surface — the whole point of v1.3.3 is to stop printing both variants. Victor can re-state the idea more clearly to shift `langue_detectee`; no hidden UI.
- **Slash command → FR default** — `/genesis-drop-zone` carries no language signal. Two options: (a) FR default (primary project language), (b) read terminal locale via `$LANG` / `$LC_ALL`. Option (b) is heavier and error-prone (terminal locale can be `C`, unset, or misconfigured on Windows). Option (a) is deterministic and aligns with the intent-trigger list's FR-first ordering. An EN-locale user who types `/genesis-drop-zone` sees FR welcome, drops EN content, `langue_detectee = EN`, mirror-onwards switches to EN — graceful degradation at the cost of one FR welcome box. The intent-phrase path is the locale-native path; slash is the engineer path where FR is a defensible default.
- **No Layer B ripple** — confirms narrow-scope discipline. v1.3.3 touches zero Layer B files. The only spec-level acknowledgement of Layer B lives in § "R9 language policy applied" (the `drop_zone_intent.md` body-rendering row changes from "FR hardcoded v1.3.2" to "locale-detected v1.3.3"; the frontmatter row stays "FR canonical, Layer B contract").
- **Living spec, version-scoped sections (third application)** — extending `v2_etape_0_drop_zone.md` with a `## Scope — v1.3.3 runtime locale rendering` section preserves the canonical vein-of-truth pattern established at v1.3.1 and reinforced at v1.3.2. Readers walk the version-scoped sections top-to-bottom to see what each ship layered on.

## Scope — v1.4.0 Citations API extraction

### In scope

1. **Second concentrated privilege class** — external Anthropic API network call. `genesis-drop-zone` previously held one privilege class (disk write, introduced v1.3.2). v1.4.0 adds **network** as an orthogonal class, declared separately in the master.md privilege map. Cross-skill-pattern #2's "at most one concentrated privilege per skill" evolves into "at most one privilege per operation class" — the skill now lists two classes with independent mitigations.
2. **Python subprocess extractor** — new file `skills/genesis-drop-zone/scripts/extract_with_citations.py`. Invoked via `Bash` from the SKILL.md dispatch using the Python portability pattern established by `session-post-processor` (`command -v python || command -v python3 || command -v py`). The script reads drop-zone inputs (cwd + attached file paths + dropped text) on stdin / argv, calls the Anthropic Messages API with `citations: {enabled: true}` and `cache_control: {type: "ephemeral", ttl: "1h"}`, and emits the 9-field extraction schema plus per-field `source_citation` on stdout as a single JSON object.
3. **Model selection** — default `claude-opus-4-7` per R8 `v2_promptor_fusion_landscape_2026-04-17.md § Stage 2` (Opus for extraction, Sonnet 4.6 as cost fallback). User override via environment variable `GENESIS_DROP_ZONE_MODEL=claude-sonnet-4-6` (documented in `## Citations API — signal + dispatch (v1.4.0) § Environment variables` below). No hardcoded secondary model in v1.4.0 — a single active model per invocation.
4. **Explicit 1h cache TTL** — extractor always passes `cache_control: {type: "ephemeral", ttl: "1h"}` on the document block. Mandated by R8 § Stage 2 ("Explicit `ttl: 1h` is now mandatory — don't rely on defaults"). Never relies on the 5-minute default.
5. **Mirror enhancement — per-field citation annotations** — when a citation is available (i.e. the source was plain text or PDF), the mirror row suffixes the value with `[page N]` (PDF) or `[lines X-Y]` (plain-text doc) in parentheses-free form. When no citation is available (image-only drop, inline-typed text with no attachment, or fallback path fired), the row renders without annotation — v1.3.3 parity. Annotation is ASCII-safe: brackets `[` `]`, digits, dash, space only.
6. **Frontmatter schema extension** — `drop_zone_intent.md` frontmatter gains an **optional** nested key per semantic field: `<field>_source_citation` (e.g. `idea_summary_source_citation`). Structure: YAML mapping with `type` (one of `pdf_page_range`, `text_char_range`, `none`), `document_index` (integer), `start` (integer), `end` (integer), `cited_text_preview` (string ≤ 80 chars, truncated with `...`). When no citation applies, the key is **omitted** (not `null`) to keep files written by content-less / fallback paths byte-identical to v1.3.3. `schema_version` stays at `1` — the addition is purely additive and backward-compatible with Layer B's Step 0.2a parser (dict-based YAML parsers ignore unknown keys naturally).
7. **Graceful fallback** — four conditions trigger fallback to v1.3.3 in-context extraction: (a) `ANTHROPIC_API_KEY` unset at skill dispatch; (b) extractor exit code non-zero (SDK import failure, API error, rate limit, bad input); (c) extractor exit code zero but JSON parse fails or schema validation fails; (d) extractor stderr signals a specific retry-exhausted state. On fallback, the skill runs the v1.3.3 in-context extraction path exactly as-is and renders the mirror without citation annotations. **No user-facing informational note prints** — fallback is silent. Forensic state goes to stderr via the subprocess stderr stream (harness-visible in verbose sessions, invisible in the default Victor-facing UX).
8. **Five mitigations for the new privilege class** — bilingual pre-flight (env check at dispatch), subprocess isolation (extractor cannot mutate filesystem beyond its own stdout/stderr), explicit TTL (1h cache, never 5-min default), token-budget logging to stderr (forensic only), silent graceful fallback (no privilege escalation on failure — fallback path has zero new privileges beyond v1.3.3).
9. **Three new fixtures** — `tests/fixtures/drop_zone_intent_fixture_v1_4_0_fr_with_citations.md` (FR body + 9 FR canonical null tokens in frontmatter + 4 `_source_citation` entries for filled fields) and `tests/fixtures/drop_zone_intent_fixture_v1_4_0_en_with_citations.md` (EN body + 9 FR canonical null tokens in frontmatter + 4 `_source_citation` entries). Both fixtures cover the schema extension for Layer B parser regression. A third fixture `tests/fixtures/drop_zone_intent_fixture_v1_4_0_fallback.md` is byte-identical to `drop_zone_intent_fixture_v1_3_3_en.md` **modulo the `skill_version` metadata value** (`"1.4.0"` vs `"1.3.3"`) — proves the fallback path writes a file whose only v1.4.0-labelled delta is the skill_version stamp itself. This is the single canonical regression target for the fallback-path byte-identity claim.
10. **MINOR semver bump** — v1.3.3 → v1.4.0. Second privilege class (network) is qualitatively different from v1.3.2 disk; first external dependency (`ANTHROPIC_API_KEY`, Anthropic Python SDK); new subprocess surface area (Python extractor). The bump honours the structural weight of the change. Precedent for PATCH (v1.3.2 shipped the *first* privilege at PATCH) does not apply — v1.3.2 was a surface addition within an established tier-3 line; v1.4.0 crosses a tier boundary.

### Out of scope (deferred to v1.4.1+)

- **Layer B citation surfacing** — the `_source_citation` entries written to `drop_zone_intent.md` are persisted by Layer A in v1.4.0 but **not surfaced in Layer B's Step 0.4 intent card or Step 0.5 `bootstrap_intent.md` template**. Layer B Step 0.2a parser ignores unknown keys naturally (zero parser code change). If user pain emerges around wanting to see "Vision came from page 3 of the brief" on the Phase 0 card, v1.4.1 adds the card / bootstrap_intent.md extension additively. Zero Layer B code change in v1.4.0 preserves the v1.3.3 zero-Layer-B-ripple discipline.
- **Files API (beta) for large PDF uploads** — v1.4.0 uses **inline base64 document blocks** within the Messages API request. The Anthropic Files API beta (header `anthropic-beta: files-api-2025-04-14`) is deferred to v1.4.1 or later. Rationale: inline base64 covers the 32 MB × 600-page PDF limit (the common Victor case); Files API pays off on repeated uploads or cross-session dedup, neither of which v1.4.0 exercises. Deferring keeps the v1.4.0 surface narrow.
- **Image source citations** — Citations API does not produce `cited_text` for image sources (only plain text and PDF). For image-only drops, per-field `_source_citation` is omitted. No "seen in attachment name" pseudo-citation is synthesized — honest null-visible discipline applied at the citation layer (the field's value still renders, the citation is just absent).
- **Structured Outputs (Path B)** — the v2 Promptor research documented that Structured Outputs and Citations are mutually exclusive on the same API call (400 if both set). v1.4.0 commits to **Path A (audit-first)** as recommended by R8 § Stage 2. Path B is a v2.x architectural pivot question, not a v1.4.x option.
- **Contradictions array** — the R8 note on cross-reference prompt pattern (`"For each field, prefer transcript > brief > sketch. Flag conflicts in contradictions[]."`) is not implemented in v1.4.0. Drops are currently one-document-dominant; multi-document conflict surfacing is a v1.5+ consideration.
- **Chain-of-Verification (CoVe) second pass** — R8 ranks Citations above CoVe as the preferred verification layer. v1.4.0 uses Citations only. CoVe is Haiku-4.5-driven, optional, and R8 recommends skipping unless evals show a specific failure class. Skip by default.
- Programmatic handoff — auto-invoke `genesis-protocol` without the user typing the slash command. Human-in-the-loop via the accept bridge is the v1.3.2+ pattern.
- `GH_BROWSER` profile routing wire-up.
- UX toolkit integration (`@clack/prompts`, Charm Gum, cli-spinners).
- Completion chime (cross-platform).
- Error handling refinements for filesystem edge cases (permission-denied / disk-full / symlink on write) — v1.4.0 inherits the v1.3.2 floor ("write succeeds or the harness shows the stack"). API-side errors have their own fallback path per § In scope item 7; filesystem-side errors still bubble.
- **Bilingual Layer B null-class parsing** — remains a v1.5+ target if real pain emerges.
- **Three-locale-or-more expansion** — unchanged deferral; `welcome_locale` / `content_locale` stay FR/EN binary until a real non-FR/EN user emerges.

### Rationale for v1.4.0 route

- **MINOR semver is the honest tranche** — v1.3.2 shipped the first concentrated privilege (disk write) at PATCH within a surface-addition cycle. v1.4.0 crosses a qualitatively different threshold: *second* privilege class (network), first external dependency (`ANTHROPIC_API_KEY`, Anthropic Python SDK), first subprocess surface (Python extractor). Forcing PATCH masks architectural weight; MINOR is the clean signal. Running average 8.87 has 0.37 tampon above 8.5 floor — MINOR bump tolerates a slightly narrower pain-driven axis without breaching the streak.
- **Option 2 (Python subprocess via SDK) vs option 1 (curl) vs option 3 (sub-agent)** — three archi options evaluated at session open:
  - **curl via Bash**: rejected. Base64-encoded PDFs blow up the Windows / bash command-line length budget (typical 32 MB PDF → ~45 MB base64 → exceeds `MAX_PATH`-derived limits on Windows); shell quoting differs between bash / PowerShell / cmd (cross-OS test matrix too wide); streaming `citations_delta` parsing from curl stderr is non-trivial; secret management via env vars works but forensic logs leak risk is higher in shell than in SDK.
  - **Python subprocess with anthropic SDK**: selected. SDK handles streaming, retries, base64 encoding, cache_control serialization, and error formatting. Precedent exists — `session-post-processor` ships `run.py` since v0.6.0 with the Python portability pattern (`command -v python || command -v python3 || command -v py`). Introduces one new dependency (`anthropic` Python package) but isolated to the drop-zone extractor script; no impact on other Genesis skills.
  - **Sub-agent (Agent tool dispatch)**: rejected. The Citations API response-level artefact (`citations[]` with `cited_text` + `document_index` + location) is not exposed to parent context by Claude Code's Agent tool interface; sub-agents emit text, not API response metadata. Would degenerate into prompt-based CoVe (soft citations) rather than API-hard audit-trail. Does not deliver "Path A" as specified by R8.
- **Second privilege class, not overload of the first** — master.md cross-skill-pattern #2 originally read "at most one concentrated privilege per skill". v1.4.0 refines this to "at most one per operation class". Rationale: disk write and network call are orthogonal operations with orthogonal mitigations (consent card gates disk; pre-flight env check + silent fallback gates network). Overloading one declaration with both would lose the mitigation-one-for-one discipline. The two-class declaration is the reference pattern for any future skill that needs both a disk privilege and a network privilege.
- **Graceful fallback is silent by design** — the first UX draft considered a bilingual informational note printed before the mirror ("Source attribution unavailable — extracted in-context"). Rejected: introduces R9 noise, distracts Victor from his own content, leaks implementation detail. Citations are additive value; their absence should be invisible at the surface layer. Forensic information stays in stderr where developers can see it during integration testing.
- **Frontmatter extension is optional-additive, not schema-version-bumping** — `drop_zone_intent.md` schema_version stays at `1`. Layer B's Step 0.2a parser is dict-based YAML parsing — unknown keys are ignored naturally. Bumping schema_version to 2 would force Layer B into a version-branching parser and introduce a real Layer B code change for no semantic value. The "additive and silent" discipline preserves v1.3.3's zero-Layer-B-ripple pattern one version further.
- **Key omission beats explicit null** — for fields without a citation, the `_source_citation` key is **omitted** from the frontmatter, not written as `null`. Rationale: fallback-path files (no API extraction ran) and API-path files with image-only drops become byte-identical to v1.3.3 files in the null case. Diff noise is minimized; regression on v1.3.3 fixtures by v1.4.0 extractor in fallback mode is literally zero bytes changed. Layer B never sees "citation layer opted in but empty" — the key's presence *is* the signal.
- **`tests/fixtures/` gains three files, not two** — the extra `_fallback.md` fixture is the explicit regression probe for the fallback-path byte-identity claim above. Without the fallback fixture, a reader has to infer the zero-diff invariant; with it, the property is assertible via `diff`.
- **Living spec, version-scoped sections (fourth application)** — extending `v2_etape_0_drop_zone.md` with a `## Scope — v1.4.0 Citations API extraction` section preserves the canonical vein-of-truth pattern established at v1.3.1 and reinforced at v1.3.2 / v1.3.3. The version history walks top-to-bottom; readers see what each ship layered on without scavenging commit history.

## Scope — v1.4.1 Layer B citation surfacing

### In scope

1. **End-to-end audit-trail visibility** — v1.4.0 persists `<field>_source_citation` nested keys in `drop_zone_intent.md` frontmatter; v1.4.1 makes them visible in `genesis-protocol`'s Phase 0 Step 0.4 intent card and Step 0.5 `bootstrap_intent.md` template. The extraction value loop opened by v1.4.0 closes inside Layer B rather than terminating at Layer A's mirror.
2. **Step 0.2a extension — citation preservation** — the dict-based YAML parse already reads the full frontmatter; v1.4.1 retains the `<field>_source_citation` nested dicts for the 9 semantic source fields alongside the existing 9+4 key preservation. No mapping change, no new mandatory field. Each preserved citation is a dict with five keys (`type`, `document_index`, `start`, `end`, `cited_text_preview`) per v1.4.0 § "Citations API — signal + dispatch (v1.4.0) / Citation object shape".
3. **Step 0.4 card — inline citation suffix on mapped fields** — five card rows gain an inline citation suffix when the corresponding `<source>_source_citation` key is present:
   - `Project name` ← `nom_source_citation`
   - `Project slug` ← `nom_source_citation` (propagated — slug is derived from `nom`)
   - `Vision` ← `idea_summary_source_citation`
   - `Stack hints` ← `hints_techniques_source_citation`
   - `Is-a-plugin` ← `type_source_citation` (propagated — inferred from `type`)
   Two of the five rows (Project slug, Is-a-plugin) propagate their citation from an upstream source field rather than sourcing directly, because the rendered value is a deterministic function of the cited source. When a citation key is absent (legacy config.txt seed, fallback-path write, image-only drop, or field without citation), the row renders exactly as v1.3.2/v1.3.3 — no placeholder, no `[unknown]`, no empty brackets.
4. **Step 0.4 card — inline citation suffix on `Additional context from drop zone` rows** — the four extras rows gain the same treatment:
   - `Target audience` ← `pour_qui_source_citation`
   - `Language detected` ← `langue_detectee_source_citation`
   - `Budget / constraint` ← `budget_ou_contrainte_source_citation`
   - `Visibility` ← `prive_ou_public_source_citation`
5. **Step 0.5 template — citation suffix inside Value columns** — the existing `## Fields` and `## Conversational context from drop zone` tables gain the same inline suffix format inside the `Value` column. No new section added, no new column added, no schema version bump. Parsers that consume `bootstrap_intent.md` (none in Genesis v1 — the file is human/Claude readable) see the suffix as part of the value string; the format is stable and deterministic.
6. **Annotation format — reuse of Layer A discipline verbatim** — the citation suffix format reuses `skills/genesis-drop-zone/phase-0-welcome.md § "Citation annotation format (v1.4.0)"` without redefinition. A single source of truth for the annotation format across both layers:
   - `pdf_page_range` with `start == end` → ` [page N]`
   - `pdf_page_range` with `start != end` → ` [pages N-M]`
   - `text_char_range` → ` [lines X-Y]`
   All ASCII, language-neutral, locale-dispatch-free. Rendering is identical under FR / EN / any future locale.
7. **Mixed media row deliberately unchanged** — the `Mixed media` card row sources its value from Step 0.3 disk `Glob` (not from `attaches`). `attaches_source_citation` (if present) is preserved by Step 0.2a but **not rendered** on the Mixed media row — the row's value is not sourced from `attaches`. Honest provenance alignment: Layer B shows citations for values it actually read from Layer A, nothing else.
8. **Patch semver bump — v1.4.0 → v1.4.1** — read-only rendering of existing data. No new privilege (`genesis-drop-zone` privilege map unchanged; `genesis-protocol` gains no new class). No new frontmatter keys. No schema version bump. No new dependency. No subprocess. No network call. Zero Layer A ripple. PATCH is the honest tranche.
9. **No new fixtures required** — the existing `tests/fixtures/drop_zone_intent_fixture_v1_4_0_fr_with_citations.md` and `_en_with_citations.md` fixtures exercise the v1.4.1 Layer B render path without modification. The fallback fixture continues to exercise the absence-of-citation render path. Zero fixture churn.

### Out of scope (deferred to v1.4.2+)

- **`cited_text_preview` surfacing** — the frontmatter citation dict carries up to 80 chars of source text. v1.4.1 does not render this preview — only the position annotation (`[page N]` etc.). Surfacing the preview on hover / expand is a v1.4.2+ UX option if users want to see the quoted text inline. Rationale: keeping the Step 0.4 card terse prevents clutter; the preview is already archived in `drop_zone_intent.md` for any reader who wants the full quote.
- **Hyperlinks into source files** — e.g. `[page 3](./cahier_des_charges.pdf#page=3)` on the card. Deferred: the Phase 0 card is rendered in Claude's terminal surface; hyperlinks require harness-level support that varies across IDE / terminal / web. The ASCII annotation works everywhere.
- **Citations on `License` / `Plan tier` / `Scope locks` rows** — these fields are not sourced from Layer A. License defaults to MIT; Plan tier is prompted at Step 0.4; Scope locks default `[none]`. No `_source_citation` key exists for them at Layer A, so no rendering possible. Deferring reflects the data contract, not a UX choice.
- **Files API (beta) adoption** — stays deferred (v1.4.0 deferred list item 2). Not blocked by v1.4.1.
- **Programmatic handoff / `GH_BROWSER` / UX toolkit / chime / error handling / contradictions / CoVe / bilingual Layer B null-class parsing / three-locale expansion / Structured Outputs** — all unchanged from v1.4.0 deferred list.

### Rationale for v1.4.1 route

- **PATCH is the honest tranche** — v1.4.1 adds no new privilege, no new dependency, no new subprocess, no new network call, no new schema keys. It reads existing frontmatter data (written by v1.4.0) and renders it on two existing surfaces. Every argument for a MINOR bump (structural weight, cross-version surface growth, external dependency) is absent. Running average ≈ 8.88 has 0.38 tampon above 8.5 — PATCH ship with ≥ 9.0 self-rating fits cleanly inside the streak envelope.
- **Closing the audit-trail loop where it terminates** — v1.4.0 positioned citations as end-to-end audit trail but rendered them only in Layer A's mirror. Victor who reaches Layer B's Phase 0 card (`detailed` / `semi-auto` mode) sees parsed fields without provenance — a gap between the Layer A surface ("Vision: ... [page 3]") and the Layer B surface ("Vision: ..."). Closing this gap is v1.4.1's sole purpose. The feature exists because v1.4.0 created an asymmetry, not because new research surfaced.
- **Cross-skill-pattern #4 discipline upgrade, not break** — v1.3.3 established *"body = locale-detected human echo; frontmatter = FR canonical data contract"*; v1.4.0 extended with *"additive frontmatter keys preserve zero-Layer-B-ripple at parser level"*. v1.4.1 refines one step further: *"Layer B may opt-in to render additive keys read-only. Parser mechanics remain unchanged; rendering logic gains conditional branches on key presence. No schema version bump required."* This is a fourth discipline data-point layering on the same principle — forward-compat with old writers is preserved (old Layer A writers + new Layer B reader = zero citations rendered since no keys exist); zero-ripple at parser level is intact (Step 0.2a still dict-based YAML, unknown keys still ignored naturally in the broader parse); the additive renders at *surface* level, not *contract* level.
- **Inline suffix, not dedicated column or section** — an earlier draft considered a dedicated `## Source attribution from drop zone` section under Step 0.5 with a mapping table (field → citation). Rejected: introduces a second section the reader must reconcile with the `## Fields` table; keeping attribution next to the value is more legible and closer to the Layer A mirror convention. An alternative with a third column `Attribution` in the `## Fields` table was also rejected: changes the table's structural shape (three columns → four) and breaks legacy config.txt sessions' table layout. Inline suffix inside the `Value` column is the minimum-surface option: one string concatenation, no layout change.
- **Mixed media row stays unadorned** — the `Mixed media` value on the Step 0.4 card is sourced from Step 0.3 disk `Glob`, not from Layer A's `attaches`. Surfacing `attaches_source_citation` on this row would create a provenance lie: "this row cites what Victor typed in the drop zone, not what Step 0.3 actually found on disk". The two sources can legitimately diverge (Victor drops "logo.png" but the file is actually `brand_logo.png`). Honest provenance alignment — cite what was actually read.
- **No new verification fixtures** — the v1.4.0 `_fr_with_citations` and `_en_with_citations` fixtures already contain the full citation frontmatter shape. v1.4.1 exercises them against the extended Step 0.4 / Step 0.5 render logic. Zero fixture churn preserves the "three fixtures" discipline established at v1.4.0 and keeps the regression surface flat.
- **Living spec, version-scoped sections (fifth application)** — extending `v2_etape_0_drop_zone.md` with a `## Scope — v1.4.1 Layer B citation surfacing` section continues the vein-of-truth pattern. Five consecutive version-scoped scope sections (v1.3.0, v1.3.1, v1.3.2, v1.3.3, v1.4.0) gave the pattern load-bearing status; v1.4.1 is the sixth instantiation across the PATCH/MINOR boundary.
- **Pain-driven axis honestly narrower than v1.3.x / v1.4.0** — no concrete user pain triggered this ship. The feature is loop-closing, not pain-responsive. Self-rating at v1.4.1 will reflect this honestly on the Pain-driven axis (projected 8.5–8.7) and compensate via Prose cleanliness, Best-at-date (same R8 source, fresh until 2026-04-24), Self-contained (single-skill touch, genesis-drop-zone unchanged), Anti-Frankenstein (narrow-scope additive rendering, no decoration). Target floor ≥ 9.0 remains plausible on 3/5 axes.

## Trigger evaluation gate

The skill is invoked in two ways:

**Path 1 — slash**: `/genesis-drop-zone`. Deterministic, scriptable, testable. Engineers and Genesis-dev sessions use this path.

**Path 2 — natural-language intent match** (Victor path): Claude auto-invokes the skill when the user's message matches one of the triggers declared in `description:` frontmatter of `SKILL.md`:

| Language | Trigger phrases |
|---|---|
| FR | `"je veux créer un projet"`, `"nouveau projet"`, `"démarre un projet"`, `"dis-moi comment commencer"` |
| EN | `"I want to create a project"`, `"start a new project"`, `"new project"` |

**Context guard (mitigates false positives)**: before the welcome box prints, the skill evaluates `is_fresh_context`, which is true if ALL of the following hold:

- cwd has no `CLAUDE.md` at its root, AND
- cwd has no populated `memory/` directory (directory absent, or present but with fewer than 2 non-template files), AND
- either cwd is not a git repository, or `git rev-list --count HEAD` returns fewer than 3.

All three are `AND`-conjoined — a single `false` disables the welcome. No disjunction, no precedence to parse.

If `is_fresh_context` is false, the skill does not print the welcome box. Instead it prints:

```
Tu es déjà dans un projet — la drop zone est réservée aux nouveaux projets.
Si tu veux en démarrer un autre, ouvre Claude Code dans un dossier vide.

You're already in a project — the drop zone is reserved for new projects.
To start another one, open Claude Code in an empty folder.
```

No halt / no error — just a graceful, bilingual redirect. The redirect itself stays always-bilingual by design: it fires before any trigger-phrase evaluation has had a chance to set `welcome_locale` reliably (the context guard fires even on ambiguous in-repo invocations), so printing both languages covers any user who reaches it.

## Runtime locale — signal + dispatch (v1.3.3)

Two locale variables govern the Layer A rendering surfaces. Each has a distinct lifecycle, a distinct signal source, and a distinct set of dependent render targets.

### `welcome_locale` — resolved at skill invocation

**Signal sources** (evaluated in order, first match wins):

1. **Intent-match trigger phrase**: if the skill was auto-invoked by a natural-language intent phrase, the phrase's language sets `welcome_locale`. The trigger list in `SKILL.md` frontmatter is partitioned by language — `je veux créer un projet`, `nouveau projet`, `démarre un projet`, `dis-moi comment commencer` → `FR`; `I want to create a project`, `start a new project`, `new project` → `EN`.
2. **Slash command**: if the skill was invoked by `/genesis-drop-zone`, no language signal is available at invocation time. `welcome_locale` defaults to `FR` (primary project language, matches trigger-list ordering).

**Render targets**:

- Welcome ASCII box (FR variant from `phase-0-welcome.md § "FR welcome box"` or EN variant from `phase-0-welcome.md § "EN welcome box"`).
- Zero-content re-prompt (`Je t'écoute...` or `I'm listening...`).

Welcome and zero-content re-prompt are the only pre-content rendering surfaces; everything downstream uses `content_locale`.

### `content_locale` — resolved after first content turn

**Signal source**: the `langue_detectee` field extracted from the user's first content turn, via the existing v1.3.1 9-field extraction mechanism. Three-value mapping:

| `langue_detectee` | `content_locale` |
|---|---|
| `FR` | `FR` |
| `EN` | `EN` |
| `mixte` | `FR` (tiebreaker) |

**Render targets**:

- Mirror template + 9-field labels (`phase-0-welcome.md § "Mirror template — FR"` or `§ "Mirror template — EN"`).
- Consent card (v1.3.2) — either FR or EN variant, not both.
- Halt message (v1.3.2) — either FR or EN variant, not both.
- Accept bridge (v1.3.2).
- Decline bridge (v1.3.2).
- `drop_zone_intent.md` body — prose intro + mirror echo.

### Divergence between `welcome_locale` and `content_locale`

The two variables are deliberately independent. A user who auto-triggers with `je veux créer un projet` (FR welcome) and then drops an EN brief (`langue_detectee = EN`, `content_locale = EN`) sees an FR welcome, then mirror-onwards in EN. The inverse is equally possible: EN-triggered welcome followed by FR content. No forced consistency — each surface honours the best signal available when it renders.

### Frontmatter data contract unchanged

`drop_zone_intent.md` frontmatter null-class tokens stay **FR canonical** regardless of `content_locale`:

- `"a trouver ensemble"` (core missing)
- `"non mentionne"` (bonus missing, masculine)
- `"non mentionnee"` (bonus missing, feminine)
- `"a affiner — X ou Y"` (ambiguity)

Layer B's `phase-0-seed-loading.md` Step 0.2a parses these verbatim. Changing the canonical ripples into a Layer B branch; v1.3.3 explicitly does not touch Layer B. The asymmetry is intentional: frontmatter is a data contract, body is a human echo.

### What happens in the zero-content branch

If the user's first response to the welcome box contains only the trigger phrase (no content), `content_locale` cannot be resolved. The skill stays in `welcome_locale` for the re-prompt and continues to wait. When content eventually arrives, the mirror flow fires and `content_locale` is resolved at that moment.

### What happens in the modification-loop branch (v1.3.2 consent card)

When the user replies to the consent card with a modification (`garde Type en boulangerie`), the skill re-runs the 9-field extraction with the correction, re-renders the mirror, and re-prints the consent card. `content_locale` is re-evaluated on each extraction; if the correction shifts `langue_detectee`, subsequent surfaces switch locale. Convergence is on the next affirmative or negative response.

## Citations API — signal + dispatch (v1.4.0)

v1.4.0 introduces an optional API-powered extraction path that augments the v1.3.1 in-context extraction with per-field source attribution (`[page N]` for PDF, `[lines X-Y]` for plain-text documents). The path is layered on top of the v1.3.3 locale dispatch — locale and citation are independent concerns, and both flow through the same `phase-0-welcome.md` mirror template.

### Dispatch lifecycle

The skill evaluates **three gates** in order at skill entry (before the welcome box prints):

1. **`is_fresh_context`** — unchanged from v1.3.0 (see § "Trigger evaluation gate"). Controls whether the welcome prints at all.
2. **`welcome_locale`** — unchanged from v1.3.3 (see § "Runtime locale — signal + dispatch (v1.3.3)"). Controls welcome and zero-content re-prompt rendering.
3. **`api_extraction_available`** (new in v1.4.0) — a boolean resolved by checking `ANTHROPIC_API_KEY` in the environment at skill dispatch. If unset or empty, the flag is `false` and the skill commits to the v1.3.3 in-context extraction path for the rest of the session. If set, the flag is `true` and the skill commits to the API extraction path subject to runtime error fallback (§ "Fallback triggers" below).

The gate is evaluated **once** at skill entry and is immutable for the session. Rationale: mid-session environment changes are out-of-scope for a conversational skill — the session's energy is committed at entry.

### Python extractor — invocation contract

**Script path**: `skills/genesis-drop-zone/scripts/extract_with_citations.py`

**Runtime**: resolved via the session-post-processor portability pattern at SKILL.md dispatch time:

```bash
PYTHON=$(command -v python || command -v python3 || command -v py)
```

If no Python is found on `$PATH`, `api_extraction_available` collapses to `false` at the subprocess launch attempt (pre-flight at skill entry checks env key only, not Python presence — the runtime check happens at the call site and triggers the same fallback).

**Input contract**: the SKILL.md dispatch passes the drop-zone content on the extractor's stdin as a single JSON object with these keys:

| Key | Type | Description |
|---|---|---|
| `cwd` | string | Absolute path of the session cwd. Used only for resolving relative attachment paths. Not written to. |
| `attachments` | array of strings | Absolute or cwd-relative paths of files the user dropped (PDFs, text documents, images). Empty array when no attachments. |
| `typed_text` | string | The user's inline typed content from the first content turn. Empty string if user only attached files. See § "Typed-text citation wrapping" below for how non-empty `typed_text` becomes a citeable source. |
| `content_locale_hint` | string | `FR`, `EN`, or `mixte` — the *pre-v1.4.0 in-context best guess* at `langue_detectee`, passed as hint only. The extractor performs its own detection and may override. |
| `model` | string | Model ID to invoke. Default `claude-opus-4-7`. Overridable via `GENESIS_DROP_ZONE_MODEL` env var (see § Environment variables). |

**Output contract (success, exit code 0)**: single JSON object on stdout, UTF-8, with exactly these keys:

| Key | Type | Description |
|---|---|---|
| `schema_version` | integer | Constant `1` (matches `drop_zone_intent.md` frontmatter `schema_version`). |
| `idea_summary` | string | 9-field extraction output. |
| `pour_qui` | string | 9-field extraction output. |
| `type` | string | 9-field extraction output. |
| `nom` | string | 9-field extraction output. |
| `attaches` | string | Mirror `Depose` row verbatim — truncated display, may include `+ N autres`. |
| `langue_detectee` | string | `FR`, `EN`, or `mixte`. |
| `budget_ou_contrainte` | string | 9-field extraction output. |
| `prive_ou_public` | string | 9-field extraction output. |
| `hints_techniques` | string | 9-field extraction output. |
| `<field>_source_citation` | object or omitted | Per-field citation (see § Citation object shape). Omitted (not null) when no citation applies. |
| `usage` | object | Token usage mirror (`input_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens`, `output_tokens`). Informational; SKILL.md dispatch may log to stderr for forensic trail. |

Null-class strings for extracted fields (`"a trouver ensemble"`, `"non mentionne"`, `"non mentionnee"`, `"a affiner — X ou Y"`) follow the v1.3.3 FR canonical contract — the extractor prompt mandates FR canonical regardless of `content_locale_hint`, preserving the Layer B data contract documented in § "Frontmatter data contract unchanged".

**Output contract (failure)**: the extractor emits nothing on stdout and writes a human-readable diagnostic to stderr. Exit codes:

| Exit | Meaning | SKILL.md response |
|---|---|---|
| `0` | Success; valid JSON on stdout. | Parse JSON, proceed with citation-annotated mirror. |
| `2` | `ANTHROPIC_API_KEY` unset at subprocess runtime (rare — pre-flight at skill entry usually catches this). | Fallback to in-context extraction. |
| `3` | SDK import error (Python `anthropic` package not installed). | Fallback. |
| `4` | API error (4xx / 5xx not 429) — bad request, invalid model, auth failure. | Fallback. |
| `5` | Rate limit (429) — the subprocess handled SDK retries and exhausted the budget. | Fallback. |
| `6` | Bad input (malformed JSON on stdin, missing required key). | Fallback. Should never happen in practice — SKILL.md dispatch controls the input shape. |
| `7` | Output JSON shape invalid (post-API schema check failed). | Fallback. |
| any other | Unknown error. | Fallback. |

All fallback paths are **silent to the user**. The skill renders the v1.3.3 in-context mirror with no visible indication that the API path was attempted. Forensic state is subprocess stderr; the SKILL.md dispatch copies stderr to the harness-visible stderr for developer inspection in verbose sessions.

### Fallback triggers

The SKILL.md dispatch commits to the fallback path under any of:

1. `api_extraction_available` is `false` at skill entry (pre-flight env check negative).
2. Python runtime unresolvable at subprocess launch.
3. Subprocess exit code ≠ 0.
4. Subprocess exit code `0` but stdout is not valid UTF-8 JSON, or is JSON but fails the output-shape check (missing required keys, wrong types).

The fallback path is exactly v1.3.3's in-context extraction — no conditional branching, no "degraded citation" mode, no visible difference in the mirror beyond the absence of `[page N]` / `[lines X-Y]` annotations.

### Citation object shape

Per-field citation when available (attached text or PDF, and the API returned a citation for the field):

```yaml
idea_summary_source_citation:
  type: pdf_page_range      # pdf_page_range | text_char_range
  document_index: 0          # zero-based index into the extractor's `documents` array
  start: 1                   # 1-indexed page for PDF; 0-indexed char offset for text
  end: 1                     # inclusive
  cited_text_preview: "boulangerie artisanale avec livraison matin frais..."  # <= 80 chars + ellipsis if truncated
```

Rendered in the mirror as:

```
   Idee          boulangerie artisanale pour livraison matin [page 1]
```

For `text_char_range` citations, the annotation becomes `[lines X-Y]` where `X` and `Y` are derived from the `start` / `end` character offsets via `\n` counting (1-indexed, inclusive). Image-only drops never produce citations — the field renders without annotation.

**Truncation rule interaction with citations**: the mirror truncation rule (row value ≤ 60 chars after the label, truncate at 57 + `...`) applies to the value *before* the annotation. The annotation adds 8–14 characters and may push the row over 60 chars — this is the only exception to the truncation rule. Rationale: truncating the annotation would hide the audit-trail, which is the whole point of v1.4.0. Annotated rows may reach 75 characters in the worst case; still fits within 80-col terminals.

### Typed-text citation wrapping

The Anthropic Citations API produces `cited_text` only for content carried in a `document` block with `citations: {enabled: true}`. Plain inline user text arriving as `typed_text` on the extractor's stdin is **not** citeable by default. v1.4.0 wraps non-empty `typed_text` into a Citations-enabled document block before sending the request, so inline text becomes a legitimate citeable source.

**Wrapping rule**: if `typed_text` is non-empty, the extractor prepends one synthetic document block to the API request:

```python
{
    "type": "document",
    "source": {
        "type": "text",
        "media_type": "text/plain",
        "data": typed_text,
    },
    "title": "User typed text",
    "context": "Inline conversational input from the drop-zone turn.",
    "citations": {"enabled": True},
    "cache_control": {"type": "ephemeral", "ttl": "1h"},
}
```

**Document-array ordering**: the `documents[]` array sent to the API consists of (1) the typed-text synthetic document (index 0) if `typed_text` is non-empty, followed by (2) one document block per file in the `attachments` array (indices 1..N, PDFs as PDF blocks, text files as text blocks, images as image blocks — images carry no `citations` flag because the API does not cite images). If `typed_text` is empty, the typed-text synthetic document is omitted and attachments start at index 0.

**Citation output**: `document_index` in the API's citation response refers to this assembled array. A `document_index: 0` citation with `text_char_range` type on a session with non-empty `typed_text` means the cited span came from inline text; the extractor translates char ranges to line ranges via `\n` counting for display purposes.

**All-or-none rule**: `citations: {enabled: true}` is mandatory per-document per the Citations API contract, and the flag is all-or-none across the request. Image blocks never carry the flag; text and PDF blocks always do.

### Environment variables

| Variable | Default | Effect |
|---|---|---|
| `ANTHROPIC_API_KEY` | unset → fallback | Presence unlocks API extraction. |
| `GENESIS_DROP_ZONE_MODEL` | `claude-opus-4-7` | Override active model. Accepts any Messages-API-compatible model ID. No validation beyond SDK's own. |
| `GENESIS_DROP_ZONE_CACHE_TTL` | `1h` | Override cache TTL. Accepts `5m` or `1h` per Anthropic's cache TTL grammar. Never defaulted to `5m` by omission (R8 § Stage 2 mandate). |
| `GENESIS_DROP_ZONE_VERBOSE` | unset | If set to `1`, the extractor emits detailed stderr tracing (token counts per phase, retry attempts, cache hit/miss). Default is minimal stderr (one line per call). |

### Interaction with the modification loop

When the user replies to the consent card with a modification, the skill re-runs the 9-field extraction. v1.4.0 re-invokes the extractor subprocess on each modification loop iteration — **citations are re-computed**. Cache is a significant economy here: the document block stays in the 1h TTL cache across iterations; only the extraction text prompt varies. Typical modification-loop re-run costs ~0.1× of the first call per R8 § Stage 2 cache economics.

If the `ANTHROPIC_API_KEY` environment variable is revoked mid-session (e.g. user unsets it externally — out-of-scope but possible), the `api_extraction_available` flag **stays `true`** (the gate is immutable per § "Dispatch lifecycle" above — it is evaluated once at skill entry and never re-read). The subprocess still launches on the next modification-loop iteration, hits exit code `2` at its own env check, and the SKILL.md dispatch routes the iteration through the fallback path via the exit-code-≠-0 trigger (fallback trigger 3 in § "Fallback triggers"). The modification loop completes via the in-context extraction path; the re-printed consent card does not indicate the path change.

### Zero Layer B ripple preserved

As with v1.3.3, v1.4.0 touches **zero Layer B files**. The Layer B Step 0.2a parser (dict-based YAML parsing) silently ignores the new `<field>_source_citation` keys when the v1.4.0 extension is written into `drop_zone_intent.md`. Layer B v1.4.1+ may add card / template surfacing of the citations additively, but v1.4.0 itself guarantees byte-level backward compatibility on the fallback path (fallback produces v1.3.3-identical files) and semantic backward compatibility on the API path (additional keys, no removed keys, no schema_version bump).

## Welcome body — FR primary + EN mirror

Both variants are authored in `phase-0-welcome.md` from day 1 per R9. FR is printed by default in v1.3.0. v1.3.3 wires `welcome_locale` so the variant printed reflects the invocation signal (FR on slash or FR intent-match; EN on EN intent-match).

### FR variant (rendered when `welcome_locale = FR`)

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│     Depose ici ton idee.                                   │
│                                                            │
│     Un texte, un PDF, une photo, un lien, un audio —       │
│     tout est bienvenu. Tu peux aussi juste ecrire.         │
│                                                            │
│     (Parcourir les fichiers)                               │
│                                                            │
│     Tes fichiers restent avec toi pendant cette session.   │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### EN variant (rendered when `welcome_locale = EN`)

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│     Drop your idea here.                                   │
│                                                            │
│     Text, PDF, photo, link, audio — anything goes.         │
│     You can also just write.                               │
│                                                            │
│     (Browse files)                                         │
│                                                            │
│     Your files stay with you during this session.          │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### UX canon backing each choice

- **Intent-first unified box** — prompt, files, URLs land together [NxCode AI app builder comparison 2025-2026, verified across v0.app / Bolt.new / Lovable].
- **Dual path rule** — "drop AND browse, always" [Filestack canonical rule on boomer-friendly file upload]. The line `(Parcourir les fichiers)` makes the button visible.
- **Accept-anything line** — IBM Docling established the 2026 bar (PDF, DOCX, PPTX, XLSX, HTML, images, audio → unified representation). Users never pick a parser.
- **Privacy in relationship language, not compliance** — "Tes fichiers restent avec toi pendant cette session" instead of "processed locally" [MIT Tech Review 2026-04-15, "Building trust in the AI era with privacy-led UX"].
- **ASCII-only inside the box, accents allowed outside** — the box mixes Unicode box-drawing characters (`┌ │ ─ └ ┐ ┘`) with content on the same line. That combination has been observed to render unstably on some Windows code-page configurations when content also carries combining diacritics. The bridge message (below) and the context-guard redirect (above) are plain prose lines with no box-drawing, routed through the terminal's stream path which is UTF-8-stable — they keep their accents (`à`, `é`, `ê`, `ô`). This asymmetry is intentional and documented here; it **extends to each new table-bearing surface the plugin adds** (e.g. v1.3.1's 9-field mirror table re-applies it to the row content, with surrounding prose keeping accents — see § "Mirror screen — template & reveal" for the extension).

ASCII-box dimensions: 60 chars wide, 10 lines high. Fits inside 80-col terminal comfortably, preserves text-centering illusion.

## Mirror screen — template & reveal

**v1.3.1 supersedes** v1.3.0's bullet-list acknowledgement. Git history preserves the prior bullet form (`◐ Je regarde... . un brief "X" (PDF, N pages) ... ✓ J'ai tout lu.`); v1.3.1 forward, the mirror is a structured 9-field aligned-column table revealed row-by-row. **v1.3.3** wires `content_locale` so the mirror renders as the FR variant or EN variant depending on `langue_detectee` (see § "Runtime locale — signal + dispatch (v1.3.3)"). Both templates were already authored in v1.3.1 per R9 tier 3; v1.3.3 flips the dispatch switch.

Between the welcome and the bridge, the skill reformulates what the user provided by extracting a 9-field intent schema (see § "Extraction schema — 9 fields" below) and rendering it as an aligned-column table. Underlying UX pattern is Ably's 2026 SSE token-streaming approach [Ably AI UX, "Token streaming for AI UX", 2026] — loading state *transforms into* the final result rather than a spinner that blocks then replaces. Each of the 9 rows appears one at a time.

### Template structure (FR — rendered when `content_locale = FR`)

```
 ◐ Je regarde et je comprends...

   Idee          <idea_summary — user's own words, 1 line>
   Pour qui      <target users — 1 line>
   Type          <kind of project — 1 line>
   Nom           <proposed project name or "a trouver ensemble">
   Depose        <list of dropped items, see truncation rule>
   Langue        <FR / EN / mixte — detected from text>
   Budget        <budget / constraint mention or "non mentionne">
   Visibilite    <private / public mention or "non mentionnee">
   Tech          <tech hints or "non mentionne">

 ✓ Lu et compris.
```

### Template structure (EN — rendered when `content_locale = EN`)

```
 ◐ I read and I understand...

   Idea          <idea_summary>
   Who for       <target users>
   Kind          <kind of project>
   Name          <proposed name or "to be found together">
   Dropped       <list of dropped items>
   Language      <FR / EN / mixed>
   Budget        <budget or "not mentioned">
   Visibility    <visibility or "not mentioned">
   Tech          <tech or "not mentioned">

 ✓ Read and understood.
```

### Alignment and rendering rules

- Labels padded to 14 characters (left-aligned), 2-space separator, value flows right.
- ASCII pure inside the table block — no accents in label or value rows (v1.3.0 rule preserved for Windows code-page stability). Accents are allowed in the opening `◐` line, the closing `✓` line, and prose values only when genuinely needed (rare — the mirror is factual, not prose).
- Row reveal is **token-streamed** one-by-one; `◐` stays visible until the 9th row renders, then `✓` closes.
- No blocking spinner, no blank screen. Welcome box's own rendering is the only moment with no partial output.

### Zero-content branch (v1.3.0 preserved, v1.3.3 locale-switched)

If the user's response contains only the trigger phrase with no content to echo, the skill prints the zero-content re-prompt. v1.3.3 dispatches on `welcome_locale` — no `content_locale` exists yet because no content has been extracted.

FR variant (rendered when `welcome_locale = FR`):

```
 Je t'écoute — dépose ou écris ce que tu veux me partager.
```

EN variant (rendered when `welcome_locale = EN`, **newly-authored in v1.3.3** — the one new bilingual pair v1.3.3 ships):

```
 I'm listening — drop or write whatever you want to share.
```

No `◐`, no mirror, no `✓`. The skill waits for the user's next turn and re-runs the mirror flow when content arrives. When content arrives, `content_locale` is resolved from `langue_detectee` and subsequent surfaces (mirror, consent card, halt, bridges, body echo) render in that locale — independent of `welcome_locale` (see § "Runtime locale — signal + dispatch (v1.3.3) / Divergence").

### Unreadable-attachment branch

If Claude cannot read an attached file (exotic binary, oversize PDF past 32 MB × 600 pages per Files API limits [Claude API docs, PDF support]), the `Depose` / `Dropped` row lists the file alongside readable items:

```
   Depose        1 brief "X" + 1 fichier illisible : <filename>
```

Extraction of the other 8 fields continues from readable content. Graceful, no error code — matches the anti-jargon error-message rule [v2_promptor_fusion_landscape_2026-04-17.md § Stage 1 failure-mode table].

### Very-thin content branch

If the user's content yields few extractable fields (e.g. "j'ai une idee de projet" with no attachments):

```
 ◐ Je regarde et je comprends...

   Idee          "j'ai une idee de projet"
   Pour qui      a trouver ensemble
   Type          a trouver ensemble
   Nom           a trouver ensemble
   Depose        texte seul
   Langue        FR
   Budget        non mentionne
   Visibilite    non mentionnee
   Tech          non mentionne

 ✓ Lu et compris.
```

Honest disclosure — the mirror renders all 9 rows regardless. Missing-core rows show `a trouver ensemble` (signalling the Étape 1 Q&A to come); missing-bonus rows show `non mentionne(e)`.

### Truncation rules

- Each row value ≤ 60 characters after the label. If longer, truncate at 57 + `...`.
- `Depose` / `Dropped` lists at most 3 items explicitly; beyond 3, append `+ N autres`.
- `Idee` / `Idea` value: Victor's own words when possible; if the user wrote a paragraph, condense to ≤ 60 chars (the full content stays in Claude's context for v1.3.2+ handoff — only the display is truncated).

### Ambiguity handling

If the user's content carries ambiguity on a field (e.g. "boulangerie OU restaurant, je sais pas encore"), the row value notes the ambiguity explicitly:

```
   Type          a affiner — boulangerie ou restaurant
```

`a affiner` is the third null-class label (beside `a trouver ensemble` and `non mentionne`). It signals "there's something, but it needs the user's arbitrage" — a natural hand-off point for Étape 1.

## Extraction schema — 9 fields

The mirror displays 9 fields. Each field has an internal name, a bilingual label, a semantic purpose, and a null-class convention when the value cannot be extracted.

| Internal name | Label FR | Label EN | Semantic | Null class when missing |
|---|---|---|---|---|
| `idea_summary` | Idee | Idea | 1-line synopsis of the user's idea, in user's own words when possible. Always filled when any content is present — mirror only fires when content is non-zero (zero-content branch re-prompts instead). | `a trouver ensemble` (class 1 degenerate fallback if content is zero-like after the guard). |
| `pour_qui` | Pour qui | Who for | Target users / audience inferred from content. | `a trouver ensemble` (core) |
| `type` | Type | Kind | Rough category: appli web, appli mobile, outil CLI, plugin, documentation, site, bibliotheque, … | `a trouver ensemble` (core) |
| `nom` | Nom | Name | Project name if the user proposed one (explicit — not auto-slugged). | `a trouver ensemble` (core) |
| `attaches` | Depose | Dropped | List of dropped items with brief descriptor (see truncation rule). `texte seul` if nothing attached. | `texte seul` when no attachment; otherwise always filled with item list. |
| `langue_detectee` | Langue | Language | `FR` / `EN` / `mixte` — detected from the user's text. Extracted in v1.3.1; starting **v1.3.3** this field is the signal source for `content_locale`, which switches mirror / consent card / halt / bridge / body-echo rendering between FR and EN variants (see § "Runtime locale — signal + dispatch (v1.3.3)"). `mixte` → FR tiebreaker. | N/A — always filled. |
| `budget_ou_contrainte` | Budget | Budget | Explicit budget / deadline / resource constraint mentioned. | `non mentionne` (bonus) |
| `prive_ou_public` | Visibilite | Visibility | Explicit private / public / team-only mention for the project. | `non mentionnee` (bonus — feminine agreement) |
| `hints_techniques` | Tech | Tech | Tech hints (stack, framework, platform) mentioned or inferred. | `non mentionne` (bonus) |

### Null-class convention

Three null classes in priority of display expressiveness:

1. **`a trouver ensemble`** — core field missing. Signals the gap will be closed in the next Layer A step (Étape 1 Q&A). Used for `pour_qui`, `type`, `nom`.
2. **`non mentionne(e)`** — bonus field missing. Signals not-blocking, Genesis doesn't need this to proceed. Used for `budget_ou_contrainte`, `prive_ou_public`, `hints_techniques`.
3. **`a affiner — <two or more hypotheses>`** — ambiguity, user's arbitrage needed. Applied on any field when the content supports multiple interpretations.

Three is the deliberate maximum. No `null`, no `?`, no `n/a`, no empty string — the mirror is Victor-facing runtime text, not a developer dump.

### Where the schema lives

In v1.3.1 the schema is held in Claude's conversational context — not serialized to disk, not printed as JSON, not handed off to any external consumer. Claude instructs itself (via the SKILL.md dispatch) to extract the 9 fields at acknowledgement time and render them as the mirror. The schema's persistence is the conversation's own duration; v1.3.2+ extraction writes this into `bootstrap_intent.md` (first concentrated privilege of Layer A).

### Why 9 fields (not 5)

- **Victor-legibility gate**: each field is named in a language Victor reads naturally. `Tech`, `Budget`, `Visibilite` are not dev jargon. `hints_techniques` stays internal; the label shown to Victor is `Tech`.
- **Non-overlapping**: the 4 bonus fields describe orthogonal axes (language, money, privacy, technology). None are derivable from the 5 core fields.
- **Cheap to extract in-context**: multimodal Claude already reads the dropped content end-to-end for the 5 core fields. Adding 4 passes in the same extraction step costs nothing — no API round-trip, no additional latency.
- **Null-visible discipline preserves honesty**: missing bonus fields render as `non mentionne` — Victor sees Genesis tracking them without pretending they are filled.

## Bridge message — bilingual (v1.3.1 update)

Closes the interaction honestly. Always printed **in both languages**, regardless of the invocation language (runtime locale detection deferred v1.3.2+). v1.3.0's bridge claimed "Extraction et création arrivent bientôt" — that became false as of v1.3.1 (extraction has now run). The v1.3.1 bridge reflects that extraction is done and only the project's actual creation (GitHub repo, files on disk, memory system) remains deferred.

```
Création du projet (GitHub, fichiers, mémoire) arrive bientôt.
Pour l'instant, j'ai lu et compris — reviens à Claude Code normalement.

Project creation (GitHub, files, memory) is coming soon.
For now, I've read and understood — go back to Claude Code normally.
```

"Création du projet" enumerates its three concrete deliverables (GitHub repo / files / memory) — promise is tangible, not abstract. "J'ai lu et compris" replaces v1.3.0's "j'ai bien vu" — catalogue becomes comprehension. "Bientôt" / "soon" stays time-free, no version number hard-coded.

**Accent discipline**: the bridge is plain-prose, non-table content routed through the terminal's UTF-8-stable stream path — it **keeps its accents** (`é`, `ô`, `à`, `—`), same as the v1.3.0 bridge. The ASCII-only discipline applies only to table content (welcome box and the v1.3.1 mirror), where Unicode box-drawing combined with combining diacritics has rendered unstably on some Windows code-page configurations. This asymmetry is the same pattern established in v1.3.0 and documented once there; the v1.3.1 mirror table extends it — mirror rows stay ASCII-pure, surrounding prose (`◐ Je regarde...`, `✓ Lu et compris.`) and the bridge keep accents.

**v1.3.2 supersession note**: the v1.3.1 bridge above is retained as regression-set context but is **superseded at runtime** in v1.3.2 by two version-scoped bridges — an accept-bridge printed after a successful write, and a decline-bridge printed when the user declines the consent card. See § "Bridge messages — accept and decline (v1.3.2)" below for the exact text. A v1.3.2 session never prints the v1.3.1 bridge above; the v1.3.1 bridge only fires for installations still pinned to v1.3.1.

## Consent card — template + flow (v1.3.2, v1.3.3 locale-switched)

v1.3.2 introduced a bilingual accept/cancel consent card between the mirror's `✓ Lu et compris.` (or `✓ Read and understood.`) line and the bridge. The card is the user's gate into the first Layer A concentrated privilege (writing `drop_zone_intent.md` to cwd). Minimal by design — one warm sentence, absolute target path rendered with an arrow marker, natural-language response. **v1.3.3** dispatches on `content_locale`: the FR variant or EN variant is printed (not both). Both variants were already authored in v1.3.2 per R9 tier 3; v1.3.3 flips the dispatch switch.

### Template — FR variant (rendered when `content_locale = FR`)

```
Je peux noter ton projet dans un fichier ici :
  → <absolute-cwd-path>/drop_zone_intent.md

Ce fichier sera le point de départ pour Claude Code la prochaine fois.
On le garde comme ça ?  (oui pour l'écrire, non pour annuler)
```

### Template — EN variant (rendered when `content_locale = EN`)

```
I can save your project here:
  → <absolute-cwd-path>/drop_zone_intent.md

This file becomes Claude Code's starting point next time.
Keep it this way?  (yes to write, no to cancel)
```

### Rendering rules

- **Plain-prose, one variant at a time** — v1.3.2 printed both; v1.3.3 prints only the `content_locale` variant. Same stability discipline as the v1.3.1 bridge. Accents allowed (`é`, `à`, `ê`, `ô`).
- **Absolute path resolution** — resolve the target directory at prompt time via the terminal's current working directory (`os.getcwd()` equivalent for the runtime, `pwd` on POSIX, `%CD%` on Windows). Path separator follows platform convention (`\` on Windows, `/` elsewhere). Arrow marker `→` is U+2192, UTF-8-stable on both terminals.
- **Path uniqueness** — one path per session, resolved once at entry. Changes in cwd mid-session are not re-computed (cwd is frozen at skill dispatch). If the user somehow changes cwd between mirror and consent card, the skill still resolves to the entry-time cwd for coherence.
- **No timeout** — the skill idles until the next user turn. Victor can walk away, come back, inspect the file system, and then respond. The context guard has already verified `is_fresh_context` at skill entry, so the session's premise is stable.

### User response handling

Three equivalence classes on the next user turn:

1. **Affirmative** — common forms in either language: `oui`, `yes`, `y`, `ok`, `d'accord`, `go`, `garde`, `écris`, `save`, `keep`. Skill proceeds to write flow (§ "Write flow"). Interpretation is natural-language — Claude evaluates the response, not a regex match.
2. **Negative** — common forms: `non`, `no`, `n`, `cancel`, `annule`, `abort`, `stop`, `nope`. Skill proceeds to decline flow (§ "Bridge messages — accept and decline"), no write.
3. **Modification** — the user asks to change a value on one or more mirror fields (`garde Type en boulangerie`, `le nom c'est VelyzyBake`, `non c'est pour un restaurant pas une boulangerie`). Claude re-runs the 9-field extraction with the modification applied, re-renders the mirror with updated rows, and re-prints the consent card. Loop until the user converges to class 1 or class 2. No iteration cap — the card is the only gate out.

Modifications that clear ambiguity (e.g. "boulangerie ou restaurant → boulangerie") collapse the corresponding `a affiner — ...` null-class value into the concrete chosen value.

## `drop_zone_intent.md` — schema + body format (v1.3.2, v1.3.3 body locale-switched)

The file written to cwd after consent. Format chosen to match the house style for Genesis artefacts (YAML frontmatter + Markdown body), parseable downstream, readable to a human reader, and archive-fidelity on the mirror Victor saw. **v1.3.3** dispatches the body prose intro + mirror echo on `content_locale`: a file written after an EN drop carries an EN body (see § "Example concrete file (EN variant, v1.3.3)" below). **Frontmatter is unchanged** — keys stay snake_case English; null-class token values stay FR canonical regardless of `content_locale` (Layer A / Layer B contract preserved — see § "Runtime locale — signal + dispatch (v1.3.3) / Frontmatter data contract unchanged").

### Full template

````markdown
<!-- SPDX-License-Identifier: MIT -->
---
schema_version: 1
created_at: <ISO-8601 UTC timestamp>
skill: genesis-drop-zone
skill_version: <plugin.json version at write time>

idea_summary: "<value or null-class string>"
pour_qui: "<value or null-class string>"
type: "<value or null-class string>"
nom: "<value or null-class string>"
attaches: "<mirror Depose field verbatim — truncated display>"
langue_detectee: "<FR / EN / mixte>"
budget_ou_contrainte: "<value or null-class string>"
prive_ou_public: "<value or null-class string>"
hints_techniques: "<value or null-class string>"
---

# Intent capturé à la drop zone le <YYYY-MM-DD>

Fichier écrit par `genesis-drop-zone` v<version> après consent utilisateur.
Lisible comme seed par `genesis-protocol` Phase 0 (Step 0.1 détection + Step 0.2a parsing).

## Mirror affiché à l'utilisateur

```
   Idee          <idea_summary value>
   Pour qui      <pour_qui value>
   Type          <type value>
   Nom           <nom value>
   Depose        <attaches value>
   Langue        <langue_detectee value>
   Budget        <budget_ou_contrainte value>
   Visibilite    <prive_ou_public value>
   Tech          <hints_techniques value>
```
````

### Field conventions

- **9 semantic fields** use snake_case English internal names (R9 tier dev-layer data). The FR/EN labels shown in the mirror live only in `phase-0-welcome.md`; the frontmatter keys are language-neutral.
- **4 metadata keys** provide forward-compat and debuggability: `schema_version` (integer, starting at `1`), `created_at` (ISO-8601 UTC per Python / Node `datetime.now(UTC).isoformat()` convention), `skill` (constant `genesis-drop-zone`), `skill_version` (read from `plugin.json` at write time).
- **Null-class strings serialized verbatim** — `"a trouver ensemble"`, `"non mentionne"`, `"non mentionnee"`, `"a affiner — X ou Y"`. Never `null`, never `~`, never `""`, never an empty YAML value. The null-visible discipline Victor sees in the mirror propagates into the file so downstream readers (Phase 0 Step 0.2a) can distinguish "user didn't say" from "field present but empty".
- **`attaches` field** — free-form descriptive string matching the mirror's `Depose` row verbatim (truncated display, `+ N autres` suffix when applicable). Not a canonical attachment list — Layer B scans cwd via `Glob` in Step 0.3 for the source of truth. `attaches` exists so the file is self-documenting without referencing the filesystem.
- **Body** — contains a short prose intro + echo of the mirror table. **v1.3.2** hardcoded FR. **v1.3.3** dispatches on `content_locale`: FR body when `content_locale = FR`, EN body when `content_locale = EN`. Echo format stays ASCII-pure inside the code fence regardless of locale (same accent discipline as the mirror). The body is archive fidelity for the user's benefit if they ever open the file; the frontmatter is the parseable contract.

### File metadata

- **Encoding**: UTF-8 without BOM. Consistent with the rest of the Genesis repo. Modern Windows tools handle it; edge cases (notepad.exe on pre-2019 builds) are out of scope for v1.3.2.
- **Line endings**: LF. Git-friendly. Future `.gitattributes` on the target project can enable `eol=crlf` checkout if a Windows user's downstream toolchain needs it; the written file does not bake CRLF in.
- **Permissions**: OS default. Windows inherits from the parent directory; POSIX applies umask (`0644` typical). No explicit `chmod` — the file is data, not executable.

### Example concrete file — FR body variant (illustrative, `content_locale = FR`)

````markdown
<!-- SPDX-License-Identifier: MIT -->
---
schema_version: 1
created_at: 2026-04-17T14:32:05Z
skill: genesis-drop-zone
skill_version: 1.3.3

idea_summary: "boulangerie artisanale pour livraison matin"
pour_qui: "habitants du quartier qui veulent du pain frais"
type: "application web avec commande en ligne"
nom: "a trouver ensemble"
attaches: "1 brief 'cahier_des_charges.pdf' + 1 photo 'logo.png'"
langue_detectee: "FR"
budget_ou_contrainte: "non mentionne"
prive_ou_public: "non mentionnee"
hints_techniques: "React ou Next.js"
---

# Intent capturé à la drop zone le 2026-04-17

Fichier écrit par `genesis-drop-zone` v1.3.3 après consent utilisateur.
Lisible comme seed par `genesis-protocol` Phase 0 (Step 0.1 détection + Step 0.2a parsing).

## Mirror affiché à l'utilisateur

```
   Idee          boulangerie artisanale pour livraison matin
   Pour qui      habitants du quartier qui veulent du pain frais
   Type          application web avec commande en ligne
   Nom           a trouver ensemble
   Depose        1 brief 'cahier_des_charges.pdf' + 1 photo 'logo.png'
   Langue        FR
   Budget        non mentionne
   Visibilite    non mentionnee
   Tech          React ou Next.js
```
````

### Example concrete file — EN body variant (illustrative, `content_locale = EN`, v1.3.3)

Note: frontmatter **still carries FR canonical null-class tokens** (`"non mentionne"`, `"non mentionnee"`) even though the body echoes the EN mirror. Intentional Layer A / Layer B asymmetry — the frontmatter is the parseable contract.

````markdown
<!-- SPDX-License-Identifier: MIT -->
---
schema_version: 1
created_at: 2026-04-17T14:32:05Z
skill: genesis-drop-zone
skill_version: 1.3.3

idea_summary: "artisan bakery for morning delivery"
pour_qui: "neighbourhood residents wanting fresh bread"
type: "web app with online ordering"
nom: "a trouver ensemble"
attaches: "1 brief 'brief.pdf' + 1 photo 'logo.png'"
langue_detectee: "EN"
budget_ou_contrainte: "non mentionne"
prive_ou_public: "non mentionnee"
hints_techniques: "React or Next.js"
---

# Intent captured at the drop zone on 2026-04-17

File written by `genesis-drop-zone` v1.3.3 after user consent.
Readable as a seed by `genesis-protocol` Phase 0 (Step 0.1 detection + Step 0.2a parsing).

## Mirror shown to the user

```
   Idea          artisan bakery for morning delivery
   Who for       neighbourhood residents wanting fresh bread
   Kind          web app with online ordering
   Name          to be found together
   Dropped       1 brief 'brief.pdf' + 1 photo 'logo.png'
   Language      EN
   Budget        not mentioned
   Visibility    not mentioned
   Tech          React or Next.js
```
````

In the EN body, null-class values render in EN display form (`to be found together`, `not mentioned`) for human readability of the mirror echo. In the frontmatter, null-class tokens stay FR canonical (`"a trouver ensemble"`, `"non mentionne"`) for Layer B's Step 0.2a parser. The contract preserves zero-ripple onto Layer B.

## Write flow — consent → write → bridge (v1.3.2)

The end-to-end state machine from mirror close through skill exit.

### Canonical sequence (happy path)

```
1. /genesis-drop-zone invoked (slash or intent match)
2. Context guard → is_fresh_context == true
3. Welcome box prints (FR v1.3.1)
4. User drops content (text + files + URLs)
5. Mirror renders token-streamed 9 rows (v1.3.1)
6. Pre-write existence check on <cwd>/drop_zone_intent.md
   ├── file exists → halt branch (§ "Halt branch — file already exists")
   └── file absent → proceed
7. Consent card prints (§ "Consent card")
8. User responds
   ├── affirmative → branch A (write)
   ├── negative → branch B (decline)
   └── modification → re-run extraction, re-render mirror, re-print consent card, loop
9a. Branch A — write drop_zone_intent.md to cwd
    ├── atomic write (temp file + rename)
    ├── post-write existence + size verification
    ├── accept-bridge prints
    └── exit clean
9b. Branch B — no write
    ├── decline-bridge prints
    └── exit clean
```

### Pre-write existence check ordering

The check at step 6 fires **after the mirror renders** and **before the consent card prints**. Rationale: the mirror is a read-only, zero-cost render (no filesystem mutation risk), while the consent card is a promise to the user ("can I save here?"). Showing the consent card when the halt condition is already known would be bait-and-switch — the user answers `oui` and gets halted anyway. Running the check before the card preserves honesty.

The mirror still renders when the halt branch fires — Victor sees what was extracted from his content, then learns the write cannot proceed. This preserves the "I read and I understand" acknowledgement that v1.3.1 guarantees, independently of whether a write will follow.

### Atomic write mechanics (Branch A)

1. Compose the full file content per § "`drop_zone_intent.md` — schema + body format".
2. Resolve target path: `<absolute-cwd-path>/drop_zone_intent.md`.
3. Write the content to a temporary file in the same directory: `<absolute-cwd-path>/drop_zone_intent.md.tmp` (same-dir tmp guarantees the rename stays on the same filesystem — atomic on POSIX, best-effort on Windows).
4. Rename `drop_zone_intent.md.tmp` → `drop_zone_intent.md`. On both POSIX and Windows, this is the canonical atomic-or-near-atomic file-replacement pattern.
5. Post-write verification: assert `os.path.exists(target)` and `os.path.getsize(target) > 0`. If either fails, the write is considered partial — print a bilingual failure message ("la sauvegarde a échoué, rien n'a été écrit / save failed, nothing written"), delete any stale `.tmp` remnant, exit without printing the accept bridge. This failure mode is rare (disk full, permission denied, filesystem race) and lets `OSError`-class exceptions bubble up for the harness to surface — v1.3.2 ships basic detection, not full error-handling taxonomy.
6. Print the accept bridge (§ "Bridge messages — accept and decline").
7. Exit clean.

### Error handling scope — what v1.3.2 does NOT handle

Per anti-Frankenstein narrow-privilege discipline, v1.3.2 does not surface custom halt + remediation messages for:

- **Permission denied on cwd** — Victor opened Claude Code in a read-only folder. `OSError` propagates naturally; Claude Code harness surfaces it.
- **Disk full** — same treatment.
- **`drop_zone_intent.md` is a symlink or directory** — the `exists()` check catches both cases as "file exists" and routes to the halt branch, which is the safe default.
- **Cwd deleted mid-flight** — theoretically possible if the user removes the folder between mirror and consent; `OSError` at write time.

Any of these producing real user pain in v1.3.2 is a v1.3.3+ candidate for a halt + remediation refinement. v1.3.2's floor is "write succeeds or the harness shows the stack".

## Halt branch — file already exists (v1.3.2, v1.3.3 locale-switched)

When the pre-write existence check at step 6 of the write flow finds a `drop_zone_intent.md` already in cwd, the skill prints a halt message and exits without proceeding to the consent card. **v1.3.3** dispatches on `content_locale`: the FR variant or EN variant is printed (not both). Both variants were already authored in v1.3.2.

### Template — FR variant (rendered when `content_locale = FR`)

```
Un fichier `drop_zone_intent.md` existe déjà ici :
  → <absolute-cwd-path>/drop_zone_intent.md

Supprime-le d'abord, ou ouvre Claude Code dans un autre dossier et relance.
```

### Template — EN variant (rendered when `content_locale = EN`)

```
A `drop_zone_intent.md` already exists here:
  → <absolute-cwd-path>/drop_zone_intent.md

Delete it first, or open Claude Code in a different folder and retry.
```

### Behaviour

- Printed **in place of** the consent card — the user never sees an accept/cancel prompt when the halt fires.
- Exit clean immediately after the halt message. No stack trace, no error code, no retry loop.
- **No overwrite, no timestamp-suffix fallback, no "are you sure" second-consent prompt.** The anomaly is genuine (the context guard has already asserted a fresh cwd on entry — an existing `drop_zone_intent.md` is unexpected state that the user should reconcile manually).
- Matches the halt-on-leak gate precedent of `session-post-processor` — when a ship-critical invariant fails, halt with remediation message, never mask-then-recover.

## Bridge messages — accept and decline (v1.3.2, v1.3.3 locale-switched)

Two version-scoped bridges replace the v1.3.1 single bridge. Selection is determined by the user's response to the consent card: accept → accept bridge + write; decline → decline bridge, no write. Both route through the UTF-8-stable stream path and keep accents. **v1.3.3** dispatches on `content_locale`: one variant printed, not both. Both variants were already authored in v1.3.2.

### Accept bridge (Branch A, after successful write)

FR variant (rendered when `content_locale = FR`):

```
C'est noté — tape `/genesis-protocol` quand tu es prêt pour créer
le projet (GitHub, fichiers, mémoire) à partir de ce fichier.
```

EN variant (rendered when `content_locale = EN`):

```
Saved — type `/genesis-protocol` when you're ready to create the
project (GitHub, files, memory) from this file.
```

- Path **not re-repeated** — the consent card rendered 2 lines above already showed the absolute path. Repeating it in the bridge would alourdir without adding information.
- `/genesis-protocol` in backticks signals the slash-command (parseable by terminals that auto-link slash-commands in Claude Code).
- "C'est noté" / "Saved" — past-tense signals the write has already happened before the bridge prints.
- "(GitHub, fichiers, mémoire)" / "(GitHub, files, memory)" enumerates the three concrete deliverables of Layer B bootstrap — same promise pattern as the v1.3.1 bridge.

### Decline bridge (Branch B, after user says no)

FR variant (rendered when `content_locale = FR`):

```
OK, rien d'écrit. Ton idée reste dans notre échange pour l'instant.
Relance-moi quand tu veux la poser sur disque.
```

EN variant (rendered when `content_locale = EN`):

```
OK, nothing written. Your idea stays in our exchange for now.
Come back whenever you want to save it to disk.
```

- "OK" / "OK" — acknowledges the refusal without judgement.
- "Rien d'écrit" / "Nothing written" — explicit confirmation so Victor knows his refusal was honoured.
- "Ton idée reste dans notre échange" / "Your idea stays in our exchange" — warm framing: the work isn't lost, it's simply not persisted.
- "Relance-moi quand tu veux" / "Come back whenever you want" — non-pressurizing invitation. No deadline, no nudge.

### Why two variants and not one with a conditional tail

A single bridge with a conditional tail (approach C in the brainstorming) would dilute two fundamentally different messages — one acknowledging an action taken, one acknowledging an action refused. Two variants keep each voice honest to its branch. The accept bridge instructs; the decline bridge invites. A unified opening would water both down.

## Layer B integration — genesis-protocol Phase 0 (v1.3.2)

The Layer A write is meaningful only when Layer B reads the written file. v1.3.2 extends `genesis-protocol`'s Phase 0 Seed runbook to detect, parse, map, and archive `drop_zone_intent.md`.

### Files touched in `genesis-protocol`

| File | Nature of change |
|---|---|
| `skills/genesis-protocol/phase-0-seed-loading.md` | Step 0.1 gains a `drop_zone_intent.md` detection row + precedence note. New Step 0.2a inserted before Step 0.2 to parse the YAML frontmatter and map to Layer B fields. Step 0.4 card template extended with origin tags per field + new `Additional context from drop zone` block. Step 0.5 `bootstrap_intent.md` template extended with new `## Conversational context from drop zone` section. |
| `skills/genesis-protocol/SKILL.md` | Phase 0 paragraph extended to name `drop_zone_intent.md` as the alternative primary seed (precedence over `config.txt`). |
| `skills/genesis-protocol/verification.md` | New scenario covering `drop_zone_intent.md` as Phase 0 seed + regression scenario covering both-files-present precedence. |

### Precedence rule (Step 0.1)

When Phase 0 Step 0.1 inspects the target folder, it checks for seeds in this order:

1. `drop_zone_intent.md` present → **primary seed**. Parse via YAML frontmatter in Step 0.2a.
2. No `drop_zone_intent.md`, `config.txt` present → **legacy seed**. Parse via free-form text extraction in Step 0.2 (existing behaviour).
3. Both present → **drop_zone_intent.md wins**. Log a precedence note: `config.txt found but drop_zone_intent.md takes precedence — ignoring config.txt`. Never merge silently.
4. Neither present → offer the interactive seed card (existing Step 0.2 fallback).

### Field mapping (Step 0.2a)

Drop-zone frontmatter fields → Layer B Phase 0 intent fields. The `nom` source field maps to two Layer B fields (Project name, Project slug) — the table lists both rows for clarity; the second row's "Transform" column makes the derivation step explicit.

| Layer A frontmatter | Layer B field | Transform |
|---|---|---|
| `idea_summary` | Vision (one-paragraph) | Verbatim. User can expand at Step 0.4 edit. If the 1-line synopsis is too short to serve as a paragraph Vision, the gap surfaces as an edit opportunity — Phase 0 does not synthesize a paragraph from Layer A atoms. |
| `nom` (source field) | Project name | Direct if `nom` is a real value. If `nom` is null-class (`a trouver ensemble`), Step 0.4 card prompts the user for the name. |
| `nom` (same source, derived) | Project slug | Derive from the resolved Project name per the existing rule (lowercase, spaces → `-`, strip accents, alphanumeric + `-` only, < 50 chars). Slug is null until the name is set. |
| `type` | Is-a-plugin | Inferred: if the `type` value contains the substring `plugin` (case-insensitive), map to `yes`; otherwise `no`. User can edit at Step 0.4. |
| `hints_techniques` | Stack hints | Direct. If null-class, render as `[none]` on the card. |
| `attaches` | Mixed media | Informational only. Phase 0 Step 0.3 still scans cwd via `Glob` for the canonical list; `attaches` describes what the user saw in their mirror. |
| `pour_qui` | (no Layer B field) | Archived in § "Conversational context from drop zone" section of `memory/project/bootstrap_intent.md` (Step 0.5 write). |
| `langue_detectee` | (no Layer B field) | Same archival treatment. |
| `budget_ou_contrainte` | (no Layer B field) | Same archival treatment. |
| `prive_ou_public` | (no Layer B field) | Same archival treatment. |
| (absent from Layer A) | License | Default MIT per existing Phase 0 rule. |
| (absent from Layer A) | Plan tier | Phase 0 Step 0.4 card prompts the user if missing. |
| (absent from Layer A) | Scope locks | Phase 0 Step 0.4 default `[none]`; user can edit. |

### Step 0.4 intent card template (extended)

```
📋 Parsed intent — Phase 0

Target folder          : <absolute path>
Project name           : <value or [missing]> (<origin>)
Project slug           : <derived or [pending name]>
Vision                 : <value or [missing]> (<origin>)
Stack hints            : <value or [none]> (<origin>)
License                : <value or MIT (default)>
Is-a-plugin            : <yes | no | [missing]> (<origin>)
Plan tier              : <value or [missing]>
Scope locks            : <list or [none]>
Mixed media            : <file list>

Additional context from drop zone:            ← rendered only if drop_zone_intent.md seeded
  Target audience      : <pour_qui value>
  Language detected    : <FR | EN | mixte>
  Budget / constraint  : <budget_ou_contrainte value>
  Visibility           : <prive_ou_public value>

Gaps to fill before Phase 1:
  - <gap 1>
  - <gap 2>

Proceed with these values?  (yes / edit / abort)
```

Origin tags on each field: `(from drop zone)`, `(from config.txt)`, `(derived)`, `(default)`, `(inferred)`. The `Additional context from drop zone` block renders only when the seed source was `drop_zone_intent.md` (never a blank block for legacy config.txt sessions). Wording visible to the user is deliberately non-jargon — `(from drop zone)` rather than `(from Layer A)`. Mode dispatch (auto / semi-auto / detailed) stays unchanged — Category C consent gate.

### Step 0.5 `bootstrap_intent.md` template (extended)

After the existing sections (`## Parsed at`, `## Fields`, `## Raw config.txt`, `## Gaps noted at Phase 0`), a new section is rendered **only when `drop_zone_intent.md` was the seed source**:

```markdown
## Conversational context from drop zone

(Rendered only when `drop_zone_intent.md` was the Phase 0 seed source.)

| Field | Value |
|---|---|
| Target audience (pour qui) | <value or "a trouver ensemble"> |
| Language detected | <FR / EN / mixte> |
| Budget or constraint | <value or "non mentionne"> |
| Visibility (private / public) | <value or "non mentionnee"> |

Source: `drop_zone_intent.md` written by `genesis-drop-zone` v<version> at <ISO timestamp>.
```

The existing `## Raw config.txt` section is retained in the template but rendered as `n/a — seeded from drop_zone_intent.md` when the source was Layer A. This preserves the file's section structure across both seed paths and makes the seed source explicit to any future reader.

### Citation rendering (v1.4.1)

Extends Step 0.2a / Step 0.4 / Step 0.5 with read-only rendering of the `<field>_source_citation` nested keys introduced by v1.4.0. Zero parser change (dict-based YAML already reads the full frontmatter); rendering logic gains conditional branches on key presence.

#### Dispatch lifecycle

Three gates determine whether citation suffixes render:

1. **Seed source was `drop_zone_intent.md`** — Step 0.1 logged `Primary seed: drop_zone_intent.md`. Legacy `config.txt` seeds have no citation source at all — all rows render without suffixes (v1.3.2 parity).
2. **Step 0.2a parse succeeded** with `schema_version == 1`. Parse failures fall through to `config.txt` path per v1.3.2 rule — same gate 1 outcome applies.
3. **At least one `<field>_source_citation` key present** in the parsed frontmatter. When all citation keys are absent (fallback-path write, image-only drop, legacy v1.3.2 / v1.3.3 writer), no row renders a suffix. This is anti-Frankenstein null-visible discipline: absence of citation is not rendered as `[unknown]` or `[n/a]` — it is simply absent.

Gate 3 evaluation is per-row, not per-card: each of the 9 citation-eligible rows (5 mapped + 4 extras) inspects its own citation key independently. Of the 5 mapped rows, 3 (Project name / Vision / Stack hints) source directly from their Layer A field's citation, and 2 (Project slug / Is-a-plugin) propagate from an upstream source field's citation. A card with some-but-not-all citations renders suffixes only on the populated rows.

#### Annotation format — single source of truth

The suffix format is **identical** to `skills/genesis-drop-zone/phase-0-welcome.md § "Citation annotation format (v1.4.0)"`. No re-definition in Layer B:

- `pdf_page_range` with `start == end` → ` [page N]`
- `pdf_page_range` with `start != end` → ` [pages N-M]`
- `text_char_range` → ` [lines X-Y]` (1-indexed, inclusive; derivation via `\n` counting on source text, identical to Layer A)

Language-neutral ASCII. No locale dispatch. Rendering is byte-identical across the FR / EN / mixte content_locale values.

One space separator between the value (or origin tag) and the suffix. No trailing punctuation.

#### Step 0.4 card — extended template

The v1.3.2 template is extended with inline citation suffixes on 4 mapped rows + 4 extras rows. The card layout, column widths, and origin-tag positions are preserved.

```
📋 Parsed intent — Phase 0

Target folder          : <absolute path>
Project name           : <value or [missing]> (<origin>)<citation>
Project slug           : <derived or [pending name]><citation>
Vision                 : <value or [missing]> (<origin>)<citation>
Stack hints            : <value or [none]> (<origin>)<citation>
License                : <value or MIT (default)>
Is-a-plugin            : <yes | no | [missing]> (<origin>)<citation>
Plan tier              : <Max | Pro | Team | Free | [missing]>
Scope locks            : <list or [none]>
Mixed media            : <file list or [none]>

Additional context from drop zone:            ← rendered only if drop_zone_intent.md seeded
  Target audience      : <pour_qui value><citation>
  Language detected    : <FR | EN | mixte><citation>
  Budget / constraint  : <value or non mentionne><citation>
  Visibility           : <value or non mentionnee><citation>

Gaps to fill before Phase 1:
  - <gap 1>
  - <gap 2>
  ...

Proceed with these values?  (yes / edit / abort)
```

Where `<citation>` is:
- **empty** (zero characters, no leading space) when the corresponding `<source>_source_citation` key is absent
- ` [page N]` / ` [pages N-M]` / ` [lines X-Y]` per annotation format when the citation key is present

Citation-source mapping per row (rows not listed receive no citation — they have no Layer A source):

| Card row | Citation source key |
|---|---|
| Project name | `nom_source_citation` |
| Project slug | `nom_source_citation` (propagated — slug is derived from `nom`) |
| Vision | `idea_summary_source_citation` |
| Stack hints | `hints_techniques_source_citation` |
| Is-a-plugin | `type_source_citation` (propagated — Is-a-plugin is inferred from `type`) |
| Target audience | `pour_qui_source_citation` |
| Language detected | `langue_detectee_source_citation` |
| Budget / constraint | `budget_ou_contrainte_source_citation` |
| Visibility | `prive_ou_public_source_citation` |

**Rows explicitly NOT annotated**:

- `Target folder` — computed from `Bash pwd`, no Layer A source.
- `License` — defaults to MIT or configured in `config.txt`, no Layer A source.
- `Plan tier` — prompted at Step 0.4 or sourced from `config.txt`, no Layer A source.
- `Scope locks` — sourced from `config.txt`, no Layer A source.
- `Mixed media` — sourced from Step 0.3 disk `Glob`. `attaches_source_citation` is preserved by Step 0.2a but **not rendered** on this row (honest provenance — the row reflects disk reality, not the user's drop-zone typed description).
- `Gaps to fill` — synthesized by Phase 0 logic, no single-source attribution.

The origin tag `(from drop zone)` is preserved exactly as in v1.3.2; the citation suffix follows it with one space separator. When the origin is `(derived)` (e.g. Project slug derived from Project name, or Is-a-plugin inferred from `type`), the citation propagates from the source field — this is the honest reading, since the derived value depends on the cited source.

#### Step 0.5 `bootstrap_intent.md` template — extended

The v1.3.2 `## Fields` table and the v1.3.2 `## Conversational context from drop zone` table gain inline citation suffixes inside the `Value` column. No new section, no new column, no new frontmatter key.

```markdown
## Fields

| Field | Value | Source |
|---|---|---|
| Project name | <value><citation> | config.txt / drop_zone_intent.md / user edit |
| Slug | <value><citation> | config.txt / derived |
| Vision | <one-paragraph><citation> | config.txt / drop_zone_intent.md |
| License | <value> | config.txt / default |
| Is-a-plugin | <yes|no><citation> | config.txt / drop_zone_intent.md / user edit |
| Plan tier | <value> | config.txt / user edit |
| Stack hints | <list><citation> | config.txt / drop_zone_intent.md |
| Scope locks | <list> | config.txt / user edit |
| Mixed media | <file list> | folder scan |

...

## Conversational context from drop zone

(Rendered only when `drop_zone_intent.md` was the Phase 0 seed source.)

| Field | Value |
|---|---|
| Target audience (pour qui) | <value or "a trouver ensemble"><citation> |
| Language detected | <FR / EN / mixte><citation> |
| Budget or constraint | <value or "non mentionne"><citation> |
| Visibility (private / public) | <value or "non mentionnee"><citation> |

Source: `drop_zone_intent.md` written by `genesis-drop-zone` v<version> at <ISO timestamp>.
```

Same citation-source mapping as the Step 0.4 card. Legacy `config.txt` sessions render the `## Fields` table exactly as v1.3.2 (no citation suffixes anywhere, since no `drop_zone_intent.md` seeded the session).

#### Zero ripple elsewhere

v1.4.1 does not modify:

- **Step 0.1 detection** — same row in the detection table, same precedence rule.
- **Step 0.2 `config.txt` parser** — unchanged.
- **Step 0.2a parser mechanics** — same dict-based YAML read, same field mapping, same null-class handling. Only the set of preserved keys widens (citation keys are preserved alongside semantic + metadata keys) — no branching logic.
- **Step 0.3 mixed media scan** — unchanged.
- **Step 0.4 card structure** — same rows, same columns, same width, same origin tags. Only the per-row value rendering gains an optional inline suffix.
- **Step 0.5 write flow** — same file path, same atomic write pattern, same exit condition.
- **Consent gate** (Category C) — unchanged. Mode dispatch (detailed / semi-auto / auto) unchanged.
- **`genesis-drop-zone` skill** — zero code change. Layer A writes v1.4.0-shape files; Layer B v1.4.1 reads them.
- **Schema version** — stays at `1`. No `schema_version: 2` anywhere.

### Cross-layer pattern (master.md cross-skill-pattern #4)

v1.3.2 is the first cross-layer wire in the Genesis plugin. The pattern established here is the reference implementation for future Étape 1 → Phase 1 / Étape 2 → Phase 2 / Étape 3 → Phase 3 wires as Layer A grows:

1. Layer A captures user intent in a dedicated file at cwd root with origin-tagged naming (`drop_zone_intent.md`, later e.g. `etincelle_refinement.md`, `creation_brief.md`, `miroir_review.md`).
2. Layer B's corresponding phase detects the Layer A file, parses it, maps its fields to the Layer B schema, and archives the Layer-A-specific extras in a dedicated section of the Layer B bootstrap file.
3. Precedence rule always favours the Layer A file over legacy / engineer-written inputs; never silent merge.
4. R9 tier stays clean: Layer A field names in frontmatter are English snake_case; Layer A user-facing labels live only in `phase-X-*.md` runtime templates; Layer B reads the snake_case and re-labels for its own card.
5. Origin tags on Layer B's Phase card make the Layer A → Layer B provenance explicit to Victor.

This pattern is load-bearing for the v2 conversational surface. Future sessions that add an Étape 1 skill will follow the same shape.

**v1.4.1 discipline upgrade — Layer B may opt-in to render additive keys read-only.** v1.3.3 established *"Layer B parser naturally ignores unknown keys"*; v1.4.0 extended with *"additive frontmatter keys preserve zero-Layer-B-ripple at parser level"*. v1.4.1 refines further: Layer B may render additive keys as read-only surface enrichment, without bumping schema version and without growing the parser. "Zero ripple" is measured at two levels: (a) **parser-level** — unchanged across the v1.3.2 → v1.4.1 range (dict-based YAML, unknown keys ignored); (b) **contract-level** — forward-compat with old writers preserved (old Layer A writers + new Layer B reader = zero citations rendered since no citation keys exist; new Layer A writer + old Layer B reader = citation keys ignored, no crash). The additive happens at the *surface* layer — Step 0.4 card and Step 0.5 template gain conditional rendering branches — without touching the data contract. Fifth discipline data-point layering on the same principle: v1.3.2 wire + v1.3.3 body-vs-frontmatter asymmetry + v1.4.0 additive keys + v1.4.1 additive rendering + (future) contradictions[] surfacing at v1.5+ would follow the same discipline.

## Concentrated privilege declaration

Per master.md's concentrated-privilege map discipline (cross-skill-pattern #2): every Genesis skill has **at most one concentrated privilege per operation class** (refinement introduced in v1.4.0 — previously "at most one concentrated privilege per skill"; see § "v1.4.0 refinement to cross-skill-pattern #2" below).

**`genesis-drop-zone` across versions**:

| Version | Disk class | Network class |
|---|---|---|
| v1.3.0 | `none` | `none` |
| v1.3.1 | `none` | `none` |
| v1.3.2 | writes `drop_zone_intent.md` to cwd after consent, halt-on-existing, no `mkdir` | `none` |
| v1.3.3 | unchanged from v1.3.2 (runtime locale dispatch only) | `none` |
| **v1.4.0** | **unchanged from v1.3.2** (additive frontmatter keys only; same write, same halt, same path) | **subprocess → Anthropic Messages API for Citations extraction, pre-flight env check, silent graceful fallback, 1h cache TTL explicit** |

Precedent for v1.3.0 / v1.3.1: `journal-system` declared `none` in the map. The welcome + acknowledgement + bridge slice writes nothing, runs no subprocess, makes no network call. Claude reads user-attached files via its native multimodal context — that is a harness-level capability, not a skill privilege. v1.3.1 extended acknowledgement into a structured 9-field mirror via the same in-context multimodal path — no disk write, no subprocess, no network call, no Anthropic API invocation.

### Disk class mitigations (unchanged since v1.3.2)

v1.3.2 broke the `none` streak with the minimum viable concentrated privilege — **one file, one path, one operation**. Mitigations remain the canonical five:

- **Bilingual consent card** (§ "Consent card — template + flow") is the single gate. The user sees the absolute target path with an arrow marker before any write can proceed. Modifications route back through mirror re-render + consent re-print, never through silent field changes.
- **Halt-on-existing** (§ "Halt branch — file already exists") covers the only unexpected state — an existing `drop_zone_intent.md` at cwd. Halt + remediation, never overwrite, never timestamp-suffix fallback, never second consent for the destructive path.
- **Narrow path resolution** — cwd only. No `mkdir`, no subdir write, no absolute-path-anywhere write. The context guard already asserts cwd fresh; keeping the privilege tight to that cwd means the filesystem surface area stays 1 file.
- **Atomic write pattern** — temp file + rename, post-write size verification, failure surfaces bilingually without half-written remnants.
- **Match pepite-flagging's per-target consent floor** — this precedent was already set for Layer A privileges in the master.md map. v1.3.2 honours it on the first real Layer A write.

This declaration is the **precedent that all future Étape 1 / Étape 2 / Étape 3 Layer A privileges will be measured against**. Widening the privilege surface in a later ship (subdir writes, `mkdir`, multi-file writes) requires the same pattern — declare privilege for code that exists, never speculate, always carry mitigations one-for-one with the privilege.

### Network class mitigations (new in v1.4.0)

v1.4.0 adds the second privilege class — an external Anthropic API call via Python subprocess. The class is orthogonal to the disk class: different operation surface (network, not filesystem), different failure modes (network errors, rate limits, billing), different consent model (silent opt-in via `ANTHROPIC_API_KEY` presence, silent fallback on absence). The five mitigations ship one-for-one with the privilege:

- **Pre-flight env check at skill entry** — `ANTHROPIC_API_KEY` unset → skill commits to the v1.3.3 in-context extraction path before the welcome box prints. No subprocess launch, no network call, no privilege actually exercised. `api_extraction_available = false` for the rest of the session. See § "Citations API — signal + dispatch (v1.4.0) / Dispatch lifecycle".
- **Subprocess isolation** — the extractor runs as a separate Python process. It cannot mutate the session filesystem beyond its own stdout/stderr streams; the SKILL.md dispatch is the only place where the subprocess output is read, validated, and consumed. If the subprocess misbehaves (bad JSON, invalid schema), the output is discarded and fallback fires.
- **Explicit 1h cache TTL always** — the extractor hardcodes `cache_control: {type: "ephemeral", ttl: "1h"}` on the document block per R8 § Stage 2 mandate. The env override `GENESIS_DROP_ZONE_CACHE_TTL` accepts `5m` or `1h`; the SDK default (5-minute) is never reached by omission.
- **Token-budget logging to stderr** — every successful extraction logs `input_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens`, `output_tokens` as a single stderr line (with `GENESIS_DROP_ZONE_VERBOSE=1` enabling full per-phase tracing). Forensic only — invisible to the Victor-facing UX, visible to developers during integration testing and cost-trending.
- **Silent graceful fallback** — any fallback trigger (env unset, Python unresolvable, subprocess exit ≠ 0, stdout not valid JSON, schema check fails) commits to the v1.3.3 in-context extraction path. The mirror renders v1.3.3-identical output (no `[page N]` / `[lines X-Y]` annotations). No user-facing informational note prints. The privilege never escalates on failure — fallback inherits zero new privileges beyond v1.3.3.

### v1.4.0 refinement to cross-skill-pattern #2

Pre-v1.4.0 read: *"at most one concentrated privilege per skill"*. The v1.3.2 → v1.4.0 trajectory revealed an edge the original formulation did not handle: a single skill can legitimately need **operations from different classes** (disk write AND network call), each with its own independent consent model and mitigations.

Refinement: *"at most one concentrated privilege per operation class, per skill"*. A class is a coarse category of privilege operations: `disk` (any write outside the skill's own scope), `network` (any external HTTP/API call), `subprocess` (any fork/exec outside the harness), `user-input` (any interactive prompt that changes external state on response), etc.

Multi-class privilege declarations are acceptable when each class:

1. Ships with its own consent model (explicit like v1.3.2's bilingual card, or implicit like v1.4.0's env presence + silent fallback).
2. Carries its own five mitigations, one-for-one with the privilege operation.
3. Is independently disableable (the user can opt out of one class without losing the other — v1.4.0 users without `ANTHROPIC_API_KEY` still get v1.3.2 disk writes intact).
4. Has its own failure mode that never escalates privilege on the other class.

The v1.3.3 / v1.4.0 `## Concentrated privilege` tracking in SKILL.md now renders as a per-class table rather than a single paragraph. master.md's cross-skill-pattern #2 map carries the updated formulation.

This declaration is the **precedent that any future multi-class privilege in Genesis will be measured against**. A hypothetical Étape 2 skill that needs both a disk write (save a refined brief) and a network call (invoke an external code-generator API) would declare both classes explicitly with their own gates and mitigations, not collapse them into one. Anti-Frankenstein gate stays tight: a skill that accretes a third class should trigger a hard review — at that point the skill probably needs splitting.

## 1:1 mirror map with SKILL.md

Cross-skill-pattern #1: when a skill is a faithful implementation of a canonical source document, `SKILL.md` mirrors the source structurally — same sections, same ordering. Drift = merge-blocker.

| This spec section | `genesis-drop-zone/SKILL.md` section | Mirror status |
|---|---|---|
| Position in the v2 architecture | `## Purpose` (condensed, covers v1.3.0 welcome + v1.3.1 mirror + v1.3.2 write) | Mirrored |
| Scope — v1.3.0 vertical slice | `## Scope / In scope (v1.3.0)` sub-block (historical, retained for version traceability) | Mirrored |
| Scope — v1.3.1 extraction | `## Scope / In scope (v1.3.1)` sub-block (in/out bullets, copied verbatim) | Mirrored |
| Scope — v1.3.2 write + Layer B handoff | `## Scope / In scope (v1.3.2)` sub-block (in/out bullets, copied verbatim) | Mirrored |
| Scope — v1.3.3 runtime locale rendering | `## Scope / In scope (v1.3.3)` sub-block (in/out bullets, copied verbatim) | Mirrored |
| Scope — v1.4.0 Citations API extraction | `## Scope / In scope (v1.4.0)` sub-block (in/out bullets, copied verbatim) | Mirrored |
| Scope — v1.4.1 Layer B citation surfacing | — (no `genesis-drop-zone/SKILL.md` counterpart — v1.4.1 touches only `genesis-protocol`) | **Spec-only** for this map; mirrored downstream per Layer B addendum below |
| Runtime locale — signal + dispatch (v1.3.3) | `## Locale dispatch (v1.3.3)` (two-variable table + render-target map) | Mirrored |
| Citations API — signal + dispatch (v1.4.0) | `## Citations API dispatch (v1.4.0)` (three-gate lifecycle + extractor contract + fallback triggers + env vars) | Mirrored |
| Trigger evaluation gate | `## Trigger` + `## Context guard` (two sections in SKILL.md for dispatch clarity) | Mirrored |
| Welcome body | `## Phase 0 — welcome` with pointer to `phase-0-welcome.md` (no duplicated template text in SKILL.md) | Mirrored (pointer) |
| Mirror screen — template & reveal | `## Phase 0 — mirror` (pattern description only; full template lives in `phase-0-welcome.md`) | Mirrored (pattern) |
| Extraction schema — 9 fields | `## Phase 0 — mirror` subsection `### Schema` (9-field table referenced from dispatch) | Mirrored (table) |
| Bridge message — bilingual (v1.3.1 update) | `## Phase 0 — bridge` with v1.3.2 supersession note | Mirrored (with supersession) |
| Consent card — template + flow (v1.3.2) | `## Phase 0 — consent card` with pointer to `phase-0-welcome.md § Consent card (v1.3.2)` | Mirrored (pointer) |
| `drop_zone_intent.md` — schema + body format (v1.3.2) | `## Phase 0 — drop_zone_intent.md file` (schema table + file metadata + example pointer) | Mirrored (table + pointer) |
| Write flow — consent → write → bridge (v1.3.2) | `## Phase 0 — write flow` (sequence + atomic write mechanics) | Mirrored |
| Halt branch — file already exists (v1.3.2) | `## Phase 0 — halt branch` with pointer to `phase-0-welcome.md § Halt message (v1.3.2)` | Mirrored (pointer) |
| Bridge messages — accept and decline (v1.3.2) | `## Phase 0 — bridges (v1.3.2)` with pointer to `phase-0-welcome.md § Accept/Decline bridges (v1.3.2)` | Mirrored (pointer) |
| Layer B integration — genesis-protocol Phase 0 (v1.3.2) | `## Phase 0 — handoff to genesis-protocol` (precedence rule + field mapping + forward note) | Mirrored (precedence + mapping) |
| Concentrated privilege declaration | `## Concentrated privilege` (per-class table v1.3.0-v1.4.0 + disk-class mitigations + network-class mitigations + cross-skill-pattern #2 refinement) | Mirrored |
| Deferred to v1.4.2+ | `## Deferred scope` (verbatim bullet list, updated — pending SKILL.md rename sweep in a future Layer A touch since v1.4.1 ships zero Layer A changes) | Mirrored (heading-label drift until next SKILL.md touch) |
| Problem statement | — | **Spec-only** (design rationale) |
| UX canon backing | — | **Spec-only** (design rationale) |
| R9 language policy applied | — | **Spec-only** (tier map across artefacts, dev-internal) |
| References / R8 citations | — | **Spec-only** (dev-internal provenance) |
| Verification scenarios | — | **Spec-only** (ship gate, dev-internal) |
| Relation to the vision doc | — | **Spec-only** (cross-doc navigation) |
| Rationale for v1.3.1 route | — | **Spec-only** (design decision log) |
| Rationale for v1.3.2 route | — | **Spec-only** (design decision log) |
| Rationale for v1.3.3 route | — | **Spec-only** (design decision log) |
| Rationale for v1.4.0 route | — | **Spec-only** (design decision log) |
| Rationale for v1.4.1 route | — | **Spec-only** (design decision log) |

Rule of thumb for the drift-check gate: **every row tagged `Mirrored` must show section-for-section correspondence; every row tagged `Spec-only` is an expected asymmetry** and is not flagged during review. SKILL.md is the dispatch surface; spec is the design record.

### Cross-skill mirror addendum for v1.3.2 Layer B touches

v1.3.2 is the first ship where this spec documents cross-skill changes (additions to `skills/genesis-protocol/*`). Those changes do not add new `## Mirrored` rows to the table above — they are a separate mirror family anchored in the Layer B skill files. The traceability contract is:

| This spec section | `genesis-protocol/phase-0-seed-loading.md` section | Mirror status |
|---|---|---|
| Layer B integration — Precedence rule (Step 0.1) | `### Step 0.1 — Inspect the input folder` — new row `drop_zone_intent.md present` + precedence rule paragraph | Mirrored |
| Layer B integration — Field mapping (Step 0.2a) | `### Step 0.2a — Parse drop_zone_intent.md` (new sub-step) | Mirrored |
| Layer B integration — Step 0.4 intent card (extended) | `### Step 0.4 — Surface the parsed intent card` (extended template with origin tags + `Additional context from drop zone` block) | Mirrored |
| Layer B integration — Step 0.5 bootstrap_intent.md template (extended) | `### Step 0.5 — Persist the intent as bootstrap_intent.md` (template extended with `## Conversational context from drop zone` section) | Mirrored |
| Layer B integration — SKILL.md seed description | `skills/genesis-protocol/SKILL.md` Phase 0 paragraph | Mirrored |
| Layer B integration — verification scenario | `skills/genesis-protocol/verification.md` new scenario block | Mirrored |
| Citation rendering (v1.4.1) — Step 0.2a citation preservation | `### Step 0.2a — Parse drop_zone_intent.md` (new "Citation preservation" subsection — lists which `_source_citation` keys are carried forward) | Mirrored |
| Citation rendering (v1.4.1) — Step 0.4 card extended template | `### Step 0.4 — Surface the parsed intent card` (extended again with `<citation>` suffix placeholder + citation-source mapping table) | Mirrored |
| Citation rendering (v1.4.1) — Step 0.5 Value-column suffix | `### Step 0.5 — Persist the intent as bootstrap_intent.md` (Value columns in `## Fields` and `## Conversational context from drop zone` tables gain inline `<citation>` placeholder) | Mirrored |
| Citation rendering (v1.4.1) — verification scenario | `skills/genesis-protocol/verification.md` new v1.4.1 scenario block | Mirrored |

Drift between this spec and any row in the Layer B mirror family is a merge-blocker at the same discipline level as the primary (genesis-drop-zone) mirror.

## R9 language policy applied

Three tiers per Layer 0 R9:

| Artefact | Tier | Language |
|---|---|---|
| `v2_etape_0_drop_zone.md` (this file) | Dev/tooling internal doc | English only |
| `skills/genesis-drop-zone/SKILL.md` | Dev/tooling skill dispatch | English only |
| `skills/genesis-drop-zone/phase-0-welcome.md` — **comments + section headings** | Dev/tooling | English only |
| `skills/genesis-drop-zone/phase-0-welcome.md` — **runtime string templates (welcome box, mirror template + 9-field labels, consent card (v1.3.2), halt message (v1.3.2), accept + decline bridges (v1.3.2), zero-content re-prompt (EN pair new in v1.3.3))** | User-facing runtime | Bilingual FR + EN coauthored day 1; **v1.3.3 runtime-locale-dispatched** via `welcome_locale` / `content_locale` — only one variant rendered at a time per § "Runtime locale — signal + dispatch (v1.3.3)" |
| Trigger phrases in `SKILL.md` `description:` frontmatter | User-facing invocation surface | Bilingual FR + EN day 1 — covers both the one-line `description:` text AND the embedded trigger phrase list; written as one frontmatter block, not two |
| `drop_zone_intent.md` written at cwd (v1.3.2) — **frontmatter keys** | Dev-layer data (file consumed by Layer B parser) | English only (snake_case) |
| `drop_zone_intent.md` written at cwd (v1.3.2) — **frontmatter values** (extracted user strings + null-class tokens) | Dev-layer data contract (parsed by Layer B Step 0.2a) | FR canonical null-class tokens (`"a trouver ensemble"`, `"non mentionne"`, `"non mentionnee"`, `"a affiner — X ou Y"`) regardless of `content_locale` — **v1.3.3 deliberately preserves FR canonical here** so Layer B's parser stays unchanged. Extracted user strings (e.g. `idea_summary`) follow the user's language naturally. |
| `drop_zone_intent.md` written at cwd (v1.3.2) — **body prose intro + mirror echo** | User-facing runtime (archive fidelity of what Victor saw) | **v1.3.3: locale-detected** via `content_locale` — FR body when content is FR, EN body when content is EN. v1.3.2 hardcoded FR. |
| Phase 0 Step 0.4 intent card origin tags (v1.3.2) | User-facing runtime (visible to Victor in detailed/semi-auto modes) | English short tags (`(from drop zone)`, `(derived)`, `(default)`, `(inferred)`); deliberately non-jargon (not `(Layer A)`) but English-only for card coherence with existing Phase 0 card text |
| Phase 0 Step 0.5 `## Conversational context from drop zone` section (v1.3.2) | User-visible archive | English headings / labels (matches surrounding Layer B bootstrap_intent.md template which is English); values preserved verbatim in their source language (typically FR for v1.3.2) |

The mixed-tier nature of `phase-0-welcome.md` is intentional: the file's structure and comments are dev-facing (so a maintainer reads the file in English), but the string templates it ships are what Victor sees and must be bilingual. This is the standard pattern for runtime-text-bearing skill bodies — a precedent to establish here, to reuse when LAYER A grows further (Étapes 1, 2, 3).

The v1.3.2 `drop_zone_intent.md` file introduces a **new tier blending**: the frontmatter is a parseable contract (dev-layer English keys + FR/EN runtime values), while the body is archive fidelity (prose intro + ASCII-pure mirror echo). Keys stay English so Layer B parsing is language-neutral; values honour the locale at capture so the file reads honestly to Victor. This is a precedent for any future file that is both dev-parseable and user-inspectable — keys stay dev-layer English, values follow the user's locale.

**v1.3.3 refinement to the tier blending**: the body is now locale-detected (body = FR when content is FR, EN when content is EN) while the frontmatter **null-class tokens** stay FR canonical regardless of `content_locale`. This split (body = locale-detected human echo; frontmatter = FR canonical data contract) is intentional: the frontmatter contract is parsed by Layer B, and a stable FR canonical token set means Layer B does not grow a bilingual parsing branch. Bilingual frontmatter null-class tokens are a v1.4+ consideration if a concrete pain point emerges. Extracted user strings in the frontmatter (e.g. `idea_summary`) naturally follow the user's language — they echo what the user wrote. Only the three synthetic null-class strings are normatively FR canonical.

**v1.4.0 additions to the tier table** (additive to the v1.3.3 rows above):

| Artefact | Tier | Language |
|---|---|---|
| `skills/genesis-drop-zone/scripts/extract_with_citations.py` — code, comments, docstrings, log lines | Dev-layer Python runtime | English only (snake_case, standard R9 tier-1) |
| Extraction prompt string inside `extract_with_citations.py` (the system / user text sent to the API) | Dev-layer prompt — not shown to Victor | English only. The prompt instructs the API to respect the null-class FR canonical tokens in its output strings, but the prompt *text* is English. |
| Subprocess stderr logs (token usage lines, error diagnostics) | Forensic / developer-facing | English only (never rendered to Victor). |
| Citation annotations in the mirror (`[page N]`, `[lines X-Y]`) | User-facing runtime | Language-neutral ASCII — brackets + digits + dash. No FR/EN branching. |
| `drop_zone_intent.md` frontmatter `<field>_source_citation` nested keys | Dev-layer data contract | English keys (`type`, `document_index`, `start`, `end`, `cited_text_preview`); `cited_text_preview` value echoes source text verbatim (any language). |

The Python extractor stays entirely English because it is developer-facing code — its strings never reach Victor's terminal directly. Citation annotations in the mirror are language-neutral by design (brackets + digits are universal) so `content_locale` dispatch does not branch them.

**v1.4.1 — no new R9 rows.** Layer B's Phase 0 card and `bootstrap_intent.md` template are already English-only per `skills/genesis-protocol/phase-0-seed-loading.md` (dev-facing runbook — tier 1) and `memory/project/bootstrap_intent.md` (dev-parseable archive with English labels, values preserved verbatim in source language — tier 2 blending from v1.3.2). The v1.4.1 inline citation suffix reuses the language-neutral ASCII annotation format from the v1.4.0 mirror row above; rendering is identical across FR / EN / mixte. Zero new locale branches, zero new bilingual pairs.

## Deferred to v1.4.2+

Ordered by rough priority, non-binding, revisit at each session boundary. Items closed across the v1.3.x / v1.4.x cycle so far: the `bootstrap_intent.md` file write and Layer B handoff (both closed in v1.3.2); **runtime locale detection** (closed in v1.3.3 — welcome + mirror + consent card + halt + bridges + body prose + body mirror echo all dispatch on `welcome_locale` / `content_locale`); **Path A Citations API extraction** (closed in v1.4.0 — second privilege class with graceful fallback, `source_citation` frontmatter extension, mirror annotations); **Layer B citation surfacing** (closed in v1.4.1 — Step 0.4 card + Step 0.5 template render `[page N]` / `[lines X-Y]` suffix inline on mapped + extras rows, zero parser change, zero schema bump, zero Layer A ripple). This list reflects what remains.

1. **`cited_text_preview` inline surfacing** — the citation dict carries up to 80 chars of quoted source text; v1.4.1 renders only the position annotation. Surfacing the preview inline (e.g. on hover or via `cited_text:` tooltip syntax) is a v1.4.2+ UX option. Preview is already archived verbatim in `drop_zone_intent.md` for any reader who wants the full quote.
2. **Hyperlinks into source files on the Phase 0 card** — e.g. `[page 3](./cahier_des_charges.pdf#page=3)`. Harness-dependent rendering (ASCII annotation works everywhere; hyperlinks work in some IDEs, not in bash terminals). Deferred until a Genesis install path runs inside a hyperlink-rendering surface by default.
3. **Files API (beta) adoption** — v1.4.0 uses inline base64 document blocks. The Anthropic Files API beta (`anthropic-beta: files-api-2025-04-14`) enables dedup across sessions and larger file limits. Useful for users who drop the same brief multiple times or exceed the 32 MB × 600-page inline limit. Ship when a concrete user hits the limit or the cost trend justifies the complexity.
4. **Programmatic handoff** — auto-invoke `genesis-protocol` without the user typing `/genesis-protocol` after the accept bridge. Requires a harness-level skill-to-skill invocation mechanism that is not 2026-04 Claude Code ready. Human-in-the-loop via the accept bridge's instruction is the v1.3.2 pattern; the programmatic path can ship when the harness supports it without changing the bridge text semantics.
5. `GH_BROWSER` profile routing wire-up — read Chrome profile map from Layer 0, export `GH_BROWSER` before any `gh` invocation in the downstream LAYER B.
6. UX toolkit integration — `@clack/prompts` structural skeleton, Charm Gum for select prompts, cli-spinners for the `◐` animation. With R9 closed (v1.3.3) and citations shipped + surfaced (v1.4.0 + v1.4.1), the surface is complete — polish can land without re-fragmenting it.
7. Completion chime (cross-platform) — macOS `afplay`, Windows `[console]::beep`, Linux `paplay`. Honours the "rising interval" convention per vision doc § "The sound of Genesis".
8. Error handling refinements — permission-denied / disk-full / symlink-pointing-to-directory edge cases currently let `OSError` bubble up naturally. v1.4.2+ adds halt + remediation if any of these produces real user pain in v1.3.2–1.4.1 usage. v1.3.2's floor is "write succeeds or harness shows the stack".
9. **Contradictions surfacing** — when multiple documents dropped, cross-reference conflicts could populate a `contradictions[]` array (per R8 Stage 2 recommendation). v1.5+ if multi-document drops become common.
10. **Chain-of-Verification (CoVe) second pass** — Haiku 4.5 verification of Citations output. R8 ranks Citations above CoVe and recommends skipping unless evals show failure. Skip until evals demand.
11. **Bilingual Layer B null-class parsing** — if `drop_zone_intent.md` frontmatter null-class tokens ever carry EN canonical variants alongside FR canonical, Layer B's Step 0.2a parser grows a bilingual branch. v1.5+ target.
12. **Three-locale-or-more expansion** — if Genesis ships beyond FR + EN (e.g. ES, DE), `welcome_locale` and `content_locale` become n-way enums. Minor, deferred until a real non-FR/EN user emerges.
13. **Structured Outputs (Path B) alternative** — v2 architectural pivot question. Would require dropping Citations (API incompatibility). Not considered until Path A evals expose a concrete shortfall.

## References (R8 inline citations consolidated)

All citations above resolve to entries in `.claude/docs/superpowers/research/sota/`:

- `v2_promptor_fusion_landscape_2026-04-17.md` — primary source. Sections: Stage 1 (drop zone UX), Stage 2 (document extraction), Stage 3 (conversational briefing). Expires 2026-04-24. Used for intent-first pattern, dual-path rule, privacy language, token-streamed ack, accept-anything norm, failure-mode table.
- `zero-friction-bootstrap-ux_2026-04-16.md` — auth revolution patterns informing the LAYER B phase-table deltas referenced in § "Position".
- `claude-in-ide-tools_2026-04-15.md` — VS Code / Claude Code harness conventions influencing the trigger gate (context-guard design).

External sources cited (resolved inside the R8 entry above):

- NxCode AI app builder comparison 2025-2026 — unified intent box norm.
- Filestack "File upload UI for non-technical users" — dual-path canonical rule.
- IBM Docling 2026 — unified representation norm, accept-anything bar.
- MIT Technology Review 2026-04-15 "Building trust in the AI era with privacy-led UX" — relationship-language privacy framing.
- Ably "Token streaming for AI UX" 2026 — SSE token-streaming pattern for loading state transformation.
- Anthropic Claude API docs — Files API (beta header `files-api-2025-04-14`), PDF support (32 MB, 600 pages/req).
- Anthropic Messages API docs — Citations (`citations: {enabled: true}` per document block, `cited_text` not billed, streams via `citations_delta`), Prompt Caching (explicit `cache_control: {type: "ephemeral", ttl: "1h"}` required since the March 2026 default-TTL tightening).

### New R8 stack entry required for v1.4.0 ship

`anthropic-python` SDK version pin — `stack/anthropic-python_2026-04-18.md` (TTL 1 day per stack convention). The v1.4.0 extractor takes a dependency on the `anthropic` Python SDK's Messages API + cache_control + Citations surface. Pinning the version at ship time (and refreshing the stack entry at each session open per R8) guards against upstream breaking changes. Documented as a ship-blocker check in the plan.

## Verification scenarios

The scenarios below cover **six ship-gate blocks** (v1.3.0 / v1.3.1 / v1.3.2 / v1.3.3 / v1.4.0 / v1.4.1). Range map:

- Scenarios **#1-#6** — v1.3.0 welcome / context-guard / trigger-evaluation regression set (preserved with expected-outcome updates as later versions supersede specific surfaces).
- Scenarios **#7-#12** — v1.3.1 additions targeting the mirror screen, extraction schema, zero-content branch, truncation, R9 audit.
- Scenarios **#13-#19** — v1.3.2 additions targeting the write flow, halt-on-existing, modification loop, Layer B parser cross-layer wire, precedence rule.
- Scenarios **#20-#27** — v1.3.3 additions targeting runtime locale divergence, EN body write, R9 audit of the new EN re-prompt, Layer B zero-ripple on locale changes.
- Scenarios **#28-#39** — v1.4.0 additions targeting API-path happy cases, four fallback triggers, fallback byte-identity, R9 audit of the Python extractor, Layer B parser zero-ripple on the extended frontmatter, annotation-truncation edge case.
- Scenarios **#40-#44** — v1.4.1 additions targeting Layer B card + bootstrap_intent.md citation rendering happy path, absence-of-citations render parity, legacy `config.txt` render parity, partial-citation per-row render, Mixed media unadorned honesty.

See § "Ship gates" at the end of this Verification section for the per-version mandatory / strongly-recommended / non-blocking split and the runtime-replay note that rolls forward from v1.3.1.

### v1.3.0 regression set (preserved — expected outcomes updated for v1.3.1 mirror + bridge)

| # | Scenario | Expected |
|---|---|---|
| 1 | Fresh empty dir, Claude Code opens, user types `/genesis-drop-zone`. | Welcome box prints (FR), skill awaits, **mirror token-streamed on response** (v1.3.1 replaces v1.3.0's bullet ack), bridge bilingual with v1.3.1 content, skill exits clean. |
| 2 | Fresh empty dir, user types "je veux créer un projet pour gérer mes dépenses". | Claude auto-invokes the skill via intent match; same as #1. |
| 3 | Open Claude Code inside `C:/Dev/Claude_cowork/project-genesis/` (active repo), type `/genesis-drop-zone`. | Context guard fires; bilingual redirect prints; skill does not welcome. |
| 4 | Fresh empty dir, user types trigger + attaches `@tests/fixtures/sample-brief.pdf` (fixture lives in the worktree, honours the "no deliverables in C:\tmp" auto-memory rule). | Mirror names the PDF in the `Depose` row and extracts schema fields from the PDF content (Idee + Pour qui + Type derived from content). |
| 5 | Fresh empty dir, user types "I want to create a project to track my expenses". | **v1.3.3 supersession**: Intent matches (EN trigger) → `welcome_locale = EN` → EN welcome box prints; content yields `langue_detectee = EN` → `content_locale = EN` → EN mirror + EN consent card + EN halt / bridges / body. (Historical v1.3.1 expectation: welcome FR + mirror FR + `Langue = EN` row + bilingual bridge.) |
| 6 | R9 audit — grep SKILL.md + this spec for French strings outside trigger list. | Zero matches. Grep `phase-0-welcome.md` for both FR and EN mirror markers. Both present. |

### v1.3.1 new scenarios

| # | Scenario | Expected |
|---|---|---|
| 7 | Fresh empty dir + text-only drop ("j'ai une idee de boulangerie"). | Mirror renders 9 rows: `Idee` filled verbatim, `Pour qui`/`Type`/`Nom` = `a trouver ensemble`, `Depose` = `texte seul`, `Langue` = `FR`, `Budget`/`Visibilite`/`Tech` = `non mentionne(e)`. Bridge v1.3.1 text prints after. |
| 8 | Fresh empty dir + text + PDF + photo (multimodal rich case). | Mirror renders 9 rows with `Depose` listing all 3 items (or truncated at 3 with `+ N autres` if more). `Idee`/`Pour qui`/`Type` extracted from combined content. |
| 9 | Fresh empty dir + trigger phrase only, zero content attached or written. | No `◐` line, no mirror, no `✓` closure. Re-prompt printed in `welcome_locale` — v1.3.3 supersession: FR re-prompt `Je t'écoute — dépose ou écris ce que tu veux me partager.` if `welcome_locale = FR` (slash / FR intent); EN re-prompt `I'm listening — drop or write whatever you want to share.` if `welcome_locale = EN` (EN intent). When user responds, mirror flow fires normally in `content_locale`. (Historical v1.3.1 expectation: FR re-prompt only.) |
| 10 | Fresh empty dir + EN content ("I want to build a small task tracker for my team"). | **v1.3.3 supersession**: welcome box in `welcome_locale` (EN if auto-triggered by EN intent; FR if slash), mirror rendered in **EN** (`content_locale = EN` from `langue_detectee = EN`), `Language` row reads `EN`, consent card / halt / bridges / body echo all render EN variants. (Historical v1.3.1 expectation: Mirror rendered in FR with `Langue = EN` row + bilingual bridge covering the gap.) |
| 11 | Very long idea text (> 60 characters — e.g. a 200-character paragraph) dropped. | `Idee` row truncated at exactly 57 chars + `...` per the truncation rule in § "Mirror screen / Truncation rules". Other rows render normally. Full content retained in Claude's context (not disposed — kept for v1.3.2+ handoff). |
| 12 | R9 audit — grep FR+EN mirror templates in `phase-0-welcome.md` after v1.3.1 additions; grep accents inside FR table block vs FR surrounding prose. | Both FR and EN mirror templates present. Zero accents inside FR table rows (ASCII-pure discipline). Accents present in `◐`/`✓` prose and in bridge (plain-prose, accent-stable). |

### v1.3.1 regression set for v1.3.2

All v1.3.0 regression guarantees preserved. Mirror template, extraction schema, zero-content branch, context guard, R9 accent discipline inside the mirror table block — all covered by scenarios #7-#12 above. v1.3.2 does not modify any of these surfaces; the only runtime change on a v1.3.1 surface is the v1.3.1 bridge being superseded by v1.3.2's two bridges (documented inline in § "Bridge message — bilingual (v1.3.1 update) — v1.3.2 supersession note").

### v1.3.2 new scenarios

| # | Scenario | Expected |
|---|---|---|
| 13 | Fresh empty dir, user drops content, mirror renders, consent card prints, user says `oui`. | `drop_zone_intent.md` written to cwd. File content validates: YAML frontmatter with 9 semantic keys + 4 metadata keys (`schema_version: 1`, `created_at` in ISO-8601 UTC, `skill: genesis-drop-zone`, `skill_version: 1.3.3`). Body contains FR prose intro + FR mirror echo inside code fence (for FR content; EN body for EN content per v1.3.3). UTF-8 no BOM. LF line endings. Accept bridge prints after write. Skill exits clean. |
| 14 | Same setup as #13 but user says `non`. | `drop_zone_intent.md` **absent** from cwd. No write performed. Decline bridge prints in the detected `content_locale` (v1.3.3). Skill exits clean. |
| 15 | Fresh dir already containing a `drop_zone_intent.md` (context guard passes — the file is neither `CLAUDE.md` nor `memory/`, git commit count < 3). User drops content. | Mirror renders token-streamed (in detected `content_locale`). Pre-write existence check at step 6 of the write flow detects the file. Halt message prints in `content_locale` with absolute path and remediation text. **Consent card does not print.** No overwrite. Skill exits clean. |
| 16 | Drop + mirror + consent card printed. User replies `"non c'est pour un restaurant pas une boulangerie"` (modification, not refusal). | Claude re-runs the 9-field extraction with the corrected `type`. Mirror re-renders with `Type` row updated. Consent card re-prints with the same absolute path. `content_locale` re-evaluated on each extraction — if the correction shifts `langue_detectee`, subsequent surfaces switch locale. Loop continues until affirmative or negative. |
| 17 | R9 audit of a post-write `drop_zone_intent.md`. | Frontmatter keys all snake_case English. Null-class string values are FR canonical accent-free ASCII (`a trouver ensemble`, `non mentionne`, `non mentionnee`) **regardless of body locale** (v1.3.3 asymmetry). Body prose intro in `content_locale` with accents allowed (UTF-8 stable). Mirror echo inside code fence is ASCII-pure (matches the v1.3.0/v1.3.1 accent discipline for table content). |
| 18 | Fresh dir already containing a valid v1.3.2-format `drop_zone_intent.md` (carried over from a prior drop-zone session). User invokes `/genesis-protocol`. | Step 0.1 detects `drop_zone_intent.md` and logs `Primary seed: drop_zone_intent.md`. Step 0.2a parses the YAML frontmatter and maps 9 Layer A fields per the § "Field mapping (Step 0.2a)" table. Step 0.4 card renders with origin tags `(from drop zone)` on Vision / Project name / Is-a-plugin / Stack hints. The `Additional context from drop zone` block renders with `pour_qui`, `langue_detectee`, `budget_ou_contrainte`, `prive_ou_public`. User confirms `yes` → Step 0.5 writes `memory/project/bootstrap_intent.md` containing populated fields + new `## Conversational context from drop zone` section + `## Raw config.txt` rendered as `n/a — seeded from drop_zone_intent.md`. Phase 1 proceeds normally. |
| 19 | Same setup as #18 but `config.txt` also present in cwd alongside `drop_zone_intent.md`. | Step 0.1 logs the precedence note: `config.txt found but drop_zone_intent.md takes precedence — ignoring config.txt`. Step 0.2a runs. Step 0.4 / 0.5 identical to #18. `## Raw config.txt` section in Step 0.5 output still reads `n/a — seeded from drop_zone_intent.md` (config.txt content never parsed, never archived in Phase 0 output). |

### v1.3.2 regression set for v1.3.3

All v1.3.0 + v1.3.1 regression guarantees preserved. The v1.3.2 Layer B parser surface (Step 0.1 detection, Step 0.2a parsing, Step 0.4 card, Step 0.5 archiving) is completely untouched by v1.3.3 — zero Layer B file changes. The v1.3.2 write flow, halt branch, consent card template schema, and bridge text are all preserved; v1.3.3 only changes which variant (FR or EN) is rendered at runtime per `welcome_locale` / `content_locale`. Scenarios #18 and #19 remain valid as regression probes against the Layer B parser, with the additional check that Layer B parser still reads FR canonical null-class tokens (which v1.3.3 preserves by contract).

### v1.3.3 new scenarios

| # | Scenario | Expected |
|---|---|---|
| 20 | Fresh empty dir, FR intent phrase `"je veux créer un projet"`, then EN content drop ("I want to build a small task tracker for my team"). | `welcome_locale = FR` → FR welcome box prints. Content extracted → `langue_detectee = EN` → `content_locale = EN`. Mirror renders in EN with EN 9-field labels. Consent card prints EN variant (not FR). Halt/accept/decline bridges all use EN variants at runtime. Divergence between welcome FR and mirror-onwards EN is expected and spec-documented. |
| 21 | Fresh empty dir, EN intent phrase `"I want to create a project"`, then FR content drop ("je veux une boulangerie artisanale"). | `welcome_locale = EN` → EN welcome box prints. Content extracted → `langue_detectee = FR` → `content_locale = FR`. Mirror renders in FR. Consent card in FR. Inverse divergence of #20; expected. |
| 22 | Fresh empty dir, FR intent, then mixed FR+EN content (e.g. a brief written in bilingual style). | `content_locale = FR` (tiebreaker on `langue_detectee = mixte`). Mirror + consent card + halt + bridges all render FR. |
| 23 | Fresh empty dir, slash invocation `/genesis-drop-zone`, no trigger phrase signal. | `welcome_locale = FR` (default on slash). Welcome FR. Then user drops EN content → `content_locale = EN` → mirror onwards in EN. Welcome FR, rest EN is the graceful-degradation path for EN-on-slash. |
| 24 | Fresh empty dir, any trigger, zero content in first response. | Zero-content re-prompt prints in `welcome_locale` (FR or EN variant depending on trigger source). When content eventually arrives, `content_locale` resolves at mirror time and subsequent surfaces switch. |
| 25 | Fresh empty dir, EN drop leading to successful write + accept. | `drop_zone_intent.md` written with frontmatter `langue_detectee: "EN"`, body prose intro in EN, mirror echo in EN (EN labels, EN null-class display strings `to be found together` / `not mentioned`). **Frontmatter null-class tokens are FR canonical** (`"a trouver ensemble"`, `"non mentionne"`) — v1.3.3 asymmetry preserved. Fixture to match: `tests/fixtures/drop_zone_intent_fixture_v1_3_3_en.md`. |
| 26 | R9 audit of v1.3.3 additions — grep `phase-0-welcome.md` for the newly-authored EN zero-content re-prompt `I'm listening — drop or write whatever you want to share.`. | Exact EN string present exactly once. FR companion `Je t'écoute — dépose ou écris ce que tu veux me partager.` still present exactly once. |
| 27 | Layer B regression — run Step 0.2a against the EN fixture from #25 (frontmatter has FR canonical null tokens alongside EN body). | Parser succeeds unchanged from v1.3.2 behaviour. Null-class detection matches on `"a trouver ensemble"`, `"non mentionne"`, `"non mentionnee"`, `"a affiner — ..."` exactly as before. Body content is cosmetic — not parsed by Layer B. Confirms v1.3.3 zero-Layer-B-ripple. |

### v1.3.3 regression set for v1.4.0

All v1.3.0 + v1.3.1 + v1.3.2 regression guarantees preserved. v1.4.0 does not touch any of the locale dispatch surfaces or the v1.3.2 write flow — the extraction *source* changes (API vs in-context) but the mirror template / consent card / halt / bridges / body render pipeline is untouched. Scenarios #20-#27 remain valid regression probes. The v1.3.3 fixture `drop_zone_intent_fixture_v1_3_3_en.md` stays byte-identical to what v1.4.0 writes on the fallback path (no API key, or API failure), verified directly by scenario #31 below.

### v1.4.0 new scenarios

| # | Scenario | Expected |
|---|---|---|
| 28 | Fresh empty dir, `ANTHROPIC_API_KEY` set, user drops a PDF brief. | Pre-flight at skill entry sets `api_extraction_available = true`. Python subprocess launches after the mirror trigger. Subprocess exits 0 with valid JSON on stdout. Mirror renders 9 rows with `[page N]` annotations on fields that received PDF-sourced citations (typical: `idea_summary`, `type`, `pour_qui`, maybe `budget_ou_contrainte`). Rows without citations render v1.3.3-identical (no annotation). Consent card prints in `content_locale`. On accept, `drop_zone_intent.md` is written with optional `<field>_source_citation` nested keys populated per § "Citation object shape". Accept bridge prints. |
| 29 | Fresh empty dir, `ANTHROPIC_API_KEY` unset, user drops a PDF brief. | Pre-flight at skill entry sets `api_extraction_available = false`. No subprocess launch. Skill runs v1.3.3 in-context extraction path exactly. Mirror renders 9 rows with NO annotations on any row (v1.3.3 parity). No user-facing note indicates the fallback fired. `drop_zone_intent.md` is written with NO `_source_citation` keys. Verified by `diff drop_zone_intent.md tests/fixtures/drop_zone_intent_fixture_v1_4_0_fallback.md` returning zero changes modulo `created_at` (ISO-8601 timestamp varies per run). |
| 30 | Fresh empty dir, `ANTHROPIC_API_KEY` set, user types inline text only (no attachment). | Pre-flight passes. Subprocess launches with empty `attachments` array and populated `typed_text`. API call uses a single `custom content` document block (typed text). Citations return `text_char_range` style. Mirror renders with `[lines X-Y]` annotations per field. Written `drop_zone_intent.md` carries `type: text_char_range` in `_source_citation` entries. |
| 31 | Fresh empty dir, `ANTHROPIC_API_KEY` set, user drops image only (e.g. `logo.png`) with no text and no PDF. | Pre-flight passes. Subprocess launches. API call contains an image block (no `document` block). Citations API returns no citations (images are not citeable sources). Mirror renders without `[page N]` / `[lines X-Y]` annotations — rows render v1.3.3-parity. Written `drop_zone_intent.md` has NO `_source_citation` keys for any field (key omission, not explicit null). |
| 32 | Fresh empty dir, `ANTHROPIC_API_KEY` set to a deliberately invalid value (`sk-ant-api03-invalidvalue`), user drops content. | Pre-flight passes (env check is presence-only, not validity). Subprocess launches, API returns 401. Extractor exits with code 4. SKILL.md dispatch routes to fallback path. Mirror renders v1.3.3-parity (no annotations). Written `drop_zone_intent.md` has no `_source_citation` keys. Harness stderr contains the extractor's diagnostic about 401. |
| 33 | Fresh empty dir, `ANTHROPIC_API_KEY` set, Python runtime's `anthropic` package deliberately not installed (simulated via renaming site-packages). | Pre-flight passes. Subprocess launches; `import anthropic` raises ImportError. Extractor catches, emits diagnostic to stderr (`"anthropic package not installed — run: pip install anthropic>=X.Y"`), exits code 3. SKILL.md dispatch routes to fallback. Mirror renders v1.3.3-parity. |
| 34 | Fresh empty dir, `ANTHROPIC_API_KEY` set, API deliberately returns HTTP 429 after the SDK's internal retry budget exhausts (simulate via overriding sleep multipliers or testing against a rate-limited key). | Extractor exits code 5. Fallback fires. v1.3.3-parity mirror. |
| 35 | Modification-loop across an API extraction — user drops content, mirror renders with citations, replies `"garde Type en boulangerie"`. | Subprocess re-invoked with the modification applied in the extraction prompt. 1h cache hits on the document block (cache_read_input_tokens > 0 in usage stats, verified via subprocess stderr). Re-rendered mirror shows updated `Type` row with annotation (`[page N]` if the source carries it). Consent card re-prints in `content_locale`. |
| 36 | R9 audit of the Python extractor — grep `skills/genesis-drop-zone/scripts/extract_with_citations.py` for French strings. | Zero non-ASCII French-specific strings in code / comments / docstrings / log lines. The extraction prompt contains the string `"a trouver ensemble"` (and the other three FR canonical null-class tokens) as LITERAL values to instruct the API output — these are dev-layer prompt content, not French prose. Allowed per R9 tier-1 (dev layer can quote data-layer strings). |
| 37 | Schema round-trip — take a fixture with `_source_citation` entries (v1.4.0 API-path write), run Layer B Step 0.2a against it. | Parser reads the 9 semantic fields and 4 metadata fields. Unknown `<field>_source_citation` keys are silently ignored (dict-based YAML parsing, behaviour unchanged). Step 0.4 intent card renders identically to v1.3.3. Step 0.5 `bootstrap_intent.md` output identical to v1.3.3 output for the same fixture modulo the `_source_citation` keys (which Layer B never reads). Zero Layer B ripple confirmed. |
| 38 | Fallback-path byte-identity — compare a v1.4.0 fallback-written `drop_zone_intent.md` to the canonical regression fixture `tests/fixtures/drop_zone_intent_fixture_v1_4_0_fallback.md` (which is itself byte-identical to `drop_zone_intent_fixture_v1_3_3_en.md` modulo `skill_version`). | `diff` reports zero differences modulo `created_at` timestamp only (ISO-8601 varies per run). `skill_version` matches (both `1.4.0`). Null-class tokens identical (FR canonical). Body content identical. No `_source_citation` keys in either. A second auxiliary diff `diff tests/fixtures/drop_zone_intent_fixture_v1_4_0_fallback.md tests/fixtures/drop_zone_intent_fixture_v1_3_3_en.md` reports the single expected delta — `skill_version` line only — documenting that the v1.4.0-labelled delta is the skill_version stamp itself, nothing else. |
| 39 | Annotated row truncation interaction — synthetic case where value + annotation exceeds 60 chars. | Value truncates at 57 chars + `...` per v1.3.1 rule. Annotation `[page N]` appended after the ellipsis. Example: `Idee          boulangerie artisanale pour livraison matin tre... [page 1]`. Total row length may exceed 60 but stays within 80-col terminal. This is the single documented exception to the 60-char rule per § "Citations API — signal + dispatch (v1.4.0) / Truncation rule interaction". |

### v1.4.0 regression set for v1.4.1

All v1.3.0 + v1.3.1 + v1.3.2 + v1.3.3 + v1.4.0 regression guarantees preserved. v1.4.1 does not modify any Layer A surface — `genesis-drop-zone/*` files are byte-identical across the boundary. Scenarios #28-#39 remain valid regression probes. The v1.4.0 fixtures `drop_zone_intent_fixture_v1_4_0_fr_with_citations.md` / `_en_with_citations.md` / `_fallback.md` stay unchanged. Layer A writes are untouched; v1.4.1 reads what v1.4.0 wrote.

### v1.4.1 new scenarios

| # | Scenario | Expected |
|---|---|---|
| 40 | Fresh empty dir, seed via `tests/fixtures/drop_zone_intent_fixture_v1_4_0_fr_with_citations.md` (has 4 `_source_citation` entries). Run `/genesis-protocol`. | Step 0.1 detects the file as `Primary seed: drop_zone_intent.md`. Step 0.2a parses frontmatter including `idea_summary_source_citation`, `pour_qui_source_citation`, `type_source_citation`, `hints_techniques_source_citation`. Step 0.4 card renders 4 mapped rows + 4 extras rows with inline suffixes. Concretely: `Project name : a trouver ensemble (from drop zone)` (no suffix — Project name's source `nom` has no citation in this fixture since `nom` is null-class), `Vision : boulangerie artisanale pour livraison matin (from drop zone) [page 1]`, `Stack hints : React ou Next.js (from drop zone) [page 3]`, `Is-a-plugin : no (inferred) [page 2]` (propagated from `type_source_citation`). `Additional context from drop zone` block shows `Target audience : habitants du quartier ... [page 1]`. Step 0.5 `bootstrap_intent.md` written with same suffixes inline in Value columns. |
| 41 | Fresh empty dir, seed via `tests/fixtures/drop_zone_intent_fixture_v1_4_0_fallback.md` (no `_source_citation` entries anywhere). Run `/genesis-protocol`. | Step 0.1 detection + Step 0.2a parse identical to scenario #18. Step 0.4 card renders with ZERO citation suffixes on any row — zero brackets, zero placeholders, identical to v1.3.2 rendering for the same fixture. Step 0.5 template writes `## Fields` table with no citation suffixes, `## Conversational context from drop zone` table with no citation suffixes. Anti-Frankenstein null-visible discipline: absence of citation is absence of suffix, not `[unknown]`. |
| 42 | Fresh empty dir, seed via legacy `config.txt` (no `drop_zone_intent.md` anywhere). Run `/genesis-protocol`. | Step 0.1 detects `config.txt` only. Step 0.2 parses free-form. No Step 0.2a. Step 0.4 card renders without the `Additional context from drop zone` block (preserved v1.3.2 behaviour) and without any citation suffixes anywhere (no Layer A source). Step 0.5 `## Fields` table without suffixes, `## Raw config.txt` with verbatim contents, no `## Conversational context from drop zone` section. Byte-identical to v1.3.2 / v1.3.3 rendering for a legacy session — v1.4.1 adds zero ripple to the legacy path. |
| 43 | Synthetic partial-citations fixture — only `idea_summary_source_citation` present, others absent. | Step 0.4 card: `Vision` row carries `[page N]` suffix; Project name / Stack hints / Is-a-plugin / extras rows render without suffix. Per-row gate evaluation confirmed: each row inspects its own citation key independently. Step 0.5 `## Fields` Vision row has suffix, others do not. |
| 44 | Mixed media unadorned honesty — fixture where `attaches_source_citation` is present and cites page 4 of the brief. | `attaches_source_citation` is preserved by Step 0.2a (dict-based parse reads the key). Step 0.4 `Mixed media` row renders **without** suffix (the row's value comes from Step 0.3 disk `Glob`, not from `attaches`). Step 0.5 `## Fields` `Mixed media` row also without suffix. Preserved-but-not-rendered is the honest stance: Layer B cites what it read, and the Mixed media value was read from disk, not from Layer A. Cross-check: a grep of the rendered `bootstrap_intent.md` for `[page 4]` on the Mixed media line returns zero matches. |

### Ship gates

- **v1.3.0 (original)**: #1, #3, #6 mandatory. #2, #4 strongly recommended. #5 documented.
- **v1.3.1 (original)**: #7, #9, #12 mandatory. Regression on v1.3.0 #3 + #6 mandatory. #8 strongly recommended. #10, #11 documented non-blocking.
- **v1.3.2 (previous)**: #13, #14, #15, #18 mandatory. #16, #19 strongly recommended. Regression on v1.3.1 #3, #6, #9, #12 mandatory. #17 documented non-blocking.
- **v1.3.3 (previous)**: #20, #21, #25, #26, #27 mandatory. #22, #23, #24 strongly recommended. Regression on v1.3.2 #15, #16, #17 mandatory. Regression on v1.3.1 #9 mandatory. #10 updated / non-blocking.
- **v1.4.0 (previous)**: **#29, #32, #33, #36, #37, #38 mandatory** — fallback path silent / identity (#29, #38), auth-error graceful fallback (#32), SDK-missing graceful fallback (#33), R9 audit of extractor code (#36), Layer B parser zero-ripple on extended schema (#37). **Strongly recommended**: #28 (happy-path PDF with citations), #30 (text-only inline with `text_char_range`), #31 (image-only, no citations). **Documented non-blocking**: #34 (rate-limit simulation — hard to reproduce offline), #35 (modification-loop cache hit — cache-token assertion depends on live API), #39 (annotation truncation — edge case, synthetic). **Regression on v1.3.3 mandatory**: #20, #25, #27 (locale dispatch + EN body write + Layer B zero-ripple). **Regression on v1.3.2 mandatory**: #13 (write flow happy path on fallback path). **Regression on v1.3.1 mandatory**: #7 (mirror render on in-context path).
- **v1.4.1 (this ship)**: **#40, #41, #42, #44 mandatory** — Layer B citation render happy path (#40), absence-of-citations render parity on fallback fixture (#41), legacy `config.txt` render parity (#42), Mixed media unadorned honesty (#44). **Strongly recommended**: #43 (synthetic partial-citations). **Regression on v1.4.0 mandatory**: #37 (Layer B parser zero-ripple — unchanged; v1.4.1 extends rendering, not parsing), #38 (fallback byte-identity — unchanged; v1.4.1 does not write anything). **Regression on v1.3.2 mandatory**: #18, #19 (Layer B card + bootstrap_intent.md surface — v1.4.1 extends both templates, so the v1.3.2 behaviour must still render correctly for legacy paths). **Regression on v1.3.1 mandatory**: #7 (Layer A mirror unchanged).

**Scenario #1 / #13 / #18 / #20 / #21 / #28 / #29 / #30 / #31 / #32 / #40 / #42 runtime replay note**: runtime replay of scenarios driven by a fresh Claude Code process in an empty directory (including v1.4.0's #28-#35 which exercise live API + subprocess launch, and v1.4.1's #40-#42 which exercise live Phase 0 card render) is not executable from inside a running session. Artefact-level verification remains the ship gate — Python module importability (`python -c "import skills.genesis-drop-zone.scripts.extract_with_citations"`), SKILL.md + phase-0-seed-loading.md dispatch-logic walkthrough, fixture byte-identity via `diff`, JSON / YAML parse validation of fixtures, Layer B parser regression on the extended fixture, grep assertions on the rendered card template (e.g. `[page N]` presence / absence counts). A consistent −0.2 Pain-driven deduction applies per replay-deferred scenario and rolls forward until runtime replay happens, continuing the v1.3.1 → v1.4.0 convention.

## Rationale for v1.3.2 route

- **Write + Layer B integration in one ship** — the anti-Frankenstein principle "declare privileges for code that ships with a downstream reader" is the structural argument. Shipping the Layer A write without updating Layer B to read the file would leave `drop_zone_intent.md` floating on disk. Bundling closes the loop in one atomic ship.
- **Rename Layer A file to `drop_zone_intent.md`** — the name `bootstrap_intent.md` is already owned by Layer B (`memory/project/bootstrap_intent.md` at Step 0.5). Same filename with different schema, different path, different audience is a faux ami. Origin-tagged renaming (`drop_zone_intent.md`) keeps both layers honest and makes Step 0.1 detection unambiguous.
- **First Layer A concentrated privilege, minimum viable** — cwd only, no `mkdir`, no path resolution, no overwrite. Every Étape 1 / 2 / 3 privilege will be measured against this precedent; starting tight is the right discipline.
- **Halt-on-existing, not overwrite nor timestamp-suffix nor second consent** — the context guard precondition (fresh cwd) makes an existing `drop_zone_intent.md` a genuine anomaly. Halt + remediation lets the user reconcile manually; overwriting or timestamping would mask the anomaly and create downstream ambiguity.
- **Two bridges, not one** — accept and decline are conceptually different voices (action taken vs action refused). A single bridge with a conditional tail would dilute both. Two variants keep each voice honest.
- **Path not repeated in accept bridge** — the consent card 2 lines above already showed the absolute path; repeating it alourdir without adding information. Scroll-back recovers the path if needed.
- **Preserve Layer-A-specific extras at Layer B** — `pour_qui`, `langue_detectee`, `budget_ou_contrainte`, `prive_ou_public` cost Victor's conversation turn to extract. Dropping them at Layer B would be silent information loss. Archiving them in `## Conversational context from drop zone` keeps the end-to-end flow informationally complete, available to Phases 1-7 that may want them.
- **Living spec, version-scoped sections** — extending `v2_etape_0_drop_zone.md` with a `## Scope — v1.3.2 write + Layer B handoff` section (and the per-surface sections below) preserves the canonical vein-of-truth pattern that v1.3.1 established. A separate spec for Layer B integration would fragment the narrative; keeping it inline means one document describes the full Étape 0 → Phase 0 cross-layer wire.

## Rationale for v1.3.3 route

- **R9 tier-3 loop closure end-to-end with one dispatch variable per stage** — v1.3.0 / v1.3.1 / v1.3.2 shipped FR + EN runtime strings in parallel (R9 tier 3: bilingual coauthored day 1, no retrofit). v1.3.3 is the single ship that flips rendering from "hardcoded FR / always bilingual" to "locale-detected one-variant-at-a-time". Every string pair already exists; the ship is a rendering policy change, not a template creation ship.
- **Two variables (`welcome_locale` + `content_locale`), not one** — the welcome surface precedes any content. Using one variable forces choosing between always-FR welcome (ignores the EN trigger signal) or blocked welcome (loses the "welcome box IS the invitation" UX principle). Two variables with distinct lifecycles honour the best signal per stage, at the cost of one piece of documented divergence behaviour (welcome in one locale, mirror onwards in another when content differs from trigger).
- **Frontmatter contract unchanged, body locale-switched** — splitting the v1.3.3 change so that Layer B has zero ripple. The Layer B Step 0.2a parser detects null classes by FR canonical string match; extending it to bilingual is a v1.4+ target if real user pain emerges, not a v1.3.x ship. The asymmetry (body = locale-detected human echo; frontmatter = FR canonical data contract) is documented in § "R9 language policy applied" and illustrated in § "Example concrete file — EN body variant".
- **`mixte` → FR tiebreaker** — `langue_detectee` has three values. Display needs deterministic routing. FR is the primary project language (French-speaking machine, Layer 0 user profile, trigger list starts with FR). Picking always-bilingual-for-mixte would re-introduce the exact anti-pattern v1.3.3 removes. Users who want EN can state their intent more clearly.
- **Slash command → FR default** — no language signal at invocation; FR default aligns with trigger-list ordering and is deterministic. Reading `$LANG` / `$LC_ALL` is heavier, error-prone on Windows, and adds environment surface area for tiny benefit (users who type a slash command already have the engineer-oriented entry point). Welcome in FR, mirror onwards in detected locale is acceptable graceful degradation.
- **One new bilingual pair only** — v1.3.3 authors exactly one new runtime string pair (the EN zero-content re-prompt). All other EN variants already existed since v1.3.0 / v1.3.1 / v1.3.2. The small surface area is a feature: the ship is narrow, the anti-Frankenstein gate clears cleanly, the reviewer pass is fast.
- **No new privilege class** — v1.3.3 touches zero privilege map entries. `genesis-drop-zone` stays at v1.3.2's single write privilege. Runtime locale rendering is a read-layer-only change; no disk write beyond what v1.3.2 already authorized, no API call, no subprocess. Clean scope.
- **Living spec, version-scoped sections (third application)** — extending `v2_etape_0_drop_zone.md` with a `## Scope — v1.3.3 runtime locale rendering` section preserves the canonical vein-of-truth pattern established at v1.3.1 and reinforced at v1.3.2. Readers walk the version-scoped sections top-to-bottom to see what each ship layered on — third consecutive application of the pattern.

## Rationale for v1.4.0 route

- **Second privilege class = MINOR bump** — v1.4.0 is the first Genesis ship to cross from PATCH to MINOR since v1.3.0 opened the v1.3.x conversational-layer line. The structural weight comes from three stacked novelties: second privilege class (network, orthogonal to v1.3.2's disk); first external dependency (`ANTHROPIC_API_KEY`, Anthropic Python SDK); first subprocess invocation in `genesis-drop-zone`. Each alone might deserve a PATCH within a generous semver reading; together they deserve a MINOR. The 0.37 tampon above the 8.5 running-average floor absorbs a MINOR ship with ≥ 8.5 self-rating comfortably.
- **Python subprocess over curl or sub-agent** — selected at brainstorm (see § "Rationale for v1.4.0 route" in the Scope v1.4.0 section for the three-way table). curl loses on base64-PDF command-line limits and cross-OS quoting; sub-agent does not deliver Citations API response-level artefacts. Python subprocess reuses the `session-post-processor` run.py portability pattern, isolates the new dependency in a single file, and is byte-identical to Genesis's existing pattern for external Python invocation.
- **Silent graceful fallback over visible degradation** — the earliest draft considered a bilingual note ("Source attribution unavailable — extracted in-context") to explain the absence of citations when the fallback path fires. Rejected: users without the API key would see the note on every session. The note would leak implementation detail into a Victor-facing surface and contaminate R9 tier 3. Silent fallback keeps the UX clean; forensic state goes to stderr.
- **Additive frontmatter, not schema version bump** — v1.4.0 adds optional `<field>_source_citation` keys. Schema version stays at `1`. Dict-based YAML parsing makes Layer B Step 0.2a silently ignore unknown keys. A version bump would force Layer B to branch on version (parser code change, regression surface), delivering zero semantic value on Layer A's side. The additive pattern preserves v1.3.3's zero-Layer-B-ripple one version further.
- **Key omission over explicit null** — when no citation applies, the `_source_citation` key is omitted from the frontmatter rather than written as `null`. Rationale: fallback-path files become byte-identical to v1.3.3 files; the regression probe `diff drop_zone_intent.md tests/fixtures/drop_zone_intent_fixture_v1_3_3_en.md` returns zero differences modulo `created_at` + `skill_version`. Explicit `null` would add noise without semantic value.
- **Three fixtures, not two** — `_fr_with_citations.md`, `_en_with_citations.md`, `_fallback.md`. The fallback fixture is the explicit regression probe for byte-identity with the v1.3.3 canonical `_en_fixture` modulo `skill_version`. Without it, a reader must infer the invariant; with it, the property is assertible via `diff`. The single canonical pairing (one v1.4.0 fixture ↔ one v1.3.3 fixture) removes the three-way contradiction the pre-polish draft carried between the scope item, scenario #29, and scenario #38.
- **1h cache TTL explicit, 5m never** — R8 § Stage 2 warns that Anthropic silently tightened the default TTL from 1h to 5m around March 2026. The extractor hardcodes the 1h TTL and never relies on defaults. The env override `GENESIS_DROP_ZONE_CACHE_TTL` accepts `5m` or `1h` for experimentation but the default path matches the R8 recommendation.
- **Model default `claude-opus-4-7`, override env** — R8 § Stage 2 recommends Opus for extraction quality, Sonnet 4.6 as cost fallback. v1.4.0 defaults to Opus; users can override via `GENESIS_DROP_ZONE_MODEL` to Sonnet or any future model. No hardcoded model-chaining logic (Opus-then-Sonnet-on-failure) — single active model per invocation, keeps the extractor's control flow flat.
- **Image-only drops produce no citations — honest null-visible discipline at the citation layer** — Citations API does not cite images. The v1.4.0 design does not synthesize a pseudo-citation like "seen in attachment.png" — the field's value still renders (Claude extracted it via vision), the citation is just absent. Same honesty principle as the null-class `a trouver ensemble` / `non mentionne` tokens, applied one level deeper.
- **Cross-skill-pattern #2 refinement ("at most one per operation class") is precedent, not one-off** — the refinement to master.md's pattern is a permanent evolution, not a v1.4.0 exception. Future skills with legitimate multi-class needs (e.g. Étape 2 creation skill with disk write + external API) will follow the same multi-class declaration. Anti-Frankenstein gate stays tight: a skill accreting a third class is a signal that the skill probably needs splitting.
- **Living spec, version-scoped sections (fourth application)** — extending `v2_etape_0_drop_zone.md` with a `## Scope — v1.4.0 Citations API extraction` section preserves the canonical vein-of-truth pattern established across the v1.3.x cycle. Four consecutive version-scoped scope sections (v1.3.0, v1.3.1, v1.3.2, v1.3.3) give the pattern load-bearing status — v1.4.0 is the fifth instantiation and demonstrates the pattern extends cleanly across the PATCH/MINOR boundary.

## Rationale for v1.4.1 route

- **PATCH is the honest tranche** — read-only rendering of existing v1.4.0 frontmatter data on two existing Layer B surfaces (Step 0.4 card + Step 0.5 template). No privilege, no dependency, no subprocess, no network, no schema bump, no new bilingual pair, no Layer A ripple. Every structural-weight argument for MINOR is absent. The change is pure surface enrichment at Layer B. Running average ≈ 8.88 has 0.38 tampon above 8.5; a PATCH ship with ≥ 9.0 self-rating fits the streak envelope.
- **Loop-closing, not pain-driven** — no concrete user pain triggered v1.4.1. The feature exists because v1.4.0 created an asymmetry (Layer A mirror shows citations; Layer B card does not) and the system asymmetry is itself the defect. Honest Pain-driven scoring reflects this (projected 8.5–8.7); compensation through Prose cleanliness (tight scope, single additive rendering concept), Best-at-date (reuses the v2_promptor_fusion R8 entry, still fresh until 2026-04-24), Self-contained (single skill touched, `genesis-drop-zone` unchanged byte-for-byte), Anti-Frankenstein (no decoration, no helper, no abstraction — just inline suffix rendering).
- **Inline suffix, not dedicated column or section** — three design options were considered: (a) dedicated `## Source attribution from drop zone` section in Step 0.5 with field→citation table; (b) third `Attribution` column in the `## Fields` table; (c) inline suffix inside the existing `Value` column. Option (a) introduces a second section the reader must reconcile with `## Fields` — two sources of truth for field-value attribution. Option (b) changes the table's structural shape (3 cols → 4) and ripples into legacy `config.txt` sessions that have nothing to put in the new column. Option (c) — selected — is the minimum-surface option: one string concatenation per row, no layout change, reader sees provenance exactly where the value is.
- **Mixed media deliberately unadorned** — the `Mixed media` row on the Step 0.4 card is sourced from Step 0.3 disk `Glob`, not from Layer A's `attaches`. Rendering `attaches_source_citation` on this row would lie about provenance: "this row cites what Victor typed, not what Step 0.3 actually found on disk". The two sources can legitimately diverge (the user drops "logo.png" but the file is actually `brand_logo.png`). The honest stance is: cite what was actually read, preserve the key for future tooling that might want to cross-check the divergence.
- **Propagated citation for derived / inferred fields** — Project slug cites `nom_source_citation` (slug is derived from `nom`, so the provenance is identical). Is-a-plugin cites `type_source_citation` (inferred from `type`, so the provenance of the decision to mark the project as plugin or not traces back to the `type` field's citation). This propagation is honest because the derived value is a deterministic function of the cited source field.
- **Discipline upgrade for cross-skill-pattern #4** — v1.3.3 said "Layer B naturally ignores unknown keys"; v1.4.0 said "additive frontmatter keys preserve zero-Layer-B-ripple at parser level"; v1.4.1 refines to "Layer B may opt-in to render additive keys read-only". Each refinement is additive to the previous — none contradict. The four data-points (v1.3.2 wire / v1.3.3 asymmetry / v1.4.0 additive keys / v1.4.1 additive rendering) give the pattern full evidence of composability. Future Étape-skills can layer on the same way.
- **Zero new fixtures** — the v1.4.0 fixtures carry all citation shapes (pdf_page_range + text_char_range). Reusing them is the narrow-scope honest move; churning fixtures for a read-only feature would be Frankenstein.
- **Living spec, version-scoped sections (sixth application)** — extending `v2_etape_0_drop_zone.md` with a `## Scope — v1.4.1 Layer B citation surfacing` section is the sixth consecutive application of the pattern. Six data-points (v1.3.0 / v1.3.1 / v1.3.2 / v1.3.3 / v1.4.0 / v1.4.1) make the pattern fully load-bearing. The spec's top-to-bottom readability scales: a new reader walks the six scope sections to see what layered on, then reads the five rationale sections for the "why" of each ship.
- **Pain-driven axis honest compensation** — projection: Pain-driven 8.5, Prose cleanliness 9.3, Best-at-date 9.2, Self-contained 9.4, Anti-Frankenstein 9.2. Average ≈ 9.12. The honest acknowledgement of weak Pain-driven is the v1.4.1 self-rating integrity anchor; forcing a false 9.0+ there would be dishonest given no user pain documented.

## Relation to the vision doc

`v2_vision_promptor_fusion.md § "Étape 0 — Le Dépôt"` remains the high-level vision anchor. This spec is the implementation-grade detail. The vision doc will receive a single pointer line near its Étape 0 section: `> **Implementation spec**: see [v2_etape_0_drop_zone.md](./v2_etape_0_drop_zone.md) for the v1.3.0+ skill implementation.` The vision doc otherwise stays intact — hybrid C of Q5 in the v1.3.0 brainstorming session.
