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

### Citation annotation format (v1.4.0)

When the v1.4.0 Citations API extraction path ran successfully and a field received a citation, the mirror row suffixes the value with a source annotation. The annotation is language-neutral ASCII — the same format renders under both `content_locale = FR` and `content_locale = EN`.

**Format per citation type**:

- `pdf_page_range` → ` [page N]` (1-indexed page, inclusive range collapses to single page when start == end; ranges print as `[pages N-M]`).
- `text_char_range` → ` [lines X-Y]` where `X` and `Y` are line numbers derived from the character offsets via `\n` counting (1-indexed, inclusive).

Example rendered row (FR variant):

```
   Idee          boulangerie artisanale pour livraison matin [page 1]
```

Example rendered row (EN variant):

```
   Idea          artisan bakery for morning delivery [lines 3-5]
```

**Truncation rule exception**: the v1.3.1 truncation rule (row value ≤ 60 chars, truncate at 57 + `...`) applies to the row *value* before the annotation. When an annotation is appended, the total row may exceed 60 chars — this is the single exception to the truncation rule. Rationale: truncating the annotation hides the audit-trail, which is the whole point of v1.4.0. Annotated rows may reach ~75 characters in the worst case; still within 80-col terminals.

**When no annotation prints**:

- Fallback path fired (API unavailable, subprocess failure, or any of the four fallback triggers per SKILL.md § "Citations API dispatch (v1.4.0) / Fallback triggers").
- Image-only drops — Citations API does not cite images.
- Field received no citation from the API (e.g. inferred rather than directly quoted).

Rows without annotations render exactly as the v1.3.3 mirror — no visible indication that the API path was attempted.

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

## Living memory templates (v1.5.0)

v1.5.0 introduces three new render surfaces (arbitration card, halt-with-remediation card, archive frontmatter) plus extends the disk class to cover archive + supersession writes. Each render surface has a verbatim FR + EN paired-authored template per R9 tier-3 discipline. Frontmatter examples are locale-neutral (English keys; FR canonical null tokens preserved per v1.3.3 data contract).

See `SKILL.md § "Living memory dispatch (v1.5.0)"` for the dispatch logic that consumes these templates.

## Arbitration card — FR variant (rendered when `content_locale = FR`)

```
⚖ Arbitrage requis — <N> divergences detectees

[1] champ=<nom_du_champ_1> [intra-drop]
    candidat 1 : "<valeur 1>" (source : <src 1>)
    candidat 2 : "<valeur 2>" (source : <src 2>)

[2] champ=<nom_du_champ_2> [cross-session]
    valeur actuelle : "<valeur existante>" (source : snapshot existant)
    nouvelle valeur : "<valeur extraite>" (source : nouvelle extraction)

Reponds avec les indices separes par des virgules : "2,1,2" choisit
la valeur 2 pour #1, valeur 1 pour #2, valeur 2 pour #3.
Ou "autre N : <valeur>" pour ecraser #N avec une valeur libre.
Ou "abort" pour quitter sans modification.
```

## Arbitration card — EN variant (rendered when `content_locale = EN`)

```
⚖ Arbitration required — <N> divergences detected

[1] field=<field_name_1> [intra-drop]
    candidate 1: "<value 1>" (source: <src 1>)
    candidate 2: "<value 2>" (source: <src 2>)

[2] field=<field_name_2> [cross-session]
    current value: "<existing value>" (source: existing snapshot)
    new value:     "<extracted value>" (source: new extraction)

Reply with comma-separated indices: "2,1,2" picks value 2 for #1,
value 1 for #2, value 2 for #3.
Or "autre N: <value>" to override #N with a free-form value.
Or "abort" to exit without changes.
```

## Halt-with-remediation card — FR variant (EXIT_NO_KEY = 2)

