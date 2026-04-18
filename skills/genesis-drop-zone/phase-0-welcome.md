<!-- SPDX-License-Identifier: MIT -->

# Phase 0 — welcome runtime templates

This file holds the runtime string templates printed by `genesis-drop-zone` during its welcome → acknowledgement → bridge flow. Dev/tooling structure around the strings stays English per R9; the strings themselves are bilingual FR + EN coauthored day 1.

**v1.3.3 runtime locale dispatch**: each user-facing surface renders exactly one locale variant per invocation based on one of two variables — `welcome_locale` (set at skill invocation from the trigger phrase language; defaults to FR on slash) for the welcome box and zero-content re-prompt, or `content_locale` (set from extracted `langue_detectee`, with `mixte` → FR tiebreaker) for the mirror, consent card, halt message, and bridges. See `SKILL.md § "Locale dispatch (v1.3.3)"` for the full two-variable model and render-target map.

## FR welcome box (rendered when `welcome_locale = FR`)

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

Plain-ASCII FR text inside the box by design: Unicode box-drawing combines unstably with combining diacritics on some Windows code-page configurations. The bridge and context-guard redirect (below / in `SKILL.md`) keep their accents because they are plain-prose lines routed through the terminal's UTF-8-stable stream path.

## EN welcome box (rendered when `welcome_locale = EN`)

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

## Mirror template — FR (rendered when `content_locale = FR`)

Reformulates what the user dropped as a 9-row aligned-column table. Each field in the extraction schema renders as one row, revealed progressively per the Ably 2026 token-streaming pattern. **v1.3.3**: dispatched on `content_locale` — FR variant when `content_locale = FR` (from `langue_detectee ∈ {FR, mixte}`).

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

### Alignment and rendering rules

- Labels padded to 14 characters (left-aligned), 2-space separator, value flows right.
- **ASCII pure inside the table block** — no accents in label or value rows (v1.3.0 rule preserved for Windows code-page stability). Accents are allowed in the `◐ Je regarde...` opening line, the `✓ Lu et compris.` closing line, and prose values only when genuinely needed (rare — the mirror is factual, not prose). All three routes through the UTF-8-stable stream path.
- Row reveal is **token-streamed** one-by-one. `◐` stays visible until the 9th row renders, then `✓` closes.
- No blocking spinner, no blank screen. Welcome box's rendering is the only moment with no partial output.

### Per-field rules

| Field | Label FR | Null-class when missing |
|---|---|---|
| `idea_summary` | Idee | class 1 degenerate: `a trouver ensemble` (mirror only fires when content non-zero) |
| `pour_qui` | Pour qui | `a trouver ensemble` (core) |
| `type` | Type | `a trouver ensemble` (core) |
| `nom` | Nom | `a trouver ensemble` (core) |
| `attaches` | Depose | `texte seul` if no attachment; else list 3 items + `+ N autres` beyond |
| `langue_detectee` | Langue | always filled: `FR` / `EN` / `mixte` |
| `budget_ou_contrainte` | Budget | `non mentionne` (bonus) |
| `prive_ou_public` | Visibilite | `non mentionnee` (bonus) |
| `hints_techniques` | Tech | `non mentionne` (bonus) |

### Truncation rules

- Each row value ≤ 60 chars after label; truncate at 57 + `...`.
- `Depose` lists at most 3 items; beyond 3, append `+ N autres`.
- `Idee` value: user's own words when possible; condense paragraph to ≤ 60 chars. Full content kept in Claude's context (v1.3.2+ handoff).

### Ambiguity branch

If the content supports multiple interpretations on a field:

```
   Type          a affiner — boulangerie ou restaurant
```

`a affiner` is the third null-class label alongside `a trouver ensemble` and `non mentionne(e)`.

### Zero-content branch (v1.3.0 preserved, v1.3.3 locale-switched)

If the user's response contains only the trigger phrase with no content to echo, the skill prints the zero-content re-prompt. **v1.3.3** dispatches on `welcome_locale` (content has not been extracted yet, so `content_locale` is not resolved).

