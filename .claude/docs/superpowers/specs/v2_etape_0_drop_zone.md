<!-- SPDX-License-Identifier: MIT -->
---
name: v2 Étape 0 — drop zone welcome + mirror + write + Layer B handoff (genesis-drop-zone skill)
description: Implementation-grade spec for the LAYER A conversational front door of Genesis v2. Living spec across versions. v1.3.0 shipped welcome + token-streamed acknowledgement + bridge; v1.3.1 upgraded the acknowledgement into a 9-field structured mirror screen (in-context extraction, zero disk write, no API call); v1.3.2 added first Layer A write privilege (drop_zone_intent.md to cwd after consent) + Layer B handoff wire into genesis-protocol Phase 0; v1.3.3 wires runtime locale detection (welcome + mirror + consent card + halt + bridges + body echo switch between FR and EN via welcome_locale / content_locale variables). Citations API upgrade, programmatic handoff, and UX toolkit polish deferred to v1.3.4+.
type: spec
target_version: v1.3.0 (welcome vertical slice) + v1.3.1 (extraction mirror) + v1.3.2 (write + Layer B handoff) + v1.3.3 (runtime locale rendering) → v1.4.0+ (full Étape 0 polish)
created_at: 2026-04-17
updated_at: 2026-04-18 (v1.3.3 brainstorming)
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

### Cross-layer pattern (master.md cross-skill-pattern #4)

v1.3.2 is the first cross-layer wire in the Genesis plugin. The pattern established here is the reference implementation for future Étape 1 → Phase 1 / Étape 2 → Phase 2 / Étape 3 → Phase 3 wires as Layer A grows:

1. Layer A captures user intent in a dedicated file at cwd root with origin-tagged naming (`drop_zone_intent.md`, later e.g. `etincelle_refinement.md`, `creation_brief.md`, `miroir_review.md`).
2. Layer B's corresponding phase detects the Layer A file, parses it, maps its fields to the Layer B schema, and archives the Layer-A-specific extras in a dedicated section of the Layer B bootstrap file.
3. Precedence rule always favours the Layer A file over legacy / engineer-written inputs; never silent merge.
4. R9 tier stays clean: Layer A field names in frontmatter are English snake_case; Layer A user-facing labels live only in `phase-X-*.md` runtime templates; Layer B reads the snake_case and re-labels for its own card.
5. Origin tags on Layer B's Phase card make the Layer A → Layer B provenance explicit to Victor.

This pattern is load-bearing for the v2 conversational surface. Future sessions that add an Étape 1 skill will follow the same shape.

## Concentrated privilege declaration

Per master.md's concentrated-privilege map discipline (cross-skill-pattern #2): every Genesis skill has **at most one** concentrated privilege — one operation that writes outside its own scope or touches something the user cannot easily undo.

**`genesis-drop-zone` in v1.3.0: none.**
**`genesis-drop-zone` in v1.3.1: still `none`.**
**`genesis-drop-zone` in v1.3.2: writes `drop_zone_intent.md` to cwd after the user accepts a bilingual consent card, halt-on-existing, no `mkdir`, no path resolution beyond cwd.**

Precedent for v1.3.0 / v1.3.1: `journal-system` declared `none` in the map. The welcome + acknowledgement + bridge slice writes nothing, runs no subprocess, makes no network call. Claude reads user-attached files via its native multimodal context — that is a harness-level capability, not a skill privilege. v1.3.1 extended acknowledgement into a structured 9-field mirror via the same in-context multimodal path — no disk write, no subprocess, no network call, no Anthropic API invocation.

v1.3.2 breaks that `none` streak with the minimum viable concentrated privilege — **one file, one path, one operation**. Mitigations:

- **Bilingual consent card** (§ "Consent card — template + flow") is the single gate. The user sees the absolute target path with an arrow marker before any write can proceed. Modifications route back through mirror re-render + consent re-print, never through silent field changes.
- **Halt-on-existing** (§ "Halt branch — file already exists") covers the only unexpected state — an existing `drop_zone_intent.md` at cwd. Halt + remediation, never overwrite, never timestamp-suffix fallback, never second consent for the destructive path.
- **Narrow path resolution** — cwd only. No `mkdir`, no subdir write, no absolute-path-anywhere write. The context guard already asserts cwd fresh; keeping the privilege tight to that cwd means the filesystem surface area stays 1 file.
- **Atomic write pattern** — temp file + rename, post-write size verification, failure surfaces bilingually without half-written remnants.
- **Match pepite-flagging's per-target consent floor** — this precedent was already set for Layer A privileges in the master.md map. v1.3.2 honours it on the first real Layer A write.

