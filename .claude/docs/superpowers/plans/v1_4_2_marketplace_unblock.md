<!-- SPDX-License-Identifier: MIT -->
# v1.4.2 Marketplace Unblock Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship v1.4.2 PATCH — fix `genesis-protocol` install-path resolution (drop legacy 3-levels-up fallback) + bundle 5 canonical R8 templates in-skill, addressing Friction #4 + #5 from 2026-04-18 v1.4.1 dogfood BLOCKERS for marketplace install.

**Architecture:** Two surgical runbook rewrites (Phase 1 Step 1.3 + Phase 2 Step 2.3) resolving rules + R8 cache seeds to skill-local paths with halt-with-remediation on missing. New `skills/genesis-protocol/research-templates/` directory carrying the 5 canonical entries (3 sota copy-and-rename from active R8 cache + 2 stack refreshed via WebSearch). `install-manifest.yaml` version bump `0.8.0 → 1.4.2` + 10 new `file_exists`/`directory_exists` checks. Zero Layer A ripple; zero schema bump; zero new privilege.

**Tech Stack:** Markdown (phase runbooks + spec + plan), YAML (install-manifest + R8 frontmatter), JSON (plugin.json), Bash (git + grep verification probes), WebSearch (R8 refresh). No Python changes, no test framework (verification via grep + scenario walkthroughs in `verification.md`).

**Ship timeline:** Six-commit rhythm 7th consecutive application. Commits already on branch (pre-plan work): `35c8b72` chore dogfood archive + `62fee9f` spec + `8bc2932` spec-polish + `7ff7319` spec-polish-2 regression fix = 4 commits. This plan produces the remaining work: plan commit (implied by saving) + plan-polish (after reviewer pass) + feat (commit 5) + chore (commit 6) + PR/merge/tag.

**Spec**: `.claude/docs/superpowers/specs/v1_4_2_marketplace_unblock.md` (commit 7ff7319, 277 lines, APPROVED after 3 review iterations)

**Pain source**: `memory/project/dogfood_v1.4.1_stress_2026-04-18/stress_test_report.md`

---

## File Structure

### New files (6 total)

| Path | Responsibility |
|---|---|
| `skills/genesis-protocol/research-templates/README.md` | Documents purpose + refresh policy for in-skill R8 bundle |
| `skills/genesis-protocol/research-templates/sota/claude-code-plugin-distribution.md` | Canonical bundle entry #1 (copy-rename from active R8 sota, date suffix stripped) |
| `skills/genesis-protocol/research-templates/sota/claude-ecosystem-cross-os.md` | Canonical bundle entry #2 (copy-rename, date suffix stripped) |
| `skills/genesis-protocol/research-templates/sota/spdx-headers.md` | Canonical bundle entry #3 (copy-rename, date suffix stripped) |
| `skills/genesis-protocol/research-templates/stack/claude-code-plugin-structure.md` | Canonical bundle entry #4 (R8-refreshed via WebSearch, no date suffix) |
| `skills/genesis-protocol/research-templates/stack/claude-code-session-jsonl-format.md` | Canonical bundle entry #5 (R8-refreshed via WebSearch, no date suffix) |

### Modified files (5 total)

| Path | Responsibility |
|---|---|
| `skills/genesis-protocol/phase-1-rules-memory.md` | Step 1.3 resolver rewrite (drop legacy fallback, new halt message) + Step 2.3 resolver rewrite (skill-local source + new halt message + 5-row table Source column patched; follow-on paragraphs preserved verbatim) |
| `skills/genesis-protocol/install-manifest.yaml` | Version bump `0.8.0 → 1.4.2` + 10 new verification checks appended |
| `skills/genesis-protocol/verification.md` | Append v1.4.2 scenarios S1-S3 |
| `.claude-plugin/plugin.json` | Version bump `1.4.1 → 1.4.2` |
| `.claude/docs/superpowers/research/INDEX.md` | Move 2 stack entries from `## Archive` back to `## Active` with fresh `expires_at` (post-refresh) |

### Unchanged + preserved-intact

| Path | Why listed |
|---|---|
| `skills/genesis-drop-zone/**` | **Zero Layer A ripple** — byte-identical across v1.4.1 → v1.4.2. Verify via `git diff main --stat -- skills/genesis-drop-zone/` returning empty. |
| `skills/phase-minus-one/**` | Zero touch |
| `skills/phase-5-5-auth-preflight/**` | Zero touch |
| `skills/journal-system/**` | Zero touch |
| `skills/session-post-processor/**` | Zero touch |
| `skills/pepite-flagging/**` | Zero touch |
| `memory/master.md` | Zero cross-skill-pattern touch (v1.4.2 adds no new pattern) |

### Project R8 cache side effect (co-created during Task 3 + 4 refresh)

| Path | Responsibility |
|---|---|
| `.claude/docs/superpowers/research/stack/claude-code-plugin-structure_2026-04-19.md` | Project-level R8 refresh (with date suffix per downstream R8 convention) |
| `.claude/docs/superpowers/research/stack/claude-code-session-jsonl-format_2026-04-19.md` | Project-level R8 refresh (with date suffix) |

---

## Task 0: R8 refresh feasibility gate (escape clause)

**Files:**
- Read: `.claude/docs/superpowers/research/archive/claude-code-plugin-structure_2026-04-14.md`
- Read: `.claude/docs/superpowers/research/archive/claude-code-session-jsonl-format_2026-04-15.md`
- Probe: WebSearch

**Context:** Spec Rationale bullet says: *"If WebSearch during feat reveals a breaking change in either topic since the 2026-04-14/17 source captures (new `plugin.json` field, new JSONL redaction pattern, schema drift), pause v1.4.2 ship and route the breaking-change delta through v1.5.x — do NOT bundle a materially-different refresh into a PATCH envelope."*

- [ ] **Step 0.1: Read archived sources to capture baseline content**

Read both archived R8 entries. Note what fields / patterns / schema they document.

Run: `cat .claude/docs/superpowers/research/archive/claude-code-plugin-structure_2026-04-14.md` + same for session-jsonl-format.

Expected: both files exist (confirmed during spec review — 4023 B + 4487 B respectively). Note the frontmatter `expires_at: 2026-04-17`.

- [ ] **Step 0.2: WebSearch for claude-code-plugin-structure current state (2026)**

