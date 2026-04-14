<!-- SPDX-License-Identifier: MIT -->
---
name: Project Genesis working rules v1
description: Rule set R1-R10 for the Project Genesis plugin repo, adapted from Aurum v1 rules per the Étape 2 scoreboard; inherits R8 and R9 (and all Layer 0 universal rules) from ~/.claude/CLAUDE.md by reference
version: 1.0
frozen_at: 2026-04-14
supersedes: null
---

# Project Genesis — Working Rules v1

These rules govern every session on the Project Genesis plugin repo. They are stricter than Claude Code defaults and take precedence.

## Inheritance from Layer 0 universal

All universal rules, user profile, hard rules, workflow patterns, and machine-specific reference are **inherited by reference** from `~/.claude/CLAUDE.md`. This file does NOT duplicate Layer 0. Read Layer 0 directly for:

- User profile (identity, language, working style, AI stack)
- Hard rules (additive auth, no new windows, R2.1 close-pressure discipline, R9 language policy, async mid-flow questions)
- Workflow patterns (per-project SSH identity, GH_TOKEN env override, fine-grained PAT scope checklist, R8 research cache, best-practice-at-date default, anti-Frankenstein, cross-project research sharing, pépite discovery routing)
- Journal system (6th memory type, trigger phrases, stratified dialogue format)
- Machine-specific Chrome profiles mapping

The rules below are **project-specific** to Genesis or **adaptations** of Aurum v1 rules. Where a rule is inherited unchanged from Layer 0, this file says so explicitly and points to Layer 0.

---

## R1 — Session lifecycle

### R1.1 Open ritual (every session, in order)

1. Read today's **absolute** date
2. Read `memory/MEMORY.md` + `memory/master.md` + any theme memory relevant to the planned work
3. Verify `main` is clean: `git status -s` must return empty — if not, investigate before any new work
4. Read the most recent file in `.claude/docs/superpowers/resume/` to pick up the previous session's handoff
5. Scan `.claude/docs/superpowers/research/INDEX.md`: for every entry, if `expires_at < today` move to `research/archive/`, mark `status: deprecated`, update the index
6. Quick stack check — any critical package / MCP changelogs since last session per R8 TTL rules
7. Create the session worktree per R2 **before any Edit/Write**

### R1.2 Execution mode

Inherited from Layer 0:
- Default: step-by-step with explicit validation between steps
- Keyword `autonome` / `termine tout` → chain steps without checkpoint until the next natural boundary
- Keyword `pause` → stop immediately, even mid-step, and return control

### R1.3 Close ritual (`fin de session`)

1. Commit cleanly on the session branch (inside the worktree, NEVER in root — the only R2.1 exception is the very first bootstrap commit)
2. Open a PR via `GH_TOKEN="$GH_TOKEN" gh pr create` (env override — never `gh auth login`)
3. Squash-merge via `GH_TOKEN="$GH_TOKEN" gh pr merge --squash` **without** `--delete-branch`
4. **Genesis-specific**: if the PR bumps the plugin version, update `plugin.json` `version` field in the same PR and tag the squashed merge commit with `v<semver>` after merge
5. Run the memory hygiene routine (R4.4)
6. Write the next resume prompt under `.claude/docs/superpowers/resume/YYYY-MM-DD_<slug>.md`
7. Deliver the exact phrase the user should say to resume next session
8. Goodbye card summarizing what changed, including updated self-ratings per R10.3

### R1.4 Close-pressure discipline (inherited from Layer 0)