FR variant (rendered when `welcome_locale = FR`):

```
 Je t'écoute — dépose ou écris ce que tu veux me partager.
```

EN variant (rendered when `welcome_locale = EN`, **newly-authored in v1.3.3**):

```
 I'm listening — drop or write whatever you want to share.
```

No `◐`, no mirror, no `✓`. Skill waits for user's next turn and re-runs the mirror flow when content arrives. When content eventually arrives, `content_locale` is resolved from `langue_detectee` and subsequent surfaces (mirror, consent card, halt, bridges, body echo) render in that locale — independent of `welcome_locale`.

### Unreadable-attachment branch

If Claude cannot read an attached file (exotic binary, oversize PDF > 32 MB × 600 pages), the `Depose` row lists the file alongside readable items:

```
   Depose        1 brief "X" + 1 fichier illisible : <filename>
```

Extraction of the other 8 fields continues from readable content. Graceful, no error code.

## Mirror template — EN (rendered when `content_locale = EN`)

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

Per-field labels EN (matching FR row-for-row):

| Field | Label EN | Null-class when missing |
|---|---|---|
| `idea_summary` | Idea | `to be found together` |
| `pour_qui` | Who for | `to be found together` |
| `type` | Kind | `to be found together` |
| `nom` | Name | `to be found together` |
| `attaches` | Dropped | `text only` if no attachment |
| `langue_detectee` | Language | always filled |
| `budget_ou_contrainte` | Budget | `not mentioned` |
| `prive_ou_public` | Visibility | `not mentioned` |
| `hints_techniques` | Tech | `not mentioned` |

Same alignment, truncation, and branch rules as the FR variant.

## Bridge message (v1.3.1 — both languages always printed)

> **v1.3.2 supersession**: the v1.3.1 bridge below is preserved as regression-set context. At runtime in v1.3.2, this bridge is replaced by the two version-scoped bridges in §"Accept bridge (v1.3.2)" and §"Decline bridge (v1.3.2)" further down. v1.3.1 installations still use the bridge below; v1.3.2 installations never reach it.

v1.3.0's bridge claimed "Extraction et création… arrivent bientôt" — that became false as of v1.3.1 since extraction now runs. The v1.3.1 bridge reflects that extraction is done and only the project's actual creation (GitHub repo, files on disk, memory system) remains deferred:

```
Création du projet (GitHub, fichiers, mémoire) arrive bientôt.
Pour l'instant, j'ai lu et compris — reviens à Claude Code normalement.

Project creation (GitHub, files, memory) is coming soon.
For now, I've read and understood — go back to Claude Code normally.
```

"Creation du projet" enumerates its three concrete deliverables (GitHub repo / files / memory) — promise is tangible, not abstract. "J'ai lu et compris" replaces v1.3.0's "j'ai bien vu" — catalogue becomes comprehension. "Bientôt" / "soon" stays time-free.

**Accent discipline**: bridge is plain-prose, non-table content routed through the UTF-8-stable stream path — **keeps its accents** (`é`, `ô`, `à`, `—`). ASCII-only rule applies only to table content (welcome box and mirror rows). Same asymmetry as v1.3.0.

After the bridge prints, the skill exits cleanly. Control returns to the normal Claude Code conversation.

## Consent card (v1.3.2, v1.3.3 locale-switched)