Run WebSearch with query: `"Claude Code plugin structure 2026 claude-plugin plugin.json skills directory"`

Expected: results describing current plugin-structure conventions. Compare against the baseline.

**Escape trigger**: if results surface a NEW required field in `.claude-plugin/plugin.json`, a NEW top-level directory convention beyond `skills/` / `templates/` / `hooks/`, or a STRUCTURAL change in how skills are discovered — **pause, escalate, route through v1.5.x**.

- [ ] **Step 0.3: WebSearch for claude-code-session-jsonl-format current state (2026)**

Run WebSearch with query: `"Claude Code session transcript JSONL format 2026 message record shape content blocks"`

Expected: results describing current JSONL record shape. Compare against the baseline.

**Escape trigger (any of these)**:
- a NEW top-level record type (beyond `user` / `assistant` / `system` etc.)
- a NEW redaction pattern convention
- a change in how content blocks are classified
- **schema drift** — content-block type rename (e.g. `text` → `text_block`), mandatory-field addition, required-key removal, field-semantics shift

If any trigger fires → **pause, escalate, route through v1.5.x** (structural refresh is not PATCH-appropriate).

- [ ] **Step 0.4: Gate decision**

If both Step 0.2 + Step 0.3 show currency refresh possible (content updates without structural change) → **proceed to Task 1**.

If either shows structural drift → **halt plan execution, escalate to user with a specific "v1.4.2 refresh not feasible as PATCH — needs v1.5.x structural update" brief**, save WebSearch findings as an R8 stub for the escalation.

---

## Task 1: Create research-templates/ directory + README.md

**Files:**
- Create: `skills/genesis-protocol/research-templates/README.md`
- Create: `skills/genesis-protocol/research-templates/sota/` (empty for now)
- Create: `skills/genesis-protocol/research-templates/stack/` (empty for now)

- [ ] **Step 1.1: Create directory skeleton**

Run: `mkdir -p skills/genesis-protocol/research-templates/sota skills/genesis-protocol/research-templates/stack`

Expected: both dirs created. Verify with `ls skills/genesis-protocol/research-templates/`.

- [ ] **Step 1.2: Write README.md**

Create `skills/genesis-protocol/research-templates/README.md` with content:

```markdown
<!-- SPDX-License-Identifier: MIT -->
# Research templates — genesis-protocol in-skill R8 bundle

## Purpose

R8 cache templates bundled with the `genesis-protocol` skill for downstream
project seeding at Phase 2 Step 2.3. Decouples downstream R8 cache seed from
plugin-envelope filesystem topology — works identically across dogfood,
`--plugin-dir`, and personal-scope (`~/.claude/skills/`) install modes.

## Structure

```
research-templates/
├── README.md       ← this file
├── sota/           ← state-of-the-art entries (TTL 7d in downstream cache)
│   ├── claude-code-plugin-distribution.md
│   ├── claude-ecosystem-cross-os.md
│   └── spdx-headers.md
└── stack/          ← stack / version-pin entries (TTL 1d in downstream cache)
    ├── claude-code-plugin-structure.md
    └── claude-code-session-jsonl-format.md
```

## Filename convention

Skill-local templates **drop the `_YYYY-MM-DD` date suffix** common in project
R8 caches. Date traceability lives in the frontmatter (`created_at` +
`expires_at`). The skill version pin (see `.claude-plugin/plugin.json`) is the
freshness anchor for templates.

## Copy discipline (Phase 2 Step 2.3)

When `genesis-protocol` Phase 2 Step 2.3 seeds the downstream project's R8
cache, it performs a **copy-and-rename** : each template file is copied to the
downstream `.claude/docs/superpowers/research/{sota,stack}/` with the seed
date appended to the filename (per downstream R8 convention :
`<topic>_<ISO-seed-date>.md`). The destination frontmatter `created_at` is
updated to the seed date; `expires_at` follows the normal R8 TTL from the
seed date. The template's original timestamps are preserved in the source
for audit.

## Refresh policy

Templates are maintained in lockstep with plugin releases. When a template's
content deviates from current-best-practice (e.g. Anthropic API surface
change, new Claude Code plugin convention), refresh before the next plugin
release. Downstream projects can independently refresh their copies post-seed
using the normal R8 cache workflow (Layer 0 research discipline).

**Escape clause (v1.4.2)**: if a refresh would introduce a structural /
breaking change (not just content currency), route the change through a
MINOR release, not a PATCH. Templates that evolve structurally are
plugin-release-gated.

## Cross-references

- Spec: `.claude/docs/superpowers/specs/v1_4_2_marketplace_unblock.md`
- Phase 2 Step 2.3 runbook: `skills/genesis-protocol/phase-1-rules-memory.md`
- R8 cache convention: Layer 0 `~/.claude/memory/layer0/workflow_research_and_memory.md`
```

- [ ] **Step 1.3: Verify README.md created correctly**

Run: `ls skills/genesis-protocol/research-templates/README.md && head -5 skills/genesis-protocol/research-templates/README.md`

Expected: file exists with SPDX header on line 1.

---

## Task 2: Copy-and-rename 3 active sota entries into research-templates/sota/

**Files:**
- Source: `.claude/docs/superpowers/research/sota/claude-code-plugin-distribution_2026-04-14.md`
- Source: `.claude/docs/superpowers/research/sota/claude-ecosystem-cross-os_2026-04-15.md`
- Source: `.claude/docs/superpowers/research/sota/spdx-headers_2026-04-14.md`
- Create: `skills/genesis-protocol/research-templates/sota/claude-code-plugin-distribution.md`
- Create: `skills/genesis-protocol/research-templates/sota/claude-ecosystem-cross-os.md`
- Create: `skills/genesis-protocol/research-templates/sota/spdx-headers.md`

- [ ] **Step 2.1: Copy plugin-distribution with date suffix stripped**

Run: `cp .claude/docs/superpowers/research/sota/claude-code-plugin-distribution_2026-04-14.md skills/genesis-protocol/research-templates/sota/claude-code-plugin-distribution.md`

Expected: file created. Verify with `ls skills/genesis-protocol/research-templates/sota/claude-code-plugin-distribution.md`.

**Note**: preserves frontmatter verbatim (including `created_at: 2026-04-14` + `expires_at`). Filename alone changes.