If the close ritual is blocked by an external failure (gh CLI rate limit, PAT scope missing, network down), **do NOT bypass R2.1 with local git operations in the parent repo root**. Push the branch (SSH works even when the gh API doesn't), update the next session's resume prompt to make the merge the first concrete action, note the blocker, and present the goodbye card reflecting the actual state. No `Rx exception` rationalizations.

---

## R2 — Worktree & branch discipline (KEEP intégral)

Inherited verbatim from Aurum v1 and Layer 0. Universal pattern, no Genesis-specific adaptation.

### R2.1 Worktree creation (mandatory, every session, before any write)

```bash
git clone . .claude/worktrees/<type>_YYYY-MM-DD_<theme>
cd .claude/worktrees/<type>_YYYY-MM-DD_<theme>
git checkout -b <type>/YYYY-MM-DD_<theme>
git remote set-url origin git@github.com-genesis:myconciergerie-prog/project-genesis.git
```

**Forbidden**:
- `git worktree add`
- The `EnterWorktree` Claude Code tool
- Any `Edit` or `Write` directly in the repo root

**The one documented exception**: the very first commit of this repo — `bootstrap: project-genesis v0.1.0 scaffold` on 2026-04-14 — which `git init`s the root before worktrees can exist. Every commit after that is worktree-origin.

### R2.2 Branch types

- `feat/<slug>` — new feature (e.g. `feat/2026-04-15_phase-minus-one-skill`)
- `fix/<slug>` — bug fix
- `chore/<slug>` — infra, CI, docs, tooling
- `spike/<slug>` — throwaway exploration, not intended to merge

### R2.3 PR & merge

- PR via `GH_TOKEN="$GH_TOKEN" gh pr create` (env override — never `gh auth login`)
- Merge via `GH_TOKEN="$GH_TOKEN" gh pr merge --squash` **without** `--delete-branch`
- **Forbidden**: direct push to `main`, `--no-verify`, `--no-gpg-sign`, force-push on any protected branch

### R2.4 PR granularity

**One PR per skill** or per coherent feature for Genesis work. `chore/` PRs (docs, internal cleanups, CI) can merge at end of session even if small. Spike PRs are never merged — delete their branches on origin after the spike concludes, but keep the worktree per R2.5.

### R2.5 Worktree retention

**Never `rm -rf` a worktree after merge.** Forensic snapshots stay on local disk indefinitely. `.claude/worktrees/` is gitignored per `.gitignore` so worktrees never pollute the repo.

---

## R3 — Deploy pipeline (ADAPT — plugin release, not OVH)

Genesis is a Claude Code plugin, not a web product. The "deploy pipeline" is the release chain from `main` to installed plugin:

1. **Worktree PR** receives a merge that bumps `plugin.json` `version` field (semver)
2. **Squash merge** to `main` via `gh pr merge --squash` (R2.3)
3. **Git tag** `v<semver>` on the squashed merge commit
4. **Optional** `GH_TOKEN="$GH_TOKEN" gh release create v<semver>` with a CHANGELOG extract as release notes
5. **CHANGELOG.md** gets a new version entry with the 5-axis self-rating block (per R10.3)
6. **Self-hosted marketplace manifest** (when v1.0.0 ships) is updated to reference the new tag
7. Users who installed via `/plugin install project-genesis@myconciergerie-prog/project-genesis` receive the update on their next Claude Code session

**No GitHub Actions deploy, no OVH, no Supabase Edge Functions** — those are Aurum-specific. Genesis has no server-side runtime.

### R3.1 Version naming

- `0.x.y` — pre-release, scaffold, experimental content (v0.1.0 is the current scaffold)
- `1.x.y` — stable plugin, installable
- Major bumps: breaking changes to skill interfaces or plugin manifest
- Minor bumps: new skills, new features, backward-compatible
- Patch bumps: bug fixes, doc updates, rule clarifications

### R3.2 Rating gate on stable tags

**Versions rated < 7.0/10 on the 5-axis rubric cannot be tagged as stable `1.x.y`.** Use `0.x.y` for anything below the 7.0 threshold. This is the gate that prevents shipping an incomplete v1 under the marketing banner of "v1".

### R3.3 Forbidden

- Publishing a version without updating CHANGELOG.md + self-rating block
- Tagging a version without a corresponding `plugin.json` version bump in the same PR
- Skipping CHANGELOG entries for any merged PR (however small)

---

## R4 — Memory (ADAPT — 7 types, with journal and pépites)

### R4.1 Architecture

```
memory/
├── MEMORY.md           ← index, always loaded at session open per R1.1
├── master.md           ← stable vision + stack + rules summary
├── user/               ← project-scoped user notes (most profile in Layer 0)
├── feedback/           ← project-scoped collaboration rules (most rules in Layer 0)
├── project/            ← ongoing state, decisions, incidents, session history
├── reference/          ← external systems & accounts for this project
├── themes/             ← per-topic memory, populated as the project grows
├── journal/            ← stratified thought capture (6th type, Layer 0 journal system spec)
└── pepites/            ← gold nugget discoveries with cross-project routing (7th type, specs/v1_pepite_discovery_flagging.md)
```

Two directories new compared to Aurum v1: `journal/` (6th type, inherited from Layer 0 journal spec) and `pepites/` (7th type, new in Genesis v1).

### R4.2 File format

```markdown
<!-- SPDX-License-Identifier: MIT -->
---
name: <title>
description: <one line, specific — used to judge relevance later>
type: user | feedback | project | reference | theme | journal | pepite
---

<body>
```

For `feedback` and `project` types: body must include `**Why:**` and `**How to apply:**` sections per Layer 0 R4.3 inheritance.

For `journal` type: body uses the stratified dialogue format per Layer 0 journal system spec. May contain near-verbatim dialogue without `**Why:**` / `**How to apply:**` — journal entries are moment-preserving, not behavior-directing.

For `pepite` type: body follows the format in `specs/v1_pepite_discovery_flagging.md` with `relevance` frontmatter holding the routing metadata.

### R4.3 Content rules (inherited from Layer 0 / Aurum v1)

- **Never pin commit hashes, version numbers, or fragile values** — reference them indirectly via branch names or "latest" markers
- **Always convert relative dates to absolute ISO** (`jeudi` → `2026-04-16`)
- **Feedback and project entries** include `**Why:**` (source / reason, often a past incident) and `**How to apply:**` (trigger conditions)
- **Never write a duplicate** — update an existing entry first
- **SPDX header on every memory file** per R10.2

### R4.4 End-of-session hygiene routine

1. Re-read every memory file touched in the session
2. Purge stale entries (abandoned features, reversed decisions)
3. Merge duplicates
4. Verify `MEMORY.md` stays tight — each entry a one-liner `- [Title](file.md) — hook`
5. Do not write ephemeral session state (plans, in-progress tasks) to memory — those belong in `.claude/docs/superpowers/plans/`

### R4.5 Dev vs runtime memory — N/A for Genesis

Aurum's R4.5 distinguished dev memory (repo) from runtime memory (Anthropic Memory Stores for the product). Genesis is not a product — only dev memory applies. **R4.5 DROPPED** for Genesis.

---

## R5 — Documentation & artefacts (ADAPT — dual-layer for plugin + dev docs)

### R5.1 Plugin content at repo root

Per Claude Code plugin convention, the following live at the **plugin root**:

- `.claude-plugin/plugin.json` — manifest (**only** file allowed in `.claude-plugin/`)
- `skills/` — skills at root level
- `templates/` — reusable templates shipped to downstream users
- `hooks/hooks.json` — auto-loaded hooks (when present)
- `agents/` — sub-agents (if/when added)
- `.mcp.json` — MCP server declarations (optional)
- `README.md` — bilingual FR + EN per R9
- `LICENSE` — MIT full text
- `CHANGELOG.md` — version history with 5-axis self-rating blocks per R10.3
- `.gitignore`, `.env.local.example`, `.envrc.example`, `CLAUDE.md`

### R5.2 Internal dev docs in `.claude/docs/superpowers/`

Development-internal documentation (not shipped with the plugin) lives in:

```
.claude/docs/superpowers/
├── plans/       ← multi-step implementation plans + archived bootstrap config
├── specs/       ← technical / design specs from the v1 bootstrap session
├── research/    ← R8 research cache with TTL
├── resume/      ← session resume prompts
├── rules/       ← this file and its successors
└── templates/   ← dev-internal templates (distinct from the shipped `templates/`)
```

The two locations **coexist without overlap**. Plugin content at root is what users consume; internal docs under `.claude/docs/superpowers/` are what maintainers work with.

### R5.3 No `docs/` at repo root

**Forbidden** — would collide with common absolute-path assumptions pointing at `main`. All documentation goes through the two locations above. All dated artefacts use `YYYY-MM-DD_<slug>.md`.

---

## R6 — Sub-agents & parallelism (ADAPT — drop R6.3 Managed Agents)

### R6.1 Two tools for Genesis

- **Claude Code sub-agents** (`Agent` tool) — dev-time work ON Genesis: research, parallel exploration, parallel edits, review
- **Messages API** — short reactive tasks (classify, reformulate, sub-second tool-use) if ever needed

**Dropped from Aurum's R6.1**: Managed Agents API (that's product-runtime, Aurum-specific). Genesis has no product runtime — it's a dev tool plugin.