This declaration is the **precedent that all future Étape 1 / Étape 2 / Étape 3 Layer A privileges will be measured against**. Widening the privilege surface in a later ship (subdir writes, `mkdir`, multi-file writes, API calls) requires the same pattern — declare privilege for code that exists, never speculate, always carry mitigations one-for-one with the privilege.

**Forward note (non-binding)**: v1.3.3+ may add a second privilege to `genesis-drop-zone` — an external Anthropic API call for Path A Citations extraction (audit-trail via `cited_text` + `document_index`). That would be a different privilege class from v1.3.2's write (network rather than disk), so the map entry would extend to list both. Cross-skill-pattern #2's "at most one" convention is about privilege *operations per skill*; a second privilege with a distinct class and its own mitigation is acceptable if the anti-Frankenstein gate clears. The decision to add it or defer further is made when the downstream reader for API-hard citations surfaces.

## 1:1 mirror map with SKILL.md

Cross-skill-pattern #1: when a skill is a faithful implementation of a canonical source document, `SKILL.md` mirrors the source structurally — same sections, same ordering. Drift = merge-blocker.

| This spec section | `genesis-drop-zone/SKILL.md` section | Mirror status |
|---|---|---|
| Position in the v2 architecture | `## Purpose` (condensed, covers v1.3.0 welcome + v1.3.1 mirror + v1.3.2 write) | Mirrored |
| Scope — v1.3.0 vertical slice | `## Scope / In scope (v1.3.0)` sub-block (historical, retained for version traceability) | Mirrored |
| Scope — v1.3.1 extraction | `## Scope / In scope (v1.3.1)` sub-block (in/out bullets, copied verbatim) | Mirrored |
| Scope — v1.3.2 write + Layer B handoff | `## Scope / In scope (v1.3.2)` sub-block (in/out bullets, copied verbatim) | Mirrored |
| Scope — v1.3.3 runtime locale rendering | `## Scope / In scope (v1.3.3)` sub-block (in/out bullets, copied verbatim) | Mirrored |
| Runtime locale — signal + dispatch (v1.3.3) | `## Locale dispatch (v1.3.3)` (two-variable table + render-target map) | Mirrored |
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
| Concentrated privilege declaration | `## Concentrated privilege` (verbatim v1.3.0 none + v1.3.1 none + v1.3.2 write declaration + mitigations) | Mirrored |
| Deferred to v1.3.4+ | `## Deferred scope` (verbatim bullet list, updated) | Mirrored |
| Problem statement | — | **Spec-only** (design rationale) |
| UX canon backing | — | **Spec-only** (design rationale) |
| R9 language policy applied | — | **Spec-only** (tier map across artefacts, dev-internal) |
| References / R8 citations | — | **Spec-only** (dev-internal provenance) |
| Verification scenarios | — | **Spec-only** (ship gate, dev-internal) |
| Relation to the vision doc | — | **Spec-only** (cross-doc navigation) |
| Rationale for v1.3.1 route | — | **Spec-only** (design decision log) |
| Rationale for v1.3.2 route | — | **Spec-only** (design decision log) |
| Rationale for v1.3.3 route | — | **Spec-only** (design decision log) |

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

## Deferred to v1.3.4+

Ordered by rough priority, non-binding, revisit at each session boundary. Items closed across the v1.3.x cycle so far: the `bootstrap_intent.md` file write and Layer B handoff (both closed in v1.3.2), and **runtime locale detection** (closed in v1.3.3 — welcome + mirror + consent card + halt + bridges + body prose + body mirror echo all dispatch on `welcome_locale` / `content_locale`). This list reflects what remains.

