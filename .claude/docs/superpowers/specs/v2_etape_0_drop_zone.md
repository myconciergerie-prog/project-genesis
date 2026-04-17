<!-- SPDX-License-Identifier: MIT -->
---
name: v2 Étape 0 — drop zone welcome + mirror (genesis-drop-zone skill)
description: Implementation-grade spec for the LAYER A conversational front door of Genesis v2. Living spec across versions. v1.3.0 shipped welcome + token-streamed acknowledgement + bridge; v1.3.1 upgrades the acknowledgement into a 9-field structured mirror screen (in-context extraction, zero disk write, no API call). Write of bootstrap_intent.md + handoff to genesis-protocol deferred to v1.3.2+.
type: spec
target_version: v1.3.0 (welcome vertical slice) + v1.3.1 (extraction mirror) → v1.4.0+ (full Étape 0)
created_at: 2026-04-17
updated_at: 2026-04-17 (v1.3.1 brainstorming)
originSessionId: project-genesis v1.3.0 brainstorming
status: active
mirrors: skills/genesis-drop-zone/SKILL.md (1:1 section-for-section across versions)
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

No halt / no error — just a graceful, bilingual redirect.

## Welcome body — FR primary + EN mirror

Both variants are authored in `phase-0-welcome.md` from day 1 per R9. FR is printed by default in v1.3.0. Runtime locale selection is deferred; the EN variant is mirror-ready so v1.3.1+ can wire it in without retrofit.

### FR variant (printed in v1.3.0)

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

### EN variant (mirror-ready, not printed in v1.3.0)

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
- **ASCII-only inside the box, accents allowed outside** — the box mixes Unicode box-drawing characters (`┌ │ ─ └ ┐ ┘`) with content on the same line. That combination has been observed to render unstably on some Windows code-page configurations when content also carries combining diacritics. The bridge message (below) and the context-guard redirect (above) are plain prose lines with no box-drawing, routed through the terminal's stream path which is UTF-8-stable — they keep their accents (`à`, `é`, `ê`, `ô`). This asymmetry is intentional and documented once here, not repeated at every Layer A string the plugin will ship.

ASCII-box dimensions: 60 chars wide, 10 lines high. Fits inside 80-col terminal comfortably, preserves text-centering illusion.

## Mirror screen — template & reveal

**v1.3.1 supersedes** v1.3.0's bullet-list acknowledgement. Git history preserves the prior bullet form (`◐ Je regarde... . un brief "X" (PDF, N pages) ... ✓ J'ai tout lu.`); v1.3.1 forward, the mirror is a structured 9-field aligned-column table revealed row-by-row.

Between the welcome and the bridge, the skill reformulates what the user provided by extracting a 9-field intent schema (see § "Extraction schema — 9 fields" below) and rendering it as an aligned-column table. Underlying UX pattern is Ably's 2026 SSE token-streaming approach [Ably AI UX, "Token streaming for AI UX", 2026] — loading state *transforms into* the final result rather than a spinner that blocks then replaces. Each of the 9 rows appears one at a time.

### Template structure (FR — rendered by default in v1.3.1)

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

### Template structure (EN — mirror-ready, not rendered in v1.3.1)

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

### Zero-content branch (v1.3.0 preserved)

If the user's response contains only the trigger phrase with no content to echo:

```
 Je t'écoute — dépose ou écris ce que tu veux me partager.