- [ ] **Step 2.2: Copy ecosystem-cross-os with date suffix stripped**

Run: `cp .claude/docs/superpowers/research/sota/claude-ecosystem-cross-os_2026-04-15.md skills/genesis-protocol/research-templates/sota/claude-ecosystem-cross-os.md`

Expected: file created.

- [ ] **Step 2.3: Copy spdx-headers with date suffix stripped**

Run: `cp .claude/docs/superpowers/research/sota/spdx-headers_2026-04-14.md skills/genesis-protocol/research-templates/sota/spdx-headers.md`

Expected: file created.

- [ ] **Step 2.4: Verify all 3 templates present with byte-count matching sources (pre-frontmatter-refresh)**

Run: `ls -la skills/genesis-protocol/research-templates/sota/`

Expected: 3 files, byte-count matches sources (the copy is verbatim before Step 2.5).

- [ ] **Step 2.5: Refresh frontmatter on the 3 copied templates — per in-skill refresh-policy**

**Why**: the source entries were created 2026-04-14 / 2026-04-15 (7-day TTL). At feat time (2026-04-19), `expires_at` in the source frontmatter is already near expiry (2026-04-21 / 2026-04-22). Templates that ship with an about-to-expire `expires_at` would force downstream seed-time refresh within days of seed. Per research-templates/README.md refresh-policy, templates track skill version — frontmatter dates should reflect the v1.4.2 ship date.

For each of the 3 copied sota templates, use Edit tool to update frontmatter fields:
- `created_at: 2026-04-14` (or `-04-15`) → `created_at: 2026-04-19`
- `expires_at: 2026-04-21` (or `-04-22`) → `expires_at: 2026-04-26` (7-day TTL from v1.4.2 ship date)
- `supersedes: null` (unchanged; these are direct copies, not supersessions — supersedes would only apply if refreshing content)
- Preserve all other frontmatter + body verbatim.

Verify post-edit: `grep "expires_at:" skills/genesis-protocol/research-templates/sota/*.md` → expect 3 lines, each `expires_at: 2026-04-26`.

**Alternative (if content currency preferred over date refresh)**: leave frontmatter verbatim and document in the README refresh-policy that skill-local template TTLs are advisory (skill version is the authoritative freshness anchor; downstream seed-time re-derives `expires_at` from seed date anyway per Task 7.4 copy-and-rename discipline). If this route chosen, skip the frontmatter edits and add a note to README.md § "Refresh policy" clarifying the precedence.

**Decision default**: execute the frontmatter refresh (primary path) since it matches the spec's "in-skill templates live alongside the skill version" discipline. Skip only if feat executor verifies README.md already documents the precedence clarification.

---

## Task 3: R8 refresh claude-code-plugin-structure (WebSearch + write)

**Files:**
- Create: `skills/genesis-protocol/research-templates/stack/claude-code-plugin-structure.md` (no date suffix, in-skill template)
- Create: `.claude/docs/superpowers/research/stack/claude-code-plugin-structure_2026-04-19.md` (with date suffix, project R8 cache)

**Context:** Archive at `.claude/docs/superpowers/research/archive/claude-code-plugin-structure_2026-04-14.md` (TTL expired 2026-04-17). Goal: refresh content currency without structural change (Task 0 escape clause already ruled structural drift out).

- [ ] **Step 3.1: WebSearch + WebFetch for latest plugin-structure docs**

Run WebSearch with targeted queries (2-3 searches):
- `"claude code plugin structure 2026 claude-plugin plugin.json"`
- `"claude code plugin skills directory install-manifest 2026"`
- `"claude code plugin marketplace submission requirements 2026"`

Synthesize current state. Compare against 2026-04-14 baseline to confirm content-only updates.

- [ ] **Step 3.2: Write in-skill template (no date suffix)**

Create `skills/genesis-protocol/research-templates/stack/claude-code-plugin-structure.md` with:
- SPDX-License-Identifier header
- Frontmatter (topic, type: stack, created_at: 2026-04-19, expires_at: 2026-04-20, status: active, confidence, scope: transverse, supersedes: `../archive/claude-code-plugin-structure_2026-04-14.md`)
- Body: refreshed content from WebSearch synthesis, focused on: `.claude-plugin/plugin.json` shape, `skills/`/`templates/`/`hooks/` root-level conventions, install-manifest.yaml patterns, marketplace install mode

Expected: file created at skill-local path.

- [ ] **Step 3.3: Write project R8 cache version (with date suffix)**

Create `.claude/docs/superpowers/research/stack/claude-code-plugin-structure_2026-04-19.md` with **identical content** to Step 3.2's file except:
- Filename has `_2026-04-19` suffix
- Frontmatter can have `created_at: 2026-04-19` matching

Expected: file created at project R8 cache path.

- [ ] **Step 3.4: Verify both files present + content-consistent**

Run: `diff skills/genesis-protocol/research-templates/stack/claude-code-plugin-structure.md .claude/docs/superpowers/research/stack/claude-code-plugin-structure_2026-04-19.md`

Expected: either zero diff (identical content) OR only frontmatter `created_at` line differs. Both files parse as valid YAML frontmatter + Markdown body.

---

## Task 4: R8 refresh claude-code-session-jsonl-format (WebSearch + write)

**Files:**
- Create: `skills/genesis-protocol/research-templates/stack/claude-code-session-jsonl-format.md`
- Create: `.claude/docs/superpowers/research/stack/claude-code-session-jsonl-format_2026-04-19.md`

Same pattern as Task 3, different topic.

- [ ] **Step 4.1: WebSearch for latest JSONL format + transcript schema**

Run WebSearch with queries:
- `"claude code session transcript JSONL format 2026"`
- `"claude code message record shape content blocks 2026"`
- `"claude code session archive redaction patterns 2026"`

Synthesize. Compare against 2026-04-15 baseline (the more recent of the two archived session-jsonl entries).

- [ ] **Step 4.2: Write in-skill template**

Create `skills/genesis-protocol/research-templates/stack/claude-code-session-jsonl-format.md` with:
- SPDX header, frontmatter (scope: transverse, TTL 1d, supersedes archive link)
- Body: current JSONL record shape, content-block type classification, redaction patterns for `session-post-processor` halt-on-leak gate downstream

- [ ] **Step 4.3: Write project R8 cache version**