### R6.2 Parallelism (inherited from Aurum v1)

Prefer N sub-agents editing N small files over one agent editing a monolith. Dispatch in parallel for independent work. Token spend is not a constraint when it buys real value.

### R6.3 Managed Agents — DROPPED

Aurum's R6.3 sub-rules on backend routing, aggressive termination, single-level delegation, cache-hit discipline, and budget kill switch are all product-runtime concerns. Genesis is not a product and has no runtime agents. **R6.3 dropped entirely.**

---

## R7 — Multi-backend via MCP (BYO-AI) — DROPPED

Purely Aurum-runtime. Genesis doesn't route AI calls at runtime because Genesis is itself a Claude Code plugin — it runs inside Claude Code's session, not in a service backend.

**R7 is dropped entirely for Genesis.** If Genesis ever generates code that uses AI in a downstream project, the generated code inherits the Layer 0 best-practice-at-date rule (which surfaces multi-LLM routing patterns via research), not a hard rule mandating it.

---

## R8 — Research cache with TTL — INHERIT from Layer 0

See `~/.claude/CLAUDE.md` "R8 — Research cache with TTL" section. Applied verbatim to Genesis's own `research/` folder at `.claude/docs/superpowers/research/`. Entries from the bootstrap session live under `sota/` and `stack/`:

