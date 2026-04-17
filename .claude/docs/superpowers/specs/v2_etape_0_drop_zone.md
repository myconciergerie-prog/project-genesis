<!-- SPDX-License-Identifier: MIT -->
---
name: v2 Étape 0 — drop zone welcome (genesis-drop-zone skill)
description: Implementation-grade spec for the LAYER A conversational front door of Genesis v2. Ships the welcome box + token-streamed acknowledgement + bridge message as a vertical slice in v1.3.0; extraction, bootstrap_intent.md write, and handoff to genesis-protocol are deferred to v1.3.1+.
type: spec
target_version: v1.3.0 (welcome vertical slice) → v1.4.0+ (full Étape 0)
created_at: 2026-04-17
originSessionId: project-genesis v1.3.0 brainstorming
status: active
mirrors: skills/genesis-drop-zone/SKILL.md (1:1 section-for-section)
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

### Out of scope (deferred to v1.3.1+)

- Structured extraction of user intent into a target schema (Path A Citations or Path B Structured Outputs per vision doc).
- Writing `bootstrap_intent.md` into any directory.
- Handoff to `genesis-protocol` Phase 0.
- Runtime locale detection (FR vs EN selection).
- `GH_BROWSER` profile routing.
- Any UX toolkit integration (@clack/prompts, Charm Gum, cli-spinners).
- Any R9-related cleanup of `genesis-protocol` or other existing skills.

The slice is intentionally surface-only so the first MINOR bump of the v1.3.x cycle demonstrates the surface without accruing plumbing that would have to be migrated again when extraction lands.

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

## Token-streamed acknowledgement template

Between the welcome and the bridge, the skill reformulates what the user provided. This is Ably's 2026 SSE token-streaming pattern applied to conversational UX [Ably AI UX, "Token streaming for AI UX", 2026] — loading state *transforms into* the final result, rather than a spinner that blocks then replaces.

### Template structure (not verbatim)

```
 ◐ Je regarde ce que tu m'as donne...
   . <one bullet per item the user attached or mentioned>
 ✓ J'ai tout lu.
```

Each bullet is **one short phrase** naming the item in the user's own words when possible. For a PDF titled "brief boulangerie Lyon.pdf" with 3 pages about a bakery project, the bullet is `. un brief "boulangerie a Lyon" (PDF, 3 pages)`. For a photo, `. une photo de <what the photo shows>`. For a URL, `. un lien vers <domain or content summary>`. For free text, `. une idée "<first 8 words verbatim>..."`.

The bullet count matches what the user actually gave. Zero bullets = user only provided the trigger phrase with no content → ack goes straight to a re-prompt: "Je t'écoute — dépose ou écris ce que tu veux me partager." No "✓" closure in that branch.

### Degraded case — unreadable attachment

If Claude cannot read an attached file (exotic binary, oversize PDF past 32 MB × 600 pages, per-request Files API limits [Claude API docs, PDF support]):

```
   . un fichier que je n'arrive pas a lire : <filename>
     Dis-moi ce qu'il contient en mots ?
```

Graceful, no error code, no halt — matches the anti-jargon error-message rule [v2_promptor_fusion_landscape_2026-04-17.md § Stage 1 failure-mode table].

## Bridge message — bilingual

Closes the interaction honestly for v1.3.0 (where extraction is not wired yet). Always printed **in both languages**, regardless of the invocation language, because v1.3.0 has no locale detection and we will not let the user be silently stuck.

```
Extraction et création du projet arrivent bientôt.
Pour l'instant, j'ai bien vu — reviens à Claude Code normalement.

Extraction and project creation are coming soon.
For now, I've seen it — go back to Claude Code normally.
```

The word "bientôt" / "soon" is deliberately time-free. If v1.3.1 ships within a week, fine. If it takes two months, the message is still accurate. No version number hard-coded.

## Concentrated privilege declaration

Per master.md's concentrated-privilege map discipline (cross-skill-pattern #2): every Genesis skill has **at most one** concentrated privilege — one operation that writes outside its own scope or touches something the user cannot easily undo.

**`genesis-drop-zone` in v1.3.0: none.**

Precedent: `journal-system` declared `none` in the map. The welcome + acknowledgement + bridge slice writes nothing, runs no subprocess, makes no network call. Claude reads user-attached files via its native multimodal context — that is a harness-level capability, not a skill privilege.

**Forward note (non-binding)**: v1.3.1+ (extraction + `bootstrap_intent.md` write) will introduce one concentrated privilege — writing the extracted intent into a user-designated project directory. That privilege is declared in the v1.3.1 ship, not here. Anticipating it now would violate the "declare privileges for code that exists" anti-Frankenstein gate.

## 1:1 mirror map with SKILL.md

Cross-skill-pattern #1: when a skill is a faithful implementation of a canonical source document, `SKILL.md` mirrors the source structurally — same sections, same ordering. Drift = merge-blocker.

