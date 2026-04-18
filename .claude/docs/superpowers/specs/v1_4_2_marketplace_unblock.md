<!-- SPDX-License-Identifier: MIT -->
---
name: v1.4.2 marketplace unblock — `genesis-protocol` install-path resolution
description: Focused PATCH spec addressing Friction #4 + #5 from the 2026-04-18 v1.4.1 stress-test dogfood. Fixes `genesis-protocol` Phase 1 rules resolver and Phase 2 R8 cache seed resolver so both work in all three install modes (dogfood / plugin-dir / personal-scope) without relying on the dogfood-specific "3 levels up" plugin envelope. Ships 5 R8 stack-relevant entries inside the skill package at `skills/genesis-protocol/research-templates/` so downstream projects get a complete seed without cross-repo dependencies.
type: spec
version: v1.4.2
target_ship: 2026-04-18
parent_ship: v1.4.1 (aec57ab)
pain_source: memory/project/dogfood_v1.4.1_stress_2026-04-18/stress_test_report.md
---

# v1.4.2 — Marketplace unblock

## Problem statement — two dogfood-observed frictions

On 2026-04-18 the first end-to-end Genesis dogfood since v1.2.0 (colocs-tracker stress test) surfaced two BLOCKERS for any install mode other than dogfood:

- **Friction #4** — Phase 1 Step 1.3 declares skill-local resolution as primary (`<skill_dir>/rules/v1_rules.md`) but still documents a legacy "three levels above this skill's SKILL.md" fallback. When Genesis is installed at `~/.claude/skills/genesis-protocol/` (personal scope), the fallback resolves to `~/.claude/.claude/docs/superpowers/rules/v1_rules.md` — a nonexistent double-`.claude` path. If for any reason the skill-local path is not populated (incomplete distribution bundle), the orchestrator falls through to this broken fallback and either halts with a confusing error or silently continues without the rules copy. **Blocks marketplace install + any machine where Genesis is not a dev-repo clone.**
- **Friction #5** — Phase 2 Step 2.3 copies R8 research entries from `<plugin-root>/.claude/docs/superpowers/research/` (same "three levels above SKILL.md" rule). This path only exists in the dogfood source — it is not part of the distributed skill package. 2 of 5 canonical stack entries (`claude-code-plugin-structure`, `claude-code-session-jsonl-format`) are currently archived in the dogfood source and thus unavailable to the Phase 2 copy even in dogfood mode. **Blocks downstream `session-post-processor` end-to-end operation on any bootstrapped project.**

Both frictions trace to the same architectural mistake: the orchestrator still depends on the plugin-envelope filesystem topology that the v1.2.1 F29 fix was supposed to retire. v1.2.1 moved the rules template in-skill but retained the fallback as a belt-and-suspenders measure; v1.4.2 completes the retirement.

## Scope — v1.4.2

### In scope

1. **Phase 1 Step 1.3 resolver — single canonical path, drop legacy fallback** — `phase-1-rules-memory.md` Step 1.3 is rewritten to declare `<skill_dir>/rules/v1_rules.md` as the sole source. The "fallback (legacy)" paragraph describing the three-levels-up resolution is deleted. If the skill-local file is absent, halt with an error pointing at the expected path and asking the user to reinstall the skill — no silent fallback, no double-path probing. Simpler resolver, stronger guarantee.
2. **Skill-local R8 cache templates directory** — new directory `skills/genesis-protocol/research-templates/` created inside the skill package. Contains the five canonical entries listed verbatim in the current Phase 2 Step 2.3 "Entries to copy" table (preserving the existing bundle membership — no narrowing, no additions):
   - `sota/claude-code-plugin-distribution.md` (self-hosted marketplace + official Anthropic marketplace)
   - `stack/claude-code-plugin-structure.md` (`.claude-plugin/plugin.json` + root-level dirs, **refreshed from archive for v1.4.2 ship**)
   - `stack/claude-code-session-jsonl-format.md` (transcript schema + redaction patterns, **refreshed from archive for v1.4.2 ship**)
   - `sota/claude-ecosystem-cross-os.md` (per-OS capability matrix; Claude Code Remote Control; 280 verified MCP connectors)
   - `sota/spdx-headers.md` (canonical SPDX per file type)
   These entries are **templates** — downstream projects copy them at Phase 2, optionally re-fetching the underlying research for freshness. They travel with the skill so install-path topology no longer matters. Bundle membership preserved identically to the existing Phase 2 Step 2.3 table — the spec intentionally does NOT narrow or expand the set.
