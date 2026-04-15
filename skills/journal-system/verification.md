<!-- SPDX-License-Identifier: MIT -->
---
name: journal-system / verification
description: Final health card emitted by the skill after install or after any trigger-phrase action. Confirms the journal wiring is healthy and the last write succeeded.
---

# Verification

This card runs in two modes:

1. **Post-install** — after `install-manifest.yaml` creates `memory/journal/` and `INDEX.md`, confirm both exist and the INDEX has the five state sections.
2. **Post-action** — after any trigger-phrase flow (`ouvre`, `reprends`, `enregistre`, `enrichis`, `clôture`), confirm the target entry was written correctly and the INDEX reflects the change.

The card is short by design. Its job is to surface failures loudly, not to narrate success.

## Post-install health check

Run these checks in order. Stop at the first failure and surface it to the user; do not silently continue.

### Check 1 — directory exists

```
memory/journal/ exists                  [ OK / MISSING ]
```

- **OK** → continue.
- **MISSING** → the install-manifest did not run, or the filesystem rejected the create. Re-run `install-manifest.yaml`. If that fails, ask the user to check `memory/` permissions.

### Check 2 — INDEX exists

```
memory/journal/INDEX.md exists          [ OK / MISSING ]
```

- **OK** → continue.
- **MISSING** → re-run the install step. If the directory exists but INDEX does not, the install-manifest's `create_if_missing_only` guard may have mis-fired; copy the template from `install-manifest.yaml` manually.

### Check 3 — INDEX has the five state sections

```
INDEX has `## Growing`                  [ OK / MISSING ]
INDEX has `## Seed`                     [ OK / MISSING ]
INDEX has `## Captured`                 [ OK / MISSING ]
INDEX has `## Dormant`                  [ OK / MISSING ]
INDEX has `## Resolved`                 [ OK / MISSING ]
```

- **All OK** → post-install health is GREEN.
- **Any MISSING** → a previous session customised the INDEX. Do **not** overwrite it. Ask the user whether to migrate the custom INDEX to the 5-section template or keep the custom layout. The skill works either way — the sections are a convenience, not a hard requirement.

## Post-action health check

After a trigger-phrase flow writes to disk, run these.

### Check 4 — target file exists

```
memory/journal/<YYYY-MM-DD>_<slug>.md exists    [ OK / MISSING ]
```

- **OK** → continue.
- **MISSING** → the write failed. Surface the filesystem error to the user. Do NOT retry silently; ask before the second attempt.

### Check 5 — frontmatter is valid

```
frontmatter parseable                   [ OK / FAIL ]
required fields present                 [ OK / FAIL ]
  - name
  - description
  - type (must be "journal")
  - state (one of: captured, seed, growing, dormant, resolved)
  - opened_at (YYYY-MM-DD)
  - last_developed (YYYY-MM-DD)
  - keywords
  - project_context
```

- **All OK** → continue.
- **Any FAIL** → the template rendering dropped a field. Re-open the file, patch the missing field, re-verify.

### Check 6 — user's verbatim quote preserved

```
the first `## Seed` or `## Layer N` contains a `> ` blockquote  [ OK / MISSING ]
the blockquote content matches the user's message              [ OK / MODIFIED ]
```

- **OK** → continue.
- **MISSING** → the skill failed to capture the user's words verbatim. Critical bug — halt and surface to the user.
- **MODIFIED** → the skill paraphrased the user. Critical violation of Rule 2. Halt, restore the verbatim quote, and flag the incident in `memory/feedback/` for future discipline.

### Check 7 — INDEX reflects the change

```
INDEX line for <entry> is present       [ OK / MISSING ]
INDEX line is in the correct state section   [ OK / WRONG ]
```

- **OK** → continue.
- **MISSING** → the INDEX update was skipped. Append the line.
- **WRONG** → a state transition happened (e.g. `seed` → `growing`) but the INDEX still lists the entry under the old section. Move the line to the new section. Do not leave duplicates.

### Check 8 — amplification attribution (only if an amplification was written this turn)

```
amplification section has `### Amplification — Claude, YYYY-MM-DD (consent-based)` header   [ OK / FAIL ]
user consented this turn                 [ OK / MISSING ]
```

- **Both OK** → health is GREEN.
- **Header FAIL** → the attribution is malformed. Fix the header per Rule 3. Non-negotiable — the reader must always know whose voice they are reading.
- **Consent MISSING** → CRITICAL violation of Rule 1. The amplification was auto-written without asking. Halt, delete the amplification sub-section, and flag the incident.

## Output format — the health card

Emit a single Markdown block that the user can scan in under five seconds:

```markdown
## Journal system health — <YYYY-MM-DD HH:MM>

**Mode**: post-install | post-action
**Entry**: `memory/journal/<YYYY-MM-DD>_<slug>.md` (post-action only)

| Check | Result |
|---|---|
| Directory exists | OK |
| INDEX exists | OK |
| INDEX has 5 state sections | OK |
| Target file exists | OK |
| Frontmatter valid | OK |
| Verbatim quote preserved | OK |
| INDEX reflects change | OK |
| Amplification attribution | OK (or N/A if no amplification this turn) |

**Status**: GREEN

**Next steps**: <one line — usually "ready for next trigger phrase" or "journal capture complete">
```

Three possible `Status` values:

- **GREEN** — every check passed, journal is healthy, user can keep working.
- **YELLOW** — at least one non-critical check failed (e.g. missing state section in INDEX). Skill still works but a cleanup is advisable.
- **RED** — a critical check failed (verbatim modified, amplification without consent, target file missing). Halt the flow and surface the specific failure. Never continue past a RED status.

## Anti-Frankenstein reminder

Verification is a read-only surface. It does **not** silently fix issues, does **not** run migrations, does **not** reformat the INDEX. It reports. If something needs fixing, the user sees the report and decides what to do. The skill does not act on its own.