1. **Path A Citations upgrade** — replace v1.3.1's in-context extraction with an Anthropic API call enabling `citations: {enabled: true}` per `document` block. Surfaces `cited_text` + `document_index` for each extracted field, so the mirror can optionally show source attribution (`[page 1 du brief]`) with API-hard traceability. Introduces the first "external API call" privilege for `genesis-drop-zone` (a second privilege class on top of v1.3.2's disk write, with its own mitigations — `ANTHROPIC_API_KEY` presence check, token-budget awareness, graceful fallback to in-context extraction). Downstream reader is now in place as of v1.3.2 so the privilege ship is no longer speculative. **v1.3.4 candidate.**
2. **Programmatic handoff** — auto-invoke `genesis-protocol` without the user typing `/genesis-protocol` after the accept bridge. Requires a harness-level skill-to-skill invocation mechanism that is not 2026-04 Claude Code ready. Human-in-the-loop via the accept bridge's instruction is the v1.3.2 pattern; the programmatic path can ship when the harness supports it without changing the bridge text semantics.
3. `GH_BROWSER` profile routing wire-up — read Chrome profile map from Layer 0, export `GH_BROWSER` before any `gh` invocation in the downstream LAYER B.
4. UX toolkit integration — `@clack/prompts` structural skeleton, Charm Gum for select prompts, cli-spinners for the `◐` animation.
5. Completion chime (cross-platform) — macOS `afplay`, Windows `[console]::beep`, Linux `paplay`. Honours the "rising interval" convention per vision doc § "The sound of Genesis".
6. Error handling refinements — permission-denied / disk-full / symlink-pointing-to-directory edge cases currently let `OSError` bubble up naturally. v1.3.4+ adds halt + remediation if any of these produces real user pain in v1.3.2–1.3.3 usage. v1.3.2's floor is "write succeeds or harness shows the stack".
7. **Bilingual Layer B null-class parsing** — if `drop_zone_intent.md` frontmatter null-class tokens ever carry EN canonical variants alongside FR canonical, Layer B's Step 0.2a parser grows a bilingual branch. **v1.4+** target, not v1.3.x.
8. **Three-locale-or-more expansion** — if Genesis ships beyond FR + EN (e.g. ES, DE), `welcome_locale` and `content_locale` become n-way enums. Minor, deferred until a real non-FR/EN user emerges.

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

## Verification scenarios

The scenarios below cover both ship gates. Scenarios #1-#6 were defined for v1.3.0 and remain valid as regression guards for v1.3.1 (the v1.3.0 welcome + context guard + trigger evaluation surface stays untouched). Scenarios #7-#12 are v1.3.1 additions targeting the mirror screen, schema extraction, and bridge update.

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

### Ship gates

- **v1.3.0 (original)**: #1, #3, #6 mandatory. #2, #4 strongly recommended. #5 documented.
- **v1.3.1 (original)**: #7, #9, #12 mandatory. Regression on v1.3.0 #3 + #6 mandatory. #8 strongly recommended. #10, #11 documented non-blocking.
- **v1.3.2 (previous)**: #13, #14, #15, #18 mandatory. #16, #19 strongly recommended. Regression on v1.3.1 #3, #6, #9, #12 mandatory. #17 documented non-blocking.
- **v1.3.3 (this ship)**: **#20, #21, #25, #26, #27 mandatory** — welcome+content divergence (bidirectional) + EN body write + R9 audit on new EN re-prompt + Layer B zero-ripple regression. **Strongly recommended**: #22 (mixte tiebreaker), #23 (slash graceful degradation), #24 (zero-content locale). **Regression on v1.3.2 mandatory**: #15 (halt-on-existing — now must render in detected `content_locale`), #16 (modification loop — `content_locale` re-evaluation), #17 (R9 audit of the written file — FR canonical null tokens preserved in frontmatter). **Regression on v1.3.1 mandatory**: #9 (zero-content branch — now has bilingual re-prompt pair). **Documented non-blocking**: #10 updated to reflect v1.3.3 closure (EN content now renders EN mirror; scenario #10's v1.3.1 expectation is superseded).

**Scenario #1 / #13 / #18 / #20 / #21 runtime replay note**: runtime replay of scenarios driven by a fresh Claude Code process in an empty directory (including v1.3.3's #20, #21, #23, #24 which exercise the locale dispatch live) is not executable from inside a running session. Artefact-level verification remains the ship gate — template parseability per locale variant, dispatch coherence, fixture inspection, Layer B parser regression on the new EN fixture. A consistent −0.2 Pain-driven deduction applies per replay-deferred scenario and rolls forward until runtime replay happens, continuing the v1.3.1 / v1.3.2 convention.

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

## Relation to the vision doc

`v2_vision_promptor_fusion.md § "Étape 0 — Le Dépôt"` remains the high-level vision anchor. This spec is the implementation-grade detail. The vision doc will receive a single pointer line near its Étape 0 section: `> **Implementation spec**: see [v2_etape_0_drop_zone.md](./v2_etape_0_drop_zone.md) for the v1.3.0+ skill implementation.` The vision doc otherwise stays intact — hybrid C of Q5 in the v1.3.0 brainstorming session.