| Entry | Type | Expires |
|---|---|---|
| `open-source-license-for-dev-tooling_2026-04-14.md` | sota | 2026-04-21 |
| `claude-code-plugin-distribution_2026-04-14.md` | sota | 2026-04-21 |
| `spdx-headers_2026-04-14.md` | sota | 2026-04-21 |
| `claude-in-ide-tools_2026-04-15.md` | sota | 2026-04-22 |
| `claude-ecosystem-cross-os_2026-04-15.md` | sota | 2026-04-22 |
| `claude-code-plugin-structure_2026-04-14.md` | stack | 2026-04-15 |
| `claude-code-session-jsonl-format_2026-04-14.md` | stack | 2026-04-15 |

R1.1 step 5 runs the TTL scan at every session open.

---

## R9 — Language policy — INHERIT from Layer 0

See `~/.claude/CLAUDE.md` "R9 — Language policy (three tiers, no exceptions)".

Applied to Genesis:
- **Dev & tooling** (this file, all memory, internal docs, commit messages, branch names, source code in skills): English only
- **Production docs** (`README.md`, `CHANGELOG.md` structure, public changelog entries): bilingual FR + EN
- **App runtime**: N/A for Genesis (no runtime)

---

## R10 — Plugin conventions & self-rating discipline (NEW)

### R10.1 Plugin convention compliance

The repo must remain a valid Claude Code plugin at every commit:

- `.claude-plugin/plugin.json` exists and has required fields (`name`, `version`, `description`, `license`)
- Skills, commands, hooks, agents live at **plugin root** level (NEVER inside `.claude-plugin/`)
- The plugin is installable via `/plugin install project-genesis@myconciergerie-prog/project-genesis` once v1.0.0 ships
- `plugin.json` version bumps follow semver and align with git tags