Create `.claude/docs/superpowers/research/stack/claude-code-session-jsonl-format_2026-04-19.md` with identical content.

- [ ] **Step 4.4: Verify**

Run: `diff skills/genesis-protocol/research-templates/stack/claude-code-session-jsonl-format.md .claude/docs/superpowers/research/stack/claude-code-session-jsonl-format_2026-04-19.md`

Expected: zero or minimal (frontmatter-only) diff.

---

## Task 5: Update R8 project INDEX.md (2 entries archive → active)

**Files:**
- Modify: `.claude/docs/superpowers/research/INDEX.md`

- [ ] **Step 5.1: Read current INDEX.md state + probe anthropic-python archive status**

Run: `cat .claude/docs/superpowers/research/INDEX.md`

Expected: see `## Active` + `## Archive` sections. The `anthropic-python_2026-04-18.md` entry was last seen in Active with `expires 2026-04-19`. At feat time (likely 2026-04-19 or later), it may have already been moved to Archive per R8 session-open TTL discipline.

**Insertion-anchor probe**: determine where to insert the 2 new rows:
- If `anthropic-python` row still in `## Active` section → insert the 2 new refreshed-stack rows immediately after it (preserves stack-section grouping).
- If `anthropic-python` has been moved to `## Archive` → insert the 2 new rows at the end of the `## Active` table (as the first stack entries post-archival).
- In both cases, confirm the 2 new rows are contiguous and clearly demarcated as stack entries.

- [ ] **Step 5.2: Append 2 refreshed entries to Active table**

Edit the Active table to add 2 rows (insertion anchor determined by Step 5.1 probe):

```markdown
| [claude-code-plugin-structure](stack/claude-code-plugin-structure_2026-04-19.md) | stack | 2026-04-19 | 2026-04-20 | high | Refreshed for v1.4.2 marketplace unblock ship. `.claude-plugin/plugin.json` shape + skills/templates/hooks conventions + install-manifest patterns. Supersedes archive/claude-code-plugin-structure_2026-04-14.md. Also shipped in-skill at `skills/genesis-protocol/research-templates/stack/claude-code-plugin-structure.md` (no date suffix, skill-local canonical). |
| [claude-code-session-jsonl-format](stack/claude-code-session-jsonl-format_2026-04-19.md) | stack | 2026-04-19 | 2026-04-20 | high | Refreshed for v1.4.2 marketplace unblock ship. JSONL record shape + content-block classification + redaction patterns. Supersedes archive/claude-code-session-jsonl-format_2026-04-15.md. Also shipped in-skill. |
```

- [ ] **Step 5.3: Archive section annotation update**

Keep the 2 archive entries in `## Archive` with a supersession note (append `→ superseded by 2026-04-19 active entry` to each).

- [ ] **Step 5.4: Verify INDEX.md structure intact**

Run: `head -30 .claude/docs/superpowers/research/INDEX.md`

Expected: Active section now has 10 entries total, Archive still has 3 entries with supersession annotations.

---

## Task 6: Rewrite phase-1-rules-memory.md Step 1.3

**Files:**
- Modify: `skills/genesis-protocol/phase-1-rules-memory.md`

**Context:** Per spec § "Phase 1 Step 1.3 — rewrite". Drop legacy fallback paragraph (lines 71-72 current). Preserve "Why skill-local" (line 73), "Adaptation" (line 75), "Do not rewrite the rules" (line 80) paragraphs verbatim.

- [ ] **Step 6.1: Read current Step 1.3 (lines 61-82)**

Run: `sed -n '61,82p' skills/genesis-protocol/phase-1-rules-memory.md`

Expected: see current Source resolution + Fallback (legacy) paragraphs, followed by 3 preserved-verbatim paragraphs.

- [ ] **Step 6.2: Delete the "Fallback (legacy)" paragraph**

Use Edit tool to replace the legacy fallback paragraph with the single-path halt message per spec.

Target text to replace (presented below in a code fence so inner backticks are preserved verbatim — copy the exact content between the code fence markers as the `old_string` argument to Edit):

