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

### Out of scope (deferred to v1.3.4+)

- API-powered Path A Citations extraction (audit-trail via `cited_text` + `document_index`). First "external API call" privilege; downstream reader (Layer B Phase 0) already in place as of v1.3.2.
- Programmatic handoff — auto-invoke `genesis-protocol` without user typing the slash command. Human-in-the-loop is the v1.3.2 pattern.
- `GH_BROWSER` profile routing.
- UX toolkit integration (@clack/prompts, Charm Gum, cli-spinners).
- Completion chime (cross-platform).
- Error handling refinements (permission-denied / disk-full / symlink edge cases).
- **Bilingual Layer B null-class parsing** — v1.4+ target if a real pain point emerges (frontmatter tokens carrying EN canonical variants alongside FR).
- **Three-locale-or-more expansion** — ES, DE, etc. Deferred until a real non-FR/EN user emerges.

The v1.3.3 ship closes R9 tier-3 rendering loop end-to-end. v1.3.4+ refines remaining polish items.

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

## Phase 0 — welcome

Print the welcome ASCII box from `phase-0-welcome.md`. Locale dispatch: use the FR variant when `welcome_locale = FR`, the EN variant when `welcome_locale = EN` (see `## Locale dispatch (v1.3.3)` above). Do not inline the template here — it lives in the phase body file so bilingual audit greps have a single target.

After printing the box, wait for the user's next conversational turn. Do not prompt, do not block, do not spin a loading indicator — the welcome box is itself the invitation. The user's next message (text, text + attached files, text + URL, or any combination) feeds the acknowledgement step below.

## Phase 0 — mirror

When the user's response arrives, extract the 9-field intent schema from the dropped content (text, PDFs, images, URLs — all read via multimodal). **v1.3.3**: resolve `content_locale` from the extracted `langue_detectee` value, then render the FR variant of the mirror template when `content_locale = FR` (from `phase-0-welcome.md § "Mirror template — FR"`) or the EN variant when `content_locale = EN` (from `phase-0-welcome.md § "Mirror template — EN"`). Reveal rows progressively (Ably token-streaming pattern).

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
| `skill_version` | string | Read from `.claude-plugin/plugin.json` at write time (`1.3.3` for this ship). |
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

See the canonical spec `.claude/docs/superpowers/specs/v2_etape_0_drop_zone.md § "drop_zone_intent.md — schema + body format (v1.3.2)"` for the full template and the concrete illustrative example.

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

The concentrated privilege of `genesis-drop-zone` across versions:

- **v1.3.0**: `none` (welcome + bullet-list ack + bridge).
- **v1.3.1**: `none` (extraction mirror, still in-context only).
- **v1.3.2**: **writes `drop_zone_intent.md` to cwd after the user accepts a bilingual consent card, halt-on-existing, no `mkdir`, no path resolution beyond cwd.** First Layer A privilege.
- **v1.3.3**: unchanged privilege class (still disk write to cwd after consent, halt-on-existing, no `mkdir`). Runtime rendering is now locale-detected via `welcome_locale` / `content_locale`; the privilege operation itself is untouched.

v1.3.2 breaks the `none` streak with the minimum viable concentrated privilege — one file, one path, one operation. Mitigations ship one-for-one with the privilege:

- **Bilingual consent card** (single gate; absolute path with arrow marker; natural-language response; modifications route back through mirror re-render). **v1.3.3**: consent card now renders in the detected `content_locale` instead of always-bilingual — still a single gate, still natural-language response routing.
- **Halt-on-existing** (pre-write check; no overwrite; no timestamp-suffix fallback; no second destructive-consent prompt; matches `session-post-processor` halt-on-leak precedent).
- **Narrow path resolution** — cwd only. No `mkdir`, no subdir, no arbitrary path. Context guard already asserted cwd fresh on entry.
- **Post-write verification** — `test -s` confirms the file exists and has non-zero size before the accept bridge prints.
- **Per-target consent floor match with `pepite-flagging`** — the precedent for Layer A privileges.

This declaration is the precedent that all future Étape 1 / Étape 2 / Étape 3 Layer A privileges will be measured against. Widening the privilege surface in a later ship (subdir writes, `mkdir`, multi-file writes, API calls) requires the same pattern: declare privilege for code that exists, never speculate, carry mitigations one-for-one.

**Forward note (non-binding)**: v1.3.4+ may introduce a second privilege — external Anthropic API call for Path A Citations (audit-trail via `cited_text` + `document_index`). That would be a different privilege class (network vs disk); the map entry would extend to list both.

## Deferred scope

Ordered by rough priority, non-binding, revisit at each session boundary:

1. API-powered Path A Citations extraction — audit-trail via `cited_text` + `document_index`. First "external API call" privilege; downstream reader in Layer B already in place as of v1.3.2. **v1.3.4 candidate.**
2. Programmatic handoff — auto-invoke `genesis-protocol` without the user typing the slash command. Requires harness-level skill-to-skill invocation not 2026-04 ready.
3. `GH_BROWSER` profile routing wire-up.
4. UX toolkit integration — @clack/prompts, Charm Gum, cli-spinners.
5. Completion chime (cross-platform).
6. Error handling refinements — permission-denied / disk-full / symlink edge cases currently let `OSError` bubble up; v1.3.4+ adds halt + remediation if user pain emerges.
7. **Bilingual Layer B null-class parsing** — if `drop_zone_intent.md` frontmatter null-class tokens ever carry EN canonical variants alongside FR canonical, Layer B's Step 0.2a parser grows a bilingual branch. **v1.4+** target, not v1.3.x.
8. **Three-locale-or-more expansion** — if Genesis ships beyond FR + EN (e.g. ES, DE), `welcome_locale` and `content_locale` become n-way enums. Deferred until a real non-FR/EN user emerges.