```

No `◐`, no mirror, no `✓`. The skill waits for the user's next turn and re-runs the mirror flow when content arrives.

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
| `idea_summary` | Idee | Idea | 1-line synopsis of the user's idea, in user's own words when possible. Always filled when any content is present — dropping the welcome path only happens with zero content. | N/A — always filled at this point. If somehow empty, `texte seul — a trouver ensemble`. |
| `pour_qui` | Pour qui | Who for | Target users / audience inferred from content. | `a trouver ensemble` (core) |
| `type` | Type | Kind | Rough category: appli web, appli mobile, outil CLI, plugin, documentation, site, bibliotheque, … | `a trouver ensemble` (core) |
| `nom` | Nom | Name | Project name if the user proposed one (explicit — not auto-slugged). | `a trouver ensemble` (core) |
| `attaches` | Depose | Dropped | List of dropped items with brief descriptor (see truncation rule). `texte seul` if nothing attached. | N/A — always filled. |
| `langue_detectee` | Langue | Language | `FR` / `EN` / `mixte` — detected from the user's text. Extracted but does **not** switch mirror rendering in v1.3.1 (runtime locale deferred v1.3.2+). | N/A — always filled. |
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

## Concentrated privilege declaration

Per master.md's concentrated-privilege map discipline (cross-skill-pattern #2): every Genesis skill has **at most one** concentrated privilege — one operation that writes outside its own scope or touches something the user cannot easily undo.

**`genesis-drop-zone` in v1.3.0: none.**
**`genesis-drop-zone` in v1.3.1: still `none`.**

Precedent: `journal-system` declared `none` in the map. The welcome + acknowledgement + bridge slice writes nothing, runs no subprocess, makes no network call. Claude reads user-attached files via its native multimodal context — that is a harness-level capability, not a skill privilege. v1.3.1 extends acknowledgement into a structured 9-field mirror via the same in-context multimodal path — no disk write, no subprocess, no network call, no Anthropic API invocation. The privilege declaration therefore remains `none` across both versions.

**Forward note (non-binding)**: v1.3.2+ (`bootstrap_intent.md` write + target-directory resolution + handoff to `genesis-protocol`) will introduce one concentrated privilege — writing the extracted intent into a user-designated project directory. That privilege is declared in the v1.3.2 ship, not here. Anticipating it now would violate the "declare privileges for code that exists" anti-Frankenstein gate. Note the first-Layer-A-privilege precedent that ship will set: it should carry a consent card, overwrite-protection, and a bilingual confirmation prompt, matching the Layer A discipline of `pepite-flagging`'s per-target consent floor.

## 1:1 mirror map with SKILL.md

Cross-skill-pattern #1: when a skill is a faithful implementation of a canonical source document, `SKILL.md` mirrors the source structurally — same sections, same ordering. Drift = merge-blocker.

| This spec section | `genesis-drop-zone/SKILL.md` section | Mirror status |
|---|---|---|
| Position in the v2 architecture | `## Purpose` (condensed, covers both v1.3.0 welcome and v1.3.1 mirror) | Mirrored |
| Scope — v1.3.0 vertical slice | `## Scope / In scope (v1.3.0)` sub-block (historical, retained for version traceability) | Mirrored |
| Scope — v1.3.1 extraction | `## Scope / In scope (v1.3.1)` sub-block (in/out bullets, copied verbatim) | Mirrored |
| Trigger evaluation gate | `## Trigger` + `## Context guard` (two sections in SKILL.md for dispatch clarity) | Mirrored |
| Welcome body | `## Phase 0 — welcome` with pointer to `phase-0-welcome.md` (no duplicated template text in SKILL.md) | Mirrored (pointer) |
| Mirror screen — template & reveal | `## Phase 0 — mirror` (pattern description only; full template lives in `phase-0-welcome.md`) | Mirrored (pattern) |
| Extraction schema — 9 fields | `## Phase 0 — mirror` subsection `### Schema` (9-field table referenced from dispatch) | Mirrored (table) |
| Bridge message — bilingual (v1.3.1 update) | `## Phase 0 — bridge` with pointer to `phase-0-welcome.md § Bridge message (v1.3.1)` | Mirrored (pointer) |
| Concentrated privilege declaration | `## Concentrated privilege` (verbatim `none` + journal-system precedent + v1.3.2 forward note) | Mirrored |
| Deferred to v1.3.2+ | `## Deferred scope` (verbatim bullet list, updated) | Mirrored |
| Problem statement | — | **Spec-only** (design rationale) |
| UX canon backing | — | **Spec-only** (design rationale) |
| R9 language policy applied | — | **Spec-only** (tier map across artefacts, dev-internal) |
| References / R8 citations | — | **Spec-only** (dev-internal provenance) |
| Verification scenarios | — | **Spec-only** (ship gate, dev-internal) |
| Relation to the vision doc | — | **Spec-only** (cross-doc navigation) |
| Rationale for v1.3.1 route | — | **Spec-only** (design decision log) |

