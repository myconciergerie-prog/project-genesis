<!-- SPDX-License-Identifier: MIT -->

# Phase 0 — welcome runtime templates

This file holds the runtime string templates printed by `genesis-drop-zone` during its welcome → acknowledgement → bridge flow. Dev/tooling structure around the strings stays English per R9; the strings themselves are bilingual FR + EN coauthored day 1. FR variants are printed by default in v1.3.0 — runtime locale selection is deferred to v1.3.1+.

## FR welcome box (printed by default in v1.3.0)

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

## EN welcome box (mirror-ready, not printed in v1.3.0)

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

## Mirror template — FR (v1.3.1, printed by default)

Reformulates what the user dropped as a 9-row aligned-column table. Each field in the extraction schema renders as one row, revealed progressively per the Ably 2026 token-streaming pattern. FR is the default rendering in v1.3.1 (runtime locale detection deferred v1.3.2+).

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

### Zero-content branch

If the user's response contains only the trigger phrase with no content to echo:

```
 Je t'écoute — dépose ou écris ce que tu veux me partager.
```

No `◐`, no mirror, no `✓`. Skill waits for user's next turn and re-runs the mirror flow when content arrives. (v1.3.0 branch preserved unchanged.)

### Unreadable-attachment branch

If Claude cannot read an attached file (exotic binary, oversize PDF > 32 MB × 600 pages), the `Depose` row lists the file alongside readable items:

```
   Depose        1 brief "X" + 1 fichier illisible : <filename>
```

Extraction of the other 8 fields continues from readable content. Graceful, no error code.

## Mirror template — EN (v1.3.1, mirror-ready, not printed in v1.3.1)

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
