<!-- SPDX-License-Identifier: MIT -->
---
name: session-post-processor / verification
description: Two-mode health card emitted by the skill — post-install (directory + INDEX + Python runtime) and post-action (archive written, redaction gate passed, INDEX updated). Halt-on-RED on any redaction leak.
---

# Verification

The skill's verification runs in two modes. Both follow the same GREEN / YELLOW / RED status convention from `phase-5-5-auth-preflight/verification.md` and `journal-system/verification.md`, with the same halt-on-RED discipline.

**The post-action mode has one critical check that no other skill has**: the redaction gate. Any pattern hit on the written archive file deletes the file immediately and blocks the user from re-running without an audit.

## Post-install health check

Run these checks in order after `install-manifest.yaml` executes.

### Check 1 — Python 3.10+ available

```
python --version                          [ OK / MISSING / TOO_OLD ]
```

- **OK** (3.10+) → continue
- **MISSING** → tell the user: *"Python 3.10+ is required. Install via the `phase-minus-one` skill if not already on the machine, or install manually via OS package manager."*
- **TOO_OLD** (3.9 or earlier) → tell the user: *"Python version too old. Upgrade to 3.10+."*

This is the only skill in the Genesis stack so far with a non-trivial runtime dependency. The check must be explicit.

### Check 2 — `memory/project/sessions/` exists

```
memory/project/sessions/ exists           [ OK / MISSING ]
```

- **OK** → continue
- **MISSING** → re-run `install-manifest.yaml` first step. Surface the filesystem error to the user if the re-run fails.

### Check 3 — `memory/project/sessions/INDEX.md` exists

```
memory/project/sessions/INDEX.md exists   [ OK / MISSING ]
```

- **OK** → continue
- **MISSING** → re-run the install step, or create from the `install-manifest.yaml` template manually.

### Check 4 — INDEX has the "Archives" section