Rule of thumb for the drift-check gate: **every row tagged `Mirrored` must show section-for-section correspondence; every row tagged `Spec-only` is an expected asymmetry** and is not flagged during review. SKILL.md is the dispatch surface; spec is the design record.

## R9 language policy applied

Three tiers per Layer 0 R9:

| Artefact | Tier | Language |
|---|---|---|
| `v2_etape_0_drop_zone.md` (this file) | Dev/tooling internal doc | English only |
| `skills/genesis-drop-zone/SKILL.md` | Dev/tooling skill dispatch | English only |
| `skills/genesis-drop-zone/phase-0-welcome.md` — **comments + section headings** | Dev/tooling | English only |
| `skills/genesis-drop-zone/phase-0-welcome.md` — **runtime string templates (welcome box, mirror template + 9-field labels, bridge)** | User-facing runtime | Bilingual FR + EN coauthored day 1 |
| Trigger phrases in `SKILL.md` `description:` frontmatter | User-facing invocation surface | Bilingual FR + EN day 1 — covers both the one-line `description:` text AND the embedded trigger phrase list; written as one frontmatter block, not two |

The mixed-tier nature of `phase-0-welcome.md` is intentional: the file's structure and comments are dev-facing (so a maintainer reads the file in English), but the string templates it ships are what Victor sees and must be bilingual. This is the standard pattern for runtime-text-bearing skill bodies — a precedent to establish here, to reuse when LAYER A grows further (Étapes 1, 2, 3).

## Deferred to v1.3.2+

Ordered by rough priority, non-binding, revisit at each session boundary. Item 1 (in-context extraction of the 9-field schema) was closed in v1.3.1; this list reflects what remains.

1. **Path A Citations upgrade** — replace v1.3.1's in-context extraction with an Anthropic API call enabling `citations: {enabled: true}` per `document` block. Surfaces `cited_text` + `document_index` for each extracted field, so the mirror can optionally show source attribution (`[page 1 du brief]`) with API-hard traceability. Introduces the first "external API call" privilege for `genesis-drop-zone`; sequenced alongside or after the write + handoff so the privilege ship is not speculative.
2. `bootstrap_intent.md` file write — consent prompt, target directory resolution (cwd or subdir or new project dir), UTF-8 encoding, overwrite protection. **First concentrated privilege for the skill.**
3. Handoff to `genesis-protocol` — invoke `genesis-protocol` with `bootstrap_intent.md` available as the LAYER B seed (replaces `config.txt` in v2 per vision doc § LAYER B phase table).
4. Runtime locale detection — detect user language from trigger match + message content; switch between FR and EN variants dynamically. Currently in v1.3.1 the `langue_detectee` field is extracted but the mirror renders FR regardless; v1.3.2 closes the loop by rendering the mirror (and the welcome box if retroactively wired) in the detected language.
5. `GH_BROWSER` profile routing wire-up — read Chrome profile map from Layer 0, export `GH_BROWSER` before any `gh` invocation in the downstream LAYER B.
6. UX toolkit integration — `@clack/prompts` structural skeleton, Charm Gum for select prompts, cli-spinners for the `◐` animation.
7. Completion chime (cross-platform) — macOS `afplay`, Windows `[console]::beep`, Linux `paplay`. Honours the "rising interval" convention per vision doc § "The sound of Genesis".

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

### v1.3.0 regression set (unchanged)

