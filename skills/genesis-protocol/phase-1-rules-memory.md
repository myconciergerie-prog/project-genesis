<!-- SPDX-License-Identifier: MIT -->
---
name: Phase 1 + Phase 2 — Rules, memory architecture, research cache
description: Runbook for Phase 1 (rules R1-R10 copy + memory subtree scaffold + four sibling-skill install-manifests) and Phase 2 (research cache INDEX with Layer 0 seed entries). These two phases run back-to-back because they both write infrastructure to the downstream project's root — rules and memory in Phase 1, research cache in Phase 2 — before git init in Phase 3 turns the folder into a tracked repo.
---

# Phase 1 + Phase 2 — Rules, memory architecture, research cache

Phase 1 sets up the rules and memory scaffold that every Genesis-bootstrapped project inherits. Phase 2 initializes the R8 research cache with seed entries derived from Layer 0's universal R8 sota cache. Both phases run in the downstream project folder, writing directly to its root — this happens **before** `git init` in Phase 3, so every file landed here becomes part of the first bootstrap commit.

The two phases are folded into one runbook because:

1. They write to adjacent subtrees (`memory/` and `.claude/docs/superpowers/research/`) of the same target folder.
2. They run back-to-back with no user interaction between them.
3. The install-manifest invocations at the end of Phase 1 can also touch `.claude/docs/superpowers/` (e.g. `session-post-processor` needs `memory/project/sessions/`) so sequencing them together avoids double-passes.

## Prerequisites

- Phase 0 is complete — `memory/project/bootstrap_intent.md` exists in the target folder with name, slug, vision, license, plugin flag, plan tier, stack hints, scope locks.
- The target folder does **not yet** contain `.git/`. Phase 1 and Phase 2 write non-git-tracked files into a plain folder; git init happens in Phase 3.
- The five sibling skills are present under `skills/` at the Genesis plugin root (verified by `install-manifest.yaml` post-install check of the `genesis-protocol` skill itself).

## Phase 1 — The flow

### Step 1.1 — Read the intent

Read `memory/project/bootstrap_intent.md` from the target folder. Extract: slug, license, is-a-plugin flag, plan tier, scope locks. These fields drive the branching in the next steps.

### Step 1.2 — Create the memory subtree

Create the canonical memory subtree under `memory/`. The exact layout is the one shipped by Genesis itself:

```
memory/
├── MEMORY.md              (index, always loaded at session open per R1.1)
├── master.md              (stable vision — written at Phase 4, scaffolded with a placeholder here)
├── user/
│   └── README.md          (project-scoped user notes)
├── feedback/
│   └── README.md          (project-scoped collaboration rules)
├── project/
│   ├── bootstrap_intent.md  (already present from Phase 0)
│   └── sessions/
│       └── INDEX.md       (session archive index — seeded by session-post-processor install-manifest at Step 1.5)
├── reference/
│   └── README.md          (external systems + accounts — populated at Phase 3 / 5.5)
├── themes/
│   └── README.md          (per-topic memory, empty initially)
├── journal/
│   └── INDEX.md           (seeded by journal-system install-manifest at Step 1.5)
└── pepites/
    └── INDEX.md           (seeded by pepite-flagging install-manifest at Step 1.5)
```

Step 1.2 creates **only** the directory scaffold plus `MEMORY.md` (scaffold index), `master.md` (placeholder), and the four `README.md` files under `user/`, `feedback/`, `themes/`, `reference/`. The three sibling-owned `INDEX.md` files (`journal/INDEX.md`, `pepites/INDEX.md`, `project/sessions/INDEX.md`) are **not** created by Step 1.2 — they are delegated to the sibling install-manifests invoked at Step 1.5. This split is deliberate: each sibling owns its own index content and the orchestrator never duplicates it. `memory/project/bootstrap_intent.md` was already written at Phase 0.

Use `Write` to create the scaffold files listed above. Idempotent — if any scaffold file already exists, leave it in place.

`MEMORY.md` at this stage contains only the scaffold index (pointers to master, user, feedback, project, reference, themes, journal, pepites) with placeholder entries. Step 1.6 re-opens `MEMORY.md` after the sibling install-manifests have run to list the now-present INDEX files. Phase 4 will fill in the project-specific entries.

### Step 1.3 — Copy the rules

Copy the canonical R1-R10 rules template shipped inside this skill at `<skill_dir>/rules/v1_rules.md` to the target folder's `.claude/docs/superpowers/rules/v1_rules.md`. The *source* is skill-local (lives inside the Genesis plugin's `skills/genesis-protocol/` directory); the *destination* remains the conventional `<target>/.claude/docs/superpowers/rules/v1_rules.md` path — every Genesis-bootstrapped project keeps its rules under the standard Claude Code docs location.

