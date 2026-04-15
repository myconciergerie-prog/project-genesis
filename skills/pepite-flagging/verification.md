<!-- SPDX-License-Identifier: MIT -->
---
name: pepite-flagging / verification
description: Two-mode health card emitted by the skill — post-install (directory + INDEX.md + INDEX content) and post-action (entry file valid, frontmatter complete, criteria respected, cross-project pointer writes consented). Halt-on-RED on missing required frontmatter fields, consent bypass, or cross-project write without per-target approval.
---

# Verification

The skill's verification runs in two modes, following the GREEN / YELLOW / RED convention from `phase-5-5-auth-preflight/verification.md`, `journal-system/verification.md`, and `session-post-processor/verification.md`. The halt-on-RED discipline is enforced on any critical failure.

**Critical checks for pépite-flagging**:
- Frontmatter schema violations (missing required field, wrong type, invalid status transition)
- Criteria count < 2 without manual force-flag
- Cross-project pointer write without explicit per-target user consent

Any of the three triggers RED and halts the skill.

## Post-install health check

Run these checks in order after `install-manifest.yaml` executes.

### Check 1 — `memory/pepites/` exists

```
memory/pepites/ exists                    [ OK / MISSING ]
```

- **OK** → continue
- **MISSING** → re-run install step. Surface the filesystem error.

### Check 2 — `memory/pepites/INDEX.md` exists

```
memory/pepites/INDEX.md exists            [ OK / MISSING ]
```

- **OK** → continue
- **MISSING** → re-run install step, or create from template in `install-manifest.yaml`.

### Check 3 — INDEX contains the trigger criteria section

```
INDEX has "Red-light trigger criteria"    [ OK / MISSING ]
INDEX has "Entry states"                  [ OK / MISSING ]
INDEX has "Surfacing protocol"            [ OK / MISSING ]
```

- **All OK** → post-install is GREEN
- **Any MISSING** → the INDEX has been customised. Do NOT overwrite. Ask the user whether to migrate to the standard template or keep the custom layout. The skill works with a custom INDEX as long as the "## Entries" heading exists for appending new rows.

### Check 4 — Spec reference is reachable

```
.claude/docs/superpowers/specs/v1_pepite_discovery_flagging.md exists  [ OK / MISSING ]
```

- **OK** → post-install GREEN
- **MISSING** → the canonical spec is missing. This is unusual because Genesis bootstrap creates it. YELLOW warning — the skill will still run but the 1:1 mirror discipline is compromised. Surface the missing spec to the user.

## Post-action health check

Run these after a trigger-phrase invocation or automatic detection creates, updates, or propagates a pépite entry.

### Check 5 — Entry file exists and is valid

```
target entry path <path>                  [ OK / MISSING ]
frontmatter parses as YAML                [ OK / INVALID ]
size > 0                                  [ OK / EMPTY ]
```

- **All OK** → continue
- **MISSING** → RED, halt. The write failed silently. Surface the expected path.
- **INVALID** (frontmatter does not parse) → RED, halt. Surface the parse error. If the file was just written in this action, delete it.
- **EMPTY** → RED, halt. Surface: *"Writer produced a zero-byte file. Entry deleted."* Delete the file.

### Check 6 — Frontmatter has all required fields

```
name                                      [ OK / MISSING ]
description                               [ OK / MISSING ]
type: pepite                              [ OK / WRONG ]
discovered_at (YYYY-MM-DD)                [ OK / MISSING / MALFORMED ]
discovered_in_project                     [ OK / MISSING ]
discovered_via                            [ OK / MISSING ]
leverage                                  [ OK / MISSING ]
relevance.origin_project                  [ OK / MISSING / INVALID ]
relevance.transverse                      [ OK / MISSING / INVALID ]
relevance.specific_projects               [ OK / MISSING / NOT_LIST ]
status                                    [ OK / MISSING / INVALID ]
criteria_matched                          [ OK / MISSING / NOT_LIST ]
tags                                      [ OK / MISSING / EMPTY ]
sources                                   [ OK / MISSING / EMPTY ]
```

- **All OK** → continue
- **Any MISSING / INVALID / MALFORMED** → **RED, halt**. Surface which fields are invalid. Delete the file if it was just created in this action. The user fixes the detection logic and re-runs. Do not auto-retry.

### Check 7 — Criteria count respects the "two or more" rule

```
len(criteria_matched) >= 2                [ OK / INSUFFICIENT ]
```

- **OK** → continue
- **INSUFFICIENT** (fewer than 2 criteria) → **RED**, unless the user explicitly force-flagged the pépite via a manual trigger phrase ("flag ceci comme pépite"). If force-flagged, YELLOW and log the force-flag in the status history. If auto-detected and under the bar, RED — the detector is too loose, audit it.

### Check 8 — Body has all required sections

```
body section "## What it is"              [ OK / MISSING ]
body section "## Why it matters"          [ OK / MISSING ]
body section "## Who should know"         [ OK / MISSING ]
body section "## Extraction plan"         [ OK / MISSING ]
body section "## Status history"          [ OK / MISSING ]
```

