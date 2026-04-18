<!-- SPDX-License-Identifier: MIT -->
---
name: Genesis Protocol v1.4.1 stress-test report
description: Friction log from the colocs-tracker stress-test bootstrap on 2026-04-18. Input matches the canonical "evolving spec via brief.md + annexe.md" shape that production Genesis users will hit. Surfaced as v1.5 enhancement candidates.
type: project
phase: 7
date: 2026-04-18
target_genesis_version: v1.4.1
test_input: brief.md + annexe.md (no canonical config.txt)
---

# Genesis Protocol v1.4.1 — stress test report

## Setup

- **Target folder** : `C:\tmp\genesis-dogfood-v1.4.1-stress-2026-04-18\`
- **Input** : `brief.md` (5 sections, 393 B) + `annexe.md` (3 sections, 349 B, post-réunion override of brief)
- **Genesis version under test** : v1.4.1 (skill installed at `~/.claude/skills/genesis-protocol/`)
- **Genesis dogfood source** : `C:\Dev\Claude_cowork\project-genesis\`
- **Stress-test scope** : phases -1, 5.5, 6 skipped (privileged side effects); phases 0, 1, 2, 3 (local), 4, 7 (partial) executed

## Phase outcomes

| Phase | Outcome | Notes |
|---|---|---|
| -1 | ⏭️ Skipped (consent) | Machine equipped (Genesis runs from it) |
| 0 | ✅ Done | brief.md + annexe.md parsed and reconciled manually |
| 1 | ✅ Done | Memory subtree, R1-R10 rules copied, 4 INDEXes seeded |
| 2 | ⚠️ Partial | 3/5 stack-relevant R8 entries copyable from dogfood; 2 absent in source |
| 3 | ⚠️ Local-only | `git init` only; no SSH, no remote |
| 4 | ✅ Done | master.md, README.md, design spec draft, .gitignore |
| 5.5 | ❌ Skipped (consent) | Out of stress-test scope |
| 6 | ❌ Skipped (consent) | Out of stress-test scope |
| 7 | ⚠️ Partial | Resume prompt + this report; session-post-processor not run |

## Frictions captured (in detection order)

### Friction #1 — Phase 0 input shape: BRIEF + ANNEXE not in canonical table

**Where** : `phase-0-seed-loading.md` Step 0.1 input shape table.

**What happened** : The actual input was `brief.md` + `annexe.md` (a 2-file evolving spec : initial brief + revision post-meeting). Phase 0 Step 0.1 table classes "no `config.txt` but `BRIEF.md` exists" as "Unusual — ask user", but doesn't anticipate **chronological multi-file seeds**.

**Why it matters** : This is the canonical shape real-world projects arrive in. Initial brief → meeting → revision annex → maybe a second annex. Treating each annex as "ask user what to do" forces the orchestrator-driver (Claude) to manually reconcile. The reconciliation logic isn't in the skill — it's improvised per session.

**Suggested v1.5 enhancement** : Add a new canonical input shape "BRIEF.md + chronological annexes (annexe*.md, revision*.md)" with explicit semantics : later files override earlier files (chronological override), with union semantics for set-typed fields (target users, in-scope features) and last-wins for scalars (budget, deadline).

### Friction #2 — Phase 0 implicitly assumes 1-file canonical seed

**Where** : `phase-0-seed-loading.md` Step 0.2 ("Parse `config.txt` into a structured intent").

**What happened** : The runbook is written assuming a single `config.txt`. There's no slot for multi-file seeds even in the "Mixed media" branch (Step 0.3) — mixed media is treated as **supplementary**, not as **chronological override** of the primary seed.

**Suggested v1.5 enhancement** : Generalize Step 0.2 to "primary seed + ordered overrides", where the orchestrator detects ordering (timestamps in filenames, meeting-date references in content, or explicit `revision: 2` frontmatter).

### Friction #3 — No conflict-reconciliation policy

**Where** : `phase-0-seed-loading.md` is silent on what to do when fields conflict (e.g. budget 500€ in brief, 800€ in annexe).

**What happened** : Default applied here ad-hoc : chronological override for scalars, union for sets. Worked for this case, but **not codified anywhere** in the skill. Next driver might apply different defaults → drift.

**Suggested v1.5 enhancement** : Add a "Reconciliation policy" section to `phase-0-seed-loading.md` Step 0.4 with explicit rules : (a) chronological override for scalars (budget, deadline, license), (b) union for sets (targets, in-scope), (c) last-wins for booleans (is-a-plugin), (d) ask user explicitly when the policy is ambiguous (e.g. stack changes in annex).

### Friction #4 — Plugin root resolution breaks for user-installed skills

**Where** : `phase-1-rules-memory.md` Step 1.3 ("Source resolution: the plugin root is always three levels above this skill's `SKILL.md`").

**What happened** : When Genesis is installed at `~/.claude/skills/genesis-protocol/` (user-level skill, no plugin envelope), the "three levels up" rule resolves to `~/.claude/`, where the rules file would have to live at `~/.claude/.claude/docs/superpowers/rules/v1_rules.md` (double `.claude`) — not a real path.

**Workaround applied** : Manual fallback to dogfood location `C:\Dev\Claude_cowork\project-genesis\skills\genesis-protocol\rules\v1_rules.md`. This works on this machine but fails the moment Genesis is installed via a Claude Code marketplace OR on a different machine.

**Suggested v1.5 enhancement** : Phase 1 Step 1.3 needs a layered resolver :
1. Check `<3-levels-up>/.claude/docs/superpowers/rules/v1_rules.md` (plugin envelope, marketplace install)
2. Check `<skill-dir>/rules/v1_rules.md` (skill-local fallback — requires shipping rules inside the skill folder)
3. Check `~/.claude/docs/superpowers/rules/v1_rules.md` (user-global fallback)
4. Halt with all paths surfaced in the error.

The cleanest fix : ship `rules/v1_rules.md` **inside** the `genesis-protocol/` skill folder so the resolver only needs Step 2. That removes the dependency on plugin-envelope assumption entirely.

### Friction #5 — Missing R8 stack-relevant entries in dogfood source

**Where** : `phase-1-rules-memory.md` Step 2.3 lists 5 canonical entries to copy. Genesis dogfood source has only 3 of 5 :
- ✅ `sota/claude-code-plugin-distribution_2026-04-14.md`
- ✅ `sota/claude-ecosystem-cross-os_2026-04-15.md`
- ✅ `sota/spdx-headers_2026-04-14.md`
- ❌ `stack/claude-code-plugin-structure_*.md` (not present)
- ❌ `stack/claude-code-session-jsonl-format_*.md` (not present)

**Why it matters** : The 2 missing `stack/` entries are explicitly required for `session-post-processor` to operate against this project's JSONL transcripts. Without them, that skill cannot run end-to-end on this downstream project.

**Suggested v1.5 enhancement** : Either (a) ship the canonical R8 entries inside the `genesis-protocol/` skill folder so they always travel with the skill, or (b) gate Phase 2 with a precondition check that surfaces the gap as a hard error (current behavior is silent partial copy).

### Friction #6 — Stale R8 entries past TTL silently copied

**Where** : `phase-1-rules-memory.md` Step 2.3 says "If the entry has already expired by the time Phase 2 runs, **archive** the source before copying, never copy a stale entry."

**What happened** : All 3 copied sota entries (TTL 7d) have `_2026-04-14` and `_2026-04-15` timestamps in their filename. Today is 2026-04-18 → all 3 are at day 3-4 of their 7-day TTL, still valid. **No friction in this case** but the protocol gives no machine-readable hint of TTL inside the file frontmatter — it's encoded in the filename only. Future driver might miscount.

**Suggested v1.5 enhancement** : Require frontmatter `expires_at: YYYY-MM-DD` in every R8 entry (already mentioned in Layer 0 R8 cache convention) and have Phase 2 read it explicitly rather than parse the filename.

## What worked well

- **Phase 1 install-manifest pattern** : reading 4 sibling install-manifests in parallel + writing their templated INDEX.md files was clean. The idempotency contracts (`create_if_missing_only: true`) make re-runs safe.
- **MEMORY.md as short index** : the pointer-file pattern from Layer 0 ports cleanly to project level. Index stays under 50 lines, full content lazy-loaded.
- **R2.1 worktree mention in CLAUDE.md** : the project CLAUDE.md inheriting Layer 0 keeps the project-level file tiny while preserving rule enforcement.
- **The consent gates** : even in stress-test, the top-level consent card (Step 0 in `SKILL.md`) forced explicit scope confirmation. Caught the "real bootstrap vs stress test" branching upfront — would have created a wasted GitHub repo otherwise.

## v1.5 prioritization

If only one friction can be fixed for v1.5 : **#4 (plugin root resolution)** — it's the only one that fully blocks installation paths other than dogfood. The others all degrade UX but are workable.

Order of impact :

1. **#4** — install-anywhere reliability (BLOCKER for marketplace install)
2. **#5** — R8 entries shipped with skill (BLOCKER for session-post-processor downstream)
3. **#1 + #2 + #3** (group) — multi-file seed handling (UX upgrade for real-world inputs)
4. **#6** — TTL parsing discipline (forensic polish, no immediate failure)