| # | Scenario | Expected |
|---|---|---|
| 1 | Fresh empty dir, Claude Code opens, user types `/genesis-drop-zone`. | Welcome box prints (FR), skill awaits, **mirror token-streamed on response** (v1.3.1 replaces v1.3.0's bullet ack), bridge bilingual with v1.3.1 content, skill exits clean. |
| 2 | Fresh empty dir, user types "je veux créer un projet pour gérer mes dépenses". | Claude auto-invokes the skill via intent match; same as #1. |
| 3 | Open Claude Code inside `C:/Dev/Claude_cowork/project-genesis/` (active repo), type `/genesis-drop-zone`. | Context guard fires; bilingual redirect prints; skill does not welcome. |
| 4 | Fresh empty dir, user types trigger + attaches `@tests/fixtures/sample-brief.pdf` (fixture lives in the worktree, honours the "no deliverables in C:\tmp" auto-memory rule). | Mirror names the PDF in the `Depose` row and extracts schema fields from the PDF content (Idee + Pour qui + Type derived from content). |
| 5 | Fresh empty dir, user types "I want to create a project to track my expenses". | Intent matches (EN trigger), welcome box still FR, mirror still FR, `Langue` row reads `EN`. Bridge bilingual covers the gap. |
| 6 | R9 audit — grep SKILL.md + this spec for French strings outside trigger list. | Zero matches. Grep `phase-0-welcome.md` for both FR and EN mirror markers. Both present. |

### v1.3.1 new scenarios

| # | Scenario | Expected |
|---|---|---|
| 7 | Fresh empty dir + text-only drop ("j'ai une idee de boulangerie"). | Mirror renders 9 rows: `Idee` filled verbatim, `Pour qui`/`Type`/`Nom` = `a trouver ensemble`, `Depose` = `texte seul`, `Langue` = `FR`, `Budget`/`Visibilite`/`Tech` = `non mentionne(e)`. Bridge v1.3.1 text prints after. |
| 8 | Fresh empty dir + text + PDF + photo (multimodal rich case). | Mirror renders 9 rows with `Depose` listing all 3 items (or truncated at 3 with `+ N autres` if more). `Idee`/`Pour qui`/`Type` extracted from combined content. |
| 9 | Fresh empty dir + trigger phrase only, zero content attached or written. | No `◐` line, no mirror, no `✓` closure. Re-prompt `Je t'écoute — dépose ou écris ce que tu veux me partager.` printed (v1.3.0 branch preserved). When user responds, mirror flow fires normally. |
| 10 | Fresh empty dir + EN content ("I want to build a small task tracker for my team"). | Mirror rendered in **FR** with `Langue` = `EN` row. Bridge bilingual covers locale gap. |
| 11 | Very long idea text (e.g. 200-character paragraph) dropped. | `Idee` row truncated at 57 chars + `...`. Other rows render normally. Full content retained in Claude's context (not disposed — kept for v1.3.2+ handoff). |
| 12 | R9 audit — grep FR+EN mirror templates in `phase-0-welcome.md` after v1.3.1 additions; grep accents inside FR table block vs FR surrounding prose. | Both FR and EN mirror templates present. Zero accents inside FR table rows (ASCII-pure discipline). Accents present in `◐`/`✓` prose and in bridge (plain-prose, accent-stable). |

### Ship gates

- **v1.3.0 (original)**: #1, #3, #6 mandatory. #2, #4 strongly recommended. #5 documented.
- **v1.3.1 (this ship)**: #7, #9, #12 mandatory — new happy path + zero-content regression + R9 discipline extension. Regression on v1.3.0 #3 + #6 still mandatory (context guard + R9 audit stay green). #8 strongly recommended (multimodal rich case). #10, #11 documented non-blocking.

**Scenario #1 replay note**: runtime replay of #1 requires a fresh Claude Code process in an empty directory, which is not executable from inside a running session. Artefact-level verification remains the ship gate (template parseability, dispatch coherence, context-guard logic verified against real filesystem), with Scenario #1's harness-level replay (actual `/genesis-drop-zone` slash command dispatch, actual intent-match routing) deferred to an externally-launched fresh session per session-traceability discipline.

## Relation to the vision doc

`v2_vision_promptor_fusion.md § "Étape 0 — Le Dépôt"` remains the high-level vision anchor. This spec is the implementation-grade detail. The vision doc will receive a single pointer line near its Étape 0 section: `> **Implementation spec**: see [v2_etape_0_drop_zone.md](./v2_etape_0_drop_zone.md) for the v1.3.0+ skill implementation.` The vision doc otherwise stays intact — hybrid C of Q5 in the v1.3.0 brainstorming session.
