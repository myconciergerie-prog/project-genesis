<!-- SPDX-License-Identifier: MIT -->
---
name: genesis-drop-zone
description: Layer A conversational front door for Genesis v2 project bootstrap — print the unified drop-zone welcome box, reformulate what the user gave in a token-streamed acknowledgement, close with an honest bilingual bridge. Invoked by the slash command /genesis-drop-zone or by natural-language intent phrases ("je veux créer un projet", "nouveau projet", "démarre un projet", "dis-moi comment commencer", "I want to create a project", "start a new project", "new project"). Only fires in a fresh context (no existing project in cwd) — inside an active project the skill prints a bilingual redirect and exits.
---

# Genesis Drop Zone

## Purpose

Genesis v1 is an engineer's protocol that speaks to engineers. The v2 vision adds a conversational Layer A where a non-technical user can open Claude Code, drop an idea in any form (text, PDF, photo, link, audio), and be met by a warm conversational surface instead of a config file. `genesis-drop-zone` is the first Layer A skill. In v1.3.0 it ships a vertical slice — welcome, acknowledgement, bridge — that demonstrates the surface without yet wiring the downstream bootstrap engine. Extraction into `bootstrap_intent.md` and handoff to `genesis-protocol` are deferred to v1.3.1+.

**Canonical spec**: `.claude/docs/superpowers/specs/v2_etape_0_drop_zone.md`. This `SKILL.md` is a 1:1 mirror of that spec for the eight sections tagged `Mirrored`. Spec-only sections (problem statement, UX canon backing, R9 tier map, R8 citations, verification scenarios, relation to the vision doc) live in the spec alone. When either file changes, the other follows — drift is a merge-blocker per cross-skill-pattern #1.

## Scope

### In scope (v1.3.0)

1. New sibling skill package `skills/genesis-drop-zone/` with this `SKILL.md` + `phase-0-welcome.md`.
2. Welcome ASCII box template, FR primary and EN mirror — both coauthored day 1 per R9. FR printed by default in v1.3.0.
3. Token-streamed acknowledgement template — pattern (not verbatim), reformulates text / PDFs / images / URLs in progressive bullets.
4. Bilingual bridge message closing the interaction honestly.
5. Trigger evaluation gate — slash + bilingual natural-language triggers + context guard.
6. Concentrated privilege declaration: `none`.

### Out of scope (deferred to v1.3.1+)

- Structured extraction of user intent into a target schema.
- Writing `bootstrap_intent.md` into any directory.
- Handoff to `genesis-protocol` Phase 0.
- Runtime locale detection (FR vs EN selection).
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

## Phase 0 — acknowledgement

When the user's response arrives, reformulate what they gave as a progressive list of short bullets, one per item. Follow the token-streamed pattern declared in `phase-0-welcome.md` § "Token-streamed acknowledgement template". The pattern is:

```
 ◐ Je regarde ce que tu m'as donne...
   . <one bullet per item, in the user's own words when possible>
 ✓ J'ai tout lu.
```

- PDFs → `. un brief "<title>" (PDF, <N pages>)` (use the user's title words, not the filename).
- Images → `. une photo de <what the image shows>`.
- URLs → `. un lien vers <domain or summary>`.
- Free text → `. une idée "<first 8 words verbatim>..."`.

**Zero-content branch**: if the user's response contains only the trigger phrase with no follow-up content, do not print the `◐` line. Instead re-prompt: `Je t'écoute — dépose ou écris ce que tu veux me partager.` No `✓` closure in that branch.

**Unreadable-attachment branch**: if Claude cannot read a file (exotic binary, oversize PDF past the 32 MB × 600 pages Files API limits), the bullet becomes `. un fichier que je n'arrive pas a lire : <filename> / Dis-moi ce qu'il contient en mots ?` — graceful, no error code.

## Phase 0 — bridge

After `✓ J'ai tout lu.` (or the re-prompt in the zero-content branch, once the user replies), print the bridge message from `phase-0-welcome.md` § "Bridge message". Always both languages, because v1.3.0 has no locale detection and will not silently strand non-French-native users.

After the bridge prints, exit cleanly — control returns to the normal Claude Code conversation.

## Concentrated privilege

The concentrated privilege of `genesis-drop-zone` in v1.3.0 is **`none`**.

Precedent: `journal-system` declared `none` in `memory/master.md`'s concentrated-privilege map. The welcome + acknowledgement + bridge slice writes nothing to disk, runs no subprocess, makes no network call. Claude reads user-attached files via its native multimodal context — a harness-level capability, not a skill privilege.

Forward note (non-binding): the v1.3.1+ extraction + `bootstrap_intent.md` write step will introduce one concentrated privilege (writing into a user-designated project directory). That privilege is declared when that code ships, not now. Anticipating it here would violate the "declare privileges for code that exists" anti-Frankenstein gate.

## Deferred scope

Ordered by rough priority, non-binding, revisit at each session boundary:

1. Structured extraction of user intent — Path A (Citations) per `v2_vision_promptor_fusion.md` § "Extraction choice". Writes extracted fields into `bootstrap_intent.md`.
2. `bootstrap_intent.md` file write — consent prompt, target directory resolution, UTF-8 encoding, overwrite protection.
3. Handoff to `genesis-protocol` — invoke `genesis-protocol` with `bootstrap_intent.md` available as the Layer B seed (replaces `config.txt` in v2).
4. Runtime locale detection — detect user language from trigger match + message content; switch between FR and EN variants dynamically.
5. `GH_BROWSER` profile routing wire-up.
6. UX toolkit integration — `@clack/prompts`, Charm Gum, cli-spinners.
7. Completion chime (cross-platform — macOS `afplay`, Windows `[console]::beep`, Linux `paplay`).