- **All OK** → continue
- **Any MISSING** → YELLOW, not RED. The entry is structurally valid enough to be usable but the template is incomplete. Log the missing sections and continue. The user can fill them in manually.

### Check 9 — Status transition is legal

```
previous status → new status              [ OK / ILLEGAL ]
```

- **OK** (transition is in the table in `pepite-format.md`) → continue
- **ILLEGAL** (e.g. `dismissed` → `actioned` without going through `seed`) → RED, halt. Surface the illegal transition. The user decides whether to manually edit the entry or abort.

### Check 10 — Cross-project pointer writes were consented per target

**This check runs only if the current action included pointer writes** (option c during surfacing, or a manual "propage" trigger).

```
for each target in propagation_targets:
  pointer file written                    [ OK / SKIPPED / FAILED ]
  explicit per-target consent logged      [ OK / MISSING ]
```

- **OK** on all → continue
- **MISSING consent** on any target → **RED, CRITICAL**:
  1. Log which target received a write without explicit consent
  2. **Delete the pointer file immediately**
  3. Surface to the user: *"Cross-project pointer written without explicit consent for target `<target>`. Pointer deleted. This is a consent-bypass incident. Audit the skill's consent logic before retrying."*
  4. Do not auto-retry. The user audits and re-invokes.

This is the pépite skill's consent floor. It exists to prevent writes to sibling projects that the user did not explicitly authorise — a prerequisite for cross-project routing to be trustworthy.

### Check 11 — Canonical status history updated

```
status history has a new line for this action     [ OK / MISSING ]
```

- **OK** → continue
- **MISSING** → YELLOW, not RED. The entry is valid but the history is incomplete. Append the missing line and log the fix.

### Check 12 — INDEX updated

```
memory/pepites/INDEX.md reflects the new / updated entry    [ OK / MISSING / DUPLICATE ]
```

- **OK** → continue
- **MISSING** → append the one-line entry. Not a halt.
- **DUPLICATE** → update in place, do not add a second line.

### Check 13 — No tmp / bak files

```
No `<entry-path>.tmp` or `.bak` files remaining           [ OK / DIRTY ]
```

- **OK** → post-action GREEN
- **DIRTY** → YELLOW, delete and log.

## Output format — the health card

```markdown
## Pépite flagging health — <YYYY-MM-DD HH:MM>

**Mode**: post-install | post-action
**Action**: auto-detection | manual-flag | status-change | propagation
**Entry**: `memory/pepites/<file>.md`   (post-action only)

### Environment
| Check | Result |
|---|---|
| memory/pepites/ directory | OK |
| INDEX.md | OK |
| Trigger criteria section | OK |
| Entry states section | OK |
| Surfacing protocol section | OK |
| Spec reference | OK |

### Processing (post-action only)
| Check | Result |
|---|---|
| Entry file valid | OK (2145 bytes) |
| Frontmatter complete | OK (14/14 required fields) |
| Criteria count | OK (3 criteria matched: 2, 3, 6) |
| Body sections | OK (5/5) |
| Status transition | OK (seed, initial creation) |
| Propagation consent | N/A (no pointer writes this action) |
| Status history | OK (1 line appended) |
| INDEX updated | OK |
| Tmp cleanup | OK |

**Status**: GREEN

**Next steps**: entry ready for surfacing. The 🔴 card will be emitted at the next natural conversation boundary.
```

## Three possible Status values

- **GREEN** — every check passed. Entry exists, frontmatter complete, body sections present, no consent issues. If the action included propagation, every pointer write had explicit consent.
- **YELLOW** — at least one non-critical check failed (missing optional body section, INDEX drift, dirty tmp file, spec-reference missing). Skill still produced a valid entry. Surface the issues but do not halt.
- **RED** — a critical check failed (missing required frontmatter field, illegal status transition, consent bypass, empty file). **Halt immediately.** If the entry or pointer was just written, delete it. Surface the incident with the exact failure and required audit action. **Never continue past RED.**

## Consent-floor reminder

The only privileged operation in this skill is **cross-project pointer writes**. Every other operation (entry creation, status transitions within the origin project, surfacing cards) is contained inside the origin project's own memory directory and does not need the cross-project consent floor.

But the cross-project pointer write is a write to **another project's state on the user's machine**. It is the equivalent of the `session-post-processor`'s halt-on-leak file deletion — a privileged operation that exists for one specific reason and must never happen without explicit per-invocation, per-target consent.

Treat it as such. Do not batch consent. Do not silently retry. Do not propagate without the user saying yes to each target.

## Anti-Frankenstein reminder

Verification surfaces issues; it does not fix them (except for tmp cleanup and duplicate INDEX line update, which are trivially reversible). If a frontmatter field is missing, the user adds it or the detector is fixed. If a transition is illegal, the user decides how to reconcile. If consent was bypassed, the user audits the code path and decides whether to strengthen the consent logic.

Automation in verification is scope creep. Keep it read-only except for the two tiny write-back operations already named.