### R10.2 SPDX headers on every source file

Every source file (`.py`, `.md`, `.sh`, `.ps1`, `.yaml`, `.yml`, `.js`, `.ts`) carries `SPDX-License-Identifier: MIT` in a comment on line 1 (or line 2 after a shebang). Comment syntax per file type:

- Python / shell / YAML: `# SPDX-License-Identifier: MIT`
- Markdown: `<!-- SPDX-License-Identifier: MIT -->`
- JavaScript / TypeScript: `// SPDX-License-Identifier: MIT`
- JSON (no comments supported): coverage via manifest-level `license` field in `plugin.json`, `package.json`, etc.

`LICENSE` at repo root holds the full MIT text. The SPDX + LICENSE combination is the canonical 2026 approach per Linux Foundation guidance, surfaced in research `sota/spdx-headers_2026-04-14.md`.

### R10.3 Self-rating at every version bump

Every `plugin.json` version bump requires a `CHANGELOG.md` entry with a **5-axis self-rating block**:

| Axis | Question |
|---|---|
| **Pain-driven coverage** | Does every feature point to a documented pain? |
| **Prose cleanliness** | Is the prose clear, no redundancy, no jargon bloat? |
| **Best-at-date alignment** | Are the tech / patterns / licenses all SOTA per research? |
| **Self-contained** | Can a new user apply the version without reading Aurum or Layer 0 extensively? |
| **Anti-Frankenstein** | Zero speculative features, every addition justified? |

Rate 1-10 per axis, average for the overall score. **Average must be < 10.** Target for v1.0.0 is **8.5/10**. Versions rated **< 7.0/10 cannot be tagged as stable `1.x.y`** per R3.2.

### R10.4 Anti-Frankenstein gate (inherited from Layer 0 + enforced project-specifically)

Any feature proposed for a new PR must point to a **documented pain point**:

- Aurum v0_init feedback memory entry
- User request in this session or a prior session
- Live dogfooding friction observed in real time
- A Genesis spec file in `.claude/docs/superpowers/specs/`

**Speculative features rejected by default.** If the user says the literal word `frankenstein` during any session, the current proposal is dropped immediately, the session backs out to the last stable point, and simplification begins.

Three similar lines is better than a premature abstraction. No half-finished implementations. No speculative abstractions for "future flexibility". No feature flags for hypothetical forks. No i18n for internal-only strings. No tests for code that doesn't exist yet.

### R10.5 Pépite discovery discipline

Per `.claude/docs/superpowers/specs/v1_pepite_discovery_flagging.md`:

- Research done during Genesis work that meets the **red-light criteria** (two or more of 6 conditions) must be captured as a pépite entry in `memory/pepites/` with routing metadata
- **Cross-project propagation** requires explicit user consent per invocation
- Pépites are **surfaced at next natural conversation boundary**, not interrupting current tool batches
- Users have the final say — pépites are proposed, never imposed

---

## R-secrets — Secret handling (INHERIT from Layer 0)

Layer 0 covers additive auth, GH_TOKEN env pattern, SSH per-project identity, never-log-out rule. See `~/.claude/CLAUDE.md` R-secrets section and related Hard rules.

Genesis-specific application:

- `.env.local` holds `GH_TOKEN=github_pat_...` — gitignored from first commit, never committed
- SSH handles git operations via `github.com-genesis` alias
- `GH_TOKEN` handles API operations via env override (`GH_TOKEN="$GH_TOKEN" gh <cmd>`)
- **Never** `gh auth login` for Genesis work — that would switch the global `gh` auth

## How to propose a rule change

Any rule change goes through a **PR on this file**, with a `**Why:**` section in the commit message describing what triggered the change. Rules are versioned (`v1_rules.md`, `v2_rules.md`, ...) — archive old version, don't silently rewrite. The Aurum pattern applies verbatim: calm-moment rule freezing, stress-moment rule honoring.
