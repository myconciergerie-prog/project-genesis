<!-- SPDX-License-Identifier: MIT -->
---
name: genesis-drop-zone
description: Layer A conversational front door for Genesis v2 project bootstrap — print the unified drop-zone welcome box, reformulate what the user gave in a token-streamed acknowledgement, close with an honest bilingual bridge. Invoked by the slash command /genesis-drop-zone or by natural-language intent phrases ("je veux créer un projet", "nouveau projet", "démarre un projet", "dis-moi comment commencer", "I want to create a project", "start a new project", "new project"). Only fires in a fresh context (no existing project in cwd) — inside an active project the skill prints a bilingual redirect and exits.
---

# Genesis Drop Zone

## Purpose

Genesis v1 is an engineer's protocol that speaks to engineers. The v2 vision adds a conversational Layer A where a non-technical user can open Claude Code, drop an idea in any form (text, PDF, photo, link, audio), and be met by a warm conversational surface instead of a config file. `genesis-drop-zone` is the first Layer A skill. v1.3.0 shipped the welcome + token-streamed acknowledgement + bridge vertical slice; **v1.3.1 upgrades the acknowledgement into a structured 9-field mirror screen** (in-context extraction of user intent, rendered as an aligned-column table revealed row by row, no API call, no disk write). The write of `bootstrap_intent.md` + handoff to `genesis-protocol` remain deferred to v1.3.2+.

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

### Out of scope (deferred to v1.3.2+)

- API-powered Path A Citations extraction (audit-trail via `cited_text` + `document_index`).
- Writing `bootstrap_intent.md` into any directory.
- Handoff to `genesis-protocol` Phase 0.
- Runtime locale detection (FR vs EN selection — `langue_detectee` extracted but mirror still renders FR in v1.3.1).
- `GH_BROWSER` profile routing.
- UX toolkit integration (@clack/prompts, Charm Gum, cli-spinners).
- Completion chime (cross-platform).

The slice stays surface-only so the first MINOR bump of the v1.3.x cycle demonstrates the surface without accruing plumbing to migrate.

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

No halt, no error, no stack trace — just a graceful bilingual redirect and clean exit.

## Phase 0 — welcome

Print the welcome ASCII box from `phase-0-welcome.md` § "FR welcome box (printed by default in v1.3.0)". Do not inline the template here — it lives in the phase body file so bilingual audit greps have a single target.

After printing the box, wait for the user's next conversational turn. Do not prompt, do not block, do not spin a loading indicator — the welcome box is itself the invitation. The user's next message (text, text + attached files, text + URL, or any combination) feeds the acknowledgement step below.

## Phase 0 — mirror

When the user's response arrives, extract the 9-field intent schema from the dropped content (text, PDFs, images, URLs — all read via multimodal) and render the mirror template from `phase-0-welcome.md § "Mirror template — FR (v1.3.1, printed by default)"`. Reveal rows progressively (Ably token-streaming pattern).

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

**Zero-content branch**: if the user's response contains only the trigger phrase with no content, do NOT print the `◐` line or the table. Instead re-prompt `Je t'écoute — dépose ou écris ce que tu veux me partager.` and wait for the user's next turn. No `✓` closure in that branch.

**Unreadable-attachment branch**: if Claude cannot read an attached file (exotic binary, oversize PDF past the 32 MB × 600 pages Files API limits), the `Depose` / `Dropped` row lists it alongside readable items: `Depose        1 brief "X" + 1 fichier illisible : <filename>`. Extraction of the other 8 fields continues from readable content.

**Truncation**: each row value ≤ 60 chars after the label. Longer → truncate at 57 + `...`. `Depose` lists at most 3 items; beyond 3, append `+ N autres`.

**Schema persistence**: v1.3.1 holds the schema in Claude's conversational context only — no disk write, no JSON serialization, no external consumer. v1.3.2+ persists to `bootstrap_intent.md` for handoff to `genesis-protocol`.

## Phase 0 — bridge

After the mirror's `✓ Lu et compris.` line prints (or after the zero-content re-prompt receives a follow-up and the mirror has then rendered), print the bridge message from `phase-0-welcome.md § "Bridge message (v1.3.1 — both languages always printed)"`. Always both languages, because v1.3.1 still has no runtime locale detection.

After the bridge prints, the skill exits cleanly — control returns to the normal Claude Code conversation.

## Concentrated privilege

The concentrated privilege of `genesis-drop-zone` in **v1.3.0 and v1.3.1** is **`none`**.

Precedent: `journal-system` declared `none` in `memory/master.md`'s concentrated-privilege map. The welcome + mirror + bridge slice writes nothing to disk, runs no subprocess, makes no network call, invokes no Anthropic API. Claude reads user-attached files via its native multimodal context — a harness-level capability, not a skill privilege. In-context extraction in v1.3.1 uses the same multimodal path; the schema lives in conversation memory only.

**Forward note (non-binding)**: v1.3.2+ will introduce the first concentrated privilege for this skill — writing `bootstrap_intent.md` into a user-designated project directory. That ship will carry a consent card, overwrite-protection, and a bilingual confirmation prompt, matching the Layer A discipline of `pepite-flagging`'s per-target consent floor. Declaring that privilege here (before the code that carries it ships) would violate the anti-Frankenstein gate.

## Deferred scope

Ordered by rough priority, non-binding, revisit at each session boundary:

1. API-powered Path A Citations extraction — upgrade v1.3.1's in-context extraction with `citations: {enabled: true}` per `document` block. Surfaces `cited_text` + `document_index` for audit-trail on the mirror. First "external API call" privilege for `genesis-drop-zone`; sequenced alongside or after write + handoff.
2. `bootstrap_intent.md` file write — consent prompt, target directory resolution, UTF-8 encoding, overwrite protection. **First concentrated privilege for the skill.**
3. Handoff to `genesis-protocol` — invoke with `bootstrap_intent.md` available as the Layer B seed (replaces `config.txt` in v2).
4. Runtime locale detection — detect user language from trigger match + message content; switch FR and EN variants dynamically for both welcome and mirror.
5. `GH_BROWSER` profile routing wire-up.
6. UX toolkit integration — `@clack/prompts`, Charm Gum, cli-spinners.
7. Completion chime (cross-platform).