3. **Phase 2 Step 2.3 resolver — skill-local R8 cache seed** — the Phase 2 R8 cache seed step is rewritten to read from `<skill_dir>/research-templates/{sota,stack}/` instead of `<plugin-root>/.claude/docs/superpowers/research/`. Target destination unchanged (`<downstream>/.claude/docs/superpowers/research/`). No legacy fallback — same discipline as Step 1.3.
4. **`install-manifest.yaml` verification** — version bumped `0.8.0` → `1.4.2` (stale since v0.8 release). **Ten new checks** added (enumerated in the Design section install-manifest subsection): (i) `rules/v1_rules.md` file_exists, (ii) `research-templates/` directory_exists, (iii) `research-templates/README.md` file_exists, (iv) `research-templates/sota/` directory_exists, (v) `research-templates/stack/` directory_exists, (vi-x) five `file_exists` for each individual template entry. These checks fail loudly if the distribution bundle is incomplete — preventing a broken marketplace install from silently shipping to users.
5. **R8 refresh of 2 archived stack entries** — `claude-code-plugin-structure` and `claude-code-session-jsonl-format` are currently archived (TTL expired 2026-04-17). v1.4.2 ships them as `research-templates/stack/<topic>.md` (no date suffix, since they live in-skill and are refreshed per skill version) with content freshened via web research during feat commit. Frontmatter preserves `expires_at` with a new TTL so downstream projects' session-open stack-check discipline works correctly.
6. **Documentation updates** — `CLAUDE.md` at project root: the R8 active-entries bullet list already mentions `claude-code-plugin-structure` + `claude-code-session-jsonl-format`; v1.4.2 does not restructure the list. What actually changes: `.claude/docs/superpowers/research/INDEX.md` moves those 2 entries from `## Archive` section (current state per the INDEX lines 23-26) back to `## Active` with fresh `expires_at` dates. The 2 entries also materialise on disk at `.claude/docs/superpowers/research/stack/<topic>_<seed-date>.md` (dogfood source R8 cache, post-refresh). The in-skill `research-templates/stack/<topic>.md` files are a separate concern (new templates, no date suffix, no archive/active dichotomy — they track skill version). `memory/master.md` cross-skill-pattern references unchanged (v1.4.2 touches no cross-skill pattern).
7. **Verification scenarios** — 3 new scenarios added to `skills/genesis-protocol/verification.md`: (a) user-scope install runtime — Phase 1 Step 1.3 resolves `<skill_dir>/rules/v1_rules.md` correctly without any three-levels-up probe, rules seeded to downstream cleanly, (b) Phase 2 runtime — Step 2.3 copies all 5 templates from skill-local `<skill_dir>/research-templates/` to downstream `.claude/docs/superpowers/research/` without cross-repo dependency, (c) install-manifest catches missing skill-local rules file — verification fails loudly with specific path-based error message rather than silent fallback.

### Out of scope (deferred)

- **Friction #1 + #2 + #3** (multi-file seed + chronological override + reconciliation policy) — these validate and motivate v1.5.0 scope; they are deferred to the v1.5.0 MINOR already spec'd on `feat/v1.5.0-living-memory` (commit `59a7640`).
- **Friction #6** (TTL frontmatter parsing vs filename) — v1.5.1+ polish. Pain-driven threshold not yet reached: the dogfood report itself says verbatim *"No friction in this case"* (the 3 copied entries at day 3-4 of their 7-day TTL were still valid; no forensic drift observed). Deferred honestly.
- **Schema version bump** — v1.4.2 is file-path + bundle-content changes, not a schema change. `schema_version: 1` on `drop_zone_intent.md` preserved. Plugin `version: 1.4.1 → 1.4.2`.
- **Genesis-drop-zone changes** — zero Layer A touch; `genesis-drop-zone` skill package byte-identical across the v1.4.1 → v1.4.2 boundary.
- **Other sibling skills** — zero touch on `phase-minus-one` / `phase-5-5-auth-preflight` / `journal-system` / `session-post-processor` / `pepite-flagging`.