~~~
**Fallback (legacy)**: if `<skill_dir>/rules/v1_rules.md` is not present — which can only happen if the skill was installed from a source earlier than v1.2.1 — look for the file at `<plugin-root>/.claude/docs/superpowers/rules/v1_rules.md` (three levels above this skill's `SKILL.md`). If neither path resolves, halt and surface BOTH expected paths in the error message. Do not silently skip the rules copy.
~~~

Replacement text:
```markdown
**If the file is missing**: halt with a single-path error message:

```
Rules template not found at: <resolved_path>
This indicates a corrupted or incomplete skill install. Reinstall the
genesis-protocol skill (re-copy the full skills/genesis-protocol/
directory from the Genesis plugin source) and re-run Phase 1.
```

Do not attempt alternate locations. Do not silently skip the rules copy. A halt with clear remediation is better than a silent gap in the downstream project's rule enforcement.
```

- [ ] **Step 6.3: Verify preserved paragraphs intact**

Run: `grep -c "Why skill-local" skills/genesis-protocol/phase-1-rules-memory.md` → expect `1`.
Run: `grep -c "Adaptation" skills/genesis-protocol/phase-1-rules-memory.md` → expect `1` or more (may appear elsewhere).
Run: `grep -c "Do not rewrite" skills/genesis-protocol/phase-1-rules-memory.md` → expect `1`.

- [ ] **Step 6.4: Verify legacy fallback gone**

Note: Step 1.3 (line 71) contains "three levels above"; Step 2.3 (line 246) contains "three levels up from". Different exact phrasing. After Task 6 deletion, only Step 2.3's "three levels up" phrase remains (fixed in Task 7).

Run: `grep -c "three levels above" skills/genesis-protocol/phase-1-rules-memory.md` → expect `0` (Step 1.3 reference deleted).
Run: `grep -c "three levels up" skills/genesis-protocol/phase-1-rules-memory.md` → expect `1` (Step 2.3 still has it, will be fixed in Task 7).
Run: `grep -c "Fallback (legacy)" skills/genesis-protocol/phase-1-rules-memory.md` → expect `0`.

---

## Task 7: Rewrite phase-1-rules-memory.md Step 2.3 + patch table Source column

**Files:**
- Modify: `skills/genesis-protocol/phase-1-rules-memory.md`

**Context:** Per spec § "Phase 2 Step 2.3 — rewrite". Two sub-edits: (a) rewrite opening paragraph (current line 246), (b) patch 5-row table Source column (lines 250-258 current). Preserve follow-on paragraph (line 248) + expiration discipline paragraph (line 260) verbatim.

- [ ] **Step 7.1: Read current Step 2.3 + table**

Run: `sed -n '244,261p' skills/genesis-protocol/phase-1-rules-memory.md`

Expected: see current opening paragraph (line 246 three-levels-up), follow-on (line 248), table (lines 250-258), expiration note (line 260).

- [ ] **Step 7.2: Rewrite the opening paragraph (line 246)**

Use Edit tool. Both target text and replacement shown in outer `~~~` fences so inner backticks render verbatim (no escape gymnastics). Copy the content between the fence markers literally as `old_string` / `new_string`.

**Target text (current line 246)** — to pass as `old_string`:

~~~
The Genesis plugin ships its own R8 cache at `<plugin-root>/.claude/docs/superpowers/research/` — where `<plugin-root>` is derived via the same "three levels up from `skills/genesis-protocol/SKILL.md`" rule used at Phase 1 Step 1.3. This cache contains entries that are also relevant to any downstream project, specifically the ones about Claude Code itself (plugin structure, session JSONL format, in-IDE tools, cross-OS ecosystem). Phase 2 **copies** these entries — not by-reference, because they are project-level references the downstream project needs to read offline.
~~~

**Replacement** — to pass as `new_string`:

~~~
The Genesis plugin ships R8 cache **templates** inside this skill at `<skill_dir>/research-templates/` — the canonical five entries listed in the "Entries to copy" table below (3 sota + 2 stack) relevant to any downstream Claude-Code-based project. Phase 2 copies these templates into the downstream project's `.claude/docs/superpowers/research/` (the conventional R8 cache location). Post-copy, the downstream project owns its cache independently; refreshing entries is a downstream-project concern.

**Source resolution (v1.4.2)**: identical discipline to Phase 1 Step 1.3. `<skill_dir>/research-templates/` is the single authoritative source. No fallback to `<plugin-root>/.claude/docs/superpowers/research/`. If the templates directory is missing, halt with a single-path error message:

```
R8 cache templates not found at: <resolved_path>
This indicates a corrupted or incomplete skill install. Reinstall the
genesis-protocol skill and re-run Phase 2.
```
~~~

- [ ] **Step 7.3: Patch 5-row table Source column — 5 surgical Edit calls**

Each row is edited separately with a verbatim before-text. The `old_string` per Edit call MUST include the full row (from leading `|` to trailing `|`) to guarantee unique match — not just the Source fragment. Destination + "Why copy not link" columns preserved verbatim in each new_string.

- [ ] **Step 7.3.1: Row 1 — claude-code-plugin-distribution**

Edit old_string:
~~~
| `sota/claude-code-plugin-distribution_*.md` | `sota/` in downstream | Every Genesis downstream may ship as a plugin — needs local reference |
~~~

Edit new_string:
~~~
| `<skill_dir>/research-templates/sota/claude-code-plugin-distribution.md` | `sota/` in downstream | Every Genesis downstream may ship as a plugin — needs local reference |
~~~

- [ ] **Step 7.3.2: Row 2 — claude-code-plugin-structure**

Edit old_string:
~~~
| `stack/claude-code-plugin-structure_*.md` | `stack/` in downstream | Same reason — plugin structure is consumed at every session |
~~~

Edit new_string:
~~~
| `<skill_dir>/research-templates/stack/claude-code-plugin-structure.md` | `stack/` in downstream | Same reason — plugin structure is consumed at every session |
~~~

- [ ] **Step 7.3.3: Row 3 — claude-code-session-jsonl-format**

Edit old_string:
~~~
| `stack/claude-code-session-jsonl-format_*.md` | `stack/` in downstream | Needed for `session-post-processor` to run on the downstream's sessions |
~~~

Edit new_string:
~~~
| `<skill_dir>/research-templates/stack/claude-code-session-jsonl-format.md` | `stack/` in downstream | Needed for `session-post-processor` to run on the downstream's sessions |
~~~

- [ ] **Step 7.3.4: Row 4 — claude-ecosystem-cross-os**

Edit old_string:
~~~
| `sota/claude-ecosystem-cross-os_*.md` | `sota/` in downstream | Multidevice refs used by Phase -1 and Phase 7 across OS |
~~~

Edit new_string:
~~~
| `<skill_dir>/research-templates/sota/claude-ecosystem-cross-os.md` | `sota/` in downstream | Multidevice refs used by Phase -1 and Phase 7 across OS |
~~~

- [ ] **Step 7.3.5: Row 5 — spdx-headers**

Edit old_string:
~~~
| `sota/spdx-headers_*.md` | `sota/` in downstream | SPDX rule is enforced in R10 — the reference must be local |
~~~

Edit new_string:
~~~
| `<skill_dir>/research-templates/sota/spdx-headers.md` | `sota/` in downstream | SPDX rule is enforced in R10 — the reference must be local |
~~~

**Row membership preserved identically** — 5 rows in the same order, only Source column cell text changes. Destination + rationale columns verbatim. Post-edits, verify via `grep -c "research-templates" skills/genesis-protocol/phase-1-rules-memory.md` → expect ≥ 5 (5 table rows + surrounding narrative).

- [ ] **Step 7.4: Copy-and-rename discipline note appended after table**

Append a paragraph after the expiration discipline line (currently line 260) explaining the copy-and-rename pattern:

```markdown
**Copy-and-rename discipline**: the skill-local templates drop the `_YYYY-MM-DD` suffix (skill version pin = freshness anchor). When seeded into the downstream project's cache, the copy adds the seed date to the filename per downstream R8 convention (e.g. skill-local `sota/claude-code-plugin-distribution.md` → downstream `sota/claude-code-plugin-distribution_<seed-date>.md`). The destination frontmatter `created_at` is updated to the seed date; `expires_at` follows the normal R8 TTL from the seed date.
```

- [ ] **Step 7.5: Verify Step 2.3 post-rewrite**

Run: `grep -c "three levels up" skills/genesis-protocol/phase-1-rules-memory.md` → expect `0` (all references gone).
Run: `grep -c "research-templates" skills/genesis-protocol/phase-1-rules-memory.md` → expect `6+` (opening paragraph + 5 table rows + copy-discipline paragraph + README refs).
Run: `sed -n '246p' skills/genesis-protocol/phase-1-rules-memory.md` → expect the new opening paragraph.

---

## Task 8: Update install-manifest.yaml

**Files:**
- Modify: `skills/genesis-protocol/install-manifest.yaml`

**Context:** Per spec § "install-manifest.yaml updates". Version bump + 10 new checks.

- [ ] **Step 8.1: Bump version 0.8.0 → 1.4.2**

Use Edit tool. Target: `version: 0.8.0` → Replace with: `version: 1.4.2`.

Verify: `grep '^version:' skills/genesis-protocol/install-manifest.yaml` → `version: 1.4.2`.

- [ ] **Step 8.2: Append 10 new verification checks**

After the last existing `check:` entry (the one for `verification.md`, currently ends around line 177), append 10 new check blocks per spec § "install-manifest.yaml updates" (b). Each check has `check:`, `path:`, `on_fail:` keys.

Exact content per spec lines 145-205 of the spec file (verbatim copy).

- [ ] **Step 8.3: Verify install-manifest.yaml still valid YAML**

Run: `python -c "import yaml; yaml.safe_load(open('skills/genesis-protocol/install-manifest.yaml'))" && echo "YAML OK"`

Expected: `YAML OK`.

- [ ] **Step 8.4: Verify check count**

Run: `grep -c "^  - check:" skills/genesis-protocol/install-manifest.yaml`

Expected: previous **17** checks + 10 new = **27 checks total**. (Pre-polish baseline: filesystem-grounded count via `grep -c` on the actual current file, not memory-assumed 13.)

---

## Task 9: Append v1.4.2 scenarios S1-S3 to verification.md

**Files:**
- Modify: `skills/genesis-protocol/verification.md`

- [ ] **Step 9.1: Read current verification.md tail**

Run: `tail -30 skills/genesis-protocol/verification.md`

Identify insertion point (end of file, after last existing scenario).

- [ ] **Step 9.2: Append v1.4.2 scenarios section**

Append to end of file:

```markdown

## v1.4.2 — Marketplace unblock scenarios

| # | Scenario | Expected |
|---|---|---|
| S1 | Personal-scope install verification — after `cp -r skills/genesis-protocol ~/.claude/skills/`, run `/genesis-protocol` on a fresh empty cwd. | Phase 1 Step 1.3 resolves `<skill_dir>/rules/v1_rules.md` as `~/.claude/skills/genesis-protocol/rules/v1_rules.md`. File is present (shipped with the skill). Rules are copied to `<cwd>/.claude/docs/superpowers/rules/v1_rules.md` successfully. Zero three-levels-up probe. Zero halt. |
| S2 | Phase 2 R8 cache seed from skill-local templates — after a Phase 1 success, run Phase 2. | Step 2.3 resolves `<skill_dir>/research-templates/sota/` and `<skill_dir>/research-templates/stack/`. All 5 entries (3 sota + 2 stack) are copied to `<cwd>/.claude/docs/superpowers/research/`. Filenames at destination include `_<seed-date>` suffix per R8 downstream convention. `INDEX.md` is populated with all 5 entries. Zero three-levels-up probe. |
| S3 | Install-manifest verification catches missing rules/ — manually delete `skills/genesis-protocol/rules/v1_rules.md` from a dogfood install, run install verification. | Verification fails loudly with the specific error message for the missing file, naming the exact expected path. Does not fall through to a legacy fallback. Does not silently succeed. Reinstall remediation is clearly surfaced. |

**Regression probes** — v1.4.1 scenarios #40-#44 (Layer B citation rendering) unchanged since zero Layer B touch in v1.4.2. v1.4.0 fallback scenarios #29, #32, #33, #38 unchanged. v1.3.x scenarios unchanged.

**Runtime replay note**: S1 is replayable standalone via a test install path. S2 is replayable as an S1→S2 chain. S3 is replayable standalone via `rm skills/genesis-protocol/rules/v1_rules.md` + re-run install-manifest verification. Per the v1.3.1 → v1.4.1 convention, runtime replay deferred if in-session replay is not practical — −0.2 Pain-driven deduction per replay-deferred scenario rolls forward.
```

- [ ] **Step 9.3: Verify scenarios appended**

Run: `grep -c "^| S[1-3] |" skills/genesis-protocol/verification.md`

Expected: `3`.

---

## Task 10: Bump plugin.json version

**Files:**
- Modify: `.claude-plugin/plugin.json`

- [ ] **Step 10.1: Read current plugin.json**

Run: `cat .claude-plugin/plugin.json`

Expected: see `"version": "1.4.1"` line.

- [ ] **Step 10.2: Bump to 1.4.2**

Edit: `"version": "1.4.1"` → `"version": "1.4.2"`.

- [ ] **Step 10.3: Verify valid JSON + version correct**

Run: `python -c "import json; d = json.load(open('.claude-plugin/plugin.json')); print(d['version'])"`

Expected: `1.4.2`.

---

## Task 11: Verification probes (pre-commit gate)

**Files:** (read-only, no file changes)

- [ ] **Step 11.1: Layer A zero-ripple check**

Run: `git diff main --stat -- skills/genesis-drop-zone/`

Expected: **empty output** (zero lines). Layer A byte-identical across v1.4.1 → v1.4.2 boundary.

- [ ] **Step 11.2: Canonical 5 bundle consistency across all surfaces**

Run these 5 grep counts across the whole worktree:
```bash
grep -r -c "claude-code-plugin-distribution" skills/ .claude/docs/superpowers/ | grep -v ":0$"
grep -r -c "claude-ecosystem-cross-os" skills/ .claude/docs/superpowers/ | grep -v ":0$"
grep -r -c "spdx-headers" skills/ .claude/docs/superpowers/ | grep -v ":0$"
grep -r -c "claude-code-plugin-structure" skills/ .claude/docs/superpowers/ | grep -v ":0$"
grep -r -c "claude-code-session-jsonl-format" skills/ .claude/docs/superpowers/ | grep -v ":0$"
grep -r -c "open-source-license-for-dev-tooling" skills/ .claude/docs/superpowers/ | grep -v ":0$"
```

Expected:
- Canonical 5 each present in: spec + phase-1-rules-memory.md table + install-manifest + research-templates + INDEX.md
- `open-source-license-for-dev-tooling`: **zero matches in `skills/` subtree** (still present in project R8 active cache as a sota entry, which is fine — it just shouldn't be part of the v1.4.2 bundle)

- [ ] **Step 11.3: YAML validity of install-manifest**

Run: `python -c "import yaml; m = yaml.safe_load(open('skills/genesis-protocol/install-manifest.yaml')); print('version:', m['version'], 'checks:', len(m['verification']))"`

Expected: `version: 1.4.2 checks: 27`.

- [ ] **Step 11.4: JSON validity of plugin.json**

Run: `python -c "import json; print(json.load(open('.claude-plugin/plugin.json'))['version'])"`

Expected: `1.4.2`.

- [ ] **Step 11.5: phase-1-rules-memory.md "three levels up" count = 0**

Run: `grep -c "three levels" skills/genesis-protocol/phase-1-rules-memory.md`

Expected: `0`.

- [ ] **Step 11.6: research-templates/ has 6 files (README + 3 sota + 2 stack)**

Run: `find skills/genesis-protocol/research-templates -type f | wc -l`

Expected: `6`.

- [ ] **Step 11.7: verification.md has 3 new scenarios**

Run: `grep -c "^| S[1-3] |" skills/genesis-protocol/verification.md`

Expected: `3`.

---

## Task 12: Feat commit

**Files:** all modified/created files from Tasks 1-10.

- [ ] **Step 12.1: Stage all feat-related files**

Run:
```bash
git add skills/genesis-protocol/research-templates/
git add skills/genesis-protocol/phase-1-rules-memory.md
git add skills/genesis-protocol/install-manifest.yaml
git add skills/genesis-protocol/verification.md
git add .claude-plugin/plugin.json
git add .claude/docs/superpowers/research/INDEX.md
git add .claude/docs/superpowers/research/stack/claude-code-plugin-structure_2026-04-19.md
git add .claude/docs/superpowers/research/stack/claude-code-session-jsonl-format_2026-04-19.md
```

- [ ] **Step 12.2: Verify staging**

Run: `git diff --cached --stat`

Expected: 10-12 files staged, ~300-500 insertions, ~15-25 deletions (the runbook rewrites + plugin.json + install-manifest).

- [ ] **Step 12.3: Commit feat**

Commit message (HEREDOC):
```
feat: v1.4.2 — marketplace unblock (genesis-protocol install-path resolution)

Closes dogfood Friction #4 (plugin root resolution BLOCKER for marketplace
install) + Friction #5 (missing R8 stack entries from skill package) from the
2026-04-18 v1.4.1 stress-test dogfood. Pain source:
memory/project/dogfood_v1.4.1_stress_2026-04-18/stress_test_report.md

Changes:

1. phase-1-rules-memory.md Step 1.3: legacy "three levels up" fallback
   removed. Single canonical path <skill_dir>/rules/v1_rules.md. Halt-with-
   remediation on missing.

2. phase-1-rules-memory.md Step 2.3: resolver rewritten to skill-local
   <skill_dir>/research-templates/. 5-row Source column patched. Follow-on
   rationale paragraph + expiration discipline preserved verbatim.

3. skills/genesis-protocol/research-templates/ created with 3 sota copy-
   and-renamed from active R8 (plugin-distribution + cross-os + spdx-headers)
   + 2 stack R8-refreshed via WebSearch (plugin-structure + session-jsonl-
   format) + README.md documenting purpose + refresh policy. No date suffix
   on filenames — skill version pin = freshness anchor.

4. install-manifest.yaml: version 0.8.0 -> 1.4.2 + 10 new verification
   checks (rules file + templates dir + README + sota/stack subdirs + 5
   individual template files). Total 23 checks.

5. verification.md: 3 new scenarios S1 (personal-scope install rules
   resolution), S2 (Phase 2 R8 seed from skill-local), S3 (install-manifest
   catches missing skill-local rules).

6. plugin.json: version 1.4.1 -> 1.4.2.

7. R8 INDEX.md: 2 refreshed stack entries re-entered in ## Active section
   with fresh 2026-04-20 expires_at. Archive entries retain supersession
   notes.

Zero Layer A ripple (skills/genesis-drop-zone/ byte-identical, verified).
Zero schema bump. Zero new privilege class. Zero new bilingual pair.

Anti-Frankenstein retroactive: the legacy fallback was v1.2.1 F29
belt-and-suspenders, three versions of zero-hit dead code retired.

Halt-with-remediation discipline travels from v1.5.0 spec (parallel branch
feat/v1.5.0-living-memory commit 59a7640) to v1.4.2 install-path
resolution. No silent middle state anywhere.

Self-rating projection: Pain-driven 9.3-9.4 (dogfood BLOCKER), Prose
cleanliness 9.1-9.2 (surgical edits), Best-at-date 9.0-9.2 (R8 refresh of
2 archived entries current-at-date), Self-contained 9.3-9.4, Anti-
Frankenstein 9.3-9.4. Average ~= 9.2-9.3. 11th consecutive ship >= 9.0.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

- [ ] **Step 12.4: Verify commit**

Run: `git log --oneline | head -3`

Expected: top commit is the v1.4.2 feat, preceded by spec polish 2 (7ff7319) + spec polish (8bc2932).

---

## Task 13: Chore commit

**Files:**
- Modify: `CHANGELOG.md`
- Create: `memory/project/session_v1_4_2_marketplace_unblock.md`
- Modify: `memory/MEMORY.md`
- Create: `.claude/docs/superpowers/resume/2026-04-19_v1_4_2_to_v1_4_3_or_v1_5_0.md`

- [ ] **Step 13.1: Append CHANGELOG entry**

Add v1.4.2 entry at top of CHANGELOG.md, following v1.4.1 pattern. Include: summary, Changed section (Phase 1/2 runbook rewrites + install-manifest + plugin.json), Added section (research-templates/ + 2 R8 refreshes + 3 verification scenarios), Removed section (legacy "three levels up" fallback), 5-axis self-rating table, cross-ref to pain source + v1.5.0 parallel branch.

- [ ] **Step 13.2: Write session trace**

Create `memory/project/session_v1_4_2_marketplace_unblock.md` with frontmatter (type: project, date: 2026-04-19, session: v1.4.2, branch: feat/v1.4.2-marketplace-unblock, parent-tag: v1.4.1, parent-commit: aec57ab) + body covering: why this ship, dogfood pain sources, 6-commit rhythm application (with chore-archive 35c8b72 outside the count), 3-iteration spec review loop, verification probes results, ship gates, self-rating final.

- [ ] **Step 13.3: Update MEMORY.md pointer**

Add one-line pointer for the v1.4.2 session trace in the Project section, before the dogfood archive pointer (chronological).

- [ ] **Step 13.4: Write resume prompt v1.4.2 → next**

Create `.claude/docs/superpowers/resume/2026-04-19_v1_4_2_to_v1_4_3_or_v1_5_0.md` with: what v1.4.2 shipped, current state (branch, tags, skill count unchanged, privilege map unchanged), candidates for next session (v1.5.0 spec review loop resume on parallel branch + plan + feat vs other direction), R8 cache state, exact phrase for next session with PowerShell launcher.

- [ ] **Step 13.5: Stage + commit chore**

```bash
git add CHANGELOG.md memory/project/session_v1_4_2_marketplace_unblock.md memory/MEMORY.md .claude/docs/superpowers/resume/2026-04-19_v1_4_2_to_v1_4_3_or_v1_5_0.md
git commit -m "chore(memory): v1.4.2 — CHANGELOG + session trace + MEMORY pointer + resume"
```

Expected: 4 files committed, chore commit added to branch.

---

## Task 14: R2.3.1 gh pre-flight + PR create

**Files:** none (GitHub side)

- [ ] **Step 14.1: R2.3.1 gh active account verification**

Run: `gh api user --jq .login && git remote get-url origin`

Expected: `gh` active account = `myconciergerie-prog` (target owner), origin URL contains `myconciergerie-prog/project-genesis`.

If mismatch: `gh auth switch --user myconciergerie-prog` + re-verify.

- [ ] **Step 14.2: Push branch**

Run: `git push -u origin feat/v1.4.2-marketplace-unblock`

Expected: branch pushed to remote.

- [ ] **Step 14.3: Create PR**

Run:
```bash
gh pr create --title "v1.4.2 — marketplace unblock (genesis-protocol install-path resolution)" --body "<PR body with Summary + Test plan + pain-source pointer>"
```

Expected: PR URL returned.

- [ ] **Step 14.4: Open PR in Chrome Profile 2 proactively**

Per Layer 0 `feedback_proactive_chrome_profile_open.md`, open the PR URL in Chrome Profile 2 (`myconciergerie@gmail.com`) for user review.

---

## Task 15: Merge + tag v1.4.2 (post user validation)

**Files:** none (GitHub + git side)

- [ ] **Step 15.1: User validates PR**

Wait for user's explicit approval before merging.

- [ ] **Step 15.2: Merge PR (no --delete-branch per R2.1)**

Run: `gh pr merge <pr-number> --squash` (or `--merge` per user preference).

**Do NOT use `--delete-branch`** per Layer 0 `feedback_r21_delete_branch_recovery.md`. Branch stays preserved.

- [ ] **Step 15.3: Tag v1.4.2**

Run:
```bash
git checkout main
git pull origin main
git tag v1.4.2
git push origin v1.4.2
```

Expected: tag created + pushed.

- [ ] **Step 15.4: Verify release visible on GitHub**

Run: `gh release view v1.4.2` OR `gh api repos/myconciergerie-prog/project-genesis/tags | jq '.[0].name'`

Expected: `v1.4.2` tag present.

---

## Review checkpoints

After Task 6 + 7 (runbook rewrites): ask user to eyeball Step 1.3 + Step 2.3 changes before continuing.

After Task 11 (verification probes): if any probe fails, halt + escalate before feat commit. Do not commit a broken state.

After Task 14 (PR create): user validation required before Task 15 merge + tag.

---

## Risk register

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Task 0 WebSearch reveals breaking change | Low-Medium | High | Escape clause: halt, escalate, route through v1.5.x |
| Task 7 Edit drift on 5-row table (row membership accidentally swapped) | Low | High | Post-edit grep probe Task 11.2 catches bundle inconsistency |
| Task 8 install-manifest YAML indentation error | Low | Medium | Task 8.3 YAML validation catches |
| Task 11 Layer A ripple detected | Very low | High | Immediate halt + root-cause diagnosis (should be impossible if plan followed) |
| Task 14 gh account mismatch | Medium | Low | R2.3.1 pre-flight catches before PR create |
| Task 15 PR merge conflicts with main | Low | Medium | Worktree was created off latest main (aec57ab); only conflict source would be parallel v1.5.0 branch work, which is on separate branch |

---

## Deferred items (post-v1.4.2)

- v1.5.0 spec review loop resume (`feat/v1.5.0-living-memory` branch commit `59a7640`) + plan + feat
- Friction #1 + #2 + #3 (multi-file seed + chronological override + reconciliation policy) → v1.5.0 scope
- Friction #6 (TTL frontmatter parsing vs filename) → v1.5.1+ polish

---

## Commit summary (end-of-ship state)

After Task 15, `feat/v1.4.2-marketplace-unblock` branch will have:

1. `35c8b72` chore(dogfood) — archive v1.4.1 stress-test artefacts (pre-plan, forensic)
2. `62fee9f` spec — v1.4.2 marketplace unblock
3. `8bc2932` spec polish — 3 P1 + 5 P2 + 2 P3 advisories landed
4. `7ff7319` spec polish 2 — P2-1 regression fix
5. *(plan commit — implicit via saving this file at Task 0 pre-flight completion)*
6. *(plan polish commit — implicit after plan-reviewer pass)*
7. *(feat commit — Task 12)*
8. *(chore commit — Task 13)*

Plus: PR merged to main, v1.4.2 tag pushed.

**6-commit rhythm discipline**: the 6 counted commits are (spec + spec-polish + plan + plan-polish + feat + chore). The `7ff7319` spec polish 2 counts as continuation of spec-polish (same review loop), and `35c8b72` chore(dogfood) is pre-ship forensic archival outside the 6-count. Running rhythm: 7th consecutive application.