```
INDEX has `## Archives`                   [ OK / MISSING ]
```

- **OK** → post-install is GREEN
- **MISSING** → a previous session customised the INDEX. Do **not** overwrite it. Ask the user whether to migrate to the standard template or keep the custom layout. The skill works either way — the section is a convenience, not a hard requirement.

### Check 5 — Source JSONL directory reachable

```
~/.claude/projects/<slug>/*.jsonl discoverable   [ OK / MISSING ]
```

- **OK** (at least one JSONL for the current project slug) → post-install GREEN
- **MISSING** (no JSONL for the current slug) → YELLOW, not RED — the install is still valid, but the skill cannot archive anything until the session runs its first tool call and the JSONL is written. Surface: *"No JSONL transcript yet for this project slug. The skill will work on the next session that produces tool calls."*

## Post-action health check

Run these after a trigger-phrase invocation writes an archive to disk.

### Check 6 — Target JSONL located

```
Source JSONL picked                       [ OK / AMBIGUOUS / NONE ]
```

- **OK** → continue with the located file path logged
- **AMBIGUOUS** (multiple JSONL with similar mtimes in the slug directory) → YELLOW, stop and ask the user which file to process
- **NONE** → RED, halt. Surface: *"No JSONL transcript found for slug `<slug>` under `~/.claude/projects/`. Either the session hasn't produced any tool calls yet, or the slug derivation is wrong."*

### Check 7 — Parser completed without fatal error

```
Parser finished                           [ OK / PARTIAL / FAILED ]
```

- **OK** → continue
- **PARTIAL** (some lines were malformed and skipped) → YELLOW, log the skipped count, continue. Surface in the health card: *"<N> malformed lines skipped during parse — archive is still usable but incomplete."*
- **FAILED** (exception in the parser itself, not a malformed line) → RED, halt. Surface the exception trace. Do not proceed to the redaction step.

### Check 8 — Redaction pass completed

```
Redaction pass completed                  [ OK / FAILED ]
redaction hit counts logged               [ OK / MISSING ]
```

- **OK** → continue with the hit count dict in the health card
- **FAILED** → RED, halt. Surface: *"Redaction pass errored before completing. Archive not written. Audit the redaction pattern set for syntax issues."*

### Check 9 — Archive file written

```
<target-path>.md exists                   [ OK / MISSING ]
size > 0                                  [ OK / EMPTY ]
parseable as markdown                     [ OK / INVALID ]
```

- **All OK** → continue
- **MISSING** → RED, halt. The write failed silently. Surface the expected path.
- **EMPTY** → RED, halt. The emitter produced nothing. Surface: *"Emitter wrote a zero-byte file. Archive deleted."* Delete the file.
- **INVALID** (frontmatter doesn't parse as YAML, or the Markdown structure is broken) → RED, halt. Delete the file.

### Check 10 — **Halt-on-leak redaction gate** (CRITICAL)

This is the skill's security floor.

```
Re-apply every pattern to the written file:
  ssh_private_key_block                   [ CLEAN / LEAK ]
  github_pat_finegrained                  [ CLEAN / LEAK ]
  github_classic_token                    [ CLEAN / LEAK ]
  anthropic_api_key                       [ CLEAN / LEAK ]
  openai_api_key                          [ CLEAN / LEAK ]
  supabase_pat                            [ CLEAN / LEAK ]
  supabase_secret_key                     [ CLEAN / LEAK ]
  stripe_secret_key                       [ CLEAN / LEAK ]
  aws_access_key                          [ CLEAN / LEAK ]
  google_api_key                          [ CLEAN / LEAK ]
  jwt_token                               [ CLEAN / LEAK ]
  env_local_paste                         [ CLEAN / LEAK ]
  generic_long_hex                        [ CLEAN / LEAK ]
  generic_long_base64                     [ CLEAN / LEAK ]
```

- **All CLEAN** → continue to INDEX update
- **Any LEAK** → **RED, CRITICAL**:
  1. Log the pattern name and hit count (never the match content)
  2. **Delete the archive file immediately**
  3. Surface to the user:
     > *"Archive halted — pattern `<name>` leaked through redaction (N hits). File deleted. Audit the redaction set in `redaction-patterns.md` and strengthen the pattern before retrying. Do NOT re-invoke the skill until the pattern is fixed."*
  4. **Do not retry automatically**. A silent retry would hide the incident.
  5. Exit with RED status. The user fixes the pattern set and manually re-invokes.

This is the single most important check in the whole skill. Every other check is a convenience; this one is a security gate. Treat it as such.

### Check 11 — INDEX updated

```
memory/project/sessions/INDEX.md reflects the new archive   [ OK / MISSING / DUPLICATE ]
```

- **OK** → continue
- **MISSING** → append the one-line entry. Not a halt — a missing INDEX line is cosmetic, not a security issue.
- **DUPLICATE** (line for the same file already present) → update in place, do not add a second line.

### Check 12 — No tmp files left behind

```
No `<target-path>.tmp` or `.bak` file remaining             [ OK / DIRTY ]
```

- **OK** → post-action GREEN
- **DIRTY** → YELLOW, delete the tmp / bak file. The write was atomic in theory but the cleanup may have been skipped.

## Output format — the health card

```markdown
## Session post-processor health — <YYYY-MM-DD HH:MM>

**Mode**: post-install | post-action
**Source**: `<path-to-jsonl>`                              (post-action only)
**Archive**: `memory/project/sessions/<YYYY-MM-DD>_<slug>.md`   (post-action only, only if passed)

### Environment
| Check | Result |
|---|---|
| Python 3.10+ | OK |
| sessions/ directory | OK |
| INDEX.md | OK |
| Source JSONL | OK |

### Processing (post-action only)
| Check | Result |
|---|---|
| Parser | OK (174 records, 0 malformed) |
| Redaction pass | OK (12 hits across 2 patterns) |
| Archive written | OK (23 KB, 8 turns) |
| Halt-on-leak gate | CLEAN (14/14 patterns verified) |
| INDEX updated | OK |
| Tmp cleanup | OK |

### Redaction hit detail
| Pattern | Hits |
|---|---|
| github_pat_finegrained | 8 |
| env_local_paste | 4 |

**Status**: GREEN

**Next steps**: archive ready for manual review. After three successful archives, `SessionEnd` hook wiring becomes a v0.6+ candidate.
```

## Three possible Status values

- **GREEN** — every check passed. Archive exists, no leaks, INDEX updated, user can commit the file.
- **YELLOW** — at least one non-critical check failed (source JSONL missing at install-time, partial parse with some malformed lines, no source slug yet, INDEX line drift). Skill still produced a valid archive OR the install is still valid. Surface the issues but do not halt.
- **RED** — a critical check failed (parser exception, emitter wrote nothing, **redaction leak**, archive invalid). Halt immediately. If the archive exists, delete it. Surface the incident to the user with the exact failure and the required audit action. **Never continue past RED.**

## Dogfood run expectations

The v0.5.0 session (this session, which ships the skill) should pass all checks when the skill is manually invoked on its own JSONL:

- Source JSONL: `~/.claude/projects/C--Dev-Claude-cowork-project-genesis/b13b44b1-59a0-4d1d-bad1-1272867fcfe8.jsonl` (or whatever the current session UUID is at invocation time)
- Redaction hits expected:
  - `github_pat_finegrained`: non-zero (the session sourced `.env.local` multiple times for `GH_TOKEN` env override)
  - `env_local_paste`: non-zero (same reason)
  - Other patterns: likely zero, but non-zero is fine
- Halt-on-leak gate: must be **CLEAN**. If the gate fires on the dogfood run, the pattern set or the redactor is broken and the v0.5.0 release is blocked until fixed.

## Anti-Frankenstein reminder

Verification is a read-only surface except for **the halt-on-leak file deletion**. Every other failure is reported; only the leak is acted upon. Treat that deletion as the single privileged operation of this skill — it exists to prevent a worse outcome (a secret persisted to the repo).

Do not auto-fix redaction patterns, do not retry the archive silently, do not disable the gate "just this once". The gate is the reason the skill can be trusted to run on every session.