```
⛔ Genesis necessite une cle API Anthropic

L'extracteur Citations a besoin d'une cle API Anthropic
configuree dans la variable d'environnement ANTHROPIC_API_KEY.

Pourquoi une cle API et pas mon abonnement Claude Max ?
  L'abonnement Claude Max paye claude.ai + Claude Desktop +
  Claude Code CLI (inference). La cle API Anthropic est un
  produit SEPARE, facture au token au niveau workspace, et
  active programmatic Messages API + Citations + Files. Les
  deux sont volontairement distincts (architecture Anthropic
  avril 2026, voir https://console.anthropic.com/settings/keys).

Remediation :

  1. Recupere une cle sur https://console.anthropic.com/settings/keys
     - Cliquer "Create Key" -> nommer "genesis-drop-zone"
     - Role : "Claude Code" (ou "Developer" si "Claude Code"
       n'est pas propose dans ton workspace)
     - Copier la valeur sk-ant-... commencant par sk-ant-

  2. Configure la variable d'environnement de facon PERSISTANTE
     (pas seulement la session courante) :

     Windows (PowerShell elevee, persistant systeme) :
       setx ANTHROPIC_API_KEY "sk-ant-..."

     POSIX (bash/zsh, ajouter au profile shell) :
       echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.zshenv
       (ou ~/.bashrc selon ton shell)

     Ne PAS utiliser uniquement `$env:ANTHROPIC_API_KEY = "..."`
     dans la session Claude Code en cours : un futur release
     Claude Code peut activer `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`
     par defaut, qui retirerait la variable des subprocess.
     setx / .zshenv survivent a ce changement.

  3. Relance Claude Code dans ce dossier (close + reopen)

  4. Reinvoque /genesis-drop-zone

Echapatoires (avance, optionnels) :
  - LLM gateway / proxy : utiliser ANTHROPIC_AUTH_TOKEN au lieu
    de ANTHROPIC_API_KEY (voir docs Anthropic)
  - Secrets rotatifs (vault, AWS Secrets Manager) : configurer
    apiKeyHelper dans ~/.anthropic/config (voir docs Anthropic)

Note : la souscription Claude Code (Max) ne donne PAS acces a
l'API. La cle API Anthropic est un produit separe.
```

## Halt-with-remediation card — EN variant (EXIT_NO_KEY = 2)

```
⛔ Genesis requires an Anthropic API key

The Citations extractor needs an Anthropic API key configured
in the ANTHROPIC_API_KEY environment variable.

Why an API key and not my Claude Max subscription?
  Your Claude Max subscription pays for claude.ai + Claude
  Desktop + Claude Code CLI (inference). The Anthropic API
  key is a SEPARATE product, billed per-token at the
  workspace level, and unlocks programmatic Messages API +
  Citations + Files. The two are intentionally distinct
  (Anthropic architecture, April 2026 — see
  https://console.anthropic.com/settings/keys).

Remediation:

  1. Get a key at https://console.anthropic.com/settings/keys
     - Click "Create Key" -> name it "genesis-drop-zone"
     - Role: "Claude Code" (or "Developer" if "Claude Code"
       is not offered in your workspace)
     - Copy the sk-ant-... value beginning with sk-ant-

  2. Set the environment variable PERSISTENTLY (not just the
     current session):

     Windows (PowerShell elevated, system-wide persistent):
       setx ANTHROPIC_API_KEY "sk-ant-..."

     POSIX (bash/zsh, add to shell profile):
       echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.zshenv
       (or ~/.bashrc depending on your shell)

     Do NOT use only `$env:ANTHROPIC_API_KEY = "..."` in the
     current Claude Code session: a future Claude Code release
     may default-enable `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`,
     which would strip the variable from subprocesses.
     setx / .zshenv survive that change.

  3. Relaunch Claude Code in this folder (close + reopen)

  4. Re-invoke /genesis-drop-zone

Escape hatches (advanced, optional):
  - LLM gateway / proxy: use ANTHROPIC_AUTH_TOKEN instead of
    ANTHROPIC_API_KEY (see Anthropic docs)
  - Rotating secrets (vault, AWS Secrets Manager): configure
    apiKeyHelper in ~/.anthropic/config (see Anthropic docs)

Note: the Claude Code (Max) subscription does NOT grant API
access. The Anthropic API key is a separate product.
```

## Halt-with-remediation card — FR variant (generic internal-error, exits 3-7, v1.5.1 collapsed)