Printed between the mirror's `✓ Lu et compris.` / `✓ Read and understood.` line and the write. Gates the first Layer A concentrated privilege (writing `drop_zone_intent.md` to cwd). The `<absolute-cwd-path>` placeholder is resolved at prompt time via the runtime's current working directory — path separator follows platform convention (`\` on Windows, `/` elsewhere). **v1.3.3 dispatch**: v1.3.2 printed both FR and EN blocks always; v1.3.3 prints only the variant matching `content_locale`.

### FR variant (rendered when `content_locale = FR`)

```
Je peux noter ton projet dans un fichier ici :
  → <absolute-cwd-path>/drop_zone_intent.md

Ce fichier sera le point de départ pour Claude Code la prochaine fois.
On le garde comme ça ?  (oui pour l'écrire, non pour annuler)
```

### EN variant (rendered when `content_locale = EN`)

```
I can save your project here:
  → <absolute-cwd-path>/drop_zone_intent.md

This file becomes Claude Code's starting point next time.
Keep it this way?  (yes to write, no to cancel)
```

### Response routing (natural-language)

Three equivalence classes on the next user turn:

1. **Affirmative** — `oui`, `yes`, `y`, `ok`, `d'accord`, `go`, `garde`, `écris`, `save`, `keep`. Proceed to write flow.
2. **Negative** — `non`, `no`, `n`, `cancel`, `annule`, `abort`, `stop`, `nope`. Proceed to decline flow.
3. **Modification** — the user asks to change a mirror field (`garde Type en boulangerie`, `le nom c'est VelyzyBake`). Re-run the 9-field extraction with the correction, re-render the mirror with updated rows, re-print this consent card. Loop until convergence to class 1 or 2. No iteration cap — the card is the only gate out.

### Accent discipline

Plain-prose bilingual — accents allowed (`é`, `à`, `ê`, `ô`). Same UTF-8-stable stream path as the v1.3.1 bridge. The arrow marker `→` is U+2192, UTF-8-stable on both terminals. Not inside a table/box fence.

## Halt message (v1.3.2, v1.3.3 locale-switched)

Printed **in place of** the consent card when the pre-write existence check detects a `drop_zone_intent.md` already in cwd. The skill exits clean after printing this — no overwrite, no timestamp-suffix fallback, no second consent. Matches the halt-on-leak precedent of `session-post-processor`. **v1.3.3 dispatch**: v1.3.2 printed both FR and EN blocks always; v1.3.3 prints only the variant matching `content_locale`.

### FR variant (rendered when `content_locale = FR`)

```
Un fichier `drop_zone_intent.md` existe déjà ici :
  → <absolute-cwd-path>/drop_zone_intent.md

Supprime-le d'abord, ou ouvre Claude Code dans un autre dossier et relance.
```

### EN variant (rendered when `content_locale = EN`)

```
A `drop_zone_intent.md` already exists here:
  → <absolute-cwd-path>/drop_zone_intent.md

Delete it first, or open Claude Code in a different folder and retry.
```

Plain-prose, same accent discipline as the consent card (each variant preserves accents where applicable).

## Accept bridge (v1.3.2, v1.3.3 locale-switched)

Printed after a successful `drop_zone_intent.md` write. Instructs the user on the next step (type `/genesis-protocol`). Path **not repeated** — the consent card rendered above already showed the absolute path. **v1.3.3 dispatch**: v1.3.2 printed both FR and EN blocks always; v1.3.3 prints only the variant matching `content_locale`.

### FR variant (rendered when `content_locale = FR`)

```
C'est noté — tape `/genesis-protocol` quand tu es prêt pour créer
le projet (GitHub, fichiers, mémoire) à partir de ce fichier.
```

### EN variant (rendered when `content_locale = EN`)

```
Saved — type `/genesis-protocol` when you're ready to create the
project (GitHub, files, memory) from this file.
```

"C'est noté" / "Saved" — past-tense, signals the write has completed. `/genesis-protocol` in backticks signals the slash-command.

## Decline bridge (v1.3.2, v1.3.3 locale-switched)

Printed after the user declines the consent card (class-2 response). No write occurred; skill exits clean. **v1.3.3 dispatch**: v1.3.2 printed both FR and EN blocks always; v1.3.3 prints only the variant matching `content_locale`.

### FR variant (rendered when `content_locale = FR`)

```
OK, rien d'écrit. Ton idée reste dans notre échange pour l'instant.
Relance-moi quand tu veux la poser sur disque.
```

### EN variant (rendered when `content_locale = EN`)

```
OK, nothing written. Your idea stays in our exchange for now.
Come back whenever you want to save it to disk.
```

Warm, non-pressurizing — the idea isn't lost, it's simply not persisted.