| This spec section | `genesis-drop-zone/SKILL.md` section | Mirror status |
|---|---|---|
| Position in the v2 architecture | `## Purpose` (condensed one-paragraph form) | Mirrored |
| Scope — v1.3.0 vertical slice | `## Scope` (in/out bullets, copied verbatim) | Mirrored |
| Trigger evaluation gate | `## Trigger` + `## Context guard` (two sections in SKILL.md for dispatch clarity) | Mirrored |
| Welcome body | `## Phase 0 — welcome` with pointer to `phase-0-welcome.md` (no duplicated template text in SKILL.md) | Mirrored (pointer) |
| Token-streamed acknowledgement | `## Phase 0 — acknowledgement` (pattern description only; full template lives in `phase-0-welcome.md`) | Mirrored (pattern) |
| Bridge message | `## Phase 0 — bridge` with pointer to `phase-0-welcome.md` | Mirrored (pointer) |
| Concentrated privilege declaration | `## Concentrated privilege` (verbatim `none` + journal-system precedent reference) | Mirrored |
| Deferred to v1.3.1+ | `## Deferred scope` (verbatim bullet list) | Mirrored |
| Problem statement | — | **Spec-only** (design rationale) |
| UX canon backing | — | **Spec-only** (design rationale) |
| R9 language policy applied | — | **Spec-only** (tier map across artefacts, dev-internal) |
| References / R8 citations | — | **Spec-only** (dev-internal provenance) |
| Verification scenarios | — | **Spec-only** (ship gate, dev-internal) |
| Relation to the vision doc | — | **Spec-only** (cross-doc navigation) |

Rule of thumb for the drift-check gate: **every row tagged `Mirrored` must show section-for-section correspondence; every row tagged `Spec-only` is an expected asymmetry** and is not flagged during review. SKILL.md is the dispatch surface; spec is the design record.

## R9 language policy applied

Three tiers per Layer 0 R9:

| Artefact | Tier | Language |
|---|---|---|
| `v2_etape_0_drop_zone.md` (this file) | Dev/tooling internal doc | English only |
| `skills/genesis-drop-zone/SKILL.md` | Dev/tooling skill dispatch | English only |
| `skills/genesis-drop-zone/phase-0-welcome.md` — **comments + section headings** | Dev/tooling | English only |
| `skills/genesis-drop-zone/phase-0-welcome.md` — **runtime string templates (welcome box, ack template, bridge)** | User-facing runtime | Bilingual FR + EN coauthored day 1 |
| Trigger phrases in `SKILL.md` `description:` frontmatter | User-facing invocation surface | Bilingual FR + EN day 1 — covers both the one-line `description:` text AND the embedded trigger phrase list; written as one frontmatter block, not two |

The mixed-tier nature of `phase-0-welcome.md` is intentional: the file's structure and comments are dev-facing (so a maintainer reads the file in English), but the string templates it ships are what Victor sees and must be bilingual. This is the standard pattern for runtime-text-bearing skill bodies — a precedent to establish here, to reuse when LAYER A grows further (Étapes 1, 2, 3).

## Deferred to v1.3.1+

Ordered by rough priority, non-binding, revisit at each session boundary:

1. Structured extraction of user intent — Path A Citations per vision doc § "Extraction choice". Writes extracted fields into `bootstrap_intent.md`.
2. `bootstrap_intent.md` file write — consent prompt, target directory resolution (cwd or subdir or new project dir), UTF-8 encoding, overwrite protection.
3. Handoff to `genesis-protocol` — invoke `genesis-protocol` with `bootstrap_intent.md` available as the LAYER B seed (replaces `config.txt` in v2 per vision doc § LAYER B phase table).
4. Runtime locale detection — detect user language from trigger match + message content; switch between FR and EN variants dynamically.
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

## Verification scenarios (to replay before v1.3.0 ship)

| # | Scenario | Expected |
|---|---|---|
| 1 | Fresh empty dir, Claude Code opens, user types `/genesis-drop-zone`. | Welcome box prints (FR), skill awaits, ack token-streamed on response, bridge bilingual, skill exits clean. |
| 2 | Fresh empty dir, user types "je veux créer un projet pour gérer mes dépenses". | Claude auto-invokes the skill via intent match; same as #1. |
| 3 | Open Claude Code inside `C:/Dev/Claude_cowork/project-genesis/` (active repo), type `/genesis-drop-zone`. | Context guard fires; bilingual redirect prints; skill does not welcome. |
| 4 | Fresh empty dir, user types trigger + attaches `@tests/fixtures/sample-brief.pdf` (fixture lives in the worktree, honours the "no deliverables in C:\tmp" auto-memory rule). | Ack names the PDF and summarises its content in one bullet. |
| 5 | Fresh empty dir, user types "I want to create a project to track my expenses". | Intent matches (EN trigger), welcome box still FR (no locale detection in v1.3.0). Bridge covers the bilingual gap. |
| 6 | R9 audit — grep SKILL.md + this spec for French strings outside trigger list. | Zero matches. Grep `phase-0-welcome.md` for both FR and EN markers. Both present. |

**Ship gate**: #1, #3, #6 mandatory. #2, #4 strongly recommended (intent match is probabilistic, must be observed to calibrate `description:`). #5 documented, non-blocking.

## Relation to the vision doc

`v2_vision_promptor_fusion.md § "Étape 0 — Le Dépôt"` remains the high-level vision anchor. This spec is the implementation-grade detail. The vision doc will receive a single pointer line near its Étape 0 section: `> **Implementation spec**: see [v2_etape_0_drop_zone.md](./v2_etape_0_drop_zone.md) for the v1.3.0+ skill implementation.` The vision doc otherwise stays intact — hybrid C of Q5 in the v1.3.0 brainstorming session.