### Rationale for v1.4.2 route (inline, elaborated in § "Rationale for v1.4.2 route" below)

- **PATCH honest** — no new privilege, no new schema, no new subprocess, no new network call, no bilingual pair, no cross-skill-pattern change. Pure install-path resolution fix + distribution bundle completion. PATCH is the honest tranche.
- **Pain-driven purity** — both frictions were dogfood-observed BLOCKERS, not speculative. Pain-driven axis projected 9.3-9.4.
- **Anti-Frankenstein retroactive** — removes the legacy "three levels up" fallback that v1.2.1 retained as a safety net but is now strictly dead weight for any v1.2.1+ install. Dropping it simplifies the resolver without losing any coverage (users on pre-v1.2.1 installs are quasi-inexistent — the v1.2.1 ship itself fixed F29).
- **Bundle completion** — the skill package now carries everything it needs (rules + R8 cache templates). Install-path topology is decoupled from the orchestrator's behaviour.

## Design

### Phase 1 Step 1.3 — rewrite

**Current (v1.4.1)** — documented in worktree's `phase-1-rules-memory.md`:

> **Source resolution**: the canonical rules template lives inside this skill at `<skill_dir>/rules/v1_rules.md`, where `<skill_dir>` is the directory containing this skill's `SKILL.md`. [...]
>
> **Fallback (legacy)**: if `<skill_dir>/rules/v1_rules.md` is not present — which can only happen if the skill was installed from a source earlier than v1.2.1 — look for the file at `<plugin-root>/.claude/docs/superpowers/rules/v1_rules.md` (three levels above this skill's `SKILL.md`). If neither path resolves, halt and surface BOTH expected paths in the error message. Do not silently skip the rules copy.

**v1.4.2 rewrite**:

> **Source resolution (v1.4.2)**: the canonical rules template lives inside this skill at `<skill_dir>/rules/v1_rules.md`, where `<skill_dir>` is the directory containing this skill's `SKILL.md`. This is the single authoritative path — no fallbacks, no alternate locations. The orchestrator derives `<skill_dir>` from the absolute path of the currently-executing `SKILL.md` and reads `rules/v1_rules.md` as a sibling file.
>
> This resolution works identically across the three install modes:
> - **Dogfood / dev** — `<repo>/skills/genesis-protocol/SKILL.md` → `<repo>/skills/genesis-protocol/rules/v1_rules.md`
> - **Plugin-dir install** (`claude --plugin-dir <path>`) — `<plugin-dir>/skills/genesis-protocol/SKILL.md` → `<plugin-dir>/skills/genesis-protocol/rules/v1_rules.md`
> - **Personal-scope install** (`cp -r skills/ ~/.claude/skills/`) — `~/.claude/skills/genesis-protocol/SKILL.md` → `~/.claude/skills/genesis-protocol/rules/v1_rules.md`
>
> **If the file is missing**: halt with a single-path error message:
> ```
> Rules template not found at: <resolved_path>
> This indicates a corrupted or incomplete skill install. Reinstall the
> genesis-protocol skill (re-copy the full skills/genesis-protocol/
> directory from the Genesis plugin source) and re-run Phase 1.
> ```
> Do not attempt alternate locations. Do not silently skip the rules copy. A halt with clear remediation is better than a silent gap in the downstream project's rule enforcement.

### New directory — `skills/genesis-protocol/research-templates/`

Structure:

```
skills/genesis-protocol/research-templates/
├── README.md                                              ← purpose + refresh policy
├── sota/
│   ├── claude-code-plugin-distribution.md
│   ├── claude-ecosystem-cross-os.md
│   └── spdx-headers.md
└── stack/
    ├── claude-code-plugin-structure.md                    ← refreshed from archive 2026-04-18
    └── claude-code-session-jsonl-format.md                ← refreshed from archive 2026-04-18
```

**README.md** (new file) — documents the purpose:
- What: R8 cache templates bundled with the genesis-protocol skill for downstream project seeding
- Why: decouple downstream Phase 2 seed from plugin-envelope filesystem topology (marketplace install blocker fix)
- Refresh policy: entries maintained in lockstep with plugin releases. When TTL expires relative to ship date, refresh before next plugin release. Downstream projects can independently refresh copies post-seed.

**Note on filename conventions** — skill-local templates drop the `_YYYY-MM-DD` date suffix from filenames since they live alongside the skill version (the plugin version pin is the freshness anchor). Date traceability lives in the frontmatter `created_at` and `expires_at` fields.

### Phase 2 Step 2.3 — rewrite

**Current** (from `phase-1-rules-memory.md` § Phase 2 Step 2.3):

> The Genesis plugin ships its own R8 cache at `<plugin-root>/.claude/docs/superpowers/research/` — where `<plugin-root>` is derived via the same "three levels up from `skills/genesis-protocol/SKILL.md`" rule used at Phase 1 Step 1.3. This cache contains entries that are also relevant to any downstream project, specifically the ones about Claude Code itself (plugin structure, session JSONL format, in-IDE tools, cross-OS ecosystem). Phase 2 **copies** these entries — not by-reference, because they are project-level references the downstream project needs to read offline.

**v1.4.2 rewrite**:

> The Genesis plugin ships R8 cache **templates** inside this skill at `<skill_dir>/research-templates/` — the same five canonical entries previously listed in the "Entries to copy" table below (3 sota + 2 stack) relevant to any downstream Claude-Code-based project. Phase 2 copies these templates into the downstream project's `.claude/docs/superpowers/research/` (the conventional R8 cache location). Post-copy, the downstream project owns its cache independently; refreshing entries is a downstream-project concern.
>
> **Source resolution (v1.4.2)**: identical discipline to Phase 1 Step 1.3. `<skill_dir>/research-templates/` is the single authoritative source. No fallback to `<plugin-root>/.claude/docs/superpowers/research/`. If the templates directory is missing, halt with a single-path error message:
> ```
> R8 cache templates not found at: <resolved_path>
> This indicates a corrupted or incomplete skill install. Reinstall the
> genesis-protocol skill and re-run Phase 2.
> ```

**Follow-on paragraph (existing, preserved verbatim modulo path patch)**: the current line-248 paragraph ("These entries apply to any Claude Code project, plugin or not...") is preserved verbatim — no wording change. v1.4.2 only patches the resolution discipline, not the rationale for copying.

**"Entries to copy" table (existing lines 250-258, preserved with path column patched)**: the 5-row table structure is kept intact; only the Source column changes from `<plugin-root>/.claude/docs/superpowers/research/<topic>_*.md` to `<skill_dir>/research-templates/<topic>.md` (no date suffix, per in-skill template convention § In scope bullet 5). Destination column unchanged. "Why copy not link" column unchanged. Row membership unchanged — the canonical 5 entries remain : plugin-distribution, plugin-structure, session-jsonl-format, cross-os, spdx-headers.

**Refresh on seed**: the downstream project creates dated filenames when copying from the skill-local templates. Filename at seed time follows the downstream R8 convention (`<topic>_<ISO-date>.md` in `sota/` or `stack/`). The copy operation is a **copy-and-rename** — skill-local template `plugin-distribution.md` lands as downstream `sota/plugin-distribution_<seed-date>.md`. Frontmatter `created_at` is updated to the seed date; `expires_at` follows the normal R8 TTL (sota 7d, stack 1d) from the seed date. The template file's original timestamps are preserved in the source frontmatter for audit.

### `install-manifest.yaml` updates

Two categories of change:

**(a) Version field bump**:
```yaml
# Before
version: 0.8.0

# After
version: 1.4.2
```

**(b) New verification checks appended to the existing `verification:` list**:

```yaml
  # v1.4.2 — verify the skill-local rules template is present
  - check: file_exists
    path: skills/genesis-protocol/rules/v1_rules.md
    on_fail: |
      skills/genesis-protocol/rules/v1_rules.md is missing. Phase 1 Step 1.3
      cannot seed the downstream project's rules without this skill-local
      template. Reinstall the genesis-protocol skill from a known-good source
      (Genesis plugin release bundle) and re-run install verification.

  # v1.4.2 — verify the skill-local R8 cache templates directory
  - check: directory_exists
    path: skills/genesis-protocol/research-templates/
    on_fail: |
      skills/genesis-protocol/research-templates/ is missing. Phase 2 Step 2.3
      cannot seed the downstream project's R8 cache without this skill-local
      template directory. Reinstall the genesis-protocol skill.

  - check: file_exists
    path: skills/genesis-protocol/research-templates/README.md
    on_fail: |
      research-templates/README.md is missing. The templates directory exists
      but its purpose/refresh-policy documentation is absent. Reinstall the skill.

  - check: directory_exists
    path: skills/genesis-protocol/research-templates/sota/
    on_fail: |
      research-templates/sota/ is missing. The 3 sota entries cannot be
      seeded into the downstream project. Reinstall the skill.

  - check: directory_exists
    path: skills/genesis-protocol/research-templates/stack/
    on_fail: |
      research-templates/stack/ is missing. The 2 stack entries cannot be
      seeded into the downstream project. Reinstall the skill.

  - check: file_exists
    path: skills/genesis-protocol/research-templates/sota/claude-code-plugin-distribution.md
    on_fail: |
      Expected template sota/claude-code-plugin-distribution.md is missing.

  - check: file_exists
    path: skills/genesis-protocol/research-templates/sota/claude-ecosystem-cross-os.md
    on_fail: |
      Expected template sota/claude-ecosystem-cross-os.md is missing.

  - check: file_exists
    path: skills/genesis-protocol/research-templates/sota/spdx-headers.md
    on_fail: |
      Expected template sota/spdx-headers.md is missing.

  - check: file_exists
    path: skills/genesis-protocol/research-templates/stack/claude-code-plugin-structure.md
    on_fail: |
      Expected template stack/claude-code-plugin-structure.md is missing.

  - check: file_exists
    path: skills/genesis-protocol/research-templates/stack/claude-code-session-jsonl-format.md
    on_fail: |
      Expected template stack/claude-code-session-jsonl-format.md is missing.
```

### `CLAUDE.md` project-root R8 active-entries list update

The project-root `CLAUDE.md` currently lists R8 active entries. The 2 stack entries re-enter currency with v1.4.2 refresh — the bullet list is updated to reflect this. No structural change, just list membership refresh.

## Verification scenarios

Three new scenarios appended to `skills/genesis-protocol/verification.md`:

| # | Scenario | Expected |
|---|---|---|
| S1 | Personal-scope install verification — after `cp -r skills/genesis-protocol ~/.claude/skills/`, run `/genesis-protocol` on a fresh empty cwd. | Phase 1 Step 1.3 resolves `<skill_dir>/rules/v1_rules.md` as `~/.claude/skills/genesis-protocol/rules/v1_rules.md`. File is present (shipped with the skill). Rules are copied to `<cwd>/.claude/docs/superpowers/rules/v1_rules.md` successfully. Zero three-levels-up probe. Zero halt. |
| S2 | Phase 2 R8 cache seed from skill-local templates — after a Phase 1 success, run Phase 2. | Step 2.3 resolves `<skill_dir>/research-templates/sota/` and `<skill_dir>/research-templates/stack/`. All 5 entries (3 sota + 2 stack) are copied to `<cwd>/.claude/docs/superpowers/research/`. Filenames at destination include `_<seed-date>` suffix per R8 downstream convention. `INDEX.md` is populated with all 5 entries. Zero three-levels-up probe. |
| S3 | Install-manifest verification catches missing rules/ — manually delete `skills/genesis-protocol/rules/v1_rules.md` from a dogfood install, run install verification. | Verification fails loudly with the specific error message for the missing file, naming the exact expected path. Does not fall through to a legacy fallback. Does not silently succeed. Reinstall remediation is clearly surfaced. |

**Regression probes** — v1.4.1 scenarios #40-#44 (Layer B citation rendering) unchanged since zero Layer B touch in v1.4.2. v1.4.0 fallback scenarios #29, #32, #33, #38 unchanged. v1.3.x scenarios unchanged. v1.4.2 does not modify any runtime surface touched by earlier scenarios — only the install-path resolution for rules and R8 templates, which are Phase 1 + 2 pre-Phase-0-UI concerns.

**Runtime replay note**: S1 is replayable standalone via a test install path. S2 is replayable as an S1→S2 chain (its Phase 1 prerequisite IS S1; once S1 passes, S2 follows directly). S3 is replayable standalone via `rm skills/genesis-protocol/rules/v1_rules.md` + re-run install-manifest verification. Per the v1.3.1 → v1.4.1 convention, runtime replay deferred if in-session replay is not practical — −0.2 Pain-driven deduction per replay-deferred scenario rolls forward.

## R9 language policy applied

No new R9 rows for v1.4.2. The halt-with-remediation error messages added in Phase 1 Step 1.3 and Phase 2 Step 2.3 are **dev-tooling tier 1** (English-only) per R9 — these messages surface only when a skill install is corrupt, addressing a developer/maintainer re-installing. They are not user-facing runtime strings.

The 2 new R8 templates refreshed (`claude-code-plugin-structure`, `claude-code-session-jsonl-format`) follow the existing R8 content convention — English-only technical research. No locale dispatch.

## 1:1 mirror map with SKILL.md

| This spec section | `skills/genesis-protocol/*` changes | Mirror status |
|---|---|---|
| Phase 1 Step 1.3 rewrite | `phase-1-rules-memory.md § "Step 1.3 — Copy the rules"` — legacy fallback paragraph deleted, single-path resolution + halt message rewritten | Mirrored |
| Phase 1 Step 1.3 "Why skill-local" paragraph | `phase-1-rules-memory.md § "Step 1.3"` final paragraph (v1.2.0 F29 forensics) | **Preserved verbatim** (no change) |
| Phase 1 Step 1.3 "Adaptation" paragraph (R1.1 ritual + scope lock) | `phase-1-rules-memory.md § "Step 1.3"` — adaptation note if present | **Preserved verbatim** (no change) |
| Phase 1 Step 1.3 "Do not rewrite the rules" discipline | `phase-1-rules-memory.md § "Step 1.3"` — immutability note if present | **Preserved verbatim** (no change) |
| Phase 2 Step 2.3 rewrite — resolution paragraphs | `phase-1-rules-memory.md § "Phase 2 — Step 2.3"` opening 2 paragraphs — resolver points to `<skill_dir>/research-templates/`, halt message rewritten | Mirrored |
| Phase 2 Step 2.3 rewrite — follow-on rationale paragraph | `phase-1-rules-memory.md § "Phase 2 — Step 2.3"` line 248 ("These entries apply to any Claude Code project...") | **Preserved verbatim** |
| Phase 2 Step 2.3 rewrite — "Entries to copy" 5-row table | `phase-1-rules-memory.md § "Phase 2 — Step 2.3"` lines 250-258 table | **Preserved structure + row membership**; Source column paths patched (`<plugin-root>/...*_*.md` → `<skill_dir>/research-templates/<topic>.md`) |
| Phase 2 Step 2.3 "Each copied entry has its `expires_at`..." paragraph | `phase-1-rules-memory.md` line 260 expiration discipline | **Preserved verbatim** (skill-local refresh discipline inherits R8 TTL) |
| research-templates/ directory | New directory `skills/genesis-protocol/research-templates/` with 3 sota + 2 stack entries + README.md | Mirrored (5 files + 1 README) |
| install-manifest.yaml updates | Version bump + 10 new `check:` entries | Mirrored |
| Verification scenarios S1-S3 | `skills/genesis-protocol/verification.md` new block | Mirrored |
| Problem statement | — | **Spec-only** (design rationale) |
| Rationale for v1.4.2 route | — | **Spec-only** (design decision log) |
| Scope block | — | **Spec-only** (design document structure) |
| Regression note | — | **Spec-only** (cross-version traceability) |

## Rationale for v1.4.2 route

- **PATCH is the honest tranche** — v1.4.2 is an install-path resolution fix + distribution bundle completion. No new privilege, no new dependency, no new subprocess, no new network call, no new schema bump, no new bilingual pair, no cross-skill-pattern change. Pure plumbing. PATCH is the semver honest label. Running average ≈ 8.89 has 0.39 tampon above 8.5; a PATCH with ≥ 9.0 self-rating fits the streak envelope comfortably.
- **Pain-driven purity — dogfood-observed, not speculative** — Friction #4 was reproduced live on 2026-04-18 at `~/.claude/skills/genesis-protocol/` install. Friction #5 was confirmed by Phase 2 partial completion (3/5 entries seeded). Both are BLOCKERS for any non-dogfood install path. Pain-driven projection: 9.3-9.4. This is the **strongest pain-driven ship on the BLOCKER-severity axis since v1.2.3** (F34 gh pre-flight). v1.2.3 retains a distinct distinction — it was **live-reproduced on its own ship** (F34 fired during the v1.2.3 ship itself). v1.4.2's pain was observed in a prior-session dogfood (2026-04-18 stress test against v1.4.1), not on v1.4.2's own ship. The axes do not compete: v1.2.3 = self-reproducing-on-ship ; v1.4.2 = dogfood-observed BLOCKER severity.
- **Anti-Frankenstein retroactive — drop the legacy fallback** — v1.2.1 retained the "three levels up" fallback as belt-and-suspenders during the F29 fix. Three versions later (v1.4.2), no v1.2.1+ install path needs it — the fallback is dead code that actively misleads orchestrators when the skill-local path is corrupted. Removing it simplifies the resolver and tightens the failure mode: either the skill-local file is present (happy path) or the install is corrupt (halt with clear remediation). No silent middle state.
- **Bundle completion — make the skill self-sufficient for Phase 1 + Phase 2** — Genesis's architectural North Star is self-contained skills. The v1.2.1 F29 fix achieved this for rules; v1.4.2 completes it for R8 cache templates. A downstream project now gets everything it needs from the skill package alone — no cross-repo reads, no plugin-envelope filesystem assumptions. This is the final install-path decoupling step.
- **Halt-with-remediation over silent fallback** — the v1.5.0 spec (already written, commit `59a7640` on `feat/v1.5.0-living-memory`) pivoted Genesis from silent-graceful to halt-with-remediation for API pre-flight. v1.4.2 applies the same discipline to the install-path resolution one version earlier. The principle travels: any unrecoverable state → explicit halt with specific remediation, never silent fallback.
- **In-skill templates drop the date suffix** — skill-local R8 templates (`sota/claude-code-plugin-distribution.md`) drop the `_YYYY-MM-DD` suffix common in project R8 caches. Rationale: date traceability lives in frontmatter (`created_at` / `expires_at`); the skill version pin is the freshness anchor for templates. Date suffix would create two date authorities per file (filename + frontmatter) with drift risk. **Creation during feat commit**: the 3 currently-active entries (`claude-code-plugin-distribution_2026-04-14.md`, `claude-ecosystem-cross-os_2026-04-15.md`, `spdx-headers_2026-04-14.md`) are **copied-and-renamed** from the dogfood source R8 cache into `research-templates/` with date suffixes stripped; the 2 stack entries are freshly written via refresh research (no pre-existing source in the dogfood cache post-archival). Downstream projects add the date suffix at seed time, following the normal R8 convention for their own cache (per Phase 2 Step 2.3 copy-and-rename discipline).
- **R8 refresh of 2 archived stack entries** — `claude-code-plugin-structure` and `claude-code-session-jsonl-format` are archived in the dogfood source (TTL expired 2026-04-17). Shipping them in v1.4.2 requires a refresh to make them active again. This refresh is incidental to v1.4.2's core scope but necessary for the bundle to be useful at ship time. Realistic feat cost ≈ 45-60 min (content research + frontmatter updates + TTL re-verification), not 30 min as originally estimated. **Escape clause**: if WebSearch during feat reveals a breaking change in either topic since the 2026-04-14/17 source captures (new `plugin.json` field, new JSONL redaction pattern, schema drift), **pause v1.4.2 ship and route the breaking-change delta through v1.5.x** — do NOT bundle a materially-different refresh into a PATCH envelope. The refresh is allowed to be a direct content-currency update; it is NOT allowed to be a structural revision.
- **install-manifest.yaml version bump catches stale lock-step** — the manifest has been stuck at `0.8.0` since that release while plugin.json progressed to `1.4.1`. v1.4.2 brings it back in lock step. Incidental cleanup; zero runtime impact (install-manifest version is not consumed anywhere functional).
- **Six-commit rhythm seventh consecutive application** — (spec + spec polish + plan + plan polish + feat + chore). Pattern unchanged. The chore commit that archived the dogfood report (commit `35c8b72` already on branch) does NOT count against the six-commit rhythm — it's separate forensic archival preceding the ship work proper.
- **Living-spec — standalone, not extension** — v1.4.2 is a topic-scoped spec (marketplace install resolution), not an extension of `v2_etape_0_drop_zone.md` (which is drop-zone Layer A scoped). A standalone spec file keeps the living-spec pattern undiluted: `v2_etape_0_drop_zone.md` grows on v1.3.x + v1.4.0 + v1.4.1 + v1.5.0 (Layer A arc); `v1_4_2_marketplace_unblock.md` is its own artefact for the genesis-protocol install-path concern.
- **Zero Layer A ripple** — `genesis-drop-zone/*` byte-identical across v1.4.1 → v1.4.2. Verifiable empirically post-feat via `git diff main --stat -- skills/genesis-drop-zone/` returning empty.
- **Self-rating projection** — Pain-driven 9.3-9.4 (dogfood BLOCKER, user-observed live), Prose cleanliness 9.1-9.2 (tight scope, surgical edits, 6-commit rhythm), Best-at-date 9.0-9.2 (pattern established v1.2.1 F29 applied consistently; R8 refresh of 2 archived entries current-at-date), Self-contained 9.3-9.4 (narrow surface, 2 runbook edits + 1 new dir + manifest update), Anti-Frankenstein 9.3-9.4 (legacy fallback dropped, no speculative addition). Average ≈ **9.2-9.3**. **11th consecutive ship ≥ 9.0**.

## References

- Dogfood report : `memory/project/dogfood_v1.4.1_stress_2026-04-18/stress_test_report.md` (pain source)
- v1.2.1 F29 fix (historical precedent — rules moved in-skill) : `memory/project/session_v1_2_1_paradox_guards.md`
- v1.5.0 spec on parallel branch : `feat/v1.5.0-living-memory` commit `59a7640` § "Rationale for v1.5.0 route" bullet on halt-with-remediation discipline travel
- R8 refresh targets (content research) : WebSearch + WebFetch for `claude-code-plugin-structure 2026` + `claude-code-session-jsonl-format 2026` during feat commit

## Relation to v1.5.0

v1.4.2 is a **prerequisite** for v1.5.0's value delivery. v1.5.0 introduces living drop zone memory with arbitration + archive — features that only benefit users who can install Genesis in the first place. Without v1.4.2's install-path unblock, v1.5.0's work would ship to a Genesis that cannot reach its users outside dogfood mode.

Post-v1.4.2 ship, v1.5.0 spec review loop resumes on `feat/v1.5.0-living-memory` branch. The spec is already written; only reviewer passes + plan + feat remain. Running average post-v1.4.2 ≈ 8.90-8.91; post-v1.5.0 (projected 9.10-9.15) ≈ 8.92-8.95. Streak ≥ 9.0 extended to 12 consecutive ships.
