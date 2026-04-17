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

## Token-streamed acknowledgement template

Reformulates what the user provided in progressive bullets, one per item. Pattern, not verbatim — bullets are filled with the user's own words when possible.

```
 ◐ Je regarde ce que tu m'as donne...
   . <one short phrase per item, using user's own words>
 ✓ J'ai tout lu.
```

Per-item bullet rules:

| Input kind | Bullet template |
|---|---|
| PDF | `. un brief "<user's title>" (PDF, <N pages>)` |
| Image | `. une photo de <what the image shows>` |
| URL | `. un lien vers <domain or content summary>` |
| Free text | `. une idée "<first 8 words verbatim>..."` |

### Zero-content branch

If the user's response contains only the trigger phrase with no content to echo:

```
 Je t'écoute — dépose ou écris ce que tu veux me partager.
```

No `◐ Je regarde...` line, no `✓` closure. The skill then waits for the user's next conversational turn and re-runs the acknowledgement flow.

### Unreadable-attachment branch

If Claude cannot read a file (exotic binary, oversize PDF past the Files API 32 MB × 600 pages limits):

```
   . un fichier que je n'arrive pas a lire : <filename>
     Dis-moi ce qu'il contient en mots ?
```

Graceful, no error code. Surrounding bullets (readable items) print normally; the unreadable-file bullet sits among them.

## Bridge message (bilingual, always both printed)

After the acknowledgement (or after the zero-content re-prompt has received a follow-up and been acknowledged), print this bridge exactly — both languages, always:

```
Extraction et création du projet arrivent bientôt.
Pour l'instant, j'ai bien vu — reviens à Claude Code normalement.

Extraction and project creation are coming soon.
For now, I've seen it — go back to Claude Code normally.
```

The word "bientôt" / "soon" is deliberately time-free. Do not insert a version number or a date — the bridge must stay accurate whether v1.3.1 ships next week or next month.

After the bridge prints, the skill exits cleanly. Control returns to the normal Claude Code conversation.