**Source resolution**: the canonical rules template lives inside this skill at `<skill_dir>/rules/v1_rules.md`, where `<skill_dir>` is the directory containing this skill's `SKILL.md`. The orchestrator derives `<skill_dir>` from the absolute path of the currently-executing `SKILL.md` and reads `rules/v1_rules.md` as a sibling file. This works in all three install modes:

- **Dogfood / dev** — `<repo>/skills/genesis-protocol/SKILL.md` → `<repo>/skills/genesis-protocol/rules/v1_rules.md`
- **Plugin-dir install** (`claude --plugin-dir <path>`) — `<plugin-dir>/skills/genesis-protocol/SKILL.md` → `<plugin-dir>/skills/genesis-protocol/rules/v1_rules.md`
- **Personal-scope install** (`cp -r skills/ ~/.claude/skills/` per F18 workaround) — `~/.claude/skills/genesis-protocol/SKILL.md` → `~/.claude/skills/genesis-protocol/rules/v1_rules.md`

**Fallback (legacy)**: if `<skill_dir>/rules/v1_rules.md` is not present — which can only happen if the skill was installed from a source earlier than v1.2.1 — look for the file at `<plugin-root>/.claude/docs/superpowers/rules/v1_rules.md` (three levels above this skill's `SKILL.md`). If neither path resolves, halt and surface BOTH expected paths in the error message. Do not silently skip the rules copy.

**Why skill-local**: v1.2.0 self-dogfood reproduced F29 — the three-levels-up heuristic resolved to `~/.claude/` (which has no `.claude/docs/superpowers/rules/`) when Genesis was installed to personal scope. Making the skill self-contained (shipping `rules/v1_rules.md` inside the skill package) eliminates the install-mode coupling.

**Adaptation**: the rules are mostly generic, but two sections are per-project:

- **R1.1 open ritual** — references `memory/MEMORY.md` and the most recent resume prompt. Leave the references as-is; they will work once Phase 4 and Phase 7 write the files.
- **Scope lock references** — if `bootstrap_intent.md` lists scope locks (other projects frozen during this bootstrap), Phase 1 appends a short "Scope locks" section to `memory/MEMORY.md` pointing to each lock. Genesis itself uses this pattern for the Aurum freeze.

Do not rewrite the rules themselves during Phase 1 — they are copied verbatim. Any amendment is a Genesis-level change, not a per-project customization.

### Step 1.4 — Write the project `CLAUDE.md`

Create `CLAUDE.md` at the target folder root with the standard Layer 0 inheritance pattern:

```markdown
# <Project name> — CLAUDE.md

This is the project-level CLAUDE.md for <project>. Auto-loaded by Claude Code
in every session opened in this directory.

## Inherits from Layer 0

All universal rules, user profile, hard rules, workflow patterns, and machine-
specific reference are inherited by reference from `~/.claude/CLAUDE.md`
(Layer 0 universal). This file does NOT duplicate them.

## Project-specific pointers

### Rules

Project-specific rules R1–R10 adapted for <project> live at:

    .claude/docs/superpowers/rules/v1_rules.md

### Memory architecture

    memory/
    ├── MEMORY.md           ← index, always loaded at session open per R1.1
    ├── master.md           ← stable vision + stack + rules summary
    ├── user/               ← project-scoped user notes
    ├── feedback/           ← project-scoped collaboration rules
    ├── project/            ← ongoing state, decisions, incidents, session history
    ├── reference/          ← external systems & accounts for this project
    ├── themes/             ← per-topic memory, populated as the project grows
    ├── journal/            ← stratified thought capture (6th memory type)
    └── pepites/            ← gold nugget discoveries (7th memory type)

### Research cache

R8 research cache with TTL at:

    .claude/docs/superpowers/research/
    ├── INDEX.md            ← auto-maintained index with expires_at dates
    ├── sota/               ← state of the art — TTL 7 days
    ├── stack/              ← package / MCP / version snapshots — TTL 1 day
    └── archive/            ← deprecated reports, kept forensic

## R1.1 Open ritual reminder

Every session opened in this directory must run R1.1 from
`rules/v1_rules.md` before any Edit / Write.
```

### Step 1.5 — Run the four sibling install-manifests

Phase 1 invokes the `install-manifest.yaml` steps of four sibling skills, in order:

1. **`phase-minus-one/install-manifest.yaml`** — this is a **stack-install spec** (per-OS package list), not a file-target manifest; it has no `targets:` section. Phase 1 Step 1.5 merely verifies the file is present and well-formed. The actual `memory/reference/automation-stack.md` is written at runtime when `phase-minus-one` runs during Phase -1 (before Phase 1 starts). If `automation-stack.md` is missing at this point, Phase -1 was skipped or incomplete — halt and surface the gap, do not attempt to fabricate a placeholder.
2. **`journal-system/install-manifest.yaml`** — creates `memory/journal/` directory and `memory/journal/INDEX.md` with the canonical stratified capture format. Idempotent via `create_if_missing_only: true`; if `INDEX.md` already exists it is left alone.
3. **`session-post-processor/install-manifest.yaml`** — creates `memory/project/sessions/` directory and `memory/project/sessions/INDEX.md` with the session archive scaffold and declares the Python 3.10+ runtime requirement. Idempotent via `create_if_missing_only: true`.
4. **`pepite-flagging/install-manifest.yaml`** — creates `memory/pepites/` directory and `memory/pepites/INDEX.md` with the red-light criteria and surfacing protocol embedded. Idempotent via `create_if_missing_only: true`.

**The orchestrator invokes these manifests — it never re-writes their content.** Each sibling skill owns its own install output. The orchestrator's job is to call them in the right order, one after the other, and halt immediately if any fails a verification check.

`phase-5-5-auth-preflight` has no install-manifest at Phase 1 — it only runs when invoked at Phase 5.5 with a project slug and a GitHub owner. It does not install anything into the downstream project folder until Phase 5.5 completes.

### Step 1.6 — Seed `memory/MEMORY.md`

After all four install-manifests have run, update `memory/MEMORY.md` so it lists the now-present files in its index. The index is the Layer 0 "short index always loaded, full content lazy-loaded" pattern — each entry is one line under 150 characters.

Template after Step 1.6:

```markdown
<!-- SPDX-License-Identifier: MIT -->

# MEMORY — <project name>

Auto-loaded at session open per R1.1. Inherits Layer 0 from ~/.claude/CLAUDE.md.

## Master

- [Master vision + stack + rules summary](master.md) — stable project vision

## User

- [user/ README](user/README.md) — project-scoped user notes

## Feedback

- [feedback/ README](feedback/README.md) — project-scoped collaboration rules

## Project

- [Bootstrap intent](project/bootstrap_intent.md) — parsed from Phase 0 of the Genesis bootstrap
- [Session archives INDEX](project/sessions/INDEX.md) — session-post-processor output

## Reference

- [reference/ README](reference/README.md) — external systems and accounts, populated at Phase 5.5

## Themes

- [themes/ README](themes/README.md) — per-topic memory, populated as the project grows

## Journal

- [Journal INDEX](journal/INDEX.md) — stratified thought capture (6th memory type)

## Pépites

- [Pépites INDEX](pepites/INDEX.md) — gold nugget discoveries (7th memory type)
```

## Phase 2 — The flow

### Step 2.1 — Create the research cache directory tree

Create `.claude/docs/superpowers/research/` with the canonical subtree:

```
.claude/docs/superpowers/research/
├── INDEX.md
├── sota/          (state of the art — TTL 7 days)
├── stack/         (package / MCP / version — TTL 1 day)
└── archive/       (deprecated entries, forensic)
```

Each subdirectory gets a `.gitkeep` if it would otherwise be empty. The `archive/` subdirectory always starts empty.

### Step 2.2 — Seed `INDEX.md` with the Layer 0 universal entries

The Layer 0 R8 cache at `~/.claude/docs/superpowers/research/sota/` contains universal-scope findings that apply to every project on this machine. Phase 2 does **not** copy those entries into the downstream project — they already live in Layer 0 and are inherited by reference. Instead, Phase 2 writes pointer lines into the downstream project's `INDEX.md` so future sessions can find them.

Seed `INDEX.md` content:

```markdown
<!-- SPDX-License-Identifier: MIT -->

# Research cache INDEX — <project name>

R8 research cache per Layer 0. Entries have TTL. Always scan this index
before launching fresh web research. If an entry has expired (check
`expires_at`), archive it first and refresh.

## TTL policy

- `sota/` — state of the art — TTL 7 days
- `stack/` — package / MCP / version snapshots — TTL 1 day
- `archive/` — expired / superseded entries, never pruned

## Universal Layer 0 entries (inherited by reference)

These are not duplicated here — they live at `~/.claude/docs/superpowers/research/`
and apply to every project on this machine:

- Universal R8 sota cache — see Layer 0 addendum for the current list

## Project-specific entries

*(none yet — Phase 4 may add project-specific seeds based on bootstrap_intent.md)*
```

### Step 2.3 — Copy stack-relevant entries from the Genesis plugin's own cache

The Genesis plugin ships its own R8 cache at `<plugin-root>/.claude/docs/superpowers/research/` — where `<plugin-root>` is derived via the same "three levels up from `skills/genesis-protocol/SKILL.md`" rule used at Phase 1 Step 1.3. This cache contains entries that are also relevant to any downstream project, specifically the ones about Claude Code itself (plugin structure, session JSONL format, in-IDE tools, cross-OS ecosystem). Phase 2 **copies** these entries — not by-reference, because they are project-level references the downstream project needs to read offline.

These entries apply to any Claude Code project, plugin or not — a non-plugin downstream still benefits from understanding plugin structure (the SKILL.md it already has inherited from Genesis uses plugin conventions), the JSONL session format (for `session-post-processor` to run), and the SPDX header rule (enforced by R10). No branching on `is-a-plugin` at this step.

Entries to copy (subject to availability and TTL):

| Source | Destination | Why copy not link |
|---|---|---|
| `sota/claude-code-plugin-distribution_*.md` | `sota/` in downstream | Every Genesis downstream may ship as a plugin — needs local reference |
| `stack/claude-code-plugin-structure_*.md` | `stack/` in downstream | Same reason — plugin structure is consumed at every session |
| `stack/claude-code-session-jsonl-format_*.md` | `stack/` in downstream | Needed for `session-post-processor` to run on the downstream's sessions |
| `sota/claude-ecosystem-cross-os_*.md` | `sota/` in downstream | Multidevice refs used by Phase -1 and Phase 7 across OS |
| `sota/spdx-headers_*.md` | `sota/` in downstream | SPDX rule is enforced in R10 — the reference must be local |

Each copied entry has its `expires_at` frontmatter preserved — the downstream project inherits the original TTL. If the entry has already expired by the time Phase 2 runs, **archive** the source (via Genesis-side R8 maintenance) before copying, never copy a stale entry.

### Step 2.4 — Update `INDEX.md` with the copied entries

After Step 2.3, update `INDEX.md` to list the five (or fewer, if some were skipped as stale) copied entries under a new "Stack-relevant inherited entries" section. Each line: `- [<title>](path) — expires <YYYY-MM-DD>`.

## Exit condition

Phase 1 + Phase 2 are complete when:

- `memory/MEMORY.md` exists and lists all eight memory subtrees as one-line index entries.
- `memory/master.md` exists as a placeholder (Phase 4 populates it with the real vision).
- `CLAUDE.md` exists at the target folder root with Layer 0 inheritance and project-specific pointers.
- `.claude/docs/superpowers/rules/v1_rules.md` is present (copied verbatim from the Genesis plugin).
- `memory/journal/INDEX.md`, `memory/pepites/INDEX.md`, `memory/project/sessions/INDEX.md` all exist via the sibling install-manifests.
- `.claude/docs/superpowers/research/INDEX.md` exists with the TTL policy + universal + stack-relevant sections populated.
- At least the five canonical stack-relevant cache entries (or their current non-expired equivalents) are present under `.claude/docs/superpowers/research/sota/` and `.../stack/`.

## Common failures

- **Sibling install-manifest verification fails** — stop immediately. Surface the failing check and ask the user to inspect the sibling skill. Do not silently retry.
- **Rules file missing in the Genesis plugin** — stop. Means the Genesis plugin is not installed correctly. Surface the path that was expected and the path that was found.
- **Target folder lacks write permission** — stop. Surface the exact file that could not be written. Do not retry with sudo or elevated permissions.
- **An R8 source entry has expired** — do not copy. Instead, surface the gap in the genesis report at the end, and recommend refreshing the entry in the next session before relying on it.

## Anti-Frankenstein reminders

- **Do not merge sibling install-manifests into this runbook.** Each sibling owns its install logic. Phase 1 calls them — it never duplicates them.
- **Do not write project-specific content during Phase 1 or Phase 2.** Project specifics (master vision, README, stubs) are Phase 4. Phase 1 is scaffold-only; Phase 2 is cache-only.
- **Do not auto-populate `memory/themes/`, `memory/user/`, or `memory/feedback/` with content.** Each starts with only a README.md explaining its role. Content accumulates across real sessions.
- **Do not skip any install-manifest invocation for speed.** All four run, every time. The idempotency rule lets them be safely re-run on partial bootstraps.
- **Do not auto-copy every entry from the Genesis plugin's R8 cache.** Only the five stack-relevant entries listed in Step 2.3. Universal entries stay in Layer 0 and are inherited by reference.
- **If the user says `frankenstein`**, back out of the last install-manifest invocation and pause.