```
⛔ Erreur interne Genesis

L'extracteur Citations a echoue. La cause exacte est dans les
logs stderr (classe d'erreur : SDK_MISSING, API_ERROR, RATE_LIMIT,
BAD_INPUT, ou OUTPUT_INVALID — affichee par l'extracteur).

Remediation :

  1. Capturer les logs stderr de l'invocation qui vient d'echouer.

  2. Pour un diagnostic plus detaille, reinvoquer avec :
       (PowerShell)  $env:GENESIS_DROP_ZONE_VERBOSE = "1"
       (bash)        export GENESIS_DROP_ZONE_VERBOSE=1
     Puis relance /genesis-drop-zone.

  3. Ouvrir un issue avec les logs stderr + la classe d'erreur :
       https://github.com/myconciergerie-prog/project-genesis/issues
     Inclure : version Genesis (`cat .claude-plugin/plugin.json`),
     OS, description du drop (pas le contenu sensible).

  4. Escape hatch temporaire — si l'urgence l'exige, une version
     ulterieure de Genesis pourrait reintroduire le path in-context
     v1.3.3 comme option explicite. v1.5.x n'offre pas ce fallback.

Note : la souscription Claude Code (Max) ne donne PAS acces a
l'API. La cle API Anthropic est un produit separe.
```

## Halt-with-remediation card — EN variant (generic internal-error, exits 3-7, v1.5.1 collapsed)

```
⛔ Genesis internal error

The Citations extractor failed. The precise cause is in the
stderr logs (error class: SDK_MISSING, API_ERROR, RATE_LIMIT,
BAD_INPUT, or OUTPUT_INVALID — printed by the extractor).

Remediation:

  1. Capture the stderr logs from the invocation that just failed.

  2. For more detailed diagnostics, re-invoke with:
       (PowerShell)  $env:GENESIS_DROP_ZONE_VERBOSE = "1"
       (bash)        export GENESIS_DROP_ZONE_VERBOSE=1
     Then relaunch /genesis-drop-zone.

  3. File an issue with the stderr logs + error class:
       https://github.com/myconciergerie-prog/project-genesis/issues
     Include: Genesis version (`cat .claude-plugin/plugin.json`),
     OS, drop description (no sensitive content).

  4. Temporary escape hatch — if urgency demands, a future Genesis
     version may reintroduce the v1.3.3 in-context path as an
     explicit opt-in. v1.5.x does not offer this fallback.

Note: the Claude Code (Max) subscription does NOT grant API
access. The Anthropic API key is a separate product.
```

## Archive frontmatter examples (locale-neutral — keys are English)

The three new v1.5.0 frontmatter keys (`snapshot_version`, `arbitrated_fields`, `supersedes_snapshot`) are added to existing v1.4.0 schema (schema_version stays at `1`, additive only). FR canonical null tokens preserved.

**First write (v1.5.0 fresh)**:

```yaml
schema_version: 1
created_at: 2026-04-19T15:30:00Z
skill: genesis-drop-zone
skill_version: "1.5.0"
snapshot_version: 1
arbitrated_fields: []
# ... 9 semantic fields ...
# ... optional <field>_source_citation entries ...
```

**Supersession write (v2 of the snapshot, after Phase 0.5 arbitration)**:

```yaml
schema_version: 1
created_at: 2026-04-19T16:00:00Z
skill: genesis-drop-zone
skill_version: "1.5.0"
snapshot_version: 2
arbitrated_fields: [pour_qui, budget_ou_contrainte]
supersedes_snapshot: ./drop_zone_intent_history/v1_20260419T153000Z.md
# ... 9 semantic fields (with arbitrated values) ...
```

**Archived predecessor frontmatter (after supersession, augmented at archive time)**:

```yaml
schema_version: 1
created_at: 2026-04-19T15:30:00Z
skill: genesis-drop-zone
skill_version: "1.5.0"
snapshot_version: 1
arbitrated_fields: []
status: deprecated
archived_at: 2026-04-19T16:00:00Z
superseded_by: ../drop_zone_intent.md
supersession_reason: cross-session re-extraction
# ... 9 semantic fields (original values) ...
```
