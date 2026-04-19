# v2 Bootstrap via Max Subscription — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Drop the v1.4.0 subprocess Citations API path. Add new skill `phase-auth-preflight` that runs `claude auth status` as a pre-flight check before any Genesis bootstrap. Wire the skill into `genesis-drop-zone` Phase 0.0 and `genesis-protocol` Phase 0. Bump to v2.0.0.

**Architecture:** New ninth Genesis skill (Phase anthropic_auth = `phase-auth-preflight`) called by both Layer A and Layer B entry points. Existing `genesis-drop-zone` skill loses its v1.4.0 network privilege class (returns to disk-only) and v1.5.0 halt-with-remediation card. Three fixtures + one R8 stack entry archived. One subprocess script + scripts dir deleted.

**Tech Stack:** Markdown skills, JSON fixtures from `claude auth status`, bash for verification probes, Python (binary mode) for any CRLF-sensitive file writes per Layer 0.

---

## User decisions captured (defaults from spec ; user can flip any before execution)

- **Q-A version label** : **v2.0.0 MAJOR** (architectural shift + drops v1.4.0 subprocess + drops anthropic SDK dependency + drops halt-card)
- **Q-B phase naming** : **`anthropic_auth`** as the user-facing phase name + `phase-auth-preflight` as the skill name + internal function `check_provider_auth(provider="anthropic")` for v3.x BYOAI extensibility
- **Q-C cleanup scope** : **keep `<field>_source_citation` schema keys deprecated in v2.x**, remove only in v3.0+ (v3 web mode re-introduces extraction subprocess server-side, citations become load-bearing again — per master.md design discipline #4)
- **Q-D self-rating projection** : 9.24 mean (pain 9.6 / prose 9.0 / best-at-date 9.2 / self-contained 9.0 / anti-Frankenstein 9.4)

---

## File structure

### Create

- `skills/phase-auth-preflight/SKILL.md` — new skill (frontmatter + decision tree + bilingual remediation card)
- `skills/phase-auth-preflight/install-manifest.yaml` — per project convention (mirrored from genesis-protocol's install-manifest)
- `skills/phase-auth-preflight/tests/runtime_evidence_v2_0_0.md` — runbook + expected outputs per scenario
- `skills/phase-auth-preflight/tests/fixtures/auth_status_authed_firstparty.json` — fixture
- `skills/phase-auth-preflight/tests/fixtures/auth_status_loggedin_false.json` — fixture
- `skills/phase-auth-preflight/tests/fixtures/auth_status_authed_bedrock.json` — fixture
- `skills/phase-auth-preflight/tests/fixtures/auth_status_corrupt.json` — fixture (intentionally malformed)
- `tests/fixtures/drop_zone_intent_fixture_v2_arbitrated.md` — v2 schema fixture (replaces archived v1_5_0_arbitrated)
- `tests/fixtures/.archive/ARCHIVE.md` — archive index
- `skills/genesis-drop-zone/.archive/v1_5_0_halt_card_content.md` — forensic preservation of halt-card text

### Modify

- `skills/genesis-drop-zone/SKILL.md` — annotate v1.4.0 + v1.5.0 sections as retired ; add v2 In Scope section ; revert privilege map (network class retired) ; wire `phase-auth-preflight` invocation as Phase 0.0
- `skills/genesis-protocol/SKILL.md` (or `skills/genesis-protocol/phase-0-seed-loading.md` — verify which file holds Phase 0) — wire `phase-auth-preflight` as first step before existing Phase 0
- `memory/master.md` — pattern #2 (network class retired ; phase-auth-preflight added as new privilege-map entry) + pattern #4 (ninth ordinal data-point entry)
- `.claude-plugin/plugin.json` — version `1.6.3` → `2.0.0`
- `.claude/docs/superpowers/research/INDEX.md` — move `anthropic-python` from Active to Archive section

### Move (archive)

- `tests/fixtures/drop_zone_intent_fixture_v1_4_0_fr_with_citations.md` → `tests/fixtures/.archive/`
- `tests/fixtures/drop_zone_intent_fixture_v1_4_0_en_with_citations.md` → `tests/fixtures/.archive/`
- `tests/fixtures/drop_zone_intent_fixture_v1_5_0_arbitrated.md` → `tests/fixtures/.archive/`
- `.claude/docs/superpowers/research/stack/anthropic-python_2026-04-18.md` → `.claude/docs/superpowers/research/archive/`

### Delete

- `skills/genesis-drop-zone/scripts/extract_with_citations.py`
- `skills/genesis-drop-zone/scripts/` (directory if empty after deletion)

---

## Tasks

### Task 1: phase-auth-preflight skill scaffold

**Files:**
- Create: `skills/phase-auth-preflight/SKILL.md` (frontmatter only, body stub)
- Create: `skills/phase-auth-preflight/install-manifest.yaml` (mirror genesis-protocol's manifest)

**Reference:** Read `skills/genesis-protocol/SKILL.md` first 20 lines and `skills/genesis-protocol/install-manifest.yaml` to mirror conventions (per cross-skill-pattern #1 1:1 mirror).

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p skills/phase-auth-preflight/tests/fixtures
mkdir -p skills/phase-auth-preflight/.archive  # may not be needed but reserves
```

- [ ] **Step 2: Read genesis-protocol install-manifest for convention mirror**

Read: `skills/genesis-protocol/install-manifest.yaml`

- [ ] **Step 3: Write phase-auth-preflight install-manifest.yaml**

Mirror the genesis-protocol shape with skill-specific fields (name = `phase-auth-preflight`, description = one-liner from spec).

- [ ] **Step 4: Write phase-auth-preflight SKILL.md frontmatter + skeleton**

Per § "SKILL.md content" below (Step 4 of Task 2 has the full body — Task 1 ends with frontmatter + section headings only ; bodies fill in Task 2).

Frontmatter (note SPDX trailing per R10.2 exception, single-quote-wrapped description per F5 lesson) :

```markdown
---
name: phase-auth-preflight
description: 'Pre-flight check for Anthropic auth via Claude Code Max subscription. Runs `claude auth status` JSON probe ; passes silently if loggedIn ; otherwise prints bilingual remediation card instructing `claude auth login` and halts. Invoked as Phase 0.0 by `/genesis-drop-zone` (Layer A) and as first step of Phase 0 by `/genesis-protocol` (Layer B). v2.0.0 introduces this skill ; replaces v1.5.0 halt-with-remediation card after v1.4.0 subprocess Citations path is dropped. Internal function signature `check_provider_auth(provider="anthropic")` is BYOAI-ready for v3.x without skill restructure.'
---

# Phase Auth Pre-flight

## Purpose

[stub — Task 2 fills]

## Decision tree

[stub — Task 2 fills]

## Remediation card content

[stub — Task 2 fills]

## Test scenarios

[stub — Task 2 fills]

<!-- SPDX-License-Identifier: MIT -->
```

- [ ] **Step 5: Verify plugin loads with new skill present**

Run: `claude plugin validate C:/Dev/Claude_cowork/project-genesis/.claude/worktrees/feat_2026-04-19_v2_max_subscription_design`

Expected: ✔ Validation passed (9 skills detected, 0 errors).

If errors appear, inspect frontmatter — most common cause = SPDX comment placement (must be trailing per R10.2 exception) or YAML parse on description (use single-quotes per v1.6.3 F5 collateral fix).

- [ ] **Step 6: Commit**

```bash
git add skills/phase-auth-preflight/
git commit -m "feat(v2): scaffold phase-auth-preflight skill (frontmatter + manifest + dir)"
```

---

### Task 2: phase-auth-preflight skill content

**Files:**
- Modify: `skills/phase-auth-preflight/SKILL.md` (fill stubs from Task 1)
- Create: `skills/phase-auth-preflight/tests/fixtures/auth_status_authed_firstparty.json`
- Create: `skills/phase-auth-preflight/tests/fixtures/auth_status_loggedin_false.json`
- Create: `skills/phase-auth-preflight/tests/fixtures/auth_status_authed_bedrock.json`
- Create: `skills/phase-auth-preflight/tests/fixtures/auth_status_corrupt.json`
- Create: `skills/phase-auth-preflight/tests/runtime_evidence_v2_0_0.md`

- [ ] **Step 1: Capture real `claude auth status` output as authed-firstparty fixture**

Run: `claude auth status > skills/phase-auth-preflight/tests/fixtures/auth_status_authed_firstparty.json`

Expected fixture content (verify):

```json
{
  "loggedIn": true,
  "authMethod": "claude.ai",
  "apiProvider": "firstParty",
  "email": "<elided-for-fixture>",
  "orgId": "<elided>",
  "orgName": "<elided>",
  "subscriptionType": "max"
}
```

Edit fixture to elide PII (email / orgId / orgName) for repo commit safety.

- [ ] **Step 2: Author 3 synthetic fixtures**

Write `auth_status_loggedin_false.json` :

```json
{
  "loggedIn": false,
  "authMethod": null,
  "apiProvider": null,
  "subscriptionType": null
}
```

Write `auth_status_authed_bedrock.json` :

```json
{
  "loggedIn": true,
  "authMethod": "bedrock",
  "apiProvider": "Bedrock",
  "subscriptionType": null
}
```

Write `auth_status_corrupt.json` (intentionally malformed) :

```
{ "loggedIn": true,  "authMethod":
```

- [ ] **Step 3: Write SKILL.md body — Purpose section**

Replace `## Purpose` stub with :

```markdown
## Purpose

Genesis bootstrapping requires Anthropic-backed inference (Claude). v2 leverages the Max subscription that Claude Code already holds at session open via `claude auth login` — no separate `ANTHROPIC_API_KEY` / Console workspace / subprocess Messages API call. This skill verifies that auth is actually present BEFORE any phase that depends on it (Layer A `genesis-drop-zone` Phase 0 ; Layer B `genesis-protocol` Phase 0). Idempotent ; ~10s when authed ; one-turn remediation when not.

Internal function signature is `check_provider_auth(provider="anthropic")` — BYOAI-ready for v3.x without restructure (see `memory/master.md § "What v3 vision is"` for the staging plan).
```

- [ ] **Step 4: Write SKILL.md body — Decision tree section**

Replace `## Decision tree` stub with the table from spec § 1.2 (5 rows : authed-firstparty / authed-Bedrock-or-Vertex / loggedIn=false / claude-not-installed / corrupt-output).

- [ ] **Step 5: Write SKILL.md body — Remediation card content section**

Per spec § 1.3 — bilingual title (FR + EN), one-paragraph explanation, exact command `claude auth login`, "what happens" description, multi-org note, NO `--console` mention.

- [ ] **Step 6: Write SKILL.md body — Test scenarios section**

Reference each fixture by relative path. For each scenario describe (a) the expected runtime behaviour, (b) how to manually trigger it on the dev machine, (c) the assertion that the LLM output should satisfy.

- [ ] **Step 7: Write tests/runtime_evidence_v2_0_0.md runbook**

Mirror the v1.6.2 `runtime_dogfood_v1_6_2.md` shape — bash commands, expected outputs, evidence capture format. 5 scenarios. Note that 4/5 are documentation-only (require disrupting dev state to test live) — only the authed-firstparty case is automatically testable via `claude -p`.

- [ ] **Step 8: Verify plugin still loads**

Run: `claude plugin validate <worktree>`

Expected: ✔ Validation passed.

- [ ] **Step 9: Commit**

```bash
git add skills/phase-auth-preflight/
git commit -m "feat(v2): phase-auth-preflight skill body + 4 fixtures + runbook"
```

---

### Task 3: Archive subprocess Citations + R8 stack + fixtures

**Files:**
- Move: `.claude/docs/superpowers/research/stack/anthropic-python_2026-04-18.md` → `.claude/docs/superpowers/research/archive/`
- Move: 3 fixtures `tests/fixtures/drop_zone_intent_fixture_v1_4_0_*_with_citations.md` + `..._v1_5_0_arbitrated.md` → `tests/fixtures/.archive/`
- Create: `tests/fixtures/.archive/ARCHIVE.md`
- Create: `tests/fixtures/drop_zone_intent_fixture_v2_arbitrated.md`
- Create: `skills/genesis-drop-zone/.archive/v1_5_0_halt_card_content.md`
- Delete: `skills/genesis-drop-zone/scripts/extract_with_citations.py` + parent dir if empty
- Modify: `.claude/docs/superpowers/research/INDEX.md`

- [ ] **Step 1: Move R8 anthropic-python entry to archive**

```bash
mkdir -p .claude/docs/superpowers/research/archive
git mv .claude/docs/superpowers/research/stack/anthropic-python_2026-04-18.md .claude/docs/superpowers/research/archive/anthropic-python_2026-04-18.md
```

- [ ] **Step 2: Add v2-retirement note to top of archived R8 entry**

Read the file, prepend a one-line note (after frontmatter) :

```markdown
> **v2 retirement note (2026-04-19)** : Genesis v2.0.0 retired the subprocess that pinned this dependency. Entry preserved for cross-project reference (other projects on this machine that use the anthropic SDK directly remain valid consumers).
```

- [ ] **Step 3: Update R8 INDEX.md — move row from Active to Archive**

Read: `.claude/docs/superpowers/research/INDEX.md`

Remove the `anthropic-python` row from the Active table. Add to the Archive section :
```markdown
- [anthropic-python_2026-04-18.md](archive/anthropic-python_2026-04-18.md) — TTL expired 2026-04-19 ; **v2.0.0 retired the subprocess that pinned this dependency**, entry preserved for cross-project reference.
```

- [ ] **Step 4: Create tests/fixtures/.archive/ + move 3 fixtures**

```bash
mkdir -p tests/fixtures/.archive
git mv tests/fixtures/drop_zone_intent_fixture_v1_4_0_fr_with_citations.md tests/fixtures/.archive/
git mv tests/fixtures/drop_zone_intent_fixture_v1_4_0_en_with_citations.md tests/fixtures/.archive/
git mv tests/fixtures/drop_zone_intent_fixture_v1_5_0_arbitrated.md tests/fixtures/.archive/
```

- [ ] **Step 5: Write tests/fixtures/.archive/ARCHIVE.md**

```markdown
<!-- SPDX-License-Identifier: MIT -->

# Archived fixtures

Fixtures retired by v2.0.0 architectural shift (drop subprocess Citations path).

| File | Reason |
|---|---|
| drop_zone_intent_fixture_v1_4_0_fr_with_citations.md | Citation keys (`*_source_citation`) present, unrepresentative of v2 schema. |
| drop_zone_intent_fixture_v1_4_0_en_with_citations.md | Same reason. |
| drop_zone_intent_fixture_v1_5_0_arbitrated.md | DUAL semantics (carries both v1.5.0 `snapshot_version` + `arbitrated_fields` AND v1.4.0 `_source_citation` keys). Replaced by `tests/fixtures/drop_zone_intent_fixture_v2_arbitrated.md` (same revision-state semantics, no citation keys). |

Fixtures retained in active set (citation-free) :
- `drop_zone_intent_fixture_v1_3_2.md`
- `drop_zone_intent_fixture_v1_3_3_en.md`
- `drop_zone_intent_fixture_v1_4_0_fallback.md` (byte-identical to v1.3.3 modulo `skill_version`)
```

- [ ] **Step 6: Create new v2 fixture (replaces archived v1.5.0 arbitrated)**

Read the archived v1.5.0 arbitrated fixture as reference. Copy structure but :
- Strip all `*_source_citation` keys
- Bump `skill_version` to `2.0.0`
- Keep `snapshot_version`, `arbitrated_fields`, `supersedes_snapshot` (revision-state metadata preserved)
- Update body prose to remove any `[page N]` / `[lines X-Y]` citation markers

Write to: `tests/fixtures/drop_zone_intent_fixture_v2_arbitrated.md`

- [ ] **Step 7: Preserve halt-card content forensically**

```bash
mkdir -p skills/genesis-drop-zone/.archive
```

Extract the v1.5.0 halt-with-remediation card content from `skills/genesis-drop-zone/SKILL.md` (search for "halt-with-remediation" and copy the content + surrounding context paragraphs). Write to:

`skills/genesis-drop-zone/.archive/v1_5_0_halt_card_content.md`

Add a one-line top note : "Forensic preservation — halt-with-remediation card content from v1.5.0, retired in v2.0.0 because subprocess Citations path no longer exists."

- [ ] **Step 8: Delete subprocess script + parent dir**

```bash
git rm skills/genesis-drop-zone/scripts/extract_with_citations.py
rmdir skills/genesis-drop-zone/scripts/  # only succeeds if dir empty
```

- [ ] **Step 9: Verify plugin still loads**

Run: `claude plugin validate <worktree>`

Expected: ✔ Validation passed.

- [ ] **Step 10: Commit**

```bash
git add .claude/docs/superpowers/research/ tests/fixtures/ skills/genesis-drop-zone/.archive/ skills/genesis-drop-zone/scripts/
git commit -m "feat(v2): archive subprocess script + R8 stack entry + 3 fixtures + create v2 fixture + preserve halt-card forensically"
```

---

### Task 4: genesis-drop-zone SKILL.md retire annotations + v2 section + privilege revert

**Files:**
- Modify: `skills/genesis-drop-zone/SKILL.md`

- [ ] **Step 1: Annotate v1.4.0 In Scope section as retired**

Locate the `### In scope (v1.4.0)` heading. Replace the heading line with :

```markdown
### In scope (v1.4.0) — RETIRED in v2.0.0

> **v2 retirement note** : This entire section is retired. The Citations API subprocess + anthropic Python SDK + ANTHROPIC_API_KEY dependency + `<field>_source_citation` writes are removed. Schema keys remain parseable (deprecated v2.x, removed v3.0+). See `.claude/docs/superpowers/specs/2026-04-19-v2-bootstrap-via-max-subscription-design.md`.
```

Section content stays for forensic continuity.

- [ ] **Step 2: Annotate v1.5.0 In Scope section as retired**

Same treatment for `### In scope (v1.5.0)` :

```markdown
### In scope (v1.5.0) — RETIRED in v2.0.0

> **v2 retirement note** : Halt-with-remediation card retired (subprocess no longer exists, nothing to remediate). Revision-state metadata (`snapshot_version`, `arbitrated_fields`, `supersedes_snapshot`) preserved — these are NOT subprocess-related. Halt-card content preserved at `skills/genesis-drop-zone/.archive/v1_5_0_halt_card_content.md`.
```

- [ ] **Step 3: Add new v2 In Scope section**

Insert after the v1.5.x sections, before the "Failure modes" section :

```markdown
### In scope (v2.0.0)

1. **Drop subprocess Citations path** — `extract_with_citations.py` deleted, anthropic SDK dependency removed, ANTHROPIC_API_KEY no longer required, halt-with-remediation card retired.
2. **Phase 0.0 invocation of `phase-auth-preflight`** — before Phase 0.1 welcome, the skill calls `phase-auth-preflight` to verify Claude Code is authed via Max subscription. If not authed, `phase-auth-preflight` halts with a remediation card instructing `claude auth login` ; control does not return to `genesis-drop-zone` until auth is re-verified on next launch.
3. **Concentrated privilege class declaration reverts to disk-only** — network class retired (was added v1.4.0). v1.5.0 disk-class extension preserved (snapshot writes + history archive).
4. **Schema backward compatibility** — `drop_zone_intent.md` files written by v1.4.0 / v1.4.1 / v1.5.0 with `<field>_source_citation` keys remain parseable. v2-written files simply omit the keys. `schema_version` stays at `1`. No migration required.
5. **In-context extraction** — extraction reverts to in-context (Claude in the current session, under Max auth), as in v1.3.x. Per-field provenance metadata (`[page N]` / `[lines X-Y]` markers) is no longer guaranteed by API ; in-context extraction can still cite sources best-effort in prose.
```

- [ ] **Step 4: Revert concentrated privilege declaration**

Locate the privilege declaration (search for "Concentrated privilege"). Update text to declare disk-class only, with the v1.5.0 disk-class extension preserved (snapshot writes + history archive). Add explicit note : "Network class retired in v2.0.0."

- [ ] **Step 5: Verify plugin still loads**

Run: `claude plugin validate <worktree>` — expect ✔.

- [ ] **Step 6: Commit**

```bash
git add skills/genesis-drop-zone/SKILL.md
git commit -m "feat(v2): genesis-drop-zone — retire v1.4.0+v1.5.0 sections, add v2 section, revert privilege to disk-only"
```

---

### Task 5: Wire phase-auth-preflight into entry points

**Files:**
- Modify: `skills/genesis-drop-zone/SKILL.md` (Layer A invocation)
- Modify: `skills/genesis-protocol/SKILL.md` OR `skills/genesis-protocol/phase-0-seed-loading.md` (Layer B invocation — verify which file holds Phase 0 first step)

- [ ] **Step 1: Locate Layer A Phase 0 entry point**

Search `skills/genesis-drop-zone/SKILL.md` for "Phase 0" or "phase-0". Identify the first runtime instruction Claude executes when the skill dispatches.

- [ ] **Step 2: Insert Phase 0.0 phase-auth-preflight call before Phase 0.1 welcome**

Add a step :

```markdown
### Phase 0.0 — Auth pre-flight (v2.0.0+)

Before printing the welcome box (Phase 0.1), invoke the `phase-auth-preflight` skill. If it returns pass, proceed to Phase 0.1. If it halts (auth missing), do not print welcome — the auth-preflight halt-card is the user-facing output for this turn.
```

- [ ] **Step 3: Locate Layer B Phase 0 first step (pre-resolved by plan author)**

Insertion site : `skills/genesis-protocol/phase-0-seed-loading.md` § "## The flow — five steps", **before `### Step 0.1 — Inspect the input folder`**, as a new `### Step 0.0 — Auth pre-flight (v2.0.0+)`. Plan author verified this location 2026-04-19 by reading the file directly.

- [ ] **Step 4: Insert phase-auth-preflight invocation as new Step 0.0 of Layer B Phase 0**

Same content shape as Step 2 above ("invoke phase-auth-preflight ; if pass proceed to Step 0.1, if halt do not proceed"), inserted at the location identified in Step 3.

- [ ] **Step 5: Verify plugin still loads**

Run: `claude plugin validate <worktree>` — expect ✔.

- [ ] **Step 6: Commit**

```bash
git add skills/genesis-drop-zone/SKILL.md skills/genesis-protocol/
git commit -m "feat(v2): wire phase-auth-preflight into Layer A + Layer B Phase 0 entry points"
```

---

### Task 6: master.md cross-skill-pattern updates

**Files:**
- Modify: `memory/master.md`

- [ ] **Step 1: Locate cross-skill-pattern #2 narrative**

Search `memory/master.md` for "Concentrated-privilege map" — the long pattern #2 paragraph.

- [ ] **Step 2: Add v2.0.0 entry — network class retirement + phase-auth-preflight new entry**

Append to the existing pattern #2 paragraph (after the v1.6.0 promptor sentence) :

```markdown
**v2.0.0 retires `genesis-drop-zone`'s network class** — Citations API subprocess removed, returns to disk-only (v1.5.0 disk-class extension preserved). The "first multi-class declaration" precedent (v1.4.0) stands as a historical data-point but the current state of every shipped skill returns to ≤1 class. **v2.0.0 also adds `phase-auth-preflight` as the 9th skill** with privilege class `subprocess` (calls `claude auth status` and probes for `claude` binary presence ; never executes `claude auth login` automatically). Five mitigations : (a) read-only commands only, (b) no auth-state-mutating side effects (only print remediation), (c) no env var writes, (d) no file writes, (e) JSON-parse-with-fallback (corrupt output halts with diagnostic, never crashes uncontrolled). Total privilege map at v2.0.0 : **9 skills, 7 with privilege classes** (genesis-drop-zone disk + genesis-protocol disk + phase-minus-one subprocess + phase-5-5-auth-preflight subprocess + pepite-flagging disk + session-post-processor disk + phase-auth-preflight subprocess), **2 with `none`** (journal-system + promptor — pre-v2 count of 2 preserved, no change).
```

(Pre-resolved by plan author 2026-04-19 via grep against current master.md — pre-v2 has 8 skills, 6 with privilege classes + 2 with `none`. v2 adds 1 skill (phase-auth-preflight subprocess) and reverts 1 (genesis-drop-zone returns to single class) → 9 total, 7 privilege, 2 none.)

- [ ] **Step 3: Locate cross-skill-pattern #4 narrative**

Search `memory/master.md` for "Layer A / Layer B stratification (v2-onwards, added v1.3.0)" — the pattern #4 paragraph.

- [ ] **Step 4: Add ninth ordinal data-point entry**

Append to the existing pattern #4 narrative (after the v1.6.2 depth-update sentence on the sixth ordinal) :

```markdown
**Ninth data-point of the zero-ripple principle** — v2.0.0 demonstrates the principle holds during architectural REMOVAL : Layer A's `<field>_source_citation` keys are no longer written by `genesis-drop-zone`, but Layer B's parser ignores unknown / missing keys gracefully (per v1.4.0 design "Key omitted (not written as null) when no citation applies"). Forward-compat with old writers (v1.4.0+ files with citation keys load cleanly post-v2) + backward-compat with old parsers (v2 files without citation keys load cleanly under v1.4.0 parser if anyone runs that combo) — both directions hold simultaneously under a key-omission regime. Distinct from v1.5.1's PATCH-prose-cleanup data-point (sixth) because v1.5.1 was "Layer A polishes wording, contract unchanged" while v2 is "Layer A stops writing entire keys, contract additively-shrinks". New ripple mode (key omission) warrants its own ordinal.
```

- [ ] **Step 5: Verify file integrity**

```bash
wc -l memory/master.md
# Note line count — should grow by ~10-15 lines.
```

- [ ] **Step 6: Commit**

```bash
git add memory/master.md
git commit -m "feat(v2): master.md cross-skill-pattern #2 (privilege map v2 update) + #4 (ninth zero-ripple ordinal)"
```

---

### Task 7: Plugin.json version bump

**Files:**
- Modify: `.claude-plugin/plugin.json`

- [ ] **Step 1: Read current plugin.json**

Read: `.claude-plugin/plugin.json`

- [ ] **Step 2: Bump version**

Change : `"version": "1.6.3"` → `"version": "2.0.0"`

- [ ] **Step 3: Verify JSON parses**

```bash
python -c "import json; print(json.load(open('.claude-plugin/plugin.json'))['version'])"
```

Expected output : `2.0.0`

- [ ] **Step 4: Verify plugin still loads**

Run: `claude plugin validate <worktree>` — expect ✔.

- [ ] **Step 5: Commit**

```bash
git add .claude-plugin/plugin.json
git commit -m "feat(v2): plugin.json 1.6.3 → 2.0.0 (MAJOR — architectural shift)"
```

---

### Task 8: Runtime evidence + AC verification + ship

**Files:**
- Create or update: `skills/phase-auth-preflight/tests/runtime_evidence_v2_0_0.md` (capture actual outputs)
- Verification only : no code change in this task

- [ ] **Step 1: Run authed-firstparty scenario**

```bash
cd C:/tmp
claude -p --plugin-dir <worktree> --output-format json "Run /phase-auth-preflight and report what happens." > C:/tmp/v2-probe-authed.json
```

Verify output contains : "✓ Auth Anthropic OK" (or equivalent confirmation line) + control returned to caller (no halt).

- [ ] **Step 2: Document scenario 2-5 expected behavior in runbook**

For loggedIn=false / claude-not-installed / authed-Bedrock / corrupt-output : these require disrupting dev state to test live. Document expected behavior in `runtime_evidence_v2_0_0.md` with the matching fixture as reference. Mark as "manual verification required" until v3.0 test harness wrapper is built.

- [ ] **Step 3: AC10 zero-ripple verification (parser-level)**

```bash
grep -rn "_source_citation" skills/genesis-protocol/ skills/journal-system/ skills/pepite-flagging/ skills/phase-5-5-auth-preflight/ skills/phase-minus-one/ skills/session-post-processor/ skills/promptor/ skills/phase-auth-preflight/
```

Expected : zero matches (citations subprocess references should NOT exist anywhere outside `skills/genesis-drop-zone/.archive/` and `tests/fixtures/.archive/`).

If matches exist outside archive paths : investigate, fix, re-verify.

- [ ] **Step 4: Probe all 9 skills surface from worktree**

```bash
cd C:/tmp
claude -p --plugin-dir <worktree> --output-format json "List all 9 project-genesis skills with one-line descriptions. Format: bullet markdown." > C:/tmp/v2-probe-9-skills.json
```

Verify output lists exactly 9 skills under `project-genesis:` namespace (8 from v1.6.3 + new `phase-auth-preflight`).

- [ ] **Step 5: Self-rating honest 5-axis**

In `tests/runtime_evidence_v2_0_0.md` add a "## Self-rating — honest post-feat" table per project convention (pain-driven / prose / best-at-date / self-contained / anti-Frankenstein). Compare projected (9.24 mean) vs honest. Apply Layer 0 `feedback_honest_self_rating_post_feat.md` discipline (willingness to drop ≥0.5 + break streak if warranted).

- [ ] **Step 6: Commit runtime evidence + self-rating**

```bash
git add skills/phase-auth-preflight/tests/runtime_evidence_v2_0_0.md
git commit -m "feat(v2): runtime evidence (1 live + 4 documented scenarios) + AC10 zero-ripple verified + self-rating honest"
```

- [ ] **Step 7: PR + tag — handoff to user for git push (R2.3 / Layer 0 destructive-action discipline)**

Print to user :

```
v2.0.0 implementation complete on branch feat/v2-max-subscription-design.

Ready to ship :
1. git push -u origin feat/v2-max-subscription-design
2. gh pr create --title "v2.0.0 — bootstrap via Max subscription, drop subprocess Citations" --body "<paste from spec TL;DR>"
3. gh pr merge --squash <pr-number>
4. git tag v2.0.0
5. git push origin v2.0.0

Confirm to proceed (or ask me to run them).
```

Wait for user confirm before pushing.

- [ ] **Step 8: After user confirm, execute push + PR + squash + tag**

(Execute the 5 commands above with user-supplied PR number for the merge step.)

- [ ] **Step 9: Chore commit — CHANGELOG + session trace + MEMORY + resume (separate PR per v1.6.3 pattern)**

Per project convention verified from v1.6.3 commit chain (`0c50440 chore(memory): v1.6.3 — CHANGELOG honest + session trace + MEMORY + resume (#48)` was a SEPARATE PR after the v1.6.3 feat ship), the chore lands as its own PR squash-merged to main :

a. Create new chore worktree :
```bash
cd C:/Dev/Claude_cowork/project-genesis
git worktree add .claude/worktrees/chore_2026-04-19_v2_0_0_session -b chore/v2-0-0-session
cd .claude/worktrees/chore_2026-04-19_v2_0_0_session
```

b. Inside chore worktree, write the 4 chore artefacts :
- Update `CHANGELOG.md` with v2.0.0 entry + 5-axis honest rating
- Write `memory/project/session_v2_0_0_max_subscription_drop_subprocess.md` (session trace per template — mirror shape of `session_v1_6_3_f5_fix.md`)
- Update `memory/MEMORY.md` index
- Write `.claude/docs/superpowers/resume/2026-04-19_v2_0_0_to_next.md` (next session handoff with PowerShell launcher per Layer 0 `feedback_end_of_session_resume_phrase.md`)

c. Commit + push + PR + squash + merge :
```bash
git add CHANGELOG.md memory/ .claude/docs/superpowers/resume/
git commit -m "chore(memory): v2.0.0 — CHANGELOG honest + session trace + MEMORY + resume"
git push -u origin chore/v2-0-0-session
gh pr create --title "chore(memory): v2.0.0 session artefacts" --body "Mirrors v1.6.3 #48 chore PR pattern."
gh pr merge --squash <pr-number>
```

d. Both feat worktree (`feat_2026-04-19_v2_max_subscription_design/`) and chore worktree (`chore_2026-04-19_v2_0_0_session/`) retained per R2.5.

---

## Acceptance criteria (all must pass before tag)

- [ ] AC1 : `claude plugin validate <worktree>` — ✔ Validation passed (9 skills detected, 0 errors)
- [ ] AC2 : `claude -p --plugin-dir <worktree>` lists 9 project-genesis skills (8 prior + phase-auth-preflight)
- [ ] AC3 : Authed-firstparty scenario test produces "✓ Auth Anthropic OK" line in real `claude -p` invocation
- [ ] AC4 : 4 synthetic fixtures present at `skills/phase-auth-preflight/tests/fixtures/`
- [ ] AC5 : `extract_with_citations.py` deleted, `scripts/` directory removed
- [ ] AC6 : 3 fixtures moved to `tests/fixtures/.archive/` ; new `v2_arbitrated.md` fixture created without citation keys
- [ ] AC7 : R8 anthropic-python entry moved to archive ; INDEX.md updated
- [ ] AC8 : `genesis-drop-zone` SKILL.md has v2 section + retired annotations + privilege map reverted to disk-only
- [ ] AC9 : Both Layer A (genesis-drop-zone) and Layer B (genesis-protocol) Phase 0 invoke `phase-auth-preflight` as their first step
- [ ] AC10 : `grep -rn "_source_citation" skills/` returns zero matches outside `.archive/` paths
- [ ] AC11 : `memory/master.md` cross-skill-pattern #2 + #4 updated with v2 entries
- [ ] AC12 : `plugin.json` version = `2.0.0`
- [ ] AC13 : Honest self-rating recorded ; mean projected 9.24, willing to drop if axes underperform

---

## Out of scope for this plan

- Implementation of any v3 vision item (BYOAI, web mode, Lovable-style hosting, external installer) — see `memory/master.md § "What v3 vision is"`
- Building a test harness wrapper for mocking `claude auth status` (defer to v3.0 when web-mode integration tests will need a similar pattern)
- Renaming `promptor` skill to `promptor-anthropic` (defer to v3.x when 2nd provider promptor ships)
- Updating `.claude/docs/superpowers/research/INDEX.md` for any other R8 entry beyond `anthropic-python`

---

## Estimated time + commit count

- 8 numbered tasks → 8 feat commits in tranche
- Plus chore commit at end
- Plus plan + plan-polish commits before feat (this commit is the plan)
- Total session estimate : 2-3 hours of active implementation work + 30 min PR / merge / tag / chore

<!-- SPDX-License-Identifier: MIT -->
